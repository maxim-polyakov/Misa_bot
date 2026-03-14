/**
 * Отключает параллельную компиляцию в react-native-webview для обхода D8040 / Permission denied.
 */
const fs = require('fs');
const path = require('path');

const vcxprojPath = path.join(
  __dirname,
  '..',
  'node_modules',
  'react-native-webview',
  'windows',
  'ReactNativeWebView',
  'ReactNativeWebView.vcxproj'
);

if (!fs.existsSync(vcxprojPath)) {
  process.exit(0);
}

let content = fs.readFileSync(vcxprojPath, 'utf8');

if (content.includes('<MultiProcessorCompilation>false</MultiProcessorCompilation>')) {
  process.exit(0);
}

content = content.replace(
  /(<ClCompile>\s*)(<PrecompiledHeader>Use<\/PrecompiledHeader>)/,
  '$1<MultiProcessorCompilation>false</MultiProcessorCompilation>\n      $2'
);

fs.writeFileSync(vcxprojPath, content);
