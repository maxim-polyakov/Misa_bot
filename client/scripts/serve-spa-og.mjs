/**
 * Production: build/ + для краулеров (Discord и др.) — HTML с API GET /og/preview/
 * (локализованный og:* по Accept-Language). Обычный nginx: proxy_pass на :3000 без отдельных location.
 */
import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BUILD = path.resolve(__dirname, "..", "build");
const PORT = Number(process.env.PORT || 3000);
const OG_API = (process.env.OG_PREVIEW_API_ORIGIN || process.env.REACT_APP_API_URL || "")
    .trim()
    .replace(/\/+$/, "");

const BOT_RE =
    /telegrambot|discordbot|facebookexternalhit|twitterbot|slackbot|whatsapp|linkedinbot|vkshare|embedly|googlebot|bingbot|yandexbot|bytespider|pinterestbot|skypeuripreview|facebot/i;

function isBot(ua) {
    return BOT_RE.test(String(ua || "").toLowerCase());
}

const MIME = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".webp": "image/webp",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".map": "application/json",
    ".txt": "text/plain; charset=utf-8",
};

function contentType(filePath) {
    return MIME[path.extname(filePath).toLowerCase()] || "application/octet-stream";
}

async function fileExists(f) {
    try {
        const st = await fs.promises.stat(f);
        return st.isFile() ? st : null;
    } catch {
        return null;
    }
}

async function sendFile(req, res, filePath) {
    const st = await fileExists(filePath);
    if (!st) return false;
    const headers = {
        "Content-Type": contentType(filePath),
        "Content-Length": st.size,
    };
    if (req.method === "HEAD") {
        res.writeHead(200, headers);
        res.end();
        return true;
    }
    res.writeHead(200, headers);
    fs.createReadStream(filePath).pipe(res);
    return true;
}

async function sendIndex(req, res) {
    const p = path.join(BUILD, "index.html");
    if (await sendFile(req, res, p)) return;
    res.writeHead(500, { "Content-Type": "text/plain" });
    res.end("index.html missing");
}

async function proxyOgPreview(req, res, originalPathAndQuery) {
    if (!OG_API) {
        return sendIndex(req, res);
    }
    const url = `${OG_API}/og/preview/`;
    try {
        const r = await fetch(url, {
            method: "GET",
            headers: {
                "X-Original-URI": originalPathAndQuery,
                "Accept-Language": req.headers["accept-language"] || "",
                "User-Agent": req.headers["user-agent"] || "",
            },
        });
        const buf = Buffer.from(await r.arrayBuffer());
        const ct = r.headers.get("content-type") || "text/html; charset=utf-8";
        if (req.method === "HEAD") {
            res.writeHead(r.status, { "Content-Type": ct, "Content-Length": buf.length });
            res.end();
            return;
        }
        res.writeHead(r.status, { "Content-Type": ct, "Content-Length": buf.length });
        res.end(buf);
    } catch {
        res.writeHead(502, { "Content-Type": "text/plain; charset=utf-8" });
        res.end("OG preview upstream error");
    }
}

const server = http.createServer(async (req, res) => {
    if (req.method !== "GET" && req.method !== "HEAD") {
        res.writeHead(405);
        res.end();
        return;
    }

    let pathname;
    let search;
    try {
        const u = new URL(req.url || "/", "http://127.0.0.1");
        pathname = u.pathname;
        search = u.search || "";
    } catch {
        res.writeHead(400);
        res.end();
        return;
    }

    const decodedPath = decodeURIComponent(pathname);
    const fullPathAndQuery = decodedPath + search;

    if (decodedPath === "/") {
        if (isBot(req.headers["user-agent"])) {
            await proxyOgPreview(req, res, fullPathAndQuery || "/");
            return;
        }
        await sendIndex(req, res);
        return;
    }

    const rel = decodedPath.replace(/^\/+/, "");
    const filePath = path.join(BUILD, rel);

    if (await sendFile(req, res, filePath)) {
        return;
    }

    if (path.extname(decodedPath)) {
        res.writeHead(404);
        res.end();
        return;
    }

    if (isBot(req.headers["user-agent"])) {
        await proxyOgPreview(req, res, fullPathAndQuery);
        return;
    }

    await sendIndex(req, res);
});

server.listen(PORT, () => {
    // eslint-disable-next-line no-console
    console.log(`serve-spa-og: build=${BUILD} port=${PORT} og_api=${OG_API || "(none)"}`);
});
