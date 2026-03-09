import React, { createContext, useContext, useState, useEffect } from "react";
import { getLanguage, setLanguage as setLocale } from "../utils/locale";
import { translations } from "../utils/translations";

export const LocaleContext = createContext(null);

export const useLocale = () => {
  const ctx = useContext(LocaleContext);
  if (!ctx) throw new Error("useLocale must be used within LocaleProvider");
  return ctx;
};

export const LocaleProvider = ({ children }) => {
  const [locale, setLocaleState] = useState("ru");

  useEffect(() => {
    getLanguage().then(setLocaleState);
  }, []);

  const t = (key) => translations[locale]?.[key] ?? translations.ru[key] ?? key;

  const setLang = async (code) => {
    await setLocale(code);
    setLocaleState(code);
  };

  return (
    <LocaleContext.Provider value={{ locale, t, setLanguage: setLang }}>
      {children}
    </LocaleContext.Provider>
  );
};
