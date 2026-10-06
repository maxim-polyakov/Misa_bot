/**
 * Базовый URL API.
 * В production фронт (misa.baxic.ru) и API (misaapi.baxic.ru) на разных доменах —
 * REACT_APP_API_URL должен быть вшит на этапе yarn build (CLIENT_ENV / Dockerfile ARG).
 */
export function getApiBaseUrl() {
    const env = (process.env.REACT_APP_API_URL || "").trim().replace(/\/+$/, "");
    if (env) return env;
    if (typeof window !== "undefined" && window.location?.origin) {
        const origin = window.location.origin.replace(/\/+$/, "");
        try {
            const u = new URL(origin);
            if (u.hostname.startsWith("misa.") && !u.hostname.startsWith("misaapi.")) {
                u.hostname = "misaapi." + u.hostname.slice("misa.".length);
                return u.origin;
            }
        } catch {
            /* ignore */
        }
        return origin;
    }
    return "";
}
