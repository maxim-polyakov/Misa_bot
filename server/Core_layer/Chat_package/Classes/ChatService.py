# -*- coding: utf-8 -*-
"""Сервис для сохранения сообщений чата в БД."""
import logging
from Deep_layer.DB_package.Classes import DB_Communication
from Deep_layer.Storage_package.Classes.S3Storage import delete_by_url


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
    def get_messages(cls, chat_id):
        """Получить сообщения чата из БД."""
        try:
            df = DB_Communication.DB_Communication().execute_query(
                'SELECT id, "user", content, is_image, timestamp, feedback, feedback_categories, feedback_comment FROM chat.chat_messages WHERE chat_id = %s ORDER BY timestamp ASC',
                (chat_id,)
            )
            if df is None or df.empty:
                return []
            messages = []
            for _, row in df.iterrows():
                ts = row['timestamp']
                fb = row.get('feedback')
                cats = row.get('feedback_categories')
                comm = row.get('feedback_comment')
                try:
                    import json
                    feedback_categories = json.loads(cats) if cats and isinstance(cats, str) else (cats if isinstance(cats, list) else None)
                except Exception:
                    feedback_categories = None
                messages.append({
                    'id': str(row['id']),
                    'user': str(row['user']),
                    'content': str(row['content']),
                    'isImage': bool(row.get('is_image', False)),
                    'timestamp': ts.isoformat() if hasattr(ts, 'isoformat') else str(ts),
                    'feedback': str(fb) if fb in ('like', 'dislike') else None,
                    'feedbackCategories': feedback_categories,
                    'feedbackComment': str(comm).strip() if comm else None,
                })
            return messages
        except Exception as e:
            logging.error(f"ChatService.get_messages error: {str(e)}")
            return []

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

    @classmethod
    def get_message_by_id(cls, chat_id, message_id):
        """Получить сообщение по id."""
        try:
            df = DB_Communication.DB_Communication().execute_query(
                'SELECT id, "user", content, is_image FROM chat.chat_messages WHERE id = %s AND chat_id = %s',
                (message_id, chat_id)
            )
            if df is None or df.empty:
                return None
            row = df.iloc[0]
            return {'id': str(row['id']), 'user': str(row['user']), 'content': str(row['content']), 'is_image': bool(row.get('is_image', False))}
        except Exception as e:
            logging.error(f"ChatService.get_message_by_id error: {str(e)}")
            return None

    @classmethod
    def update_message_content(cls, chat_id, message_id, content, is_image=False):
        """Обновить контент сообщения (для regenerate)."""
        try:
            DB_Communication.DB_Communication().execute_update(
                'UPDATE chat.chat_messages SET content = %s, is_image = %s WHERE id = %s AND chat_id = %s',
                (content, is_image, message_id, chat_id)
            )
            return True
        except Exception as e:
            logging.error(f"ChatService.update_message_content error: {str(e)}")
            return False

    @classmethod
    def set_message_feedback(cls, chat_id, message_id, feedback, categories=None, comment=None):
        """Установить лайк/дизлайк для сообщения. feedback: 'like'|'dislike'|None. categories: list, comment: str."""
        try:
            import json
            val = feedback if feedback in ('like', 'dislike') else None
            cats_raw = None
            comm = None
            if val == 'dislike':
                if categories and isinstance(categories, (list, tuple)):
                    cats_raw = json.dumps([c for c in categories if c in ('harmful', 'fake', 'unhelpful', 'others')])
                comm = (comment or '').strip()[:2000] if comment else None
            DB_Communication.DB_Communication().execute_update(
                'UPDATE chat.chat_messages SET feedback = %s, feedback_categories = %s, feedback_comment = %s WHERE id = %s AND chat_id = %s',
                (val, cats_raw, comm, message_id, chat_id)
            )
            return True
        except Exception as e:
            logging.error(f"ChatService.set_message_feedback error: {str(e)}")
            return False

    @classmethod
    def get_title(cls, chat_id):
        """Получить текущий заголовок чата."""
        try:
            df = DB_Communication.DB_Communication().execute_query(
                "SELECT title FROM chat.chats WHERE id = %s",
                (chat_id,)
            )
            if df is not None and not df.empty:
                return str(df.iloc[0].get('title', '')).strip()
        except Exception as e:
            logging.error(f"ChatService.get_title error: {str(e)}")
        return None

    @classmethod
    def update_title(cls, chat_id, title):
        """Обновить заголовок чата в БД. Только если ещё не назван (Новый чат или пусто)."""
        try:
            if not title or len(title) > 500:
                return False
            current = cls.get_title(chat_id)
            if current and current != 'Новый чат' and len(current) > 0:
                return False
            DB_Communication.DB_Communication().execute_update(
                "UPDATE chat.chats SET title = %s WHERE id = %s",
                (title[:500], chat_id)
            )
            return True
        except Exception as e:
            logging.error(f"ChatService.update_title error: {str(e)}")
        return False

    @classmethod
    def delete_chat_images_from_s3(cls, chat_id):
        """Удаляет изображения из S3 для всех сообщений чата с S3 URL."""
        messages = cls.get_messages(chat_id)
        for m in messages:
            content = m.get('content', '')
            if content and content.startswith('https://storage.yandexcloud.net/'):
                delete_by_url(content)
