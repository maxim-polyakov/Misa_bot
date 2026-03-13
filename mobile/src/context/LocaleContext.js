import React, { createContext, useContext, useState, useEffect } from "react";
import { I18nManager } from "react-native";
import { getLanguage, setLanguage as setLocale, RTL_CODES } from "../utils/locale";
import { translations } from "../utils/translations";

export const LocaleContext = createContext(null);

export const useLocale = () => {
  const ctx = useContext(LocaleContext);
  if (!ctx) throw new Error("useLocale must be used within LocaleProvider");
  return ctx;
};

const applyRTL = (code) => {
  const needRTL = RTL_CODES.has(code);
  if (I18nManager.isRTL !== needRTL) {
    I18nManager.forceRTL(needRTL);
    // RTL применяется после перезапуска приложения
  }
};

export const LocaleProvider = ({ children }) => {
  const [locale, setLocaleState] = useState("ru");

  useEffect(() => {
    getLanguage().then((code) => {
      setLocaleState(code);
      applyRTL(code);
    });
  }, []);

  const t = (key) => translations[locale]?.[key] ?? translations.en?.[key] ?? translations.ru?.[key] ?? key;

  const setLang = async (code) => {
    await setLocale(code);
    setLocaleState(code);
    applyRTL(code);
  };

  return (
    <LocaleContext.Provider value={{ locale, t, setLanguage: setLang }}>
      {children}
    </LocaleContext.Provider>
  );
};
