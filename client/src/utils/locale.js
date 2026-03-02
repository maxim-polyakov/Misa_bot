const STORAGE_KEY = "misa_locale";

export const LANGUAGES = [
    { code: "ru", label: "Русский" },
    { code: "en", label: "English" },
];

export const getLanguage = () => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && LANGUAGES.some((l) => l.code === saved)) return saved;
    const browserLang = navigator.language?.slice(0, 2);
    return LANGUAGES.some((l) => l.code === browserLang) ? browserLang : "ru";
};

export const setLanguage = (code) => {
    if (LANGUAGES.some((l) => l.code === code)) {
        localStorage.setItem(STORAGE_KEY, code);
        window.dispatchEvent(new CustomEvent("localechange", { detail: code }));
    }
};
