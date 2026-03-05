#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Очистка помеченных изображений (telegram/discord) из S3.
Удаляет файлы в images/telegram/ и images/discord/ старше 7 дней.
Запуск: из папки server: python scripts/cleanup_s3.py
Cron (ежедневно в 3:00): 0 3 * * * cd /path/to/server && python scripts/cleanup_s3.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(_env_path):
    from dotenv import load_dotenv
    load_dotenv(_env_path)

from Deep_layer.Storage_package.Classes.S3Storage import cleanup_temp_images

DAYS_OLD = int(os.getenv('S3_CLEANUP_DAYS', '7'))


def main():
    deleted = cleanup_temp_images(days_old=DAYS_OLD)
    print(f'Удалено помеченных изображений (telegram/discord) из S3: {deleted}')


if __name__ == '__main__':
    main()
