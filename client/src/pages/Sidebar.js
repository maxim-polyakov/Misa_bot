import { useContext } from "react";
import { Context } from "../index.js";
import Navbar from "react-bootstrap/Navbar";
import { Button, Nav } from "react-bootstrap";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom";
import { useMenuToggle } from "./MainLayout"; // Добавьте этот импорт
import "./Styles.css";

const Sidebar = observer(() => {
    const { user } = useContext(Context);
    const navigate = useNavigate();
    const { isSidebarOpen, closeSidebar } = useMenuToggle(); // Получите состояние и функцию

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
            <div className="sidebar-overlay mobile-open" />

            <Navbar className="sidebar" bg="dark" data-bs-theme="dark">
                <div className="sidebar-content">

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