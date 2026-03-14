import { Platform } from "react-native";
import { storage } from "../storage";

const STORAGE_KEY = "misa_locale";

export const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "ru", label: "Русский" },
  { code: "de", label: "Deutsch" },
  { code: "ar", label: "العربية" },
  { code: "sq", label: "Shqip" },
  { code: "am", label: "አማርኛ" },
  { code: "hy", label: "Հայերեն" },
  { code: "az", label: "Azərbaycan" },
  { code: "eu", label: "Euskara" },
  { code: "be", label: "Беларуская" },
  { code: "bn", label: "বাংলা" },
  { code: "bg", label: "Български" },
  { code: "my", label: "မြန်မာဘာသာ" },
  { code: "ca", label: "Català" },
  { code: "zh", label: "简体中文" },
  { code: "zh-TW", label: "繁體中文" },
  { code: "hr", label: "Hrvatski" },
  { code: "cs", label: "Čeština" },
  { code: "da", label: "Dansk" },
  { code: "nl", label: "Nederlands" },
  { code: "et", label: "Eesti" },
  { code: "fi", label: "Suomi" },
  { code: "fr", label: "Français" },
  { code: "gl", label: "Galego" },
  { code: "ka", label: "ქართული" },
  { code: "el", label: "Ελληνικά" },
  { code: "he", label: "עברית" },
  { code: "hi", label: "हिन्दी" },
  { code: "hu", label: "Magyar" },
  { code: "is", label: "Íslenska" },
  { code: "id", label: "Bahasa Indonesia" },
  { code: "ga", label: "Gaeilge" },
  { code: "it", label: "Italiano" },
  { code: "ja", label: "日本語" },
  { code: "kn", label: "ಕನ್ನಡ" },
  { code: "kk", label: "Қазақша" },
  { code: "km", label: "ភាសាខ្មែរ" },
  { code: "ko", label: "한국어" },
  { code: "lo", label: "ພາສາລາວ" },
  { code: "lv", label: "Latviešu" },
  { code: "lt", label: "Lietuvių" },
  { code: "mk", label: "Македонски" },
  { code: "ms", label: "Bahasa Melayu" },
  { code: "ml", label: "മലയാളം" },
  { code: "mt", label: "Malti" },
  { code: "mr", label: "मराठी" },
  { code: "mn", label: "Монгол" },
  { code: "ne", label: "नेपाली" },
  { code: "nb", label: "Norsk (bokmål)" },
  { code: "fa", label: "فارسی" },
  { code: "pl", label: "Polski" },
  { code: "pt", label: "Português" },
  { code: "pa", label: "ਪੰਜਾਬੀ" },
  { code: "ro", label: "Română" },
  { code: "sr", label: "Српски" },
  { code: "si", label: "සිංහල" },
  { code: "sk", label: "Slovenčina" },
  { code: "sl", label: "Slovenščina" },
  { code: "es", label: "Español" },
  { code: "sw", label: "Kiswahili" },
  { code: "tl", label: "Tagalog" },
  { code: "tg", label: "Тоҷикӣ" },
  { code: "th", label: "ภาษาไทย" },
  { code: "tr", label: "Türkçe" },
  { code: "uk", label: "Українська" },
  { code: "ur", label: "اردو" },
  { code: "uz", label: "Oʻzbek" },
  { code: "vi", label: "Tiếng Việt" },
  { code: "cy", label: "Cymraeg" },
  { code: "xh", label: "isiXhosa" },
  { code: "yi", label: "ייִדיש" },
  { code: "yo", label: "Yorùbá" },
  { code: "zu", label: "isiZulu" },
  { code: "gu", label: "ગુજરાતી" },
  { code: "haw", label: "ʻŌlelo Hawaiʻi" },
  { code: "ig", label: "Igbo" },
];

export const getSystemLocaleSync = () => {
  return "en";
};

export const getLanguage = async () => {
  const saved = await storage.getItem(STORAGE_KEY);
  if (saved && LANGUAGES.some((l) => l.code === saved)) return saved;
  return getSystemLocaleSync();
};

export const setLanguage = async (code) => {
  if (LANGUAGES.some((l) => l.code === code)) {
    await storage.setItem(STORAGE_KEY, code);
  }
};

export const RTL_CODES = new Set(["ar", "he", "fa", "ur", "yi"]);
export const getIntlLocale = (code) => {
  const map = { zh: "zh-CN", "zh-TW": "zh-TW", pt: "pt-BR", nb: "nb-NO", pa: "pa-IN" };
  return map[code] || code;
};

const MONTH_NAMES_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

/**
 * Format month and year. Uses Intl when available (not in RNW Hermes), else fallback.
 */
export const formatMonthYear = (locale, year, month) => {
  const date = new Date(year, month, 1);
  if (typeof Intl !== "undefined" && Intl.DateTimeFormat) {
    return new Intl.DateTimeFormat(locale, { month: "long", year: "numeric" }).format(date);
  }
  return `${MONTH_NAMES_EN[month]} ${year}`;
};

/**
 * Format time (HH:MM). Uses Intl when available, else fallback.
 */
export const formatTime = (locale, date) => {
  if (typeof Intl !== "undefined" && Intl.DateTimeFormat) {
    return new Intl.DateTimeFormat(locale, { hour: "2-digit", minute: "2-digit" }).format(date);
  }
  const h = date.getHours();
  const m = date.getMinutes();
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
};
