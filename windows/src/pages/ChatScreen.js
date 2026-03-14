import React, { useState, useRef, useEffect, useMemo } from "react";
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
  Alert,
  AppState,
  Modal,
  Pressable,
  Share,
} from "react-native";
import MaterialCommunityIcons from "react-native-vector-icons/MaterialCommunityIcons";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import Clipboard from "../utils/clipboard";
import { useStores } from "../store/rootStoreContext";
import { useUser } from "../context/UserContext";
import { useTheme } from "../context/ThemeContext";
import { useLocale } from "../context/LocaleContext";
import { getIntlLocale, formatMonthYear, formatTime } from "../utils/locale";
import { API_URL } from "../config";
import SettingsModal from "./SettingsModal";

const SIDEBAR_WIDTH = 280;

const getBlockType = (language) => {
  const lang = (language || "plaintext").toLowerCase();
  const typeMap = {
    json: "json", yaml: "yaml", yml: "yaml", xml: "xml",
    bash: "bash", sh: "bash", shell: "bash", sql: "sql",
    md: "md", markdown: "md", diff: "diff",
    warning: "warning", warn: "warning", error: "error", err: "error",
    quote: "quote", citation: "quote", output: "output", log: "output",
  };
  return typeMap[lang] || "code";
};

const parseMessageContent = (content) => {
  if (!content || typeof content !== "string") return [{ type: "text", content: "" }];
  const parts = [];
  const regex = /```\s*([\w+-]*)\s*\r?\n([\s\S]*?)```/g;
  let lastIndex = 0;
  let match;
  while ((match = regex.exec(content)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ type: "text", content: content.slice(lastIndex, match.index) });
    }
    const language = match[1] || "plaintext";
    parts.push({
      type: "code",
      language,
      blockType: getBlockType(language),
      content: match[2].trim(),
    });
    lastIndex = regex.lastIndex;
  }
  if (lastIndex < content.length) {
    parts.push({ type: "text", content: content.slice(lastIndex) });
  }
  return parts.length ? parts : [{ type: "text", content }];
};

