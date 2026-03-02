import { useState, useContext } from "react";
import { Button, Card, Container, Form, Alert } from "react-bootstrap";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { verifyRegistrationCode, sendRegistrationCode } from "../http/userApi.js";
import { observer } from "mobx-react-lite";
import { Context } from "../index.js";
import { useStores } from "../store/rootStoreContext";
import { CHAT_ROUTE, REGISTRATION_ROUTE } from "../utils/consts.js";

const VerifyCode = observer(() => {
    const { user } = useContext(Context);
    const { chatStore } = useStores();
    const navigate = useNavigate();
    const location = useLocation();
    const { email, password } = location.state || {};

    const [code, setCode] = useState("");
    const [error, setError] = useState("");
    const [resendLoading, setResendLoading] = useState(false);

    const handleVerify = async () => {
        if (!email || !password) {
            setError("Сессия истекла. Начните регистрацию заново.");
            return;
        }
        if (!code.trim()) {
            setError("Введите код из письма");
            return;
        }
        try {
            setError("");
            const data = await verifyRegistrationCode(email, password, code.trim());
            chatStore.setIsAuth(true);
            chatStore.setUser(data.email, data.user_id);
            user.setUser(data);
            user.setIsAuth(true);
            chatStore.connect();
            navigate(CHAT_ROUTE);
        } catch (err) {
            setError(err.message || "Неверный или истёкший код");
        }
    };

    const handleResend = async () => {
        try {
            setResendLoading(true);
            setError("");
            await sendRegistrationCode(email, password);
            setError("");
        } catch (err) {
            setError(err.message || "Не удалось отправить код");
        } finally {
            setResendLoading(false);
        }
    };

    if (!email || !password) {
        return (
            <Container className="d-flex justify-content-center align-items-center" style={{ height: window.innerHeight - 54 }}>
                <Card style={{ width: 500 }} className="p-4">
                    <Alert variant="warning">Сессия истекла. Пожалуйста, начните регистрацию заново.</Alert>
                    <Link to={REGISTRATION_ROUTE}>Вернуться к регистрации</Link>
                </Card>
            </Container>
        );
    }

    return (
        <Container className="d-flex justify-content-center align-items-center" style={{ height: window.innerHeight - 54 }}>
            <Card style={{ width: 500 }} className="p-5">
                <h2 className="m-auto text-center">Подтверждение email</h2>
                <p className="text-muted text-center mt-2">
                    Код отправлен на <strong>{email}</strong>
                    <Button variant="link" size="sm" onClick={handleResend} disabled={resendLoading} className="p-0 ms-2">
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
                    <div className="d-flex justify-content-between mt-4 align-items-center">
                        <Link to={REGISTRATION_ROUTE} state={{ email, password }}>Назад</Link>
                        <Button
                            variant="outline-success"
                            onClick={handleVerify}
                            disabled={code.length !== 6}
                        >
                            Подтвердить
                        </Button>
                    </div>
                </Form>
            </Card>
        </Container>
    );
});

export default VerifyCode;
