import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { login, sendRegistrationCode, verifyRegistrationCode } from "../api/userApi";
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
          <TouchableOpacity style={styles.btn} onPress={signIn}>
            <Text style={styles.btnText}>
              {step === "login" ? "Войти" : step === "register" ? "Отправить код" : "Подтвердить"}
            </Text>
          </TouchableOpacity>
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
