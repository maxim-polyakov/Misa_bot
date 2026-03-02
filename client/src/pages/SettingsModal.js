import { createPortal } from "react-dom";
import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { observer } from "mobx-react-lite";
import JSZip from "jszip";
import { Context } from "../index.js";
import { useStores } from "../store/rootStoreContext";
import { useLocale } from "../contexts/LocaleContext";
import { getTheme, setTheme, THEMES } from "../utils/theme.js";
import { getLanguage, LANGUAGES } from "../utils/locale.js";
import "./Styles.css";

const SettingsModal = observer(({ isOpen, onClose }) => {
    const { user } = useContext(Context);
    const { chatStore } = useStores();
    const { t, setLanguage: setLocale } = useLocale();
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState("profile");
    const [theme, setThemeState] = useState(getTheme);
    const [locale, setLocaleState] = useState(getLanguage);

    const SETTINGS_TABS = [
        { id: "general", label: t("general"), icon: "⚙" },
        { id: "profile", label: t("profile"), icon: "👤" },
        { id: "data", label: t("data"), icon: "📊" },
        { id: "about", label: t("about"), icon: "ℹ" },
    ];

    useEffect(() => {
        if (isOpen) {
            setThemeState(getTheme());
            setLocaleState(getLanguage());
        }
    }, [isOpen]);

    useEffect(() => {
        const handleStorage = () => setThemeState(getTheme());
        window.addEventListener("storage", handleStorage);
        return () => window.removeEventListener("storage", handleStorage);
    }, []);

    const displayName = user?.user?.display_name;
    const email = user?.user?.email || chatStore?.user || "";
    const picture = user?.user?.picture;
    const isGoogleUser = !!picture;

    const maskEmail = (e) => {
        if (!e || !e.includes("@")) return "-";
        const [local, domain] = e.split("@");
        if (local.length <= 2) return e;
        return local.slice(0, 2) + "*".repeat(Math.min(local.length - 2, 5)) + local.slice(-2) + "@" + domain;
    };

    const handleLogout = () => {
        onClose();
        chatStore.clearUserFromStorage();
        chatStore.logout();
        user?.setUser({});
        user?.setIsAuth(false);
        navigate("/login", { replace: true });
    };

    const handleDeleteAccount = () => {
        if (window.confirm("Вы уверены, что хотите удалить аккаунт? Это действие необратимо.")) {
            handleLogout();
            // TODO: вызов API удаления аккаунта
        }
    };

    if (!isOpen) return null;

    return createPortal(
        <div className="settings-modal-overlay" onClick={onClose}>
            <div className="settings-modal" onClick={(e) => e.stopPropagation()}>
                    <div className="settings-modal-header">
                    <h2 className="settings-modal-title">{t("settings")}</h2>
                    <button type="button" className="settings-modal-close" onClick={onClose} aria-label="Закрыть">
                        ×
                    </button>
                </div>
                <div className="settings-modal-body">
                    <nav className="settings-modal-nav">
                        {SETTINGS_TABS.map((tab) => (
                            <button
                                key={tab.id}
                                type="button"
                                className={`settings-modal-nav-item ${tab.id === activeTab ? "active" : ""}`}
                                onClick={() => setActiveTab(tab.id)}
                            >
                                <span className="settings-modal-nav-icon">{tab.icon}</span>
                                {tab.label}
                            </button>
                        ))}
                    </nav>
                    <div className="settings-modal-content">
                        {activeTab === "profile" && (
                        <div className="settings-profile-section">
                            {isGoogleUser && displayName && (
                                <div className="settings-profile-row">
                                    <span className="settings-profile-label">{t("name")}</span>
                                    <span className="settings-profile-value">
                                        {displayName}
                                        <span className="settings-google-badge" title="Вход через Google">G</span>
                                    </span>
                                </div>
                            )}
                            <div className="settings-profile-row">
                                <span className="settings-profile-label">{t("email")}</span>
                                <span className="settings-profile-value">{maskEmail(email) || "-"}</span>
                            </div>
                            <div className="settings-profile-row">
                                <span className="settings-profile-label">{t("phone")}</span>
                                <span className="settings-profile-value">-</span>
                            </div>
                            <div className="settings-profile-row settings-profile-row-actions">
                                <span className="settings-profile-label">{t("logoutAll")}</span>
                                <button type="button" className="settings-btn-logout" onClick={handleLogout}>
                                    {t("logout")}
                                </button>
                            </div>
                            <div className="settings-profile-row settings-profile-row-actions">
                                <span className="settings-profile-label">{t("deleteAccount")}</span>
                                <button type="button" className="settings-btn-delete" onClick={handleDeleteAccount}>
                                    {t("delete")}
                                </button>
                            </div>
                        </div>
                        )}
                        {activeTab === "general" && (
                            <div className="settings-general-section">
                                <div className="settings-theme-block">
                                    <span className="settings-theme-label">{t("theme")}</span>
                                    <div className="settings-theme-options">
                                        <button
                                            type="button"
                                            className={`settings-theme-btn ${theme === THEMES.LIGHT ? "active" : ""}`}
                                            onClick={() => { setTheme(THEMES.LIGHT); setThemeState(THEMES.LIGHT); }}
                                            title={t("themeLight")}
                                        >
                                            <span className="settings-theme-icon">☀</span>
                                            <span>{t("themeLight")}</span>
                                        </button>
                                        <button
                                            type="button"
                                            className={`settings-theme-btn ${theme === THEMES.DARK ? "active" : ""}`}
                                            onClick={() => { setTheme(THEMES.DARK); setThemeState(THEMES.DARK); }}
                                            title={t("themeDark")}
                                        >
                                            <span className="settings-theme-icon">🌙</span>
                                            <span>{t("themeDark")}</span>
                                        </button>
                                        <button
                                            type="button"
                                            className={`settings-theme-btn ${theme === THEMES.SYSTEM ? "active" : ""}`}
                                            onClick={() => { setTheme(THEMES.SYSTEM); setThemeState(THEMES.SYSTEM); }}
                                            title={t("themeSystem")}
                                        >
                                            <span className="settings-theme-icon">💻</span>
                                            <span>{t("themeSystem")}</span>
                                        </button>
                                    </div>
                                </div>
                                <div className="settings-language-block">
                                    <span className="settings-theme-label">{t("language")}</span>
                                    <select
                                        className="settings-language-select"
                                        value={locale}
                                        onChange={(e) => { setLocale(e.target.value); setLocaleState(e.target.value); }}
                                    >
                                        {LANGUAGES.map((lang) => (
                                            <option key={lang.code} value={lang.code}>
                                                {lang.label}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                        )}
                        {activeTab === "data" && (
                            <div className="settings-data-section">
                                <div className="settings-data-block">
                                    <div className="settings-data-block-header">
                                        <span className="settings-data-block-title">{t("exportData")}</span>
                                    </div>
                                    <p className="settings-data-block-desc">{t("exportDataDesc")}</p>
                                    <button
                                        type="button"
                                        className="settings-btn-export"
                                        onClick={async () => {
                                            const zip = new JSZip();
                                            const dateStr = new Date().toISOString().slice(0, 10);
                                            const conversationsData = chatStore.getConversationsExportData();
                                            zip.file("conversations.json", JSON.stringify(conversationsData, null, 2));
                                            const userData = {
                                                exportedAt: new Date().toISOString(),
                                                display_name: displayName || null,
                                                email: email || null,
                                                picture: picture || null,
                                            };
                                            zip.file("user.json", JSON.stringify(userData, null, 2));
                                            const blob = await zip.generateAsync({ type: "blob" });
                                            const url = URL.createObjectURL(blob);
                                            const a = document.createElement("a");
                                            a.href = url;
                                            a.download = `misa_data-${dateStr}.zip`;
                                            a.click();
                                            URL.revokeObjectURL(url);
                                        }}
                                    >
                                        {t("exportButton")}
                                    </button>
                                </div>
                                <div className="settings-data-block">
                                    <div className="settings-data-block-header">
                                        <span className="settings-data-block-title">{t("deleteAllChats")}</span>
                                    </div>
                                    <p className="settings-data-block-desc">{t("deleteAllChatsDesc")}</p>
                                    <button
                                        type="button"
                                        className="settings-btn-delete-all"
                                        onClick={() => {
                                            if (window.confirm(t("confirmDeleteAllChats"))) {
                                                chatStore.deleteAllChats();
                                                onClose();
                                            }
                                        }}
                                    >
                                        {t("deleteAllButton")}
                                    </button>
                                </div>
                            </div>
                        )}
                        {activeTab === "about" && (
                            <div className="settings-placeholder">Misa AI Чат</div>
                        )}
                    </div>
                </div>
            </div>
        </div>,
        document.body
    );
});

export default SettingsModal;
