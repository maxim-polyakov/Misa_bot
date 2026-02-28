"""
In-memory хранилище OAuth-кодов. Код используется для обмена на JWT токен
(избегаем передачи JWT в URL при редиректе на frontend).
По аналогии с e-commerce-java-two.
"""
import time
import uuid
import threading

_TTL_SEC = 2 * 60  # 2 минуты
_store = {}
_lock = threading.Lock()


def put(jwt_token):
    code = uuid.uuid4().hex
    with _lock:
        _store[code] = (time.time(), jwt_token)
    return code


def get_and_remove(code):
    with _lock:
        entry = _store.pop(code, None)
    if entry is None:
        return None
    created_at, jwt_token = entry
    if time.time() - created_at > _TTL_SEC:
        return None
    return jwt_token
