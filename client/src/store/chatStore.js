import { makeAutoObservable } from "mobx";

const generateId = () => Date.now().toString(36) + Math.random().toString(36).slice(2);
const API_URL = process.env.REACT_APP_API_URL || '';

const apiFetch = async (path, options = {}) => {
    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(`${API_URL}${path}`, { ...options, headers });
    const data = await res.json().catch(() => ({}));
    if (data.status === 'error') throw new Error(data.message || 'API error');
    return data.data;
};

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
        localStorage.removeItem('userProfile');
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

    _loadChatsInProgress = false;

    // Загрузка чатов из API (БД на бэкенде)
    async loadChats() {
        if (this._loadChatsInProgress) return;
        try {
            const userId = this.getCurrentUserId();
            if (!userId) {
                this.chats = [];
                this.currentChatId = null;
                return;
            }
            if (!API_URL) {
                this._loadChatsFromLocalStorage();
                return;
            }
            this._loadChatsInProgress = true;
            try {
                const chatsData = await apiFetch('/api/chats/');
                if (Array.isArray(chatsData) && chatsData.length > 0) {
                    const seen = new Set();
                    this.chats = chatsData
                        .filter(c => {
                            if (seen.has(c.id)) return false;
                            seen.add(c.id);
                            return true;
                        })
                        .map(c => ({
                            id: c.id,
                            title: c.title || 'Новый чат',
                            messages: [],
                            createdAt: c.createdAt ? new Date(c.createdAt) : new Date(),
                            _messagesLoaded: false
                        }));
                    this.currentChatId = this.chats[0].id;
                    this._loadChatMessagesIfNeeded(this.chats[0].id);
                } else {
                    this.chats = [];
                    await this.newChat();
                }
            } catch (e) {
                console.warn("Ошибка загрузки чатов с API, fallback на localStorage:", e);
                this._loadChatsFromLocalStorage();
            }
        } catch (error) {
            console.error("Ошибка загрузки чатов:", error);
            this.chats = [];
            this.currentChatId = null;
        } finally {
            this._loadChatsInProgress = false;
        }
    }

    async _loadChatMessagesIfNeeded(chatId) {
        const chat = this.chats.find(c => c.id === chatId);
        if (!chat || chat._messagesLoaded) return;
        if (this.socket && this.isConnected) {
            this._loadChatMessagesViaWebSocket(chatId);
        } else if (API_URL) {
            try {
                const msgs = await apiFetch(`/api/chats/${chatId}/messages/`);
                chat.messages = (msgs || []).map(m => ({
                    id: String(m.id),
                    content: m.content,
                    user: m.user,
                    timestamp: new Date(m.timestamp),
                    isImage: m.isImage
                }));
                chat._messagesLoaded = true;
            } catch (e) {
                console.warn("Ошибка загрузки сообщений:", e);
            }
        }
    }

    _loadChatMessagesViaWebSocket(chatId) {
        if (!this.socket || !this.isConnected) return;
        const chat = this.chats.find(c => c.id === chatId);
        if (!chat) return;
        this.socket.send(JSON.stringify({ type: 'load_history', chat_id: chatId }));
        chat._pendingHistory = true;
    }

    /** Подключиться к группе чата для получения broadcast (сообщения, typing) на всех устройствах */
    ensureJoinedToChat(chatId) {
        if (!this.socket || !this.isConnected || !chatId) return;
        this.socket.send(JSON.stringify({ type: 'join_chat', chat_id: chatId }));
    }

    _loadChatsFromLocalStorage() {
        const userId = this.getCurrentUserId();
        const saved = localStorage.getItem(`chats_${userId}`);
        if (saved) {
            const parsed = JSON.parse(saved);
            this.chats = parsed.map(chat => ({
                ...chat,
                messages: (chat.messages || []).map(m => ({
                    ...m,
                    timestamp: new Date(m.timestamp)
                })),
                createdAt: chat.createdAt ? new Date(chat.createdAt) : new Date()
            }));
            if (this.chats.length > 0 && !this.currentChatId) this.currentChatId = this.chats[0].id;
        } else {
            this.newChat();
        }
    }


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

    // Группировка чатов по периодам (Сегодня, Вчера, 7 дней, 30 дней)
    getChatsGroupedByPeriod() {
        const now = new Date();
        const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const yesterdayStart = new Date(todayStart);
        yesterdayStart.setDate(yesterdayStart.getDate() - 1);
        const sevenDaysAgo = new Date(todayStart);
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
        const thirtyDaysAgo = new Date(todayStart);
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

        const groups = { today: [], yesterday: [], last7Days: [], last30Days: [] };

        for (const chat of this.chats) {
            let date = chat.createdAt ? new Date(chat.createdAt) : new Date();
            if (isNaN(date.getTime())) date = new Date();
            if (date >= todayStart) {
                groups.today.push(chat);
            } else if (date >= yesterdayStart) {
                groups.yesterday.push(chat);
            } else if (date >= sevenDaysAgo) {
                groups.last7Days.push(chat);
            } else if (date >= thirtyDaysAgo) {
                groups.last30Days.push(chat);
            }
        }

        return groups;
    }

    // Переключение на чат (подгружает сообщения с сервера при необходимости)
    switchChat(chatId) {
        if (this.chats.some(c => c.id === chatId)) {
            this.currentChatId = chatId;
            if (this.socket && this.isConnected) {
                this.socket.send(JSON.stringify({ type: 'join_chat', chat_id: chatId }));
            }
            this._loadChatMessagesIfNeeded(chatId);
        }
    };

    // Новый чат (создаёт в БД через API)
    async newChat() {
        // Если есть пустой чат — переключаемся на него, не создаём новый (чтобы не флудить)
        const emptyChat = this.chats.find(c => !c.messages || c.messages.length === 0);
        if (emptyChat) {
            this.switchChat(emptyChat.id);
            return;
        }
        let id = generateId();
        if (API_URL) {
            try {
                const res = await apiFetch('/api/chats/', {
                    method: 'POST',
                    body: JSON.stringify({ id, title: 'Новый чат' })
                });
                if (res?.id) id = res.id;
            } catch (e) {
                console.warn("Ошибка создания чата на сервере:", e);
            }
        }
        const newChat = {
            id,
            title: "Новый чат",
            messages: [],
            createdAt: new Date(),
            _messagesLoaded: true
        };
        this.chats.unshift(newChat);
        this.currentChatId = id;
        this.saveChats();
        if (this.socket && this.isConnected && this.user) {
            this.socket.send(this.user + '|message|__NEW_CHAT__');
        }
    };

    // Очистка истории текущего чата (удаляет сообщения на бэкенде)
    async clearMessages() {
        const chat = this.currentChat;
        if (!chat) return;
        if (API_URL) {
            try {
                await apiFetch(`/api/chats/${chat.id}/messages/clear/`, { method: 'DELETE' });
            } catch (e) {
                console.warn("Ошибка очистки сообщений на сервере:", e);
            }
        }
        chat.messages = [];
        this.saveChats();
        // Синхронизация: broadcast на другие устройства
        if (this.socket && this.isConnected) {
            this.socket.send(JSON.stringify({ type: 'clear_messages', chat_id: chat.id }));
        }
    };

    // Удаление всех чатов (с сервера)
    async deleteAllChats() {
        if (API_URL) {
            try {
                for (const chat of [...this.chats]) {
                    await apiFetch(`/api/chats/${chat.id}/delete/`, { method: 'DELETE' });
                }
            } catch (e) {
                console.warn("Ошибка удаления чатов:", e);
            }
        }
        await this.newChat();
    };

    // Данные для conversations.json (экспорт)
    getConversationsExportData() {
        return {
            exportedAt: new Date().toISOString(),
            conversations: this.chats.map(c => ({
                id: c.id,
                title: c.title,
                createdAt: c.createdAt,
                messages: (c.messages || []).map(m => ({
                    content: m.content,
                    user: m.user,
                    timestamp: m.timestamp
                }))
            }))
        };
    }

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
                    if (event.code !== 1000) {
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
            const msg = {
                id: Date.now().toString() + Math.random().toString(36).slice(2),
                content: data.message,
                user: data.user || "Misa",
                timestamp: new Date(),
                isImage: data.isImage || /^(\/images\/|https?:\/\/).+(\.(jpg|jpeg|png|gif|bmp|webp|svg))($|\?)/i.test(data.message)
            };
            const chatId = data.chat_id || this.currentChatId;
            const chat = this.chats.find(c => c.id === chatId);
            if (chat) {
                chat.messages.push(msg);
                // Сообщение от пользователя → Миса печатает; от Misa → печатание закончено (только для текущего чата)
                if (chatId === this.currentChatId) {
                    this.isLoading = (data.user && data.user !== "Misa");
                }
                this.saveChats();
            }
        }
        else if (data.type === 'history') {
            const chat = this.chats.find(c => c.id === data.chat_id);
            if (chat) {
                chat.messages = (data.messages || []).map(m => ({
                    id: String(m.id),
                    content: m.content,
                    user: m.user,
                    timestamp: new Date(m.timestamp),
                    isImage: m.isImage
                }));
                chat._messagesLoaded = true;
                chat._pendingHistory = false;
                this.saveChats();
            }
        }
        else if (data.type === 'error') {
            this.error = data.detail
                ? `${data.message || "Произошла ошибка"}: ${data.detail}`
                : (data.message || "Произошла ошибка");
            this.isLoading = false;
        }
        else if (data.type === 'connection_established') {
            console.log("Соединение подтверждено сервером");
            if (this.currentChatId) {
                this._loadChatMessagesViaWebSocket(this.currentChatId);
            }
        }
        else if (data.type === 'messages_cleared') {
            const chatId = data.chat_id;
            const chat = this.chats.find(c => c.id === chatId);
            if (chat) {
                chat.messages = [];
                this.saveChats();
            }
        }
        else if (data.type === 'typing') {
            if (data.chat_id === this.currentChatId) {
                this.isLoading = !!data.isTyping;
            }
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
        const isFirstUserMsg = chat.messages.filter(m => m.user !== 'Misa').length === 1;
        if (isFirstUserMsg && API_URL) {
            const title = content.replace(/\n/g, ' ').trim().slice(0, 40) + (content.length > 40 ? '…' : '');
            apiFetch(`/api/chats/${chatId}/`, {
                method: 'PATCH',
                body: JSON.stringify({ title: title || 'Новый чат' })
            }).then(() => { chat.title = title || 'Новый чат'; }).catch(() => {});
        }
        this.saveChats();

        try {
            const payload = this.currentChatId
                ? `${this.user}|${this.currentChatId}|message|${content}`
                : `${this.user}|message|${content}`;
            this.socket.send(payload);
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