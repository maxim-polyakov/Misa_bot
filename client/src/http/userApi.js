import { $host, $authhost} from ".";
import { jwtDecode } from "jwt-decode";

export const registration = async (email, password) => {
    try {
        const { data } = await $host.post("auth/register/", {
            email,
            password,
        });
        localStorage.setItem("token", data.data.token);
        return jwtDecode(data.data.token);
    } catch (error) {
        console.log("Registration error:", error);

        let errorMessage = "Ошибка регистрации";

        if (typeof error.response?.data === 'string' && error.response.data.includes('<!DOCTYPE html>')) {
            const errorMatch = error.response.data.match(/Error: (.+?)(<br>|\n|$)/);
            if (errorMatch && errorMatch[1]) {
                errorMessage = errorMatch[1].trim();
            }
        } else if (error.response?.data?.message) {
            errorMessage = error.response.data.message;
        } else if (error.message) {
            errorMessage = error.message;
        }

        throw new Error(errorMessage);
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
        return jwtDecode(data.data.token);
    } catch (error) {
        console.log("Login error:", error);

        let errorMessage = "Ошибка авторизации";

        // Обработка ошибок БИЗНЕС-ЛОГИКИ (сервер ответил с ошибкой)
        if (error.response) {
            // Сервер ответил, но с ошибкой (4xx, 5xx)
            if (error.response.status === 404) {
                // Это может быть как "Пользователь не найден", так и ошибка маршрута
                // Проверяем, есть ли в ответе сообщение об ошибке
                if (error.response.data?.message) {
                    errorMessage = error.response.data.message; // "Пользователь не найден"
                } else if (typeof error.response.data === 'string') {
                    // Пытаемся извлечь сообщение из HTML/текста
                    const match = error.response.data.match(/Пользователь не найден|User not found/i);
                    errorMessage = match ? match[0] : "Ресурс не найден";
                } else {
                    errorMessage = "Пользователь не найден";
                }
            }
            else if (error.response.status === 401) {
                errorMessage = "Неверный email или пароль";
            }
            else if (error.response.status === 400) {
                errorMessage = error.response.data?.message || "Неверные данные";
            }
            else if (error.response.data?.message) {
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
        return jwtDecode(data.jwt);
    } catch (error) {
        console.log("Google OAuth exchange error:", error);
        let errorMessage = "Ошибка входа через Google. Попробуйте ещё раз.";
        if (error.response?.data?.message) errorMessage = error.response.data.message;
        else if (error.message) errorMessage = error.message;
        throw new Error(errorMessage);
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

        // В зависимости от структуры ответа вашего сервера:

        // Вариант 1: если сервер возвращает обновленный токен
        if (data.data.token) {
            const newToken = data.data.token;
            localStorage.setItem("token", newToken);
            const decoded = jwtDecode(newToken);
            console.log("Новый токен установлен:", decoded);
            return decoded;
        }

    } catch (error) {
        console.log("Ошибка проверки авторизации:", error.response?.data || error.message);
        if (error.response?.status === 401) {
            console.log("Удаляем невалидный токен");
            localStorage.removeItem("token");
            localStorage.removeItem("currentUser");
            localStorage.removeItem("currentUserId");
        }
        return null;
    }
};
