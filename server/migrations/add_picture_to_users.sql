-- Опционально: добавить колонку picture для хранения аватара Google
-- Выполнить при необходимости: psql -f add_picture_to_users.sql
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS picture TEXT;
