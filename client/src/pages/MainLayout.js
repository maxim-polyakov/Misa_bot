import { useState, useContext, createContext, useMemo, useCallback } from "react";
import { Context } from "../index";
import Sidebar from "../pages/Sidebar";
import "./MainLayout.css";

// Create context for menu toggle
export const MenuToggleContext = createContext();

export const useMenuToggle = () => {
    const context = useContext(MenuToggleContext);
    if (context === undefined) {
        throw new Error('useMenuToggle must be used within a MenuToggleProvider');
    }
    return context;
};

const MainLayout = ({ children }) => {
    const { user } = useContext(Context);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    // Используем useCallback для стабильности функций
    const toggleSidebar = useCallback(() => {
        setIsSidebarOpen(prev => !prev);
    }, []);

    const closeSidebar = useCallback(() => {
        setIsSidebarOpen(false);
    }, []);

    // Memoize context value to prevent unnecessary re-renders
    const contextValue = useMemo(() => ({
        isSidebarOpen,
        toggleSidebar,
        closeSidebar
    }), [isSidebarOpen, toggleSidebar, closeSidebar]);

    return (
        <MenuToggleContext.Provider value={contextValue}>
            <div className="main-layout">
                {/* Sidebar with accessibility improvements */}
                {user?.isAuth && (
                    <div
                        className={`sidebar-wrapper ${isSidebarOpen ? 'mobile-open' : ''}`}
                        inert={!isSidebarOpen ? "" : undefined} // Apply inert when sidebar is closed
                    >
                        <Sidebar />
                    </div>
                )}

                {/* Overlay with enhanced accessibility */}
                {isSidebarOpen && (
                    <div
                        className="sidebar-overlay"
                        onClick={closeSidebar}
                        role="button"
                        aria-label="Close menu"
                        tabIndex={0}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' || e.key === ' ') {
                                closeSidebar();
                            }
                        }}
                    />
                )}

                {/* Main content */}
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