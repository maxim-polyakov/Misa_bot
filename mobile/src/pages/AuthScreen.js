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
  ScrollView,
} from "react-native";
import Constants from "expo-constants";
import { GoogleSignin } from "@react-native-google-signin/google-signin";
import {
  login,
  sendRegistrationCode,
  verifyRegistrationCode,
  loginWithGoogleIdToken,
  sendForgotPasswordCode,
  verifyForgotPasswordCode,
} from "../api/userApi";
import { useUser } from "../context/UserContext";
import { useStores } from "../store/rootStoreContext";

export default function AuthScreen() {
  const { setUser, setIsAuth } = useUser();
  const { chatStore } = useStores();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [step, setStep] = useState("login"); // login | register | verify | forgot | forgot_verify
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);

  const signInWithGoogle = async () => {
    const webClientId = Constants.expoConfig?.extra?.googleWebClientId;
    const iosClientId = Constants.expoConfig?.extra?.googleIosClientId;
    const hasConfig = Platform.OS === "ios" ? (webClientId || iosClientId) : webClientId;
    if (!hasConfig) {
      setError(
        Platform.OS === "ios"
          ? "Google Sign-In не настроен (добавьте EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID и EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID в .env)"
          : "Google Sign-In не настроен (добавьте EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID в .env)"
      );
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
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.trim() || !password.trim()) {
      setError("Все поля должны быть заполнены");
      return;
    }
    if (!emailRegex.test(email)) {
      setError("Введите корректный email адрес");
      return;
    }
    if (password.length < 6) {
      setError("Пароль должен содержать минимум 6 символов");
      return;
    }
    setLoading(true);
    setError("");
    try {
      if (step === "login") {
        try {
          const data = await login(email, password);
          chatStore.setUser(data.email, data.user_id ?? data.id);
          setUser(data);
          setIsAuth(true);
          chatStore.connect();
        } catch (err) {
          if (err.message === "email_not_verified") {
            setStep("verify");
            throw new Error("Подтвердите email. Код отправлен на почту.");
          }
          throw err;
        }
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

  const handleForgotRequest = async () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.trim()) {
      setError("Введите email");
      return;
    }
    if (!emailRegex.test(email)) {
      setError("Введите корректный email");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await sendForgotPasswordCode(email.trim());
      setStep("forgot_verify");
    } catch (err) {
      setError(err.message || "Не удалось отправить код");
    } finally {
      setLoading(false);
    }
  };

  const handleForgotVerify = async () => {
    if (!code.trim()) {
      setError("Введите код из письма");
      return;
    }
    if (!newPassword.trim()) {
      setError("Введите новый пароль");
      return;
    }
    if (newPassword.length < 6) {
      setError("Пароль должен содержать минимум 6 символов");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const data = await verifyForgotPasswordCode(email, code.trim(), newPassword);
      chatStore.setUser(data.email, data.user_id ?? data.id);
      setUser(data);
      setIsAuth(true);
      chatStore.connect();
    } catch (err) {
      setError(err.message || "Неверный или истёкший код");
    } finally {
      setLoading(false);
    }
  };

  const goBack = () => {
    setStep(step === "login" ? "register" : "login");
    setError("");
  };

  const goToForgot = () => {
    setStep("forgot");
    setError("");
  };

  const goBackFromForgot = () => {
    setStep("login");
    setError("");
  };

  const getTitle = () => {
    if (step === "login") return "Авторизация";
    if (step === "register") return "Регистрация";
    if (step === "verify") return "Код подтверждения";
    if (step === "forgot") return "Восстановление пароля";
    if (step === "forgot_verify") return "Введите код";
    return "Авторизация";
  };

  const renderForgotScreen = () => (
    <>
      <Text style={styles.subtitle}>
        Введите email, на который зарегистрирован аккаунт. Мы отправим код для сброса пароля.
      </Text>
      <TextInput
        style={styles.input}
        placeholder="Введите email"
        value={email}
        onChangeText={(t) => { setEmail(t); setError(""); }}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      <View style={styles.rowBetween}>
        <TouchableOpacity onPress={goBackFromForgot}>
          <Text style={styles.linkText}>Назад к входу</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.btnOutline, styles.btnSuccess]}
          onPress={handleForgotRequest}
          disabled={loading || !email.trim()}
        >
          <Text style={styles.btnOutlineText}>{loading ? "Отправка…" : "Отправить код"}</Text>
        </TouchableOpacity>
      </View>
    </>
  );

  const handleResendForgotCode = async () => {
    setResendLoading(true);
    setError("");
    try {
      await sendForgotPasswordCode(email);
    } catch (err) {
      setError(err.message || "Не удалось отправить код");
    } finally {
      setResendLoading(false);
    }
  };

  const renderForgotVerifyScreen = () => (
    <>
      <View style={styles.subtitleRow}>
        <Text style={styles.subtitle}>Код отправлен на {email} </Text>
        <TouchableOpacity onPress={handleResendForgotCode} disabled={resendLoading}>
          <Text style={styles.linkText}>{resendLoading ? "Отправка…" : "Отправить повторно"}</Text>
        </TouchableOpacity>
      </View>
      <TextInput
        style={styles.input}
        placeholder="Введите 6-значный код"
        value={code}
        onChangeText={(t) => { setCode(t.replace(/\D/g, "").slice(0, 6)); setError(""); }}
        keyboardType="number-pad"
        maxLength={6}
      />
      <TextInput
        style={styles.input}
        placeholder="Новый пароль (мин. 6 символов)"
        value={newPassword}
        onChangeText={(t) => { setNewPassword(t); setError(""); }}
        secureTextEntry
      />
      <View style={styles.rowBetween}>
        <TouchableOpacity onPress={() => { setStep("forgot"); setError(""); }}>
          <Text style={styles.linkText}>Назад</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.btnOutline, styles.btnSuccess]}
          onPress={handleForgotVerify}
          disabled={code.length !== 6 || newPassword.length < 6 || loading}
        >
          <Text style={styles.btnOutlineText}>{loading ? "Сохранение…" : "Сбросить пароль"}</Text>
        </TouchableOpacity>
      </View>
    </>
  );

  const renderMainForm = () => (
    <>
      <TextInput
        style={styles.input}
        placeholder="Введите email"
        value={email}
        onChangeText={(t) => { setEmail(t); setError(""); }}
        autoCapitalize="none"
        keyboardType="email-address"
        editable={step !== "verify"}
      />
      <TextInput
        style={styles.input}
        placeholder="Введите пароль"
        value={password}
        onChangeText={(t) => { setPassword(t); setError(""); }}
        secureTextEntry
        editable={step !== "verify"}
      />
      {step === "verify" && (
        <TextInput
          style={styles.input}
          placeholder="Код из письма"
          value={code}
          onChangeText={(t) => { setCode(t); setError(""); }}
          keyboardType="number-pad"
        />
      )}
      {step === "login" && (
        <TouchableOpacity style={styles.btnGoogle} onPress={signInWithGoogle}>
          <Text style={styles.btnGoogleText}>Войти через Google</Text>
        </TouchableOpacity>
      )}
      {step === "login" && (
        <View style={styles.forgotRow}>
          <TouchableOpacity onPress={goToForgot}>
            <Text style={styles.linkText}>Забыл пароль</Text>
          </TouchableOpacity>
        </View>
      )}
      <View style={styles.rowBetween}>
        <TouchableOpacity onPress={goBack}>
          <Text style={styles.linkText}>
            {step === "login" ? "Нет аккаунта? Регистрация" : "Уже есть аккаунт? Войти"}
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.btnOutline, styles.btnSuccess]}
          onPress={signIn}
          disabled={
            loading ||
            (step === "login" && (!email.trim() || !password.trim())) ||
            (step === "register" && (!email.trim() || !password.trim())) ||
            (step === "verify" && !code.trim())
          }
        >
          <Text style={styles.btnOutlineText}>
            {loading ? "…" : step === "login" ? "Войти" : step === "register" ? "Зарегистрироваться" : step === "verify" ? "Подтвердить" : "Войти"}
          </Text>
        </TouchableOpacity>
      </View>
    </>
  );

  const isForgotFlow = step === "forgot" || step === "forgot_verify";
  const showMainForm = step === "login" || step === "register" || step === "verify";

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.card}>
          <Text style={styles.title}>{getTitle()}</Text>
          {error ? <Text style={styles.error}>{error}</Text> : null}
          {loading && (step === "login" || step === "register" || step === "verify") ? (
            <ActivityIndicator size="large" style={styles.loader} />
          ) : isForgotFlow ? (
            step === "forgot" ? renderForgotScreen() : renderForgotVerifyScreen()
          ) : (
            renderMainForm()
          )}
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#2d2d2d",
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  card: {
    width: "100%",
    maxWidth: 500,
    backgroundColor: "#fff",
    borderRadius: 8,
    padding: 24,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 4,
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 16,
  },
  subtitle: {
    fontSize: 14,
    color: "#6c757d",
    marginBottom: 16,
  },
  subtitleRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    alignItems: "center",
    marginBottom: 16,
  },
  error: {
    color: "#dc3545",
    marginBottom: 12,
    textAlign: "center",
    fontSize: 14,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ced4da",
    borderRadius: 6,
    padding: 12,
    marginBottom: 12,
    fontSize: 16,
    backgroundColor: "#fff",
  },
  btnGoogle: {
    backgroundColor: "#fff",
    borderWidth: 1,
    borderColor: "#6c757d",
    borderRadius: 6,
    padding: 12,
    alignItems: "center",
    marginBottom: 12,
  },
  btnGoogleText: {
    color: "#495057",
    fontSize: 16,
  },
  forgotRow: {
    alignItems: "flex-end",
    marginBottom: 12,
  },
  rowBetween: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 16,
    flexWrap: "wrap",
    gap: 8,
  },
  btnOutline: {
    borderWidth: 1,
    borderRadius: 6,
    paddingVertical: 10,
    paddingHorizontal: 16,
  },
  btnSuccess: {
    borderColor: "#198754",
    backgroundColor: "#fff",
  },
  btnOutlineText: {
    color: "#198754",
    fontSize: 16,
  },
  linkText: {
    color: "#0d6efd",
    fontSize: 14,
  },
  loader: {
    marginVertical: 24,
  },
});
