import { OG_PREVIEW } from "./ogPreviewStrings.js";

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
 * В браузере: og:* по локали (настройки). У краулеров превью даёт Django GET /og/preview/
 * (через scripts/serve-spa-og.mjs в production) — без JS.
 */
export function applySeoMeta(locale) {
    if (typeof document === "undefined") return;
    const text = OG_PREVIEW[locale] ?? OG_PREVIEW.en;
    if (!text) return;

    upsertMetaByName("description", text);
    upsertMetaByProperty("og:title", text);
    upsertMetaByProperty("og:description", text);
    upsertMetaByName("twitter:title", text);
    upsertMetaByName("twitter:description", text);
}
