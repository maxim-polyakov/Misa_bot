/**
 * Copies MaterialCommunityIcons font to Windows Package Assets for react-native-vector-icons
 */
const fs = require('fs');
const path = require('path');

const fontSource = path.join(
  __dirname,
  '../node_modules/react-native-vector-icons/Fonts/MaterialCommunityIcons.ttf'
);
const assetsDir = path.join(__dirname, '../windows/MisaWindows.Package/Assets');
const fontDest = path.join(assetsDir, 'MaterialCommunityIcons.ttf');

if (fs.existsSync(fontSource)) {
  if (!fs.existsSync(assetsDir)) {
    fs.mkdirSync(assetsDir, { recursive: true });
  }
  fs.copyFileSync(fontSource, fontDest);
  console.log('Copied MaterialCommunityIcons.ttf to Package Assets');
}
