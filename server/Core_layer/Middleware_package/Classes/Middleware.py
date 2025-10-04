import jwt
import logging
from django.http import JsonResponse
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Middleware_package.Interfaces import IMiddleware
import pandas as pd


class Middleware(IMiddleware.IMiddleware):
    JWT_SECRET = "your-secret-key-here-change-in-production"
    JWT_ALGORITHM = 'HS256'

    def __init__(self, get_response):
        self.get_response = get_response
        self.dbc = DB_Communication.DB_Communication()

    def __call__(self, request):
        """Синхронный обработчик запроса"""
        try:
            # Публичные пути (без аутентификации)
            if request.path in ['/auth/register/', '/auth/login/', '/images/misaimg.png']:
                return self.get_response(request)

            # Проверяем аутентификацию для других путей
            auth_header = request.headers.get('Authorization', '')

            if not auth_header.startswith('Bearer '):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Authentication required'
                }, status=401)

            token = auth_header.split(' ')[1]
            user = self.verify_token_and_get_user(token)

            if user is None:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid or expired token'
                }, status=401)

            # Добавляем пользователя в request
            request.user = user

            # Продолжаем выполнение
            return self.get_response(request)

        except Exception as e:
            logging.error(f"Middleware error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error'
            }, status=500)

    def verify_token_and_get_user(self, token):
        """Синхронная верификация JWT токена"""
        try:
            # Декодируем JWT токен синхронно
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            user_id = payload['user_id']

            # Синхронный запрос к базе данных
            query = f"SELECT id, email FROM auth.users WHERE id = {user_id}"
            user_df = self.dbc.get_data(query)

            if user_df is None or user_df.empty:
                return None

            user_data = user_df.iloc[0]

            # Создаем упрощенный объект пользователя
            class SimpleUser:
                def __init__(self, user_data):
                    self.id = int(user_data['id'])
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