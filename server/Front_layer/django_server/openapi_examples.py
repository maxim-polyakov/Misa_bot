"""Схемы тел запросов, параметров и примеров ответов для Swagger UI (Try it out)."""
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# --- Обёртка ответов API (как в Controller.success_response) ---
_ENVELOPE_SCHEMA = {
    'type': 'object',
    'properties': {
        'status': {'type': 'string', 'example': 'success'},
        'message': {'type': 'string'},
        'data': {'nullable': True},
    },
}


def _envelope_example(data, message='Success'):
    return {'status': 'success', 'message': message, 'data': data}


EX_RESP_LOGIN = OpenApiExample(
    'Успешный вход',
    value=_envelope_example(
        {
            'user': {'id': 1, 'email': 'user@example.com', 'display_name': 'user'},
            'token': '<jwt>',
            'expires_in': '7 days',
        },
        'Login successful',
    ),
    response_only=True,
)
RESP_LOGIN = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    description='Успешная авторизация',
    examples=[EX_RESP_LOGIN],
)

EX_RESP_CHECK = OpenApiExample(
    'Проверка токена',
    value=_envelope_example(
        {
            'user': {
                'id': 1,
                'email': 'user@example.com',
                'display_name': 'user',
                'picture': None,
            },
            'token': '<новый_jwt>',
            'authenticated': True,
        },
        'User is authenticated, new token generated',
    ),
    response_only=True,
)
RESP_CHECK = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    description='Токен валиден; в data — пользователь и новый JWT',
    examples=[EX_RESP_CHECK],
)

EX_RESP_CHATS_LIST = OpenApiExample(
    'Список чатов',
    value=_envelope_example(
        [
            {
                'id': 'chat-1',
                'title': 'Новый чат',
                'createdAt': '2026-01-01T12:00:00',
            }
        ],
    ),
    response_only=True,
)
RESP_CHATS_LIST = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    examples=[EX_RESP_CHATS_LIST],
)

EX_RESP_CHAT_CREATE = OpenApiExample(
    'Создан чат',
    value=_envelope_example(
        {
            'id': 'chat-1',
            'title': 'Мой чат',
            'createdAt': '2026-01-01T12:00:00Z',
        },
        'Success',
    ),
    response_only=True,
)
RESP_CHAT_CREATE = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    description='201 — чат создан',
    examples=[EX_RESP_CHAT_CREATE],
)

EX_RESP_OAUTH_TOKEN = OpenApiExample(
    'JWT по коду OAuth',
    value={'jwt': '<jwt_строка>'},
    response_only=True,
)
RESP_OAUTH_TOKEN = OpenApiResponse(
    response={
        'type': 'object',
        'properties': {'jwt': {'type': 'string', 'description': 'JWT для Authorization: Bearer'}},
    },
    description='Обмен code на JWT (формат отличается от success_response)',
    examples=[EX_RESP_OAUTH_TOKEN],
)

EX_RESP_FEEDBACK = OpenApiExample(
    'Feedback',
    value=_envelope_example({'feedback': 'like'}),
    response_only=True,
)
RESP_MESSAGE_FEEDBACK = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    examples=[EX_RESP_FEEDBACK],
)

EX_RESP_SHARE = OpenApiExample(
    'Публичный просмотр',
    value=_envelope_example(
        {
            'id': 'example-chat-id',
            'title': 'Название чата',
            'messages': [],
        },
    ),
    response_only=True,
)
RESP_SHARE_PUBLIC = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    examples=[EX_RESP_SHARE],
)

EX_RESP_MESSAGES = OpenApiExample(
    'Сообщения чата',
    value=_envelope_example(
        [
            {
                'id': 'msg-1',
                'user': 'user',
                'content': 'Текст',
            }
        ],
    ),
    response_only=True,
)
RESP_CHAT_MESSAGES = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    examples=[EX_RESP_MESSAGES],
)

EX_RESP_EXPORT = OpenApiExample(
    'Экспорт',
    value=_envelope_example(
        {
            'conversations': [
                {
                    'id': 'c1',
                    'title': 'Чат',
                    'createdAt': '2026-01-01T00:00:00',
                    'messages': [],
                }
            ],
            'user': {
                'email': 'user@example.com',
                'display_name': 'user',
                'picture': None,
            },
        },
    ),
    response_only=True,
)
RESP_CHATS_EXPORT = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    examples=[EX_RESP_EXPORT],
)

EX_RESP_TITLE = OpenApiExample(
    'Обновление заголовка',
    value=_envelope_example({'id': 'example-chat-id', 'title': 'Новое имя'}),
    response_only=True,
)
RESP_CHAT_UPDATE = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    examples=[EX_RESP_TITLE],
)

EX_RESP_EMPTY_OK = OpenApiExample(
    'Успех без data',
    value={'status': 'success', 'message': 'OK', 'data': None},
    response_only=True,
)
RESP_EMPTY_OK = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    examples=[EX_RESP_EMPTY_OK],
)

EX_RESP_EMAIL_SENT = OpenApiExample(
    'Код отправлен',
    value=_envelope_example({'email': 'user@example.com'}, 'Verification code sent to email'),
    response_only=True,
)
RESP_AUTH_EMAIL_SENT = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    description='Код отправлен на email',
    examples=[EX_RESP_EMAIL_SENT],
)

