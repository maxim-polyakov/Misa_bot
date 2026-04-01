from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from Core_layer.Controller_package.Classes import Controller
from . import openapi_examples as oex

_BEARER = [{'bearerAuth': []}]


# Контроллер регистрации
@extend_schema(
    summary='Регистрация (legacy)',
    tags=['Auth'],
    request=oex.REQ_EMAIL_PASSWORD,
    examples=[oex.EX_EMAIL_PASSWORD],
    responses={201: oex.RESP_AUTH_TOKEN_USER},
)
@api_view(['POST'])
@csrf_exempt
def register(request):
    """Регистрация нового пользователя (legacy, без верификации)"""
    ctrlr = Controller.Controller()
    return ctrlr.register(request)


@extend_schema(
    summary='Отправка кода верификации',
    tags=['Auth'],
    request=oex.REQ_EMAIL_PASSWORD,
    examples=[oex.EX_EMAIL_PASSWORD],
    responses={200: oex.RESP_AUTH_EMAIL_SENT},
)
@api_view(['POST'])
@csrf_exempt
def register_send_code(request):
    """Отправка кода верификации на email"""
    ctrlr = Controller.Controller()
    return ctrlr.register_send_code(request)


@extend_schema(
    summary='Проверка кода и создание пользователя',
    tags=['Auth'],
    request=oex.REQ_REGISTER_VERIFY,
    examples=[oex.EX_REGISTER_VERIFY],
    responses={201: oex.RESP_AUTH_TOKEN_USER},
)
@api_view(['POST'])
@csrf_exempt
def register_verify(request):
    """Проверка кода и создание пользователя"""
    ctrlr = Controller.Controller()
    return ctrlr.register_verify(request)


@extend_schema(
    summary='Отправка кода восстановления пароля',
    tags=['Auth'],
    request=oex.REQ_EMAIL_ONLY,
    examples=[oex.EX_EMAIL_ONLY],
    responses={200: oex.RESP_AUTH_EMAIL_SENT},
)
@api_view(['POST'])
@csrf_exempt
def forgot_password_send_code(request):
    """Отправка кода восстановления пароля на email"""
    ctrlr = Controller.Controller()
    return ctrlr.forgot_password_send_code(request)


@extend_schema(
    summary='Проверка кода и установка нового пароля',
    tags=['Auth'],
    request=oex.REQ_FORGOT_VERIFY,
    examples=[oex.EX_FORGOT_VERIFY],
    responses={200: oex.RESP_AUTH_TOKEN_USER},
)
@api_view(['POST'])
@csrf_exempt
def forgot_password_verify(request):
    """Проверка кода и установка нового пароля"""
    ctrlr = Controller.Controller()
    return ctrlr.forgot_password_verify(request)


# Контроллер авторизации
@extend_schema(
    summary='Вход по email/паролю',
    tags=['Auth'],
    request=oex.REQ_EMAIL_PASSWORD,
    examples=[oex.EX_EMAIL_PASSWORD],
    responses={200: oex.RESP_LOGIN},
)
@api_view(['POST'])
@csrf_exempt
def login_view(request):
    ctrlr = Controller.Controller()
    return ctrlr.login_view(request)


