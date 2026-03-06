-- Добавить колонки feedback, feedback_categories, feedback_comment в chat.chat_messages
-- Выполнить: psql <connection_string> -f add_message_feedback.sql

ALTER TABLE chat.chat_messages ADD COLUMN IF NOT EXISTS feedback VARCHAR(10) DEFAULT NULL;
ALTER TABLE chat.chat_messages ADD COLUMN IF NOT EXISTS feedback_categories TEXT DEFAULT NULL;
ALTER TABLE chat.chat_messages ADD COLUMN IF NOT EXISTS feedback_comment TEXT DEFAULT NULL;

COMMENT ON COLUMN chat.chat_messages.feedback IS 'like | dislike | null';
COMMENT ON COLUMN chat.chat_messages.feedback_categories IS 'JSON array: harmful, fake, unhelpful, others';
COMMENT ON COLUMN chat.chat_messages.feedback_comment IS 'Free text from feedback modal';
