/**
 * Patches @react-native-clipboard/clipboard to use CppWinRT 2.0.230706.1
 * (compatible with react-native-windows 0.76)
 */
const fs = require('fs');
const path = require('path');

const base = path.join(__dirname, '..', 'node_modules', '@react-native-clipboard', 'clipboard', 'windows', 'Clipboard');

const packagesConfig = path.join(base, 'packages.config');
const vcxproj = path.join(base, 'Clipboard.vcxproj');

if (!fs.existsSync(packagesConfig) || !fs.existsSync(vcxproj)) {
  process.exit(0);
}

let changed = false;

let content = fs.readFileSync(packagesConfig, 'utf8');
if (content.includes('2.0.200316.3')) {
  content = content.replace('2.0.200316.3', '2.0.230706.1');
  fs.writeFileSync(packagesConfig, content);
  changed = true;
}

content = fs.readFileSync(vcxproj, 'utf8');
if (content.includes('2.0.200316.3')) {
  content = content.replace(/2\.0\.200316\.3/g, '2.0.230706.1');
  fs.writeFileSync(vcxproj, content);
  changed = true;
}

if (changed) {
  console.log('patch-clipboard: updated CppWinRT to 2.0.230706.1');
}
