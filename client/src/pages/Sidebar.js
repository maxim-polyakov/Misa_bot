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
    const profileRef = useRef(null);

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
        };
        if (profileOpen) {
            document.addEventListener("mousedown", handleClickOutside);
        }
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [profileOpen]);

    const handleSwitchChat = (chatId) => {
        chatStore.switchChat(chatId);
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
                                            <button
                                                key={chat.id}
                                                className={`sidebar-chat-item ${chat.id === chatStore.currentChatId ? 'active' : ''}`}
                                                onClick={() => handleSwitchChat(chat.id)}
                                                title={chat.title || chat.messages?.find(m => m.user !== 'Misa')?.content || ''}
                                            >
                                                <span className="sidebar-chat-icon">💬</span>
                                                <span className="sidebar-chat-title">
                                                    {chatStore.getChatTitle(chat)}
                                                </span>
                                            </button>
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