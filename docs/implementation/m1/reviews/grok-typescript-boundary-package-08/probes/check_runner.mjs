/** Focused packaging-runner controls. Does not restage the 224-case catalog. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const review = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const pkg = path.join(review, 'copy/tools/typescript-boundary');
const outDir = path.join(review, 'results');
const rows = [];
const check = (name, passed, detail = '') => {
  rows.push({name, passed: Boolean(passed), detail: String(detail).slice(0, 500)});
  console.log(passed ? 'PASS' : 'FAIL', name, String(detail).slice(0, 180));
};

const mapping = JSON.parse(fs.readFileSync(path.join(pkg, 'tests/fixtures/staging-map.json'), 'utf8'));
const tests = mapping.files.filter((r) => r.path.startsWith('tests/') && !r.path.includes('/support/') && !r.path.includes('/fixtures/'));
const helpers = mapping.files.filter((r) => r.path.includes('/support/'));
const fixtures = mapping.files.filter((r) => r.path.includes('/fixtures/') && r.path !== 'tests/fixtures/staging-map.json');
check('map-5-tests-10-helpers-9-fixtures', tests.length === 5 && helpers.length === 10 && fixtures.length === 9, JSON.stringify({tests: tests.length, helpers: helpers.length, fixtures: fixtures.length}));
const targets = mapping.files.map((r) => r.stagePath);
check('map-stagepaths-unique', new Set(targets).size === targets.length);
check('map-no-absolute-or-dotdot', mapping.files.every((r) => [r.path, r.stagePath].every((v) => v && !path.isAbsolute(v) && !v.includes('\\') && !v.split('/').some((p) => !p || p === '.' || p === '..'))));
const adapted = mapping.files.filter((r) => r.upstreamSha256);
check('two-execpath-adaptations', adapted.length === 2 && adapted.every((r) => r.adaptation && r.path.includes('support/') && fs.readFileSync(path.join(pkg, r.path), 'utf8').includes('process.execPath') && !fs.readFileSync(path.join(pkg, r.path), 'utf8').includes('/Users/')));

const runner = fs.readFileSync(path.join(pkg, 'tests/run.mjs'), 'utf8');
check('runner-mkdir-results', runner.includes("mkdirSync(path.join(staging, 'results'))"));
check('runner-tmp-not-ostmpdir', runner.includes("path.join('/tmp'") && !runner.includes('os.tmpdir()'));
check('runner-import-meta-resolve-flag', runner.includes('--experimental-import-meta-resolve'));
check('runner-finally-rmSync', runner.includes('finally') && runner.includes('rmSync(staging'));
check('runner-exitCode-from-status', runner.includes('process.exitCode = status') && runner.includes('result.status ?? 1'));

// Failure propagation: spawn a node --test that fails; runner-equivalent status mapping.
const failDir = fs.mkdtempSync(path.join('/tmp', 'opensip-boundary-failprop-'));
try {
  fs.writeFileSync(path.join(failDir, 'fail.test.mjs'), "import {test} from 'node:test'; test('x', () => { throw new Error('boom'); });\n");
  const result = spawnSync(process.execPath, ['--test', path.join(failDir, 'fail.test.mjs')], {encoding: 'utf8'});
  const status = result.status ?? 1;
  check('spawnSync-failed-test-nonzero', status !== 0, String(status));
} finally {
  fs.rmSync(failDir, {recursive: true, force: true});
}

// Cleanup: stage like the runner, then rmSync; directory must vanish even after throw.
const staging = fs.realpathSync(fs.mkdtempSync(path.join('/tmp', 'opensip-boundary-tests-')));
let cleaned = false;
try {
  fs.mkdirSync(path.join(staging, 'results'));
  fs.writeFileSync(path.join(staging, 'marker'), 'x');
  throw new Error('forced');
} catch {
  /* expected */
} finally {
  fs.rmSync(staging, {recursive: true, force: true});
  cleaned = !fs.existsSync(staging);
}
check('staging-removed-after-throw', cleaned, staging);

const leftover = fs.readdirSync('/tmp').filter((n) => n.startsWith('opensip-boundary-tests-') || n.startsWith('opensip-boundary-failprop-'));
check('no-control-staging-leftover', leftover.length === 0, leftover.join(','));

const failed = rows.filter((r) => !r.passed).map((r) => r.name);
fs.writeFileSync(path.join(outDir, 'runner-controls.json'), JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed, cases: rows}, null, 2) + '\n');
console.log(JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed}));
if (failed.length) process.exitCode = 1;
