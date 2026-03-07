# Misa AI — Android (React Native / Expo)

Клиент Misa AI для Android. Подключается к API сервера Misa (URL из `.env`).

## Настройка

1. Скопируйте URL из `client/.env` в `android/.env`:
   ```
   EXPO_PUBLIC_API_URL=https://misaapi.baxic.ru
   EXPO_PUBLIC_API_WSS=wss://misaapi.baxic.ru/ws/chat/misa/
   ```

2. Установка зависимостей (уже выполнена):
   ```bash
   npm install
   ```

## Запуск

```bash
npm run android
```

Или через Expo Go на устройстве:
```bash
npm start
```
Затем отсканируйте QR-код приложением Expo Go.

## Сборка APK (установка на телефон без Expo Go)

### Вариант 1: EAS Build (облако, проще всего)

1. Установи EAS CLI:
   ```bash
   npm install -g eas-cli
   ```

2. Войди в аккаунт Expo (создай бесплатный на [expo.dev](https://expo.dev)):
   ```bash
   eas login
   ```

3. Собери APK:
   ```bash
   cd android
   eas build -p android --profile preview
   ```

4. После сборки (5–15 мин) появится ссылка на APK. Скачай файл и перекинь на телефон (USB, облако, мессенджер).

5. На телефоне включи «Установка из неизвестных источников» и установи APK.

### Вариант 2: Локальная сборка (без облака)

Нужны: Android Studio, JDK 17.

1. Сгенерируй нативный проект:
   ```bash
   cd android
   npx expo prebuild --platform android
   ```

2. Собери APK:
   ```bash
   cd android
   .\gradlew assembleRelease
   ```

3. APK будет в `android\app\build\outputs\apk\release\app-release.apk`

4. Скопируй файл на телефон и установи.

---

## Функции

- Вход / регистрация (email + пароль, код из письма)
- Список чатов, создание нового
- Отправка сообщений через WebSocket
- Получение ответов Misa в реальном времени
