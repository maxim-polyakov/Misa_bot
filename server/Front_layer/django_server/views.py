from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from Core_layer.Controller_package.Classes import Controller

# Контроллер регистрации
@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Регистрация нового пользователя (legacy, без верификации)"""
    ctrlr = Controller.Controller()
    return ctrlr.register(request)


@csrf_exempt
@require_http_methods(["POST"])
def register_send_code(request):
    """Отправка кода верификации на email"""
    ctrlr = Controller.Controller()
    return ctrlr.register_send_code(request)


@csrf_exempt
@require_http_methods(["POST"])
def register_verify(request):
    """Проверка кода и создание пользователя"""
    ctrlr = Controller.Controller()
    return ctrlr.register_verify(request)

# Контроллер авторизации
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    ctrlr = Controller.Controller()
    return ctrlr.login_view(request)


# Google OAuth (redirect flow, по аналогии с e-commerce-java-two)
@csrf_exempt
@require_http_methods(["GET"])
def oauth_google_redirect(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_redirect(request)


@csrf_exempt
@require_http_methods(["GET"])
def oauth_google_callback(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_google_callback(request)


@csrf_exempt
@require_http_methods(["GET"])
def oauth_token(request):
    ctrlr = Controller.Controller()
    return ctrlr.oauth_token(request)

# Этот view будет вызываться через middleware
@csrf_exempt
@require_http_methods(["GET"])
def check(request):
    ctrlr = Controller.Controller()
    return ctrlr.check(request)


@csrf_exempt
@require_http_methods(["POST"])
def logout_all(request):
    """Выход со всех устройств"""
    ctrlr = Controller.Controller()
    return ctrlr.logout_all(request)


# Chat API (требует JWT)
@csrf_exempt
@require_http_methods(["GET", "POST"])
def chats_list_or_create(request):
    ctrlr = Controller.Controller()
    if request.method == "GET":
        return ctrlr.chats_list(request)
    return ctrlr.chats_create(request)


@require_http_methods(["GET"])
def chats_export(request):
    ctrlr = Controller.Controller()
    return ctrlr.chats_export(request)


@require_http_methods(["GET"])
def chats_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_messages(request, chat_id)


@csrf_exempt
@require_http_methods(["DELETE"])
def chats_clear_messages(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_clear_messages(request, chat_id)


@csrf_exempt
@require_http_methods(["PATCH"])
def chats_update(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_update_title(request, chat_id)


@csrf_exempt
@require_http_methods(["DELETE"])
def chats_delete(request, chat_id):
    ctrlr = Controller.Controller()
    return ctrlr.chats_delete(request, chat_id)