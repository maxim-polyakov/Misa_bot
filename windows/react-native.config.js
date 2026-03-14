module.exports = {
  dependencies: {
    'react-native-screens': {
      platforms: {
        windows: null, // Несовместим с New Arch + WinUI 3 (MIDL2011)
      },
    },
    '@react-native-clipboard/clipboard': {
      platforms: {
        windows: null, // cppwinrt IXamlMetadataProvider conflict
      },
    },
    // react-native-webview включён для Windows — OAuth в WebView (избегаем спама окон при misa://)
    'react-native-http-bridge': {
      platforms: {
        windows: null, // нет нативной реализации для Windows
      },
    },
  },
};
