// Config for Windows — переменные из .env
import {
  EXPO_PUBLIC_API_URL,
  EXPO_PUBLIC_API_WSS,
  EXPO_PUBLIC_WEB_APP_URL,
} from "@env";

export const API_URL = EXPO_PUBLIC_API_URL || "https://misaapi.baxic.ru";
export const API_WSS = EXPO_PUBLIC_API_WSS || "wss://misaapi.baxic.ru/ws/chat/misa/";
export const WEB_APP_URL = EXPO_PUBLIC_WEB_APP_URL || "https://misa.baxic.ru";
