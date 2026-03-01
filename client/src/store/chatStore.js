import { makeAutoObservable } from "mobx";

const generateId = () => Date.now().toString(36) + Math.random().toString(36).slice(2);

class ChatStore {
    chats = []; // [{ id, title, messages, createdAt }]
    currentChatId = null;
    isConnected = false;
    isConnecting = false;
    isLoading = false;
    error = null;
    socket = null;
    reconnectAttempts = 0;
    maxReconnectAttempts = 8;
    reconnectDelay = 1000;
    user = null;
    isAuth = false;

    constructor(rootStore) {
        this.rootStore = rootStore;
        makeAutoObservable(this);
        this.loadUserFromStorage();
        this.loadChats();
    }

    get messages() {
        const chat = this.chats.find(c => c.id === this.currentChatId);
        return chat ? chat.messages : [];
    }

    get currentChat() {
        return this.chats.find(c => c.id === this.currentChatId);
    }

    // Получение ID текущего пользователя
    getCurrentUserId() {
        // Пробуем получить из rootStore.user, если есть
        if (this.rootStore?.user?.getCurrentUserId) {
            return this.rootStore.user.getCurrentUserId();
        }
        // Или из локального состояния
        const id = localStorage.getItem('currentUserId');
        return this.user?.user_id || id
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
    saveUserToStorage(id) {
        if (this.user && this.isAuth) {
            try {
                localStorage.setItem('currentUser', this.user);
                localStorage.setItem('currentUserId', id);
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
        localStorage.removeItem('currentUserId');
        console.log("Данные пользователя очищены");
    };

    // Установка пользователя
    setUser(user, id) {
        this.user = user;
        this.isAuth = true;
        this.saveUserToStorage(id);
        this.loadChats();
    };

    // Установка статуса авторизации
    setIsAuth(bool) {
        this.isAuth = bool;
        if (!bool) {
            this.logout();
        }
    };

    // Выход из системы
    logout()  {
        this.clearUserFromStorage();
        this.disconnect();
        this.user = null;
        this.isAuth = false;
    };

    // Загрузка чатов из localStorage
    loadChats() {
        try {
            const userId = this.getCurrentUserId();
            if (!userId) {
                this.chats = [];
                this.currentChatId = null;
                return;
            }
            let saved = localStorage.getItem(`chats_${userId}`);
            if (!saved) {
                const oldMessages = localStorage.getItem(`chatMessages_${userId}`);
                if (oldMessages) {
                    try {
                        const msgs = JSON.parse(oldMessages).map(m => ({
                            ...m,
                            timestamp: new Date(m.timestamp)
                        }));
                        const migratedChat = {
                            id: generateId(),
                            title: "Новый чат",
                            messages: msgs,
                            createdAt: new Date()
                        };
                        this.chats = [migratedChat];
                        this.currentChatId = migratedChat.id;
                        this.saveChats();
                        localStorage.removeItem(`chatMessages_${userId}`);
                        return;
                    } catch (e) {
                        console.warn("Миграция старых сообщений не удалась", e);
                    }
                }
            }
            if (saved) {
                const parsed = JSON.parse(saved);
                this.chats = parsed.map(chat => ({
                    ...chat,
                    messages: (chat.messages || []).map(m => ({
                        ...m,
                        timestamp: new Date(m.timestamp)
                    })),
                    createdAt: new Date(chat.createdAt)
                }));
                if (this.chats.length > 0 && !this.currentChatId) {
                    this.currentChatId = this.chats[0].id;
                } else if (this.currentChatId && !this.chats.find(c => c.id === this.currentChatId)) {
                    this.currentChatId = this.chats[0]?.id || null;
                }
            } else {
                const defaultChat = {
                    id: generateId(),
                    title: "Новый чат",
                    messages: [],
                    createdAt: new Date()
                };
                this.chats = [defaultChat];
                this.currentChatId = defaultChat.id;
                this.saveChats();
            }
        } catch (error) {
            console.error("Ошибка загрузки чатов:", error);
            this.chats = [];
            this.currentChatId = null;
        }
    };

    // Сохранение чатов в localStorage
    saveChats() {
        const userId = this.getCurrentUserId();
        if (userId && this.chats.length > 0) {
            try {
                localStorage.setItem(`chats_${userId}`, JSON.stringify(this.chats));
            } catch (error) {
                console.error("Ошибка сохранения чатов:", error);
            }
        }
    };

    // Генерация заголовка чата по первому сообщению
    getChatTitle(chat) {
        const firstUserMsg = chat.messages?.find(m => m.user !== "Misa");
        if (firstUserMsg) {
            const text = (firstUserMsg.content || "").replace(/\n/g, " ").trim();
            return text.length > 40 ? text.slice(0, 40) + "…" : text || "Новый чат";
        }
        return "Новый чат";
    }

    // Переключение на чат
    switchChat(chatId) {
        if (this.chats.some(c => c.id === chatId)) {
            this.currentChatId = chatId;
        }
    };

    // Новый чат
    newChat() {
        const id = generateId();
        const newChat = {
            id,
            title: "Новый чат",
            messages: [],
            createdAt: new Date()
        };
        this.chats.unshift(newChat);
        this.currentChatId = id;
        this.saveChats();
        if (this.socket && this.isConnected && this.user) {
            this.socket.send(this.user + '|message|__NEW_CHAT__');
        }
    };

    // Очистка истории текущего чата
    clearMessages() {
        const chat = this.currentChat;
        if (chat) {
            chat.messages = [];
            this.saveChats();
        }
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
                    if(event.code != 1000) {
                        setTimeout(() => {
                            if(this.isAuth) {
                                this.reconnectAttempts++;
                                this.reconnectDelay = Math.min(this.reconnectDelay * 1.5, 30000);
                                console.log(`Попытка переподключения #${this.reconnectAttempts} через ${this.reconnectDelay}ms`);
                                this.connect();
                            }
                        }, this.reconnectDelay);
                    }
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
                userId: this.getCurrentUserId()
            };
            const chat = this.currentChat;
            if (chat) {
                chat.messages.push(botMessage);
                this.isLoading = false;
                this.saveChats();
            }
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

    async sendMessage(content) {
        if (!this.isConnected || !this.socket) {
            this.error = "Нет соединения с сервером";
            return false;
        }
        if (!content.trim()) return false;

        const chatId = this.currentChatId;
        if (!chatId) {
            this.newChat();
            return this.sendMessage(content);
        }

        const chat = this.currentChat;
        if (!chat) return false;

        this.isLoading = true;
        this.error = null;
        const userMessage = {
            id: Date.now().toString(),
            content: content,
            user: this.user,
            timestamp: new Date(),
            userId: this.getCurrentUserId()
        };
        chat.messages.push(userMessage);
        this.saveChats();

        try {
            this.socket.send(this.user + '|message|' + content);
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