import { observer } from "mobx-react-lite";
import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { useStores } from "../store/rootStoreContext";
import { useLocale } from "../contexts/LocaleContext";
import { useMenuToggle } from "./MainLayout";
import CachedImage from "./CachedImage";
import "./Styles.css";
import { imageDB } from "./ImageDB";

const Chat = observer(() => {
    const { chatStore } = useStores();
    const { t } = useLocale();
    const [searchParams, setSearchParams] = useSearchParams();
    const { toggleSidebar, sidebarExpanded } = useMenuToggle();
    const [message, setMessage] = useState("");
    const [linkCopiedToast, setLinkCopiedToast] = useState(false);
    const [feedbackModalMsgId, setFeedbackModalMsgId] = useState(null);
    const [feedbackCategories, setFeedbackCategories] = useState([]);
    const [feedbackComment, setFeedbackComment] = useState("");
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
    }, [chatStore.messages, chatStore.isChatLoading(chatStore.currentChatId)]);

    // Подключаемся к группе чата при открытии — чтобы получать broadcast на других устройствах
    useEffect(() => {
        if (chatStore.currentChatId && chatStore.isConnected) {
            chatStore.ensureJoinedToChat(chatStore.currentChatId);
        }
    }, [chatStore.currentChatId, chatStore.isConnected]);

    // Заголовок активного чата в названии вкладки
    useEffect(() => {
        const title = chatStore.currentChat?.title?.trim();
        document.title = (title && title !== 'Новый чат') ? title : 'Misa AI Chat';
    }, [chatStore.currentChatId, chatStore.currentChat?.title]);

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

    // Открытие чата по ссылке ?chat=id
    useEffect(() => {
        const chatId = searchParams.get('chat');
        if (chatId && chatStore.chats.some(c => c.id === chatId)) {
            chatStore.switchChat(chatId);
            setSearchParams({}, { replace: true });
        }
    }, [searchParams, chatStore.chats]);

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
            await chatStore.clearMessages();
            await imageDB.clearAll();
        }
    };


    const getBlockType = (language) => {
        const lang = (language || 'plaintext').toLowerCase();
        const typeMap = {
            json: 'json', yaml: 'yaml', yml: 'yaml', xml: 'xml',
            bash: 'bash', sh: 'bash', shell: 'bash',
            sql: 'sql',
            md: 'md', markdown: 'md',
            diff: 'diff',
            warning: 'warning', warn: 'warning',
            error: 'error', err: 'error',
            quote: 'quote', citation: 'quote',
            output: 'output', log: 'output',
        };
        return typeMap[lang] || 'code';
    };

    const parseMessageContent = (content) => {
        if (!content || typeof content !== 'string') return [{ type: 'text', content: '' }];
        const parts = [];
        const regex = /```\s*([\w+-]*)\s*\r?\n([\s\S]*?)```/g;
        let lastIndex = 0;
        let match;
        while ((match = regex.exec(content)) !== null) {
            if (match.index > lastIndex) {
                parts.push({ type: 'text', content: content.slice(lastIndex, match.index) });
            }
            const language = match[1] || 'plaintext';
            parts.push({
                type: 'code',
                language,
                blockType: getBlockType(language),
                content: match[2].trim(),
            });
            lastIndex = regex.lastIndex;
        }
        if (lastIndex < content.length) {
            parts.push({ type: 'text', content: content.slice(lastIndex) });
        }
        return parts.length ? parts : [{ type: 'text', content }];
    };

    const isShareMode = chatStore.shareModeForChatId === chatStore.currentChatId;

    const renderMessage = (msg) => {
        const messageUser = msg.user;
        const messageContent = msg.content;
        const isSelected = isShareMode && chatStore.isMessageSelected(msg.id);

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
                            <div key={i} className={`message-code-block message-code-block--${part.blockType}`}>
                                <div className="message-code-header">{part.language}</div>
                                <pre><code>{part.content}</code></pre>
                            </div>
                        )
                    )}
                </div>
            );
        };

        const messageEl = (
            <div
                key={msg.id}
                className={`message ${messageUser === "Misa" ? "misa-message" : "user-message"} ${isSelected ? "message-selected" : ""}`}
                onClick={isShareMode ? () => chatStore.toggleMessageSelection(msg.id) : undefined}
                role={isShareMode ? "button" : undefined}
                tabIndex={isShareMode ? 0 : undefined}
                onKeyDown={isShareMode ? (e) => { if (e.key === "Enter" || e.key === " ") chatStore.toggleMessageSelection(msg.id); } : undefined}
            >
                <div className="message-content">
                    {isShareMode && (
                        <span className="message-select-icon">{isSelected ? "✓" : ""}</span>
                    )}
                    {renderContent()}
                    <div className="message-time">
                        {new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </div>
                    {messageUser === 'Misa' && (
                        <div className="message-actions" onClick={e => e.stopPropagation()}>
                            <button
                                type="button"
                                className="message-action-btn"
                                onClick={e => handleCopyMessage(e, msg)}
                                title={t("copy")}
                            >
                                {copiedMsgId === msg.id ? "✓" : "📋"}
                            </button>
                            <button
                                type="button"
                                className="message-action-btn"
                                onClick={e => handleRegenerate(e, msg)}
                                title={t("regenerate")}
                            >
                                ↻
                            </button>
                            <button
                                type="button"
                                className={`message-action-btn message-action-btn-icon ${chatStore.getMessageFeedback(msg.id) === 'like' ? 'active filled' : ''}`}
                                onClick={e => { e.stopPropagation(); chatStore.setMessageFeedback(msg.id, chatStore.getMessageFeedback(msg.id) === 'like' ? null : 'like'); }}
                                title={t("like")}
                            >
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path className="icon-outline" fill="none" d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
                                    <path className="icon-fill" fill="currentColor" stroke="none" d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
                                </svg>
                            </button>
                            <button
                                type="button"
                                className={`message-action-btn message-action-btn-icon ${chatStore.getMessageFeedback(msg.id) === 'dislike' ? 'active filled' : ''}`}
                                onClick={e => {
                                    e.stopPropagation();
                                    if (chatStore.getMessageFeedback(msg.id) === 'dislike') {
                                        chatStore.setMessageFeedback(msg.id, null);
                                    } else {
                                        setFeedbackModalMsgId(msg.id);
                                        setFeedbackCategories(msg.feedbackCategories || []);
                                        setFeedbackComment(msg.feedbackComment || "");
                                    }
                                }}
                                title={t("dislike")}
                            >
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path className="icon-outline" fill="none" d="M7 13V5a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h3a4 4 0 0 1 4 4v1a2 2 0 0 0 4 0v-5h3a2 2 0 0 0 2-2l-1-5a2 3 0 0 0-2-2h-7a3 3 0 0 0-3 3" />
                                    <path className="icon-fill" fill="currentColor" stroke="none" d="M7 13V5a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h3a4 4 0 0 1 4 4v1a2 2 0 0 0 4 0v-5h3a2 2 0 0 0 2-2l-1-5a2 3 0 0 0-2-2h-7a3 3 0 0 0-3 3" />
                                </svg>
                            </button>
                            <button
                                type="button"
                                className="message-action-btn"
                                onClick={e => handleShareMessage(e, msg)}
                                title={t("share")}
                            >
                                ↗
                            </button>
                        </div>
                    )}
                </div>
            </div>
        );
        return messageEl;
    };

    const handleCreateLink = async () => {
        const url = chatStore.getShareLink();
        try {
            await navigator.clipboard.writeText(url);
            setLinkCopiedToast(true);
            setTimeout(() => setLinkCopiedToast(false), 2000);
        } catch (e) {
            console.warn("Copy failed:", e);
        }
    };

    const [copiedMsgId, setCopiedMsgId] = useState(null);
    const handleCopyMessage = async (e, msg) => {
        e?.stopPropagation?.();
        try {
            await navigator.clipboard.writeText(msg.content);
            setCopiedMsgId(msg.id);
            setTimeout(() => setCopiedMsgId(null), 1500);
        } catch (err) {
            console.warn("Copy failed:", err);
        }
    };

    const handleShareMessage = (e, msg) => {
        e?.stopPropagation?.();
        chatStore.startShareModeWithMessage(chatStore.currentChatId, msg.id);
    };

    const handleRegenerate = (e, msg) => {
        e?.stopPropagation?.();
        chatStore.regenerateReply(msg.id);
    };

    const FEEDBACK_CATEGORIES = [
        { id: 'harmful', tKey: 'feedbackHarmful' },
        { id: 'fake', tKey: 'feedbackFake' },
        { id: 'unhelpful', tKey: 'feedbackUnhelpful' },
        { id: 'others', tKey: 'feedbackOthers' },
    ];

    const toggleFeedbackCategory = (id) => {
        setFeedbackCategories(prev =>
            prev.includes(id) ? prev.filter(c => c !== id) : [...prev, id]
        );
    };

    const handleFeedbackSubmit = async () => {
        if (feedbackModalMsgId) {
            await chatStore.setMessageFeedback(feedbackModalMsgId, 'dislike', feedbackCategories, feedbackComment);
            setFeedbackModalMsgId(null);
            setFeedbackCategories([]);
            setFeedbackComment("");
        }
    };

    const handleFeedbackCancel = () => {
        setFeedbackModalMsgId(null);
        setFeedbackCategories([]);
        setFeedbackComment("");
    };

    return (
        <div className="chat-container">
            {/* Плавающие кнопки поверх чата */}
            {!sidebarExpanded && (
                <div className="chat-floating-buttons">
                    <img
                        src="/favicon.ico"
                        alt=""
                        className="chat-floating-logo"
                        onClick={toggleSidebar}
                        role="button"
                        tabIndex={0}
                        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") toggleSidebar(); }}
                        title="Меню"
                    />
                    <button
                        type="button"
                        className="chat-floating-menu-btn"
                        onClick={toggleSidebar}
                        aria-label="Развернуть меню"
                        title="Меню"
                    >
                        ☰
                    </button>
                    <button
                        type="button"
                        className="chat-floating-new-chat-btn"
                        onClick={() => chatStore.newChat()}
                        title={t("newChat")}
                    >
                        +
                    </button>
                </div>
            )}

            {/* Контейнер для сообщений с прокруткой */}
            <div className={`messages-container ${chatStore.messages.length === 0 ? 'chat-empty' : ''}`} ref={messagesContainerRef}>
                <div className="messages-content">
                    {chatStore.currentChat?.title && chatStore.messages.length > 0 && (
                        <h2 key={chatStore.currentChatId} className="chat-title-center">
                            {chatStore.currentChat.title}
                        </h2>
                    )}
                    {chatStore.messages.length === 0 ? (
                        <div className="empty-chat">
                            <div className="empty-chat-header">
                                <img src="/favicon.ico" alt="Misa" className="empty-chat-logo" />
                                <h2 className="empty-chat-title">{t("startChat")}</h2>
                            </div>
                            <p className="empty-chat-hint">{t("startHint")}</p>
                        </div>
                    ) : (
                        chatStore.messages.map(renderMessage)
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {chatStore.isChatLoading(chatStore.currentChatId) && (
                <div className="typing-indicator">
                    <div className="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    {t("typing")}
                </div>
            )}

            {linkCopiedToast && (
                <div className="share-toast">{t("linkCopied")}</div>
            )}

            {feedbackModalMsgId && (
                <div className="feedback-modal-overlay" onClick={handleFeedbackCancel}>
                    <div className="feedback-modal" onClick={e => e.stopPropagation()}>
                        <h3 className="feedback-modal-title">{t("feedback")}</h3>
                        <div className="feedback-modal-categories">
                            {FEEDBACK_CATEGORIES.map(({ id, tKey }) => (
                                <button
                                    key={id}
                                    type="button"
                                    className={`feedback-modal-pill ${feedbackCategories.includes(id) ? "active" : ""}`}
                                    onClick={() => toggleFeedbackCategory(id)}
                                >
                                    {t(tKey)}
                                </button>
                            ))}
                        </div>
                        <textarea
                            className="feedback-modal-textarea"
                            placeholder={t("feedbackPlaceholder")}
                            value={feedbackComment}
                            onChange={e => setFeedbackComment(e.target.value)}
                            rows={4}
                        />
                        <div className="feedback-modal-actions">
                            <button type="button" className="feedback-modal-btn feedback-modal-btn-cancel" onClick={handleFeedbackCancel}>
                                {t("cancel")}
                            </button>
                            <button type="button" className="feedback-modal-btn feedback-modal-btn-submit" onClick={handleFeedbackSubmit}>
                                {t("submit")}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            <div className="input-container">
                {isShareMode ? (
                    <div className="share-bar">
                        <button type="button" className="share-bar-btn" onClick={() => chatStore.selectAllMessages()}>
                            {t("selectAll")}
                        </button>
                        <span className="share-bar-count">
                            {chatStore.selectedMessageIds.length} {t("selectedTurns")}
                        </span>
                        <button type="button" className="share-bar-btn" onClick={() => chatStore.endShareMode()}>
                            {t("cancel")}
                        </button>
                        <button
                            type="button"
                            className="share-bar-btn share-bar-btn-primary"
                            onClick={handleCreateLink}
                            title={t("createPublicLink")}
                        >
                            ⎘ {t("createPublicLink")}
                        </button>
                    </div>
                ) : (
                    <>
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
                    disabled={chatStore.isChatLoading(chatStore.currentChatId) || !chatStore.isConnected}
                    className="message-textarea"
                />
                <button
                    onClick={handleSendMessage}
                    disabled={!message.trim() || chatStore.isChatLoading(chatStore.currentChatId) || !chatStore.isConnected}
                    className="send-button"
                    title="Отправить сообщение"
                >
                    ➤
                </button>
                    </>
                )}
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