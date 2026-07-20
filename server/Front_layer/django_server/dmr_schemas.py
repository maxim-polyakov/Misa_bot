from typing import Any

import msgspec


class ApiEnvelope(msgspec.Struct, kw_only=True):
    status: str
    message: str | None = None
    data: Any = None
    detail: str | None = None


class OAuthTokenResponse(msgspec.Struct, kw_only=True):
    jwt: str | None = None


class EmailPasswordBody(msgspec.Struct, kw_only=True):
    email: str | None = None
    password: str | None = None


class RegisterVerifyBody(EmailPasswordBody, kw_only=True):
    code: str | None = None


class EmailOnlyBody(msgspec.Struct, kw_only=True):
    email: str | None = None


class ForgotPasswordVerifyBody(EmailOnlyBody, kw_only=True):
    code: str | None = None
    new_password: str | None = None


class GoogleIdTokenBody(msgspec.Struct, kw_only=True):
    id_token: str | None = None
    idToken: str | None = None


class EmptyBody(msgspec.Struct, kw_only=True):
    pass


class ChatCreateBody(msgspec.Struct, kw_only=True):
    id: str | None = None
    title: str | None = None


class ChatTitleBody(msgspec.Struct, kw_only=True):
    title: str | None = None


class MessageFeedbackBody(msgspec.Struct, kw_only=True):
    feedback: str | None = None
    categories: list[str] | None = None
    comment: str | None = None


class UiLocaleBody(msgspec.Struct, kw_only=True):
    locale: str | None = None
    lang: str | None = None
