// Independent TS assembly join probes against assemble_ts.cjs.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {spawnSync} = require('node:child_process');
const COPY = '/tmp/opensip-implementation/m1-grok-native-integration-review-02/review/copy';
const NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node';
const BASE = '/tmp/opensip-implementation/m1-report-codec-candidate-02/output04';
const NATIVE = path.join(COPY, 'output-c');
const SCRIPT = path.join(COPY, 'assemble_ts.cjs');
const RESULTS = '/tmp/opensip-implementation/m1-grok-native-integration-review-02/review/results';

function run(nativeDir, outDir) {
  fs.rmSync(outDir, {recursive: true, force: true});
  fs.mkdirSync(outDir, {recursive: true});
  const r = spawnSync(NODE, [SCRIPT, BASE, nativeDir, outDir], {encoding: 'utf8'});
  return {status: r.status, stdout: (r.stdout || '').trim(), stderr: (r.stderr || '').trim()};
}

const rows = [];
function rec(name, passed, detail) {
  rows.push({name, passed: !!passed, ...detail});
  console.log((passed ? 'PASS' : 'FAIL'), name);
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'asm-'));
const good = run(NATIVE, path.join(tmp, 'good'));
rec('baseline-assembly-exits-0', good.status === 0, {stdout: good.stdout, stderr: good.stderr.slice(0, 300)});
let counts = {};
try { counts = JSON.parse(good.stdout); } catch (e) { counts = {}; }
rec('baseline-counts-30-12-70', counts.providerNative === 30 && counts.providerExternal === 12 && counts.reportNative === 70, counts);

const report = fs.readFileSync(path.join(BASE, 'apps/report/src/generated/report.ts'), 'utf8');
const collide = 'Baseline2Root';
const nativeDir = path.join(tmp, 'native-collide');
fs.cpSync(NATIVE, nativeDir, {recursive: true});
let wire = fs.readFileSync(path.join(nativeDir, 'wire.ts'), 'utf8');
wire += '\nexport type ' + collide + ' = string;\n';
fs.writeFileSync(path.join(nativeDir, 'wire.ts'), wire);
const hit = run(nativeDir, path.join(tmp, 'out-collide'));
rec('native-type-colliding-with-report-name-refuses', hit.status !== 0 && /native name collision|duplicate native/.test(hit.stderr + hit.stdout), {status: hit.status, stderr: (hit.stderr + hit.stdout).slice(0, 400)});

const nativeDup = path.join(tmp, 'native-dup');
fs.cpSync(NATIVE, nativeDup, {recursive: true});
let w2 = fs.readFileSync(path.join(nativeDup, 'wire.ts'), 'utf8');
const m = w2.match(/export (?:type|interface) (Ts2[A-Za-z0-9]+)/);
if (!m) rec('duplicate-native-declaration-refuses', false, {reason: 'no Ts2 name'});
else {
  w2 += '\nexport type ' + m[1] + ' = number;\n';
  fs.writeFileSync(path.join(nativeDup, 'wire.ts'), w2);
  const r = run(nativeDup, path.join(tmp, 'out-dup'));
  rec('duplicate-native-declaration-refuses', r.status !== 0 && /duplicate native declaration/.test(r.stderr + r.stdout), {status: r.status, stderr: (r.stderr + r.stdout).slice(0, 400), name: m[1]});
}

const nativeUnresolved = path.join(tmp, 'native-unresolved');
fs.cpSync(NATIVE, nativeUnresolved, {recursive: true});
let w3 = fs.readFileSync(path.join(nativeUnresolved, 'wire.ts'), 'utf8');
w3 += '\nexport type Ts2OrphanProbe = Ts2DoesNotExist;\n';
fs.writeFileSync(path.join(nativeUnresolved, 'wire.ts'), w3);
const r3 = run(nativeUnresolved, path.join(tmp, 'out-unresolved'));
rec('unresolved-native-type-refuses', r3.status !== 0 && /unresolved native type/.test(r3.stderr + r3.stdout), {status: r3.status, stderr: (r3.stderr + r3.stdout).slice(0, 400)});

const out = {standing: 'Independent assemble_ts.cjs join probes', passed: rows.every(r => r.passed), caseCount: rows.length, failed: rows.filter(r => !r.passed).map(r => r.name), checks: rows};
fs.writeFileSync(path.join(RESULTS, 'independent-assembly.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify({passed: out.passed, caseCount: out.caseCount, failed: out.failed}));
process.exit(out.passed ? 0 : 1);
