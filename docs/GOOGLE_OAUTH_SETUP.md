# Настройка Google OAuth (по аналогии с e-commerce-java-two)

## Ссылка на Google Console

**Создание и настройка OAuth credentials:**
https://console.cloud.google.com/apis/credentials

## Шаги настройки

1. Перейдите по ссылке выше и войдите в Google аккаунт.

2. Создайте проект (или выберите существующий).

3. Нажмите **"+ Создать учётные данные"** → **"Идентификатор клиента OAuth"**.

4. Выберите тип приложения: **"Веб-приложение"**.

5. Укажите:
   - **Имя**: например, "Misa Bot"
   - **Авторизованные URI перенаправления**: `https://ваш-api-домен/auth/oauth/callback/` (например `https://misaapi.baxic.ru/auth/oauth/callback/`)

6. Нажмите **"Создать"** и скопируйте **Client ID** и **Client Secret**.

7. Создайте `server/.env` (скопируйте из `server/.env.example`) и заполните:
   - `GOOGLE_CLIENT_ID` — Client ID из Google Console
   - `GOOGLE_CLIENT_SECRET` — Client Secret из Google Console
   - `API_BASE_URL` — базовый URL API (например `https://misaapi.baxic.ru`)
   - `FRONTEND_URL` — URL фронтенда для редиректа после OAuth (например `https://ваш-клиент.ru` или `http://localhost:3000`)

   Сервер читает переменные из `.env`, а не из environment.

8. Выполните миграцию БД:
   ```bash
   psql -U your_user -d your_db -f server/migrations/001_google_oauth_users.sql
   ```

## Поток OAuth (как в e-commerce-java-two)

1. Пользователь нажимает «Войти через Google» → редирект на `${API_URL}/auth/oauth/google/`
2. Сервер редиректит на Google для авторизации
3. Google редиректит на `${API_BASE_URL}/auth/oauth/callback/?code=...`
4. Сервер обменивает code на данные пользователя, создаёт/находит пользователя, генерирует JWT, кладёт в OAuthCodeStore
5. Редирект на `${FRONTEND_URL}/login?oauth=google&code=xxx`
6. Фронтенд вызывает `GET /auth/oauth-token/?code=xxx` и получает JWT
