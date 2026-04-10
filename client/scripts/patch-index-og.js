/**
 * После react-scripts build подставляет REACT_APP_WEB_ORIGIN в index.html
 * для og:image / og:url (абсолютные URL — как у страницы /share/ на API).
 * Читает .env.production / .env так же, как ожидает пользователь при сборке.
 */
const fs = require('fs');
const path = require('path');

const buildIndex = path.join(__dirname, '..', 'build', 'index.html');
const PLACEHOLDER = '__OG_SITE_ORIGIN__';

function readWebOriginFromEnvFiles() {
  const root = path.join(__dirname, '..');
  const files = [
    '.env.production.local',
    '.env.production',
    '.env.local',
    '.env',
  ];
  for (const name of files) {
    const f = path.join(root, name);
    if (!fs.existsSync(f)) continue;
    const text = fs.readFileSync(f, 'utf8');
    for (const line of text.split(/\r?\n/)) {
      const m = line.match(/^\s*REACT_APP_WEB_ORIGIN\s*=\s*(.+?)\s*$/);
      if (m) {
        let v = m[1].trim();
        if (
          (v.startsWith('"') && v.endsWith('"')) ||
          (v.startsWith("'") && v.endsWith("'"))
        ) {
          v = v.slice(1, -1);
        }
        return v.replace(/\/$/, '');
      }
    }
  }
  return (process.env.REACT_APP_WEB_ORIGIN || '').replace(/\/$/, '');
}

function main() {
  if (!fs.existsSync(buildIndex)) {
    console.error('patch-index-og: build/index.html not found. Run react-scripts build first.');
    process.exit(1);
  }
  const origin = readWebOriginFromEnvFiles();
  let html = fs.readFileSync(buildIndex, 'utf8');
  if (!html.includes(PLACEHOLDER)) {
    return;
  }
  html = html.split(PLACEHOLDER).join(origin);
  fs.writeFileSync(buildIndex, html, 'utf8');
  if (origin) {
    console.log('patch-index-og: OG URLs use origin', origin);
  } else {
    console.log('patch-index-og: REACT_APP_WEB_ORIGIN not set; OG tags use root-relative paths.');
  }
}

main();
