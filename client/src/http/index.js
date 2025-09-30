import axios from "axios";


const $host = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
});

$host.interceptors.request.use(request => {
    console.log('Отправляемые заголовки:', request.headers);
    return request;
});
export { $host };
