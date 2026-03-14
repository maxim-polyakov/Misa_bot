/**
 * Патчи для совместимости RN 0.76 с RNW canary.
 * Добавляет отсутствующие файлы CdpJson и PerfMonitorV2.
 */
const fs = require('fs');
const path = require('path');

const rnPath = path.join(__dirname, '..', 'node_modules', 'react-native', 'ReactCommon', 'jsinspector-modern');
const cdpPath = path.join(rnPath, 'cdp');

const cdpJsonH = `/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 * Licensed under the MIT License.
 */
#pragma once
#include <folly/dynamic.h>
#include <optional>
#include <string>
#include <string_view>
namespace facebook::react::jsinspector_modern::cdp {
using RequestId = long long;
enum class ErrorCode { ParseError = -32700, InvalidRequest = -32600, MethodNotFound = -32601, InvalidParams = -32602, InternalError = -32603 };
struct PreparsedRequest {
  RequestId id{}; std::string method; folly::dynamic params;
  inline bool operator==(const PreparsedRequest& rhs) const { return id == rhs.id && method == rhs.method && params == rhs.params; }
  std::string toJson() const;
};
PreparsedRequest preparse(std::string_view message);
using TypeError = folly::TypeError;
using ParseError = folly::json::parse_error;
std::string jsonError(std::optional<RequestId> id, ErrorCode code, std::optional<std::string> message = std::nullopt);
std::string jsonResult(RequestId id, const folly::dynamic& result = folly::dynamic::object());
std::string jsonNotification(const std::string& method, std::optional<folly::dynamic> params = std::nullopt);
std::string jsonRequest(RequestId id, const std::string& method, std::optional<folly::dynamic> params = std::nullopt);
}
`;

const cdpJsonCpp = `/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 * Licensed under the MIT license.
 */
#include "CdpJson.h"
#include <folly/json.h>
namespace facebook::react::jsinspector_modern::cdp {
PreparsedRequest preparse(std::string_view message) {
  folly::dynamic parsed = folly::parseJson(message);
  return PreparsedRequest{.id = parsed["id"].getInt(), .method = parsed["method"].getString(), .params = parsed.count("params") != 0u ? parsed["params"] : nullptr};
}
std::string PreparsedRequest::toJson() const {
  folly::dynamic obj = folly::dynamic::object("id", id)("method", method);
  if (params != nullptr) obj["params"] = params;
  return folly::toJson(obj);
}
std::string jsonError(std::optional<RequestId> id, ErrorCode code, std::optional<std::string> message) {
  auto dynamicError = folly::dynamic::object("code", static_cast<int>(code));
  if (message) dynamicError["message"] = *message;
  folly::dynamic result = folly::dynamic::object("error", std::move(dynamicError));
  result["id"] = id ? folly::dynamic(*id) : nullptr;
  return folly::toJson(result);
}
std::string jsonResult(RequestId id, const folly::dynamic& result) { return folly::toJson(folly::dynamic::object("id", id)("result", result)); }
std::string jsonNotification(const std::string& method, std::optional<folly::dynamic> params) {
  auto dynamicNotification = folly::dynamic::object("method", method);
  if (params) dynamicNotification["params"] = *params;
  return folly::toJson(std::move(dynamicNotification));
}
std::string jsonRequest(RequestId id, const std::string& method, std::optional<folly::dynamic> params) {
  auto dynamicRequest = folly::dynamic::object("id", id)("method", method);
  if (params) dynamicRequest["params"] = *params;
  return folly::toJson(std::move(dynamicRequest));
}
}
`;

const perfMonitorStub = `/*
 * Stub for RN 0.76 compatibility with RNW canary.
 */
`;

if (!fs.existsSync(rnPath)) return;
if (!fs.existsSync(cdpPath)) fs.mkdirSync(cdpPath, { recursive: true });
fs.writeFileSync(path.join(cdpPath, 'CdpJson.h'), cdpJsonH);
fs.writeFileSync(path.join(cdpPath, 'CdpJson.cpp'), cdpJsonCpp);
fs.writeFileSync(path.join(rnPath, 'CdpJson.h'), cdpJsonH);
fs.writeFileSync(path.join(rnPath, 'PerfMonitorV2.cpp'), perfMonitorStub);
console.log('RN patches applied (CdpJson, PerfMonitorV2)');
