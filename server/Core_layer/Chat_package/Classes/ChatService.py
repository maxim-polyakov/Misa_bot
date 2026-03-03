# -*- coding: utf-8 -*-
"""Сервис для сохранения сообщений чата в БД."""
import logging
from Deep_layer.DB_package.Classes import DB_Communication


class ChatService:
    """Сохранение сообщений в chat.chat_messages."""

    @classmethod
    def _get_user_id_by_email(cls, email):
        """Получить user_id по email."""
        try:
            df = DB_Communication.DB_Communication().execute_query(
                "SELECT id FROM auth.users WHERE email = %s",
                (email,)
            )
            if df is not None and not df.empty:
                return int(df.iloc[0]['id'])
        except Exception as e:
            logging.error(f"ChatService._get_user_id_by_email error: {str(e)}")
        return None

    @classmethod
    def _ensure_chat_exists(cls, chat_id, user_email):
        """Создать чат если не существует."""
        try:
            df = DB_Communication.DB_Communication().execute_query(
                "SELECT id FROM chat.chats WHERE id = %s",
                (chat_id,)
            )
            if df is not None and not df.empty:
                return True
            user_id = cls._get_user_id_by_email(user_email)
            if user_id:
                DB_Communication.DB_Communication().execute_update(
                    "INSERT INTO chat.chats (id, user_id, title) VALUES (%s, %s, %s)",
                    (chat_id, user_id, 'Новый чат')
                )
                return True
        except Exception as e:
            logging.error(f"ChatService._ensure_chat_exists error: {str(e)}")
        return False

    @classmethod
    def save_message(cls, chat_id, user, content, is_image=False):
        """Сохранить сообщение в БД."""
        try:
            if user != 'Misa' and not cls._ensure_chat_exists(chat_id, user):
                return
            DB_Communication.DB_Communication().execute_update(
                'INSERT INTO chat.chat_messages (chat_id, "user", content, is_image) VALUES (%s, %s, %s, %s)',
                (chat_id, user, content, is_image)
            )
        except Exception as e:
            logging.error(f"ChatService.save_message error: {str(e)}")