# Google OAuth
@extend_schema(
    summary='OAuth Google redirect',
    tags=['Auth'],
    parameters=[oex.PARAM_REDIRECT_URI],
)
@api_view(['GET'])
@csrf_exempt
def oauth_google_redirect(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_redirect(request)


@extend_schema(
    summary='OAuth Google callback',
    tags=['Auth'],
    parameters=oex.PARAM_GOOGLE_CALLBACK,
)
@api_view(['GET'])
@csrf_exempt
def oauth_google_callback(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_callback(request)


@extend_schema(
    summary='OAuth token',
    tags=['Auth'],
    parameters=[oex.PARAM_OAUTH_CODE],
    responses={200: oex.RESP_OAUTH_TOKEN},
)
@api_view(['GET'])
@csrf_exempt
def oauth_token(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_token(request)


@extend_schema(
    summary='Google ID token (Android)',
    tags=['Auth'],
    request=oex.REQ_GOOGLE_ID_TOKEN,
    examples=[oex.EX_GOOGLE_ID_TOKEN],
    responses={200: oex.RESP_AUTH_TOKEN_USER},
)
@api_view(['POST'])
@csrf_exempt
def google_id_token(request):
    ctrlr = Controller.Controller()
    return ctrlr.google_id_token(request)


@extend_schema(
    summary='Проверка JWT',
    tags=['Auth'],
    auth=_BEARER,
    responses={200: oex.RESP_CHECK},
)
@api_view(['GET'])
@csrf_exempt
def check(request):
    ctrlr = Controller.Controller()
    return ctrlr.check(request)


@extend_schema(
    summary='Выход со всех устройств',
    tags=['Auth'],
    auth=_BEARER,
    request=oex.REQ_EMPTY_OBJECT,
    examples=[oex.EX_EMPTY_OBJECT],
    responses={200: oex.RESP_EMPTY_OK},
)
@api_view(['POST'])
@csrf_exempt
def logout_all(request):
    """Выход со всех устройств"""
    ctrlr = Controller.Controller()
    return ctrlr.logout_all(request)


@extend_schema(
    summary='Удаление аккаунта',
    tags=['Auth'],
    auth=_BEARER,
    request=oex.REQ_EMPTY_OBJECT,
    examples=[oex.EX_EMPTY_OBJECT],
    responses={200: oex.RESP_EMPTY_OK},
)
@api_view(['POST'])
@csrf_exempt
def delete_account(request):
    """Удаление аккаунта пользователя (необратимо)"""
    ctrlr = Controller.Controller()
    return ctrlr.delete_account(request)


# Chat API (требует JWT)
@extend_schema(
    summary='Список чатов',
    tags=['Chats'],
    auth=_BEARER,
    methods=['GET'],
    responses={200: oex.RESP_CHATS_LIST},
)
@extend_schema(
    summary='Создать чат',
    tags=['Chats'],
    auth=_BEARER,
    methods=['POST'],
    request=oex.REQ_CHAT_CREATE,
    examples=[oex.EX_CHAT_CREATE],
    responses={201: oex.RESP_CHAT_CREATE},
)
@api_view(['GET', 'POST'])
@csrf_exempt
def chats_list_or_create(request):
    ctrlr = Controller.Controller()
    if request.method == "GET":
        return ctrlr.chats_list(request)
    return ctrlr.chats_create(request)


@extend_schema(
    summary='Экспорт чатов',
    tags=['Chats'],
    auth=_BEARER,
    responses={200: oex.RESP_CHATS_EXPORT},
)
@api_view(['GET'])
def chats_export(request):
    ctrlr = Controller.Controller()
    return ctrlr.chats_export(request)


@extend_schema(
    summary='Публичный просмотр чата (без авторизации)',
    tags=['Chats'],
    parameters=[oex.PARAM_CHAT_ID, oex.PARAM_SHARE_MSG],
    responses={200: oex.RESP_SHARE_PUBLIC},
)
@api_view(['GET'])
@csrf_exempt
def chats_share_public(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_share_public(request, chat_id)


@extend_schema(
    summary='Сообщения чата',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID],
    responses={200: oex.RESP_CHAT_MESSAGES},
)
@api_view(['GET'])
def chats_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_messages(request, chat_id)


@extend_schema(
    summary='Лайк/дизлайк сообщения',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID, oex.PARAM_MESSAGE_ID],
    request=oex.REQ_MESSAGE_FEEDBACK,
    examples=[oex.EX_MESSAGE_FEEDBACK],
    responses={200: oex.RESP_MESSAGE_FEEDBACK},
)
@api_view(['PATCH'])
@csrf_exempt
def chats_message_feedback(request, chat_id, message_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_message_feedback(request, chat_id, message_id)


@extend_schema(
    summary='Очистить сообщения чата',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID],
    responses={200: oex.RESP_EMPTY_OK},
)
@api_view(['DELETE'])
@csrf_exempt
def chats_clear_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_clear_messages(request, chat_id)


@extend_schema(
    summary='Обновить чат',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID],
    request=oex.REQ_CHAT_TITLE,
    examples=[oex.EX_CHAT_TITLE],
    responses={200: oex.RESP_CHAT_UPDATE},
)
@api_view(['PATCH'])
@csrf_exempt
def chats_update(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_update_title(request, chat_id)


@extend_schema(
    summary='Удалить чат',
    tags=['Chats'],
    auth=_BEARER,
    parameters=[oex.PARAM_CHAT_ID],
    responses={200: oex.RESP_EMPTY_OK},
)
@api_view(['DELETE'])
@csrf_exempt
def chats_delete(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_delete(request, chat_id)
