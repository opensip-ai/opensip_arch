// Preserve the accepted regression harness in a disposable directory. The
// product tree uses stable category names; historical aliases are fixture-only.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
if (process.platform !== 'darwin' || process.version !== 'v24.16.0') {
  throw new Error('This developer regression profile requires macOS and Node v24.16.0; other platform qualification is separate.');
}
const staging = fs.realpathSync(fs.mkdtempSync(path.join('/tmp', 'opensip-boundary-tests-')));
let status = 1;
try {
  fs.mkdirSync(path.join(staging, 'checker'));
  fs.mkdirSync(path.join(staging, 'results'));
  for (const name of ['src', 'bin']) fs.cpSync(path.join(root, name), path.join(staging, 'checker', name), {recursive:true});
  for (const name of ['package.json', 'package-lock.json']) fs.copyFileSync(path.join(root, name), path.join(staging, 'checker', name));
  // Already provisioned compiler/bundler packages, never an install during tests.
  fs.symlinkSync(path.join(root, 'node_modules'), path.join(staging, 'checker/node_modules'), 'dir');
  const mapping = JSON.parse(fs.readFileSync(path.join(root, 'tests/fixtures/staging-map.json'), 'utf8'));
  const targets = new Set();
  for (const row of mapping.files) {
    for (const value of [row.path, row.stagePath]) {
      if (!value || path.isAbsolute(value) || value.includes('\\') || value.split('/').some(p => !p || p === '.' || p === '..')) throw new Error('Invalid fixture path');
    }
    if (targets.has(row.stagePath)) throw new Error('Duplicate fixture target');
    targets.add(row.stagePath);
    const raw = fs.readFileSync(path.join(root, row.path));
    if (raw.length !== row.bytes || crypto.createHash('sha256').update(raw).digest('hex') !== row.sha256) throw new Error('Fixture source differs: '+row.path);
    const dest = path.join(staging, row.stagePath);
    fs.mkdirSync(path.dirname(dest), {recursive:true});
    fs.writeFileSync(dest, raw);
  }
  const tests = mapping.files.filter(row => row.stagePath.startsWith('checker/test/')).map(row => path.join(staging, row.stagePath));
  const result = spawnSync(process.execPath, ['--experimental-import-meta-resolve', '--no-warnings', '--test', '--test-concurrency=1', ...tests], {
    cwd:staging, stdio:'inherit', timeout:300_000,
    env:{...process.env, OPENSIP_BOUNDARY_CHECKER:path.join(staging,'checker/bin/check-boundary.mjs'), OPENSIP_BOUNDARY_TEST_LABEL:'product'},
  });
  if (result.error) console.error(result.error.message);
  status = result.status ?? 1;
} finally {
  fs.rmSync(staging, {recursive:true,force:true});
}
process.exitCode = status;
