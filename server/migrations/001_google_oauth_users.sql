-- Миграция для поддержки Google OAuth
-- 1. Делаем пароль nullable (Google не предоставляет пароли)
-- 2. Добавляем колонку display_name для имени из Google аккаунта

-- Делаем password nullable
ALTER TABLE auth.users ALTER COLUMN password DROP NOT NULL;

-- Добавляем display_name если его нет (PostgreSQL)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'auth' AND table_name = 'users' AND column_name = 'display_name'
    ) THEN
        ALTER TABLE auth.users ADD COLUMN display_name VARCHAR(255) NULL;
    END IF;
END $$;
