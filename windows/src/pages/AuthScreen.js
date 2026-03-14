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
import {
  login,
  sendRegistrationCode,
  verifyRegistrationCode,
  sendForgotPasswordCode,
  verifyForgotPasswordCode,
} from "../api/userApi";
import { useUser } from "../context/UserContext";
import { useStores } from "../store/rootStoreContext";
import { useLocale } from "../context/LocaleContext";

export default function AuthScreen() {
  const { setUser, setIsAuth } = useUser();
  const { chatStore } = useStores();
  const { t } = useLocale();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [step, setStep] = useState("login");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);

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
    if (step === "login") return t("authSignIn");
    if (step === "register") return t("authRegistration");
    if (step === "verify") return t("authVerifyCode");
    if (step === "forgot") return t("authForgotPassword");
    if (step === "forgot_verify") return t("authEnterCode");
    return t("authSignIn");
  };

  const renderForgotScreen = () => (
    <>
      <Text style={styles.subtitle}>{t("authForgotSubtitle")}</Text>
      <TextInput
        style={styles.input}
        placeholder={t("authPlaceholderEmail")}
        value={email}
        onChangeText={(val) => { setEmail(val); setError(""); }}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      <View style={styles.rowBetween}>
        <TouchableOpacity onPress={goBackFromForgot}>
          <Text style={styles.linkText}>{t("authBackToSignIn")}</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.btnOutline, styles.btnSuccess]}
          onPress={handleForgotRequest}
          disabled={loading || !email.trim()}
        >
          <Text style={styles.btnOutlineText}>{loading ? t("authSending") : t("authSendCode")}</Text>
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
        <Text style={styles.subtitle}>{t("authCodeSentTo")} {email} </Text>
        <TouchableOpacity onPress={handleResendForgotCode} disabled={resendLoading}>
          <Text style={styles.linkText}>{resendLoading ? t("authSending") : t("authResendCode")}</Text>
        </TouchableOpacity>
      </View>
      <TextInput
        style={styles.input}
        placeholder={t("authEnter6DigitCode")}
        value={code}
        onChangeText={(val) => { setCode(val.replace(/\D/g, "").slice(0, 6)); setError(""); }}
        keyboardType="number-pad"
        maxLength={6}
      />
      <TextInput
        style={styles.input}
        placeholder={t("authNewPasswordPlaceholder")}
        value={newPassword}
        onChangeText={(val) => { setNewPassword(val); setError(""); }}
        secureTextEntry
      />
      <View style={styles.rowBetween}>
        <TouchableOpacity onPress={() => { setStep("forgot"); setError(""); }}>
          <Text style={styles.linkText}>{t("authBack")}</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.btnOutline, styles.btnSuccess]}
          onPress={handleForgotVerify}
          disabled={code.length !== 6 || newPassword.length < 6 || loading}
        >
          <Text style={styles.btnOutlineText}>{loading ? t("authSaving") : t("authResetPassword")}</Text>
        </TouchableOpacity>
      </View>
    </>
  );

  const renderMainForm = () => (
    <>
      <TextInput
        style={styles.input}
        placeholder={t("authPlaceholderEmail")}
        value={email}
        onChangeText={(val) => { setEmail(val); setError(""); }}
        autoCapitalize="none"
        keyboardType="email-address"
        editable={step !== "verify"}
      />
      <TextInput
        style={styles.input}
        placeholder={t("authPlaceholderPassword")}
        value={password}
        onChangeText={(val) => { setPassword(val); setError(""); }}
        secureTextEntry
        editable={step !== "verify"}
      />
      {step === "verify" && (
        <TextInput
          style={styles.input}
          placeholder={t("authCodeFromEmail")}
          value={code}
          onChangeText={(val) => { setCode(val); setError(""); }}
          keyboardType="number-pad"
        />
      )}
      {step === "login" && (
        <View style={styles.forgotRow}>
          <TouchableOpacity onPress={goToForgot}>
            <Text style={styles.linkText}>{t("authForgotPasswordLink")}</Text>
          </TouchableOpacity>
        </View>
      )}
      <View style={styles.rowBetween}>
        <TouchableOpacity onPress={goBack}>
          <Text style={styles.linkText}>
            {step === "login" ? `${t("authNoAccount")} ${t("authRegistration")}` : `${t("authAlreadyHaveAccount")} ${t("authSignInButton")}`}
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
            {loading ? "…" : step === "login" ? t("authSignInButton") : step === "register" ? t("authRegisterButton") : step === "verify" ? t("authConfirmButton") : t("authSignInButton")}
          </Text>
        </TouchableOpacity>
      </View>
    </>
  );

  const isForgotFlow = step === "forgot" || step === "forgot_verify";

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
