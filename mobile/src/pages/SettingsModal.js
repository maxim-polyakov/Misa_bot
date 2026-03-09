import React, { useState, useEffect, useMemo } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Modal,
  ScrollView,
  StyleSheet,
  Alert,
  FlatList,
  Platform,
} from "react-native";
import { observer } from "mobx-react-lite";
import JSZip from "jszip";
import * as FileSystem from "expo-file-system/legacy";
import * as Sharing from "expo-sharing";
import { useStores } from "../store/rootStoreContext";
import { useUser } from "../context/UserContext";
import { API_URL } from "../config";
import { apiFetch } from "../api/http";
import { logoutAll } from "../api/userApi";
import { THEMES } from "../utils/theme";
import { LANGUAGES } from "../utils/locale";
import { useTheme } from "../context/ThemeContext";
import { useLocale } from "../context/LocaleContext";

const maskEmail = (e) => {
  if (!e || !e.includes("@")) return "-";
  const [local, domain] = e.split("@");
  if (local.length <= 2) return e;
  return local.slice(0, 2) + "*".repeat(Math.min(local.length - 2, 5)) + local.slice(-2) + "@" + domain;
};

const getSettingsTabs = (t) => [
  { id: "general", label: t("general"), icon: "⚙" },
  { id: "profile", label: t("profile"), icon: "👤" },
  { id: "data", label: t("data"), icon: "📊" },
  { id: "about", label: t("about"), icon: "ℹ" },
];

