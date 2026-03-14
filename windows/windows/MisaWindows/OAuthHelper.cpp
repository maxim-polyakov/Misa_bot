#include "pch.h"
#include "OAuthHelper.h"

namespace winrt::MisaWindows {

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
  if (!ReadFile(h, content.data(), size, &read, NULL) || read != size) {
    CloseHandle(h);
    return std::nullopt;
  }
  CloseHandle(h);

  DeleteFileW(filePath.c_str());

  return content;
}

}  // namespace winrt::MisaWindows
