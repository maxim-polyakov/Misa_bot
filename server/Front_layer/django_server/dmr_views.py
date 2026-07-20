import json
from http import HTTPStatus
from typing import Any

from django.conf import settings
from django.http import HttpResponse
from dmr import Body, Controller, ResponseSpec, validate
from dmr.plugins.msgspec import MsgspecSerializer

from Core_layer.Controller_package.Classes import Controller as CoreController
from . import og_preview
from .dmr_schemas import (
    ApiEnvelope,
    ChatCreateBody,
    ChatTitleBody,
    EmailOnlyBody,
    EmailPasswordBody,
    ForgotPasswordVerifyBody,
    GoogleIdTokenBody,
    MessageFeedbackBody,
    OAuthTokenResponse,
    RegisterVerifyBody,
    UiLocaleBody,
)
from .views import _normalize_ui_locale_code


_ENVELOPE_RESPONSES = (
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.OK),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.CREATED),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.BAD_REQUEST),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.UNAUTHORIZED),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.FORBIDDEN),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.NOT_FOUND),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.CONFLICT),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.INTERNAL_SERVER_ERROR),
)
_ERROR_ENVELOPE_RESPONSES = (
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.BAD_REQUEST),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.UNAUTHORIZED),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.FORBIDDEN),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.NOT_FOUND),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.CONFLICT),
    ResponseSpec(ApiEnvelope, status_code=HTTPStatus.INTERNAL_SERVER_ERROR),
)


class _BaseController(Controller[MsgspecSerializer]):
    """DMR adapter around the existing Core controller methods."""

    def _core(self) -> CoreController.Controller:
        return CoreController.Controller()

    def _from_django_response(self, response) -> HttpResponse:
        try:
            payload: Any = json.loads(response.content.decode(response.charset or "utf-8"))
        except (AttributeError, UnicodeDecodeError, json.JSONDecodeError):
            payload = response.content.decode(getattr(response, "charset", "utf-8"), errors="replace")
        return self.to_response(payload, status_code=HTTPStatus(response.status_code))

    def _call_core(self, method_name: str, *args) -> HttpResponse:
        response = getattr(self._core(), method_name)(self.request, *args)
        return self._from_django_response(response)


class RegisterController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def post(self, parsed_body: Body[EmailPasswordBody]) -> HttpResponse:
        return self._call_core("register")


class RegisterSendCodeController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def post(self, parsed_body: Body[EmailPasswordBody]) -> HttpResponse:
        return self._call_core("register_send_code")


class RegisterVerifyController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def post(self, parsed_body: Body[RegisterVerifyBody]) -> HttpResponse:
        return self._call_core("register_verify")


class ForgotPasswordSendCodeController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def post(self, parsed_body: Body[EmailOnlyBody]) -> HttpResponse:
        return self._call_core("forgot_password_send_code")


class ForgotPasswordVerifyController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def post(self, parsed_body: Body[ForgotPasswordVerifyBody]) -> HttpResponse:
        return self._call_core("forgot_password_verify")


class LoginController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def post(self, parsed_body: Body[EmailPasswordBody]) -> HttpResponse:
        return self._call_core("login_view")


class OAuthTokenController(_BaseController):
    @validate(
        ResponseSpec(OAuthTokenResponse, status_code=HTTPStatus.OK),
        *_ERROR_ENVELOPE_RESPONSES,
    )
    def get(self) -> HttpResponse:
        return self._call_core("oauth_token")


class GoogleIdTokenController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def post(self, parsed_body: Body[GoogleIdTokenBody]) -> HttpResponse:
        return self._call_core("google_id_token")


class CheckController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def get(self) -> HttpResponse:
        return self._call_core("check")


class LogoutAllController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def post(self) -> HttpResponse:
        return self._call_core("logout_all")


class DeleteAccountController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def post(self) -> HttpResponse:
        return self._call_core("delete_account")


class ChatsController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def get(self) -> HttpResponse:
        return self._call_core("chats_list")

    @validate(*_ENVELOPE_RESPONSES)
    def post(self, parsed_body: Body[ChatCreateBody]) -> HttpResponse:
        return self._call_core("chats_create")


class ChatsExportController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def get(self) -> HttpResponse:
        return self._call_core("chats_export")


class ChatSharePublicController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def get(self) -> HttpResponse:
        chat_id = self.kwargs["chat_id"]
        return self._call_core("chats_share_public", chat_id)


class ChatMessagesController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def get(self) -> HttpResponse:
        chat_id = self.kwargs["chat_id"]
        return self._call_core("chats_messages", chat_id)


class ChatMessageFeedbackController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def patch(self, parsed_body: Body[MessageFeedbackBody]) -> HttpResponse:
        chat_id = self.kwargs["chat_id"]
        message_id = self.kwargs["message_id"]
        return self._call_core("chats_message_feedback", chat_id, message_id)


class ChatClearMessagesController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def delete(self) -> HttpResponse:
        chat_id = self.kwargs["chat_id"]
        return self._call_core("chats_clear_messages", chat_id)


class ChatUpdateController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def patch(self, parsed_body: Body[ChatTitleBody]) -> HttpResponse:
        chat_id = self.kwargs["chat_id"]
        return self._call_core("chats_update_title", chat_id)


class ChatDeleteController(_BaseController):
    @validate(*_ENVELOPE_RESPONSES)
    def delete(self) -> HttpResponse:
        chat_id = self.kwargs["chat_id"]
        return self._call_core("chats_delete", chat_id)


class UiLocaleController(Controller[MsgspecSerializer]):
    @validate(
        ResponseSpec(dict[str, Any], status_code=HTTPStatus.OK),
        ResponseSpec(dict[str, Any], status_code=HTTPStatus.BAD_REQUEST),
    )
    def post(self, parsed_body: Body[UiLocaleBody]) -> HttpResponse:
        raw = parsed_body.locale or parsed_body.lang or ""
        code = _normalize_ui_locale_code(raw)
        if not code:
            return self.to_response(
                {"ok": False, "error": "invalid or missing locale"},
                status_code=HTTPStatus.BAD_REQUEST,
            )

        response = self.to_response({"ok": True, "locale": code}, status_code=HTTPStatus.OK)
        domain = getattr(settings, "UI_LOCALE_COOKIE_DOMAIN", None) or None
        if isinstance(domain, str):
            domain = domain.strip() or None
        response.set_cookie(
            "misa_locale",
            code,
            max_age=31536000,
            path="/",
            samesite="Lax",
            domain=domain,
            secure=self.request.is_secure(),
        )
        return response


class SpaOgPreviewController(Controller[MsgspecSerializer]):
    @validate(ResponseSpec(dict[str, str], status_code=HTTPStatus.OK))
    def get(self) -> HttpResponse:
        locale = _normalize_ui_locale_code(self.request.COOKIES.get("misa_locale", ""))
        if not locale:
            locale = _normalize_ui_locale_code(self.request.headers.get("Accept-Language", ""))
        tagline = og_preview.TAGLINES.get(locale or "en", og_preview.TAGLINES["en"])
        return self.to_response({"tagline": tagline}, status_code=HTTPStatus.OK)
