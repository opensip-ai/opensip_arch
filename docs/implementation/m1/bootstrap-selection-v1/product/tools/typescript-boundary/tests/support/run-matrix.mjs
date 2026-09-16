// Runs the author02 matrix (88), review-02 probes (46) and author-03 regression
// cases against the author-03 checker and the frozen author02 dependency-cruiser
// candidate, from the same shared positive payload. Node oracles run after both
// checkers and load only controlled fixture modules.
//
// usage: node run-cases.mjs [--only REGEX] [--candidates new,baseline] [--out FILE] [--sets author,reviewer,regression]
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const top = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);
const opt = name => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : undefined; };
const only = opt('--only') ? new RegExp(opt('--only')) : null;
const candidates = (opt('--candidates') ?? 'new,baseline').split(',');
const sets = (opt('--sets') ?? 'author,reviewer,regression').split(',');
const out = path.resolve(top, opt('--out') ?? 'results/cases.json');
const checkerBin = path.resolve(process.env.OPENSIP_BOUNDARY_CHECKER ?? path.join(top, 'checker/bin/check-boundary.mjs'));
const baselineChecker = path.join(top, 'baseline/subject-02-trial/candidate/check-lane.mjs');
const designLock = path.join(top, 'inputs/product/design-lock.json');
const tmp = path.join(top, 'work', 'tmp');
fs.mkdirSync(tmp, { recursive: true });
const env = { ...process.env, TMPDIR: tmp };
const scratch = path.join(top, 'work', 'cases', path.basename(out, '.json'));

const { baseFiles, baseLanes, writeTree } = await import(path.join(top, 'baseline/subject-02-trial/harness/fixture.mjs'));
const { cases: authorCases } = await import(path.join(top, 'baseline/subject-02-trial/harness/cases.mjs'));
const reviewer = await import('./reviewer-probes.generated.mjs');
const { regressionCases } = await import('./regression-cases.mjs');
const { laneRecordFor } = await import('./adapter.mjs');
const { expectationFor, grade } = await import('./expectations.mjs');

const catalog = [
  ...(sets.includes('author') ? authorCases.map(c => ['author', c]) : []),
  ...(sets.includes('reviewer') ? reviewer.probes.map(c => ['reviewer', c]) : []),
  ...(sets.includes('regression') ? regressionCases.map(c => ['regression', c]) : []),
].filter(([, c]) => !only || only.test(c.id));

function parseJson(text) { try { return JSON.parse(text); } catch { return null; } }
function timed(command, args) {
  const started = process.hrtime.bigint();
  const child = spawnSync(command, args, { encoding: 'utf8', env, maxBuffer: 256 * 1024 * 1024 });
  return { status: child.status, stdout: child.stdout, stderr: child.stderr.slice(0, 800), milliseconds: Math.round(Number(process.hrtime.bigint() - started) / 1e6), report: parseJson(child.stdout) };
}

