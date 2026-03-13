import React from "react";
import { BrowserRouter } from "react-router-dom";
import { Spinner, Container } from "react-bootstrap";
import { useContext, useEffect, useState } from "react";
import { observer } from "mobx-react-lite";
import { jwtDecode } from "jwt-decode";
import { Context } from "./index.js";
import { check } from "./http/userApi.js";
import AppRouter from "./components/AppRouter";
import { useStores } from "./store/rootStoreContext";
import { LocaleProvider } from "./contexts/LocaleContext";

const App = observer(() => {
    const { user } = useContext(Context);
    const { chatStore } = useStores();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                let userData = await check();
                const stored = JSON.parse(localStorage.getItem("userProfile") || "{}");
                const token = localStorage.getItem("token");

                if (!userData && token) {
                    try {
                        const decoded = jwtDecode(token);
                        if (decoded.exp && decoded.exp * 1000 > Date.now()) {
                            const dn = decoded.display_name ?? stored.display_name ?? decoded.email?.split("@")[0];
                            const pic = decoded.picture ?? stored.picture;
                            userData = { ...decoded, display_name: dn, picture: pic };
                            if (dn || pic) {
                                localStorage.setItem("userProfile", JSON.stringify({ display_name: dn, picture: pic }));
                            }
                        }
                    } catch {
                        /* token invalid */
                    }
                }

                if (userData) {
                    const merged = {
                        ...userData,
                        display_name: userData.display_name ?? stored.display_name ?? userData.email?.split("@")[0],
                        picture: userData.picture ?? stored.picture,
                    };
                    user.setUser(merged);
                    user.setIsAuth(true);
                    chatStore.setUser(merged.email, merged.user_id ?? merged.id);
                    chatStore.connect();
                } else {
                    localStorage.setItem("userIsAuth", "false");
                    user.setIsAuth(false);
                    user.setUser({});
                    chatStore.logout();
                }
            } catch (error) {
                console.log("Auth check error:", error.message);
                localStorage.setItem("userIsAuth", "false");
                user.setIsAuth(false);
                user.setUser({});
                chatStore.logout();
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, [user, chatStore]);

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