import React, { useEffect, useState } from "react";
import { StatusBar } from "expo-status-bar";
import { ActivityIndicator, View, StyleSheet, Platform } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { observer } from "mobx-react-lite";
import { jwtDecode } from "jwt-decode";
import Constants from "expo-constants";
import { GoogleSignin } from "@react-native-google-signin/google-signin";
import { UserProvider, useUser } from "./src/context/UserContext";
import { ThemeProvider, useTheme } from "./src/context/ThemeContext";
import { LocaleProvider } from "./src/context/LocaleContext";
import { RootStoreProvider, useStores } from "./src/store/rootStoreContext";
import { check } from "./src/api/userApi";
import { storage } from "./src/storage";
import AuthScreen from "./src/pages/AuthScreen";
import ChatScreen from "./src/pages/ChatScreen";

const AppContent = observer(() => {
  const { setUser, isAuth, setIsAuth } = useUser();
  const { chatStore } = useStores();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    try {
      const webClientId = Constants.expoConfig?.extra?.googleWebClientId;
      const iosClientId = Constants.expoConfig?.extra?.googleIosClientId;
      if (webClientId || iosClientId) {
        GoogleSignin.configure({
          webClientId: webClientId || undefined,
          iosClientId: Platform.OS === "ios" ? iosClientId || undefined : undefined,
        });
      }
    } catch (e) {
      console.warn("Google Sign-In init:", e?.message);
    }
  }, []);

  useEffect(() => {
    const init = async () => {
      try {
        let userData = await check();
        const token = await storage.getItem("token");
        const storedProfile = JSON.parse((await storage.getItem("userProfile")) || "{}");

        if (!userData && token) {
          try {
            const decoded = jwtDecode(token);
            if (decoded.exp && decoded.exp * 1000 > Date.now()) {
              const dn = decoded.display_name ?? storedProfile.display_name ?? decoded.email?.split("@")[0];
              userData = { ...decoded, display_name: dn, picture: decoded.picture };
            }
          } catch {}
        }

        if (userData) {
          setUser(userData);
          setIsAuth(true);
          chatStore.setUser(userData.email, userData.user_id ?? userData.id);
          chatStore.connect();
        } else {
          setIsAuth(false);
          setUser({});
          chatStore.logout();
        }
      } catch (err) {
        console.log("Auth init error:", err);
        setIsAuth(false);
        chatStore.logout();
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color="#0a7ea4" />
      </View>
    );
  }

  return isAuth ? <ChatScreen /> : <AuthScreen />;
});

const AppWithTheme = () => {
  const { isDark } = useTheme();
  return (
    <>
      <AppContent />
      <StatusBar style={isDark ? "light" : "dark"} />
    </>
  );
};

export default function App() {
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <LocaleProvider>
          <UserProvider>
            <RootStoreProvider>
              <AppWithTheme />
            </RootStoreProvider>
          </UserProvider>
        </LocaleProvider>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  loading: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f5f5f5",
  },
});
