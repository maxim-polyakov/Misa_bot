import {Context} from "../index.js";
import { useContext } from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import { authRoutes, publicRoutes } from "../Routes.js";
import { observer } from "mobx-react-lite";
import Chat from "../pages/Chat.js";

const AppRouter = observer(() => {
    return (
        <Routes>
            {/* Редирект с корневой страницы на чат */}
            <Route path="/" element={<Navigate to="/chat" replace />} />

            {/* Только этот маршрут ведет в чат */}
            <Route path="/chat" element={<Chat />} />

            {/* Все остальные маршруты (если они есть в ваших routes.js) */}
            {publicRoutes.map(({path, Component}) =>
                <Route key={path} path={path} element={<Component />} />
            )}

            {/* Защищенные маршруты (если нужно) */}
            {authRoutes.map(({path, Component}) =>
                <Route key={path} path={path} element={<Component />} />
            )}

            {/* Дефолтный маршрут - можно оставить или изменить */}
            <Route path="*" element={<div>Страница не найдена</div>} />
        </Routes>
    );
});

export default AppRouter;