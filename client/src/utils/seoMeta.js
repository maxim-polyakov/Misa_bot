import { translations } from "./translations.js";

function upsertMetaByName(name, content) {
    let el = document.head.querySelector(`meta[name="${name}"]`);
    if (!el) {
        el = document.createElement("meta");
        el.setAttribute("name", name);
        document.head.appendChild(el);
    }
    el.setAttribute("content", content);
}

function upsertMetaByProperty(property, content) {
    let el = document.head.querySelector(`meta[property="${property}"]`);
    if (!el) {
        el = document.createElement("meta");
        el.setAttribute("property", property);
        document.head.appendChild(el);
    }
    el.setAttribute("content", content);
}

/**
 * Updates description / Open Graph / Twitter preview text from translations for the active locale.
 */
export function applySeoMeta(locale) {
    if (typeof document === "undefined") return;
    const text =
        translations[locale]?.ogPreview ??
        translations.en?.ogPreview ??
        "";
    if (!text) return;

    upsertMetaByName("description", text);
    upsertMetaByProperty("og:title", text);
    upsertMetaByProperty("og:description", text);
    upsertMetaByName("twitter:title", text);
    upsertMetaByName("twitter:description", text);
}
