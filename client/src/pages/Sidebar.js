import { useContext } from "react";
import { Context } from "../index.js";
import Navbar from "react-bootstrap/Navbar";
import { Button } from "react-bootstrap";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom";
import "./Styles.css";
import { useStores } from "../store/rootStoreContext";
import { useMenuToggle } from "../pages/MainLayout";

const Sidebar = observer(() => {
    const { user } = useContext(Context);
    const { chatStore } = useStores();
    const { closeSidebar } = useMenuToggle();
    const navigate = useNavigate();

    const handleSwitchChat = (chatId) => {
        chatStore.switchChat(chatId);
        closeSidebar?.();
    };

    const logOut = async () => {
        chatStore.clearUserFromStorage();
        chatStore.logout();

        user?.setUser({});
        user?.setIsAuth(false);


        navigate("/login", { replace: true });
    };

    if (!user?.isAuth) {
        return null;
    }

    return (
        <div className="sidebar-wrapper">
            <Navbar className="sidebar" bg="dark" data-bs-theme="dark">
                <div className="sidebar-content">
                    <div className="sidebar-new-chat">
                        <Button
                            variant="outline-light"
                            className="w-100 new-chat-button"
                            onClick={() => chatStore.newChat()}
                        >
                            <span className="new-chat-icon">+</span>
                            <span>Новый чат</span>
                        </Button>
                    </div>
                    <div className="sidebar-chats">
                        {chatStore.chats.map((chat) => (
                            <button
                                key={chat.id}
                                className={`sidebar-chat-item ${chat.id === chatStore.currentChatId ? 'active' : ''}`}
                                onClick={() => handleSwitchChat(chat.id)}
                            >
                                <span className="sidebar-chat-icon">💬</span>
                                <span className="sidebar-chat-title">
                                    {chatStore.getChatTitle(chat)}
                                </span>
                            </button>
                        ))}
                    </div>
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