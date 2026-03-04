from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from drf_yasg.utils import swagger_auto_schema
from Core_layer.Controller_package.Classes import Controller

# Контроллер регистрации
@swagger_auto_schema(operation_summary='Регистрация (legacy)', tags=['Auth'])
@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Регистрация нового пользователя (legacy, без верификации)"""
    ctrlr = Controller.Controller()
    return ctrlr.register(request)


@swagger_auto_schema(operation_summary='Отправка кода верификации', tags=['Auth'])
@csrf_exempt
@require_http_methods(["POST"])
def register_send_code(request):
    """Отправка кода верификации на email"""
    ctrlr = Controller.Controller()
    return ctrlr.register_send_code(request)


@swagger_auto_schema(operation_summary='Проверка кода и создание пользователя', tags=['Auth'])
@csrf_exempt
@require_http_methods(["POST"])
def register_verify(request):
    """Проверка кода и создание пользователя"""
    ctrlr = Controller.Controller()
    return ctrlr.register_verify(request)


@swagger_auto_schema(operation_summary='Отправка кода восстановления пароля', tags=['Auth'])
@csrf_exempt
@require_http_methods(["POST"])
def forgot_password_send_code(request):
    """Отправка кода восстановления пароля на email"""
    ctrlr = Controller.Controller()
    return ctrlr.forgot_password_send_code(request)


@swagger_auto_schema(operation_summary='Проверка кода и установка нового пароля', tags=['Auth'])
@csrf_exempt
@require_http_methods(["POST"])
def forgot_password_verify(request):
    """Проверка кода и установка нового пароля"""
    ctrlr = Controller.Controller()
    return ctrlr.forgot_password_verify(request)


# Контроллер авторизации
@swagger_auto_schema(operation_summary='Вход по email/паролю', tags=['Auth'])
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    ctrlr = Controller.Controller()
    return ctrlr.login_view(request)


# Google OAuth
@swagger_auto_schema(operation_summary='OAuth Google redirect', tags=['Auth'])
@csrf_exempt
@require_http_methods(["GET"])
def oauth_google_redirect(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_redirect(request)


@swagger_auto_schema(operation_summary='OAuth Google callback', tags=['Auth'])
@csrf_exempt
@require_http_methods(["GET"])
def oauth_google_callback(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_callback(request)


@swagger_auto_schema(operation_summary='OAuth token', tags=['Auth'])
@csrf_exempt
@require_http_methods(["GET"])
def oauth_token(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_token(request)

@swagger_auto_schema(operation_summary='Проверка JWT', tags=['Auth'])
@csrf_exempt
@require_http_methods(["GET"])
def check(request):
    ctrlr = Controller.Controller()
    return ctrlr.check(request)


@swagger_auto_schema(operation_summary='Выход со всех устройств', tags=['Auth'])
@csrf_exempt
@require_http_methods(["POST"])
def logout_all(request):
    """Выход со всех устройств"""
    ctrlr = Controller.Controller()
    return ctrlr.logout_all(request)


# Chat API (требует JWT)
@swagger_auto_schema(operation_summary='Список/создание чатов', tags=['Chats'])
@csrf_exempt
@require_http_methods(["GET", "POST"])
def chats_list_or_create(request):
    ctrlr = Controller.Controller()
    if request.method == "GET":
        return ctrlr.chats_list(request)
    return ctrlr.chats_create(request)


@swagger_auto_schema(operation_summary='Экспорт чатов', tags=['Chats'])
@require_http_methods(["GET"])
def chats_export(request):
    ctrlr = Controller.Controller()
    return ctrlr.chats_export(request)


@swagger_auto_schema(operation_summary='Сообщения чата', tags=['Chats'])
@require_http_methods(["GET"])
def chats_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_messages(request, chat_id)


@swagger_auto_schema(operation_summary='Очистить сообщения чата', tags=['Chats'])
@csrf_exempt
@require_http_methods(["DELETE"])
def chats_clear_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_clear_messages(request, chat_id)


@swagger_auto_schema(operation_summary='Обновить чат', tags=['Chats'])
@csrf_exempt
@require_http_methods(["PATCH"])
def chats_update(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_update_title(request, chat_id)


@swagger_auto_schema(operation_summary='Удалить чат', tags=['Chats'])
@csrf_exempt
@require_http_methods(["DELETE"])
def chats_delete(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_delete(request, chat_id)