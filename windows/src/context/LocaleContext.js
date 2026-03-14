import React, { createContext, useContext, useState, useEffect } from "react";
import { View, StyleSheet } from "react-native";
import { getLanguage, getSystemLocaleSync, setLanguage as setLocale, RTL_CODES } from "../utils/locale";
import { translations } from "../utils/translations";

export const LocaleContext = createContext(null);

export const useLocale = () => {
  const ctx = useContext(LocaleContext);
  if (!ctx) throw new Error("useLocale must be used within LocaleProvider");
  return ctx;
};

export const LocaleProvider = ({ children }) => {
  const [locale, setLocaleState] = useState(getSystemLocaleSync);

  useEffect(() => {
    getLanguage().then((code) => {
      setLocaleState(code);
    });
  }, []);

  const t = (key) => translations[locale]?.[key] ?? key;
  const isRTL = RTL_CODES.has(locale);

  const setLang = async (code) => {
    await setLocale(code);
    setLocaleState(code);
  };

  return (
    <LocaleContext.Provider value={{ locale, t, setLanguage: setLang, isRTL }}>
      <View style={[styles.root, { direction: isRTL ? "rtl" : "ltr" }]}>
        {children}
      </View>
    </LocaleContext.Provider>
  );
};

const styles = StyleSheet.create({
  root: {
    flex: 1,
  },
});
