import AsyncStorage from "@react-native-async-storage/async-storage";

export const storage = {
  getItem: (key) => AsyncStorage.getItem(key),
  setItem: (key, value) => AsyncStorage.setItem(key, String(value)),
  removeItem: (key) => AsyncStorage.removeItem(key),
};
