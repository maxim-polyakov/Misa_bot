import React, { createContext, useContext, useState, useEffect } from "react";
import { useColorScheme } from "react-native";
import { getTheme, setTheme as saveTheme, THEMES } from "../utils/theme";

const COLORS_DARK = {
  primaryBg: "#1c1c1e",
  secondaryBg: "#2c2c2e",
  messageBg: "#2c2c2e",
  userMessageBg: "#4a90e2",
  borderColor: "#3a3a3c",
  textPrimary: "#ffffff",
  textSecondary: "#8e8e93",
  accentColor: "#4a90e2",
  sidebarBg: "#2a2a2d",
};

const COLORS_LIGHT = {
  primaryBg: "#f2f2f7",
  secondaryBg: "#ffffff",
  messageBg: "#e5e5ea",
  userMessageBg: "#4a90e2",
  borderColor: "#d1d1d6",
  textPrimary: "#1c1c1e",
  textSecondary: "#6e6e73",
  accentColor: "#4a90e2",
  sidebarBg: "#e5e5ea",
};

const ThemeContext = createContext(null);

export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
};

export const ThemeProvider = ({ children }) => {
  const systemPrefersDark = useColorScheme() === "dark";
  const [rawTheme, setRawTheme] = useState(THEMES.DARK);
  const [ready, setReady] = useState(false);

  const effectiveTheme =
    rawTheme === THEMES.SYSTEM ? (systemPrefersDark ? THEMES.DARK : THEMES.LIGHT) : rawTheme;
  const colors = effectiveTheme === THEMES.LIGHT ? COLORS_LIGHT : COLORS_DARK;
  const isDark = effectiveTheme === THEMES.DARK;

  useEffect(() => {
    getTheme().then((t) => {
      setRawTheme(t);
      setReady(true);
    });
  }, []);

  const setTheme = async (theme) => {
    if (Object.values(THEMES).includes(theme)) {
      await saveTheme(theme);
      setRawTheme(theme);
    }
  };

  return (
    <ThemeContext.Provider
      value={{
        theme: rawTheme,
        effectiveTheme,
        colors,
        isDark,
        setTheme,
        ready,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};
