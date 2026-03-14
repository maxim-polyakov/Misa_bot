/**
 * Ensures Microsoft.Windows.CppWinRT 2.0.230706.1 is in solution packages.
 * Copies from NuGet cache if missing (for Clipboard/AsyncStorage packages.config).
 */
const fs = require('fs');
const path = require('path');

const nugetCache = path.join(
  process.env.USERPROFILE || process.env.HOME,
  '.nuget',
  'packages',
  'microsoft.windows.cppwinrt',
  '2.0.230706.1'
);
const destDir = path.join(__dirname, '..', 'windows', 'packages', 'Microsoft.Windows.CppWinRT.2.0.230706.1');

if (!fs.existsSync(nugetCache)) {
  process.exit(0);
}

if (fs.existsSync(destDir)) {
  process.exit(0);
}

try {
  fs.mkdirSync(path.dirname(destDir), { recursive: true });
  copyRecursive(nugetCache, destDir);
  console.log('ensure-cppwinrt: copied CppWinRT 2.0.230706.1 to solution packages');
} catch (e) {
  // Ignore
}

function copyRecursive(src, dest) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const entry of fs.readdirSync(src)) {
      copyRecursive(path.join(src, entry), path.join(dest, entry));
    }
  } else {
    fs.copyFileSync(src, dest);
  }
}
