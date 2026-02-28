from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Controller_package.Interfaces import IController
import json
import pandas as pd
import jwt
import logging
import datetime
import os

try:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests
    from google_auth_oauthlib.flow import Flow
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    Flow = None

from Core_layer.Auth_package.Classes.OAuthCodeStore import put as oauth_code_put, get_and_remove as oauth_code_get





class Controller(IController.IController):
    # Настройки JWT
    JWT_SECRET = 'your-secret-key-here-change-in-production'
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_DAYS = 7
    __dbc = DB_Communication.DB_Communication()

    @classmethod
    def _log_data_structure(cls, obj, depth=0, path="root"):
        """Логирование структуры данных для отладки"""
        if depth > 3:  # Ограничиваем глубину
            return

        indent = "  " * depth
        logging.info(f"{indent}{path}: {type(obj)}")

        if isinstance(obj, dict):
            for k, v in obj.items():
                cls._log_data_structure(v, depth + 1, f"dict[{k}]")
        elif isinstance(obj, (list, tuple)):
            for i, item in enumerate(obj[:3]):  # Первые 3 элемента
                cls._log_data_structure(item, depth + 1, f"list[{i}]")

    @classmethod
    def _deep_convert(cls, obj):
        """Глубокое преобразование всех элементов"""
        if obj is None:
            return None
        elif isinstance(obj, (str, int, float, bool)):
            return obj
        elif isinstance(obj, dict):
            return {cls._deep_convert(k): cls._deep_convert(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [cls._deep_convert(item) for item in obj]
        else:
            # Принудительное преобразование
            try:
                if hasattr(obj, 'item'):
                    result = obj.item()
                    # Рекурсивно проверяем результат
                    return cls._deep_convert(result)
                elif hasattr(obj, 'tolist'):
                    return cls._deep_convert(obj.tolist())
                else:
                    # Все остальное в строку
                    return str(obj)
            except Exception as e:
                logging.warning(f"Could not convert {type(obj)}, using string: {str(e)}")
                return str(obj)

    @classmethod
    def success_response(cls, data=None, message="Success", status=200):
        """Версия с детальным логированием для отладки"""
        try:
            # Логируем что пришло
            logging.info(f"success_response received data type: {type(data)}")

            if data is not None:
                # Рекурсивно логируем структуру данных
                cls._log_data_structure(data)

                # Глубокое преобразование
                data = cls._deep_convert(data)

            # Пробуем создать JsonResponse
            response = JsonResponse({
                'status': 'success',
                'message': message,
                'data': data
            }, status=status)

            logging.info("success_response completed successfully")
            return response

        except Exception as e:
            logging.error(f"Error in success_response: {str(e)}")
            logging.error(f"Error type: {type(e)}")

            # Пробуем вернуть без данных
            try:
                return JsonResponse({
                    'status': 'success',
                    'message': message,
                    'data': None
                }, status=status)
            except:
                # Последний fallback
                return HttpResponse(
                    '{"status": "success", "message": "' + message + '", "data": null}',
                    content_type='application/json',
                    status=status
                )

    @classmethod
    def error_response(cls, message="Error", status=400):
        return JsonResponse({
            'status': 'error',
            'message': message
        }, status=status)

    @classmethod
    def generate_jwt_token(cls, user_id, email):
        try:
            # Use UTC explicitly
            current_time = datetime.datetime.utcnow()
            expiration_time = current_time + datetime.timedelta(days=cls.JWT_EXPIRATION_DAYS)

            payload = {
                'user_id': int(user_id),
                'email': str(email),
                'exp': expiration_time,  # jwt.encode will handle conversion to timestamp
                'iat': current_time
            }

            token = jwt.encode(payload, cls.JWT_SECRET, algorithm=cls.JWT_ALGORITHM)
            return token

        except Exception as e:
            logging.error(f"Error generating JWT token: {str(e)}")
            raise ValueError(f"Failed to generate token: {str(e)}")

    @classmethod
    def verify_jwt_token(cls, token):
        """Верификация JWT токена"""
        try:
            # Убедимся, что токен - строка
            if isinstance(token, bytes):
                token = token.decode('utf-8')

            payload = jwt.decode(
                token,
                cls.JWT_SECRET,
                algorithms=[cls.JWT_ALGORITHM],
                options={"verify_exp": True}
            )
            return payload

        except jwt.ExpiredSignatureError:
            logging.warning("JWT token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logging.warning(f"Invalid JWT token: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error verifying token: {str(e)}")
            return None

    @classmethod
    def get_user_from_token(cls, request):
        """Получение пользователя из JWT токена с использованием DB_Communication"""
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        payload = cls.verify_jwt_token(token)

        if payload is None:
            return None

        try:
            user_id = payload['user_id']

            # Используем DB_Communication для получения пользователя
            query = f"SELECT * FROM auth.users WHERE id = {user_id}"
            user_df = cls.__dbc.get_data(query)

            # Проверяем, что данные получены и не пустые
            if user_df is None or user_df.empty:
                logging.warning(f"User with id {user_id} not found in database")
                return None

            # Получаем первую запись
            user_data = user_df.iloc[0]

            # Создаем объект пользователя Django
            user = User(
                id=user_data['id'],
                email=user_data['email']
            )

            # Устанавливаем даты, если они есть в данных
            if 'date_joined' in user_data and pd.notna(user_data['date_joined']):
                user.date_joined = user_data['date_joined']
            if 'last_login' in user_data and pd.notna(user_data['last_login']):
                user.last_login = user_data['last_login']

            logging.info(f"Successfully retrieved user {user.username} from token")
            return user

        except Exception as e:
            logging.error(f"Error getting user from token: {str(e)}")
            return None

    @classmethod
    def register(cls, request):
        """Регистрация нового пользователя с использованием DB_Communication"""
        try:
            data = json.loads(request.body)

            # Валидация обязательных полей
            required_fields = ['email', 'password']
            for field in required_fields:
                if not data.get(field):
                    return cls.error_response(f"Field '{field}' is required", 400)

            email = data.get('email').strip().lower()
            password = data.get('password')

            # Валидация email
            try:
                validate_email(email)
            except ValidationError:
                return cls.error_response("Invalid email format", 400)

            # Валидация пароля
            if len(password) < 6:
                return cls.error_response("Password must be at least 6 characters long", 400)

            # Проверка существующего пользователя через DB_Communication
            email_check_query = f"SELECT id FROM auth.users WHERE email = '{email}'"
            email_df = cls.__dbc.get_data(email_check_query)

            if email_df is not None and not email_df.empty:
                return cls.error_response("Email already registered", 409)

            # Хеширование пароля
            hashed_password = make_password(password)

            # Получаем следующий ID для пользователя - ИСПРАВЛЕННАЯ ЧАСТЬ
            max_id_query = "SELECT COALESCE(MAX(id), 0) as max_id FROM auth.users"
            max_id_df = cls.__dbc.get_data(max_id_query)

            # Безопасное преобразование max_id
            if max_id_df is not None and not max_id_df.empty:
                max_id = max_id_df.iloc[0]['max_id']
                # Исправляем преобразование для случая, когда таблица пуста
                if max_id is None or pd.isna(max_id):
                    next_id = 1
                else:
                    next_id = int(max_id) + 1
            else:
                next_id = 1

            # Создание пользователя через DB_Communication
            display_name = email.split('@')[0]  # По умолчанию - часть до @
            user_data = {
                'id': next_id,  # Явно указываем ID
                'email': email,
                'password': hashed_password,
                'display_name': display_name,
            }

            # Создаем DataFrame с данными пользователя
            user_df = pd.DataFrame([user_data])

            # Вставляем данные в таблицу auth_user
            cls.__dbc.insert_to(user_df, 'users', 'auth')

            # Получаем созданного пользователя для подтверждения
            user_confirm_query = f"SELECT id, email FROM auth.users WHERE id = {next_id}"
            user_confirm_df = cls.__dbc.get_data(user_confirm_query)

            if user_confirm_df is None or user_confirm_df.empty:
                return cls.error_response("Failed to create user", 500)

            user_data_from_db = user_confirm_df.iloc[0]

            # Преобразуем pandas типы в нативные Python типы
            user_id = int(user_data_from_db['id'])
            user_email = str(user_data_from_db['email'])

            # Генерация JWT токена
            token = cls.generate_jwt_token(user_id, user_email)

            user_response_data = {
                'id': user_id,
                'email': user_email,
            }

            response = cls.success_response({
                'user': user_response_data,
                'token': token
            }, "User registered successfully", 201)

            return response

        except json.JSONDecodeError:
            return cls.error_response("Invalid JSON data", 400)
        except Exception as e:
            logging.error(f"Registration error: {str(e)}")
            return cls.error_response(f"Registration error: {str(e)}", 500)

    @classmethod
    def login_view(cls, request):
        """Авторизация пользователя по email"""
        try:
            data = json.loads(request.body)

            # Валидация обязательных полей
            if not data.get('email') or not data.get('password'):
                return cls.error_response("Email and password are required", 400)

            email = data.get('email').strip().lower()
            password = data.get('password')

            # Сначала находим пользователя по email через DB_Communication
            user_query = f"SELECT * FROM auth.users WHERE email = '{email}'"
            user_df = cls.__dbc.get_data(user_query)

            if user_df is None or user_df.empty:
                return cls.error_response("Invalid email or password", 401)

            # Получаем данные пользователя
            user_data = user_df.iloc[0]
            user_id = int(user_data['id'].item()) if hasattr(user_data['id'], 'item') else int(user_data['id'])
            user_email = str(user_data['email'])
            hashed_password = str(user_data['password'])
            is_active = bool(user_data.get('is_active', True))

            # Проверяем активность аккаунта
            if not is_active:
                return cls.error_response("Account is disabled", 403)

            # Пользователь с Google OAuth (password = NULL) не может войти по паролю
            if hashed_password is None or (isinstance(hashed_password, float) and pd.isna(hashed_password)):
                return cls.error_response("Используйте вход через Google", 401)

            # Проверяем пароль вручную
            if check_password(password, hashed_password):
                # Генерация JWT токена
                token = cls.generate_jwt_token(user_id, user_email)

                user_response_data = {
                    'id': user_id,
                    'email': user_email,
                }

                return cls.success_response({
                    'user': user_response_data,
                    'token': token,
                    'expires_in': f"{cls.JWT_EXPIRATION_DAYS} days"
                }, "Login successful")
            else:
                return cls.error_response("Invalid email or password", 401)

        except json.JSONDecodeError:
            return cls.error_response("Invalid JSON data", 400)
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            return cls.error_response(f"Login error: {str(e)}", 500)

    @classmethod
    def _get_or_create_google_user(cls, email, display_name):
        """Создаёт или находит пользователя по email. Возвращает (user_id, user_email, display_name)."""
        user_query = f"SELECT id, email, display_name FROM auth.users WHERE email = '{email}'"
        user_df = cls.__dbc.get_data(user_query)

        if user_df is not None and not user_df.empty:
            user_data = user_df.iloc[0]
            user_id = int(user_data['id'].item()) if hasattr(user_data['id'], 'item') else int(user_data['id'])
            user_email = str(user_data['email'])
            dn = str(user_data['display_name']) if 'display_name' in user_data and pd.notna(user_data.get('display_name')) else display_name
            return user_id, user_email, dn

        max_id_query = "SELECT COALESCE(MAX(id), 0) as max_id FROM auth.users"
        max_id_df = cls.__dbc.get_data(max_id_query)
        next_id = 1
        if max_id_df is not None and not max_id_df.empty:
            max_id = max_id_df.iloc[0]['max_id']
            next_id = 1 if (max_id is None or pd.isna(max_id)) else int(max_id) + 1

        user_data_insert = {
            'id': next_id,
            'email': email,
            'password': None,
            'display_name': display_name,
        }
        user_df_insert = pd.DataFrame([user_data_insert])
        cls.__dbc.insert_to(user_df_insert, 'users', 'auth')
        return next_id, email, display_name

    @classmethod
    def oauth_google_redirect(cls, request):
        """
        Редирект на Google OAuth (по аналогии с e-commerce-java-two).
        Пользователь кликает ссылку -> попадает сюда -> редирект на Google.
        """
        if not GOOGLE_AUTH_AVAILABLE or Flow is None:
            return cls.error_response("Google OAuth not configured", 500)

        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        api_base = os.getenv('API_BASE_URL', request.build_absolute_uri('/').rstrip('/'))
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')

        if not client_id or not client_secret:
            logging.error("GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set")
            return cls.error_response("Google OAuth not configured", 500)

        callback_uri = f"{api_base}/auth/oauth/callback"
        client_config = {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": [callback_uri],
            }
        }
        scopes = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

        try:
            flow = Flow.from_client_config(client_config, scopes=scopes, redirect_uri=callback_uri)
            authorization_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
            return HttpResponseRedirect(authorization_url)
        except Exception as e:
            logging.error(f"OAuth redirect error: {str(e)}", exc_info=True)
            return cls.error_response(f"OAuth redirect failed: {str(e)}", 500)

    @classmethod
    def oauth_google_callback(cls, request):
        """
        Callback от Google. Обменивает code на токены, создаёт/находит пользователя,
        кладёт JWT в OAuthCodeStore, редиректит на frontend с ?oauth=google&code=xxx
        """
        if not GOOGLE_AUTH_AVAILABLE or Flow is None:
            return HttpResponseRedirect(
                f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/login?oauth_error=OAUTH_AUTH_ERROR"
            )

        code = request.GET.get('code')
        if not code:
            return HttpResponseRedirect(
                f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/login?oauth_error=OAUTH_MISSING_DATA"
            )

        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        api_base = os.getenv('API_BASE_URL', request.build_absolute_uri('/').rstrip('/'))
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000').rstrip('/')

        if not client_id or not client_secret:
            return HttpResponseRedirect(f"{frontend_url}/login?oauth_error=OAUTH_AUTH_ERROR")

        callback_uri = f"{api_base}/auth/oauth/callback"
        client_config = {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": [callback_uri],
            }
        }
        scopes = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

        try:
            flow = Flow.from_client_config(client_config, scopes=scopes, redirect_uri=callback_uri)
            flow.fetch_token(code=code)

            credentials = flow.credentials
            idinfo = id_token.verify_oauth2_token(
                credentials.id_token,
                google_requests.Request(),
                client_id
            )

            email = idinfo.get('email', '').strip().lower()
            display_name = idinfo.get('name') or idinfo.get('given_name') or email.split('@')[0] or 'User'

            if not email:
                return HttpResponseRedirect(f"{frontend_url}/login?oauth_error=OAUTH_MISSING_DATA")

            user_id, user_email, display_name = cls._get_or_create_google_user(email, display_name)
            jwt_token = cls.generate_jwt_token(user_id, user_email)

            oauth_code = oauth_code_put(jwt_token)
            redirect_url = f"{frontend_url}/login?oauth=google&code={oauth_code}"
            return HttpResponseRedirect(redirect_url)

        except Exception as e:
            logging.error(f"OAuth callback error: {str(e)}")
            return HttpResponseRedirect(f"{frontend_url}/login?oauth_error=OAUTH_AUTH_ERROR")

    @classmethod
    def oauth_token(cls, request):
        """
        Обмен OAuth code на JWT (по аналогии с e-commerce-java-two).
        GET /auth/oauth-token?code=xxx
        """
        code = request.GET.get('code')
        if not code:
            return cls.error_response("Code is required", 400)

        jwt_token = oauth_code_get(code)
        if jwt_token is None:
            return cls.error_response("Invalid or expired code", 400)

        return JsonResponse({'jwt': jwt_token})

    @classmethod
    def check(cls, request):
        """Проверка аутентификации пользователя с обновлением токена"""
        try:
            # Получаем пользователя из токена (используем существующий метод)
            user = cls.get_user_from_token(request)

            if user is None:
                return cls.error_response("Authentication required", 401)

            # Генерируем НОВЫЙ токен для пользователя
            new_token = cls.generate_jwt_token(user.id, user.email)

            user_data = {
                'id': user.id,
                'email': user.email,
            }

            return cls.success_response({
                'user': user_data,
                'token': new_token,  # Возвращаем новый токен
                'authenticated': True
            }, "User is authenticated, new token generated")

        except Exception as e:
            logging.error(f"Auth check error: {str(e)}")
            return cls.error_response("Authentication check failed", 500)