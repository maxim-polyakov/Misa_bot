import { observer } from "mobx-react-lite";
import { useState, useRef, useEffect } from "react";
import { useStores } from "../store/rootStoreContext";
import { getImage } from "../http/userApi"
import "./Styles.css";
// Создайте отдельный компонент для сообщения
const MessageItem = observer(({ msg }) => {
    const [imageBlobUrl, setImageBlobUrl] = useState(null);
    const [imageError, setImageError] = useState(false);

    // Проверяем, было ли сообщение изначально изображением
    const wasImage = msg.isImage ||
        /^(\/images\/|https?:\/\/).+(\.(jpg|jpeg|png|gif|bmp|webp|svg))($|\?)/i.test(msg.content);

    const isRelativeImagePath = /^\/images\/[^\\]+\.(jpg|jpeg|png|gif|bmp|webp|svg)$/i.test(msg.content);

    // useEffect теперь вызывается в правильном месте - внутри React компонента
    useEffect(() => {
        if (isRelativeImagePath && !imageBlobUrl && !imageError) {
            getImage(msg.content)
                .then(blob => {
                    const blobUrl = URL.createObjectURL(blob);
                    setImageBlobUrl(blobUrl);
                })
                .catch(error => {
                    console.error('Failed to load image:', error);
                    setImageError(true);
                });
        }
    }, [isRelativeImagePath, msg.content]);

    return (
        <div className={`message ${msg.user === "Misa" ? "misa-message" : "user-message"}`}>
            <div className="message-avatar">
                {msg.user === "Misa" ? "M" : "👤"}
            </div>
            <div className="message-content">
                <div className="message-sender">{msg.user}</div>
                {wasImage && imageBlobUrl ? (
                    <img
                        src={imageBlobUrl}
                        alt="Изображение от Misa"
                        className="message-image"
                        onError={(e) => {
                            console.error('Image load error');
                            setImageError(true);
                        }}
                    />
                ) : (
                    <div className="message-text" style={{ whiteSpace: 'pre-line' }}>
                        {msg.content}
                    </div>
                )}
                {wasImage && imageError && (
                    <div className="message-text error">
                        Не удалось загрузить изображение: {msg.content}
                    </div>
                )}
                <div className="message-time">
                    {new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </div>
            </div>
        </div>
    );
});

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
                        chatStore.messages.map(msg => (
                            <MessageItem key={msg.id} msg={msg} />
                        ))
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