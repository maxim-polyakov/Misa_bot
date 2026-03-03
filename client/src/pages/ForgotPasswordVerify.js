import { useState, useContext } from "react";
import { Button, Card, Container, Form, Alert } from "react-bootstrap";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { verifyForgotPasswordCode, sendForgotPasswordCode } from "../http/userApi.js";
import { useStores } from "../store/rootStoreContext";
import { Context } from "../index.js";
import { observer } from "mobx-react-lite";
import { CHAT_ROUTE, FORGOT_PASSWORD_ROUTE } from "../utils/consts.js";

const ForgotPasswordVerify = observer(() => {
    const { user } = useContext(Context);
    const { chatStore } = useStores();
    const navigate = useNavigate();
    const location = useLocation();
    const { email } = location.state || {};

    const [code, setCode] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [error, setError] = useState("");
    const [resendLoading, setResendLoading] = useState(false);
    const [submitLoading, setSubmitLoading] = useState(false);

    const handleVerify = async () => {
        if (!email) {
            setError("Сессия истекла. Начните заново.");
            return;
        }
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
        try {
            setSubmitLoading(true);
            setError("");
            const data = await verifyForgotPasswordCode(email, code.trim(), newPassword);
            chatStore.setIsAuth(true);
            chatStore.setUser(data.email, data.user_id ?? data.id);
            user.setUser(data);
            user.setIsAuth(true);
            chatStore.connect();
            navigate(CHAT_ROUTE);
        } catch (err) {
            setError(err.message || "Неверный или истёкший код");
        } finally {
            setSubmitLoading(false);
        }
    };

    const handleResend = async () => {
        try {
            setResendLoading(true);
            setError("");
            await sendForgotPasswordCode(email);
        } catch (err) {
            setError(err.message || "Не удалось отправить код");
        } finally {
            setResendLoading(false);
        }
    };

    if (!email) {
        return (
            <Container
                className="d-flex justify-content-center align-items-center"
                style={{ height: window.innerHeight - 54 }}
            >
                <Card style={{ width: 500 }} className="p-4">
                    <Alert variant="warning">Сессия истекла. Пожалуйста, начните заново.</Alert>
                    <Link to={FORGOT_PASSWORD_ROUTE}>Восстановить пароль</Link>
                </Card>
            </Container>
        );
    }

    return (
        <Container
            className="d-flex justify-content-center align-items-center"
            style={{ height: window.innerHeight - 54 }}
        >
            <Card style={{ width: 500 }} className="p-5">
                <h2 className="m-auto text-center">Введите код</h2>
                <p className="text-muted text-center mt-2">
                    Код отправлен на <strong>{email}</strong>
                    <Button
                        variant="link"
                        size="sm"
                        onClick={handleResend}
                        disabled={resendLoading}
                        className="p-0 ms-2"
                    >
                        {resendLoading ? "Отправка…" : "Отправить повторно"}
                    </Button>
                </p>
                {error && <Alert variant="danger">{error}</Alert>}
                <Form>
                    <Form.Control
                        className="mt-3"
                        placeholder="Введите 6-значный код"
                        value={code}
                        onChange={(e) => {
                            setCode(e.target.value.replace(/\D/g, "").slice(0, 6));
                            setError("");
                        }}
                        maxLength={6}
                    />
                    <Form.Control
                        className="mt-2"
                        placeholder="Новый пароль (мин. 6 символов)"
                        type="password"
                        value={newPassword}
                        onChange={(e) => {
                            setNewPassword(e.target.value);
                            setError("");
                        }}
                    />
                    <div className="d-flex justify-content-between mt-4 align-items-center">
                        <Link to={FORGOT_PASSWORD_ROUTE} state={{ email }}>Назад</Link>
                        <Button
                            variant="outline-success"
                            onClick={handleVerify}
                            disabled={code.length !== 6 || newPassword.length < 6 || submitLoading}
                        >
                            {submitLoading ? "Сохранение…" : "Сбросить пароль"}
                        </Button>
                    </div>
                </Form>
            </Card>
        </Container>
    );
});

export default ForgotPasswordVerify;
