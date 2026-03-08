import { makeAutoObservable } from "mobx";
import { API_URL, API_WSS } from "../config";
import { apiFetch } from "../api/http";
import { storage } from "../storage";

const generateId = () => Date.now().toString(36) + Math.random().toString(36).slice(2);

class ChatStore {
  chats = [];
  currentChatId = null;
  isConnected = false;
  isConnecting = false;
  loadingChatIds = [];
  error = null;
  socket = null;
  reconnectAttempts = 0;
  maxReconnectAttempts = 8;
  reconnectDelay = 1000;
  user = null;
  isAuth = false;
  _pingIntervalId = null;
  _userId = null;

  constructor(rootStore) {
    this.rootStore = rootStore;
    makeAutoObservable(this);
  }

  get messages() {
    const chat = this.chats.find((c) => c.id === this.currentChatId);
    return chat ? chat.messages : [];
  }

  get currentChat() {
    return this.chats.find((c) => c.id === this.currentChatId);
  }

  get isLoading() {
    return this.loadingChatIds.length > 0;
  }

  isChatLoading(chatId) {
    return this.loadingChatIds.includes(chatId);
  }

  getChatTitle(chat) {
    if (chat?.title && chat.title !== "Новый чат") return chat.title;
    const firstUser = chat?.messages?.find((m) => m.user !== "Misa");
    if (firstUser?.content) return firstUser.content.slice(0, 40) + (firstUser.content.length > 40 ? "…" : "");
    return "Новый чат";
  }

  async getCurrentUserId() {
    return this._userId || (await storage.getItem("currentUserId"));
  }

  setUser(email, id) {
    this.user = email;
    this._userId = id;
    this.isAuth = true;
    storage.setItem("currentUser", email);
    if (id) storage.setItem("currentUserId", String(id));
    this.loadChats();
  }

  logout() {
    this.disconnect();
    this.user = null;
    this._userId = null;
    this.isAuth = false;
    storage.removeItem("currentUser");
    storage.removeItem("currentUserId");
    storage.removeItem("token");
    storage.removeItem("userProfile");
  }

  clearUserFromStorage() {
    this.logout();
  }

  async deleteAllChats() {
    if (API_URL) {
      try {
        for (const chat of [...this.chats]) {
          await apiFetch(`/api/chats/${chat.id}/delete/`, { method: "DELETE" });
        }
      } catch (e) {
        console.warn("Ошибка удаления чатов:", e);
      }
    }
    this.chats = [];
    await this.newChat();
  }

  getConversationsExportData() {
    return {
      exportedAt: new Date().toISOString(),
      conversations: this.chats.map((c) => ({
        id: c.id,
        title: c.title,
        createdAt: c.createdAt,
        messages: (c.messages || []).map((m) => ({
          content: m.content,
          user: m.user,
          timestamp: m.timestamp,
        })),
      })),
    };
  }

  _clearPingInterval() {
    if (this._pingIntervalId) {
      clearInterval(this._pingIntervalId);
      this._pingIntervalId = null;
    }
  }

  async loadChats() {
    const userId = await this.getCurrentUserId();
    if (!userId) {
      this.chats = [];
      this.currentChatId = null;
      return;
    }
    if (!API_URL) return;
    try {
      const chatsData = await apiFetch("/api/chats/");
      if (Array.isArray(chatsData) && chatsData.length > 0) {
        this.chats = chatsData.map((c) => ({
          id: c.id,
          title: c.title || "Новый чат",
          messages: [],
          createdAt: c.createdAt ? new Date(c.createdAt) : new Date(),
          _messagesLoaded: false,
        }));
        this.currentChatId = this.chats[0].id;
        this._loadChatMessagesIfNeeded(this.chats[0].id);
      } else {
        this.chats = [];
        await this.newChat();
      }
    } catch (e) {
      console.warn("Ошибка загрузки чатов:", e);
      this.chats = [];
      await this.newChat();
    }
  }

  async _loadChatMessagesIfNeeded(chatId) {
    const chat = this.chats.find((c) => c.id === chatId);
    if (!chat || chat._messagesLoaded) return;
    if (this.socket && this.isConnected) {
      this.socket.send(JSON.stringify({ type: "load_history", chat_id: chatId }));
      chat._pendingHistory = true;
    } else if (API_URL) {
      try {
        const msgs = await apiFetch(`/api/chats/${chatId}/messages/`);
        chat.messages = (msgs || []).map((m) => ({
          id: String(m.id),
          content: m.content,
          user: m.user,
          timestamp: new Date(m.timestamp),
          isImage: m.isImage,
        }));
        chat._messagesLoaded = true;
      } catch (e) {
        console.warn("Ошибка загрузки сообщений:", e);
      }
    }
  }

