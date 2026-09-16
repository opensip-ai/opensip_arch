// Runs every case against the dependency-cruiser candidate and the reference
// copy, each in a fresh child process, from the same verified positive payload.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import ts from 'typescript';
import { baseFiles, baseLanes, writeTree, treeDigest } from './fixture.mjs';
import { cases } from './cases.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const trial = path.resolve(here, '..');
const node = process.execPath;
const work = path.join(trial, 'work', 'matrix');
const only = process.argv[2] ? new RegExp(process.argv[2]) : null;

const REFERENCE_CATEGORY = [
  [/forbidden internal TS edge|cross-package source|relative module escapes|triple-slash reference crosses/, 'lane-escape'],
  [/resolved local module missing from declared inputs|compiler discovered undeclared local input/, 'undeclared-local'],
  [/config source missing from declared inputs/, 'config-include'],
  [/unresolved module request|unresolved type-reference/, 'unresolved'],
  [/external module is not declared|ambient type dependency is not declared/, 'undeclared-external'],
  [/shadows a local package/, 'local-name-shadow'],
  [/browser source/, 'browser-node'],
  [/nonliteral|computed|alias|createRequire/, 'unsupported-loader'],
  [/syntax is not supported/, 'parse-failure'],
  [/symlink/, 'symlink'],
  [/configuration reads another package/, 'config-owner'],
  [/selected package manifest is required/, 'manifest-missing'],
  [/invalid TS config/, 'config-invalid'],
];
const referenceCategory = message => REFERENCE_CATEGORY.find(([re]) => re.test(message))?.[1] ?? 'other';

function grade(testCase, passed, categories) {
  if (testCase.expect === 'accept') return passed ? 'correct' : 'false-refusal';
  if (passed) return 'missed';
  return categories.some(c => testCase.refuse.includes(c)) ? 'correct' : 'wrong-reason';
}

function syntaxHygiene(root, files) {
  const names = Object.entries(files ?? {}).filter(([n, v]) => typeof v === 'string' && /\.(?:[cm]?[jt]sx?)$/.test(n) && !n.endsWith('.d.ts') && !n.endsWith('.d.mts') && !n.endsWith('.d.cts')).map(([n]) => path.join(root, n));
  if (!names.length) return [];
  const program = ts.createProgram(names, { allowJs: true, noResolve: true, noLib: true, types: [], noEmit: true, module: ts.ModuleKind.NodeNext, moduleResolution: ts.ModuleResolutionKind.NodeNext });
  return program.getSyntacticDiagnostics().map(d => path.relative(root, d.file.fileName) + ': ' + ts.flattenDiagnosticMessageText(d.messageText, '\n'));
}

function nodeOracle(root, probes) {
  return (probes ?? []).map(({ from, request }) => {
    const script = `try { console.log(JSON.stringify({ resolved: require('node:module').createRequire(process.argv[1]).resolve(process.argv[2]) })) } catch (e) { console.log(JSON.stringify({ error: e.code })) }`;
    const out = JSON.parse(execFileSync(node, ['-e', script, path.join(root, from), request], { encoding: 'utf8' }));
    return { from, request, mode: 'require', ...(out.resolved ? { resolved: path.relative(root, out.resolved) } : out) };
  });
}

fs.rmSync(work, { recursive: true, force: true });
fs.mkdirSync(work, { recursive: true });
const controlRoot = path.join(work, 'control');
writeTree(controlRoot, baseFiles());
const controlDigest = treeDigest(controlRoot);
const controlHygiene = syntaxHygiene(controlRoot, baseFiles());
if (controlHygiene.length) throw new Error('positive payload has syntax diagnostics: ' + controlHygiene.join('; '));

