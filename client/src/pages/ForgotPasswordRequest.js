import { useState } from "react";
import { Button, Card, Container, Form, Alert } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { sendForgotPasswordCode } from "../http/userApi.js";
import { FORGOT_PASSWORD_VERIFY_ROUTE, LOGIN_ROUTE } from "../utils/consts.js";

const ForgotPasswordRequest = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!email.trim()) {
            setError("Введите email");
            return;
        }
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            setError("Введите корректный email");
            return;
        }
        try {
            setLoading(true);
            setError("");
            await sendForgotPasswordCode(email.trim());
            navigate(FORGOT_PASSWORD_VERIFY_ROUTE, { state: { email: email.trim() } });
        } catch (err) {
            setError(err.message || "Не удалось отправить код");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container
            className="d-flex justify-content-center align-items-center"
            style={{ height: window.innerHeight - 54 }}
        >
            <Card style={{ width: 500 }} className="p-5">
                <h2 className="m-auto text-center">Восстановление пароля</h2>
                <p className="text-muted text-center mt-2">
                    Введите email, на который зарегистрирован аккаунт. Мы отправим код для сброса пароля.
                </p>
                {error && <Alert variant="danger">{error}</Alert>}
                <Form onSubmit={handleSubmit}>
                    <Form.Control
                        className="mt-3"
                        placeholder="Введите email"
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value);
                            setError("");
                        }}
                        type="email"
                        required
                    />
                    <div className="d-flex justify-content-between mt-4 align-items-center">
                        <Link to={LOGIN_ROUTE}>Назад к входу</Link>
                        <Button
                            variant="outline-success"
                            type="submit"
                            disabled={loading || !email.trim()}
                        >
                            {loading ? "Отправка…" : "Отправить код"}
                        </Button>
                    </div>
                </Form>
            </Card>
        </Container>
    );
};

export default ForgotPasswordRequest;
