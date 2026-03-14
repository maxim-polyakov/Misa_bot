/**
 * Patches RNScreens.idl for WinUI 3 compatibility (ForcePaperUseWinUI3).
 * Windows.UI.Xaml -> Microsoft.UI.Xaml
 */
const fs = require('fs');
const path = require('path');

const targetPath = path.join(
  __dirname,
  '..',
  'node_modules',
  'react-native-screens',
  'windows',
  'RNScreens',
  'RNScreens.idl'
);

if (!fs.existsSync(targetPath)) {
  process.exit(0);
}

let content = fs.readFileSync(targetPath, 'utf8');

if (content.includes('Microsoft.UI.Xaml.Controls.TextBox')) {
  process.exit(0);
}

content = content.replace(
  'Windows.UI.Xaml.Controls.TextBox',
  'Microsoft.UI.Xaml.Controls.TextBox'
);
fs.writeFileSync(targetPath, content);
console.log('patch-rnscreens: applied WinUI 3 IDL fix');
