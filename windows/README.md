# Misa AI — клиент для Windows (React Native for Windows)

Нативный клиент Misa AI для Windows на базе React Native for Windows.

## Требования

- **Windows 10/11**
- **Node.js** 18+
- **Visual Studio 2022** с компонентами:
  - Desktop development with C++
  - Universal Windows Platform development
  - Windows 10 SDK (10.0.22621.0)

Установить зависимости можно скриптом (PowerShell от администратора):

```powershell
Set-ExecutionPolicy Unrestricted -Scope Process -Force;
iex (New-Object System.Net.WebClient).DownloadString('https://aka.ms/rnw-vs2022-deps.ps1');
```

## Установка

```bash
cd windows
npm install --legacy-peer-deps
```

## Запуск

```bash
# Запустить Metro
npm start

# В другом терминале — запустить приложение
npm run windows
```

## Отличия от мобильной версии

- Нет входа через Google (только email/пароль)
- Экспорт данных — JSON копируется в буфер обмена
- Конфиг через переменные окружения: `EXPO_PUBLIC_API_URL`, `EXPO_PUBLIC_API_WSS`, `EXPO_PUBLIC_WEB_APP_URL`

## Сборка для распространения

1. Открыть `windows/MisaWindows.sln` в Visual Studio
2. Выбрать конфигурацию **Release** и платформу **x64**
3. Собрать решение
4. Для упаковки в MSIX: Project → Publish → Create App Packages...