EX_RESP_TOKEN_USER = OpenApiExample(
    'Токен и пользователь',
    value=_envelope_example(
        {
            'user': {'id': 1, 'email': 'user@example.com', 'display_name': 'user'},
            'token': '<jwt>',
        },
        'User registered successfully',
    ),
    response_only=True,
)
RESP_AUTH_TOKEN_USER = OpenApiResponse(
    response=_ENVELOPE_SCHEMA,
    description='201 — пользователь и JWT (регистрация / сброс пароля / verify)',
    examples=[EX_RESP_TOKEN_USER],
)

REQ_EMAIL_PASSWORD = {
    'application/json': {
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'format': 'email'},
            'password': {'type': 'string', 'minLength': 6},
        },
        'required': ['email', 'password'],
    },
}
EX_EMAIL_PASSWORD = OpenApiExample(
    'Email и пароль',
    value={'email': 'user@example.com', 'password': 'Secret123456'},
    request_only=True,
)

REQ_REGISTER_VERIFY = {
    'application/json': {
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'format': 'email'},
            'password': {'type': 'string'},
            'code': {'type': 'string', 'description': 'Код из письма (6 цифр)'},
        },
        'required': ['email', 'password', 'code'],
    },
}
EX_REGISTER_VERIFY = OpenApiExample(
    'Подтверждение регистрации',
    value={'email': 'user@example.com', 'password': 'Secret123456', 'code': '123456'},
    request_only=True,
)

REQ_EMAIL_ONLY = {
    'application/json': {
        'type': 'object',
        'properties': {'email': {'type': 'string', 'format': 'email'}},
        'required': ['email'],
    },
}
EX_EMAIL_ONLY = OpenApiExample(
    'Только email',
    value={'email': 'user@example.com'},
    request_only=True,
)

REQ_FORGOT_VERIFY = {
    'application/json': {
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'format': 'email'},
            'code': {'type': 'string'},
            'new_password': {'type': 'string', 'minLength': 6},
        },
        'required': ['email', 'code', 'new_password'],
    },
}
EX_FORGOT_VERIFY = OpenApiExample(
    'Новый пароль после кода из письма',
    value={
        'email': 'user@example.com',
        'code': '123456',
        'new_password': 'NewSecret123456',
    },
    request_only=True,
)

REQ_GOOGLE_ID_TOKEN = {
    'application/json': {
        'type': 'object',
        'properties': {
            'id_token': {'type': 'string', 'description': 'Google ID token (JWT)'},
            'idToken': {'type': 'string', 'description': 'Алиас для id_token'},
        },
    },
}
EX_GOOGLE_ID_TOKEN = OpenApiExample(
    'Google ID token',
    value={'id_token': '<вставьте JWT из Google Sign-In>'},
    request_only=True,
)

REQ_CHAT_CREATE = {
    'application/json': {
        'type': 'object',
        'properties': {
            'title': {'type': 'string', 'maxLength': 500},
            'id': {'type': 'string', 'description': 'Необязательный id чата'},
        },
    },
}
EX_CHAT_CREATE = OpenApiExample(
    'Создать чат',
    value={'title': 'Новый чат'},
    request_only=True,
)

REQ_MESSAGE_FEEDBACK = {
    'application/json': {
        'type': 'object',
        'properties': {
            'feedback': {'type': 'string', 'enum': ['like', 'dislike']},
            'categories': {'type': 'array', 'items': {'type': 'string'}},
            'comment': {'type': 'string'},
            'feedbackCategories': {'type': 'array', 'items': {'type': 'string'}},
            'feedbackComment': {'type': 'string'},
        },
    },
}
EX_MESSAGE_FEEDBACK = OpenApiExample(
    'Лайк',
    value={'feedback': 'like'},
    request_only=True,
)

REQ_CHAT_TITLE = {
    'application/json': {
        'type': 'object',
        'properties': {'title': {'type': 'string', 'maxLength': 500}},
        'required': ['title'],
    },
}
EX_CHAT_TITLE = OpenApiExample(
    'Новое название чата',
    value={'title': 'Переименованный чат'},
    request_only=True,
)

REQ_EMPTY_OBJECT = {
    'application/json': {
        'type': 'object',
        'additionalProperties': False,
    },
}
EX_EMPTY_OBJECT = OpenApiExample('Без полей', value={}, request_only=True)

PARAM_OAUTH_CODE = OpenApiParameter(
    name='code',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description='Временный код для обмена на JWT (из URL после OAuth или из callback)',
    examples=[
        OpenApiExample('Код OAuth', value='paste-authorization-code-here'),
    ],
)

PARAM_REDIRECT_URI = OpenApiParameter(
    name='redirect_uri',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=False,
    description='Для desktop: custom scheme или localhost',
    examples=[
        OpenApiExample('Misa desktop', value='misa://oauth'),
    ],
)

PARAM_GOOGLE_CALLBACK = [
    OpenApiParameter(
        name='code',
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description='Код от Google (после redirect)',
        examples=[OpenApiExample('Authorization code', value='4/0Aean...')],
    ),
    OpenApiParameter(
        name='state',
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description='OAuth state (в т.ч. закодированный redirect_uri)',
    ),
]

PARAM_SHARE_MSG = OpenApiParameter(
    name='msg',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=False,
    description='Показать только перечисленные сообщения (id через запятую)',
    examples=[OpenApiExample('Фильтр', value='msg-id-1,msg-id-2')],
)

PARAM_CHAT_ID = OpenApiParameter(
    name='chat_id',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    required=True,
    description='Идентификатор чата (как в списке чатов)',
    examples=[OpenApiExample('ID чата', value='example-chat-id')],
)

PARAM_MESSAGE_ID = OpenApiParameter(
    name='message_id',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    required=True,
    description='Идентификатор сообщения',
    examples=[OpenApiExample('ID сообщения', value='msg-example-id')],
)
