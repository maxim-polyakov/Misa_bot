import { Context } from "../index.js";
import { useContext, useState, useEffect } from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import { authRoutes, publicRoutes } from "../Routes.js";
import { observer } from "mobx-react-lite";
import Chat from "../pages/Chat.js";
import { LOGIN_ROUTE } from "../utils/consts.js";

const AppRouter = observer(() => {
    const { user } = useContext(Context);

    // 🔐 Инициализируем состояние из localStorage
    const [isAuth, setIsAuth] = useState(() => {
        const savedAuth = localStorage.getItem('userIsAuth');
        return savedAuth ? JSON.parse(savedAuth) : false;
    });

    // 🔄 Синхронизируем MobX и localStorage
    useEffect(() => {
        if (user?.isAuth !== undefined) {
            setIsAuth(user.isAuth);
            localStorage.setItem('userIsAuth', JSON.stringify(user.isAuth));
        }
    }, [user?.isAuth]);

    // 🚀 Восстанавливаем сессию при загрузке
    useEffect(() => {
        const savedAuth = localStorage.getItem('userIsAuth');
        // Важно: Приведение строки к булеву значению
        if (savedAuth === 'true') {
            console.log("Восстановление статуса авторизации из localStorage");
            // Вызов метода вашего MobX-хранилища для установки флага авторизации
            user.setIsAuth(true);
        }
    }, [user]); // Добавьте `user` в зависимости, если `setIsAuth` является его методом

    console.log("User auth status:", isAuth);

    return (
        <Routes>
            {/* Защищенные маршруты - только для авторизованных */}
            {isAuth &&
                authRoutes.map(({ path, Component }) => (
                    <Route
                        key={path}
                        path={path}
                        element={<Component />}
                    />
                ))}

            {/* Публичные маршруты - доступны всем */}
            {publicRoutes.map(({ path, Component }) => (
                <Route
                    key={path}
                    path={path}
                    element={<Component />}
                />
            ))}

            {/* КОРНЕВОЙ ПУТЬ: Если авторизован - в /chat, если нет - в /login */}
            <Route
                path="/"
                element={
                    isAuth ?
                        <Navigate to="/chat" replace /> :
                        <Navigate to={LOGIN_ROUTE} replace />
                }
            />

            {/* Для всех других путей: если авторизован - галерея, если нет - логин */}
            <Route
                path="*"
                element={
                    isAuth ?
                        <Chat /> :
                        <Navigate to={LOGIN_ROUTE} replace />
                }
            />
        </Routes>
    );
});

export default AppRouter;