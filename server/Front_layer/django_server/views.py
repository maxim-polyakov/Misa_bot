from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from Core_layer.Controller_package.Classes import Controller

# Контроллер регистрации
@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Регистрация нового пользователя"""
    ctrlr = Controller.Controller()
    return ctrlr.register(request)

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