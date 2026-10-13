import { makeAutoObservable } from "mobx";
import { jwtDecode } from "jwt-decode";
import { getLanguage } from "../utils/locale";
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
    _pendingChatCreates = {};
    _ensuredServerChats = new Set();

    constructor(rootStore) {
        this.rootStore = rootStore;
        makeAutoObservable(this);
        this.loadUserFromStorage();
        // Только быстрый preview из localStorage; список с сервера — после checkAuth (setUser / MainLayout)
        this._hydrateChatsFromCacheIfEmpty();
        if (typeof document !== 'undefined') {
            this._setupVisibilityReconnect();
        }
    }

    _clearPingInterval() {
        if (this._pingIntervalId) {
            clearInterval(this._pingIntervalId);
            this._pingIntervalId = null;
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
            if (API_URL) setTimeout(() => this.loadChats(), 500);
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

    _setChatTyping(chatId, isTyping) {
        if (!chatId) return;
        if (isTyping) {
            if (!this.loadingChatIds.includes(chatId)) {
                this.loadingChatIds = [...this.loadingChatIds, chatId];
            }
        } else {
            this.loadingChatIds = this.loadingChatIds.filter((id) => id !== chatId);
        }
    }

    /** Восстановить плашку «Миса печатает» после reload/history */
    _restoreTypingAfterHistory(chatId, serverIsTyping) {
        if (!chatId) return;
        if (serverIsTyping === true) {
            this._setChatTyping(chatId, true);
            return;
        }
        const chat = this.chats.find((c) => c.id === chatId);
        const msgs = chat?.messages || [];
        if (msgs.length === 0) {
            this._setChatTyping(chatId, false);
            return;
        }
        const last = msgs[msgs.length - 1];
        const lastIsUser = last && last.user !== 'Misa';
        const lastTs = this._getMessageTimestamp(last);
        // Fallback: последнее от пользователя и свежее — вероятно генерация ещё идёт (или только что упала)
        const recent = lastTs > 0 && (Date.now() - lastTs) < 10 * 60 * 1000;
        this._setChatTyping(chatId, !!(lastIsUser && recent));
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
        // Ссылка на домене API: Django отдаёт og:* ботам; браузер редиректит на веб (SPA)
        const api = (process.env.REACT_APP_API_URL || '').trim().replace(/\/$/, '');
        const base =
            api ||
            (typeof window !== 'undefined' ? window.location.origin : '');
        const chatId = this.shareModeForChatId || this.currentChatId;
        if (!chatId) return base;
        const url = new URL(`${base}/share/${encodeURIComponent(chatId)}`);
        if (this.selectedMessageIds?.length > 0) {
            url.searchParams.set("msg", this.selectedMessageIds.join(","));
        }
        url.searchParams.set("lang", getLanguage());
        return url.toString();
    }

    // Получение ID текущего пользователя
    getCurrentUserId() {
        const id = localStorage.getItem('currentUserId');
        if (id) return id;
        if (this.user?.user_id) return this.user.user_id;
        // Fallback: извлекаем user_id из JWT
        try {
            const token = localStorage.getItem('token');
            if (token) {
                const decoded = jwtDecode(token);
                const uid = decoded?.user_id ?? decoded?.id;
                if (uid != null) {
                    const s = String(uid);
                    if (!localStorage.getItem('currentUserId')) localStorage.setItem('currentUserId', s);
                    return s;
                }
            }
        } catch {}
        return null;
    };

    // Загрузка пользователя из localStorage
    loadUserFromStorage() {
        try {
            const savedUser = localStorage.getItem('currentUser');
            const token = localStorage.getItem('token');
            if (savedUser) {
                const userData = savedUser;
                this.user = userData;
                this.isAuth = true;
                console.log("Пользователь загружен из localStorage", this.user);
            } else if (token) {
                // Есть сессия по JWT — дождёмся checkAuth, но loadChats может идти по token
                this.isAuth = false;
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

    /** Сброс чатов в памяти при смене аккаунта / выходе (кэш на диске остаётся по ключу userId) */
    _resetChatState() {
        this.chats = [];
        this.currentChatId = null;
        this.pinnedChatIds = [];
        this.shareModeForChatId = null;
        this.selectedMessageIds = [];
        this.loadingChatIds = [];
        this.error = null;
        this._loadChatsInProgress = false;
    }

    // Выход из системы
    logout()  {
        this.clearUserFromStorage();
        this.disconnect();
        this.user = null;
        this.isAuth = false;
        this._resetChatState();
    };

    _loadChatsInProgress = false;

    /** Сразу показать чаты из localStorage (stale-while-revalidate), пока ждём API */
    _hydrateChatsFromCacheIfEmpty() {
        const userId = this.getCurrentUserId();
        if (!userId || this.chats.length > 0) return;
        this._loadPinnedChatIds();
        let saved;
        try {
            saved = localStorage.getItem(`chats_${userId}`);
            if (!saved) return;
            const parsed = JSON.parse(saved);
            if (!Array.isArray(parsed) || parsed.length === 0) return;
            this.chats = parsed.map(chat => ({
                ...chat,
                messages: (chat.messages || []).map(m => ({
                    ...m,
                    timestamp: new Date(m.timestamp)
                })),
                createdAt: chat.createdAt ? new Date(chat.createdAt) : new Date(),
                // Показываем кэш сразу, но не считаем историю финальной
                _messagesLoaded: false,
            }));
            if (this.chats.length > 0 && !this.currentChatId) this.currentChatId = this.chats[0].id;
        } catch (e) {
            console.warn('hydrate chats cache:', e);
        }
    }

    _hasAuthToken() {
        return !!localStorage.getItem('token');
    }

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
            if (!this._hasAuthToken()) {
                return;
            }
            this._hydrateChatsFromCacheIfEmpty();
            this._loadChatsInProgress = true;
            try {
                let chatsData;
                const prevById = new Map(this.chats.map(c => [c.id, c]));
                const prevCurrentId = this.currentChatId;
                for (let attempt = 0; attempt < 10; attempt++) {
                    if (!this.isAuth && !this._hasAuthToken()) return;
                    if (!this.isAuth && this._hasAuthToken()) {
                        await new Promise((r) => setTimeout(r, attempt === 0 ? 150 : 400));
                    }
                    try {
                        const res = await fetch(`${API_URL}/api/chats/`, {
                            headers: {
                                'Content-Type': 'application/json',
                                ...(localStorage.getItem('token') && { Authorization: `Bearer ${localStorage.getItem('token')}` }),
                            },
                        });
                        const data = await res.json().catch(() => ({}));
                        if (data.status === 'error') throw new Error(data.message || 'API error');
                        if (res.status === 401) {
                            this.clearUserFromStorage();
                            this.isAuth = false;
                            this._resetChatState();
                            return;
                        }
                        chatsData = data.data;
                        break;
                    } catch (err) {
                        console.warn("Ошибка загрузки чатов, повтор через 1 сек:", err?.message);
                        await new Promise(r => setTimeout(r, attempt === 0 ? 200 : 1000));
                    }
                }
                if (chatsData === undefined) {
                    console.warn("Не удалось загрузить чаты после нескольких попыток");
                    this._loadChatsFromLocalStorage();
                    return;
                }
                if (Array.isArray(chatsData) && chatsData.length > 0) {
                    const chatIds = new Set(chatsData.map(c => c.id));
                    this.pinnedChatIds = this.pinnedChatIds.filter(id => chatIds.has(id));
                    this._savePinnedChatIds();
                    // Берём актуальное in-memory состояние ПОСЛЕ await — иначе затрём
                    // оптимистично отправленные сообщения снимком с начала loadChats.
                    const latestById = new Map(this.chats.map((c) => [c.id, c]));
                    const seen = new Set();
                    this.chats = chatsData
                        .filter(c => {
                            if (seen.has(c.id)) return false;
                            seen.add(c.id);
                            return true;
                        })
                        .map(c => {
                            const latest = latestById.get(c.id) || prevById.get(c.id);
                            const hasCached =
                                latest &&
                                Array.isArray(latest.messages) &&
                                latest.messages.length > 0;
                            return {
                                id: c.id,
                                title: c.title || latest?.title || 'Новый чат',
                                messages: hasCached ? latest.messages : [],
                                createdAt: c.createdAt ? new Date(c.createdAt) : (latest?.createdAt || new Date()),
                                // Кэш только для мгновенного UI — историю всегда перепроверяем с сервера
                                _messagesLoaded: false,
                                _pendingHistory: false,
                            };
                        });
                    // Не теряем локально созданные чаты, которых ещё нет в ответе API
                    for (const [id, latest] of latestById.entries()) {
                        if (chatIds.has(id) || !latest) continue;
                        if (this._pendingChatCreates[id] || latest.messages?.length > 0 || id === prevCurrentId) {
                            this.chats.unshift({
                                ...latest,
                                messages: [...(latest.messages || [])],
                                _messagesLoaded: !!(latest.messages?.length),
                                _pendingHistory: false,
                            });
                        }
                    }
                    // Закреплённые сверху, остальные — по последней активности
                    this.chats = [...this.chats].sort((a, b) => {
                        const pa = this.pinnedChatIds.includes(a.id);
                        const pb = this.pinnedChatIds.includes(b.id);
                        if (pa && pb) {
                            return this.pinnedChatIds.indexOf(a.id) - this.pinnedChatIds.indexOf(b.id);
                        }
                        if (pa) return -1;
                        if (pb) return 1;
                        return this.getChatLastActivityTs(b) - this.getChatLastActivityTs(a);
                    });
                    if (prevCurrentId && this.chats.some(c => c.id === prevCurrentId)) {
                        this.currentChatId = prevCurrentId;
                    } else if (this.chats.length > 0) {
                        this.currentChatId = this.chats[0].id;
                    }
                    void this._refreshChatMessages(this.currentChatId);
                    this._loadAllChatMessagesInBackground();
                    this.saveChats();
                } else {
                    this.chats = [];
                    await this.newChat();
                }
            } catch (e) {
                console.warn("Ошибка загрузки чатов с API, fallback на localStorage:", e);
                if (this.chats.length === 0) {
                    this._loadChatsFromLocalStorage();
                }
            }
        } catch (error) {
            console.error("Ошибка загрузки чатов:", error);
            this.chats = [];
            this.currentChatId = null;
        } finally {
            this._loadChatsInProgress = false;
        }
    }

    _mapServerMessages(msgs) {
        return (msgs || []).map((m) => ({
            id: String(m.id),
            content: m.content,
            user: m.user,
            timestamp: new Date(m.timestamp),
            isImage: m.isImage,
            feedback: m.feedback && (m.feedback === 'like' || m.feedback === 'dislike') ? m.feedback : null,
            feedbackCategories: m.feedbackCategories || null,
            feedbackComment: m.feedbackComment || null
        }));
    }

    // Не затираем оптимистичные локальные сообщения пустым/устаревшим снимком с сервера
    _applyServerMessages(chat, msgs) {
        if (!chat) return;
        const incoming = this._mapServerMessages(msgs);
        const local = Array.isArray(chat.messages) ? chat.messages : [];
        const serverIds = new Set(incoming.map((m) => String(m.id)));
        const serverKeys = new Set(incoming.map((m) => `${m.user}|${m.content}`));
        // Всегда оставляем локальные optimistic/sending, которых ещё нет на сервере
        const localOnly = local.filter((m) =>
            !serverIds.has(String(m.id)) && !serverKeys.has(`${m.user}|${m.content}`)
        );
        chat.messages = [...incoming, ...localOnly];
        chat._messagesLoaded = true;
        chat._pendingHistory = false;
    }

    async _loadChatMessagesIfNeeded(chatId) {
        const chat = this.chats.find(c => c.id === chatId);
        if (!chat || chat._messagesLoaded) return;
        await this._refreshChatMessages(chatId);
    }

    /** Всегда подтянуть историю с сервера (кэш может быть устаревшим) */
    async _refreshChatMessages(chatId) {
        const chat = this.chats.find(c => c.id === chatId);
        if (!chat) return;
        if (this.socket && this.isConnected) {
            this._loadChatMessagesViaWebSocket(chatId);
            return;
        }
        if (!API_URL) return;
        try {
            const msgs = await apiFetch(`/api/chats/${chatId}/messages/`);
            this._applyServerMessages(chat, msgs);
            this.saveChats();
        } catch (e) {
            console.warn("Ошибка загрузки сообщений:", e);
        }
    }

    _loadChatMessagesViaWebSocket(chatId) {
        if (!this.socket || !this.isConnected) return;
        const chat = this.chats.find(c => c.id === chatId);
        if (!chat) return;
        this.socket.send(JSON.stringify({ type: 'load_history', chat_id: chatId }));
        chat._pendingHistory = true;
    }

    _loadAllChatMessagesInBackground() {
        if (!API_URL) return;
        const toLoad = this.chats.filter(c => !c._pendingHistory && !c._messagesLoaded);
        toLoad.forEach((chat) => {
            apiFetch(`/api/chats/${chat.id}/messages/`)
                .then((msgs) => {
                    const c = this.chats.find((x) => x.id === chat.id);
                    if (!c) return;
                    this._applyServerMessages(c, msgs);
                    this.saveChats();
                })
                .catch((e) => console.warn(`Ошибка загрузки сообщений чата ${chat.id}:`, e?.message));
        });
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
                createdAt: chat.createdAt ? new Date(chat.createdAt) : new Date(),
                _messagesLoaded: false,
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

    _getMessageTimestamp(m) {
        const t = m?.timestamp;
        if (!t) return 0;
        if (t instanceof Date && !isNaN(t.getTime())) return t.getTime();
        const d = new Date(t);
        return isNaN(d.getTime()) ? 0 : d.getTime();
    }

    getChatLastActivityTs(chat) {
        if (!chat) return 0;
        const msgs = chat.messages || [];
        const maxTs = msgs.reduce((acc, m) => Math.max(acc, this._getMessageTimestamp(m)), 0);
        if (maxTs) return maxTs;
        if (chat.createdAt) {
            const d = new Date(chat.createdAt);
            return isNaN(d.getTime()) ? 0 : d.getTime();
        }
        return 0;
    }

    _sortChatsByLastActivity(chats) {
        return [...chats].sort((a, b) => this.getChatLastActivityTs(b) - this.getChatLastActivityTs(a));
    }

    /** Поднять чат в списке (после закреплённых) после нового сообщения */
    _bumpChatInList(chatId) {
        if (this.pinnedChatIds.includes(chatId)) return;
        const idx = this.chats.findIndex((c) => c.id === chatId);
        if (idx < 0) return;
        const [chat] = this.chats.splice(idx, 1);
        let insertAt = 0;
        while (insertAt < this.chats.length && this.pinnedChatIds.includes(this.chats[insertAt].id)) {
            insertAt += 1;
        }
        this.chats.splice(insertAt, 0, chat);
    }

    // Группировка чатов по периодам (Закреплённые, Сегодня, Вчера, 7 дней, 30 дней)
    // Сравнение по календарным датам в локальной timezone — избегаем ошибок с UTC
    getChatsGroupedByPeriod() {
        const now = new Date();
        const toDateNum = (d) => d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
        const todayNum = toDateNum(now);
        const yesterdayNum = toDateNum(new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1));
        const sevenDaysAgoNum = toDateNum(new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7));

        const groups = { pinned: [], today: [], yesterday: [], last7Days: [], olderByMonth: {} };
        const pinnedSet = new Set(this.pinnedChatIds);

        for (const chat of this.chats) {
            const title = chat?.title?.trim() || '';
            const hasContent =
                (chat.messages?.length ?? 0) > 0 || (title && title !== 'Новый чат');
            if (!hasContent) continue;

            if (pinnedSet.has(chat.id)) {
                groups.pinned.push(chat);
                continue;
            }
            const maxTs = this.getChatLastActivityTs(chat);
            let date = maxTs ? new Date(maxTs) : (chat.createdAt ? new Date(chat.createdAt) : new Date());
            if (isNaN(date.getTime())) date = new Date();
            const dateNum = toDateNum(date);
            if (dateNum >= todayNum) {
                groups.today.push(chat);
            } else if (dateNum >= yesterdayNum) {
                groups.yesterday.push(chat);
            } else if (dateNum >= sevenDaysAgoNum) {
                groups.last7Days.push(chat);
            } else {
                const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
                if (!groups.olderByMonth[key]) groups.olderByMonth[key] = { year: date.getFullYear(), month: date.getMonth(), chats: [] };
                groups.olderByMonth[key].chats.push(chat);
            }
        }

        groups.today = this._sortChatsByLastActivity(groups.today);
        groups.yesterday = this._sortChatsByLastActivity(groups.yesterday);
        groups.last7Days = this._sortChatsByLastActivity(groups.last7Days);

        for (const key of Object.keys(groups.olderByMonth)) {
            groups.olderByMonth[key].chats = this._sortChatsByLastActivity(groups.olderByMonth[key].chats);
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

    // Переключение на чат — всегда обновляем историю с сервера (иначе кэш прячет новые сообщения)
    switchChat(chatId) {
        if (this.chats.some(c => c.id === chatId)) {
            this.currentChatId = chatId;
            if (this.shareModeForChatId && this.shareModeForChatId !== chatId) {
                this.endShareMode();
            }
            if (this.socket && this.isConnected) {
                this.socket.send(JSON.stringify({ type: 'join_chat', chat_id: chatId }));
            }
            void this._refreshChatMessages(chatId);
        }
    };

    // Новый чат: сразу активируем локально, создание на сервере идёт в фоне
    async newChat() {
        // Переиспользуем только чат с уже загруженной пустой историей.
        // Иначе messages=[] значит «ещё не подтянули», и открывается старый чат.
        const emptyChat = this.chats.find(
            (c) => c._messagesLoaded && (!c.messages || c.messages.length === 0)
        );
        if (emptyChat) {
            this.switchChat(emptyChat.id);
            return emptyChat.id;
        }

        const id = generateId();
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

        if (this.socket && this.isConnected) {
            this.socket.send(JSON.stringify({ type: 'join_chat', chat_id: id }));
            if (this.user) {
                this.socket.send(this.user + '|message|__NEW_CHAT__');
            }
        }

        if (API_URL) {
            // Создаём на сервере в фоне; локальный чат не откатываем —
            // sendMessage при необходимости повторит ensure.
            const createPromise = (async () => {
                try {
                    await apiFetch('/api/chats/', {
                        method: 'POST',
                        body: JSON.stringify({ id, title: 'Новый чат' })
                    });
                    this._ensuredServerChats.add(id);
                } catch (e) {
                    console.warn("Ошибка создания чата на сервере:", e);
                } finally {
                    delete this._pendingChatCreates[id];
                }
            })();
            this._pendingChatCreates[id] = createPromise;
        }

        return id;
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
            this._clearPingInterval();
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
                this._clearPingInterval();
                this._pingIntervalId = setInterval(() => {
                    if (this.socket?.readyState === WebSocket.OPEN) {
                        this.socket.send(JSON.stringify({ type: 'ping' }));
                    }
                }, 30000);
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
                this._clearPingInterval();
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
                const msgs = chat.messages || [];
                const already = msgs.some((m) =>
                    String(m.id) === String(msg.id) ||
                    (m.user === msg.user && m.content === msg.content &&
                        (m.deliveryStatus === 'sending' || m.deliveryStatus === 'sent'))
                );
                if (!already) {
                    chat.messages = [...msgs, msg];
                } else {
                    chat.messages = msgs.map((m) => {
                        if (
                            String(m.id) === String(msg.id) ||
                            (m.user === msg.user && m.content === msg.content &&
                                (m.deliveryStatus === 'sending' || m.deliveryStatus === 'sent'))
                        ) {
                            return { ...m, ...msg, deliveryStatus: 'sent' };
                        }
                        return m;
                    });
                }
                this._bumpChatInList(chatId);
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
                this._applyServerMessages(chat, data.messages);
                if (data.title != null && data.title !== '') {
                    chat.title = String(data.title).trim();
                }
                this.saveChats();
                // После F5: сервер говорит что генерация ещё идёт, либо последнее — от пользователя
                this._restoreTypingAfterHistory(data.chat_id, data.isTyping);
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
        else if (data.type === 'ping') {
            this.socket?.readyState === WebSocket.OPEN && this.socket.send(JSON.stringify({ type: 'pong' }));
        }
        else if (data.type === 'pong') {
            // keepalive — игнорируем
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
            const idx = chat?.messages?.findIndex(m => m.id === data.message_id);
            if (chat && idx >= 0) {
                const msg = chat.messages[idx];
                chat.messages[idx] = { ...msg, content: data.message ?? msg.content, isImage: data.isImage ?? msg.isImage };
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

    async _ensureChatOnServer(chatId, { timeoutMs = 15000 } = {}) {
        if (!chatId) return false;
        if (this._ensuredServerChats.has(chatId)) return true;

        const pending = this._pendingChatCreates[chatId];
        if (pending) {
            try {
                await Promise.race([
                    pending,
                    new Promise((_, reject) =>
                        setTimeout(() => reject(new Error('Создание чата слишком долго')), timeoutMs)
                    ),
                ]);
                if (this._ensuredServerChats.has(chatId)) return true;
            } catch (e) {
                console.warn('Ожидание создания чата:', e);
            }
        }

        if (!API_URL) {
            this._ensuredServerChats.add(chatId);
            return true;
        }
        try {
            await apiFetch('/api/chats/', {
                method: 'POST',
                body: JSON.stringify({ id: chatId, title: 'Новый чат' }),
            });
        } catch (e) {
            // Частый кейс: чат уже создан — продолжаем отправку
            console.warn('Ошибка создания чата на сервере:', e);
        }
        this._ensuredServerChats.add(chatId);
        return true;
    }

    _markLocalMessage(chatId, localMsgId, deliveryStatus) {
        const chat = this.chats.find((c) => c.id === chatId);
        const msg = chat?.messages?.find((m) => m.id === localMsgId);
        if (msg) {
            msg.deliveryStatus = deliveryStatus;
            this.saveChats();
        }
    }

    async _deliverMessage(chatId, content, localMsgId) {
        try {
            await this._ensureChatOnServer(chatId);
            if (!this.chats.some((c) => c.id === chatId)) {
                this._markLocalMessage(chatId, localMsgId, 'failed');
                this.loadingChatIds = this.loadingChatIds.filter((id) => id !== chatId);
                return;
            }
            if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
                this.error = "Нет соединения с сервером";
                this._markLocalMessage(chatId, localMsgId, 'failed');
                this.loadingChatIds = this.loadingChatIds.filter((id) => id !== chatId);
                return;
            }
            this.socket.send(`${this.user}|${chatId}|message|${content}`);
            this._markLocalMessage(chatId, localMsgId, 'sent');
        } catch (error) {
            console.error("Ошибка отправки сообщения:", error);
            this.error = "Ошибка при отправке сообщения";
            this._markLocalMessage(chatId, localMsgId, 'failed');
            this.loadingChatIds = this.loadingChatIds.filter((id) => id !== chatId);
        }
    }

    async sendMessage(content) {
        if (!this.isConnected || !this.socket) {
            this.error = "Нет соединения с сервером";
            return false;
        }
        if (!content.trim()) return false;

        if (!this.currentChatId) {
            await this.newChat();
        }

        const chatId = this.currentChatId;
        const chat = this.currentChat;
        if (!chatId || !chat) return false;

        // 1) сразу рисуем сообщение  2) очищаем инпут у UI  3) доставляем в фоне
        if (!this.loadingChatIds.includes(chatId)) this.loadingChatIds.push(chatId);
        this.error = null;
        const localMsgId = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
        chat.messages = [
            ...(chat.messages || []),
            {
                id: localMsgId,
                content,
                user: this.user,
                timestamp: new Date(),
                userId: this.getCurrentUserId(),
                deliveryStatus: 'sending',
            },
        ];
        this._bumpChatInList(chatId);
        this.saveChats();

        void this._deliverMessage(chatId, content, localMsgId);
        return true;
    };

    disconnect() {
        this._clearPingInterval();
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