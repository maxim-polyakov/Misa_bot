import { useContext } from "react";
import { Context } from "../index.js";
import Navbar from "react-bootstrap/Navbar";
import { Button, Nav } from "react-bootstrap";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom";
import "./Styles.css";
import { useStores } from "../store/rootStoreContext";

const Sidebar = observer(() => {
    const { user } = useContext(Context);
    const { chatStore } = useStores();
    const navigate = useNavigate();

    const logOut = () => {
        user?.setUser({});
        user?.setIsAuth(false);
        chatStore.logout();
        localStorage.removeItem("token");
        localStorage.removeItem("currentUser");
        localStorage.removeItem("currentUserId");
        navigate("/login", { replace: true });
    };

    if (!user?.isAuth) {
        return null;
    }

    return (
        <div className="sidebar-wrapper">
            <Navbar className="sidebar" bg="dark" data-bs-theme="dark">
                <div className="sidebar-content">

                    <div className="sidebar-footer">
                        <Button
                            variant="outline-light"
                            className="w-100"
                            onClick={logOut}
                        >
                            <i>🚪</i>
                            <span>Выйти</span>
                        </Button>
                    </div>
                </div>
            </Navbar>
        </div>
    );
});

export default Sidebar;