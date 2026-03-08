import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Modal,
  ScrollView,
  StyleSheet,
  Alert,
  Platform,
} from "react-native";
import { Picker } from "@react-native-picker/picker";
import { observer } from "mobx-react-lite";
import JSZip from "jszip";
import * as FileSystem from "expo-file-system";
import * as Sharing from "expo-sharing";
import { useStores } from "../store/rootStoreContext";
import { useUser } from "../context/UserContext";
import { API_URL } from "../config";
import { apiFetch } from "../api/http";
import { logoutAll } from "../api/userApi";
import { getTheme, setTheme, THEMES } from "../utils/theme";
import { getLanguage, setLanguage, LANGUAGES } from "../utils/locale";

const COLORS = {
  primaryBg: "#1c1c1e",
  secondaryBg: "#2c2c2e",
  borderColor: "#3a3a3c",
  textPrimary: "#ffffff",
  textSecondary: "#8e8e93",
  accentColor: "#4a90e2",
};

const maskEmail = (e) => {
  if (!e || !e.includes("@")) return "-";
  const [local, domain] = e.split("@");
  if (local.length <= 2) return e;
  return local.slice(0, 2) + "*".repeat(Math.min(local.length - 2, 5)) + local.slice(-2) + "@" + domain;
};

const SETTINGS_TABS = [
  { id: "general", label: "Общие", icon: "⚙" },
  { id: "profile", label: "Профиль", icon: "👤" },
  { id: "data", label: "Данные", icon: "📊" },
  { id: "about", label: "О приложении", icon: "ℹ" },
];

