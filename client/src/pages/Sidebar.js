// Sidebar.jsx
import { useContext } from "react";
import { Context } from "../index.js";
import Navbar from "react-bootstrap/Navbar";
import { Button, Nav } from "react-bootstrap";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom";
import { useMenuToggle } from "./MainLayout"; // Импортируем хук
import "./Sidebar.css";

const Sidebar = observer(({ onClose } ) => {
    const { user } = useContext(Context);
    const navigate = useNavigate();
    const { closeSidebar } = useMenuToggle(); // Получаем функцию закрытия

    const logOut = () => {
        user?.setUser({});
        user?.setIsAuth(false);
        localStorage.removeItem("token");
        navigate("/login", { replace: true });
    };

    if (!user?.isAuth) {
        return null;
    }

    return (
        <>
            {/* Оверлей для мобильных */}
            <div className="sidebar-overlay" onClick={closeSidebar} />

            <Navbar className="sidebar" bg="dark" data-bs-theme="dark">
                <div className="sidebar-content">
                    {/* Заголовок с кнопкой закрытия */}
                    <div className="sidebar-header">
                        <Navbar.Brand href="/">Ваш Логотип</Navbar.Brand>
                        <button onClick={onClose} className="sidebar-close" title="Закрыть меню">
                            ×
                        </button>
                    </div>
                    {/* Кнопка выхода внизу */}
                    <div className="sidebar-footer">
                        <Button
                            variant="outline-light"
                            className="w-100"
                            onClick={logOut}
                        >
                            Выйти
                        </Button>
                    </div>
                </div>
            </Navbar>
        </>
    );
});

export default Sidebar;