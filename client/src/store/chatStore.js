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
    pinnedChatIds = []; // id закреплённых чатов (только клиент, localStorage)
    currentChatId = null;
    shareModeForChatId = null; // chatId — режим выделения для шаринга
    selectedMessageIds = []; // id выделенных сообщений
    isConnected = false;
    isConnecting = false;
    loadingChatIds = []; // массив chat_id, в которых Миса печатает (параллельная обработка)
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
        if (typeof document !== 'undefined') {
            this._setupVisibilityReconnect();
        }
    }

    _setupVisibilityReconnect() {
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState !== 'visible') return;
            if (!this.isAuth) return;
            const socketDead = this.socket && (this.socket.readyState === WebSocket.CLOSING || this.socket.readyState === WebSocket.CLOSED);
            const needReconnect = !this.isConnected && !this.isConnecting;
            if (socketDead) {
                this.socket = null;
                this.isConnected = false;
                this.isConnecting = false;
            }
            if (needReconnect || socketDead) {
                this.reconnectAttempts = 0;
                this.reconnectDelay = 1000;
                setTimeout(() => this.connect(), 300);
            }
        });
    }

    get messages() {
        const chat = this.chats.find(c => c.id === this.currentChatId);
        return chat ? chat.messages : [];
    }

    get currentChat() {
        return this.chats.find(c => c.id === this.currentChatId);
    }

    get isLoading() {
        return this.loadingChatIds.length > 0;
    }

    isChatLoading(chatId) {
        return this.loadingChatIds.includes(chatId);
    }

    // Режим шаринга — выделение сообщений
    startShareMode(chatId) {
        this.shareModeForChatId = chatId;
        this.selectedMessageIds = [];
    }

    startShareModeWithMessage(chatId, msgId) {
        this.shareModeForChatId = chatId;
        const chat = this.chats.find(c => c.id === chatId);
        const idx = chat?.messages?.findIndex(m => m.id === msgId);
        const ids = [msgId];
        if (idx != null && idx > 0) {
            const prev = chat.messages[idx - 1];
            if (prev?.user !== 'Misa') ids.unshift(prev.id);
        }
        this.selectedMessageIds = ids;
    }

    endShareMode() {
        this.shareModeForChatId = null;
        this.selectedMessageIds = [];
    }

    toggleMessageSelection(msgId) {
        const idx = this.selectedMessageIds.indexOf(msgId);
        if (idx >= 0) {
            this.selectedMessageIds = this.selectedMessageIds.filter(id => id !== msgId);
        } else {
            this.selectedMessageIds = [...this.selectedMessageIds, msgId];
        }
    }

    selectAllMessages() {
        const chat = this.currentChat;
        if (!chat?.messages) return;
        this.selectedMessageIds = chat.messages.map(m => m.id);
    }

    isMessageSelected(msgId) {
        return this.selectedMessageIds.includes(msgId);
    }

    async setMessageFeedback(msgId, feedback, categories = null, comment = null) {
        const chat = this.currentChat;
        const idx = chat?.messages?.findIndex(m => m.id === msgId);
        if (idx == null || idx < 0) return;
        const msg = chat.messages[idx];
        const prev = msg?.feedback ?? null;
        const prevCats = msg?.feedbackCategories ?? null;
        const prevComm = msg?.feedbackComment ?? null;
        const nextFeedback = feedback === 'dislike' ? (categories || []) : null;
        const nextComment = feedback === 'dislike' ? (comment || null) : null;
        chat.messages[idx] = {
            ...msg,
            feedback,
            feedbackCategories: nextFeedback,
            feedbackComment: nextComment,
        };
        this.saveChats();
        if (API_URL) {
            try {
                await apiFetch(`/api/chats/${this.currentChatId}/messages/${msgId}/feedback/`, {
                    method: 'PATCH',
                    body: JSON.stringify({ feedback, categories: categories || [], comment: comment || '' })
                });
            } catch (e) {
                chat.messages[idx] = { ...msg, feedback: prev, feedbackCategories: prevCats, feedbackComment: prevComm };
                this.saveChats();
                console.warn('Ошибка сохранения feedback:', e);
            }
        }
    }

    getMessageFeedback(msgId) {
        const msg = this.currentChat?.messages?.find(m => m.id === msgId);
        return msg?.feedback ?? null;
    }

    getShareLink() {
        const base = typeof window !== 'undefined' ? window.location.origin : '';
        const chatId = this.shareModeForChatId || this.currentChatId;
        if (!chatId) return base;
        return `${base}/share/${encodeURIComponent(chatId)}`;
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
        this._loadPinnedChatIds();
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
                    const chatIds = new Set(chatsData.map(c => c.id));
                    this.pinnedChatIds = this.pinnedChatIds.filter(id => chatIds.has(id));
                    this._savePinnedChatIds();
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
                    isImage: m.isImage,
                    feedback: m.feedback && (m.feedback === 'like' || m.feedback === 'dislike') ? m.feedback : null,
                    feedbackCategories: m.feedbackCategories || null,
                    feedbackComment: m.feedbackComment || null
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
        this._loadPinnedChatIds();
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

    // Заголовок чата (только от GPT — чаты без заголовка не показываются на панели)
    getChatTitle(chat) {
        return (chat.title && chat.title.trim()) ? chat.title.trim() : '';
    }

    // Группировка чатов по периодам (Закреплённые, Сегодня, Вчера, 7 дней, 30 дней)
    getChatsGroupedByPeriod() {
        const now = new Date();
        const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const yesterdayStart = new Date(todayStart);
        yesterdayStart.setDate(yesterdayStart.getDate() - 1);
        const sevenDaysAgo = new Date(todayStart);
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
        const thirtyDaysAgo = new Date(todayStart);
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

        const groups = { pinned: [], today: [], yesterday: [], last7Days: [], olderByMonth: {} };
        const pinnedSet = new Set(this.pinnedChatIds);

        for (const chat of this.chats) {
            if (!chat.messages || chat.messages.length === 0) continue;
            if (!chat.title || chat.title.trim() === '' || chat.title.trim() === 'Новый чат') continue;
            if (pinnedSet.has(chat.id)) {
                groups.pinned.push(chat);
                continue;
            }
            let date = chat.createdAt ? new Date(chat.createdAt) : new Date();
            if (isNaN(date.getTime())) date = new Date();
            if (date >= todayStart) {
                groups.today.push(chat);
            } else if (date >= yesterdayStart) {
                groups.yesterday.push(chat);
            } else if (date >= sevenDaysAgo) {
                groups.last7Days.push(chat);
            } else if (date < thirtyDaysAgo) {
                const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
                if (!groups.olderByMonth[key]) groups.olderByMonth[key] = { year: date.getFullYear(), month: date.getMonth(), chats: [] };
                groups.olderByMonth[key].chats.push(chat);
            }
        }

        // Сортировка чатов внутри каждой месячной группы (новые сверху)
        for (const key of Object.keys(groups.olderByMonth)) {
            groups.olderByMonth[key].chats.sort((a, b) => {
                const da = a.createdAt ? new Date(a.createdAt).getTime() : 0;
                const db = b.createdAt ? new Date(b.createdAt).getTime() : 0;
                return db - da;
            });
        }

        // Порядок закреплённых — по порядку закрепления (первый закреплённый сверху)
        groups.pinned.sort((a, b) => {
            const ia = this.pinnedChatIds.indexOf(a.id);
            const ib = this.pinnedChatIds.indexOf(b.id);
            return (ia >= 0 ? ia : 999) - (ib >= 0 ? ib : 999);
        });

        // Преобразуем olderByMonth в массив, отсортированный по дате (новые месяцы сверху)
        groups.olderByMonth = Object.entries(groups.olderByMonth)
            .sort(([a], [b]) => b.localeCompare(a))
            .map(([key, val]) => ({ key, year: val.year, month: val.month, chats: val.chats }));

        return groups;
    }

    // Закрепить/открепить чат
    togglePinChat(chatId) {
        const idx = this.pinnedChatIds.indexOf(chatId);
        if (idx >= 0) {
            this.pinnedChatIds = this.pinnedChatIds.filter(id => id !== chatId);
        } else {
            this.pinnedChatIds = [...this.pinnedChatIds, chatId];
        }
        this._savePinnedChatIds();
    }

    isChatPinned(chatId) {
        return this.pinnedChatIds.includes(chatId);
    }

    _savePinnedChatIds() {
        const userId = this.getCurrentUserId();
        if (userId) {
            try {
                localStorage.setItem(`pinned_chats_${userId}`, JSON.stringify(this.pinnedChatIds));
            } catch (e) {
                console.error("Ошибка сохранения закреплённых чатов:", e);
            }
        }
    }

    _loadPinnedChatIds() {
        const userId = this.getCurrentUserId();
        if (!userId) return;
        try {
            const saved = localStorage.getItem(`pinned_chats_${userId}`);
            if (saved) {
                const parsed = JSON.parse(saved);
                this.pinnedChatIds = Array.isArray(parsed) ? parsed : [];
            }
        } catch (e) {
            this.pinnedChatIds = [];
        }
    }

    // Переключение на чат (подгружает сообщения с сервера при необходимости)
    switchChat(chatId) {
        if (this.chats.some(c => c.id === chatId)) {
            this.currentChatId = chatId;
            if (this.shareModeForChatId && this.shareModeForChatId !== chatId) {
                this.endShareMode();
            }
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

    // Удаление одного чата
    async deleteChat(chatId) {
        if (API_URL) {
            try {
                await apiFetch(`/api/chats/${chatId}/delete/`, { method: 'DELETE' });
            } catch (e) {
                console.warn("Ошибка удаления чата:", e);
                return false;
            }
        }
        this.pinnedChatIds = this.pinnedChatIds.filter(id => id !== chatId);
        this._savePinnedChatIds();
        this.chats = this.chats.filter(c => c.id !== chatId);
        if (this.currentChatId === chatId) {
            this.currentChatId = this.chats[0]?.id ?? null;
            if (this.chats.length === 0) this.newChat();
        }
        this.saveChats();
        return true;
    }

    // Переименование чата
    async renameChat(chatId, newTitle) {
        const chat = this.chats.find(c => c.id === chatId);
        if (!chat) return false;
        const title = (newTitle || '').trim().slice(0, 500) || 'Новый чат';
        if (API_URL) {
            try {
                await apiFetch(`/api/chats/${chatId}/`, {
                    method: 'PATCH',
                    body: JSON.stringify({ title })
                });
            } catch (e) {
                console.warn("Ошибка переименования чата:", e);
                return false;
            }
        }
        chat.title = title;
        this.saveChats();
        return true;
    }

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
                id: data.message_id || Date.now().toString() + Math.random().toString(36).slice(2),
                content: data.message,
                user: data.user || "Misa",
                timestamp: new Date(),
                isImage: data.isImage || /^(\/images\/|https?:\/\/).+(\.(jpg|jpeg|png|gif|bmp|webp|svg))($|\?)/i.test(data.message),
                feedback: null
            };
            const chatId = data.chat_id || this.currentChatId;
            const chat = this.chats.find(c => c.id === chatId);
            if (chat) {
                chat.messages.push(msg);
                if (data.user === "Misa") {
                    this.loadingChatIds = this.loadingChatIds.filter(id => id !== chatId);
                } else {
                    if (!this.loadingChatIds.includes(chatId)) this.loadingChatIds.push(chatId);
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
                    isImage: m.isImage,
                    feedback: m.feedback && (m.feedback === 'like' || m.feedback === 'dislike') ? m.feedback : null,
                    feedbackCategories: m.feedbackCategories || null,
                    feedbackComment: m.feedbackComment || null
                }));
                if (data.title != null && data.title !== '') {
                    chat.title = String(data.title).trim();
                }
                chat._messagesLoaded = true;
                chat._pendingHistory = false;
                this.saveChats();
            }
        }
        else if (data.type === 'error') {
            this.error = data.detail
                ? `${data.message || "Произошла ошибка"}: ${data.detail}`
                : (data.message || "Произошла ошибка");
            if (data.chat_id) {
                this.loadingChatIds = this.loadingChatIds.filter(id => id !== data.chat_id);
            } else {
                this.loadingChatIds = [];
            }
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
            if (data.isTyping) {
                if (!this.loadingChatIds.includes(data.chat_id)) this.loadingChatIds.push(data.chat_id);
            } else {
                this.loadingChatIds = this.loadingChatIds.filter(id => id !== data.chat_id);
            }
        }
        else if (data.type === 'chat_title') {
            const chat = this.chats.find(c => c.id === data.chat_id);
            if (chat && data.title) {
                chat.title = data.title.trim().slice(0, 500);
                this.saveChats();
            }
        }
        else if (data.type === 'message_updated') {
            const chat = this.chats.find(c => c.id === data.chat_id);
            const msg = chat?.messages?.find(m => m.id === data.message_id);
            if (msg) {
                msg.content = data.message || msg.content;
                msg.isImage = data.isImage ?? msg.isImage;
                this.loadingChatIds = this.loadingChatIds.filter(id => id !== data.chat_id);
                this.saveChats();
            }
        }
        else {
            console.log("Неизвестный тип сообщения:", data);
        }
    };

    regenerateReply(msgId) {
        if (!this.isConnected || !this.socket || !this.currentChatId) return false;
        const chat = this.currentChat;
        const msg = chat?.messages?.find(m => m.id === msgId);
        if (!msg || msg.user !== 'Misa') return false;
        if (!this.loadingChatIds.includes(this.currentChatId)) {
            this.loadingChatIds = [...this.loadingChatIds, this.currentChatId];
        }
        try {
            this.socket.send(JSON.stringify({
                type: 'regenerate',
                chat_id: this.currentChatId,
                message_id: msgId,
                user: this.user,
            }));
            return true;
        } catch (e) {
            this.loadingChatIds = this.loadingChatIds.filter(id => id !== this.currentChatId);
            return false;
        }
    }

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

        const isFirstUserMsg = chat.messages.filter(m => m.user !== 'Misa').length === 0;
        if (isFirstUserMsg && API_URL) {
            try {
                await apiFetch('/api/chats/', {
                    method: 'POST',
                    body: JSON.stringify({ id: chatId, title: 'Новый чат' })
                });
            } catch (e) {
                console.warn("Ошибка создания чата на сервере:", e);
            }
        }

        if (!this.loadingChatIds.includes(chatId)) this.loadingChatIds.push(chatId);
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
            const payload = this.currentChatId
                ? `${this.user}|${this.currentChatId}|message|${content}`
                : `${this.user}|message|${content}`;
            this.socket.send(payload);
            return true;
        } catch (error) {
            this.error = "Ошибка при отправке сообщения";
            this.loadingChatIds = this.loadingChatIds.filter(id => id !== chatId);
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