const results = [];
for (const testCase of cases.filter(c => !only || only.test(c.id))) {
  const dir = path.join(work, testCase.id);
  const root = path.join(dir, 'root');
  writeTree(root, baseFiles());
  const payloadDigest = treeDigest(root);
  if (payloadDigest !== controlDigest) throw new Error(testCase.id + ': pre-mutation payload differs from control');
  writeTree(root, testCase.files ?? {});
  const lanes = baseLanes();
  testCase.lanes?.(lanes);
  const lanesFile = path.join(dir, 'lanes.json');
  fs.writeFileSync(lanesFile, JSON.stringify(lanes, null, 2) + '\n');
  const hygiene = syntaxHygiene(root, testCase.files);
  const fixtureValid = testCase.expectSyntaxError ? hygiene.length > 0 : hygiene.length === 0;

  let started = process.hrtime.bigint();
  const c = spawnSync(node, [path.join(trial, 'candidate/check-lane.mjs'), '--root', root, '--lanes', lanesFile, '--lane', testCase.lane], { encoding: 'utf8', cwd: trial });
  const candidateMs = Number(process.hrtime.bigint() - started) / 1e6;
  let candidate;
  try { candidate = JSON.parse(c.stdout); } catch { candidate = { passed: false, refusals: [{ source: 'harness', category: 'tool-error', message: (c.stderr || 'no output').slice(0, 400) }], graphs: [] }; }
  const all = candidate.refusals.map(r => r.category);
  const depcruiseOnly = candidate.refusals.filter(r => r.source === 'depcruise').map(r => r.category);

  started = process.hrtime.bigint();
  const r = spawnSync(node, [path.join(here, 'run-reference.cjs'), root, testCase.lane, lanesFile], { encoding: 'utf8', cwd: trial });
  const referenceMs = Number(process.hrtime.bigint() - started) / 1e6;
  const reference = JSON.parse(r.stdout);
  const refCategories = reference.passed ? [] : [referenceCategory(reference.message)];

  const row = {
    id: testCase.id, lane: testCase.lane, requirement: testCase.requirement,
    expected: testCase.expect === 'accept' ? 'accept' : { refuse: testCase.refuse },
    fixture: { payloadDigest, mutated: Object.keys(testCase.files ?? {}), syntaxDiagnostics: hygiene, valid: fixtureValid },
    oracle: nodeOracle(root, testCase.nodeOracle),
    depcruiseOnly: { passed: depcruiseOnly.length === 0, categories: [...new Set(depcruiseOnly)], grade: grade(testCase, depcruiseOnly.length === 0, depcruiseOnly) },
    candidate: { passed: candidate.passed, categories: [...new Set(all)], grade: grade(testCase, candidate.passed, all), refusals: candidate.refusals, milliseconds: Math.round(candidateMs) },
    reference: { passed: reference.passed, categories: refCategories, grade: grade(testCase, reference.passed, refCategories), message: reference.message, milliseconds: Math.round(referenceMs) },
    edges: (candidate.graphs ?? []).map(g => ({ graph: g.graph, group: g.name, conditions: g.conditions, edges: g.edges.map(e => `${e.from} -> ${e.module} => ${e.resolved} [${e.dependencyTypes.join(',')}]`) })),
  };
  results.push(row);
  process.stdout.write(`${row.id.padEnd(38)} fixture:${fixtureValid ? 'ok ' : 'BAD'} depcruise-only:${row.depcruiseOnly.grade.padEnd(13)} candidate:${row.candidate.grade.padEnd(13)} reference:${row.reference.grade.padEnd(13)} ${row.candidate.categories.join(',')} | ${row.reference.categories.join(',')}\n`);
}

const summary = {};
for (const tool of ['depcruiseOnly', 'candidate', 'reference']) {
  summary[tool] = {};
  for (const row of results) summary[tool][row[tool].grade] = (summary[tool][row[tool].grade] ?? 0) + 1;
}
const out = path.join(trial, '..', 'results');
fs.mkdirSync(out, { recursive: true });
if (!only) {
  fs.writeFileSync(path.join(out, 'matrix.json'), JSON.stringify({
    schemaVersion: 1, standing: 'trial author evidence; not independent approval or qualification',
    node: process.version, typescript: ts.version, controlDigest, cases: results.length,
    invalidFixtures: results.filter(r => !r.fixture.valid).map(r => r.id), summary, results,
  }, null, 2) + '\n');
}
process.stdout.write(JSON.stringify(summary) + '\n');
