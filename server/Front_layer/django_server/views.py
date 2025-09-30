from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from Core_layer.Controller_package.Classes import Controller
import json








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

#
#
# # Контроллер выхода
# @csrf_exempt
# @require_http_methods(["POST"])
# def logout_view(request):
#     """Выход пользователя"""
#     try:
#         logout(request)
#         return success_response(None, "Logout successful")
#     except Exception as e:
#         return error_response(f"Logout error: {str(e)}", 500)
#
#
# # Контроллер проверки токена
# @csrf_exempt
# @require_http_methods(["GET"])
# def verify_token(request):
#     """Проверка валидности JWT токена"""
#     try:
#         user = get_user_from_token(request)
#
#         if user is None:
#             return error_response("Invalid or expired token", 401)
#
#         user_data = {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'first_name': user.first_name,
#             'last_name': user.last_name
#         }
#
#         return success_response({
#             'user': user_data,
#             'token_valid': True
#         }, "Token is valid")
#
#     except Exception as e:
#         return error_response(f"Token verification error: {str(e)}", 500)
#
#
# # Контроллер профиля пользователя
# @csrf_exempt
# @require_http_methods(["GET", "PUT", "PATCH"])
# def profile(request):
#     """Получение и обновление профиля пользователя"""
#     try:
#         user = get_user_from_token(request)
#
#         if user is None:
#             return error_response("Authentication required", 401)
#
#         if request.method == 'GET':
#             # Получение профиля
#             user_data = {
#                 'id': user.id,
#                 'username': user.username,
#                 'email': user.email,
#                 'first_name': user.first_name,
#                 'last_name': user.last_name,
#                 'date_joined': user.date_joined.isoformat(),
#                 'last_login': user.last_login.isoformat() if user.last_login else None
#             }
#
#             return success_response(user_data)
#
#         elif request.method in ['PUT', 'PATCH']:
#             # Обновление профиля
#             data = json.loads(request.body)
#
#             if 'first_name' in data:
#                 user.first_name = data['first_name']
#             if 'last_name' in data:
#                 user.last_name = data['last_name']
#             if 'email' in data:
#                 new_email = data['email'].strip().lower()
#                 if new_email != user.email:
#                     try:
#                         validate_email(new_email)
#                         if User.objects.filter(email=new_email).exclude(id=user.id).exists():
#                             return error_response("Email already registered", 409)
#                         user.email = new_email
#                     except ValidationError:
#                         return error_response("Invalid email format", 400)
#
#             user.save()
#
#             updated_data = {
#                 'id': user.id,
#                 'username': user.username,
#                 'email': user.email,
#                 'first_name': user.first_name,
#                 'last_name': user.last_name
#             }
#
#             return success_response(updated_data, "Profile updated successfully")
#
#     except json.JSONDecodeError:
#         return error_response("Invalid JSON data", 400)
#     except Exception as e:
#         return error_response(f"Profile error: {str(e)}", 500)
#
#
# # Контроллер смены пароля
# @csrf_exempt
# @require_http_methods(["POST"])
# def change_password(request):
#     """Смена пароля"""
#     try:
#         user = get_user_from_token(request)
#
#         if user is None:
#             return error_response("Authentication required", 401)
#
#         data = json.loads(request.body)
#
#         required_fields = ['current_password', 'new_password']
#         for field in required_fields:
#             if not data.get(field):
#                 return error_response(f"Field '{field}' is required", 400)
#
#         # Проверка текущего пароля
#         if not user.check_password(data['current_password']):
#             return error_response("Current password is incorrect", 401)
#
#         # Валидация нового пароля
#         new_password = data['new_password']
#         if len(new_password) < 6:
#             return error_response("New password must be at least 6 characters long", 400)
#
#         # Установка нового пароля
#         user.set_password(new_password)
#         user.save()
#
#         # Генерация нового токена после смены пароля
#         new_token = generate_jwt_token(user.id, user.username)
#
#         return success_response({
#             'token': new_token
#         }, "Password changed successfully. New token generated.")
#
#     except json.JSONDecodeError:
#         return error_response("Invalid JSON data", 400)
#     except Exception as e:
#         return error_response(f"Password change error: {str(e)}", 500)