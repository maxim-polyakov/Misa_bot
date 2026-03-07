from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from Core_layer.Controller_package.Classes import Controller

# Контроллер регистрации
@swagger_auto_schema(method='post', operation_summary='Регистрация (legacy)', tags=['Auth'])
@api_view(['POST'])
@csrf_exempt
def register(request):
    """Регистрация нового пользователя (legacy, без верификации)"""
    ctrlr = Controller.Controller()
    return ctrlr.register(request)


@swagger_auto_schema(method='post', operation_summary='Отправка кода верификации', tags=['Auth'])
@api_view(['POST'])
@csrf_exempt
def register_send_code(request):
    """Отправка кода верификации на email"""
    ctrlr = Controller.Controller()
    return ctrlr.register_send_code(request)


@swagger_auto_schema(method='post', operation_summary='Проверка кода и создание пользователя', tags=['Auth'])
@api_view(['POST'])
@csrf_exempt
def register_verify(request):
    """Проверка кода и создание пользователя"""
    ctrlr = Controller.Controller()
    return ctrlr.register_verify(request)


@swagger_auto_schema(method='post', operation_summary='Отправка кода восстановления пароля', tags=['Auth'])
@api_view(['POST'])
@csrf_exempt
def forgot_password_send_code(request):
    """Отправка кода восстановления пароля на email"""
    ctrlr = Controller.Controller()
    return ctrlr.forgot_password_send_code(request)


@swagger_auto_schema(method='post', operation_summary='Проверка кода и установка нового пароля', tags=['Auth'])
@api_view(['POST'])
@csrf_exempt
def forgot_password_verify(request):
    """Проверка кода и установка нового пароля"""
    ctrlr = Controller.Controller()
    return ctrlr.forgot_password_verify(request)


# Контроллер авторизации
@swagger_auto_schema(method='post', operation_summary='Вход по email/паролю', tags=['Auth'])
@api_view(['POST'])
@csrf_exempt
def login_view(request):
    ctrlr = Controller.Controller()
    return ctrlr.login_view(request)


# Google OAuth
@swagger_auto_schema(method='get', operation_summary='OAuth Google redirect', tags=['Auth'])
@api_view(['GET'])
@csrf_exempt
def oauth_google_redirect(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_redirect(request)


@swagger_auto_schema(method='get', operation_summary='OAuth Google callback', tags=['Auth'])
@api_view(['GET'])
@csrf_exempt
def oauth_google_callback(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_callback(request)


@swagger_auto_schema(method='get', operation_summary='OAuth token', tags=['Auth'])
@api_view(['GET'])
@csrf_exempt
def oauth_token(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_token(request)


@swagger_auto_schema(method='post', operation_summary='Google ID token (Android)', tags=['Auth'])
@api_view(['POST'])
@csrf_exempt
def google_id_token(request):
    ctrlr = Controller.Controller()
    return ctrlr.google_id_token(request)


@swagger_auto_schema(method='get', operation_summary='Проверка JWT', tags=['Auth'])
@api_view(['GET'])
@csrf_exempt
def check(request):
    ctrlr = Controller.Controller()
    return ctrlr.check(request)


@swagger_auto_schema(method='post', operation_summary='Выход со всех устройств', tags=['Auth'])
@api_view(['POST'])
@csrf_exempt
def logout_all(request):
    """Выход со всех устройств"""
    ctrlr = Controller.Controller()
    return ctrlr.logout_all(request)


# Chat API (требует JWT)
@swagger_auto_schema(method='get', operation_summary='Список чатов', tags=['Chats'])
@swagger_auto_schema(method='post', operation_summary='Создать чат', tags=['Chats'])
@api_view(['GET', 'POST'])
@csrf_exempt
def chats_list_or_create(request):
    ctrlr = Controller.Controller()
    if request.method == "GET":
        return ctrlr.chats_list(request)
    return ctrlr.chats_create(request)


@swagger_auto_schema(method='get', operation_summary='Экспорт чатов', tags=['Chats'])
@api_view(['GET'])
def chats_export(request):
    ctrlr = Controller.Controller()
    return ctrlr.chats_export(request)


@swagger_auto_schema(method='get', operation_summary='Публичный просмотр чата (без авторизации)', tags=['Chats'])
@api_view(['GET'])
@csrf_exempt
def chats_share_public(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_share_public(request, chat_id)


@swagger_auto_schema(method='get', operation_summary='Сообщения чата', tags=['Chats'])
@api_view(['GET'])
def chats_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_messages(request, chat_id)


@swagger_auto_schema(method='patch', operation_summary='Лайк/дизлайк сообщения', tags=['Chats'])
@api_view(['PATCH'])
@csrf_exempt
def chats_message_feedback(request, chat_id, message_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_message_feedback(request, chat_id, message_id)


@swagger_auto_schema(method='delete', operation_summary='Очистить сообщения чата', tags=['Chats'])
@api_view(['DELETE'])
@csrf_exempt
def chats_clear_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_clear_messages(request, chat_id)


@swagger_auto_schema(method='patch', operation_summary='Обновить чат', tags=['Chats'])
@api_view(['PATCH'])
@csrf_exempt
def chats_update(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_update_title(request, chat_id)


@swagger_auto_schema(method='delete', operation_summary='Удалить чат', tags=['Chats'])
@api_view(['DELETE'])
@csrf_exempt
def chats_delete(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_delete(request, chat_id)