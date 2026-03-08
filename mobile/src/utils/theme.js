import { storage } from "../storage";

const STORAGE_KEY = "misa_theme";

export const THEMES = { LIGHT: "light", DARK: "dark", SYSTEM: "system" };

export const getTheme = async () => {
  const saved = await storage.getItem(STORAGE_KEY);
  return saved && Object.values(THEMES).includes(saved) ? saved : THEMES.DARK;
};

export const setTheme = async (theme) => {
  if (Object.values(THEMES).includes(theme)) {
    await storage.setItem(STORAGE_KEY, theme);
  }
};
