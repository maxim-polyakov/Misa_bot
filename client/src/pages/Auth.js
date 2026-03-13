import { useContext, useState, useEffect, useRef } from "react";
import { Button, Card, Container, Form, Alert } from "react-bootstrap";
import { Link, useLocation, useNavigate, useSearchParams } from "react-router-dom";
import { CHAT_ROUTE, LOGIN_ROUTE, REGISTRATION_ROUTE, REGISTRATION_VERIFY_ROUTE, FORGOT_PASSWORD_ROUTE } from "../utils/consts.js";
import { login, sendRegistrationCode, exchangeOAuthCode } from "../http/userApi.js";
import { observer } from "mobx-react-lite";
import { Context } from "../index.js";
import { useStores } from "../store/rootStoreContext";
import { useLocale } from "../contexts/LocaleContext";

const API_URL = process.env.REACT_APP_API_URL || "";

const Auth = observer(() => {
    const { user } = useContext(Context);
    const { chatStore } = useStores();
    const { t } = useLocale();
    const location = useLocation();
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();
    const oauthHandled = useRef(false);
    const isLogin = location.pathname === LOGIN_ROUTE && true;

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        const oauthError = searchParams.get("oauth_error");
        const oauthDetail = searchParams.get("oauth_detail");
        if (oauthError) {
            const messages = {
                OAUTH_MISSING_DATA: "Не удалось получить данные от Google.",
                OAUTH_AUTH_ERROR: "Ошибка входа через Google.",
            };
            let msg = messages[oauthError] || "Ошибка входа через Google.";
            if (oauthDetail) {
                try {
                    msg += " Подробности: " + decodeURIComponent(oauthDetail);
                } catch {
                    msg += " " + oauthDetail;
                }
            } else {
                msg += " Попробуйте позже.";
            }
            setError(msg);
            setSearchParams({}, { replace: true });
            return;
        }

        const code = searchParams.get("code");
        if (!code || searchParams.get("oauth") !== "google" || oauthHandled.current) return;

        oauthHandled.current = true;
        setError("");
        exchangeOAuthCode(code)
            .then((data) => {
                chatStore.setIsAuth(true);
                chatStore.setUser(data.email, data.user_id ?? data.id);
                user.setUser(data);
                user.setIsAuth(true);
                chatStore.connect();
                swapMethod();
                navigate(CHAT_ROUTE);
            })
            .catch((err) => {
                oauthHandled.current = false;
                setError(err.message || "Ошибка входа через Google");
                setSearchParams({}, { replace: true });
            });
    }, [searchParams, navigate, setSearchParams, user, chatStore]);

    const swapMethod = () => {
        setEmail("");
        setPassword("");
        setError(""); // Очищаем ошибки при смене формы
    };

    const signIn = async () => {
        // Проверка на пустые поля
        if (!email.trim() || !password.trim()) {
            setError("Все поля должны быть заполнены");
            return;
        }

        // Проверка валидности email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            setError("Введите корректный email адрес");
            return;
        }

        // Проверка длины пароля
        if (password.length < 6) {
            setError("Пароль должен содержать минимум 6 символов");
            return;
        }

        try {
            setError(""); // Очищаем ошибки перед запросом

            if (isLogin) {
                try {
                    const data = await login(email, password);
                    chatStore.setIsAuth(true);
                    chatStore.setUser(data.email, data.user_id ?? data.id);
                    user.setUser(data);
                    user.setIsAuth(true);
                    chatStore.connect();
                    setEmail("");
                    setPassword("");
                    navigate(CHAT_ROUTE);
                } catch (err) {
                    if (err.message === "email_not_verified") {
                        navigate(REGISTRATION_VERIFY_ROUTE, { state: { email, password } });
                        return;
                    }
                    throw err;
                }
            } else {
                await sendRegistrationCode(email, password);
                navigate(REGISTRATION_VERIFY_ROUTE, { state: { email, password } });
            }

        } catch (error) {
            console.log("Ошибка авторизации:", error);
            // Просто используем message из ошибки, так как мы уже обработали её в API функциях
            setError(error.message);
        }
    };

    return (
        <Container
            className="d-flex justify-content-center align-items-center"
            style={{ height: window.innerHeight - 54 }}
        >
            <Card style={{ width: 700 }} className="p-5">
                <h2 className="m-auto text-center">
                    {isLogin ? t("authSignIn") : t("authRegistration")}
                </h2>

                {/* Отображение ошибок */}
                {error && (
                    <Alert variant="danger" className="mt-3">
                        {error}
                    </Alert>
                )}

                <Form className="d-flex flex-column">
                    <Form.Control
                        className="mt-3"
                        placeholder={t("authPlaceholderEmail")}
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value);
                            setError(""); // Очищаем ошибку при изменении поля
                        }}
                        required
                    />
                    <Form.Control
                        className="mt-2"
                        placeholder={t("authPlaceholderPassword")}
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value);
                            setError(""); // Очищаем ошибку при изменении поля
                        }}
                        type="password"
                        required
                    />
                    {API_URL && (
                        <div className="mt-3 d-flex justify-content-center">
                            <a
                                href={`${API_URL}/auth/oauth/google/`}
                                className="btn btn-outline-secondary btn-lg"
                                style={{ textDecoration: "none" }}
                            >
                                {t("authSignInWithGoogle")}
                            </a>
                        </div>
                    )}
                    {isLogin && (
                        <div className="mt-2 text-end">
                            <Link to={FORGOT_PASSWORD_ROUTE} style={{ textDecoration: "none", fontSize: "0.9rem" }}>
                                {t("authForgotPasswordLink")}
                            </Link>
                        </div>
                    )}
                    <div className="d-flex justify-content-between mt-3 pl-3 pr-3 align-items-center">
                        <div>
                            {isLogin ? (
                                <>
                                    {t("authNoAccount")}{" "}
                                    <Link
                                        to={REGISTRATION_ROUTE}
                                        style={{ textDecoration: "none" }}
                                        onClick={() => swapMethod()}
                                    >
                                        {t("authRegistration")}
                                    </Link>
                                </>
                            ) : (
                                <>
                                    {t("authAlreadyHaveAccount")}{" "}
                                    <Link
                                        to={LOGIN_ROUTE}
                                        style={{ textDecoration: "none" }}
                                        onClick={() => swapMethod()}
                                    >
                                        {t("authSignInButton")}
                                    </Link>
                                </>
                            )}
                        </div>
                        <Button
                            variant="outline-success"
                            onClick={signIn}
                            disabled={!email.trim() || !password.trim()} // Кнопка неактивна при пустых полях
                        >
                            {isLogin ? t("authSignInButton") : t("authRegisterButton")}
                        </Button>
                    </div>
                </Form>
            </Card>
        </Container>
    );
});

export default Auth;