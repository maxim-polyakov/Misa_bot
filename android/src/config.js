import Constants from "expo-constants";

export const API_URL = Constants.expoConfig?.extra?.apiUrl || "https://misaapi.baxic.ru";
export const API_WSS = Constants.expoConfig?.extra?.apiWss || "wss://misaapi.baxic.ru/ws/chat/misa/";
