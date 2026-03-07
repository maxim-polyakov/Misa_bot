export default {
  expo: {
    name: "Misa AI",
    slug: "misa-android",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "light",
    splash: {
      image: "./assets/splash-icon.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff",
    },
    ios: { supportsTablet: true },
    android: {
      package: "ru.baxic.misa",
      adaptiveIcon: {
        backgroundColor: "#E6F4FE",
        foregroundImage: "./assets/android-icon-foreground.png",
        backgroundImage: "./assets/android-icon-background.png",
        monochromeImage: "./assets/android-icon-monochrome.png",
      },
    },
    web: { favicon: "./assets/favicon.png" },
    extra: {
      apiUrl: process.env.EXPO_PUBLIC_API_URL || "https://misaapi.baxic.ru",
      apiWss: process.env.EXPO_PUBLIC_API_WSS || "wss://misaapi.baxic.ru/ws/chat/misa/",
      eas: {
        projectId: "f515349c-4ff2-4dd9-aaaa-3c9287c5c793",
      },
    },
  },
};
