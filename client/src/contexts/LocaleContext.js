import { createContext, useContext, useState, useEffect } from "react";
import { getLanguage, setLanguage as setLocale } from "../utils/locale.js";
import { translations } from "../utils/translations.js";

export const LocaleContext = createContext(null);

export const useLocale = () => {
    const ctx = useContext(LocaleContext);
    if (!ctx) throw new Error("useLocale must be used within LocaleProvider");
    return ctx;
};

export const LocaleProvider = ({ children }) => {
    const [locale, setLocaleState] = useState(getLanguage);

    useEffect(() => {
        const handleChange = () => setLocaleState(getLanguage());
        window.addEventListener("localechange", handleChange);
        return () => window.removeEventListener("localechange", handleChange);
    }, []);

    const t = (key) => translations[locale]?.[key] ?? translations.en?.[key] ?? translations.ru?.[key] ?? key;
    const setLang = (code) => {
        setLocale(code);
        setLocaleState(code);
    };

    return (
        <LocaleContext.Provider value={{ locale, t, setLanguage: setLang }}>
            {children}
        </LocaleContext.Provider>
    );
};
