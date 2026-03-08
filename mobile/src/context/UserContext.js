import React, { createContext, useContext, useState } from "react";

const UserContext = createContext(null);

export const UserProvider = ({ children }) => {
  const [user, setUserState] = useState({});
  const [isAuth, setIsAuthState] = useState(false);

  const setUser = (data) => setUserState(data || {});
  const setIsAuth = (v) => setIsAuthState(!!v);

  return (
    <UserContext.Provider value={{ user, setUser, isAuth, setIsAuth }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const ctx = useContext(UserContext);
  if (!ctx) throw new Error("useUser must be used within UserProvider");
  return ctx;
};
