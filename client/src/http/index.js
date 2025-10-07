import axios from "axios";

const $host = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
});

const $authhost = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
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