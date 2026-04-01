"""Схемы тел запросов и примеры для Swagger UI (Try it out)."""
from drf_spectacular.utils import OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

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
