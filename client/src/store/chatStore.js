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
    user = null; // Добавляем поле для пользователя
    isAuth = false;

    constructor(rootStore) {

        this.rootStore = rootStore;
        makeAutoObservable(this);
        this.loadUserFromStorage();
        this.loadMessages();
    }

    // Получение ID текущего пользователя
    getCurrentUserId() {
        // Пробуем получить из rootStore.user, если есть
        if (this.rootStore?.user?.getCurrentUserId) {
            return this.rootStore.user.getCurrentUserId();
        }
        // Или из локального состояния
        return this.user?.id || localStorage.getItem('currentUserId');
    };

    // Загрузка пользователя из localStorage
    loadUserFromStorage() {
        try {
            const savedUser = localStorage.getItem('currentUser');
            if (savedUser) {
                const userData = savedUser;
                this.user = userData;
                this.isAuth = true;
                console.log("Пользователь загружен из localStorage", this.user);
            }
        } catch (error) {
            console.error("Ошибка загрузки пользователя:", error);
            this.clearUserFromStorage();
        }
    };

    // Сохранение пользователя в localStorage
    saveUserToStorage() {
        if (this.user && this.isAuth) {
            try {
                localStorage.setItem('currentUser', JSON.stringify(this.user));
                console.log("Пользователь сохранен в localStorage");
            } catch (error) {
                console.error("Ошибка сохранения пользователя:", error);
            }
        }
    };

    // Очистка данных пользователя
    clearUserFromStorage() {
        localStorage.removeItem('currentUser');
        localStorage.removeItem('token');
        console.log("Данные пользователя очищены");
    };

    // Установка пользователя
    setUser = (user) => {
        this.user = user;
        this.saveUserToStorage();
    };

    // Установка статуса авторизации
    setIsAuth = (bool) => {
        this.isAuth = bool;
        if (!bool) {
            this.logout();
        }
    };

    // Выход из системы
    logout = () => {
        this.user = null;
        this.isAuth = false;
        this.clearUserFromStorage();
        this.clearMessages();
        this.disconnect();
    };

    // Загрузка сообщений из localStorage для текущего пользователя
    loadMessages(){
        try {
            const userId = this.getCurrentUserId();

            if (!userId) {
                console.log("Пользователь не авторизован, сообщения не загружены");
                this.messages = [];
                return;
            }

            const savedMessages = localStorage.getItem(`chatMessages_${userId}`);
            if (savedMessages) {
                const parsedMessages = JSON.parse(savedMessages);
                this.messages = parsedMessages.map(msg => ({
                    ...msg,
                    timestamp: new Date(msg.timestamp)
                }));
                console.log(`Сообщения загружены для пользователя ${userId}:`, this.messages.length);
            } else {
                this.messages = [];
                console.log("Нет сохраненных сообщений для пользователя");
            }
        } catch (error) {
            console.error("Ошибка при загрузке сообщений:", error);
            const userId = this.getCurrentUserId();
            if (userId) {
                localStorage.removeItem(`chatMessages_${userId}`);
            }
            this.messages = [];
        }
    };

    // Сохранение сообщений в localStorage для текущего пользователя
    saveMessages() {
        const userId = this.getCurrentUserId();
        if (userId && this.messages.length > 0) {
            try {
                localStorage.setItem(`chatMessages_${userId}`, JSON.stringify(this.messages));
                console.log(`Сообщения сохранены для пользователя ${userId}`);
            } catch (error) {
                console.error("Ошибка при сохранении сообщений:", error);
            }
        }
    };

    // Очистка истории сообщений для текущего пользователя
    clearMessages() {
        const userId = this.getCurrentUserId();
        if (userId) {
            localStorage.removeItem(`chatMessages_${userId}`);
        }
        this.messages = [];
        console.log("Сообщения очищены");
    };

    // Получение сообщений другого пользователя (для админских целей)
    getUserMessages(userId) {
        try {
            const savedMessages = localStorage.getItem(`chatMessages_${userId}`);
            if (savedMessages) {
                const parsedMessages = JSON.parse(savedMessages);
                return parsedMessages.map(msg => ({
                    ...msg,
                    timestamp: new Date(msg.timestamp)
                }));
            }
            return [];
        } catch (error) {
            console.error(`Ошибка при загрузке сообщений пользователя ${userId}:`, error);
            return [];
        }
    };

    // Миграция сообщений со старого формата на новый (при смене системы хранения)
    migrateMessagesToUser(userId) {
        try {
            // Проверяем есть ли сообщения в старом формате
            const oldMessages = localStorage.getItem('chatMessages');
            if (oldMessages && userId) {
                const parsedMessages = JSON.parse(oldMessages);

                // Сохраняем под новым ключом
                localStorage.setItem(`chatMessages_${userId}`, oldMessages);

                // Удаляем старый формат
                localStorage.removeItem('chatMessages');

                console.log(`Сообщения мигрированы для пользователя ${userId}`);
                this.loadMessages(); // Перезагружаем сообщения
            }
        } catch (error) {
            console.error("Ошибка миграции сообщений:", error);
        }
    };

    // Проверка наличия сообщений у пользователя
    hasUserMessages(userId = null) {
        const targetUserId = userId || this.getCurrentUserId();
        if (!targetUserId) return false;

        const savedMessages = localStorage.getItem(`chatMessages_${targetUserId}`);
        return !!savedMessages;
    };

    // Получение статистики по сообщениям
    getMessagesStats = () => {
        const userId = this.getCurrentUserId();
        if (!userId) return null;

        return {
            userId: userId,
            totalMessages: this.messages.length,
            userMessages: this.messages.filter(msg => msg.user === "Вы").length,
            botMessages: this.messages.filter(msg => msg.user !== "Вы").length,
            lastMessage: this.messages.length > 0 ? this.messages[this.messages.length - 1].timestamp : null
        };
    };

    connect() {
        if (this.isConnecting || this.isConnected) return;

        this.isConnecting = true;
        this.error = null;

        try {
            const wsUrl = process.env.REACT_APP_API_WSS;
            if (this.socket) {
                this.socket.close(1000, "Reconnecting");
                this.socket = null;
            }
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

    handleIncomingMessage(data) {
        if (data.type === 'chat_message') {
            const botMessage = {
                id: Date.now().toString(),
                content: data.message,
                user: data.user || "Misa",
                timestamp: new Date(),
                userId: this.getCurrentUserId() // Добавляем привязку к пользователю
            };

            this.messages.push(botMessage);
            this.isLoading = false;
            this.saveMessages();
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

    // Отправка сообщения с привязкой к пользователю
    async sendMessage (content) {
        if (!this.isConnected || !this.socket) {
            this.error = "Нет соединения с сервером";
            return false;
        }

        if (!content.trim()) {
            return false;
        }

        this.isLoading = true;
        this.error = null;
        console.log(this.user);
        const userMessage = {
            id: Date.now().toString(),
            content: content,
            user: this.user,
            timestamp: new Date(),
            userId: this.getCurrentUserId() // Привязываем к пользователю
        };

        this.messages.push(userMessage);
        this.saveMessages();

        try {
            this.socket.send(this.user + '|message|' +content);
            return true;
        } catch (error) {
            this.error = "Ошибка при отправке сообщения";
            this.isLoading = false;
            console.error("Ошибка отправки сообщения:", error);
            return false;
        }
    };

    disconnect() {
        if (this.socket) {
            this.socket.close(1000, "Пользователь закрыл соединение");
            this.socket = null;
        }
        this.isConnected = false;
        this.isConnecting = false;
    };

    clearError() {
        this.error = null;
    };

    cleanup() {
        this.disconnect();
    };
}

export default ChatStore;