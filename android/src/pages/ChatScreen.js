import React, { useState, useRef, useEffect } from "react";
import { observer } from "mobx-react-lite";
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
  Animated,
  ScrollView,
  useWindowDimensions,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import * as Clipboard from "expo-clipboard";
import { useStores } from "../store/rootStoreContext";
import { useUser } from "../context/UserContext";
import { API_URL } from "../config";

const SIDEBAR_WIDTH = 280;

const COLORS = {
  primaryBg: "#1c1c1e",
  secondaryBg: "#2c2c2e",
  messageBg: "#2c2c2e",
  userMessageBg: "#4a90e2",
  borderColor: "#3a3a3c",
  textPrimary: "#ffffff",
  textSecondary: "#8e8e93",
  accentColor: "#4a90e2",
  sidebarBg: "#2a2a2d",
};

function ChatScreen() {
  const { chatStore } = useStores();
  const { user, setIsAuth } = useUser();
  const [message, setMessage] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [copiedMsgId, setCopiedMsgId] = useState(null);
  const sidebarAnim = useRef(new Animated.Value(0)).current;
  const flatListRef = useRef(null);
  const { width: screenWidth, height: screenHeight } = useWindowDimensions();
  const insets = useSafeAreaInsets();

  const isSmallScreen = screenHeight < 600 || screenWidth < 360;

  const handleLogout = () => {
    setSidebarOpen(false);
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

  useEffect(() => {
    Animated.timing(sidebarAnim, {
      toValue: sidebarOpen ? 1 : 0,
      duration: 250,
      useNativeDriver: true,
    }).start();
  }, [sidebarOpen]);

  const sidebarTranslate = sidebarAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [-SIDEBAR_WIDTH, 0],
  });

  const overlayOpacity = sidebarAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 1],
  });

  const handleSend = async () => {
    if (!message.trim()) return;
    const text = message.trim();
    setMessage("");
    await chatStore.sendMessage(text);
  };

  const handleCopyMessage = async (msg) => {
    try {
      await Clipboard.setStringAsync(msg.content);
      setCopiedMsgId(msg.id);
      setTimeout(() => setCopiedMsgId(null), 1500);
    } catch (e) {}
  };

  const handleLike = (msg) => {
    const current = chatStore.getMessageFeedback(msg.id);
    chatStore.setMessageFeedback(msg.id, current === "like" ? null : "like");
  };

  const handleDislike = (msg) => {
    const current = chatStore.getMessageFeedback(msg.id);
    chatStore.setMessageFeedback(msg.id, current === "dislike" ? null : "dislike");
  };

  const handleRegenerate = (msg) => {
    chatStore.regenerateReply(msg.id);
  };

  const renderMessage = ({ item }) => {
    const isUser = item.user !== "Misa";
    const isImage = item.isImage || (item.content && /^https?:\/\//.test(item.content));
    const feedback = chatStore.getMessageFeedback(item.id);

    return (
      <View style={[styles.msgRow, isUser ? styles.msgUser : styles.msgMisa]}>
        <View style={[styles.msgBubble, isUser ? styles.bubbleUser : styles.bubbleMisa]}>
          {isImage && (item.content.startsWith("http") || item.content.startsWith("/")) ? (
            <Image
              source={{
                uri: item.content.startsWith("/") ? `${API_URL.replace(/\/$/, "")}${item.content}` : item.content,
              }}
              style={styles.msgImage}
              resizeMode="contain"
            />
          ) : (
            <Text style={[styles.msgText, isUser && styles.msgTextUser]}>{item.content}</Text>
          )}
          <Text style={styles.msgTime}>
            {new Date(item.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
          </Text>
          {!isUser && (
            <View style={styles.msgActions}>
              <TouchableOpacity
                style={styles.msgActionBtn}
                onPress={() => handleCopyMessage(item)}
              >
                <Text style={styles.msgActionIcon}>{copiedMsgId === item.id ? "✓" : "📋"}</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.msgActionBtn}
                onPress={() => handleRegenerate(item)}
              >
                <Text style={styles.msgActionIcon}>↻</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.msgActionBtn, feedback === "like" && styles.msgActionActive]}
                onPress={() => handleLike(item)}
              >
                <Text style={styles.msgActionIcon}>👍</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.msgActionBtn, feedback === "dislike" && styles.msgActionActive]}
                onPress={() => handleDislike(item)}
              >
                <Text style={styles.msgActionIcon}>👎</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      </View>
    );
  };

  const renderEmptyChat = () => (
    <ScrollView
      style={styles.emptyScroll}
      contentContainerStyle={[styles.emptyChat, isSmallScreen && styles.emptyChatSmall]}
      keyboardShouldPersistTaps="handled"
      showsVerticalScrollIndicator={false}
    >
      <Image source={require("../../assets/icon.png")} style={[styles.emptyLogo, isSmallScreen && styles.emptyLogoSmall]} />
      <Text style={[styles.emptyTitle, isSmallScreen && styles.emptyTitleSmall]}>Начните общение с Misa AI</Text>
      <Text style={[styles.emptyHint, isSmallScreen && styles.emptyHintSmall]}>Задайте вопрос или поделитесь мыслями</Text>
    </ScrollView>
  );

  const renderMessagesList = () => (
    <FlatList
      ref={flatListRef}
      data={chatStore.messages}
      keyExtractor={(item) => item.id}
      renderItem={renderMessage}
      style={styles.flatList}
      contentContainerStyle={styles.messagesContent}
      ListFooterComponent={
        chatStore.isLoading ? (
          <View style={styles.typing}>
            <ActivityIndicator size="small" color={COLORS.accentColor} />
            <Text style={styles.typingText}>Misa печатает...</Text>
          </View>
        ) : null
      }
      keyboardShouldPersistTaps="handled"
    />
  );

  const renderSidebar = () => (
    <Animated.View style={[styles.sidebar, { transform: [{ translateX: sidebarTranslate }] }]}>
      <View style={styles.sidebarHeader}>
        <Image source={require("../../assets/icon.png")} style={styles.sidebarLogo} />
        <Text style={styles.sidebarBrand}>Misa AI Чат</Text>
        <TouchableOpacity style={styles.sidebarCloseBtn} onPress={() => setSidebarOpen(false)}>
          <Text style={styles.sidebarCloseText}>✕</Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity style={styles.newChatBtn} onPress={() => { chatStore.newChat(); setSidebarOpen(false); }}>
        <Text style={styles.newChatBtnText}>+ Новый чат</Text>
      </TouchableOpacity>
      <View style={styles.chatList}>
        {chatStore.chats.map((c) => (
          <TouchableOpacity
            key={c.id}
            style={[styles.chatItem, c.id === chatStore.currentChatId && styles.chatItemActive]}
            onPress={() => { chatStore.switchChat(c.id); setSidebarOpen(false); }}
          >
            <Text style={styles.chatItemIcon}>💬</Text>
            <Text numberOfLines={1} style={styles.chatItemTitle}>
              {chatStore.getChatTitle(c)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      <View style={styles.sidebarFooter}>
        <TouchableOpacity style={styles.profileBtn} onPress={handleLogout}>
          <Text style={styles.profileAvatar}>
            {(user?.display_name || user?.email || "?")[0].toUpperCase()}
          </Text>
          <Text style={styles.profileName} numberOfLines={1}>
            {user?.display_name || user?.email || "Пользователь"}
          </Text>
        </TouchableOpacity>
      </View>
    </Animated.View>
  );

  const isEmpty = chatStore.messages.length === 0;
  const inputPaddingBottom = Math.max(insets.bottom, 8);

  const inputBlock = (
    <View
      style={[
        styles.inputRow,
        { backgroundColor: COLORS.primaryBg, borderTopColor: COLORS.borderColor, paddingBottom: inputPaddingBottom },
        isSmallScreen && styles.inputRowSmall,
      ]}
    >
      <TextInput
        style={[styles.input, isSmallScreen && styles.inputSmall]}
        placeholder="Введите сообщение..."
        placeholderTextColor={COLORS.textSecondary}
        value={message}
        onChangeText={setMessage}
        multiline
        maxLength={4000}
        editable={!chatStore.isLoading && chatStore.isConnected}
      />
      <TouchableOpacity
        style={[
          styles.sendBtn,
          (!message.trim() || chatStore.isLoading || !chatStore.isConnected) && styles.sendBtnDisabled,
        ]}
        onPress={handleSend}
        disabled={!message.trim() || chatStore.isLoading || !chatStore.isConnected}
      >
        <Text style={styles.sendBtnText}>➤</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.wrapper}>
      <Animated.View
        style={[styles.overlay, { opacity: overlayOpacity }]}
        pointerEvents={sidebarOpen ? "auto" : "none"}
      >
        <TouchableOpacity style={StyleSheet.absoluteFill} onPress={() => setSidebarOpen(false)} activeOpacity={1} />
      </Animated.View>

      {renderSidebar()}

      <View style={[styles.main, { paddingTop: insets.top }]}>
        <View style={[styles.header, { backgroundColor: COLORS.primaryBg, borderBottomColor: COLORS.borderColor }]}>
          <TouchableOpacity onPress={() => setSidebarOpen(true)} style={styles.menuBtn}>
            <Text style={styles.menuBtnText}>☰</Text>
          </TouchableOpacity>
          <Text style={[styles.headerTitle, isSmallScreen && styles.headerTitleSmall]} numberOfLines={1}>
            {chatStore.currentChat?.title || "Misa AI"}
          </Text>
          <TouchableOpacity onPress={() => chatStore.newChat()} style={styles.newChatBtnHeader}>
            <Text style={styles.newChatBtnHeaderText}>+</Text>
          </TouchableOpacity>
        </View>

        {chatStore.error ? (
          <View style={styles.errorBar}>
            <Text style={styles.errorText}>{chatStore.error}</Text>
            <TouchableOpacity onPress={() => chatStore.connect()}>
              <Text style={styles.retryText}>Повторить</Text>
            </TouchableOpacity>
          </View>
        ) : null}

        <KeyboardAvoidingView
          style={[styles.container, { backgroundColor: COLORS.primaryBg }]}
          behavior={Platform.OS === "ios" ? "padding" : "padding"}
          keyboardVerticalOffset={Platform.OS === "ios" ? 0 : 20}
        >
          <View style={styles.contentArea}>
            {isEmpty ? renderEmptyChat() : renderMessagesList()}
          </View>
          {inputBlock}
        </KeyboardAvoidingView>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: { flex: 1 },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(0,0,0,0.5)",
    zIndex: 100,
  },
  sidebar: {
    position: "absolute",
    left: 0,
    top: 0,
    bottom: 0,
    width: SIDEBAR_WIDTH,
    backgroundColor: COLORS.sidebarBg,
    zIndex: 101,
    borderRightWidth: 1,
    borderRightColor: COLORS.borderColor,
  },
  sidebarHeader: {
    flexDirection: "row",
    alignItems: "center",
    padding: 16,
    gap: 12,
  },
  sidebarLogo: {
    width: 28,
    height: 28,
    borderRadius: 6,
  },
  sidebarBrand: {
    flex: 1,
    fontSize: 18,
    fontWeight: "600",
    color: COLORS.textPrimary,
  },
  sidebarCloseBtn: {
    padding: 8,
  },
  sidebarCloseText: {
    color: COLORS.textPrimary,
    fontSize: 18,
  },
  newChatBtn: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    marginHorizontal: 12,
    marginBottom: 12,
    backgroundColor: "rgba(255,255,255,0.08)",
    borderRadius: 8,
  },
  newChatBtnText: {
    color: COLORS.textPrimary,
    fontSize: 16,
  },
  chatList: {
    flex: 1,
    paddingHorizontal: 12,
  },
  chatItem: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    borderRadius: 8,
    marginBottom: 4,
  },
  chatItemActive: {
    backgroundColor: COLORS.messageBg,
  },
  chatItemIcon: {
    fontSize: 16,
    marginRight: 8,
  },
  chatItemTitle: {
    flex: 1,
    color: COLORS.textPrimary,
    fontSize: 14,
  },
  sidebarFooter: {
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: COLORS.borderColor,
  },
  profileBtn: {
    flexDirection: "row",
    alignItems: "center",
  },
  profileAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: COLORS.accentColor,
    color: COLORS.textPrimary,
    fontSize: 16,
    fontWeight: "600",
    textAlign: "center",
    lineHeight: 36,
    marginRight: 10,
  },
  profileName: {
    flex: 1,
    color: COLORS.textPrimary,
    fontSize: 14,
  },
  main: { flex: 1 },
  header: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  menuBtn: { padding: 8, marginRight: 8 },
  menuBtnText: { fontSize: 22, color: COLORS.textPrimary },
  headerTitle: { flex: 1, fontSize: 18, fontWeight: "600", color: COLORS.textPrimary },
  headerTitleSmall: { fontSize: 16 },
  newChatBtnHeader: { padding: 8 },
  newChatBtnHeaderText: { fontSize: 24, fontWeight: "300", color: COLORS.textPrimary },
  errorBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "rgba(239,68,68,0.15)",
    padding: 10,
  },
  errorText: { color: "#ef4444", flex: 1 },
  retryText: { color: COLORS.accentColor, fontWeight: "600" },
  container: { flex: 1, minHeight: 0 },
  contentArea: { flex: 1, minHeight: 0 },
  flatList: { flex: 1 },
  messagesContent: { padding: 16, paddingBottom: 24 },
  msgRow: { paddingHorizontal: 12, paddingVertical: 6 },
  msgUser: { alignItems: "flex-end" },
  msgMisa: { alignItems: "flex-start" },
  msgBubble: {
    maxWidth: "85%",
    padding: 12,
    borderRadius: 16,
  },
  bubbleUser: { backgroundColor: COLORS.userMessageBg },
  bubbleMisa: {
    backgroundColor: COLORS.messageBg,
    borderWidth: 1,
    borderColor: COLORS.borderColor,
  },
  msgText: { fontSize: 16, color: COLORS.textPrimary },
  msgTextUser: { color: "#fff" },
  msgTime: {
    fontSize: 11,
    color: COLORS.textSecondary,
    marginTop: 8,
  },
  msgActions: {
    flexDirection: "row",
    alignItems: "center",
    paddingTop: 8,
    gap: 4,
  },
  msgActionBtn: {
    padding: 6,
  },
  msgActionActive: {
    opacity: 1,
  },
  msgActionIcon: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  msgImage: { width: 200, height: 200, borderRadius: 8 },
  emptyScroll: { flex: 1 },
  emptyChat: {
    flexGrow: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingVertical: 24,
    paddingHorizontal: 20,
  },
  emptyChatSmall: {
    paddingVertical: 16,
  },
  emptyLogo: {
    width: 48,
    height: 48,
    borderRadius: 8,
    marginBottom: 16,
  },
  emptyLogoSmall: {
    width: 40,
    height: 40,
    marginBottom: 12,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: "600",
    color: COLORS.textPrimary,
    marginBottom: 8,
    textAlign: "center",
  },
  emptyTitleSmall: {
    fontSize: 20,
    marginBottom: 6,
  },
  emptyHint: {
    fontSize: 15,
    color: COLORS.textSecondary,
    textAlign: "center",
  },
  emptyHintSmall: {
    fontSize: 14,
  },
  inputRow: {
    flexDirection: "row",
    paddingHorizontal: 12,
    paddingTop: 12,
    paddingBottom: 12,
    borderTopWidth: 1,
    alignItems: "flex-end",
    gap: 8,
  },
  inputRowSmall: {
    paddingHorizontal: 10,
    paddingTop: 10,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: COLORS.borderColor,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 12,
    maxHeight: 120,
    fontSize: 16,
    backgroundColor: COLORS.secondaryBg,
    color: COLORS.textPrimary,
  },
  inputSmall: {
    paddingHorizontal: 12,
    paddingVertical: 10,
    maxHeight: 100,
    fontSize: 15,
  },
  sendBtn: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: COLORS.accentColor,
    justifyContent: "center",
    alignItems: "center",
  },
  sendBtnDisabled: { backgroundColor: COLORS.borderColor, opacity: 0.5 },
  sendBtnText: { color: "#fff", fontSize: 18, fontWeight: "bold" },
  typing: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    gap: 8,
  },
  typingText: { color: COLORS.textSecondary, fontSize: 14 },
});

export default observer(ChatScreen);
