import { storage } from "../storage";

const STORAGE_KEY = "misa_locale";

export const LANGUAGES = [
  { code: "ru", label: "Русский" },
  { code: "en", label: "English" },
  { code: "de", label: "Deutsch" },
];

export const getLanguage = async () => {
  const saved = await storage.getItem(STORAGE_KEY);
  if (saved && LANGUAGES.some((l) => l.code === saved)) return saved;
  return "ru";
};

export const setLanguage = async (code) => {
  if (LANGUAGES.some((l) => l.code === code)) {
    await storage.setItem(STORAGE_KEY, code);
  }
};
