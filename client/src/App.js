import React  from 'react';
import { BrowserRouter } from "react-router-dom";
import { Spinner, Container } from "react-bootstrap";

import { useContext, useEffect, useState } from 'react';
import { observer } from "mobx-react-lite";
import { Context } from "./index.js";
import { check } from "./http/userApi.js";
import AppRouter from "./components/AppRouter";
import { useStores } from "./store/rootStoreContext";

const App = observer(() => {
    const { user } = useContext(Context);
    const { chatStore } = useStores();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const userData = await check();
                console.log(userData);
                if (userData) {
                    user.setUser(userData);
                    user.setIsAuth(true);
                    localStorage.setItem('currentUser', userData.email);
                    localStorage.setItem('currentUserId', userData.id);
                    chatStore.connect();
                } else {
                    user.setIsAuth(false);
                    user.setUser({});
                }
            } catch (error) {
                console.log("Auth check error:", error.message);
                user.setIsAuth(false);
                user.setUser({});
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, [user]);

    if (loading) {
        return (
            <Container className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
                <Spinner animation="border" variant="primary" />
            </Container>
        );
    }

    return (
        <BrowserRouter>
            <AppRouter />
        </BrowserRouter>
    );
});

export default App;