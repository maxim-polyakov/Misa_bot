#include "pch.h"
#include "OAuthHelper.h"

#include <Shobjidl.h>
#include <vector>
#include <Wincrypt.h>

#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Storage.h>
#include <winrt/Windows.Storage.Pickers.h>

#pragma comment(lib, "Crypt32.lib")

namespace winrt::MisaWindows {

namespace {

bool IsValidExportFileName(const std::string &name) noexcept {
  if (name.size() < 5 || name.size() > 220) return false;
  if (name.compare(name.size() - 4, 4, ".zip") != 0) return false;
  for (unsigned char c : name) {
    if (c >= 'a' && c <= 'z') continue;
    if (c >= 'A' && c <= 'Z') continue;
    if (c >= '0' && c <= '9') continue;
    if (c == '.' || c == '-' || c == '_') continue;
    return false;
  }
  return true;
}

bool DecodeBase64ToBytes(const std::string &b64, std::vector<uint8_t> &out) noexcept {
  DWORD cb = 0;
  if (!CryptStringToBinaryA(
          b64.c_str(), static_cast<DWORD>(b64.size()), CRYPT_STRING_BASE64, nullptr, &cb, nullptr, nullptr))
    return false;
  out.resize(cb);
  return CryptStringToBinaryA(
             b64.c_str(),
             static_cast<DWORD>(b64.size()),
             CRYPT_STRING_BASE64,
             out.data(),
             &cb,
             nullptr,
             nullptr) != FALSE;
}

}  // namespace

void OAuthHelper::Initialize(winrt::Microsoft::ReactNative::ReactContext const &reactContext) noexcept {
  m_reactContext = reactContext;
}

static std::string WidePathToUtf8(std::wstring_view wpath) noexcept {
  int pathLen = WideCharToMultiByte(CP_UTF8, 0, wpath.data(), static_cast<int>(wpath.size()), nullptr, 0, nullptr, nullptr);
  if (pathLen <= 0) return {};
  std::string utf8(static_cast<size_t>(pathLen), '\0');
  WideCharToMultiByte(CP_UTF8, 0, wpath.data(), static_cast<int>(wpath.size()), utf8.data(), pathLen, nullptr, nullptr);
  return utf8;
}

void OAuthHelper::saveExportZipBase64(
    std::string base64, std::string fileName, ::React::ReactPromise<std::string> &&result) noexcept {
  if (!IsValidExportFileName(fileName)) {
    result.Reject("Invalid file name");
    return;
  }
  std::vector<uint8_t> bytes;
  if (!DecodeBase64ToBytes(base64, bytes)) {
    result.Reject("Invalid base64");
    return;
  }
  if (!m_reactContext) {
    result.Reject("React context not ready");
    return;
  }

  auto reactContext = m_reactContext;
  reactContext.UIDispatcher().Post([reactContext, bytes = std::move(bytes), fileName = std::move(fileName), result = std::move(result)]() mutable {
    // Main window title is set in MisaWindows.cpp (AppWindow.Title). ReactCoreInjection.h is not on the app project's include path.
    HWND hwnd = FindWindowW(nullptr, L"Misa AI");

    using winrt::Windows::Storage::Pickers::FileSavePicker;
    using winrt::Windows::Storage::Pickers::PickerLocationId;
    FileSavePicker picker;
    picker.SuggestedStartLocation(PickerLocationId::DocumentsLibrary);
    std::wstring wFileName(fileName.begin(), fileName.end());
    std::wstring suggested = wFileName;
    if (suggested.size() > 4 && suggested.compare(suggested.size() - 4, 4, L".zip") == 0) {
      suggested.erase(suggested.size() - 4, 4);
    }
    picker.SuggestedFileName(suggested);
    picker.FileTypeChoices().Insert(L"ZIP archive", winrt::single_threaded_vector<winrt::hstring>({L".zip"}));

    if (hwnd) {
      if (auto init = picker.try_as<IInitializeWithWindow>()) {
        init->Initialize(hwnd);
      }
    }

    auto pickOp = picker.PickSaveFileAsync();
    pickOp.Completed([reactContext, bytes = std::move(bytes), result = std::move(result)](auto &&op, winrt::AsyncStatus status) mutable {
      if (status != winrt::AsyncStatus::Completed) {
        reactContext.JSDispatcher().Post([result = std::move(result)]() mutable { result.Reject("Save dialog failed"); });
        return;
      }
      auto file = op.GetResults();
      if (!file) {
        reactContext.JSDispatcher().Post([result = std::move(result)]() mutable { result.Reject("Cancelled"); });
        return;
      }

      winrt::array_view<const uint8_t> view;
      if (!bytes.empty()) {
        view = winrt::array_view<const uint8_t>(bytes.data(), bytes.data() + bytes.size());
      }

      auto writeOp = winrt::Windows::Storage::FileIO::WriteBytesAsync(file, view);
      writeOp.Completed([reactContext, file, result = std::move(result)](auto &&, winrt::AsyncStatus status2) mutable {
        if (status2 != winrt::AsyncStatus::Completed) {
          reactContext.JSDispatcher().Post([result = std::move(result)]() mutable { result.Reject("Write failed"); });
          return;
        }
        std::wstring wpath(file.Path().c_str());
        std::string utf8Path = WidePathToUtf8(wpath);
        reactContext.JSDispatcher().Post([result = std::move(result), utf8Path = std::move(utf8Path)]() mutable {
          result.Resolve(utf8Path);
        });
      });
    });
  });
}

std::optional<std::string> OAuthHelper::getPendingOAuthUrl() noexcept {
  wchar_t path[MAX_PATH];
  if (FAILED(SHGetFolderPathW(NULL, CSIDL_APPDATA, NULL, 0, path))) return std::nullopt;
  std::wstring filePath(path);
  filePath += L"\\Misa\\pending_oauth.txt";

  HANDLE h = CreateFileW(filePath.c_str(), GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
  if (h == INVALID_HANDLE_VALUE) return std::nullopt;

  DWORD size = GetFileSize(h, NULL);
  if (size == INVALID_FILE_SIZE || size == 0) {
    CloseHandle(h);
    return std::nullopt;
  }

  std::string content(size, 0);
  DWORD read;
  if (!ReadFile(h, content.data(), size, &read, NULL) || read == 0) {
    CloseHandle(h);
    return std::nullopt;
  }
  CloseHandle(h);

  DeleteFileW(filePath.c_str());

  content.resize(read);
  while (!content.empty() && (content.back() == '\r' || content.back() == '\n' || content.back() == ' ' || content.back() == '\t')) content.pop_back();
  if (content.size() >= 3 && (unsigned char)content[0] == 0xEF && (unsigned char)content[1] == 0xBB && (unsigned char)content[2] == 0xBF) content.erase(0, 3);
  if (content.empty() || content.find("misa://") == std::string::npos) return std::nullopt;
  return content;
}

}  // namespace winrt::MisaWindows
