"""
S3-совместимое хранилище (Yandex Object Storage).
Загрузка файлов с уникальными именами и получение публичных URL.
Работает без Django (telegram/discord) — использует только os.getenv.
"""
import os
import uuid
import logging

# Загрузка .env для telegram/discord (без Django settings)
_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))
if os.path.exists(_env_path):
    from dotenv import load_dotenv
    load_dotenv(_env_path)

logger = logging.getLogger(__name__)


def _get_s3_credentials():
    """Получить S3 credentials из env (Django settings не используется — падает при telegram/discord)."""
    return (
        os.getenv('S3_ACCESS_KEY_ID'),
        os.getenv('S3_SECRET_ACCESS_KEY'),
        os.getenv('S3_BUCKET'),
    )

# Yandex Object Storage endpoint
S3_ENDPOINT = 'https://storage.yandexcloud.net'


def upload_image(image_bytes: bytes, content_type: str = 'image/png') -> str | None:
    """
    Загружает изображение в S3 и возвращает публичный URL.
    Имя файла: uuid4.png
    """
    access_key, secret_key, bucket = _get_s3_credentials()

    if not all([access_key, secret_key, bucket]):
        logger.warning('S3 не настроен (S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_BUCKET). Сохранение в images/')
        return None

    try:
        import boto3
        from botocore.config import Config

        s3 = boto3.client(
            's3',
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='ru-central1',
            config=Config(signature_version='s3v4'),
        )

        key = f"images/{uuid.uuid4().hex}.png"
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=image_bytes,
            ContentType=content_type,
        )

        # Публичный URL (bucket должен быть публичным для чтения)
        url = f"https://storage.yandexcloud.net/{bucket}/{key}"
        logger.info(f'Изображение загружено в S3: {url}')
        return url

    except Exception as e:
        logger.exception(f'Ошибка загрузки в S3: {e}')
        return None


def delete_by_url(url: str) -> bool:
    """
    Удаляет объект из S3 по публичному URL.
    URL: https://storage.yandexcloud.net/{bucket}/{key}
    """
    if not url or not isinstance(url, str) or 'storage.yandexcloud.net' not in url:
        return False

    access_key, secret_key, bucket = _get_s3_credentials()

    if not all([access_key, secret_key, bucket]):
        return False

    try:
        # Парсим URL: https://storage.yandexcloud.net/bucket/key
        prefix = 'https://storage.yandexcloud.net/'
        if not url.startswith(prefix):
            return False
        rest = url[len(prefix):].split('/', 1)
        if len(rest) != 2:
            return False
        url_bucket, key = rest[0], rest[1]
        if url_bucket != bucket:
            return False

        import boto3
        from botocore.config import Config

        s3 = boto3.client(
            's3',
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='ru-central1',
            config=Config(signature_version='s3v4'),
        )
        s3.delete_object(Bucket=bucket, Key=key)
        logger.info(f'Изображение удалено из S3: {url}')
        return True
    except Exception as e:
        logger.exception(f'Ошибка удаления из S3: {e}')
        return False
