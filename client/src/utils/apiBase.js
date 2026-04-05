/**
 * Базовый URL API. Если REACT_APP_API_URL не задан при сборке — используется origin
 * (подходит, когда nginx проксирует /api на тот же домен, что и SPA).
 */
export function getApiBaseUrl() {
    const env = (process.env.REACT_APP_API_URL || "").trim().replace(/\/+$/, "");
    if (env) return env;
    if (typeof window !== "undefined" && window.location?.origin) {
        return window.location.origin;
    }
    return "";
}
