from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Controller_package.Interfaces import IController
import json
import logging
import os
import random
import string
from urllib.parse import quote
import datetime
import pandas as pd
import jwt

try:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests
    from google_auth_oauthlib.flow import Flow
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    Flow = None

from Core_layer.Auth_package.Classes.OAuthCodeStore import put as oauth_code_put, get_and_remove as oauth_code_get
from Core_layer.Chat_package.Classes.ChatService import ChatService
from django.core.mail import send_mail
from django.core.cache import cache

VERIFICATION_CODE_TTL_MINUTES = 15





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
    def generate_jwt_token(cls, user_id, email, display_name=None, picture=None):
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
            if display_name is not None:
                payload['display_name'] = str(display_name)
            if picture is not None:
                payload['picture'] = str(picture)

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
            cache_key = f"auth_user_full:{user_id}"
            user_data = cache.get(cache_key)
            if user_data is None:
                query = f"SELECT * FROM auth.users WHERE id = {user_id}"
                user_df = cls.__dbc.get_data(query)
                if user_df is None or user_df.empty:
                    logging.warning(f"User with id {user_id} not found in database")
                    return None
                user_data = user_df.iloc[0].to_dict()
                cache.set(cache_key, user_data, 300)

            # Создаем объект пользователя Django
            user = User(
                id=user_data['id'],
                email=user_data['email']
            )

            # Устанавливаем даты, display_name и picture, если они есть в данных
            if 'date_joined' in user_data and pd.notna(user_data.get('date_joined')):
                user.date_joined = user_data['date_joined']
            if 'last_login' in user_data and pd.notna(user_data.get('last_login')):
                user.last_login = user_data['last_login']
            if 'display_name' in user_data and pd.notna(user_data.get('display_name')):
                user.display_name = str(user_data['display_name'])
            if 'picture' in user_data and pd.notna(user_data.get('picture')):
                user.picture = str(user_data['picture'])

            logging.info(f"Successfully retrieved user {user.username} from token")
            return user

        except Exception as e:
            logging.error(f"Error getting user from token: {str(e)}")
            return None

    @staticmethod
    def _normalize_email(email):
        """Нормализация email: trim, lowercase. Plus-addressing (user+tag@domain) оставляем как есть."""
        return email.strip().lower()

    @staticmethod
    def _generate_verification_code(length=6):
        return ''.join(random.choices(string.digits, k=length))

    @classmethod
    def register_send_code(cls, request):
        """Отправка кода верификации на email при регистрации. Код хранится в auth.users."""
        try:
            data = json.loads(request.body)
            required_fields = ['email', 'password']
            for field in required_fields:
                if not data.get(field):
                    return cls.error_response(f"Field '{field}' is required", 400)

            email = cls._normalize_email(data.get('email'))
            password = data.get('password')

            try:
                validate_email(email)
            except ValidationError:
                return cls.error_response("Invalid email format", 400)

            if len(password) < 6:
                return cls.error_response("Password must be at least 6 characters long", 400)

            hashed_password = make_password(password)
            code = cls._generate_verification_code()
            sent_at = datetime.datetime.now(datetime.timezone.utc)

            user_check_query = f"SELECT id, verification_code FROM auth.users WHERE email = '{email}'"
            user_df = cls.__dbc.get_data(user_check_query)

            if user_df is not None and not user_df.empty:
                stored_code = user_df.iloc[0].get('verification_code')
                if pd.isna(stored_code) or stored_code is None or str(stored_code).strip() == '':
                    return cls.error_response("Email already registered", 409)
                # Resend: обновляем код и время
                update_sql = """
                    UPDATE auth.users
                    SET verification_code = %s, verification_code_sent_at = %s, password = %s
                    WHERE email = %s
                """
                cls.__dbc.execute_update(update_sql, (code, sent_at, hashed_password, email))
            else:
                max_id_query = "SELECT COALESCE(MAX(id), 0) as max_id FROM auth.users"
                max_id_df = cls.__dbc.get_data(max_id_query)
                if max_id_df is not None and not max_id_df.empty:
                    max_id = max_id_df.iloc[0]['max_id']
                    next_id = 1 if (max_id is None or pd.isna(max_id)) else int(max_id) + 1
                else:
                    next_id = 1
                display_name = email.split('@')[0]
                user_data = {
                    'id': next_id,
                    'email': email,
                    'password': hashed_password,
                    'display_name': display_name,
                    'verification_code': code,
                    'verification_code_sent_at': sent_at,
                }
                user_df_insert = pd.DataFrame([user_data])
                cls.__dbc.insert_to(user_df_insert, 'users', 'auth')

            try:
                send_mail(
                    subject='Код подтверждения регистрации',
                    message=f'Ваш код подтверждения: {code}\n\nКод действителен {VERIFICATION_CODE_TTL_MINUTES} минут.',
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as mail_err:
                logging.error(f"Failed to send verification email: {mail_err}")
                return cls.error_response("Failed to send verification email", 500)

            return cls.success_response(
                {'email': email},
                "Verification code sent to email",
                200
            )
        except json.JSONDecodeError:
            return cls.error_response("Invalid JSON data", 400)
        except Exception as e:
            logging.error(f"register_send_code error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def register_verify(cls, request):
        """Проверка кода и подтверждение регистрации. Пользователь уже в auth.users, очищаем verification_code."""
        try:
            data = json.loads(request.body)
            required_fields = ['email', 'password', 'code']
            for field in required_fields:
                if not data.get(field):
                    return cls.error_response(f"Field '{field}' is required", 400)

            email = cls._normalize_email(data.get('email'))
            password = data.get('password')
            code = str(data.get('code')).strip()

            try:
                validate_email(email)
            except ValidationError:
                return cls.error_response("Invalid email format", 400)

            user_query = f"SELECT id, email, password, display_name, verification_code, verification_code_sent_at FROM auth.users WHERE email = '{email}'"
            user_df = cls.__dbc.get_data(user_query)
            if user_df is None or user_df.empty:
                return cls.error_response("Invalid or expired verification code", 400)

            row = user_df.iloc[0]
            stored_code = row.get('verification_code')
            sent_at = row.get('verification_code_sent_at')
            hashed_password = row.get('password')

            if pd.isna(stored_code) or str(stored_code).strip() != code:
                return cls.error_response("Invalid or expired verification code", 400)

            if pd.isna(sent_at):
                return cls.error_response("Invalid or expired verification code", 400)

            sent_at_dt = pd.to_datetime(sent_at)
            if sent_at_dt.tzinfo is None:
                sent_at_dt = sent_at_dt.replace(tzinfo=datetime.timezone.utc)
            now = datetime.datetime.now(datetime.timezone.utc)
            age_minutes = (now - sent_at_dt).total_seconds() / 60
            if age_minutes > VERIFICATION_CODE_TTL_MINUTES:
                return cls.error_response("Verification code has expired", 400)

            if not check_password(password, hashed_password):
                return cls.error_response("Password does not match", 400)

            update_sql = """
                UPDATE auth.users
                SET verification_code = NULL, verification_code_sent_at = NULL
                WHERE email = %s
            """
            cls.__dbc.execute_update(update_sql, (email,))

            user_id = int(row['id'])
            user_email = str(row['email'])
            display_name = str(row['display_name']) if pd.notna(row.get('display_name')) else email.split('@')[0]
            token = cls.generate_jwt_token(user_id, user_email)

            return cls.success_response({
                'user': {'id': user_id, 'email': user_email, 'display_name': display_name},
                'token': token
            }, "User registered successfully", 201)
        except json.JSONDecodeError:
            return cls.error_response("Invalid JSON data", 400)
        except Exception as e:
            logging.error(f"register_verify error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def forgot_password_send_code(cls, request):
        """Отправка кода восстановления пароля на email. Код хранится в auth.users (password_reset_code, password_reset_sent_at)."""
        try:
            data = json.loads(request.body)
            if not data.get('email'):
                return cls.error_response("Field 'email' is required", 400)

            email = cls._normalize_email(data.get('email'))
            try:
                validate_email(email)
            except ValidationError:
                return cls.error_response("Invalid email format", 400)

            user_check_query = f"SELECT id, verification_code FROM auth.users WHERE email = '{email}'"
            user_df = cls.__dbc.get_data(user_check_query)

            if user_df is None or user_df.empty:
                return cls.error_response("User not found", 404)

            stored_code = user_df.iloc[0].get('verification_code')
            if stored_code is not None and not (pd.isna(stored_code) or str(stored_code).strip() == ''):
                return cls.error_response("Email not verified. Complete registration first.", 403)

            code = cls._generate_verification_code()
            sent_at = datetime.datetime.now(datetime.timezone.utc)

            update_sql = """
                UPDATE auth.users
                SET password_reset_code = %s, password_reset_sent_at = %s
                WHERE email = %s
            """
            cls.__dbc.execute_update(update_sql, (code, sent_at, email))

            try:
                send_mail(
                    subject='Код восстановления пароля',
                    message=f'Ваш код восстановления пароля: {code}\n\nКод действителен {VERIFICATION_CODE_TTL_MINUTES} минут.',
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as mail_err:
                logging.error(f"Failed to send password reset email: {mail_err}")
                return cls.error_response("Failed to send email", 500)

            return cls.success_response({'email': email}, "Password reset code sent", 200)
        except json.JSONDecodeError:
            return cls.error_response("Invalid JSON data", 400)
        except Exception as e:
            logging.error(f"forgot_password_send_code error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def forgot_password_verify(cls, request):
        """Проверка кода и установка нового пароля. Очищаем password_reset_code."""
        try:
            data = json.loads(request.body)
            required_fields = ['email', 'code', 'new_password']
            for field in required_fields:
                if not data.get(field):
                    return cls.error_response(f"Field '{field}' is required", 400)

            email = cls._normalize_email(data.get('email'))
            code = str(data.get('code')).strip()
            new_password = data.get('new_password')

            try:
                validate_email(email)
            except ValidationError:
                return cls.error_response("Invalid email format", 400)

            if len(new_password) < 6:
                return cls.error_response("Password must be at least 6 characters long", 400)

            user_query = f"SELECT id, email, password_reset_code, password_reset_sent_at FROM auth.users WHERE email = '{email}'"
            user_df = cls.__dbc.get_data(user_query)
            if user_df is None or user_df.empty:
                return cls.error_response("Invalid or expired code", 400)

            row = user_df.iloc[0]
            stored_code = row.get('password_reset_code')
            sent_at = row.get('password_reset_sent_at')

            if pd.isna(stored_code) or str(stored_code).strip() != code:
                return cls.error_response("Invalid or expired code", 400)

            if pd.isna(sent_at):
                return cls.error_response("Invalid or expired code", 400)

            sent_at_dt = pd.to_datetime(sent_at)
            if sent_at_dt.tzinfo is None:
                sent_at_dt = sent_at_dt.replace(tzinfo=datetime.timezone.utc)
            now = datetime.datetime.now(datetime.timezone.utc)
            age_minutes = (now - sent_at_dt).total_seconds() / 60
            if age_minutes > VERIFICATION_CODE_TTL_MINUTES:
                return cls.error_response("Code has expired", 400)

            hashed_password = make_password(new_password)
            update_sql = """
                UPDATE auth.users
                SET password = %s, password_reset_code = NULL, password_reset_sent_at = NULL
                WHERE email = %s
            """
            cls.__dbc.execute_update(update_sql, (hashed_password, email))

            user_id = int(row['id'])
            user_email = str(row['email'])
            token = cls.generate_jwt_token(user_id, user_email)

            return cls.success_response({
                'user': {'id': user_id, 'email': user_email},
                'token': token
            }, "Password reset successfully", 200)
        except json.JSONDecodeError:
            return cls.error_response("Invalid JSON data", 400)
        except Exception as e:
            logging.error(f"forgot_password_verify error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def register(cls, request):
        """Legacy: прямая регистрация без верификации. Используйте send-code + verify."""
        try:
            data = json.loads(request.body)
            required_fields = ['email', 'password']
            for field in required_fields:
                if not data.get(field):
                    return cls.error_response(f"Field '{field}' is required", 400)
            email = cls._normalize_email(data.get('email'))
            password = data.get('password')
            try:
                validate_email(email)
            except ValidationError:
                return cls.error_response("Invalid email format", 400)
            if len(password) < 6:
                return cls.error_response("Password must be at least 6 characters long", 400)
            email_check_query = f"SELECT id FROM auth.users WHERE email = '{email}'"
            email_df = cls.__dbc.get_data(email_check_query)
            if email_df is not None and not email_df.empty:
                return cls.error_response("Email already registered", 409)
            hashed_password = make_password(password)
            max_id_query = "SELECT COALESCE(MAX(id), 0) as max_id FROM auth.users"
            max_id_df = cls.__dbc.get_data(max_id_query)
            if max_id_df is not None and not max_id_df.empty:
                max_id = max_id_df.iloc[0]['max_id']
                next_id = 1 if (max_id is None or pd.isna(max_id)) else int(max_id) + 1
            else:
                next_id = 1
            display_name = email.split('@')[0]
            user_data = {'id': next_id, 'email': email, 'password': hashed_password, 'display_name': display_name}
            cls.__dbc.insert_to(pd.DataFrame([user_data]), 'users', 'auth')
            user_confirm_df = cls.__dbc.get_data(f"SELECT id, email FROM auth.users WHERE id = {next_id}")
            if user_confirm_df is None or user_confirm_df.empty:
                return cls.error_response("Failed to create user", 500)
            row = user_confirm_df.iloc[0]
            user_id, user_email = int(row['id']), str(row['email'])
            token = cls.generate_jwt_token(user_id, user_email)
            return cls.success_response({'user': {'id': user_id, 'email': user_email, 'display_name': display_name}, 'token': token}, "User registered successfully", 201)
        except json.JSONDecodeError:
            return cls.error_response("Invalid JSON data", 400)
        except Exception as e:
            logging.error(f"Registration error: {str(e)}")
            return cls.error_response(str(e), 500)

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

            # Пользователь с неподтверждённым email (ожидает верификацию)
            vc = user_data.get('verification_code')
            if vc is not None and not (pd.isna(vc) or str(vc).strip() == ''):
                return cls.error_response("email_not_verified", 403)
            user_id = int(user_data['id'].item()) if hasattr(user_data['id'], 'item') else int(user_data['id'])
            user_email = str(user_data['email'])
            hashed_password = str(user_data['password'])
            is_active = bool(user_data.get('is_active', True))

            # Проверяем активность аккаунта
            if not is_active:
                return cls.error_response("Account is disabled", 403)

            # Пользователь с Google OAuth (unusable password) не может войти по паролю
            if not is_password_usable(str(hashed_password) if hashed_password is not None else None):
                return cls.error_response("Используйте вход через Google", 401)

            # Проверяем пароль вручную
            if check_password(password, hashed_password):
                # Генерация JWT токена
                token = cls.generate_jwt_token(user_id, user_email)

                display_name = str(user_data['display_name']) if 'display_name' in user_data and pd.notna(user_data.get('display_name')) else user_email.split('@')[0]
                user_response_data = {
                    'id': user_id,
                    'email': user_email,
                    'display_name': display_name,
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
    def _get_or_create_google_user(cls, email, display_name, picture=None):
        """Создаёт или находит пользователя по email. Возвращает (user_id, user_email, display_name, picture)."""
        user_query = f"SELECT id, email, display_name FROM auth.users WHERE email = '{email}'"
        user_df = cls.__dbc.get_data(user_query)

        if user_df is not None and not user_df.empty:
            user_data = user_df.iloc[0]
            user_id = int(user_data['id'].item()) if hasattr(user_data['id'], 'item') else int(user_data['id'])
            user_email = str(user_data['email'])
            dn = str(user_data['display_name']) if 'display_name' in user_data and pd.notna(user_data.get('display_name')) else display_name
            pic = picture  # picture всегда из текущего запроса Google
            return user_id, user_email, dn, pic

        max_id_query = "SELECT COALESCE(MAX(id), 0) as max_id FROM auth.users"
        max_id_df = cls.__dbc.get_data(max_id_query)
        next_id = 1
        if max_id_df is not None and not max_id_df.empty:
            max_id = max_id_df.iloc[0]['max_id']
            next_id = 1 if (max_id is None or pd.isna(max_id)) else int(max_id) + 1

        # Колонка password имеет NOT NULL — используем Django unusable password
        user_data_insert = {
            'id': next_id,
            'email': email,
            'password': make_password(None),
            'display_name': display_name,
        }
        user_df_insert = pd.DataFrame([user_data_insert])
        try:
            cls.__dbc.insert_to(user_df_insert, 'users', 'auth')
        except Exception as e:
            logging.error(f"Failed to insert Google user: {e}")
            raise
        verify_df = cls.__dbc.get_data(f"SELECT id FROM auth.users WHERE id = {next_id}")
        if verify_df is None or verify_df.empty:
            logging.error("Google user insert succeeded but user not found in DB")
            raise ValueError("Failed to create user in database")
        return next_id, email, display_name, picture

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
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
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
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
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
            picture = idinfo.get('picture')

            if not email:
                return HttpResponseRedirect(f"{frontend_url}/login?oauth_error=OAUTH_MISSING_DATA")

            user_id, user_email, display_name, picture = cls._get_or_create_google_user(email, display_name, picture)
            jwt_token = cls.generate_jwt_token(user_id, user_email, display_name, picture)

            oauth_code = oauth_code_put(jwt_token)
            redirect_url = f"{frontend_url}/login?oauth=google&code={oauth_code}"
            return HttpResponseRedirect(redirect_url)

        except Exception as e:
            logging.error(f"OAuth callback error: {str(e)}", exc_info=True)
            detail = quote(str(e)[:200], safe='')
            return HttpResponseRedirect(f"{frontend_url}/login?oauth_error=OAUTH_AUTH_ERROR&oauth_detail={detail}")

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
    def google_id_token(cls, request):
        """
        Вход через Google ID token (для Android/iOS).
        POST /auth/google-id-token/ body: {"id_token": "..."}
        """
        if not GOOGLE_AUTH_AVAILABLE:
            return cls.error_response("Google OAuth not configured", 500)

        try:
            data = json.loads(request.body) if request.body else {}
            id_token_raw = data.get('id_token') or data.get('idToken')
            if not id_token_raw:
                return cls.error_response("id_token is required", 400)

            client_ids = [c for c in [os.getenv('GOOGLE_CLIENT_ID'), os.getenv('GOOGLE_CLIENT_ID_ANDROID')] if c]
            if not client_ids:
                return cls.error_response("Google OAuth not configured", 500)

            idinfo = None
            for cid in client_ids:
                try:
                    idinfo = id_token.verify_oauth2_token(id_token_raw, google_requests.Request(), cid)
                    break
                except ValueError:
                    continue
            if idinfo is None:
                return cls.error_response("Invalid or expired token", 401)

            email = idinfo.get('email', '').strip().lower()
            display_name = idinfo.get('name') or idinfo.get('given_name') or email.split('@')[0] or 'User'
            picture = idinfo.get('picture')

            if not email:
                return cls.error_response("Email not found in token", 400)

            user_id, user_email, display_name, picture = cls._get_or_create_google_user(email, display_name, picture)
            jwt_token = cls.generate_jwt_token(user_id, user_email, display_name, picture)

            return cls.success_response({
                'token': jwt_token,
                'user': {'id': user_id, 'email': user_email, 'display_name': display_name, 'picture': picture}
            }, "OK", 200)
        except ValueError as e:
            logging.warning(f"Google id_token verify: {e}")
            return cls.error_response("Invalid or expired token", 401)
        except Exception as e:
            logging.error(f"google_id_token error: {str(e)}", exc_info=True)
            return cls.error_response(str(e), 500)

    @classmethod
    def logout_all(cls, request):
        """Выход со всех устройств: помечает все токены пользователя как недействительные"""
        try:
            user = getattr(request, 'user', None)
            if user is None:
                return cls.error_response("Authentication required", 401)
            user_id = getattr(user, 'id', None)
            if user_id is None:
                return cls.error_response("Authentication required", 401)
            update_sql = "UPDATE auth.users SET logout_all_at = CURRENT_TIMESTAMP WHERE id = %s"
            cls.__dbc.execute_update(update_sql, (user_id,))
            cache.delete(f"auth_user:{user_id}")
            cache.delete(f"auth_user_full:{user_id}")
            return cls.success_response(None, "Logged out from all devices", 200)
        except Exception as e:
            logging.error(f"logout_all error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def check(cls, request):
        """Проверка аутентификации пользователя с обновлением токена"""
        try:
            # Получаем пользователя из токена (используем существующий метод)
            user = cls.get_user_from_token(request)

            if user is None:
                return cls.error_response("Authentication required", 401)

            # Сохраняем display_name и picture из текущего токена (для Google и после refresh)
            auth_header = request.headers.get('Authorization', '')
            picture = None
            display_name_from_token = None
            if auth_header.startswith('Bearer '):
                payload = cls.verify_jwt_token(auth_header.split(' ')[1])
                if payload:
                    picture = payload.get('picture')
                    display_name_from_token = payload.get('display_name')

            display_name = (
                getattr(user, 'display_name', None)
                or display_name_from_token
                or user.email.split('@')[0]
            )
            picture = picture or getattr(user, 'picture', None)
            new_token = cls.generate_jwt_token(user.id, user.email, display_name, picture)

            user_data = {
                'id': user.id,
                'email': user.email,
                'display_name': display_name,
                'picture': picture,
            }

            return cls.success_response({
                'user': user_data,
                'token': new_token,  # Возвращаем новый токен
                'authenticated': True
            }, "User is authenticated, new token generated")

        except Exception as e:
            logging.error(f"Auth check error: {str(e)}")
            return cls.error_response("Authentication check failed", 500)

    # ========== Chat API (хранение в БД как у DeepSeek) ==========

    @classmethod
    def chats_list(cls, request):
        """GET /api/chats/ — список чатов пользователя"""
        try:
            user = cls.get_user_from_token(request)
            if user is None:
                return cls.error_response("Authentication required", 401)
            user_id = user.id
            df = cls.__dbc.execute_query(
                "SELECT id, title, created_at FROM chat.chats WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,)
            )
            if df is None:
                logging.error("chats_list: DB query returned None (connection/query error)")
                return cls.error_response("Database error, please retry", 500)
            if df.empty:
                return cls.success_response([])
            chats = []
            for _, row in df.iterrows():
                chats.append({
                    'id': str(row['id']),
                    'title': str(row['title']) if pd.notna(row['title']) else 'Новый чат',
                    'createdAt': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else str(row['created_at']),
                })
            return cls.success_response(chats)
        except Exception as e:
            logging.error(f"chats_list error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def chats_create(cls, request):
        """POST /api/chats/ — создать новый чат"""
        try:
            user = cls.get_user_from_token(request)
            if user is None:
                return cls.error_response("Authentication required", 401)
            data = json.loads(request.body) if request.body else {}
            chat_id = data.get('id') or (datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S') + str(random.randint(100, 999)))
            title = data.get('title', 'Новый чат')[:500]
            cls.__dbc.execute_update(
                """INSERT INTO chat.chats (id, user_id, title) VALUES (%s, %s, %s)
                   ON CONFLICT (id) DO NOTHING""",
                (chat_id, user.id, title)
            )
            return cls.success_response({
                'id': chat_id,
                'title': title,
                'createdAt': datetime.datetime.utcnow().isoformat() + 'Z',
            }, status=201)
        except Exception as e:
            logging.error(f"chats_create error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def chats_share_public(cls, request, chat_id):
        """GET /api/chats/<id>/share/ — публичный просмотр чата (без авторизации). ?msg=id1,id2 — только выбранные сообщения."""
        try:
            df_chat = cls.__dbc.execute_query(
                "SELECT id, title FROM chat.chats WHERE id = %s",
                (chat_id,)
            )
            if df_chat is None or df_chat.empty:
                return cls.error_response("Chat not found", 404)
            title = str(df_chat.iloc[0].get('title', '')).strip() or 'Новый чат'
            messages = ChatService.get_messages(chat_id)
            msg_param = request.GET.get('msg') if hasattr(request, 'GET') else None
            if msg_param:
                msg_ids = {m.strip() for m in msg_param.split(',') if m.strip()}
                if msg_ids:
                    messages = [m for m in messages if str(m.get('id', '')) in msg_ids]
            return cls.success_response({'id': chat_id, 'title': title, 'messages': messages})
        except Exception as e:
            logging.error(f"chats_share_public error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def chats_messages(cls, request, chat_id):
        """GET /api/chats/<id>/messages/ — сообщения чата"""
        try:
            user = cls.get_user_from_token(request)
            if user is None:
                return cls.error_response("Authentication required", 401)
            df_chat = cls.__dbc.execute_query(
                "SELECT id, user_id FROM chat.chats WHERE id = %s",
                (chat_id,)
            )
            if df_chat is None or df_chat.empty:
                return cls.error_response("Chat not found", 404)
            if int(df_chat.iloc[0]['user_id']) != user.id:
                return cls.error_response("Forbidden", 403)
            messages = ChatService.get_messages(chat_id)
            return cls.success_response(messages)
        except Exception as e:
            logging.error(f"chats_messages error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def chats_message_feedback(cls, request, chat_id, message_id):
        """PATCH /api/chats/<id>/messages/<mid>/feedback/ — установить лайк/дизлайк"""
        try:
            user = cls.get_user_from_token(request)
            if user is None:
                return cls.error_response("Authentication required", 401)
            df = cls.__dbc.execute_query(
                "SELECT user_id FROM chat.chats WHERE id = %s",
                (chat_id,)
            )
            if df is None or df.empty:
                return cls.error_response("Chat not found", 404)
            if int(df.iloc[0]['user_id']) != user.id:
                return cls.error_response("Forbidden", 403)
            data = json.loads(request.body) if request.body else {}
            feedback = data.get('feedback')
            if feedback is not None and feedback not in ('like', 'dislike'):
                feedback = None
            categories = data.get('categories') or data.get('feedbackCategories')
            comment = data.get('comment') or data.get('feedbackComment')
            ChatService.set_message_feedback(chat_id, message_id, feedback, categories=categories, comment=comment)
            return cls.success_response({'feedback': feedback})
        except Exception as e:
            logging.error(f"chats_message_feedback error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def chats_update_title(cls, request, chat_id):
        """PATCH /api/chats/<id>/ — обновить заголовок чата"""
        try:
            user = cls.get_user_from_token(request)
            if user is None:
                return cls.error_response("Authentication required", 401)
            df = cls.__dbc.execute_query("SELECT user_id FROM chat.chats WHERE id = %s", (chat_id,))
            if df is None or df.empty:
                return cls.error_response("Chat not found", 404)
            if int(df.iloc[0]['user_id']) != user.id:
                return cls.error_response("Forbidden", 403)
            data = json.loads(request.body) if request.body else {}
            title = (data.get('title') or 'Новый чат')[:500]
            cls.__dbc.execute_update(
                "UPDATE chat.chats SET title = %s WHERE id = %s",
                (title, chat_id)
            )
            return cls.success_response({'id': chat_id, 'title': title})
        except Exception as e:
            logging.error(f"chats_update_title error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def chats_delete(cls, request, chat_id):
        """DELETE /api/chats/<id>/ — удалить чат"""
        try:
            user = cls.get_user_from_token(request)
            if user is None:
                return cls.error_response("Authentication required", 401)
            df = cls.__dbc.execute_query("SELECT user_id FROM chat.chats WHERE id = %s", (chat_id,))
            if df is None or df.empty:
                return cls.error_response("Chat not found", 404)
            if int(df.iloc[0]['user_id']) != user.id:
                return cls.error_response("Forbidden", 403)
            ChatService.delete_chat_images_from_s3(chat_id)
            cls.__dbc.execute_update("DELETE FROM chat.chat_messages WHERE chat_id = %s", (chat_id,))
            cls.__dbc.execute_update("DELETE FROM chat.chats WHERE id = %s", (chat_id,))
            return cls.success_response(None, "Chat deleted", 200)
        except Exception as e:
            logging.error(f"chats_delete error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def chats_clear_messages(cls, request, chat_id):
        """DELETE /api/chats/<id>/messages/ — удалить все сообщения в чате"""
        try:
            user = cls.get_user_from_token(request)
            if user is None:
                return cls.error_response("Authentication required", 401)
            df = cls.__dbc.execute_query("SELECT user_id FROM chat.chats WHERE id = %s", (chat_id,))
            if df is None or df.empty:
                return cls.error_response("Chat not found", 404)
            if int(df.iloc[0]['user_id']) != user.id:
                return cls.error_response("Forbidden", 403)
            ChatService.delete_chat_images_from_s3(chat_id)
            cls.__dbc.execute_update("DELETE FROM chat.chat_messages WHERE chat_id = %s", (chat_id,))
            return cls.success_response(None, "Messages cleared", 200)
        except Exception as e:
            logging.error(f"chats_clear_messages error: {str(e)}")
            return cls.error_response(str(e), 500)

    @classmethod
    def chats_export(cls, request):
        """GET /api/chats/export/ — экспорт всех чатов с сообщениями для ZIP"""
        try:
            user = cls.get_user_from_token(request)
            if user is None:
                return cls.error_response("Authentication required", 401)
            user_id = user.id
            df_chats = cls.__dbc.execute_query(
                "SELECT id, title, created_at FROM chat.chats WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,)
            )
            if df_chats is None or df_chats.empty:
                return cls.success_response({
                    'conversations': [],
                    'user': {
                        'display_name': getattr(user, 'display_name', None) or user.email.split('@')[0],
                        'email': user.email,
                        'picture': getattr(user, 'picture', None),
                    }
                })
            conversations = []
            for _, row in df_chats.iterrows():
                chat_id = str(row['id'])
                df_msgs = cls.__dbc.execute_query(
                    'SELECT "user", content, is_image, timestamp FROM chat.chat_messages WHERE chat_id = %s ORDER BY timestamp ASC',
                    (chat_id,)
                )
                messages = []
                if df_msgs is not None and not df_msgs.empty:
                    for _, m in df_msgs.iterrows():
                        ts = m['timestamp']
                        messages.append({
                            'content': str(m['content']),
                            'user': str(m['user']),
                            'timestamp': ts.isoformat() if hasattr(ts, 'isoformat') else str(ts),
                        })
                conversations.append({
                    'id': chat_id,
                    'title': str(row['title']) if pd.notna(row['title']) else 'Новый чат',
                    'createdAt': row['created_at'].isoformat() if hasattr(row['created_at'], 'isoformat') else str(row['created_at']),
                    'messages': messages,
                })
            return cls.success_response({
                'conversations': conversations,
                'user': {
                    'display_name': getattr(user, 'display_name', None) or user.email.split('@')[0],
                    'email': user.email,
                    'picture': getattr(user, 'picture', None),
                }
            })
        except Exception as e:
            logging.error(f"chats_export error: {str(e)}")
            return cls.error_response(str(e), 500)