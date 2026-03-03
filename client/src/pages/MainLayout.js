import { useState, useContext, createContext, useMemo, useCallback, useEffect } from "react";
import { Context } from "../index";
import Sidebar from "../pages/Sidebar";
import "./Styles.css";

// Create context for menu toggle
export const MenuToggleContext = createContext();

export const useMenuToggle = () => {
    const context = useContext(MenuToggleContext);
    if (context === undefined) {
        throw new Error('useMenuToggle must be used within a MenuToggleProvider');
    }
    return context;
};

const SIDEBAR_COLLAPSED_KEY = "misa_sidebar_collapsed";

const MainLayout = ({ children }) => {
    const { user } = useContext(Context);
    const [sidebarExpanded, setSidebarExpanded] = useState(() => {
        if (typeof window === "undefined") return true;
        if (window.innerWidth <= 768) return false;
        try {
            return localStorage.getItem(SIDEBAR_COLLAPSED_KEY) !== "true";
        } catch {
            return true;
        }
    });
    const [isMobile, setIsMobile] = useState(typeof window !== "undefined" && window.innerWidth <= 768);

    useEffect(() => {
        const mq = window.matchMedia("(max-width: 768px)");
        const handler = () => {
            const mobile = mq.matches;
            setIsMobile(mobile);
            if (mobile) setSidebarExpanded(false);
        };
        handler();
        mq.addEventListener("change", handler);
        return () => mq.removeEventListener("change", handler);
    }, []);

    useEffect(() => {
        if (!isMobile) {
            try {
                const saved = localStorage.getItem(SIDEBAR_COLLAPSED_KEY);
                setSidebarExpanded(saved !== "true");
            } catch {}
        }
    }, [isMobile]);

    const toggleSidebar = useCallback(() => {
        setSidebarExpanded(prev => {
            const next = !prev;
            if (!isMobile) {
                try {
                    localStorage.setItem(SIDEBAR_COLLAPSED_KEY, (!next).toString());
                } catch {}
            }
            return next;
        });
    }, [isMobile]);

    const closeSidebar = useCallback(() => {
        if (isMobile) setSidebarExpanded(false);
    }, [isMobile]);

    const openSidebar = useCallback(() => {
        setSidebarExpanded(true);
    }, []);

    const contextValue = useMemo(() => ({
        sidebarExpanded,
        isMobile,
        toggleSidebar,
        closeSidebar,
        openSidebar
    }), [sidebarExpanded, isMobile, toggleSidebar, closeSidebar, openSidebar]);

    const showOverlay = isMobile && sidebarExpanded;

    return (
        <MenuToggleContext.Provider value={contextValue}>
            <div className="main-layout">
                {user?.isAuth && (
                    <>
                        {/* Рейка с единой кнопкой — всегда видна */}
                        <div className="sidebar-rail">
                            <button
                                type="button"
                                className="sidebar-rail-btn"
                                onClick={toggleSidebar}
                                aria-label={sidebarExpanded ? "Свернуть меню" : "Развернуть меню"}
                                title={sidebarExpanded ? "Свернуть" : "Развернуть"}
                            >
                                {sidebarExpanded ? "◀" : "☰"}
                            </button>
                        </div>
                        {/* Панель — расширяется вправо от рейки */}
                        <div
                            className={`sidebar-panel ${sidebarExpanded ? "sidebar-panel-open" : ""} ${showOverlay ? "sidebar-panel-mobile-open" : ""}`}
                            inert={isMobile && !sidebarExpanded ? "" : undefined}
                        >
                            <Sidebar />
                        </div>
                    </>
                )}

                {showOverlay && (
                    <div
                        className="sidebar-overlay"
                        onClick={closeSidebar}
                        role="button"
                        aria-label="Закрыть меню"
                        tabIndex={0}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === " ") closeSidebar();
                        }}
                    />
                )}

                <div className="main-content">
                    <div className="chat-container-wrapper">
                        {children}
                    </div>
                </div>
            </div>
        </MenuToggleContext.Provider>
    );
};

export default MainLayout;