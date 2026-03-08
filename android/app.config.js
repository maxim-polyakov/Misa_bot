export default {
  expo: {
    name: "Misa AI",
    plugins: [
      "expo-sharing",
      [
        "@react-native-google-signin/google-signin",
        {
          iosUrlScheme: process.env.EXPO_PUBLIC_GOOGLE_IOS_URL_SCHEME || "com.googleusercontent.apps.placeholder",
        },
      ],
    ],
    slug: "misa-android",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "light",
    splash: {
      image: "./assets/icon.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff",
    },
    ios: {
      supportsTablet: true,
      bundleIdentifier: "ru.baxic.misa",
    },
    android: {
      package: "ru.baxic.misa",
      softwareKeyboardLayoutMode: "resize",
      adaptiveIcon: {
        backgroundColor: "#E6F4FE",
        foregroundImage: "./assets/icon.png",
      },
    },
    web: { favicon: "./assets/favicon.png" },
    extra: {
      apiUrl: process.env.EXPO_PUBLIC_API_URL || "https://misaapi.baxic.ru",
      apiWss: process.env.EXPO_PUBLIC_API_WSS || "wss://misaapi.baxic.ru/ws/chat/misa/",
      webAppUrl: process.env.EXPO_PUBLIC_WEB_APP_URL || "https://misa.baxic.ru",
      googleWebClientId: process.env.EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID || "",
      eas: {
        projectId: "f515349c-4ff2-4dd9-aaaa-3c9287c5c793",
      },
    },
  },
};
