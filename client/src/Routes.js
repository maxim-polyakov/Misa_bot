// routes.js
import Chat from "./pages/Chat";
import Auth from "./pages/Auth";
import VerifyCode from "./pages/VerifyCode";
import {
    CHAT_ROUTE,
    LOGIN_ROUTE,
    REGISTRATION_ROUTE,
    REGISTRATION_VERIFY_ROUTE
} from "./utils/consts";

export const authRoutes = [
    {
        path: CHAT_ROUTE,
        Component: Chat
    }
];

export const publicRoutes = [
    {
        path: LOGIN_ROUTE,
        Component: Auth
    },
    {
        path: REGISTRATION_ROUTE,
        Component: Auth
    },
    {
        path: REGISTRATION_VERIFY_ROUTE,
        Component: VerifyCode
    }
];