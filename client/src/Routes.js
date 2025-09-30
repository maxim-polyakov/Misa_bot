// routes.js
import Chat from "./pages/Chat";
import Auth from "./pages/Auth";
import {
    CHAT_ROUTE,
    LOGIN_ROUTE,
    REGISTRATION_ROUTE
} from "./utils/consts";

export const authRoutes = [
    {
        path: CHAT_ROUTE,
        Component: Chat
    }
];

export const publicRoutes = [ // Исправлено: publicRoutes вместо publickRoutes
    {
        path: LOGIN_ROUTE,
        Component: Auth
    },
    {
        path: REGISTRATION_ROUTE,
        Component: Auth
    }
];