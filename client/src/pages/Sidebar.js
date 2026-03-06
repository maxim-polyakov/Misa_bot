import { useContext, useState, useRef, useEffect } from "react";
import { Context } from "../index.js";
import Navbar from "react-bootstrap/Navbar";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom";
import "./Styles.css";
import { useStores } from "../store/rootStoreContext";
import { useMenuToggle } from "./MainLayout";
import { useLocale } from "../contexts/LocaleContext";
import SettingsModal from "./SettingsModal";

const Sidebar = observer(() => {
    const { user } = useContext(Context);
    const { t } = useLocale();
    const { chatStore } = useStores();
    const { closeSidebar, sidebarExpanded, toggleSidebar } = useMenuToggle();
    const navigate = useNavigate();
    const [profileOpen, setProfileOpen] = useState(false);
    const [settingsOpen, setSettingsOpen] = useState(false);
    const [chatMenuOpen, setChatMenuOpen] = useState(null); // chatId or null
    const [editingChatId, setEditingChatId] = useState(null); // chatId или null — inline переименование
    const profileRef = useRef(null);
    const chatMenuRef = useRef(null);
    const renameInputRef = useRef(null);

    const storedProfile = (() => {
        try {
            return JSON.parse(localStorage.getItem("userProfile") || "{}");
        } catch {
            return {};
        }
    })();
    const displayName = user?.user?.display_name ?? storedProfile.display_name;
    const email = user?.user?.email || chatStore?.user || "";
    // Если display_name — это только часть до @ (авто-сгенерировано), показываем email с маскировкой
    const isAutoDisplayName = !displayName || displayName === email?.split("@")[0];
    const rawLabel = isAutoDisplayName ? email : displayName;
    const maskEmail = (e) => {
        if (!e || !e.includes("@")) return rawLabel || "-";
        const [local, domain] = e.split("@");
        if (local.length <= 2) return e;
        return local.slice(0, 2) + "*".repeat(Math.min(local.length - 2, 5)) + local.slice(-2) + "@" + domain;
    };
    const profileLabel = isAutoDisplayName && rawLabel ? maskEmail(rawLabel) : rawLabel;
    const picture = user?.user?.picture ?? storedProfile.picture;
    const avatarLetter = (typeof rawLabel === "string" && rawLabel.length > 0 ? rawLabel.charAt(0) : "?").toUpperCase();

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (profileRef.current && !profileRef.current.contains(e.target)) {
                setProfileOpen(false);
            }
            if (chatMenuOpen && chatMenuRef.current && !chatMenuRef.current.contains(e.target)) {
                setChatMenuOpen(null);
            }
            if (editingChatId && renameInputRef.current && !renameInputRef.current.closest('.sidebar-chat-item-wrap')?.contains(e.target)) {
                const chat = chatStore.chats.find(c => c.id === editingChatId);
                const val = renameInputRef.current?.value?.trim();
                if (val && chat) chatStore.renameChat(editingChatId, val);
                setEditingChatId(null);
            }
        };
        if (profileOpen || chatMenuOpen || editingChatId) {
            document.addEventListener("mousedown", handleClickOutside);
        }
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [profileOpen, chatMenuOpen, editingChatId, chatStore.chats]);

    const handleSwitchChat = (chatId) => {
        chatStore.switchChat(chatId);
        closeSidebar?.();
    };

    const handleChatMenuToggle = (e, chatId) => {
        e.stopPropagation();
        setChatMenuOpen(prev => prev === chatId ? null : chatId);
    };

    const handleRename = (chatId) => {
        setChatMenuOpen(null);
        setEditingChatId(chatId);
        setTimeout(() => renameInputRef.current?.focus(), 0);
    };

    const handleRenameSubmit = (chatId) => {
        const val = renameInputRef.current?.value?.trim();
        if (val) chatStore.renameChat(chatId, val);
        setEditingChatId(null);
    };

    const handleRenameKeyDown = (e, chatId) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleRenameSubmit(chatId);
        } else if (e.key === 'Escape') {
            setEditingChatId(null);
            renameInputRef.current?.blur();
        }
    };

    const handleDelete = async (chatId) => {
        setChatMenuOpen(null);
        if (window.confirm(t("confirmDeleteChat"))) {
            await chatStore.deleteChat(chatId);
        }
    };

    const handlePin = (chatId) => {
        setChatMenuOpen(null);
        chatStore.togglePinChat(chatId);
    };

    const handleShare = (chatId) => {
        setChatMenuOpen(null);
        chatStore.switchChat(chatId);
        chatStore.startShareMode(chatId);
        closeSidebar?.();
    };

    const logOut = () => {
        setProfileOpen(false);
        chatStore.clearUserFromStorage();
        chatStore.logout();
        user?.setUser({});
        user?.setIsAuth(false);
        navigate("/login", { replace: true });
    };

    if (!user?.isAuth) {
        return null;
    }

    return (
        <>
        <Navbar className="sidebar" bg="dark" data-bs-theme="dark">
                <div className={`sidebar-content ${sidebarExpanded ? "" : "sidebar-content-collapsed"}`}>
                    <div className="sidebar-brand-row">
                        <img src="/favicon.ico" alt="" className="sidebar-logo" />
                        {sidebarExpanded && (
                            <>
                                <span className="sidebar-brand-name">{t("misaChat")}</span>
                                <button
                                    type="button"
                                    className="menu-toggle-btn"
                                    onClick={toggleSidebar}
                                    aria-label="Свернуть меню"
                                    title="Свернуть"
                                >
                                    ☰
                                </button>
                            </>
                        )}
                    </div>
                    <div className="sidebar-new-chat">
                        <button
                            type="button"
                            className="new-chat-button"
                            onClick={() => chatStore.newChat()}
                        >
                            <span className="new-chat-icon">+</span>
                            <span className="new-chat-text">{t("newChat")}</span>
                        </button>
                    </div>
                    <div className="sidebar-chats">
                        {(() => {
                            const groups = chatStore.getChatsGroupedByPeriod();
                            const sections = [
                                { key: 'pinned', label: t('pinned'), chats: groups.pinned },
                                { key: 'today', label: t('today'), chats: groups.today },
                                { key: 'yesterday', label: t('yesterday'), chats: groups.yesterday },
                                { key: 'last7Days', label: t('last7Days'), chats: groups.last7Days },
                                { key: 'last30Days', label: t('last30Days'), chats: groups.last30Days },
                            ];
                            return sections
                                .filter(({ chats }) => chats.length > 0)
                                .map(({ key, label, chats }) => (
                                    <div key={key} className="sidebar-chats-group">
                                        <div className="sidebar-chats-group-title">{label}</div>
                                        {chats.map((chat) => (
                                            <div
                                                key={chat.id}
                                                className={`sidebar-chat-item-wrap ${chat.id === chatStore.currentChatId ? 'active' : ''} ${editingChatId === chat.id ? 'editing' : ''}`}
                                                ref={chatMenuOpen === chat.id ? chatMenuRef : null}
                                            >
                                                {editingChatId === chat.id ? (
                                                    <div className="sidebar-chat-item sidebar-chat-item-editing">
                                                        <span className="sidebar-chat-icon">💬</span>
                                                        <input
                                                            ref={renameInputRef}
                                                            type="text"
                                                            className="sidebar-chat-rename-input"
                                                            defaultValue={chatStore.getChatTitle(chat)}
                                                            onBlur={() => handleRenameSubmit(chat.id)}
                                                            onKeyDown={(e) => handleRenameKeyDown(e, chat.id)}
                                                            onClick={(e) => e.stopPropagation()}
                                                        />
                                                    </div>
                                                ) : (
                                                    <>
                                                        <button
                                                            type="button"
                                                            className="sidebar-chat-item"
                                                            onClick={() => handleSwitchChat(chat.id)}
                                                            title={chat.title || chat.messages?.find(m => m.user !== 'Misa')?.content || ''}
                                                        >
                                                            <span className="sidebar-chat-icon">💬</span>
                                                            <span className="sidebar-chat-title">
                                                                {chatStore.getChatTitle(chat)}
                                                            </span>
                                                        </button>
                                                        <button
                                                            type="button"
                                                            className="sidebar-chat-menu-btn"
                                                            onClick={(e) => handleChatMenuToggle(e, chat.id)}
                                                            aria-label={t("rename")}
                                                            title="Меню"
                                                        >
                                                            ⋯
                                                        </button>
                                                    </>
                                                )}
                                                {chatMenuOpen === chat.id && editingChatId !== chat.id && (
                                                    <div className="sidebar-chat-menu">
                                                        <button type="button" className="sidebar-chat-menu-item" onClick={() => handleRename(chat.id)}>
                                                            <span className="sidebar-chat-menu-icon">✎</span>
                                                            {t("rename")}
                                                        </button>
                                                        <button type="button" className="sidebar-chat-menu-item" onClick={() => handlePin(chat.id)}>
                                                            <span className="sidebar-chat-menu-icon">📌</span>
                                                            {chatStore.isChatPinned(chat.id) ? t("unpin") : t("pin")}
                                                        </button>
                                                        <button type="button" className="sidebar-chat-menu-item" onClick={() => handleShare(chat.id)}>
                                                            <span className="sidebar-chat-menu-icon">⎘</span>
                                                            {t("share")}
                                                        </button>
                                                        <button type="button" className="sidebar-chat-menu-item sidebar-chat-menu-item-delete" onClick={() => handleDelete(chat.id)}>
                                                            <span className="sidebar-chat-menu-icon">🗑</span>
                                                            {t("delete")}
                                                        </button>
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                ));
                        })()}
                    </div>
                    <div className="sidebar-footer" ref={profileRef}>
                        <button
                            type="button"
                            className="sidebar-profile-trigger"
                            onClick={() => setProfileOpen(!profileOpen)}
                            aria-expanded={profileOpen}
                            aria-haspopup="true"
                        >
                            <div className="sidebar-profile-avatar">
                                {picture ? (
                                    <img src={picture} alt="" className="sidebar-profile-avatar-img" referrerPolicy="no-referrer" />
                                ) : (
                                    avatarLetter
                                )}
                            </div>
                            <span className="sidebar-profile-name">{profileLabel}</span>
                            <span className="sidebar-profile-dots">⋯</span>
                        </button>
                        {profileOpen && (
                            <div className="sidebar-profile-panel">
                                <button type="button" className="sidebar-profile-item" onClick={() => { setProfileOpen(false); setSettingsOpen(true); }}>
                                    <span className="sidebar-profile-item-icon">⚙</span>
                                    {t("settings")}
                                </button>
                                <button type="button" className="sidebar-profile-item" onClick={() => { setProfileOpen(false); /* TODO: помощь */ }}>
                                    <span className="sidebar-profile-item-icon">?</span>
                                    {t("helpFeedback")}
                                </button>
                                <button type="button" className="sidebar-profile-item sidebar-profile-item-logout" onClick={logOut}>
                                    <span className="sidebar-profile-item-icon">→</span>
                                    {t("logout")}
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </Navbar>
        <SettingsModal isOpen={settingsOpen} onClose={() => setSettingsOpen(false)} />
        </>
    );
});

export default Sidebar;