function ChatScreen() {
  const { chatStore } = useStores();
  const { user, setIsAuth } = useUser();
  const { colors } = useTheme();
  const { t, locale, isRTL } = useLocale();
  const styles = useMemo(() => createStyles(colors), [colors]);
  const [message, setMessage] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [copiedMsgId, setCopiedMsgId] = useState(null);
  const [feedbackModalMsgId, setFeedbackModalMsgId] = useState(null);
  const [feedbackCategories, setFeedbackCategories] = useState([]);
  const [feedbackComment, setFeedbackComment] = useState("");
  const [chatMenuOpen, setChatMenuOpen] = useState(null);
  const [renameModalChatId, setRenameModalChatId] = useState(null);
  const [renameInputValue, setRenameInputValue] = useState("");
  const sidebarAnim = useRef(new Animated.Value(0)).current;
  const flatListRef = useRef(null);
  const { width: screenWidth, height: screenHeight } = useWindowDimensions();
  const insets = useSafeAreaInsets();

  const isSmallScreen = screenHeight < 600 || screenWidth < 360;

  const handleLogout = () => {
    setProfileOpen(false);
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
    const sub = AppState.addEventListener("change", (state) => {
      if (state === "active" && chatStore.isAuth) {
        chatStore.loadChats();
      }
    });
    return () => sub?.remove?.();
  }, [chatStore.isAuth]);

  useEffect(() => {
    flatListRef.current?.scrollToEnd({ animated: true });
  }, [chatStore.messages]);

  useEffect(() => {
    Animated.timing(sidebarAnim, {
      toValue: sidebarOpen ? 1 : 0,
      duration: 250,
      useNativeDriver: Platform.OS !== "windows",
    }).start();
  }, [sidebarOpen]);

  const sidebarTranslate = sidebarAnim.interpolate({
    inputRange: [0, 1],
    outputRange: isRTL ? [SIDEBAR_WIDTH, 0] : [-SIDEBAR_WIDTH, 0],
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
      Clipboard.setString(msg.content);
      setCopiedMsgId(msg.id);
      setTimeout(() => setCopiedMsgId(null), 1500);
    } catch (e) {}
  };

  const FEEDBACK_CATEGORIES = [
    { id: "harmful", label: t("feedbackHarmful") },
    { id: "fake", label: t("feedbackFake") },
    { id: "unhelpful", label: t("feedbackUnhelpful") },
    { id: "others", label: t("feedbackOthers") },
  ];

  const handleLike = (msg) => {
    const current = chatStore.getMessageFeedback(msg.id);
    chatStore.setMessageFeedback(msg.id, current === "like" ? null : "like");
  };

  const handleDislike = (msg) => {
    const current = chatStore.getMessageFeedback(msg.id);
    if (current === "dislike") {
      chatStore.setMessageFeedback(msg.id, null);
    } else {
      setFeedbackModalMsgId(msg.id);
      setFeedbackCategories(msg.feedbackCategories || []);
      setFeedbackComment(msg.feedbackComment || "");
    }
  };

  const toggleFeedbackCategory = (id) => {
    setFeedbackCategories((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]
    );
  };

  const handleFeedbackSubmit = async () => {
    if (feedbackModalMsgId) {
      await chatStore.setMessageFeedback(
        feedbackModalMsgId,
        "dislike",
        feedbackCategories,
        feedbackComment
      );
      setFeedbackModalMsgId(null);
      setFeedbackCategories([]);
      setFeedbackComment("");
    }
  };

  const handleFeedbackCancel = () => {
    setFeedbackModalMsgId(null);
    setFeedbackCategories([]);
    setFeedbackComment("");
  };

  const handleRegenerate = (msg) => {
    chatStore.regenerateReply(msg.id);
  };

  const handleShareMessage = async (chatId, msg) => {
    let messageIds = null;
    if (msg && msg.user === "Misa") {
      const chat = chatStore.chats.find((c) => c.id === (chatId ?? chatStore.currentChatId));
      const idx = chat?.messages?.findIndex((m) => m.id === msg.id);
      if (idx != null && idx >= 0) {
        const ids = [msg.id];
        if (idx > 0) {
          const prev = chat.messages[idx - 1];
          if (prev?.user !== "Misa") ids.unshift(prev.id);
        }
        messageIds = ids;
      }
    }
    const url = chatStore.getShareLink(chatId ?? chatStore.currentChatId, messageIds);
    try {
      await Share.share({
        message: url,
        url: Platform.OS === "ios" ? url : undefined,
        title: t("shareChatTitle"),
      });
    } catch (e) {
      Clipboard.setString(url);
      Alert.alert(t("linkCopied"), t("linkCopiedDesc"));
    }
  };

  const handleChatMenuToggle = (chatId) => {
    setChatMenuOpen((prev) => (prev === chatId ? null : chatId));
  };

  const handleRename = (chat) => {
    setChatMenuOpen(null);
    setRenameModalChatId(chat.id);
    setRenameInputValue(chatStore.getChatTitle(chat));
  };

  const handleRenameSubmit = async () => {
    if (renameModalChatId && renameInputValue.trim()) {
      await chatStore.renameChat(renameModalChatId, renameInputValue.trim());
      setRenameModalChatId(null);
      setRenameInputValue("");
    }
  };

  const handlePin = (chatId) => {
    chatStore.togglePinChat(chatId);
    setChatMenuOpen(null);
  };

  const handleShareFromMenu = async (chatId) => {
    setChatMenuOpen(null);
    setSidebarOpen(false);
    setProfileOpen(false);
    await handleShareMessage(chatId);
  };

  const handleDelete = (chatId) => {
    setChatMenuOpen(null);
    Alert.alert(
      t("confirmDeleteChat"),
      t("confirmDeleteChatDesc"),
      [
        { text: t("cancel"), style: "cancel" },
        {
          text: t("delete"),
          style: "destructive",
          onPress: async () => {
            await chatStore.deleteChat(chatId);
            setSidebarOpen(false);
            setProfileOpen(false);
          },
        },
      ]
    );
  };

  const renderMessageContent = (content, isUser) => {
    const parsed = parseMessageContent(content);
    return (
      <View style={styles.msgContentWrap}>
        {parsed.map((part, i) =>
          part.type === "text" ? (
            <Text key={i} style={[styles.msgText, isUser && styles.msgTextUser]}>
              {part.content}
            </Text>
          ) : (
            <View
              key={i}
              style={[
                styles.codeBlock,
                styles[`codeBlock_${part.blockType}`] || styles.codeBlock_code,
                isUser && styles.codeBlockUser,
              ]}
            >
              <View
                style={[
                  styles.codeBlockHeaderWrap,
                  styles[`codeBlockHeader_${part.blockType}`] || styles.codeBlockHeader_code,
                  isUser && styles.codeBlockHeaderWrapUser,
                ]}
              >
                <Text style={styles.codeBlockHeader}>{part.language}</Text>
              </View>
              <Text style={[styles.msgText, styles.codeBlockText, isUser && styles.codeBlockTextUser]}>{part.content}</Text>
            </View>
          )
        )}
      </View>
    );
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
            renderMessageContent(item.content, isUser)
          )}
          <Text style={styles.msgTime}>
            {formatTime(getIntlLocale(locale), new Date(item.timestamp))}
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
                <MaterialCommunityIcons
                  name={feedback === "like" ? "thumb-up" : "thumb-up-outline"}
                  size={18}
                  color={feedback === "like" ? colors.accentColor : colors.textSecondary}
                />
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.msgActionBtn, feedback === "dislike" && styles.msgActionActive]}
                onPress={() => handleDislike(item)}
              >
                <MaterialCommunityIcons
                  name={feedback === "dislike" ? "thumb-down" : "thumb-down-outline"}
                  size={18}
                  color={feedback === "dislike" ? "#ef4444" : colors.textSecondary}
                />
              </TouchableOpacity>
              <TouchableOpacity style={styles.msgActionBtn} onPress={() => handleShareMessage(chatStore.currentChatId, item)}>
                <Text style={styles.msgActionIcon}>↗</Text>
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
      <View style={[styles.emptyHeader, isSmallScreen && styles.emptyHeaderSmall]}>
        <View style={[styles.emptyLogoWrap, isSmallScreen && styles.emptyLogoWrapSmall]}>
          <Image
            source={require("../../assets/misa.png")}
            style={[styles.emptyLogo, isSmallScreen && styles.emptyLogoSmall]}
            resizeMode="contain"
          />
        </View>
        <View style={styles.emptyTextBlock}>
          <Text style={[styles.emptyTitle, isSmallScreen && styles.emptyTitleSmall]}>{t("startChat")}</Text>
          <Text style={[styles.emptyHint, isSmallScreen && styles.emptyHintSmall]}>{t("startHint")}</Text>
        </View>
      </View>
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
            <ActivityIndicator size="small" color={colors.accentColor} />
            <Text style={styles.typingText}>{t("typing")}</Text>
          </View>
        ) : null
      }
      keyboardShouldPersistTaps="handled"
    />
  );

  const sidebarPositionStyle = isRTL
    ? { right: 0, borderLeftWidth: 1, borderLeftColor: colors.borderColor, borderRightWidth: 0 }
    : { left: 0, borderRightWidth: 1, borderRightColor: colors.borderColor };

  const renderSidebar = () => (
    <Animated.View style={[styles.sidebar, sidebarPositionStyle, { paddingBottom: insets.bottom, transform: [{ translateX: sidebarTranslate }] }]}>
      <View style={styles.sidebarHeader}>
        <View style={styles.sidebarLogoWrap}>
          <Image
            source={require("../../assets/misa.png")}
            style={styles.sidebarLogo}
            resizeMode="contain"
          />
        </View>
        <Text style={styles.sidebarBrand}>{t("misaChat")}</Text>
        <TouchableOpacity style={styles.sidebarCloseBtn} onPress={() => { setSidebarOpen(false); setProfileOpen(false); }}>
          <Text style={styles.sidebarCloseText}>✕</Text>
        </TouchableOpacity>
      </View>
        <TouchableOpacity style={styles.newChatBtn} onPress={() => { chatStore.newChat(); setSidebarOpen(false); setProfileOpen(false); }}>
        <Text style={styles.newChatBtnText}>+ {t("newChat")}</Text>
      </TouchableOpacity>
      <ScrollView style={styles.chatList} showsVerticalScrollIndicator={false}>
        {(() => {
          const groups = chatStore.getChatsGroupedByPeriod();
          const intlLocale = getIntlLocale(locale);
          const sections = [
            { key: "pinned", label: t("pinned"), chats: groups.pinned },
            { key: "today", label: t("today"), chats: groups.today },
            { key: "yesterday", label: t("yesterday"), chats: groups.yesterday },
            { key: "last7Days", label: t("last7Days"), chats: groups.last7Days },
            ...(groups.olderByMonth || []).map(({ key, year, month, chats }) => {
              const label = formatMonthYear(intlLocale, year, month);
              return { key: `older-${key}`, label: label.charAt(0).toUpperCase() + label.slice(1), chats };
            }),
          ];
          return sections
            .filter((s) => s.chats?.length > 0)
            .map((section) => (
              <View key={section.key} style={styles.chatGroup}>
                <Text style={styles.chatGroupTitle}>{section.label}</Text>
                {section.chats.map((c) => (
          <View key={c.id} style={styles.chatItemWrap}>
            <TouchableOpacity
              style={[styles.chatItem, c.id === chatStore.currentChatId && styles.chatItemActive]}
              onPress={() => { chatStore.switchChat(c.id); setSidebarOpen(false); setProfileOpen(false); setChatMenuOpen(null); }}
            >
              <Text style={styles.chatItemIcon}>💬</Text>
              <Text numberOfLines={1} style={styles.chatItemTitle}>
                {chatStore.getChatTitle(c) === "Новый чат" ? t("newChat") : chatStore.getChatTitle(c)}
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.chatItemMenuBtn}
              onPress={() => handleChatMenuToggle(c.id)}
            >
              <Text style={styles.chatItemMenuBtnText}>⋯</Text>
            </TouchableOpacity>
            {chatMenuOpen === c.id && (
              <View style={styles.chatMenu}>
                <TouchableOpacity style={styles.chatMenuItem} onPress={() => handleRename(c)}>
                  <Text style={styles.chatMenuItemIcon}>✎</Text>
                  <Text style={styles.chatMenuItemText}>{t("rename")}</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.chatMenuItem} onPress={() => handlePin(c.id)}>
                  <Text style={styles.chatMenuItemIcon}>📌</Text>
                  <Text style={styles.chatMenuItemText}>
                    {chatStore.isChatPinned(c.id) ? t("unpin") : t("pin")}
                  </Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.chatMenuItem} onPress={() => handleShareFromMenu(c.id)}>
                  <Text style={styles.chatMenuItemIcon}>⎘</Text>
                  <Text style={styles.chatMenuItemText}>{t("share")}</Text>
                </TouchableOpacity>
                <TouchableOpacity style={[styles.chatMenuItem, styles.chatMenuItemDelete]} onPress={() => handleDelete(c.id)}>
                  <Text style={styles.chatMenuItemIcon}>🗑</Text>
                  <Text style={[styles.chatMenuItemText, styles.chatMenuItemDeleteText]}>{t("delete")}</Text>
                </TouchableOpacity>
              </View>
            )}
          </View>
                ))}
              </View>
            ));
        })()}
      </ScrollView>
      <View style={styles.sidebarFooter}>
        {profileOpen && (
          <View style={styles.profilePanel}>
            <TouchableOpacity
              style={styles.profileItem}
              onPress={() => { setProfileOpen(false); setSidebarOpen(false); setSettingsOpen(true); }}
            >
              <Text style={styles.profileItemIcon}>⚙</Text>
              <Text style={styles.profileItemText}>{t("settings")}</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.profileItem}
              onPress={() => { setProfileOpen(false); Alert.alert(t("help"), "Обратная связь: напишите нам на support@misa.ai"); }}
            >
              <Text style={styles.profileItemIcon}>?</Text>
              <Text style={styles.profileItemText}>{t("helpFeedback")}</Text>
            </TouchableOpacity>
            <TouchableOpacity style={[styles.profileItem, styles.profileItemLogout]} onPress={handleLogout}>
              <Text style={styles.profileItemIcon}>→</Text>
              <Text style={styles.profileItemText}>{t("logout")}</Text>
            </TouchableOpacity>
          </View>
        )}
        <TouchableOpacity style={styles.profileBtn} onPress={() => setProfileOpen(!profileOpen)}>
          {user?.picture ? (
            <Image source={{ uri: user.picture }} style={styles.profileAvatarImg} />
          ) : (
            <View style={styles.profileAvatar}>
              <Text style={styles.profileAvatarText}>
                {(user?.display_name || user?.email || t("user"))[0].toUpperCase()}
              </Text>
            </View>
          )}
          <Text style={styles.profileName} numberOfLines={1}>
            {user?.display_name || user?.email || t("user")}
          </Text>
          <Text style={styles.profileDots}>⋯</Text>
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
        { backgroundColor: colors.primaryBg, borderTopColor: colors.borderColor, paddingBottom: inputPaddingBottom },
        isSmallScreen && styles.inputRowSmall,
      ]}
    >
      <TextInput
        style={[styles.input, isSmallScreen && styles.inputSmall]}
        placeholder={t("placeholder")}
        placeholderTextColor={colors.textSecondary}
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
        <TouchableOpacity style={StyleSheet.absoluteFill} onPress={() => { setSidebarOpen(false); setProfileOpen(false); }} activeOpacity={1} />
      </Animated.View>

      {renderSidebar()}

      <View style={[styles.main, { paddingTop: insets.top }]}>
        <View style={[styles.header, { backgroundColor: colors.primaryBg, borderBottomColor: colors.borderColor }, isRTL && styles.headerRTL]}>
          <TouchableOpacity onPress={() => setSidebarOpen(true)} style={styles.menuBtn}>
            <Text style={styles.menuBtnText}>☰</Text>
          </TouchableOpacity>
          <Text style={[styles.headerTitle, isSmallScreen && styles.headerTitleSmall]} numberOfLines={1}>
            {chatStore.currentChat?.title && chatStore.currentChat.title.trim() && chatStore.currentChat.title !== "Новый чат"
              ? chatStore.currentChat.title
              : chatStore.currentChat
                ? t("newChat")
                : "Misa AI"}
          </Text>
          <TouchableOpacity onPress={() => chatStore.newChat()} style={styles.newChatBtnHeader}>
            <Text style={styles.newChatBtnHeaderText}>+</Text>
          </TouchableOpacity>
        </View>

        {chatStore.error ? (
          <View style={styles.errorBar}>
            <Text style={styles.errorText}>{chatStore.error}</Text>
            <TouchableOpacity onPress={() => chatStore.connect()}>
              <Text style={styles.retryText}>{t("reconnect")}</Text>
            </TouchableOpacity>
          </View>
        ) : null}

        <KeyboardAvoidingView
          style={[styles.container, { backgroundColor: colors.primaryBg }]}
          behavior={Platform.OS === "ios" ? "padding" : "padding"}
          keyboardVerticalOffset={Platform.OS === "ios" ? 0 : 20}
        >
          <View style={styles.contentArea}>
            {isEmpty ? renderEmptyChat() : renderMessagesList()}
          </View>
          {inputBlock}
        </KeyboardAvoidingView>
      </View>
      <SettingsModal isOpen={settingsOpen} onClose={() => setSettingsOpen(false)} />

      <Modal visible={!!renameModalChatId} transparent animationType="fade">
        <Pressable style={styles.feedbackOverlay} onPress={() => { setRenameModalChatId(null); setRenameInputValue(""); }}>
          <Pressable style={styles.renameModal} onPress={() => {}}>
            <Text style={styles.feedbackTitle}>{t("renameChat")}</Text>
            <TextInput
              style={styles.renameInput}
              value={renameInputValue}
              onChangeText={setRenameInputValue}
              placeholder={t("chatName")}
              placeholderTextColor={colors.textSecondary}
              autoFocus
            />
            <View style={styles.feedbackActions}>
              <TouchableOpacity style={styles.feedbackBtnCancel} onPress={() => { setRenameModalChatId(null); setRenameInputValue(""); }}>
                <Text style={styles.feedbackBtnCancelText}>{t("cancel")}</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.feedbackBtnSubmit} onPress={handleRenameSubmit}>
                <Text style={styles.feedbackBtnSubmitText}>{t("save")}</Text>
              </TouchableOpacity>
            </View>
          </Pressable>
        </Pressable>
      </Modal>

      <Modal
        visible={!!feedbackModalMsgId}
        transparent
        animationType="fade"
        onRequestClose={handleFeedbackCancel}
      >
        <Pressable style={styles.feedbackOverlay} onPress={handleFeedbackCancel}>
          <Pressable style={styles.feedbackModal} onPress={() => {}}>
            <Text style={styles.feedbackTitle}>{t("feedback")}</Text>
            <View style={styles.feedbackCategories}>
              {FEEDBACK_CATEGORIES.map(({ id, label }) => (
                <TouchableOpacity
                  key={id}
                  style={[
                    styles.feedbackPill,
                    feedbackCategories.includes(id) && styles.feedbackPillActive,
                  ]}
                  onPress={() => toggleFeedbackCategory(id)}
                >
                  <Text
                    style={[
                      styles.feedbackPillText,
                      feedbackCategories.includes(id) && styles.feedbackPillTextActive,
                    ]}
                  >
                    {label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
            <TextInput
              style={styles.feedbackTextarea}
              placeholder={t("feedbackPlaceholder")}
              placeholderTextColor={colors.textSecondary}
              value={feedbackComment}
              onChangeText={setFeedbackComment}
              multiline
              numberOfLines={4}
            />
            <View style={styles.feedbackActions}>
              <TouchableOpacity style={styles.feedbackBtnCancel} onPress={handleFeedbackCancel}>
                <Text style={styles.feedbackBtnCancelText}>{t("cancel")}</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.feedbackBtnSubmit} onPress={handleFeedbackSubmit}>
                <Text style={styles.feedbackBtnSubmitText}>{t("submit")}</Text>
              </TouchableOpacity>
            </View>
          </Pressable>
        </Pressable>
      </Modal>
    </View>
  );
}

const createStyles = (colors) =>
  StyleSheet.create({
  wrapper: { flex: 1, overflow: "visible" },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(0,0,0,0.5)",
    zIndex: 100,
  },
  sidebar: {
    position: "absolute",
    top: 0,
    bottom: 0,
    width: SIDEBAR_WIDTH,
    backgroundColor: colors.sidebarBg,
    zIndex: 101,
    flexDirection: "column",
  },
  sidebarHeader: {
    flexDirection: "row",
    alignItems: "center",
    padding: 16,
    gap: 12,
  },
  sidebarLogoWrap: {
    width: 28,
    height: 42,
    overflow: "hidden",
  },
  sidebarLogo: {
    width: 28,
    height: 42,
  },
  sidebarBrand: {
    flex: 1,
    fontSize: 18,
    fontWeight: "600",
    color: colors.textPrimary,
  },
  sidebarCloseBtn: {
    padding: 8,
  },
  sidebarCloseText: {
    color: colors.textPrimary,
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
    color: colors.textPrimary,
    fontSize: 16,
  },
  chatList: {
    flex: 1,
    minHeight: 0,
    paddingHorizontal: 12,
  },
  chatGroup: {
    marginBottom: 16,
  },
  chatGroupTitle: {
    fontSize: 12,
    color: colors.textSecondary,
    marginBottom: 8,
    paddingHorizontal: 4,
  },
  chatItemWrap: {
    position: "relative",
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 4,
  },
  chatItem: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    borderRadius: 8,
  },
  chatItemActive: {
    backgroundColor: colors.messageBg,
  },
  chatItemIcon: {
    fontSize: 16,
    marginRight: 8,
  },
  chatItemTitle: {
    flex: 1,
    color: colors.textPrimary,
    fontSize: 14,
  },
  chatItemMenuBtn: {
    padding: 8,
    marginLeft: 4,
  },
  chatItemMenuBtnText: {
    color: colors.textSecondary,
    fontSize: 18,
  },
  chatMenu: {
    position: "absolute",
    top: "100%",
    right: 0,
    marginTop: 4,
    backgroundColor: colors.secondaryBg,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.borderColor,
    minWidth: 180,
    zIndex: 10,
    overflow: "hidden",
  },
  chatMenuItem: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 12,
    paddingHorizontal: 14,
  },
  chatMenuItemIcon: {
    fontSize: 16,
    marginRight: 10,
    color: colors.textSecondary,
  },
  chatMenuItemText: {
    color: colors.textPrimary,
    fontSize: 15,
  },
  chatMenuItemDelete: {
    borderTopWidth: 1,
    borderTopColor: colors.borderColor,
  },
  chatMenuItemDeleteText: {
    color: "#ef4444",
  },
  renameModal: {
    backgroundColor: colors.secondaryBg,
    borderRadius: 16,
    padding: 20,
    width: "100%",
    maxWidth: 360,
    borderWidth: 1,
    borderColor: colors.borderColor,
  },
  renameInput: {
    borderWidth: 1,
    borderColor: colors.borderColor,
    borderRadius: 12,
    padding: 12,
    fontSize: 16,
    color: colors.textPrimary,
    backgroundColor: colors.primaryBg,
    marginBottom: 16,
  },
  sidebarFooter: {
    position: "relative",
    padding: 16,
    paddingBottom: 16,
    borderTopWidth: 1,
    borderTopColor: colors.borderColor,
    flexShrink: 0,
  },
  profileBtn: {
    flexDirection: "row",
    alignItems: "center",
  },
  profileAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: colors.accentColor,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 10,
  },
  profileAvatarText: {
    color: colors.textPrimary,
    fontSize: 16,
    fontWeight: "600",
  },
  profileAvatarImg: {
    width: 36,
    height: 36,
    borderRadius: 18,
    marginRight: 10,
  },
  profileName: {
    flex: 1,
    color: colors.textPrimary,
    fontSize: 14,
  },
  profileDots: {
    color: colors.textSecondary,
    fontSize: 18,
    marginLeft: 4,
  },
  profilePanel: {
    position: "absolute",
    bottom: 56,
    left: 16,
    right: 16,
    backgroundColor: colors.secondaryBg,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.borderColor,
    overflow: "hidden",
  },
  profileItem: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 12,
    paddingHorizontal: 14,
  },
  profileItemIcon: {
    fontSize: 16,
    marginRight: 10,
    color: colors.textSecondary,
  },
  profileItemText: {
    color: colors.textPrimary,
    fontSize: 15,
  },
  profileItemLogout: {
    borderTopWidth: 1,
    borderTopColor: colors.borderColor,
  },
  main: { flex: 1 },
  header: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  headerRTL: { flexDirection: "row-reverse" },
  menuBtn: { padding: 8, marginRight: 8 },
  menuBtnText: { fontSize: 22, color: colors.textPrimary },
  headerTitle: { flex: 1, fontSize: 18, fontWeight: "600", color: colors.textPrimary },
  headerTitleSmall: { fontSize: 16 },
  newChatBtnHeader: { padding: 8 },
  newChatBtnHeaderText: { fontSize: 24, fontWeight: "300", color: colors.textPrimary },
  errorBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "rgba(239,68,68,0.15)",
    padding: 10,
  },
  errorText: { color: "#ef4444", flex: 1 },
  retryText: { color: colors.accentColor, fontWeight: "600" },
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
  bubbleUser: { backgroundColor: colors.userMessageBg },
  bubbleMisa: {
    backgroundColor: colors.messageBg,
    borderWidth: 1,
    borderColor: colors.borderColor,
  },
  msgContentWrap: { gap: 8 },
  msgText: { fontSize: 16, color: colors.textPrimary },
  msgTextUser: { color: "#fff" },
  codeBlock: {
    backgroundColor: "#0d1117",
    borderWidth: 2,
    borderColor: colors.accentColor,
    borderRadius: 8,
    marginTop: 12,
    marginBottom: 4,
    overflow: "hidden",
  },
  codeBlockUser: {
    backgroundColor: "rgba(0,0,0,0.4)",
    borderColor: "rgba(255,255,255,0.25)",
  },
  codeBlockHeaderWrap: {
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: "rgba(74,144,226,0.15)",
    borderBottomWidth: 1,
    borderBottomColor: "rgba(74,144,226,0.3)",
  },
  codeBlockHeader: {
    fontSize: 12,
    color: colors.textSecondary,
    fontFamily: Platform.OS === "ios" ? "Menlo" : "monospace",
  },
  codeBlockHeaderWrapUser: {
    backgroundColor: "rgba(255,255,255,0.1)",
    borderBottomColor: "rgba(255,255,255,0.15)",
  },
  codeBlockHeader_code: {},
  codeBlockHeader_json: { backgroundColor: "rgba(167,139,250,0.15)", borderBottomColor: "rgba(167,139,250,0.3)" },
  codeBlockHeader_yaml: { backgroundColor: "rgba(52,211,153,0.15)", borderBottomColor: "rgba(52,211,153,0.3)" },
  codeBlockHeader_xml: { backgroundColor: "rgba(245,158,11,0.15)", borderBottomColor: "rgba(245,158,11,0.3)" },
  codeBlockHeader_bash: { backgroundColor: "rgba(249,115,22,0.15)", borderBottomColor: "rgba(249,115,22,0.3)" },
  codeBlockHeader_sql: { backgroundColor: "rgba(34,197,94,0.15)", borderBottomColor: "rgba(34,197,94,0.3)" },
  codeBlockHeader_md: { backgroundColor: "rgba(59,130,246,0.15)", borderBottomColor: "rgba(59,130,246,0.3)" },
  codeBlockHeader_diff: { backgroundColor: "rgba(107,114,128,0.2)", borderBottomColor: "rgba(107,114,128,0.3)" },
  codeBlockHeader_warning: { backgroundColor: "rgba(245,158,11,0.2)", borderBottomColor: "rgba(245,158,11,0.4)" },
  codeBlockHeader_error: { backgroundColor: "rgba(239,68,68,0.2)", borderBottomColor: "rgba(239,68,68,0.4)" },
  codeBlockHeader_quote: { backgroundColor: "rgba(148,163,184,0.1)", borderBottomColor: "rgba(148,163,184,0.2)" },
  codeBlockHeader_output: { backgroundColor: "rgba(100,116,139,0.15)", borderBottomColor: "rgba(100,116,139,0.25)" },
  codeBlock_code: {},
  codeBlock_json: { borderColor: "#a78bfa" },
  codeBlock_yaml: { borderColor: "#34d399" },
  codeBlock_xml: { borderColor: "#f59e0b" },
  codeBlock_bash: { borderColor: "#f97316" },
  codeBlock_sql: { borderColor: "#22c55e" },
  codeBlock_md: { borderColor: "#3b82f6" },
  codeBlock_diff: { borderColor: "#6b7280" },
  codeBlock_warning: { borderColor: "#f59e0b" },
  codeBlock_error: { borderColor: "#ef4444" },
  codeBlock_quote: { borderColor: "#94a3b8", borderLeftWidth: 4 },
  codeBlock_output: { borderColor: "#64748b" },
  codeBlockText: {
    fontFamily: Platform.OS === "ios" ? "Menlo" : "monospace",
    fontSize: 13,
    lineHeight: 22,
    color: "#e6edf3",
    paddingHorizontal: 12,
    paddingVertical: 12,
  },
  codeBlockTextUser: { color: "rgba(255,255,255,0.95)" },
  msgTime: {
    fontSize: 11,
    color: colors.textSecondary,
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
    color: colors.textSecondary,
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
  emptyHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 16,
    maxWidth: 340,
  },
  emptyHeaderSmall: {
    gap: 12,
  },
  emptyLogoWrap: {
    width: 80,
    height: 120,
    overflow: "hidden",
  },
  emptyLogoWrapSmall: {
    width: 64,
    height: 96,
  },
  emptyLogo: {
    width: 80,
    height: 120,
  },
  emptyLogoSmall: {
    width: 64,
    height: 96,
  },
  emptyTextBlock: {
    flex: 1,
    minWidth: 0,
  },
  emptyTitle: {
    fontSize: 22,
    fontWeight: "600",
    color: colors.textPrimary,
    marginBottom: 6,
  },
  emptyTitleSmall: {
    fontSize: 18,
    marginBottom: 4,
  },
  emptyHint: {
    fontSize: 15,
    color: colors.textSecondary,
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
    borderColor: colors.borderColor,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 12,
    maxHeight: 120,
    fontSize: 16,
    backgroundColor: colors.secondaryBg,
    color: colors.textPrimary,
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
    backgroundColor: colors.accentColor,
    justifyContent: "center",
    alignItems: "center",
  },
  sendBtnDisabled: { backgroundColor: colors.borderColor, opacity: 0.5 },
  sendBtnText: { color: "#fff", fontSize: 18, fontWeight: "bold" },
  typing: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    gap: 8,
  },
  typingText: { color: colors.textSecondary, fontSize: 14 },
  feedbackOverlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.5)",
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  feedbackModal: {
    backgroundColor: colors.secondaryBg,
    borderRadius: 16,
    padding: 20,
    width: "100%",
    maxWidth: 360,
    borderWidth: 1,
    borderColor: colors.borderColor,
  },
  feedbackTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: colors.textPrimary,
    marginBottom: 16,
  },
  feedbackCategories: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
    marginBottom: 16,
  },
  feedbackPill: {
    paddingVertical: 8,
    paddingHorizontal: 14,
    borderRadius: 20,
    backgroundColor: "rgba(255,255,255,0.08)",
    borderWidth: 1,
    borderColor: colors.borderColor,
  },
  feedbackPillActive: {
    backgroundColor: "rgba(74,144,226,0.25)",
    borderColor: colors.accentColor,
  },
  feedbackPillText: {
    fontSize: 14,
    color: colors.textSecondary,
  },
  feedbackPillTextActive: {
    color: colors.accentColor,
  },
  feedbackTextarea: {
    borderWidth: 1,
    borderColor: colors.borderColor,
    borderRadius: 12,
    padding: 12,
    fontSize: 15,
    color: colors.textPrimary,
    backgroundColor: colors.primaryBg,
    minHeight: 100,
    textAlignVertical: "top",
    marginBottom: 16,
  },
  feedbackActions: {
    flexDirection: "row",
    justifyContent: "flex-end",
    gap: 12,
  },
  feedbackBtnCancel: {
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 10,
  },
  feedbackBtnCancelText: {
    color: colors.textSecondary,
    fontSize: 16,
  },
  feedbackBtnSubmit: {
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 10,
    backgroundColor: colors.accentColor,
  },
  feedbackBtnSubmitText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
  });

export default observer(ChatScreen);
