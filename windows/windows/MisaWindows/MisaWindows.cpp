// MisaWindows.cpp : Defines the entry point for the application.
//

#include "pch.h"
#include "MisaWindows.h"

#include "AutolinkedNativeModules.g.h"

#include "OAuthHelper.h"

// A PackageProvider containing any turbo modules you define within this app project
struct CompReactPackageProvider
    : winrt::implements<CompReactPackageProvider, winrt::Microsoft::ReactNative::IReactPackageProvider> {
 public: // IReactPackageProvider
  void CreatePackage(winrt::Microsoft::ReactNative::IReactPackageBuilder const &packageBuilder) noexcept {
    AddAttributedModules(packageBuilder, true);
  }
};

namespace {
constexpr wchar_t kMutexName[] = L"Global\\MisaWindows_SingleInstance_7D8F2E";
constexpr wchar_t kWindowTitle[] = L"Misa AI";

std::wstring GetPendingOAuthPath() {
  wchar_t path[MAX_PATH];
  if (FAILED(SHGetFolderPathW(NULL, CSIDL_APPDATA, NULL, 0, path))) return {};
  std::wstring dir(path);
  dir += L"\\Misa";
  CreateDirectoryW(dir.c_str(), NULL);
  return dir + L"\\pending_oauth.txt";
}

std::wstring ExtractMisaUrlFromCommandLine() {
  LPWSTR cmdLine = GetCommandLineW();
  if (!cmdLine) return {};
  std::wstring s(cmdLine);
  size_t pos = s.find(L"misa://");
  if (pos == std::wstring::npos) return {};
  size_t end = s.find_first_of(L" \t", pos);
  if (end == std::wstring::npos) end = s.length();
  return s.substr(pos, end - pos);
}

bool TrySecondInstanceHandoff() {
  HANDLE mutex = CreateMutexW(NULL, FALSE, kMutexName);
  if (!mutex) return false;
  if (GetLastError() == ERROR_ALREADY_EXISTS) {
    std::wstring url = ExtractMisaUrlFromCommandLine();
    if (!url.empty()) {
      std::wstring path = GetPendingOAuthPath();
      if (!path.empty()) {
        HANDLE h = CreateFileW(path.c_str(), GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        if (h != INVALID_HANDLE_VALUE) {
          int len = WideCharToMultiByte(CP_UTF8, 0, url.c_str(), (int)url.size(), NULL, 0, NULL, NULL);
          if (len > 0) {
            std::string utf8(len, 0);
            WideCharToMultiByte(CP_UTF8, 0, url.c_str(), (int)url.size(), utf8.data(), len, NULL, NULL);
            DWORD written;
            WriteFile(h, utf8.c_str(), (DWORD)utf8.size(), &written, NULL);
          }
          CloseHandle(h);
        }
      }
    }
    HWND hwnd = FindWindowW(NULL, kWindowTitle);
    if (hwnd) {
      SetForegroundWindow(hwnd);
      ShowWindow(hwnd, SW_RESTORE);
    }
    CloseHandle(mutex);
    return true;
  }
  CloseHandle(mutex);
  return false;
}
}  // namespace

// The entry point of the Win32 application
_Use_decl_annotations_ int CALLBACK WinMain(HINSTANCE instance, HINSTANCE, PSTR /* commandLine */, int showCmd) {
  if (TrySecondInstanceHandoff()) return 0;

  // Initialize WinRT
  winrt::init_apartment(winrt::apartment_type::single_threaded);

  // Enable per monitor DPI scaling
  SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2);

  // Find the path hosting the app exe file
  WCHAR appDirectory[MAX_PATH];
  GetModuleFileNameW(NULL, appDirectory, MAX_PATH);
  PathCchRemoveFileSpec(appDirectory, MAX_PATH);

  // Create a ReactNativeWin32App with the ReactNativeAppBuilder
  auto reactNativeWin32App{winrt::Microsoft::ReactNative::ReactNativeAppBuilder().Build()};

  // Configure the initial InstanceSettings for the app's ReactNativeHost
  auto settings{reactNativeWin32App.ReactNativeHost().InstanceSettings()};
  // Register any autolinked native modules
  RegisterAutolinkedNativeModulePackages(settings.PackageProviders());
  // Register any native modules defined within this app project
  settings.PackageProviders().Append(winrt::make<CompReactPackageProvider>());

#if BUNDLE
  // Load the JS bundle from a file (not Metro):
  // Set the path (on disk) where the .bundle file is located
  settings.BundleRootPath(std::wstring(L"file://").append(appDirectory).append(L"\\Bundle\\").c_str());
  // Set the name of the bundle file (without the .bundle extension)
  settings.JavaScriptBundleFile(L"index.windows");
  // Disable hot reload
  settings.UseFastRefresh(false);
#else
  // Load the JS bundle from Metro
  settings.JavaScriptBundleFile(L"index");
  // Enable hot reload
  settings.UseFastRefresh(true);
#endif
#if _DEBUG
  // For Debug builds
  // Enable Direct Debugging of JS
  settings.UseDirectDebugger(true);
  // Enable the Developer Menu
  settings.UseDeveloperSupport(true);
#else
  // For Release builds:
  // Disable Direct Debugging of JS
  settings.UseDirectDebugger(false);
  // Disable the Developer Menu
  settings.UseDeveloperSupport(false);
#endif

  // Get the AppWindow so we can configure its initial title and size
  auto appWindow{reactNativeWin32App.AppWindow()};
  appWindow.Title(L"Misa AI");
  appWindow.Resize({1000, 1000});

  // Get the ReactViewOptions so we can set the initial RN component to load
  auto viewOptions{reactNativeWin32App.ReactViewOptions()};
  viewOptions.ComponentName(L"Misa AI");

  // Start the app
  reactNativeWin32App.Start();
}
