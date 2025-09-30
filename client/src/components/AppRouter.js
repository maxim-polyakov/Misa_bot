import { Context } from "../index.js";
import { useContext, useState, useEffect } from "react";
import { Route, Routes, Navigate, Outlet } from "react-router-dom";
import { authRoutes, publicRoutes } from "../Routes.js";
import { observer } from "mobx-react-lite";
import MainLayout from "./MainLayout";
import { LOGIN_ROUTE } from "../utils/consts.js";

const AppRouter = observer(() => {
    const { user } = useContext(Context);
    const [isAuth, setIsAuth] = useState(false);

    useEffect(() => {
        if (user?.isAuth !== undefined) {
            setIsAuth(user.isAuth);
            localStorage.setItem('userIsAuth', JSON.stringify(user.isAuth));
        }
    }, [user?.isAuth]);

    useEffect(() => {
        const savedAuth = localStorage.getItem('userIsAuth');
        if (savedAuth === 'true') {
            user.setIsAuth(true);
        }
    }, [user]);

    // Защищенный лейаут - только для авторизованных
    const ProtectedLayout = () => {
        return isAuth ? (
            <MainLayout>
                <Outlet /> {/* Сюда будут рендериться защищенные роуты */}
            </MainLayout>
        ) : (
            <Navigate to={LOGIN_ROUTE} replace />
        );
    };

    return (
        <Routes>
            {/* Защищенные маршруты внутри MainLayout */}
            <Route element={<ProtectedLayout />}>
                {authRoutes.map(({ path, Component }) => (
                    <Route
                        key={path}
                        path={path}
                        element={<Component />}
                    />
                ))}
                <Route path="/" element={<Navigate to="/chat" replace />} />
            </Route>

            {/* Публичные маршруты - без MainLayout */}
            {publicRoutes.map(({ path, Component }) => (
                <Route
                    key={path}
                    path={path}
                    element={<Component />}
                />
            ))}

            {/* Fallback маршруты */}
            <Route
                path="*"
                element={
                    isAuth ?
                        <Navigate to="/chat" replace /> :
                        <Navigate to={LOGIN_ROUTE} replace />
                }
            />
        </Routes>
    );
});

export default AppRouter;