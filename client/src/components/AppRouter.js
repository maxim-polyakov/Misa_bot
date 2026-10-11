import { Context } from "../index.js";
import { useContext, useState, useEffect } from "react";
import { Route, Routes, Navigate, Outlet, useLocation } from "react-router-dom";
import { authRoutes, publicRoutes } from "../Routes.js";
import { observer } from "mobx-react-lite";
import MainLayout from "../pages/MainLayout";
import Chat from "../pages/Chat";
import Auth from "../pages/Auth";

const AppRouter = observer(() => {
    const { user } = useContext(Context);
    const [isAuth, setIsAuth] = useState(false);
    const [isLoading, setIsLoading] = useState(true); // Add loading state

    useEffect(() => {
        const savedAuth = localStorage.getItem('userIsAuth');
        if (savedAuth === 'true') {
            user.setIsAuth(true);
            setIsAuth(true);
        } else {
            setIsAuth(false);
        }
        setIsLoading(false); // Authentication check complete
    }, [user]);

    useEffect(() => {
        if (user?.isAuth !== undefined) {
            setIsAuth(user.isAuth);
            localStorage.setItem('userIsAuth', JSON.stringify(user.isAuth));
        }
    }, [user?.isAuth]);

    // Protected layout with loading check
    const ProtectedLayout = () => {
        if (isLoading) {
            return <div>Loading...</div>; // Or your custom loader
        }

        return isAuth ? (
            <MainLayout>
                <Outlet />
            </MainLayout>
        ) : (
            <Navigate to="/" replace />
        );
    };

    const HomeRoute = () => (
        isAuth ? (
            <MainLayout>
                <Chat />
            </MainLayout>
        ) : (
            <Auth />
        )
    );

    const LegacyLoginRoute = () => {
        const location = useLocation();
        return <Navigate to={`/${location.search}${location.hash}`} replace />;
    };

    // Show loading during authentication check
    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <Routes>
            <Route path="/" element={<HomeRoute />} />
            <Route path="/login" element={<LegacyLoginRoute />} />
            <Route path="/chat" element={<Navigate to="/" replace />} />

            {/* Публичные маршруты первыми — /share должен быть доступен без входа */}
            {publicRoutes.map(({ path, Component }) => (
                <Route
                    key={path}
                    path={path}
                    element={<Component />}
                />
            ))}

            {/* Protected routes inside MainLayout */}
            <Route element={<ProtectedLayout />}>
                {authRoutes.map(({ path, Component }) => (
                    <Route
                        key={path}
                        path={path}
                        element={<Component />}
                    />
                ))}
            </Route>

            {/* Fallback routes */}
            <Route
                path="*"
                element={<Navigate to="/" replace />}
            />
        </Routes>
    );
});

export default AppRouter;