import { useState, useEffect } from "react";
import { useLocale } from "../contexts/LocaleContext";
import { snippetFromShareMessages } from "../utils/shareLink";
import { getApiBaseUrl } from "../utils/apiBase";

/**
 * Превью публичной ссылки на чат внутри ленты сообщений (данные с GET /api/chats/.../share/).
 */
export default function ShareLinkPreviewCard({ chatId, query }) {
    const { t } = useLocale();
    const [state, setState] = useState({ loading: true, data: null, error: null });

    useEffect(() => {
        let cancelled = false;
        const qs = query ? `?${query}` : "";
        const base = getApiBaseUrl();
        const url = `${base}/api/chats/${encodeURIComponent(chatId)}/share/${qs}`;
        setState({ loading: true, data: null, error: null });
        fetch(url, { credentials: "omit" })
            .then(async (r) => {
                const json = await r.json().catch(() => ({}));
                return { ok: r.ok, status: r.status, json };
            })
            .then(({ ok, status, json }) => {
                if (cancelled) return;
                if (!ok || json.status === "error") {
                    setState({ loading: false, data: null, error: json.message || status });
                    return;
                }
                if (json.data != null && (json.status === "success" || json.data)) {
                    setState({ loading: false, data: json.data, error: null });
                } else {
                    setState({ loading: false, data: null, error: "notfound" });
                }
            })
            .catch(() => {
                if (!cancelled) setState({ loading: false, data: null, error: "fetch" });
            });
        return () => {
            cancelled = true;
        };
    }, [chatId, query]);

    const href =
        typeof window !== "undefined"
            ? `${window.location.origin}/share/${encodeURIComponent(chatId)}${query ? `?${query}` : ""}`
            : "#";

    if (state.loading) {
        return (
            <div className="share-link-preview-card share-link-preview-card--loading" aria-busy="true">
                <span className="share-link-preview-card__hint">{t("shareChatLoading")}</span>
            </div>
        );
    }

    if (state.error || !state.data) {
        return (
            <div className="share-link-preview-card share-link-preview-card--error">
                <span className="share-link-preview-card__hint">{t("shareChatNotFound")}</span>
            </div>
        );
    }

    const title = state.data.title || "Misa AI";
    const snippet = snippetFromShareMessages(state.data.messages);

    return (
        <a
            className="share-link-preview-card"
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
        >
            <img src="/favicon-195.png" alt="" className="share-link-preview-card__icon" width={40} height={40} />
            <div className="share-link-preview-card__body">
                <div className="share-link-preview-card__title">{title}</div>
                {snippet ? <div className="share-link-preview-card__snippet">{snippet}</div> : null}
                <div className="share-link-preview-card__badge">{t("shareChatBadge")}</div>
            </div>
        </a>
    );
}
