import jwt
import logging
import traceback
from datetime import datetime, timezone
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Middleware_package.Interfaces import IMiddleware
import pandas as pd

USER_CACHE_TTL = 300  # 5 минут


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
            public_paths = [
                '/auth/register/', '/auth/register/send-code/', '/auth/register/verify/',
                '/auth/login/', '/auth/forgot-password/send-code/', '/auth/forgot-password/verify/',
                '/auth/oauth/google/', '/auth/oauth/callback', '/auth/oauth-token/',
                '/images/misaimg.png',
                '/swagger/', '/swagger-ui/', '/swagger-ui/index.html', '/redoc/', '/swagger.json',
                '/accounts/login/',  # DRF "Django Login" редирект — не блокировать
            ]
            # Публичный просмотр шаринга чата — /api/chats/<id>/share/
            if (request.path.startswith('/api/chats/') and request.path.endswith('/share/')):
                return self.get_response(request)

            if (request.path in public_paths or request.path.startswith('/swagger') or
                    request.path.startswith('/redoc') or request.path.startswith('/static/') or
                    request.path.startswith('/accounts/')):
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
            response_data = {'status': 'error', 'message': 'Internal server error'}
            if getattr(settings, 'DEBUG', False):
                response_data['error'] = str(e)
                response_data['traceback'] = traceback.format_exc()
            return JsonResponse(response_data, status=500)

    def verify_token_and_get_user(self, token):
        """Синхронная верификация JWT токена (с кэшем Redis)"""
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            user_id = payload['user_id']
            iat = payload.get('iat')
            if iat is None:
                return None

            cache_key = f"auth_user:{user_id}"
            user_data = cache.get(cache_key)
            if user_data is None:
                query = f"SELECT id, email, logout_all_at FROM auth.users WHERE id = {user_id}"
                user_df = self.dbc.get_data(query)
                if user_df is None or user_df.empty:
                    return None
                row = user_df.iloc[0]
                user_data = {
                    'id': int(row['id']),
                    'email': str(row['email']),
                    'logout_all_at': row.get('logout_all_at'),
                }
                cache.set(cache_key, user_data, USER_CACHE_TTL)

            logout_all_at = user_data.get('logout_all_at')
            if logout_all_at is not None and not pd.isna(logout_all_at):
                token_issued = datetime.fromtimestamp(iat, tz=timezone.utc)
                logout_dt = pd.to_datetime(logout_all_at)
                if logout_dt.tzinfo is None:
                    logout_dt = logout_dt.replace(tzinfo=timezone.utc)
                if token_issued < logout_dt:
                    logging.warning("Token invalidated by logout from all devices")
                    return None

            class SimpleUser:
                def __init__(self, data):
                    self.id = data['id']
                    self.email = data['email']
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