const SettingsModal = observer(({ isOpen, onClose }) => {
  const { chatStore } = useStores();
  const { user, setIsAuth } = useUser();
  const { colors, theme, setTheme: setThemeFromContext } = useTheme();
  const { t, locale, setLanguage: setLocale } = useLocale();
  const [activeTab, setActiveTab] = useState("general");
  const [langDropdownOpen, setLangDropdownOpen] = useState(false);
  const styles = useMemo(() => createStyles(colors), [colors]);
  const SETTINGS_TABS = useMemo(() => getSettingsTabs(t), [t]);

  const displayName = user?.display_name;
  const email = user?.email || chatStore?.user || "";
  const picture = user?.picture;
  const isGoogleUser = !!picture;

  useEffect(() => {
    if (!isOpen) setLangDropdownOpen(false);
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
      t("deleteAccount"),
      t("deleteAccountConfirm"),
      [
        { text: t("cancel"), style: "cancel" },
        { text: t("delete"), style: "destructive", onPress: () => handleLogout() },
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
      const dir = FileSystem.documentDirectory || FileSystem.cacheDirectory;
      if (!dir) {
        throw new Error("Storage access denied");
      }
      const path = dir + `misa_data-${dateStr}.zip`;
      await FileSystem.writeAsStringAsync(path, blob, { encoding: FileSystem.EncodingType.Base64 });
      const canShare = await Sharing.isAvailableAsync();
      if (canShare) {
        // ExpoSharing.shareAsync требует file:// URI, content:// не поддерживается
        await Sharing.shareAsync(path, {
          mimeType: "application/zip",
          dialogTitle: "Misa " + t("exportData"),
        });
      } else {
        Alert.alert(t("exportData"), t("fileSaved") + ": " + path);
      }
    } catch (e) {
      console.error("Export error:", e);
      Alert.alert(t("error"), e?.message || t("exportFailed"));
    }
  };

  const handleDeleteAllChats = () => {
    Alert.alert(
      t("deleteAllChats"),
      t("confirmDeleteAllChats"),
      [
        { text: t("cancel"), style: "cancel" },
        {
          text: t("deleteAllButton"),
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
            <Text style={styles.title}>{t("settings")}</Text>
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
                    <Text style={styles.label}>{t("name")}</Text>
                    <View style={styles.valueRow}>
                      <Text style={styles.value}>{displayName}</Text>
                      <View style={styles.googleBadge}>
                        <Text style={styles.googleBadgeText}>G</Text>
                      </View>
                    </View>
                  </View>
                )}
                <View style={styles.row}>
                  <Text style={styles.label}>{t("email")}</Text>
                  <Text style={styles.value}>{maskEmail(email) || "-"}</Text>
                </View>
                <View style={styles.row}>
                  <Text style={styles.label}>{t("phone")}</Text>
                  <Text style={styles.value}>-</Text>
                </View>
                <View style={[styles.row, styles.rowActions]}>
                  <Text style={styles.label}>{t("logoutAll")}</Text>
                  <TouchableOpacity style={styles.btnLogout} onPress={() => handleLogout(true)}>
                    <Text style={styles.btnLogoutText}>{t("logout")}</Text>
                  </TouchableOpacity>
                </View>
                <View style={[styles.row, styles.rowActions]}>
                  <Text style={styles.label}>{t("deleteAccount")}</Text>
                  <TouchableOpacity style={styles.btnDelete} onPress={handleDeleteAccount}>
                    <Text style={styles.btnDeleteText}>{t("delete")}</Text>
                  </TouchableOpacity>
                </View>
              </View>
            )}
            {activeTab === "general" && (
              <View style={styles.section}>
                <View style={styles.themeBlock}>
                  <Text style={styles.themeLabel}>{t("theme")}</Text>
                  <View style={styles.themeOptions}>
                    {[THEMES.LIGHT, THEMES.DARK, THEMES.SYSTEM].map((t) => (
                      <TouchableOpacity
                        key={t}
                        style={[
                          styles.themeBtn,
                          theme === t && styles.themeBtnActive,
                          { borderColor: theme === t ? colors.accentColor : colors.borderColor, backgroundColor: theme === t ? "rgba(74,144,226,0.25)" : "rgba(128,128,128,0.1)" },
                        ]}
                        onPress={async () => {
                          await setThemeFromContext(t);
                        }}
                      >
                        <Text style={styles.themeIcon}>
                          {t === THEMES.LIGHT ? "☀" : t === THEMES.DARK ? "🌙" : "💻"}
                        </Text>
                        <Text style={styles.themeBtnText}>
                          {t === THEMES.LIGHT ? t("themeLight") : t === THEMES.DARK ? t("themeDark") : t("themeSystem")}
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </View>
                </View>
                <View style={styles.langBlock}>
                  <Text style={styles.themeLabel}>{t("language")}</Text>
                  <TouchableOpacity
                    style={styles.pickerWrap}
                    onPress={() => setLangDropdownOpen(true)}
                    activeOpacity={0.7}
                  >
                    <Text style={styles.pickerText}>{LANGUAGES.find((l) => l.code === locale)?.label || "Русский"}</Text>
                    <Text style={styles.pickerChevron}>▼</Text>
                  </TouchableOpacity>
                  <Modal visible={langDropdownOpen} transparent animationType="fade">
                    <TouchableOpacity
                      style={styles.langDropdownOverlay}
                      activeOpacity={1}
                      onPress={() => setLangDropdownOpen(false)}
                    >
                      <View style={styles.langDropdown} onStartShouldSetResponder={() => true}>
                        <FlatList
                          data={LANGUAGES}
                          keyExtractor={(item) => item.code}
                          renderItem={({ item }) => (
                            <TouchableOpacity
                              style={[styles.langDropdownItem, locale === item.code && styles.langDropdownItemActive]}
                              onPress={async () => {
                                await setLocale(item.code);
                                setLangDropdownOpen(false);
                              }}
                            >
                              <Text style={styles.langDropdownItemText}>{item.label}</Text>
                            </TouchableOpacity>
                          )}
                        />
                      </View>
                    </TouchableOpacity>
                  </Modal>
                </View>
              </View>
            )}
            {activeTab === "data" && (
              <View style={styles.section}>
                <View style={styles.dataBlock}>
                  <Text style={styles.dataTitle}>{t("exportData")}</Text>
                  <Text style={styles.dataDesc}>{t("exportDataDesc")}</Text>
                  <TouchableOpacity style={styles.btnExport} onPress={handleExport}>
                    <Text style={styles.btnExportText}>{t("exportButton")}</Text>
                  </TouchableOpacity>
                </View>
                <View style={styles.dataBlock}>
                  <Text style={styles.dataTitle}>{t("deleteAllChats")}</Text>
                  <Text style={styles.dataDesc}>{t("deleteAllChatsDesc")}</Text>
                  <TouchableOpacity style={styles.btnDeleteAll} onPress={handleDeleteAllChats}>
                    <Text style={styles.btnDeleteAllText}>{t("deleteAllButton")}</Text>
                  </TouchableOpacity>
                </View>
              </View>
            )}
            {activeTab === "about" && (
              <View style={styles.placeholder}>
                <Text style={styles.placeholderText}>{t("misaChat")}</Text>
              </View>
            )}
            </ScrollView>
          </View>
        </View>
      </View>
    </Modal>
  );
});

const createStyles = (colors) =>
  StyleSheet.create({
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
      backgroundColor: colors.secondaryBg,
      borderRadius: 12,
      borderWidth: 1,
      borderColor: colors.borderColor,
      overflow: "hidden",
    },
    header: {
      flexDirection: "row",
      alignItems: "center",
      justifyContent: "space-between",
      padding: 16,
      borderBottomWidth: 1,
      borderBottomColor: colors.borderColor,
    },
    title: { fontSize: 20, fontWeight: "600", color: colors.textPrimary },
    closeBtn: { padding: 8 },
    closeText: { fontSize: 24, color: colors.textPrimary },
    body: { flex: 1, flexDirection: "row", minHeight: 0 },
    nav: {
      width: 140,
      paddingVertical: 12,
      paddingHorizontal: 0,
      borderRightWidth: 1,
      borderRightColor: colors.borderColor,
      gap: 2,
    },
    navItem: { flexDirection: "row", alignItems: "center", paddingVertical: 10, paddingHorizontal: 16, gap: 8 },
    navItemActive: { backgroundColor: "rgba(74,144,226,0.15)" },
    navIcon: { fontSize: 16 },
    navLabel: { fontSize: 14, color: colors.textSecondary },
    navLabelActive: { color: colors.accentColor },
    content: { flex: 1, padding: 20, minWidth: 0 },
    section: { marginBottom: 24 },
    row: { marginBottom: 16 },
    rowActions: { marginTop: 8 },
    label: { fontSize: 13, color: colors.textSecondary, marginBottom: 4 },
    value: { fontSize: 15, color: colors.textPrimary },
    valueRow: { flexDirection: "row", alignItems: "center", gap: 8 },
    googleBadge: { backgroundColor: "#4285F4", paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4 },
    googleBadgeText: { color: "#fff", fontSize: 12, fontWeight: "600" },
    btnLogout: {
      alignSelf: "flex-start",
      paddingVertical: 8,
      paddingHorizontal: 16,
      backgroundColor: "rgba(74,144,226,0.3)",
      borderRadius: 8,
    },
    btnLogoutText: { color: colors.accentColor, fontWeight: "500" },
    btnDelete: {
      alignSelf: "flex-start",
      paddingVertical: 8,
      paddingHorizontal: 16,
      backgroundColor: "rgba(239,68,68,0.2)",
      borderRadius: 8,
    },
    btnDeleteText: { color: "#ef4444", fontWeight: "500" },
    themeBlock: { marginBottom: 20 },
    themeLabel: { fontSize: 14, color: colors.textSecondary, marginBottom: 10 },
    themeOptions: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
    themeBtn: {
      flexDirection: "row",
      alignItems: "center",
      paddingVertical: 10,
      paddingHorizontal: 14,
      borderRadius: 8,
      borderWidth: 1,
    },
    themeBtnActive: {},
    themeIcon: { fontSize: 18, marginRight: 8 },
    themeBtnText: { fontSize: 14, color: colors.textPrimary },
    langBlock: { marginBottom: 16 },
    pickerWrap: {
      flexDirection: "row",
      alignItems: "center",
      justifyContent: "space-between",
      paddingVertical: 12,
      paddingHorizontal: 14,
      borderRadius: 8,
      borderWidth: 1,
      borderColor: colors.borderColor,
      backgroundColor: "rgba(128,128,128,0.1)",
    },
    pickerText: { fontSize: 15, color: colors.textPrimary },
    pickerChevron: { fontSize: 12, color: colors.textSecondary },
    langDropdownOverlay: {
      flex: 1,
      backgroundColor: "rgba(0,0,0,0.5)",
      justifyContent: "center",
      alignItems: "center",
      padding: 24,
    },
    langDropdown: {
      width: "100%",
      maxWidth: 280,
      maxHeight: 300,
      backgroundColor: colors.secondaryBg,
      borderRadius: 12,
      borderWidth: 1,
      borderColor: colors.borderColor,
      overflow: "hidden",
    },
    langDropdownItem: {
      paddingVertical: 14,
      paddingHorizontal: 16,
      borderBottomWidth: 1,
      borderBottomColor: colors.borderColor,
    },
    langDropdownItemActive: { backgroundColor: "rgba(74,144,226,0.15)" },
    langDropdownItemText: { fontSize: 16, color: colors.textPrimary },
    dataBlock: {
      marginBottom: 24,
      padding: 16,
      backgroundColor: "rgba(128,128,128,0.06)",
      borderRadius: 8,
      borderWidth: 1,
      borderColor: colors.borderColor,
    },
    dataTitle: { fontSize: 16, fontWeight: "600", color: colors.textPrimary, marginBottom: 6 },
    dataDesc: { fontSize: 13, color: colors.textSecondary, marginBottom: 12 },
    btnExport: {
      alignSelf: "flex-start",
      paddingVertical: 10,
      paddingHorizontal: 16,
      backgroundColor: colors.accentColor,
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
    placeholder: { padding: 24, alignItems: "center" },
    placeholderText: { fontSize: 18, color: colors.textSecondary },
  });

export default SettingsModal;
