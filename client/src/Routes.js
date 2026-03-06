// routes.js
import Chat from "./pages/Chat";
import ShareChat from "./pages/ShareChat";
import Auth from "./pages/Auth";
import VerifyCode from "./pages/VerifyCode";
import ForgotPasswordRequest from "./pages/ForgotPasswordRequest";
import ForgotPasswordVerify from "./pages/ForgotPasswordVerify";
import {
    CHAT_ROUTE,
    SHARE_ROUTE,
    LOGIN_ROUTE,
    REGISTRATION_ROUTE,
    REGISTRATION_VERIFY_ROUTE,
    FORGOT_PASSWORD_ROUTE,
    FORGOT_PASSWORD_VERIFY_ROUTE
} from "./utils/consts";

export const authRoutes = [
    {
        path: CHAT_ROUTE,
        Component: Chat
    }
];

export const publicRoutes = [
    {
        path: `${SHARE_ROUTE}/:chatId`,
        Component: ShareChat
    },
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
    },
    {
        path: FORGOT_PASSWORD_ROUTE,
        Component: ForgotPasswordRequest
    },
    {
        path: FORGOT_PASSWORD_VERIFY_ROUTE,
        Component: ForgotPasswordVerify
    }
];