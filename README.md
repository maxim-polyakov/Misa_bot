# Misa

Мультиплатформенный AI-ассистент: боты в Discord и Telegram, REST/WebSocket API на Django и клиенты для веба, Android и Windows.

## Структура репозитория

| Каталог | Описание |
|---------|----------|
| [`server/`](server/) | Python-бэкенд: Django API, WebSocket-чат, боты Discord/Telegram, NLP и хранилище |
| [`client/`](client/) | Веб-клиент (React) |
| [`mobile/`](mobile/) | Android-клиент (React Native / Expo) |
| [`windows/`](windows/) | Нативный клиент для Windows (React Native for Windows) |
| [`docs/`](docs/) | Дополнительная документация (например, [Google OAuth](docs/GOOGLE_OAUTH_SETUP.md)) |

## Возможности

- Чат с Misa в реальном времени (WebSocket)
- Регистрация и вход по email, сброс пароля, OAuth Google (веб и мобильные клиенты)
- Список чатов, экспорт, публичный шаринг с Open Graph-превью
- Боты в **Telegram** и **Discord**: сообщения, голос, картинки, погода, поиск, wiki и др.
- Трёхслойная архитектура сервера (Front / Core / Deep) — подробнее в [server/README.md](server/README.md)

## Архитектура (кратко)

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   client    │  │   mobile    │  │   windows   │  │  Telegram   │
│   (React)   │  │   (Expo)    │  │  (RN Win)   │  │   Discord   │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │
       └────────────────┴────────────────┴────────────────┘
                                │
                    Django API + WebSocket (Hypercorn)
                    Redis (опционально) · PostgreSQL · S3
```

Точки входа на сервере (см. [`server/run.sh`](server/run.sh)):

- `server_main.py` — ASGI API (порт **8001**)
- `telegram_main.py` — Telegram-бот (Flask **9000**)
- `discord_main.py` — Discord-бот (Flask **8000**)

## Быстрый старт

### Сервер

```bash
cd server
cp .env.example .env   # заполните переменные
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python server_main.py
```

Для полного стека (боты + API) в Docker:

```bash
cd server
docker build -t misa-server .
# см. run.sh и .env для переменных окружения
```

Подробности: [server/README.md](server/README.md)

### Веб-клиент

```bash
cd client
cp .env.example .env
npm install
npm start
```

Приложение откроется на [http://localhost:3000](http://localhost:3000). Для production: `npm run build`.

### Android

```bash
cd mobile
npm install
# EXPO_PUBLIC_API_URL и EXPO_PUBLIC_API_WSS в .env
npm run android
```

Подробности: [mobile/README.md](mobile/README.md)

### Windows

Требуются Node.js 18+, Visual Studio 2022 с UWP/C++ workload.

```bash
cd windows
npm install --legacy-peer-deps
npm start          # Metro
npm run windows    # в другом терминале
```

Подробности: [windows/README.md](windows/README.md)

## Переменные окружения

| Компонент | Файл-образец |
|-----------|----------------|
| API | [`server/.env.example`](server/.env.example) |
| Веб | [`client/.env.example`](client/.env.example) |
| Android / Windows | `EXPO_PUBLIC_API_URL`, `EXPO_PUBLIC_API_WSS` (см. README в `mobile/` и `windows/`) |

В production обычно разделяют домены API и фронта (например `misaapi.example.com` и `misa.example.com`).

## API и документация

После запуска Django доступны:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`
- OpenAPI schema: `/schema/`

## Тесты (сервер)

```bash
cd server
python tests_main.py
```

## Лицензия

Уточните лицензию в репозитории при публикации; отдельный файл `LICENSE` в корне пока не задан.
