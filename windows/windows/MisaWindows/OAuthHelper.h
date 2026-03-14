#pragma once

#include "pch.h"
#include "codegen/NativeOAuthHelperSpec.g.h"
#include <NativeModules.h>

namespace winrt::MisaWindows {

REACT_MODULE(OAuthHelper)
struct OAuthHelper {
  using ModuleSpec = MisaOAuthHelperCodegen::OAuthHelperSpec;

  REACT_SYNC_METHOD(getPendingOAuthUrl)
  std::optional<std::string> getPendingOAuthUrl() noexcept;
};

}  // namespace winrt::MisaWindows
