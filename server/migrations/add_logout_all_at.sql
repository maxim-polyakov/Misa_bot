-- Колонка для выхода со всех устройств
-- Выполнить: psql -f add_logout_all_at.sql
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS logout_all_at TIMESTAMP WITH TIME ZONE;
