#pragma once

#include "pch.h"
#include "codegen/NativeOAuthHelperSpec.g.h"
#include <NativeModules.h>

namespace winrt::MisaWindows {

REACT_MODULE(OAuthHelper)
struct OAuthHelper {
  using ModuleSpec = MisaOAuthHelperCodegen::OAuthHelperSpec;

  REACT_INIT(Initialize)
  void Initialize(winrt::Microsoft::ReactNative::ReactContext const &reactContext) noexcept;

  REACT_SYNC_METHOD(getPendingOAuthUrl)
  std::optional<std::string> getPendingOAuthUrl() noexcept;

  REACT_METHOD(saveExportZipBase64)
  void saveExportZipBase64(std::string base64, std::string fileName, ::React::ReactPromise<std::string> &&result) noexcept;

 private:
  winrt::Microsoft::ReactNative::ReactContext m_reactContext{nullptr};
};

}  // namespace winrt::MisaWindows
