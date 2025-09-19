import { observer } from "mobx-react-lite";
import { useState, useRef, useEffect } from "react";
import { useStores } from "../store/rootStoreContext";
import "./Chat.css";

const Chat = observer(() => {
    const { chatStore } = useStores();
    const [message, setMessage] = useState("");
    const messagesEndRef = useRef(null);
    const textareaRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [chatStore.messages]);

    // Функция для автоматического изменения высоты textarea
    const adjustTextareaHeight = () => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px';
        }
    };

    useEffect(() => {
        adjustTextareaHeight();
    }, [message]);

    const handleSendMessage = async () => {
        if (message.trim()) {
            await chatStore.sendMessage(message);
            setMessage("");
            textareaRef.current?.focus();
            // Сбрасываем высоту textarea после отправки
            if (textareaRef.current) {
                textareaRef.current.style.height = 'auto';
            }
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
        // Shift+Enter - автоматически переносит строку
    };

    const handleInputChange = (e) => {
        setMessage(e.target.value);
    };

    const handleClearHistory = () => {
        if (window.confirm("Очистить всю историю сообщений?")) {
            chatStore.clearMessages();
        }
    };

    const renderMessage = (msg) => {
        // Проверяем, является ли сообщение относительным путем к изображению
        const isRelativeImagePath = /^\/images\/[^\\]+\.(jpg|jpeg|png|gif|bmp|webp|svg)$/i.test(msg.content);

        // Если это относительный путь, преобразуем в абсолютный URL
        const imageUrl = isRelativeImagePath
            ? `${process.env.REACT_APP_API_URL}${msg.content}`
            : msg.content;

        // Проверяем, является ли содержимое URL изображения
        const isImage = isRelativeImagePath ||
            /^https?:\/\/.+(\.(jpg|jpeg|png|gif|bmp|webp|svg))($|\?)/i.test(msg.content);

        return (
            <div key={msg.id} className={`message ${msg.user === "Misa" ? "misa-message" : "user-message"}`}>
                <div className="message-avatar">
                    {msg.user === "Misa" ? "M" : "👤"}
                </div>
                <div className="message-content">
                    <div className="message-sender">{msg.user}</div>
                    {isImage ? (
                        <img
                            src={imageUrl}
                            alt="Изображение от Misa"
                            className="message-image"
                            onError={(e) => {
                                e.currentTarget.style.display = 'none';
                                const textElement = document.createElement('div');
                                textElement.className = 'message-text';
                                textElement.textContent = msg.content;
                                e.currentTarget.parentNode.appendChild(textElement);
                            }}
                            onLoad={() => {
                                // Прокрутка к новому изображению после загрузки
                                setTimeout(scrollToBottom, 100);
                            }}
                        />
                    ) : (
                        <div className="message-text">{msg.content}</div>
                    )}
                    <div className="message-time">
                        {new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </div>
                </div>
            </div>
        );
    };

    const getConnectionStatus = () => {
        if (chatStore.isConnected) {
            return <span className="connection-status status-connected">● Подключено</span>;
        } else if (chatStore.isConnecting) {
            return <span className="connection-status status-connecting">● Подключение...</span>;
        } else {
            return <span className="connection-status status-disconnected">● Отключено</span>;
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h1>Misa AI Чат</h1>
                <div className="chat-header-controls">
                    <div className="chat-status">
                        {getConnectionStatus()}
                    </div>
                    {chatStore.messages.length > 0 && (
                        <button
                            onClick={handleClearHistory}
                            className="clear-history-button"
                            title="Очистить историю"
                        >
                            🗑️
                        </button>
                    )}
                </div>
            </div>

            <div className="messages-container">
                {chatStore.messages.length === 0 ? (
                    <div className="empty-chat">
                        <div className="empty-icon">💬</div>
                        <p>Начните общение с Misa AI</p>
                        <small>Задайте вопрос или поделитесь мыслями</small>
                    </div>
                ) : (
                    chatStore.messages.map(renderMessage)
                )}
                <div ref={messagesEndRef} />
            </div>

            {chatStore.isLoading && (
                <div className="typing-indicator">
                    <div className="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    Misa AI печатает...
                </div>
            )}

            <div className="input-container">
                <textarea
                    ref={textareaRef}
                    value={message}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                    placeholder="Введите ваше сообщение... (Shift+Enter для переноса строки)"
                    rows={1}
                    style={{
                        minHeight: '40px',
                        maxHeight: '150px',
                        resize: 'none',
                        padding: '12px',
                        border: '1px solid #ddd',
                        borderRadius: '20px',
                        fontSize: '14px',
                        outline: 'none',
                        transition: 'border-color 0.3s ease',
                        fontFamily: 'inherit',
                        lineHeight: '1.4'
                    }}
                    disabled={chatStore.isLoading || !chatStore.isConnected}
                    className="message-textarea"
                />
                <button
                    onClick={handleSendMessage}
                    disabled={!message.trim() || chatStore.isLoading || !chatStore.isConnected}
                    className="send-button"
                    title="Отправить сообщение"
                >
                    ➤
                </button>
            </div>

            {chatStore.error && (
                <div className="error-message">
                    <span>⚠️ {chatStore.error}</span>
                    <button
                        onClick={() => chatStore.clearError()}
                        className="error-close"
                        title="Закрыть"
                    >
                        ×
                    </button>
                </div>
            )}

            {!chatStore.isConnected && !chatStore.isConnecting && (
                <div className="reconnect-container">
                    <p>Соединение потеряно</p>
                    <button
                        onClick={() => chatStore.connect()}
                        className="reconnect-button"
                    >
                        🔄 Переподключиться
                    </button>
                </div>
            )}
        </div>
    );
});

export default Chat;