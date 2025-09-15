import { makeAutoObservable } from "mobx";

class ChatStore {
    messages = [];
    isConnected = false;
    isConnecting = false;
    isLoading = false;
    error = null;
    socket = null;
    reconnectAttempts = 0;
    maxReconnectAttempts = 8;
    reconnectDelay = 1000;

    constructor() {
        makeAutoObservable(this);
        this.loadMessages(); // Загружаем сообщения при инициализации
        this.connect();
    }

    // Загрузка сообщений из localStorage
    loadMessages = () => {
        try {
            const savedMessages = localStorage.getItem('chatMessages');
            if (savedMessages) {
                const parsedMessages = JSON.parse(savedMessages);
                // Восстанавливаем объекты Date из строк
                this.messages = parsedMessages.map(msg => ({
                    ...msg,
                    timestamp: new Date(msg.timestamp)
                }));
                console.log("Сообщения загружены из localStorage:", this.messages.length);
            }
        } catch (error) {
            console.error("Ошибка при загрузке сообщений:", error);
            // Очищаем поврежденные данные
            localStorage.removeItem('chatMessages');
        }
    };

    // Сохранение сообщений в localStorage
    saveMessages = () => {
        try {
            localStorage.setItem('chatMessages', JSON.stringify(this.messages));
        } catch (error) {
            console.error("Ошибка при сохранении сообщений:", error);
        }
    };

    // Очистка истории сообщений
    clearMessages = () => {
        this.messages = [];
        localStorage.removeItem('chatMessages');
    };

    connect = () => {
        if (this.isConnecting || this.isConnected) return;

        this.isConnecting = true;
        this.error = null;

        try {
            const wsUrl = process.env.REACT_APP_API_WSS;
            console.log("Подключаемся к:", wsUrl);
            this.socket = new WebSocket(wsUrl);

            this.socket.onopen = () => {
                this.isConnected = true;
                this.isConnecting = false;
                this.reconnectAttempts = 0;
                this.reconnectDelay = 1000;
                console.log("WebSocket соединение установлено");
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleIncomingMessage(data);
                } catch (error) {
                    console.error("Ошибка парсинга сообщения:", error, event.data);
                }
            };

            this.socket.onclose = (event) => {
                this.isConnected = false;
                this.isConnecting = false;
                console.log("WebSocket соединение закрыто", event.code, event.reason);

                if (event.code === 1006) {
                    this.error = "Ошибка подключения (1006). Проверьте консоль для деталей.";
                }

                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    setTimeout(() => {
                        this.reconnectAttempts++;
                        this.reconnectDelay = Math.min(this.reconnectDelay * 1.5, 30000);
                        console.log(`Попытка переподключения #${this.reconnectAttempts} через ${this.reconnectDelay}ms`);
                        this.connect();
                    }, this.reconnectDelay);
                }
            };

            this.socket.onerror = (error) => {
                this.isConnecting = false;
                this.error = "Ошибка подключения к серверу";
                console.error("WebSocket ошибка:", error);
            };

            setTimeout(() => {
                if (!this.isConnected && this.isConnecting) {
                    this.socket?.close();
                    this.isConnecting = false;
                    this.error = "Таймаут подключения (10 секунд)";
                    console.error("Таймаут подключения");
                }
            }, 10000);

        } catch (error) {
            this.isConnecting = false;
            this.error = "Не удалось установить соединение";
            console.error("Ошибка создания WebSocket:", error);
        }
    };

    handleIncomingMessage = (data) => {
        if (data.type === 'chat_message') {
            const botMessage = {
                id: Date.now().toString(),
                content: data.message,
                user: data.user || "Misa",
                timestamp: new Date(),
            };

            this.messages.push(botMessage);
            this.isLoading = false;
            this.saveMessages(); // Сохраняем после добавления нового сообщения
        }
        else if (data.type === 'error') {
            this.error = data.message || "Произошла ошибка";
            this.isLoading = false;
        }
        else if (data.type === 'connection_established') {
            console.log("Соединение подтверждено сервером");
        }
        else {
            console.log("Неизвестный тип сообщения:", data);
        }
    };

    sendMessage = async (content) => {
        if (!this.isConnected || !this.socket) {
            this.error = "Нет соединения с сервером";
            return false;
        }

        this.isLoading = true;
        this.error = null;

        const userMessage = {
            id: Date.now().toString(),
            content,
            user: "Вы",
            timestamp: new Date(),
        };

        this.messages.push(userMessage);
        this.saveMessages(); // Сохраняем после добавления сообщения пользователя

        try {
            this.socket.send(content);
            return true;
        } catch (error) {
            this.error = "Ошибка при отправке сообщения";
            this.isLoading = false;
            console.error("Ошибка отправки сообщения:", error);
            return false;
        }
    };

    disconnect = () => {
        if (this.socket) {
            this.socket.close(1000, "Пользователь закрыл соединение");
            this.socket = null;
        }
        this.isConnected = false;
        this.isConnecting = false;
    };

    clearError = () => {
        this.error = null;
    };

    cleanup = () => {
        this.disconnect();
    };
}

export default ChatStore;