  async saveChats() {
    const userId = await this.getCurrentUserId();
    if (userId && this.chats.length > 0) {
      await storage.setItem(
        `chats_${userId}`,
        JSON.stringify(
          this.chats.map((c) => ({
            ...c,
            messages: c.messages || [],
            createdAt: c.createdAt?.toISOString?.() || c.createdAt,
          }))
        )
      );
    }
  }

  switchChat(chatId) {
    if (this.chats.some((c) => c.id === chatId)) {
      this.currentChatId = chatId;
      if (this.socket && this.isConnected) {
        this.socket.send(JSON.stringify({ type: "join_chat", chat_id: chatId }));
      }
      this._loadChatMessagesIfNeeded(chatId);
    }
  }

  ensureJoinedToChat(chatId) {
    if (this.socket && this.isConnected && chatId) {
      this.socket.send(JSON.stringify({ type: "join_chat", chat_id: chatId }));
    }
  }

  async newChat() {
    const emptyChat = this.chats.find((c) => !c.messages || c.messages.length === 0);
    if (emptyChat) {
      this.switchChat(emptyChat.id);
      return;
    }
    let id = generateId();
    if (API_URL) {
      try {
        const res = await apiFetch("/api/chats/", {
          method: "POST",
          body: JSON.stringify({ id, title: "Новый чат" }),
        });
        if (res?.id) id = res.id;
      } catch (e) {
        console.warn("Ошибка создания чата:", e);
      }
    }
    const newChat = {
      id,
      title: "Новый чат",
      messages: [],
      createdAt: new Date(),
      _messagesLoaded: true,
    };
    this.chats.unshift(newChat);
    this.currentChatId = id;
    this.saveChats();
    if (this.socket && this.isConnected && this.user) {
      this.socket.send(this.user + "|message|__NEW_CHAT__");
    }
  }

