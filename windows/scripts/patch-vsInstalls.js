/**
 * Patches vsInstalls.js to add fallback for finding VS 2022 when vswhere returns nothing.
 * Run after npm install.
 */
const fs = require('fs');
const path = require('path');

const targetPath = path.join(
  __dirname,
  '..',
  'node_modules',
  '@react-native-windows',
  'cli',
  'lib-commonjs',
  'utils',
  'vsInstalls.js'
);

if (!fs.existsSync(targetPath)) {
  process.exit(0);
}

let content = fs.readFileSync(targetPath, 'utf8');

if (content.includes('findVsByStandardPath')) {
  process.exit(0);
}

// Patch: add fallback and wrap enumerateVsInstalls in try/catch
const search = `exports.enumerateVsInstalls = enumerateVsInstalls;
/**
 * Find the latest available VS installation that matches the given constraints
 */
function findLatestVsInstall(opts) {
    let installs = enumerateVsInstalls({ ...opts, latest: true });
    if (opts.prerelease && installs.length > 0) {
        installs = installs.filter(x => x.prerelease === 'True');
    }
    if (installs.length > 0) {
        return installs[0];
    }
    else {
        return null;
    }
}`;

const replace = `exports.enumerateVsInstalls = enumerateVsInstalls;
/**
 * Fallback: find VS 2022 by standard path when vswhere returns nothing
 */
function findVsByStandardPath() {
    const programFiles = process.env['ProgramFiles'] || 'C:\\\\Program Files';
    const candidates = [
        path_1.default.join(programFiles, 'Microsoft Visual Studio', '2022', 'Community'),
        path_1.default.join(programFiles, 'Microsoft Visual Studio', '2022', 'Professional'),
        path_1.default.join(programFiles, 'Microsoft Visual Studio', '2022', 'Enterprise'),
    ];
    for (const installationPath of candidates) {
        const msbuildPath = path_1.default.join(installationPath, 'MSBuild', 'Current', 'Bin', 'MSBuild.exe');
        const vcToolsPath = path_1.default.join(installationPath, 'VC', 'Tools', 'MSVC');
        if (fs_1.default.existsSync(msbuildPath) && fs_1.default.existsSync(vcToolsPath)) {
            return {
                installationPath,
                installationVersion: '17.11.0',
                catalog: { productMilestoneIsPreRelease: 'False' },
                prerelease: 'False',
            };
        }
    }
    return null;
}
function findLatestVsInstall(opts) {
    let installs = [];
    try {
        installs = enumerateVsInstalls({ ...opts, latest: true });
    }
    catch (_e) {
        // vswhere failed or returned nothing
    }
    if (opts.prerelease && installs.length > 0) {
        installs = installs.filter(x => x.prerelease === 'True');
    }
    if (installs.length > 0) {
        return installs[0];
    }
    return findVsByStandardPath();
}`;

if (!content.includes(search)) {
  process.exit(0);
}

content = content.replace(search, replace);
fs.writeFileSync(targetPath, content);
console.log('patch-vsInstalls: applied VS fallback');
