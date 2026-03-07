import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import Constants from "expo-constants";
import { GoogleSignin } from "@react-native-google-signin/google-signin";
import { login, sendRegistrationCode, verifyRegistrationCode, loginWithGoogleIdToken } from "../api/userApi";
import { useUser } from "../context/UserContext";
import { useStores } from "../store/rootStoreContext";

export default function AuthScreen() {
  const { user, setUser, setIsAuth } = useUser();
  const { chatStore } = useStores();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [step, setStep] = useState("login"); // login | register | verify
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const signInWithGoogle = async () => {
    const webClientId = Constants.expoConfig?.extra?.googleWebClientId;
    if (!webClientId) {
      setError("Google Sign-In не настроен (добавьте EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID в .env)");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await GoogleSignin.hasPlayServices();
      const response = await GoogleSignin.signIn();
      const idToken = response?.type === "success" ? response?.data?.idToken : null;
      if (!idToken) {
        setLoading(false);
        return;
      }
      const data = await loginWithGoogleIdToken(idToken);
      chatStore.setUser(data.email, data.user_id ?? data.id);
      setUser(data);
      setIsAuth(true);
      chatStore.connect();
    } catch (err) {
      setError(err.message || "Ошибка входа через Google");
    } finally {
      setLoading(false);
    }
  };

  const signIn = async () => {
    if (!email.trim() || !password.trim()) {
      setError("Заполните все поля");
      return;
    }
    if (password.length < 6) {
      setError("Пароль минимум 6 символов");
      return;
    }
    setLoading(true);
    setError("");
    try {
      if (step === "login") {
        const data = await login(email, password);
        chatStore.setUser(data.email, data.user_id ?? data.id);
        setUser(data);
        setIsAuth(true);
        chatStore.connect();
      } else if (step === "register") {
        await sendRegistrationCode(email, password);
        setStep("verify");
      } else if (step === "verify") {
        const data = await verifyRegistrationCode(email, password, code);
        chatStore.setUser(data.email, data.user_id ?? data.id);
        setUser(data);
        setIsAuth(true);
        chatStore.connect();
      }
    } catch (err) {
      setError(err.message || "Ошибка");
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={styles.card}>
        <Text style={styles.title}>
          {step === "login" ? "Вход" : step === "register" ? "Регистрация" : "Код подтверждения"}
        </Text>
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          editable={step !== "verify"}
        />
        <TextInput
          style={styles.input}
          placeholder="Пароль"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          editable={step !== "verify"}
        />
        {step === "verify" && (
          <TextInput
            style={styles.input}
            placeholder="Код из письма"
            value={code}
            onChangeText={setCode}
            keyboardType="number-pad"
          />
        )}
        {loading ? (
          <ActivityIndicator size="large" style={styles.loader} />
        ) : (
          <>
            <TouchableOpacity style={styles.btn} onPress={signIn}>
              <Text style={styles.btnText}>
                {step === "login" ? "Войти" : step === "register" ? "Отправить код" : "Подтвердить"}
              </Text>
            </TouchableOpacity>
            {step === "login" && (
              <TouchableOpacity
                style={styles.btnGoogle}
                onPress={signInWithGoogle}
              >
                <Text style={styles.btnGoogleText}>Войти через Google</Text>
              </TouchableOpacity>
            )}
          </>
        )}
        <TouchableOpacity
          style={styles.link}
          onPress={() => {
            setStep(step === "login" ? "register" : "login");
            setError("");
          }}
        >
          <Text style={styles.linkText}>
            {step === "login" ? "Нет аккаунта? Регистрация" : "Уже есть аккаунт? Войти"}
          </Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f5f5f5",
  },
  card: {
    width: "90%",
    maxWidth: 400,
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 24,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 20,
  },
  error: {
    color: "#c00",
    marginBottom: 12,
    textAlign: "center",
  },
  input: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
    fontSize: 16,
  },
  btn: {
    backgroundColor: "#0a7ea4",
    borderRadius: 8,
    padding: 14,
    alignItems: "center",
    marginTop: 8,
  },
  btnText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
  btnGoogle: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    padding: 14,
    alignItems: "center",
    marginTop: 12,
  },
  btnGoogleText: {
    color: "#333",
    fontSize: 16,
    fontWeight: "600",
  },
  loader: {
    marginVertical: 20,
  },
  link: {
    marginTop: 16,
    alignItems: "center",
  },
  linkText: {
    color: "#0a7ea4",
    fontSize: 14,
  },
});
