const STORAGE_KEY = "misa_theme";

export const THEMES = { LIGHT: "light", DARK: "dark", SYSTEM: "system" };

const getEffectiveTheme = (theme) => {
    if (theme === THEMES.SYSTEM) {
        return window.matchMedia("(prefers-color-scheme: dark)").matches ? THEMES.DARK : THEMES.LIGHT;
    }
    return theme;
};

export const getTheme = () => {
    return localStorage.getItem(STORAGE_KEY) || THEMES.DARK;
};

export const setTheme = (theme) => {
    localStorage.setItem(STORAGE_KEY, theme);
    applyTheme();
};

export const applyTheme = () => {
    const theme = getTheme();
    const effective = getEffectiveTheme(theme);
    document.documentElement.setAttribute("data-theme", effective);
};

// Инициализация при загрузке
if (typeof window !== "undefined") {
    applyTheme();
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
        if (getTheme() === THEMES.SYSTEM) applyTheme();
    });
}
