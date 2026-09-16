// Real CLI invocations (review-02 R1): realpath, the macOS /tmp -> /private/tmp
// alias, and a node_modules/.bin-style symlink executed through its shebang with
// the pinned Node first on PATH. Accepting lanes must exit 0 with a report;
// refusing lanes must exit 1 with a report; usage errors must exit 2 with no stdout.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const top = fs.realpathSync(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..'));
const tmpAlias = top.replace(/^\/private\/tmp\//, '/tmp/');
if (tmpAlias === top || fs.realpathSync(tmpAlias) !== top) throw new Error('expected the checker under /private/tmp with a /tmp alias');
const { baseFiles, baseLanes, writeTree } = await import(path.join(top, 'baseline/subject-02-trial/harness/fixture.mjs'));
const { laneRecordFor } = await import('./adapter.mjs');

const label = process.env.OPENSIP_BOUNDARY_TEST_LABEL ?? 'cli';
const checkerBin = fs.realpathSync(process.env.OPENSIP_BOUNDARY_CHECKER ?? path.join(top, 'checker/bin/check-boundary.mjs'));
const work = path.join(top, 'work', 'cli-' + label);
fs.rmSync(work, { recursive: true, force: true });
const tmp = path.join(top, 'work', 'tmp');
fs.mkdirSync(tmp, { recursive: true });
const nodeDir = path.dirname(process.execPath);
const env = { ...process.env, TMPDIR: tmp, PATH: `${nodeDir}:/usr/bin:/bin` };

function fixture(name, files) {
  const root = path.join(work, name, 'root');
  writeTree(root, baseFiles());
  writeTree(root, files);
  const { record } = laneRecordFor(root, baseLanes(), 'report');
  const recordFile = path.join(work, name, 'lane-record.json');
  fs.writeFileSync(recordFile, JSON.stringify(record));
  return { root, recordFile };
}
const accepting = fixture('accepting', {});
const refusing = fixture('refusing', { 'apps/report/src/help-view.ts': 'import { name } from "compiler-api";\nexport const n = name;\nexport function help(): string {\n  return "help";\n}\n' });

const binDir = path.join(work, 'node_modules', '.bin');
fs.mkdirSync(binDir, { recursive: true });
const binLink = path.join(binDir, 'check-boundary');
fs.symlinkSync(path.relative(binDir, checkerBin), binLink);

const entries = [
  ['node-realpath', process.execPath, [checkerBin]],
  ['node-tmp-alias', process.execPath, [checkerBin.replace(top, tmpAlias)]],
  ['bin-symlink-exec', binLink, []],
  ['bin-symlink-exec-tmp-alias', binLink.replace(top, tmpAlias), []],
  // The resolver flag given up front skips the re-exec, so argv[1] stays the symlinked path.
  ['node-flag-tmp-alias', process.execPath, ['--experimental-import-meta-resolve', '--no-warnings', checkerBin.replace(top, tmpAlias)]],
  ['node-flag-bin-symlink', process.execPath, ['--experimental-import-meta-resolve', '--no-warnings', binLink]],
];
const lanes = (f, alias) => ['--root', alias ? f.root.replace(top, tmpAlias) : f.root, '--lane-record', f.recordFile, '--design-lock', path.join(top, 'inputs/product/design-lock.json'), '--architecture', path.join(top, 'inputs/architecture')];

const rows = [];
for (const [name, command, prefix] of entries) {
  const alias = name.includes('tmp-alias');
  for (const [scenario, args, expectStatus, expectPassed] of [
    ['accepting-lane', lanes(accepting, alias), 0, true],
    ['refusing-lane', lanes(refusing, alias), 1, false],
    ['no-arguments', [], 2, null],
    ['duplicate-flag', ['--root', accepting.root, '--root', accepting.root], 2, null],
  ]) {
    const child = spawnSync(command, [...prefix, ...args], { encoding: 'utf8', env });
    // A failed exec (for example a missing execute bit) supplies no stdout.
    // Record the real spawn failure and refuse; do not mask it with TypeError.
    const stdout = typeof child.stdout === 'string' ? child.stdout : '';
    const stderr = typeof child.stderr === 'string' ? child.stderr : '';
    const spawnError = child.error ? { code: child.error.code ?? null, message: child.error.message } : null;
    let report = null;
    try { report = JSON.parse(stdout); } catch { /* usage errors print nothing */ }
    const ok = !child.error && child.status === expectStatus && (expectPassed === null ? stdout === '' : report?.passed === expectPassed);
    rows.push({ invocation: name, command: command === process.execPath ? 'node ' + prefix[0] : command, scenario, status: child.status, expectStatus, passed: report?.passed ?? null, stdoutBytes: stdout.length, stderr: stderr.slice(0, 200), spawnError, ok });
    process.stdout.write(`${ok ? 'ok  ' : 'FAIL'} ${name.padEnd(28)} ${scenario.padEnd(16)} exit=${child.status} passed=${report?.passed ?? '-'} spawn=${spawnError?.code ?? '-'}\n`);
  }
}
fs.mkdirSync(path.join(top, 'results'), { recursive: true });
fs.writeFileSync(path.join(top, label === 'cli' ? 'results/cli-invocation.json' : `work/cli-${label}/cli-invocation.json`), JSON.stringify({ schemaVersion: 1, tmpAlias, realpath: top, rows, allOk: rows.every(r => r.ok) }, null, 2) + '\n');
process.exitCode = rows.every(r => r.ok) ? 0 : 1;
