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

export const getLanguage = () => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && LANGUAGES.some((l) => l.code === saved)) return saved;
    const full = navigator.language || "";
    const short = full.slice(0, 2);
    const exact = LANGUAGES.find((l) => l.code === full);
    if (exact) return exact.code;
    const prefix = LANGUAGES.find((l) => l.code === short || l.code.startsWith(short + "-"));
    return prefix ? prefix.code : "en";
};

const LOCALE_COOKIE = "misa_locale";
const LOCALE_COOKIE_MAX_AGE = 31536000;

function setLocaleCookie(code) {
    try {
        document.cookie = `${LOCALE_COOKIE}=${encodeURIComponent(code)}; Path=/; Max-Age=${LOCALE_COOKIE_MAX_AGE}; SameSite=Lax`;
    } catch {
        /* ignore */
    }
}

/** URL ?lang= и cookie — совпадают с языком в настройках; боты читают query в X-Original-URI (cookie часто не шлют). */
export function syncLangQueryWithSettings(code) {
    if (typeof document === "undefined") return;
    if (!LANGUAGES.some((l) => l.code === code)) return;
    setLocaleCookie(code);
    try {
        const u = new URL(window.location.href);
        if ((u.searchParams.get("lang") || "").toLowerCase() !== String(code).toLowerCase()) {
            u.searchParams.set("lang", code);
            window.history.replaceState({}, "", `${u.pathname}${u.search}${u.hash}`);
        }
    } catch {
        /* ignore */
    }
}

/** POST на API: Set-Cookie misa_locale на сервере (для og/preview; при UI_LOCALE_COOKIE_DOMAIN=. — общий с вебом). */
export function postUiLocaleToServer(code) {
    const base = (typeof process !== "undefined" && process.env && process.env.REACT_APP_API_URL
        ? process.env.REACT_APP_API_URL
        : ""
    ).replace(/\/$/, "");
    if (!base || !LANGUAGES.some((l) => l.code === code)) return;
    fetch(`${base}/api/ui-locale/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ locale: code }),
    }).catch(() => {
        /* сеть / CORS — локально остаются localStorage и клиентский cookie */
    });
}

export const setLanguage = (code) => {
    if (LANGUAGES.some((l) => l.code === code)) {
        localStorage.setItem(STORAGE_KEY, code);
        setLocaleCookie(code);
        postUiLocaleToServer(code);
        window.dispatchEvent(new CustomEvent("localechange", { detail: code }));
    }
};

export const RTL_CODES = new Set(["ar", "he", "fa", "ur", "yi"]);

export const getIntlLocale = (code) => {
    const map = { zh: "zh-CN", "zh-TW": "zh-TW", pt: "pt-BR", nb: "nb-NO", pa: "pa-IN" };
    return map[code] || code;
};

export const applyDocumentLocale = (code) => {
    if (typeof document === "undefined") return;
    document.documentElement.lang = getIntlLocale(code);
    document.documentElement.dir = RTL_CODES.has(code) ? "rtl" : "ltr";
    syncLangQueryWithSettings(code);
};
