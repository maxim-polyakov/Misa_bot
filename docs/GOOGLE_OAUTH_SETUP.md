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

7. **Для Android-приложения** создайте дополнительный OAuth-клиент:
   - **"+ Создать учётные данные"** → **"Идентификатор клиента OAuth"**
   - Тип: **"Android"**
   - Имя: например, "Misa Android"
   - Package name: `ru.baxic.misa` (из `android/app.config.js`)
   - SHA-1: отпечаток сертификата подписи:
     - **Через терминал** (рекомендуется): `cd android && eas credentials` → Android → Keystore → в выводе будет SHA-1. Если keystore ещё нет, сначала выполните `eas build -p android --profile preview`.
     - **Через сайт**: [expo.dev](https://expo.dev) → войти → ваш проект → **Credentials** (или Build → выберите сборку → Configure → Credentials).
     - **Локальная debug-сборка**: `npx expo prebuild` (создаёт папку `android/`), затем `cd android && .\gradlew.bat signingReport` (Windows) или `./gradlew signingReport` (macOS/Linux) — SHA-1 в блоке `Variant: debug`.
   - Нажмите **"Создать"**

8. Создайте `server/.env` (скопируйте из `server/.env.example`) и заполните:
   - `GOOGLE_CLIENT_ID` — Web Client ID из Google Console (для веб OAuth и проверки id_token)
   - `GOOGLE_CLIENT_SECRET` — Client Secret из Google Console
   - `GOOGLE_CLIENT_ID_ANDROID` — (опционально) Android Client ID для проверки id_token с Android
   - `GOOGLE_CLIENT_ID_IOS` — (опционально) iOS Client ID для проверки id_token с iOS
   - `API_BASE_URL` — базовый URL API (например `https://misaapi.baxic.ru`)
   - `FRONTEND_URL` — URL фронтенда для редиректа после OAuth (например `https://ваш-клиент.ru` или `http://localhost:3000`)

   Сервер читает переменные из `.env`, а не из environment.

9. Для Android-приложения добавьте в `android/.env`:
   - `EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID` — тот же Web Client ID, что и `GOOGLE_CLIENT_ID` на сервере

10. Выполните миграцию БД:
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

## Android: вход через Google

1. Android-приложение использует `@react-native-google-signin/google-signin`.
2. При нажатии «Войти через Google» приложение получает `id_token` от Google и отправляет его на `POST /auth/google-id-token/`.
3. Сервер проверяет токен через `GOOGLE_CLIENT_ID` (или `GOOGLE_CLIENT_ID_ANDROID`) и возвращает JWT.
4. Требуется OAuth-клиент типа **Android** с package `ru.baxic.misa` и SHA-1 в Google Console.
5. `EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID` в `android/.env` должен совпадать с Web Client ID.

## iOS: вход через Google

1. Создайте OAuth-клиент типа **iOS** в Google Console:
   - Package name: `ru.baxic.misa` (bundleIdentifier из app.config.js)
   - (опционально) App Store ID, Team ID, Key ID для production
2. Добавьте в `server/.env`: `GOOGLE_CLIENT_ID_IOS` — iOS Client ID из Google Console.
3. Добавьте в `android/.env`: `EXPO_PUBLIC_GOOGLE_IOS_URL_SCHEME` — reversed iOS Client ID (например `com.googleusercontent.apps.906407442864-xxxxx`).
4. Сервер проверяет id_token через `GOOGLE_CLIENT_ID_IOS` и возвращает JWT.
