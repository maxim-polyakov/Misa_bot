-- Колонки для хранения кода верификации в auth.users
-- Выполнить: psql -f add_verification_columns.sql
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS verification_code VARCHAR(10);
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS verification_code_sent_at TIMESTAMP WITH TIME ZONE;
