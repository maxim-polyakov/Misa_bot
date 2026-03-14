/**
 * Clipboard wrapper. On Windows, @react-native-clipboard/clipboard is excluded from the build,
 * so we provide a stub to avoid RNCClipboard native module errors.
 */
import { Platform } from "react-native";

let Clipboard = null;
if (Platform.OS !== "windows") {
  Clipboard = require("@react-native-clipboard/clipboard").default;
}

export default Clipboard
  ? Clipboard
  : {
      setString: (text) => {
        // Clipboard not supported on Windows; could show toast in future
      },
      getString: () => Promise.resolve(""),
    };
