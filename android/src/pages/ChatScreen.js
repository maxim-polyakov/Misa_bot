import React, { useState, useRef, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  Image,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Modal,
  ScrollView,
} from "react-native";
import { useStores } from "../store/rootStoreContext";
import { useUser } from "../context/UserContext";
import { API_URL } from "../config";

export default function ChatScreen() {
  const { chatStore } = useStores();
  const { user, setIsAuth } = useUser();
  const [message, setMessage] = useState("");
  const [chatsModalVisible, setChatsModalVisible] = useState(false);
  const flatListRef = useRef(null);

  const handleLogout = () => {
    chatStore.logout();
    setIsAuth(false);
  };

  useEffect(() => {
    if (chatStore.currentChatId && chatStore.isConnected) {
      chatStore.ensureJoinedToChat(chatStore.currentChatId);
    }
  }, [chatStore.currentChatId, chatStore.isConnected]);

  useEffect(() => {
    flatListRef.current?.scrollToEnd({ animated: true });
  }, [chatStore.messages]);

  const handleSend = async () => {
    if (!message.trim()) return;
    const text = message.trim();
    setMessage("");
    await chatStore.sendMessage(text);
  };

  const renderMessage = ({ item }) => {
    const isUser = item.user !== "Misa";
    const isImage = item.isImage || (item.content && /^https?:\/\//.test(item.content));
    return (
      <View style={[styles.msgRow, isUser ? styles.msgUser : styles.msgMisa]}>
        <View style={[styles.msgBubble, isUser ? styles.bubbleUser : styles.bubbleMisa]}>
          {isImage && (item.content.startsWith("http") || item.content.startsWith("/")) ? (
            <Image
              source={{ uri: item.content.startsWith("/") ? `${API_URL.replace(/\/$/, "")}${item.content}` : item.content }}
              style={styles.msgImage}
              resizeMode="contain"
            />
          ) : (
            <Text style={[styles.msgText, isUser && styles.msgTextUser]}>{item.content}</Text>
          )}
        </View>
      </View>
    );
  };

  return (
    <View style={styles.wrapper}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => setChatsModalVisible(true)} style={styles.menuBtn}>
          <Text style={styles.menuBtnText}>☰</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle} numberOfLines={1}>
          {chatStore.currentChat?.title || "Misa AI"}
        </Text>
        <TouchableOpacity onPress={() => chatStore.newChat()} style={styles.newChatBtn}>
          <Text style={styles.newChatBtnText}>+</Text>
        </TouchableOpacity>
      </View>
      <Modal visible={chatsModalVisible} animationType="slide" transparent>
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setChatsModalVisible(false)}
        >
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Чаты</Text>
              <TouchableOpacity onPress={() => setChatsModalVisible(false)}>
                <Text style={styles.closeBtn}>✕</Text>
              </TouchableOpacity>
            </View>
            <ScrollView>
              {chatStore.chats.map((c) => (
                <TouchableOpacity
                  key={c.id}
                  style={[styles.chatItem, c.id === chatStore.currentChatId && styles.chatItemActive]}
                  onPress={() => {
                    chatStore.switchChat(c.id);
                    setChatsModalVisible(false);
                  }}
                >
                  <Text numberOfLines={1} style={styles.chatItemTitle}>
                    {c.title || "Новый чат"}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
            <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
              <Text style={styles.logoutBtnText}>Выйти</Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </Modal>
      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
        keyboardVerticalOffset={90}
      >
      {chatStore.error ? (
        <View style={styles.errorBar}>
          <Text style={styles.errorText}>{chatStore.error}</Text>
          <TouchableOpacity onPress={() => chatStore.connect()}>
            <Text style={styles.retryText}>Повторить</Text>
          </TouchableOpacity>
        </View>
      ) : null}
      <FlatList
        ref={flatListRef}
        data={chatStore.messages}
        keyExtractor={(item) => item.id}
        renderItem={renderMessage}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={styles.emptyText}>Начните общение с Misa AI</Text>
          </View>
        }
        ListFooterComponent={
          chatStore.isLoading ? (
            <View style={styles.typing}>
              <ActivityIndicator size="small" />
              <Text style={styles.typingText}>Misa печатает...</Text>
            </View>
          ) : null
        }
      />
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder="Введите сообщение..."
          value={message}
          onChangeText={setMessage}
          multiline
          maxLength={4000}
          onSubmitEditing={handleSend}
        />
        <TouchableOpacity
          style={[styles.sendBtn, !message.trim() && styles.sendBtnDisabled]}
          onPress={handleSend}
          disabled={!message.trim()}
        >
          <Text style={styles.sendBtnText}>→</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: { flex: 1 },
  header: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
    backgroundColor: "#fff",
  },
  menuBtn: { padding: 8, marginRight: 8 },
  menuBtnText: { fontSize: 22 },
  headerTitle: { flex: 1, fontSize: 18, fontWeight: "600" },
  newChatBtn: { padding: 8 },
  newChatBtnText: { fontSize: 24, fontWeight: "300" },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.5)",
    justifyContent: "flex-start",
    paddingTop: 60,
  },
  modalContent: {
    backgroundColor: "#fff",
    borderTopLeftRadius: 16,
    borderTopRightRadius: 16,
    maxHeight: "80%",
  },
  modalHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#eee",
  },
  modalTitle: { fontSize: 18, fontWeight: "600" },
  closeBtn: { fontSize: 20, padding: 4 },
  chatItem: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#f0f0f0",
  },
  chatItemActive: { backgroundColor: "#e8f4f8" },
  chatItemTitle: { fontSize: 16 },
  logoutBtn: {
    padding: 16,
    alignItems: "center",
    borderTopWidth: 1,
    borderTopColor: "#eee",
  },
  logoutBtnText: { color: "#c00", fontSize: 16 },
  container: { flex: 1, backgroundColor: "#fff" },
  errorBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#fee",
    padding: 10,
  },
  errorText: { color: "#c00", flex: 1 },
  retryText: { color: "#0a7ea4", fontWeight: "600" },
  msgRow: { paddingHorizontal: 12, paddingVertical: 4 },
  msgUser: { alignItems: "flex-end" },
  msgMisa: { alignItems: "flex-start" },
  msgBubble: {
    maxWidth: "80%",
    padding: 12,
    borderRadius: 16,
  },
  bubbleUser: { backgroundColor: "#0a7ea4" },
  bubbleMisa: { backgroundColor: "#e8e8e8" },
  msgText: { fontSize: 16, color: "#333" },
  msgTextUser: { color: "#fff" },
  msgImage: { width: 200, height: 200, borderRadius: 8 },
  empty: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingVertical: 60,
  },
  emptyText: { fontSize: 18, color: "#888" },
  typing: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    gap: 8,
  },
  typingText: { color: "#888", fontSize: 14 },
  inputRow: {
    flexDirection: "row",
    padding: 12,
    borderTopWidth: 1,
    borderTopColor: "#eee",
    alignItems: "flex-end",
    gap: 8,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 24,
    paddingHorizontal: 16,
    paddingVertical: 10,
    maxHeight: 120,
    fontSize: 16,
  },
  sendBtn: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: "#0a7ea4",
    justifyContent: "center",
    alignItems: "center",
  },
  sendBtnDisabled: { backgroundColor: "#ccc" },
  sendBtnText: { color: "#fff", fontSize: 20, fontWeight: "bold" },
});
