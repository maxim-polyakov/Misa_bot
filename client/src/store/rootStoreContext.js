import { createContext, useContext, useEffect } from "react";
import ChatStore from "./chatStore";

const rootStore = {
    chatStore: new ChatStore(),
};

export const StoreContext = createContext(rootStore);

export const useStores = () => useContext(StoreContext);

// Хук для очистки при размонтировании
export const useCleanup = () => {
    const stores = useStores();

    useEffect(() => {
        return () => {
            // Очистка всех хранилищ
            if (stores.chatStore.cleanup) {
                stores.chatStore.cleanup();
            }
        };
    }, [stores]);
};