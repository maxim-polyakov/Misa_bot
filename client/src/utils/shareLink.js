/**
 * Извлекает ссылки вида /share/<chat_id> из текста (с любым origin или без).
 * @returns {{ chatId: string, query: string }[]} уникальные пары (query без ведущего ?)
 */
export function extractShareLinksFromText(text) {
    if (!text || typeof text !== 'string') return [];
    const re = /(?:https?:\/\/[^\s/]+)?\/share\/([^?\s#]+)(?:\?([^\s#]*))?/gi;
    const seen = new Set();
    const out = [];
    let m;
    while ((m = re.exec(text)) !== null) {
        let chatId;
        try {
            chatId = decodeURIComponent(m[1]);
        } catch {
            chatId = m[1];
        }
        const query = (m[2] || '').trim();
        const key = `${chatId}\0${query}`;
        if (seen.has(key)) continue;
        seen.add(key);
        out.push({ chatId, query });
    }
    return out;
}

/** Краткое описание для превью (как для og:description) */
export function snippetFromShareMessages(messages) {
    for (const msg of messages || []) {
        const c = (msg.content || '').trim();
        if (!c) continue;
        const text = c.replace(/```[\s\S]*?```/g, '').replace(/\s+/g, ' ').trim();
        if (!text) continue;
        return text.length > 160 ? `${text.slice(0, 159)}…` : text;
    }
    return '';
}