fs.rmSync(scratch, { recursive: true, force: true });
const rows = [];
for (const [set, testCase] of catalog) {
  const dir = path.join(scratch, set, testCase.id);
  const root = path.join(dir, 'root');
  writeTree(root, baseFiles());
  writeTree(root, testCase.files ?? {});
  const lanes = baseLanes();
  testCase.lanes?.(lanes);
  const legacyFile = path.join(dir, 'legacy-lanes.json');
  fs.writeFileSync(legacyFile, JSON.stringify(lanes, null, 2) + '\n');
  const { record, unbound } = laneRecordFor(root, lanes, testCase.lane);
  testCase.recordEdit?.(record, root);
  const recordFile = path.join(dir, 'lane-record.json');
  fs.writeFileSync(recordFile, JSON.stringify(record, null, 2) + '\n');
  let architecture = path.join(top, 'inputs/architecture');
  if (testCase.architectureEdit) {
    const copy = path.join(dir, 'architecture');
    fs.cpSync(architecture, copy, { recursive: true, verbatimSymlinks: true });
    testCase.architectureEdit(copy);
    architecture = copy;
  }
  const expectation = expectationFor(set, testCase);
  const row = { set, id: testCase.id, lane: testCase.lane, why: testCase.why ?? testCase.requirement, expected: expectation.original, expectedForNew: expectation.forNew, revision: expectation.revision?.rationale };

  if (candidates.includes('new')) {
    const args = [checkerBin, '--root', root, '--lane-record', recordFile, '--design-lock', designLock, '--architecture', architecture,
      ...(unbound && !testCase.args?.includes('--unbound-lane') ? ['--unbound-lane', unbound] : []), ...(testCase.args ?? [])];
    const run = timed(process.execPath, args);
    row.new = { status: run.status, passed: run.report?.passed ?? null, grade: grade(expectation.forNew, run), categories: [...new Set((run.report?.refusals ?? []).map(r => r.category))],
      refusals: run.report?.refusals ?? [], trustedUsagesApplied: run.report?.trustedUsagesApplied ?? [], standing: run.report?.lane?.standing, stderr: run.stderr,
      milliseconds: run.milliseconds, checkerMilliseconds: run.report?.stats?.milliseconds, maxRssBytes: run.report?.stats?.maxRssBytes,
      edges: (run.report?.edges ?? []).map(e => `${e.graph}/${e.group ?? '-'} ${e.from}:${e.line ?? ''} -${e.mode ?? e.kind}-> ${e.request} => ${e.resolved ?? e.coreModule ?? (e.ignored ? 'ignored' : 'UNRESOLVED ' + (e.error ?? ''))}`) };
  }
  if (candidates.includes('baseline') && !testCase.newOnly) {
    const run = timed(process.execPath, [baselineChecker, '--root', root, '--lanes', legacyFile, '--lane', testCase.lane]);
    row.baseline = { status: run.status, passed: run.report?.passed ?? null, grade: grade(expectation.original, run, { legacy: true }), categories: [...new Set((run.report?.refusals ?? []).map(r => r.category))], milliseconds: run.milliseconds };
  }
  const oracles = [...(testCase.oracle ?? []), ...(testCase.nodeOracle ?? [])];
  if (oracles.length) {
    row.oracle = oracles.map(o => reviewer.nodeOracle(root, o.emit ? o : { mode: 'require', ...o }));
    row.oracleVerdict = row.oracle.some(o => o.error) ? 'node-fails' : 'node-loads';
    if (row.new) row.new.oracleAgrees = (row.oracleVerdict === 'node-loads') === (row.new.passed === true);
    if (row.baseline) row.baseline.oracleAgrees = (row.oracleVerdict === 'node-loads') === (row.baseline.passed === true);
  }
  rows.push(row);
  const mark = r => r ? `${r.grade}${r.oracleAgrees === false ? '!ORACLE' : ''}` : '-';
  process.stdout.write(`${(set + ':' + testCase.id).padEnd(66)} new:${mark(row.new).padEnd(22)} baseline:${mark(row.baseline).padEnd(22)} ${row.new?.categories.join(',') ?? ''}\n`);
}

const summary = {};
for (const row of rows) for (const candidate of ['new', 'baseline']) {
  if (!row[candidate]) continue;
  const bucket = (summary[candidate] ??= {})[row.set] ??= {};
  bucket[row[candidate].grade] = (bucket[row[candidate].grade] ?? 0) + 1;
}
const oracle = {};
for (const candidate of ['new', 'baseline']) {
  const withOracle = rows.filter(r => r[candidate] && r.oracle);
  oracle[candidate] = { rows: withOracle.length, agree: withOracle.filter(r => r[candidate].oracleAgrees).length, disagree: withOracle.filter(r => !r[candidate].oracleAgrees).map(r => `${r.set}:${r.id}`) };
}
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, JSON.stringify({ schemaVersion: 1, standing: 'author-03 comparison evidence; not independent review', node: process.version, checker: path.relative(top, checkerBin), summary, oracle, rows }, null, 2) + '\n');
process.stdout.write(JSON.stringify({ summary, oracle }) + '\n');
