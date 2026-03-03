import { observer } from "mobx-react-lite";
import { useState, useRef, useEffect } from "react";
import { useStores } from "../store/rootStoreContext";
import { useLocale } from "../contexts/LocaleContext";
import { useMenuToggle } from "./MainLayout";
import CachedImage from "./CachedImage";
import "./Styles.css";
import { imageDB } from "./ImageDB";

const Chat = observer(() => {
    const { chatStore } = useStores();
    const { t } = useLocale();
    const { toggleSidebar, sidebarExpanded } = useMenuToggle();
    const [message, setMessage] = useState("");
    const messagesEndRef = useRef(null);
    const textareaRef = useRef(null);
    const messagesContainerRef = useRef(null);

    const scrollToBottom = () => {
        requestAnimationFrame(() => {
            messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
        });
    };

    useEffect(() => {
        scrollToBottom();
    }, [chatStore.messages, chatStore.isLoading]);

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

    const handleClearHistory = async () => {
        if (window.confirm(t("confirmClearHistory") + "?")) {
            chatStore.clearMessages();
            await imageDB.clearAll()
        }
    };


    const getConnectionStatus = () => {
        if (chatStore.isConnected) {
            return <span className="connection-status status-connected">● {t("connected")}</span>;
        } else if (chatStore.isConnecting) {
            return <span className="connection-status status-connecting">● {t("connecting")}</span>;
        } else {
            return <span className="connection-status status-disconnected">● {t("disconnected")}</span>;
        }
    };

    const parseMessageContent = (content) => {
        if (!content || typeof content !== 'string') return [{ type: 'text', content: '' }];
        const parts = [];
        // Поддержка ```language и ``` с разными переносами строк (\n, \r\n)
        const regex = /```\s*([\w+-]*)\s*\r?\n([\s\S]*?)```/g;
        let lastIndex = 0;
        let match;
        while ((match = regex.exec(content)) !== null) {
            if (match.index > lastIndex) {
                parts.push({ type: 'text', content: content.slice(lastIndex, match.index) });
            }
            parts.push({ type: 'code', language: match[1] || 'plaintext', content: match[2].trim() });
            lastIndex = regex.lastIndex;
        }
        if (lastIndex < content.length) {
            parts.push({ type: 'text', content: content.slice(lastIndex) });
        }
        return parts.length ? parts : [{ type: 'text', content }];
    };

    const renderMessage = (msg) => {
        const messageUser = msg.user;
        const messageContent = msg.content;

        const wasImage = msg.isImage ||
            /^(\/images\/|https?:\/\/).+(\.(jpg|jpeg|png|gif|bmp|webp|svg))($|\?)/i.test(messageContent);

        const isRelativeImagePath = /^\/images\/[^\\]+\.(jpg|jpeg|png|gif|bmp|webp|svg)$/i.test(messageContent);
        const imageUrl = isRelativeImagePath
            ? `${process.env.REACT_APP_API_URL}${messageContent}`
            : messageContent;

        const cacheKey = `img_${msg.id}`;

        const renderContent = () => {
            if (wasImage) {
                return (
                    <CachedImage
                        src={imageUrl}
                        cacheKey={cacheKey}
                        messageContent={messageContent}
                        messageUser={messageUser}
                    />
                );
            }
            const parsed = parseMessageContent(messageContent);
            return (
                <div className="message-text">
                    {parsed.map((part, i) =>
                        part.type === 'text' ? (
                            <span key={i} style={{ whiteSpace: 'pre-line' }}>{part.content}</span>
                        ) : (
                            <div key={i} className="message-code-block">
                                <div className="message-code-header">{part.language}</div>
                                <pre><code>{part.content}</code></pre>
                            </div>
                        )
                    )}
                </div>
            );
        };

        return (
            <div key={msg.id} className={`message ${messageUser === "Misa" ? "misa-message" : "user-message"}`}>
                <div className="message-content">
                    {renderContent()}
                    <div className="message-time">
                        {new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </div>
                </div>
            </div>
        );
    };


    return (
        <div className="chat-container">
            {/* Плавающие кнопки поверх чата */}
            {!sidebarExpanded && (
                <button
                    type="button"
                    className="chat-floating-menu-btn"
                    onClick={toggleSidebar}
                    aria-label="Развернуть меню"
                    title="Меню"
                >
                    ☰
                </button>
            )}
            {chatStore.messages.length > 0 && (
                <button
                    onClick={handleClearHistory}
                    className="chat-floating-clear-btn"
                    title={t("clearHistory")}
                >
                    🗑️
                </button>
            )}
            <div className="chat-status-floating">
                {getConnectionStatus()}
            </div>

            {/* Контейнер для сообщений с прокруткой */}
            <div className="messages-container" ref={messagesContainerRef}>
                <div className="messages-content">
                    {chatStore.messages.length === 0 ? (
                        <div className="empty-chat">
                            <div className="empty-icon">💬</div>
                            <p>{t("startChat")}</p>
                            <small>{t("startHint")}</small>
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
                    {t("typing")}
                </div>
            )}

            <div className="input-container">
                <textarea
                    ref={textareaRef}
                    value={message}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                    placeholder={t("placeholder")}
                    rows={1}
                    style={{
                        minHeight: '40px',
                        maxHeight: '150px',
                        resize: 'none',
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
                    <p>{t("connectionLost")}</p>
                    <button
                        onClick={() => chatStore.connect()}
                        className="reconnect-button"
                    >
                        🔄 {t("reconnect")}
                    </button>
                </div>
            )}
        </div>
    );
});

export default Chat;