  connect() {
    if (this.isConnecting || this.isConnected) return;
    this.isConnecting = true;
    this.error = null;
    this._clearPingInterval();
    if (this.socket) {
      this.socket.close(1000, "Reconnecting");
      this.socket = null;
    }
    try {
      this.socket = new WebSocket(API_WSS);
      this.socket.onopen = () => {
        this.isConnected = true;
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.reconnectDelay = 1000;
        this._pingIntervalId = setInterval(() => {
          if (this.socket?.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({ type: "ping" }));
          }
        }, 30000);
        if (this.currentChatId) {
          this.socket.send(JSON.stringify({ type: "load_history", chat_id: this.currentChatId }));
        }
      };
      this.socket.onmessage = (e) => {
        try {
          const data = JSON.parse(e.data);
          this.handleIncomingMessage(data);
        } catch (err) {
          console.error("Parse error:", err);
        }
      };
      this.socket.onclose = (e) => {
        this._clearPingInterval();
        this.isConnected = false;
        this.isConnecting = false;
        if (e.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts && this.isAuth) {
          this.reconnectAttempts++;
          this.reconnectDelay = Math.min(this.reconnectDelay * 1.5, 30000);
          setTimeout(() => this.connect(), this.reconnectDelay);
        }
      };
      this.socket.onerror = () => {
        this.isConnecting = false;
        this.error = "Ошибка подключения";
      };
    } catch (err) {
      this.isConnecting = false;
      this.error = "Не удалось подключиться";
    }
  }

  handleIncomingMessage(data) {
    if (data.type === "chat_message") {
      const msg = {
        id: data.message_id || Date.now().toString() + Math.random().toString(36).slice(2),
        content: data.message,
        user: data.user || "Misa",
        timestamp: new Date(),
        isImage: data.isImage,
      };
      const chatId = data.chat_id || this.currentChatId;
      const chat = this.chats.find((c) => c.id === chatId);
      if (chat) {
        chat.messages.push(msg);
        if (data.user === "Misa") {
          this.loadingChatIds = this.loadingChatIds.filter((id) => id !== chatId);
        } else {
          if (!this.loadingChatIds.includes(chatId)) this.loadingChatIds.push(chatId);
        }
        this.saveChats();
      }
    } else if (data.type === "history") {
      const chat = this.chats.find((c) => c.id === data.chat_id);
      if (chat) {
        chat.messages = (data.messages || []).map((m) => ({
          id: String(m.id),
          content: m.content,
          user: m.user,
          timestamp: new Date(m.timestamp),
          isImage: m.isImage,
          feedback: m.feedback,
          feedbackCategories: m.feedbackCategories,
          feedbackComment: m.feedbackComment,
        }));
        if (data.title != null && data.title !== "") chat.title = String(data.title).trim();
        chat._messagesLoaded = true;
        chat._pendingHistory = false;
        this.saveChats();
      }
    } else if (data.type === "connection_established") {
      if (this.currentChatId) {
        this.socket?.send(JSON.stringify({ type: "load_history", chat_id: this.currentChatId }));
      }
    } else if (data.type === "ping") {
      this.socket?.readyState === WebSocket.OPEN && this.socket.send(JSON.stringify({ type: "pong" }));
    } else if (data.type === "chat_title") {
      const chat = this.chats.find((c) => c.id === data.chat_id);
      if (chat && data.title) {
        chat.title = data.title.trim().slice(0, 500);
        this.saveChats();
      }
    } else if (data.type === "message_updated") {
      const chat = this.chats.find((c) => c.id === data.chat_id);
      const msg = chat?.messages?.find((m) => m.id === data.message_id);
      if (msg) {
        msg.content = data.message || msg.content;
        msg.isImage = data.isImage ?? msg.isImage;
        this.loadingChatIds = this.loadingChatIds.filter((id) => id !== data.chat_id);
        this.saveChats();
      }
    }
  }

  getMessageFeedback(msgId) {
    const msg = this.currentChat?.messages?.find((m) => m.id === msgId);
    return msg?.feedback ?? null;
  }

  async setMessageFeedback(msgId, feedback, categories = null, comment = null) {
    const chat = this.currentChat;
    const idx = chat?.messages?.findIndex((m) => m.id === msgId);
    if (idx == null || idx < 0) return;
    const msg = chat.messages[idx];
    const prev = msg?.feedback ?? null;
    chat.messages[idx] = {
      ...msg,
      feedback,
      feedbackCategories: feedback === "dislike" ? categories || [] : null,
      feedbackComment: feedback === "dislike" ? comment || null : null,
    };
    this.saveChats();
    if (API_URL) {
      try {
        await apiFetch(`/api/chats/${this.currentChatId}/messages/${msgId}/feedback/`, {
          method: "PATCH",
          body: JSON.stringify({ feedback, categories: categories || [], comment: comment || "" }),
        });
      } catch (e) {
        chat.messages[idx] = { ...msg, feedback: prev };
        this.saveChats();
      }
    }
  }

  regenerateReply(msgId) {
    if (!this.isConnected || !this.socket || !this.currentChatId) return false;
    const msg = this.currentChat?.messages?.find((m) => m.id === msgId);
    if (!msg || msg.user !== "Misa") return false;
    if (!this.loadingChatIds.includes(this.currentChatId)) {
      this.loadingChatIds = [...this.loadingChatIds, this.currentChatId];
    }
    try {
      this.socket.send(
        JSON.stringify({
          type: "regenerate",
          chat_id: this.currentChatId,
          message_id: msgId,
          user: this.user,
        })
      );
      return true;
    } catch (e) {
      this.loadingChatIds = this.loadingChatIds.filter((id) => id !== this.currentChatId);
      return false;
    }
  }

  async sendMessage(content) {
    if (!this.socket || !this.isConnected) {
      this.error = "Нет соединения";
      return false;
    }
    if (!content.trim()) return false;
    const chatId = this.currentChatId;
    if (!chatId) {
      await this.newChat();
      return this.sendMessage(content);
    }
    const chat = this.currentChat;
    if (!chat) return false;
    const isFirst = chat.messages.filter((m) => m.user !== "Misa").length === 0;
    if (isFirst && API_URL) {
      try {
        await apiFetch("/api/chats/", {
          method: "POST",
          body: JSON.stringify({ id: chatId, title: "Новый чат" }),
        });
      } catch (e) {}
    }
    if (!this.loadingChatIds.includes(chatId)) this.loadingChatIds.push(chatId);
    this.error = null;
    chat.messages.push({
      id: Date.now().toString(),
      content,
      user: this.user,
      timestamp: new Date(),
    });
    this.saveChats();
    try {
      const payload = `${this.user}|${chatId}|message|${content}`;
      this.socket.send(payload);
      return true;
    } catch (e) {
      this.error = "Ошибка отправки";
      this.loadingChatIds = this.loadingChatIds.filter((id) => id !== chatId);
      return false;
    }
  }

  disconnect() {
    this._clearPingInterval();
    if (this.socket) {
      this.socket.close(1000, "Close");
      this.socket = null;
    }
    this.isConnected = false;
    this.isConnecting = false;
  }
}

export default ChatStore;
