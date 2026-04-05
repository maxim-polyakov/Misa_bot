
/*
 * This file is auto-generated from a NativeModule spec file in js.
 *
 * This is a C++ Spec class that should be used with MakeTurboModuleProvider to register native modules
 * in a way that also verifies at compile time that the native module matches the interface required
 * by the TurboModule JS spec.
 */
#pragma once
// clang-format off


#include <NativeModules.h>
#include <tuple>

namespace MisaOAuthHelperCodegen {

struct OAuthHelperSpec : winrt::Microsoft::ReactNative::TurboModuleSpec {
  static constexpr auto methods = std::tuple{
      SyncMethod<std::optional<std::string>() noexcept>{0, L"getPendingOAuthUrl"},
      Method<void(std::string, std::string, Promise<std::string>) noexcept>{1, L"saveExportZipBase64"},
  };

  template <class TModule>
  static constexpr void ValidateModule() noexcept {
    constexpr auto methodCheckResults = CheckMethods<TModule, OAuthHelperSpec>();

    REACT_SHOW_METHOD_SPEC_ERRORS(
          0,
          "getPendingOAuthUrl",
          "    REACT_SYNC_METHOD(getPendingOAuthUrl) std::optional<std::string> getPendingOAuthUrl() noexcept { /* implementation */ }\n"
          "    REACT_SYNC_METHOD(getPendingOAuthUrl) static std::optional<std::string> getPendingOAuthUrl() noexcept { /* implementation */ }\n");
    REACT_SHOW_METHOD_SPEC_ERRORS(
          1,
          "saveExportZipBase64",
          "    REACT_METHOD(saveExportZipBase64) void saveExportZipBase64(std::string base64, std::string fileName, ::React::ReactPromise<std::string> &&result) noexcept { /* implementation */ }\n"
          "    REACT_METHOD(saveExportZipBase64) static void saveExportZipBase64(std::string base64, std::string fileName, ::React::ReactPromise<std::string> &&result) noexcept { /* implementation */ }\n");
  }
};

} // namespace MisaOAuthHelperCodegen
