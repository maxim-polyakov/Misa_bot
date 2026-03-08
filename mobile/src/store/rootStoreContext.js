import React, { createContext, useContext } from "react";
import ChatStore from "./chatStore";

class RootStore {
  constructor() {
    this.chatStore = new ChatStore(this);
  }
}

const RootStoreContext = createContext(null);

export const RootStoreProvider = ({ children }) => {
  const [rootStore] = React.useState(() => new RootStore());
  return (
    <RootStoreContext.Provider value={rootStore}>
      {children}
    </RootStoreContext.Provider>
  );
};

export const useStores = () => {
  const store = useContext(RootStoreContext);
  if (!store) throw new Error("useStores must be used within RootStoreProvider");
  return { chatStore: store.chatStore };
};
