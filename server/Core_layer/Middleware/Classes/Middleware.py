import jwt
import logging
from django.http import JsonResponse
from Deep_layer.DB_package.Classes import DB_Communication
import pandas as pd


class Middleware:
    get_response = None
    __dbc = DB_Communication.DB_Communication()
    JWT_SECRET = "your-secret-key-here-change-in-production"
    JWT_ALGORITHM = 'HS256'

    def __init__(self, get_response):
        Middleware.get_response = get_response

    def __call__(self, request):
        return self.process_request(request)

    @classmethod
    def process_request(cls, request):
        """Обработка запроса"""
        # Пропускаем аутентификацию для публичных endpoints
        public_paths = [
            '/auth/register',
            '/auth/login',
        ]

        # Проверяем, нужно ли аутентифицировать этот путь
        if any(request.path.startswith(path) for path in public_paths):
            return cls.get_response(request)

        # Для пути /auth - проверяем аутентификацию
        if request.path == '/auth':
            return cls.handle_auth_check(request)

        # Для остальных защищенных путей - проверяем токен
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                'status': 'error',
                'message': 'Authentication required'
            }, status=401)

        token = auth_header.split(' ')[1]
        user = cls.verify_token_and_get_user(token)

        if user is None:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token'
            }, status=401)

        # Добавляем пользователя в request
        request.user = user

        # Проверяем что get_response не None
        if cls.get_response is None:
            return JsonResponse({
                'status': 'error',
                'message': 'Middleware not properly initialized'
            }, status=500)

        response = cls.get_response(request)
        return response

    @classmethod
    def handle_auth_check(cls, request):
        """Обработка запроса /auth"""
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                'status': 'error',
                'message': 'Authentication required'
            }, status=401)

        token = auth_header.split(' ')[1]
        user = cls.verify_token_and_get_user(token)

        if user is None:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired token'
            }, status=401)

        # Добавляем пользователя в request и передаем дальше
        request.user = user

        if cls.get_response is None:
            return JsonResponse({
                'status': 'error',
                'message': 'Middleware not properly initialized'
            }, status=500)

        response = cls.get_response(request)
        return response

    @classmethod
    def verify_token_and_get_user(cls, token):
        """Верификация JWT токена и получение пользователя"""
        try:
            payload = jwt.decode(token, cls.JWT_SECRET, algorithms=[cls.JWT_ALGORITHM])
            user_id = payload['user_id']

            # Получаем пользователя из базы через DB_Communication
            query = f"SELECT id, email FROM auth.users WHERE id = {user_id}"
            user_df = cls.__dbc.get_data(query)

            if user_df is None or user_df.empty:
                return None

            user_data = user_df.iloc[0]

            # Создаем упрощенный объект пользователя
            class SimpleUser:
                def __init__(self, user_data):
                    self.id = int(user_data['id'].item()) if hasattr(user_data['id'], 'item') else int(user_data['id'])
                    self.email = str(user_data['email'])
                    self.is_authenticated = True

            return SimpleUser(user_data)

        except jwt.ExpiredSignatureError:
            logging.warning("JWT token has expired")
            return None
        except jwt.InvalidTokenError:
            logging.warning("Invalid JWT token")
            return None
        except Exception as e:
            logging.error(f"Error verifying token: {str(e)}")
            return None