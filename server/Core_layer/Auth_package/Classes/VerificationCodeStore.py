"""
In-memory хранилище кодов верификации email при регистрации.
Код отправляется на почту, пользователь вводит его на странице подтверждения.
По аналогии с OAuthCodeStore.
"""
import time
import random
import string
import threading

_TTL_SEC = 10 * 60  # 10 минут
_store = {}  # email -> (created_at, code, password_hash)
_lock = threading.Lock()


def _generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


def put(email, password_hash):
    """Сохраняет код для email. Возвращает сгенерированный код."""
    code = _generate_code()
    with _lock:
        _store[email] = (time.time(), code, password_hash)
    return code


def has_pending(email):
    """Проверяет, есть ли ожидающая верификация для email (без удаления)."""
    with _lock:
        entry = _store.get(email)
    if entry is None:
        return False
    created_at, _, _ = entry
    return time.time() - created_at <= _TTL_SEC


def get_and_remove(email, code):
    """
    Проверяет код и возвращает password_hash при успехе, иначе None.
    Удаляет запись после проверки (одноразовый код).
    """
    with _lock:
        entry = _store.pop(email, None)
    if entry is None:
        return None
    created_at, stored_code, password_hash = entry
    if time.time() - created_at > _TTL_SEC:
        return None
    if stored_code != code:
        return None
    return password_hash
