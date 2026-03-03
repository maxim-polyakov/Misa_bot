-- Схема и таблицы для хранения чатов пользователей (как у DeepSeek)
-- Выполнить: psql <connection_string> -f add_chat_tables.sql

CREATE SCHEMA IF NOT EXISTS chat;

CREATE TABLE IF NOT EXISTS chat.chats (
    id VARCHAR(64) PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title VARCHAR(500) DEFAULT 'Новый чат',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chat.chats(user_id);
CREATE INDEX IF NOT EXISTS idx_chats_created_at ON chat.chats(created_at DESC);

CREATE TABLE IF NOT EXISTS chat.chat_messages (
    id SERIAL PRIMARY KEY,
    chat_id VARCHAR(64) NOT NULL REFERENCES chat.chats(id) ON DELETE CASCADE,
    "user" VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    is_image BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_chat_id ON chat.chat_messages(chat_id);
