import { $host, $authhost} from ".";
import { jwtDecode } from "jwt-decode";

const extractApiError = (error) => {
    if (typeof error.response?.data === 'string' && error.response?.data?.includes?.('<!DOCTYPE html>')) {
        const m = error.response.data.match(/Error: (.+?)(<br>|\n|$)/);
        return m?.[1]?.trim() || "Ошибка";
    }
    return error.response?.data?.message || error.message || "Ошибка";
};

export const sendRegistrationCode = async (email, password) => {
    try {
        const { data } = await $host.post("auth/register/send-code/", { email, password });
        return data;
    } catch (error) {
        throw new Error(extractApiError(error));
    }
};

export const sendForgotPasswordCode = async (email) => {
    try {
        const { data } = await $host.post("auth/forgot-password/send-code/", { email });
        return data;
    } catch (error) {
        throw new Error(extractApiError(error));
    }
};

export const verifyForgotPasswordCode = async (email, code, newPassword) => {
    try {
        const { data } = await $host.post("auth/forgot-password/verify/", {
            email,
            code,
            new_password: newPassword,
        });
        localStorage.setItem("token", data.data.token);
        const decoded = jwtDecode(data.data.token);
        const userFromServer = data.data.user || {};
        return { ...decoded, ...userFromServer };
    } catch (error) {
        throw new Error(extractApiError(error));
    }
};

export const verifyRegistrationCode = async (email, password, code) => {
    try {
        const { data } = await $host.post("auth/register/verify/", { email, password, code });
        localStorage.setItem("token", data.data.token);
        const decoded = jwtDecode(data.data.token);
        const userFromServer = data.data.user || {};
        return { ...decoded, ...userFromServer };
    } catch (error) {
        throw new Error(extractApiError(error));
    }
};

export const registration = async (email, password) => {
    try {
        const { data } = await $host.post("auth/register/", {
            email,
            password,
        });
        localStorage.setItem("token", data.data.token);
        const decoded = jwtDecode(data.data.token);
        const userFromServer = data.data.user || {};
        const result = { ...decoded, ...userFromServer };
        if (result.display_name || result.picture) {
            localStorage.setItem("userProfile", JSON.stringify({
                display_name: result.display_name,
                picture: result.picture,
            }));
        }
        return result;
    } catch (error) {
        throw new Error(extractApiError(error));
    }
};

export const login = async (email, password) => {
    try {
        const { data } = await $host.post("auth/login/", {
            email,
            password,
        });
        const token = data.data.token.toString();
        localStorage.setItem("token", token);
        const decoded = jwtDecode(data.data.token);
        const userFromServer = data.data.user || {};
        const result = { ...decoded, ...userFromServer };
        if (result.display_name || result.picture) {
            localStorage.setItem("userProfile", JSON.stringify({
                display_name: result.display_name,
                picture: result.picture,
            }));
        }
        return result;
    } catch (error) {
        console.log("Login error:", error);

        let errorMessage = "Ошибка авторизации";

        // Обработка ошибок БИЗНЕС-ЛОГИКИ (сервер ответил с ошибкой)
        if (error.response) {
            // Сервер ответил, но с ошибкой (4xx, 5xx)
            if (error.response.status === 404) {
                if (error.response.data?.message) {
                    errorMessage = error.response.data.message;
                } else if (typeof error.response.data === 'string') {
                    const match = error.response.data.match(/Пользователь не найден|User not found/i);
                    errorMessage = match ? match[0] : "Ресурс не найден";
                } else {
                    errorMessage = "Пользователь не найден";
                }
            } else if (error.response.status === 401) {
                errorMessage = "Неверный email или пароль";
            } else if (error.response.status === 403 && error.response?.data?.message === "email_not_verified") {
                errorMessage = "email_not_verified";
            } else if (error.response.status === 400) {
                errorMessage = error.response.data?.message || "Неверные данные";
            } else if (error.response.data?.message) {
                errorMessage = error.response.data.message;
            }
        }
        // Обработка ошибок ПОДКЛЮЧЕНИЯ (сервер не ответил)
        else if (error.code === 'NETWORK_ERROR' || error.code === 'ECONNREFUSED') {
            errorMessage = "Не удалось подключиться к серверу";
        }
        // Обработка других ошибок
        else if (error.message) {
            errorMessage = error.message;
        }

        throw new Error(errorMessage);
    }
};

