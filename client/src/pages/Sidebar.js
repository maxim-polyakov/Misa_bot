import { useContext } from "react";
import { Context } from "../index.js";
import Navbar from "react-bootstrap/Navbar";
import { Button, Nav } from "react-bootstrap";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom"; // Добавьте этот импорт
import "./Sidebar.css";

const Sidebar = observer(() => {
    const { user } = useContext(Context);
    const navigate = useNavigate(); // Используйте хук навигации

    const logOut = () => {
        user?.setUser({});
        user?.setIsAuth(false);
        localStorage.removeItem("token");
        navigate("/login", { replace: true }); // Программное перенаправление
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
                    {/* Бренд сверху */}
                    <div className="sidebar-brand">
                        <Navbar.Brand href="/">Ваш Логотип</Navbar.Brand>
                    </div>

                    {/* Навигация по центру */}
                    <Nav className="flex-column w-100">
                        <Nav.Link href="/profile" className="sidebar-link">
                            Профиль
                        </Nav.Link>
                        <Nav.Link href="/settings" className="sidebar-link">
                            Настройки
                        </Nav.Link>
                        <Nav.Link href="/dashboard" className="sidebar-link">
                            Дашборд
                        </Nav.Link>
                    </Nav>

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