const SettingsModal = observer(({ isOpen, onClose }) => {
  const { chatStore } = useStores();
  const { user, setIsAuth } = useUser();
  const [activeTab, setActiveTab] = useState("profile");
  const [theme, setThemeState] = useState(THEMES.DARK);
  const [locale, setLocaleState] = useState("ru");

  const displayName = user?.display_name;
  const email = user?.email || chatStore?.user || "";
  const picture = user?.picture;
  const isGoogleUser = !!picture;

  useEffect(() => {
    if (isOpen) {
      getTheme().then(setThemeState);
      getLanguage().then(setLocaleState);
    }
  }, [isOpen]);

  const handleLogout = async (fromAllDevices = false) => {
    onClose();
    if (fromAllDevices) {
      await logoutAll();
    }
    chatStore.clearUserFromStorage();
    setIsAuth(false);
  };

  const handleDeleteAccount = () => {
    Alert.alert(
      "Удалить аккаунт",
      "Вы уверены, что хотите удалить аккаунт? Это действие необратимо.",
      [
        { text: "Отмена", style: "cancel" },
        { text: "Удалить", style: "destructive", onPress: () => handleLogout() },
      ]
    );
  };

  const handleExport = async () => {
    try {
      const dateStr = new Date().toISOString().slice(0, 10);
      let conversationsData = chatStore.getConversationsExportData();
      let userData = {
        exportedAt: new Date().toISOString(),
        display_name: displayName || null,
        email: email || null,
        picture: picture || null,
      };
      if (API_URL) {
        try {
          const data = await apiFetch("/api/chats/export/");
          if (data?.conversations) {
            conversationsData = {
              exportedAt: new Date().toISOString(),
              conversations: data.conversations || [],
            };
            userData = {
              exportedAt: new Date().toISOString(),
              display_name: data.user?.display_name ?? displayName ?? null,
              email: data.user?.email ?? email ?? null,
              picture: data.user?.picture ?? picture ?? null,
            };
          }
        } catch (e) {
          console.warn("Ошибка экспорта с бэкенда, fallback на локальные данные:", e);
        }
      }
      const zip = new JSZip();
      zip.file("conversations.json", JSON.stringify(conversationsData, null, 2));
      zip.file("user.json", JSON.stringify(userData, null, 2));
      const blob = await zip.generateAsync({ type: "base64" });
      const path = FileSystem.cacheDirectory + `misa_data-${dateStr}.zip`;
      await FileSystem.writeAsStringAsync(path, blob, { encoding: FileSystem.EncodingType.Base64 });
      const canShare = await Sharing.isAvailableAsync();
      if (canShare) {
        await Sharing.shareAsync(path, { mimeType: "application/zip" });
      } else {
        Alert.alert("Экспорт", "Файл сохранён: " + path);
      }
    } catch (e) {
      console.error("Export error:", e);
      Alert.alert("Ошибка", "Не удалось экспортировать данные");
    }
  };

  const handleDeleteAllChats = () => {
    Alert.alert(
      "Удалить все чаты",
      "Вы уверены, что хотите удалить все чаты? Это действие необратимо.",
      [
        { text: "Отмена", style: "cancel" },
        {
          text: "Удалить всё",
          style: "destructive",
          onPress: async () => {
            await chatStore.deleteAllChats();
            onClose();
          },
        },
      ]
    );
  };

  if (!isOpen) return null;

  return (
    <Modal visible={isOpen} transparent animationType="fade">
      <View style={styles.overlay}>
        <TouchableOpacity style={StyleSheet.absoluteFill} activeOpacity={1} onPress={onClose} />
        <View style={styles.modal} onStartShouldSetResponder={() => true}>
          <View style={styles.header}>
            <Text style={styles.title}>Настройки</Text>
            <TouchableOpacity onPress={onClose} style={styles.closeBtn}>
              <Text style={styles.closeText}>×</Text>
            </TouchableOpacity>
          </View>
          <View style={styles.body}>
            <View style={styles.nav}>
              {SETTINGS_TABS.map((tab) => (
                <TouchableOpacity
                  key={tab.id}
                  style={[styles.navItem, activeTab === tab.id && styles.navItemActive]}
                  onPress={() => setActiveTab(tab.id)}
                >
                  <Text style={styles.navIcon}>{tab.icon}</Text>
                  <Text style={[styles.navLabel, activeTab === tab.id && styles.navLabelActive]}>{tab.label}</Text>
                </TouchableOpacity>
              ))}
            </View>
            <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
            {activeTab === "profile" && (
              <View style={styles.section}>
                {isGoogleUser && displayName && (
                  <View style={styles.row}>
                    <Text style={styles.label}>Имя</Text>
                    <View style={styles.valueRow}>
                      <Text style={styles.value}>{displayName}</Text>
                      <View style={styles.googleBadge}>
                        <Text style={styles.googleBadgeText}>G</Text>
                      </View>
                    </View>
                  </View>
                )}
                <View style={styles.row}>
                  <Text style={styles.label}>Email</Text>
                  <Text style={styles.value}>{maskEmail(email) || "-"}</Text>
                </View>
                <View style={styles.row}>
                  <Text style={styles.label}>Телефон</Text>
                  <Text style={styles.value}>-</Text>
                </View>
                <View style={[styles.row, styles.rowActions]}>
                  <Text style={styles.label}>Выйти со всех устройств</Text>
                  <TouchableOpacity style={styles.btnLogout} onPress={() => handleLogout(true)}>
                    <Text style={styles.btnLogoutText}>Выйти</Text>
                  </TouchableOpacity>
                </View>
                <View style={[styles.row, styles.rowActions]}>
                  <Text style={styles.label}>Удалить аккаунт</Text>
                  <TouchableOpacity style={styles.btnDelete} onPress={handleDeleteAccount}>
                    <Text style={styles.btnDeleteText}>Удалить</Text>
                  </TouchableOpacity>
                </View>
              </View>
            )}
            {activeTab === "general" && (
              <View style={styles.section}>
                <View style={styles.themeBlock}>
                  <Text style={styles.themeLabel}>Тема</Text>
                  <View style={styles.themeOptions}>
                    {[THEMES.LIGHT, THEMES.DARK, THEMES.SYSTEM].map((t) => (
                      <TouchableOpacity
                        key={t}
                        style={[styles.themeBtn, theme === t && styles.themeBtnActive]}
                        onPress={async () => {
                          await setTheme(t);
                          setThemeState(t);
                        }}
                      >
                        <Text style={styles.themeIcon}>
                          {t === THEMES.LIGHT ? "☀" : t === THEMES.DARK ? "🌙" : "💻"}
                        </Text>
                        <Text style={styles.themeBtnText}>
                          {t === THEMES.LIGHT ? "Светлая" : t === THEMES.DARK ? "Тёмная" : "Системная"}
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </View>
                </View>
                <View style={styles.langBlock}>
                  <Text style={styles.themeLabel}>Язык</Text>
                  <View style={styles.pickerWrap}>
                    <Picker
                      selectedValue={locale}
                      onValueChange={async (code) => {
                        await setLanguage(code);
                        setLocaleState(code);
                      }}
                      style={styles.picker}
                      dropdownIconColor={COLORS.textPrimary}
                      mode="dropdown"
                    >
                      {LANGUAGES.map((lang) => (
                        <Picker.Item key={lang.code} label={lang.label} value={lang.code} color={COLORS.textPrimary} />
                      ))}
                    </Picker>
                  </View>
                </View>
              </View>
            )}
            {activeTab === "data" && (
              <View style={styles.section}>
                <View style={styles.dataBlock}>
                  <Text style={styles.dataTitle}>Экспорт данных</Text>
                  <Text style={styles.dataDesc}>Скачайте все чаты в формате JSON.</Text>
                  <TouchableOpacity style={styles.btnExport} onPress={handleExport}>
                    <Text style={styles.btnExportText}>Экспортировать</Text>
                  </TouchableOpacity>
                </View>
                <View style={styles.dataBlock}>
                  <Text style={styles.dataTitle}>Удалить все чаты</Text>
                  <Text style={styles.dataDesc}>Безвозвратно удалить всю историю чатов.</Text>
                  <TouchableOpacity style={styles.btnDeleteAll} onPress={handleDeleteAllChats}>
                    <Text style={styles.btnDeleteAllText}>Удалить всё</Text>
                  </TouchableOpacity>
                </View>
              </View>
            )}
            {activeTab === "about" && (
              <View style={styles.placeholder}>
                <Text style={styles.placeholderText}>Misa AI Чат</Text>
              </View>
            )}
            </ScrollView>
          </View>
        </View>
      </View>
    </Modal>
  );
});

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.6)",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  modal: {
    width: "100%",
    maxWidth: 560,
    height: "85%",
    minHeight: 320,
    backgroundColor: COLORS.secondaryBg,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: COLORS.borderColor,
    overflow: "hidden",
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.borderColor,
  },
  title: {
    fontSize: 20,
    fontWeight: "600",
    color: COLORS.textPrimary,
  },
  closeBtn: { padding: 8 },
  closeText: { fontSize: 24, color: COLORS.textPrimary },
  body: {
    flex: 1,
    flexDirection: "row",
    minHeight: 0,
  },
  nav: {
    width: 140,
    paddingVertical: 12,
    paddingHorizontal: 0,
    borderRightWidth: 1,
    borderRightColor: COLORS.borderColor,
    gap: 2,
  },
  navItem: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    paddingHorizontal: 16,
    gap: 8,
  },
  navItemActive: {
    backgroundColor: "rgba(74,144,226,0.15)",
  },
  navIcon: { fontSize: 16 },
  navLabel: { fontSize: 14, color: COLORS.textSecondary },
  navLabelActive: { color: COLORS.accentColor },
  content: {
    flex: 1,
    padding: 20,
    minWidth: 0,
  },
  section: { marginBottom: 24 },
  row: {
    marginBottom: 16,
  },
  rowActions: { marginTop: 8 },
  label: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  value: { fontSize: 15, color: COLORS.textPrimary },
  valueRow: { flexDirection: "row", alignItems: "center", gap: 8 },
  googleBadge: {
    backgroundColor: "#4285F4",
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  googleBadgeText: { color: "#fff", fontSize: 12, fontWeight: "600" },
  btnLogout: {
    alignSelf: "flex-start",
    paddingVertical: 8,
    paddingHorizontal: 16,
    backgroundColor: "rgba(74,144,226,0.3)",
    borderRadius: 8,
  },
  btnLogoutText: { color: COLORS.accentColor, fontWeight: "500" },
  btnDelete: {
    alignSelf: "flex-start",
    paddingVertical: 8,
    paddingHorizontal: 16,
    backgroundColor: "rgba(239,68,68,0.2)",
    borderRadius: 8,
  },
  btnDeleteText: { color: "#ef4444", fontWeight: "500" },
  themeBlock: { marginBottom: 20 },
  themeLabel: { fontSize: 14, color: COLORS.textSecondary, marginBottom: 10 },
  themeOptions: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  themeBtn: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    paddingHorizontal: 14,
    borderRadius: 8,
    backgroundColor: "rgba(255,255,255,0.06)",
    borderWidth: 1,
    borderColor: COLORS.borderColor,
  },
  themeBtnActive: {
    backgroundColor: "rgba(74,144,226,0.25)",
    borderColor: COLORS.accentColor,
  },
  themeIcon: { fontSize: 18, marginRight: 8 },
  themeBtnText: { fontSize: 14, color: COLORS.textPrimary },
  langBlock: { marginBottom: 16 },
  pickerWrap: {
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.borderColor,
    backgroundColor: "rgba(255,255,255,0.06)",
    overflow: "hidden",
  },
  picker: {
    color: COLORS.textPrimary,
    height: Platform.OS === "android" ? 48 : 44,
  },
  dataBlock: {
    marginBottom: 24,
    padding: 16,
    backgroundColor: "rgba(255,255,255,0.04)",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.borderColor,
  },
  dataTitle: { fontSize: 16, fontWeight: "600", color: COLORS.textPrimary, marginBottom: 6 },
  dataDesc: { fontSize: 13, color: COLORS.textSecondary, marginBottom: 12 },
  btnExport: {
    alignSelf: "flex-start",
    paddingVertical: 10,
    paddingHorizontal: 16,
    backgroundColor: COLORS.accentColor,
    borderRadius: 8,
  },
  btnExportText: { color: "#fff", fontWeight: "600" },
  btnDeleteAll: {
    alignSelf: "flex-start",
    paddingVertical: 10,
    paddingHorizontal: 16,
    backgroundColor: "rgba(239,68,68,0.3)",
    borderRadius: 8,
  },
  btnDeleteAllText: { color: "#ef4444", fontWeight: "600" },
  placeholder: {
    padding: 24,
    alignItems: "center",
  },
  placeholderText: { fontSize: 18, color: COLORS.textSecondary },
});

export default SettingsModal;
