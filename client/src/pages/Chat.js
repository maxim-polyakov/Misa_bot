import { observer } from "mobx-react-lite";
import { useState, useRef, useEffect } from "react";
import { useStores } from "../store/rootStoreContext";
import "./Chat.css";

const Chat = observer(({ onMenuToggle }) => {
    const { chatStore } = useStores();
    const [message, setMessage] = useState("");
    const messagesEndRef = useRef(null);
    const textareaRef = useRef(null);
    const messagesContainerRef = useRef(null);

    const scrollToBottom = () => {
        if (messagesContainerRef.current) {
            messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
        }
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
        // Проверяем, было ли сообщение изначально изображением
        const wasImage = msg.isImage ||
            /^(\/images\/|https?:\/\/).+(\.(jpg|jpeg|png|gif|bmp|webp|svg))($|\?)/i.test(msg.content);

        // Если это относительный путь к изображению, преобразуем в абсолютный URL
        const isRelativeImagePath = /^\/images\/[^\\]+\.(jpg|jpeg|png|gif|bmp|webp|svg)$/i.test(msg.content);
        const imageUrl = isRelativeImagePath
            ? `${process.env.REACT_APP_API_URL}${msg.content}`
            : msg.content;

        return (
            <div key={msg.id} className={`message ${msg.user === "Misa" ? "misa-message" : "user-message"}`}>
                <div className="message-avatar">
                    {msg.user === "Misa" ? "M" : "👤"}
                </div>
                <div className="message-content">
                    <div className="message-sender">{msg.user}</div>
                    {wasImage ? (
                        <img
                            src={imageUrl}
                            alt="Изображение от Misa"
                            className="message-image"
                            onError={(e) => {
                                // Если изображение не загружается, показываем текст
                                e.currentTarget.style.display = 'none';
                                const textElement = document.createElement('div');
                                textElement.className = 'message-text';
                                textElement.style.whiteSpace = 'pre-line';
                                textElement.textContent = msg.content;
                                e.currentTarget.parentNode.appendChild(textElement);
                            }}
                        />
                    ) : (
                        <div className="message-text" style={{ whiteSpace: 'pre-line' }}>
                            {msg.content}
                        </div>
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
                {/* Добавленная кнопка меню */}
                <button
                    onClick={onMenuToggle}
                    className="menu-toggle"
                    title="Открыть меню"
                >
                    ☰
                </button>
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

            {/* Контейнер для сообщений с прокруткой */}
            <div className="messages-container" ref={messagesContainerRef}>
                <div className="messages-content">
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