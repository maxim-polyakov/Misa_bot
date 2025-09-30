import { Context } from "../index.js";
import { useContext, useState, useEffect } from "react";
import { Route, Routes, Navigate, Outlet } from "react-router-dom";
import { authRoutes, publicRoutes } from "../Routes.js";
import { observer } from "mobx-react-lite";
import MainLayout from "../pages/MainLayout";
import { LOGIN_ROUTE } from "../utils/consts.js";

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
            <Navigate to={LOGIN_ROUTE} replace />
        );
    };

    // Show loading during authentication check
    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <Routes>
            {/* Protected routes inside MainLayout */}
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

            {/* Public routes - without MainLayout */}
            {publicRoutes.map(({ path, Component }) => (
                <Route
                    key={path}
                    path={path}
                    element={<Component />}
                />
            ))}

            {/* Fallback routes */}
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