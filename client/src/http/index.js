import axios from "axios";
import { getApiBaseUrl } from "../utils/apiBase";

const apiBase = getApiBaseUrl();

const $host = axios.create({
    baseURL: apiBase || undefined,
});

const $authhost = axios.create({
    baseURL: apiBase || undefined,
});

const authInterceptor = (config) => {
    const token = localStorage.getItem("token");
    // Добавляем токен только если он есть
    if (token) {
        config.headers.authorization = `Bearer ${token}`;
    }
    return config;
};

$authhost.interceptors.request.use(authInterceptor);

export { $host, $authhost };