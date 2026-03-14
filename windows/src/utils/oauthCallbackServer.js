/**
 * Локальный HTTP-сервер для приёма OAuth callback.
 * Возвращает { port, getResult } — port для redirect_uri, getResult() — Promise с { code } или { error, detail }.
 */
export function startOAuthCallbackServer() {
  return new Promise((resolve, reject) => {
    let http;
    try {
      http = require("http");
    } catch (e) {
      reject(new Error("http module not available"));
      return;
    }

    const resultPromise = new Promise((resolveResult) => {
      const server = http.createServer((req, res) => {
        const url = new URL(req.url || "/", "http://localhost");
        const oauthError = url.searchParams.get("oauth_error");
        const oauthDetail = url.searchParams.get("oauth_detail");
        const code = url.searchParams.get("code");
        const oauth = url.searchParams.get("oauth");

        const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>Misa AI</title></head>
<body style="font-family:sans-serif;padding:2rem;text-align:center;">
<p>Авторизация завершена. Можно закрыть это окно.</p>
</body></html>`;

        res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
        res.end(html);

        server.close();
        if (oauthError) {
          resolveResult({ error: oauthError, detail: oauthDetail });
        } else if (oauth === "google" && code) {
          resolveResult({ code });
        } else {
          resolveResult({ error: "OAUTH_MISSING_DATA" });
        }
      });

      server.listen(0, "127.0.0.1", () => {
        const port = server.address().port;
        resolve({ port, getResult: () => resultPromise, stop: () => server.close() });
      });

      server.on("error", reject);
    });
  });
}
