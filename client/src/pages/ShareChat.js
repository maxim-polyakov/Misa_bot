import { useState, useEffect } from "react";
import { useParams, useSearchParams, Link } from "react-router-dom";
import CachedImage from "./CachedImage";
import { useLocale } from "../contexts/LocaleContext";
import "./Styles.css";

const API_URL = process.env.REACT_APP_API_URL || '';

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

const ShareChat = () => {
    const { chatId } = useParams();
    const [searchParams] = useSearchParams();
    const { t } = useLocale();
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!chatId) {
            setLoading(false);
            setError('No chat ID');
            return;
        }
        const msgIds = searchParams.get('msg');
        const shareUrl = `${API_URL}/api/chats/${encodeURIComponent(chatId)}/share/${msgIds ? `?msg=${encodeURIComponent(msgIds)}` : ''}`;
        const fetchChat = async () => {
            try {
                const res = await fetch(shareUrl);
                const json = await res.json().catch(() => ({}));
                if (json.status === 'error') {
                    setError(json.message || 'Chat not found');
                } else if (json.data) {
                    setData(json.data);
                } else {
                    setError('Chat not found');
                }
            } catch (e) {
                setError('Failed to load chat');
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        fetchChat();
    }, [chatId, searchParams]);

    // Обновляем title для SEO и превью при шаринге (хук должен быть до любых return)
    useEffect(() => {
        if (data?.title) {
            document.title = `${data.title} | Misa AI`;
            return () => { document.title = 'Misa AI Chat'; };
        }
    }, [data?.title]);

    // Прокрутка в начало при загрузке контента
    useEffect(() => {
        if (data && !loading) {
            window.scrollTo(0, 0);
        }
    }, [data, loading]);

    const renderMessage = (msg) => {
        const messageUser = msg.user;
        const messageContent = msg.content;

        const wasImage = msg.isImage ||
            /^(\/images\/|https?:\/\/).+(\.(jpg|jpeg|png|gif|bmp|webp|svg))($|\?)/i.test(messageContent);

        const isRelativeImagePath = /^\/images\/[^\\]+\.(jpg|jpeg|png|gif|bmp|webp|svg)$/i.test(messageContent);
        const imageUrl = isRelativeImagePath
            ? `${API_URL}${messageContent}`
            : messageContent;

        const renderContent = () => {
            if (wasImage) {
                return (
                    <CachedImage
                        src={imageUrl}
                        cacheKey={`share_${msg.id}`}
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

        return (
            <div key={msg.id} className={`message ${messageUser === "Misa" ? "misa-message" : "user-message"}`}>
                <div className="message-content">
                    {renderContent()}
                    <div className="message-time">
                        {msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
                    </div>
                </div>
            </div>
        );
    };

    if (loading) {
        return (
            <div className="share-chat-page">
                <header className="share-chat-topbar">
                    <Link to="/" className="share-chat-logo">
                        <img src="/favicon.ico" alt="Misa" />
                        <span>Misa AI</span>
                    </Link>
                </header>
                <div className="share-chat-loading">{t('shareChatLoading')}</div>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="share-chat-page">
                <header className="share-chat-topbar">
                    <Link to="/" className="share-chat-logo">
                        <img src="/favicon.ico" alt="Misa" />
                        <span>Misa AI</span>
                    </Link>
                </header>
                <div className="share-chat-error">
                    <p>{error || t('shareChatNotFound')}</p>
                    <Link to="/login" className="share-chat-link">{t('shareChatLogin')}</Link>
                </div>
            </div>
        );
    }

    return (
        <div className="share-chat-page">
            <header className="share-chat-topbar">
                <Link to="/" className="share-chat-logo">
                    <img src="/favicon.ico" alt="Misa" />
                    <span>Misa AI</span>
                </Link>
                <span className="share-chat-badge">{t('shareChatBadge')}</span>
            </header>

            <div className="share-chat-body">
                <h1 className="share-chat-title">{data.title || 'Чат'}</h1>
                <div className="share-chat-messages">
                    {(data.messages || []).map(renderMessage)}
                </div>
            </div>

            <footer className="share-chat-footer">
                <Link to="/login" className="share-chat-cta">
                    {t('shareChatCta')}
                </Link>
            </footer>
        </div>
    );
};

export default ShareChat;
