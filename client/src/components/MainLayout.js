import { useState, useContext, createContext } from "react";
import { Context } from "../index";
import Sidebar from "../pages/Sidebar";
import "./MainLayout.css";

// Create context for menu toggle
export const MenuToggleContext = createContext();

const MainLayout = ({ children }) => {
    const { user } = useContext(Context);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    const closeSidebar = () => {
        setIsSidebarOpen(false);
    };

    return (
        <MenuToggleContext.Provider value={{ toggleSidebar, closeSidebar }}>
            <div className="main-layout">
                {/* Сайдбар */}
                <div className={`sidebar-wrapper ${isSidebarOpen ? 'mobile-open' : ''}`}>
                    <Sidebar />
                </div>

                {/* Оверлей для мобильных */}
                {isSidebarOpen && (
                    <div className="sidebar-overlay" onClick={closeSidebar} />
                )}

                {/* Основной контент */}
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