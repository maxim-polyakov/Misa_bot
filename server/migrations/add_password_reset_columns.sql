-- Колонки для хранения кода восстановления пароля в auth.users
-- Выполнить: psql -f add_password_reset_columns.sql
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS password_reset_code VARCHAR(10);
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS password_reset_sent_at TIMESTAMP WITH TIME ZONE;