/**
 * Обмен OAuth code на JWT (по аналогии с e-commerce-java-two).
 * Вызывается после редиректа с Google с ?oauth=google&code=xxx
 */
export const exchangeOAuthCode = async (code) => {
    try {
        const { data } = await $host.get(`auth/oauth-token/?code=${encodeURIComponent(code)}`);
        localStorage.setItem("token", data.jwt);
        const decoded = jwtDecode(data.jwt);
        if (decoded.display_name || decoded.picture) {
            localStorage.setItem("userProfile", JSON.stringify({
                display_name: decoded.display_name,
                picture: decoded.picture,
            }));
        }
        return decoded;
    } catch (error) {
        console.log("Google OAuth exchange error:", error);
        let detail = error.response?.data?.message
            ?? error.response?.data?.data?.message
            ?? (error.response?.data && typeof error.response.data === "string" ? error.response.data.slice(0, 200) : null)
            ?? error.message;
        const status = error.response?.status;
        const msg = status ? `Ошибка входа через Google (HTTP ${status}): ${detail}` : `Ошибка входа через Google: ${detail}`;
        throw new Error(msg);
    }
};

/**
 * Выход со всех устройств: инвалидирует все токены пользователя на сервере
 */
export const logoutAll = async () => {
    try {
        await $authhost.post("auth/logout-all/");
    } catch (error) {
        console.warn("logoutAll API error:", error?.response?.data || error?.message);
        // Продолжаем локальный выход даже при ошибке API
    }
};

/**
 * Удаление аккаунта: удаляет пользователя на сервере (необратимо)
 */
export const deleteAccount = async () => {
    try {
        const { data } = await $authhost.post("auth/delete-account/");
        if (data?.status === "error") {
            throw new Error(data?.message || "Не удалось удалить аккаунт");
        }
    } catch (error) {
        throw new Error(extractApiError(error));
    }
};

export const check = async () => {
    try {
        // Проверяем наличие токена в localStorage перед запросом
        const token = localStorage.getItem("token");
        if (!token) {
            console.log("Токен не найден в localStorage");
            return null;
        }

        const { data } = await $authhost.get("auth/check/");
        const payload = data?.data ?? data;

        if (payload?.token) {
            const newToken = payload.token;
            localStorage.setItem("token", newToken);
            const decoded = jwtDecode(newToken);
            const userFromServer = payload.user || {};
            const stored = JSON.parse(localStorage.getItem("userProfile") || "{}");
            // display_name и picture: ответ → JWT → localStorage (fallback после refresh)
            const display_name = userFromServer.display_name ?? decoded.display_name ?? stored.display_name ?? decoded.email?.split("@")[0];
            const picture = userFromServer.picture ?? decoded.picture ?? stored.picture;
            const result = { ...decoded, ...userFromServer, display_name, picture };
            if (display_name || picture) {
                localStorage.setItem("userProfile", JSON.stringify({ display_name, picture }));
            }
            return result;
        }

    } catch (error) {
        console.log("Ошибка проверки авторизации:", error.response?.data || error.message);
        if (error.response?.status === 401) {
            console.log("Удаляем невалидный токен");
            localStorage.removeItem("token");
            localStorage.removeItem("currentUser");
            localStorage.removeItem("currentUserId");
            localStorage.removeItem("userProfile");
            localStorage.setItem("userIsAuth", "false");
            return null;
        }
        // При сетевой ошибке (сервер недоступен, пересборка) — не очищаем данные,
        // возвращаем пользователя из токена, если он ещё действителен
        const token = localStorage.getItem("token");
        if (token) {
            try {
                const decoded = jwtDecode(token);
                if (decoded.exp && decoded.exp * 1000 > Date.now()) {
                    const stored = JSON.parse(localStorage.getItem("userProfile") || "{}");
                    return {
                        ...decoded,
                        user_id: decoded.user_id ?? decoded.id,
                        display_name: decoded.display_name ?? stored.display_name ?? decoded.email?.split("@")[0],
                        picture: decoded.picture ?? stored.picture,
                    };
                }
            } catch {
                /* token invalid */
            }
        }
        return null;
    }
};
