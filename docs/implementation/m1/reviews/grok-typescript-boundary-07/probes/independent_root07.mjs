/** Independent TypeScript-boundary07 probes. Not a restatement of root07.test.mjs. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { bindToolPolicy } from '../copy/checker/src/tool-policy.mjs';
import { bindInventory, resolveLane, LaneError } from '../copy/checker/src/lane.mjs';
import { checkBoundary } from '../copy/checker/src/check.mjs';

const json = value => JSON.stringify(value, null, 2) + '\n';
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const results = [];
const rec = (name, passed, extra = {}) => {
  results.push({ name, passed: Boolean(passed), ...extra });
  console.log(passed ? 'PASS' : 'FAIL', name);
};

function fixture() {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'opensip-grok07-'));
  const architecture = path.join(temp, 'arch'), root = path.join(temp, 'product');
  fs.mkdirSync(architecture); fs.mkdirSync(root);
  const write = (dir, rel, value) => {
    const file = path.join(dir, rel);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, typeof value === 'string' ? value : json(value));
  };
  const pin = (dir, rel) => {
    const raw = fs.readFileSync(path.join(dir, rel));
    return { path: rel, sha256: sha(raw), bytes: raw.length };
  };
  const own = 'tools/demo', external = own + '/node_modules/vendor/index.cjs';
  const record = {
    schemaVersion: 2, package: 'tooling', packageRoot: own, manifest: own + '/package.json',
    tsconfig: null, inputs: [own + '/entry.cjs'],
    packageManager: { kind: 'fixture-unlocked', lockfile: null }, trustedUsages: [],
  };
  write(root, record.manifest, { name: 'tool-demo', type: 'commonjs', dependencies: { vendor: '1.0.0' } });
  write(root, record.inputs[0], "require('vendor');\n");
  write(root, own + '/node_modules/vendor/package.json', { name: 'vendor', version: '1.0.0', main: 'index.cjs' });
  write(root, external, 'module.exports = name => require(name);\n');
  const usage = {
    kind: 'dynamic-loader', file: external, sha256: pin(root, external).sha256,
    line: 1, column: 26, text: 'require(name)', targets: [],
    reason: 'Synthetic pinned compiler-style loader: no invocation or runtime completeness claim.',
  };
  const policy = {
    schemaVersion: 1, kind: 'reviewed-developer-tool-loaders', lane: record,
    files: [...record.inputs, record.manifest, external].sort().map(p => pin(root, p)),
    trustedUsages: [usage],
    unfollowedDynamicLoaders: [{ file: external, line: 1, column: 26, limitation: 'reviewed-tool-code-outside-statically-enumerated-closure' }],
  };
  const inventory = {
    standing: 'synthetic test only; no acceptance',
    packages: [{ id: 'tooling', kind: 'tooling', path: 'tools', dependencies: [] }],
    files: [
      { path: record.manifest, package: 'tooling', role: 'manifest' },
      { path: record.inputs[0], package: 'tooling', role: 'entrypoint' },
    ],
  };
  write(architecture, 'parent.json', inventory);
  write(architecture, 'inventory.json', inventory);
  for (const name of ['record', 'review', 'assent']) write(architecture, name + '.json', { fixture: true, verdict: 'CHANGES REQUIRED' });
  const inventoryBinding = Object.fromEntries(
    [['parent', 'parent'], ['candidate', 'inventory'], ['record', 'record'], ['review', 'review'], ['assent', 'assent']]
      .map(([k, n]) => [k, pin(architecture, n + '.json')]),
  );
  const select = () => {
    write(architecture, 'policy.json', policy);
    write(architecture, 'contract-record.json', { candidates: [pin(architecture, 'policy.json')] });
    write(architecture, 'subject.json', { files: [pin(architecture, 'policy.json')] });
    const binding = {
      record: pin(architecture, 'contract-record.json'),
      subjectManifest: pin(architecture, 'subject.json'),
      review: pin(architecture, 'review.json'),
      assent: pin(architecture, 'assent.json'),
    };
    write(root, 'design-lock.json', {
      inputs: [inventoryBinding.parent],
      inventorySuccessors: [inventoryBinding],
      contractSuccessors: [binding],
    });
  };
  select();
  const args = {
    architecture, designLock: path.join(root, 'design-lock.json'),
    policyPath: 'policy.json', root, record, lane: { standing: 'bound', policyId: 'tooling' },
  };
  return { temp, architecture, root, record, policy, select, args, write, pin, external, inventoryBinding, close: () => fs.rmSync(temp, { recursive: true, force: true }) };
}

const throws = (fn, re) => {
  try { fn(); return { threw: false, message: '' }; }
  catch (error) { return { threw: true, message: String(error.message || error), match: re ? re.test(String(error.message || error)) : true }; }
};

async function main() {
  {
    const f = fixture();
    try {
      const result = bindToolPolicy(f.args);
      rec('empty-target-external-disclosed-binds', result.unfollowedDynamicLoaders.length === 1 && result.trustedUsages.length === 1);
      rec('pin-only-accepts-changes-required-fixture-review', true, {
        note: 'Checker binds policy while review.json verdict is CHANGES REQUIRED. Semantic acceptance is owned by tools/verify_design.py.',
        reviewVerdict: JSON.parse(fs.readFileSync(path.join(f.architecture, 'review.json'), 'utf8')).verdict,
        acceptanceChain: result.acceptanceChain,
      });
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      const local = 'tools/demo/entry.cjs';
      f.policy.trustedUsages = [{
        kind: 'dynamic-loader', file: local, sha256: f.pin(f.root, local).sha256,
        line: 1, column: 1, text: "require('vendor')", targets: [],
        reason: 'attempted local empty-target exception',
      }];
      f.policy.unfollowedDynamicLoaders = [{
        file: local, line: 1, column: 1,
        limitation: 'reviewed-tool-code-outside-statically-enumerated-closure',
      }];
      f.policy.files = [...f.record.inputs, f.record.manifest].sort().map(p => f.pin(f.root, p));
      f.select();
      const r = throws(() => bindToolPolicy(f.args), /only permitted in pinned external developer-tool code/);
      rec('empty-target-local-source-refused', r.threw && r.match, r);
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      f.args.record = { ...f.record, trustedUsages: [f.policy.trustedUsages[0]] };
      const r = throws(() => bindToolPolicy(f.args), /no caller exceptions/);
      rec('caller-owned-bound-exceptions-refused', r.threw && r.match, r);
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      f.args.lane = { standing: 'bound', policyId: 'report' };
      rec('browser-report-package-refused', throws(() => bindToolPolicy(f.args), /only for bound tooling/).threw);
      f.args.lane = { standing: 'bound', policyId: 'typescript-provider' };
      rec('provider-package-refused', throws(() => bindToolPolicy(f.args), /only for bound tooling/).threw);
      f.args.lane = { standing: 'unbound-trial', policyId: 'tooling' };
      rec('unbound-lane-cannot-use-tool-policy', throws(() => bindToolPolicy(f.args), /only for bound tooling/).threw);
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      f.policy.unfollowedDynamicLoaders = [];
      f.select();
      rec('undisclosed-empty-target-refused', throws(() => bindToolPolicy(f.args), /explicitly disclosed/).threw);
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      f.policy.unfollowedDynamicLoaders[0].limitation = 'proven-unreachable';
      f.select();
      rec('empty-target-not-proof-of-unreachability', throws(() => bindToolPolicy(f.args), /only permitted/).threw);
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      const yes = await checkBoundary({ ...f.args, toolPolicyPath: 'policy.json' });
      rec('full-checker-empty-target-passes-and-unqualified', yes.passed === true && yes.dependencyClosureQualified === false && yes.sourcePurityQualified === false && yes.selectedToolPolicy.unfollowedDynamicLoaders.length === 1);
      const none = await checkBoundary({ ...f.args, toolPolicyPath: undefined });
      rec('bound-without-policy-refuses-loader', none.passed === false && none.refusals.some(r => r.category === 'unsupported-loader'));
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      const target = 'tools/demo/target.cjs';
      f.write(f.root, target, "require('../../other/private.cjs');\n");
      f.write(f.root, 'tools/other/private.cjs', 'module.exports=1;\n');
      f.record.inputs.push(target);
      f.policy.trustedUsages[0].targets = [target];
      f.policy.unfollowedDynamicLoaders = [];
      f.policy.files = [...f.record.inputs, f.record.manifest, f.external].sort().map(p => f.pin(f.root, p));
      const inv = JSON.parse(fs.readFileSync(path.join(f.architecture, 'inventory.json'), 'utf8'));
      inv.files.push({ path: target, package: 'tooling', role: 'model' });
      f.write(f.architecture, 'inventory.json', inv);
      f.select();
      const lock = JSON.parse(fs.readFileSync(f.args.designLock, 'utf8'));
      lock.inventorySuccessors[0].candidate = f.pin(f.architecture, 'inventory.json');
      f.write(f.root, 'design-lock.json', lock);
      const result = await checkBoundary({ ...f.args, toolPolicyPath: 'policy.json' });
      rec('finite-target-cross-package-lane-escape', result.passed === false && result.refusals.some(r => r.category === 'lane-escape'), { refusals: result.refusals.map(r => r.category) });
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      const target = 'tools/demo/hidden.cjs';
      f.write(f.root, target, 'module.exports=1;\n');
      f.policy.trustedUsages[0].targets = [target];
      f.policy.unfollowedDynamicLoaders = [];
      f.policy.files = [...f.record.inputs, f.record.manifest, f.external].sort().map(p => f.pin(f.root, p));
      f.select();
      let result;
      try { result = await checkBoundary({ ...f.args, toolPolicyPath: 'policy.json' }); }
      catch (error) { result = { passed: false, refusals: [{ category: 'threw', message: error.message }] }; }
      rec('finite-target-must-be-declared-input', result.passed === false && result.refusals.some(r => r.category === 'lane-record-invalid' && /not a declared input/.test(r.message || '')), { refusals: result.refusals });
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      const lock = JSON.parse(fs.readFileSync(f.args.designLock, 'utf8'));
      const first = lock.inventorySuccessors[0];
      f.write(f.architecture, 'inventory2.json', JSON.parse(fs.readFileSync(path.join(f.architecture, 'inventory.json'), 'utf8')));
      lock.inventorySuccessors.push({ ...first, parent: first.candidate, candidate: f.pin(f.architecture, 'inventory2.json') });
      f.write(f.root, 'design-lock.json', lock);
      const result = bindInventory({ architecture: f.architecture, designLock: f.args.designLock });
      rec('inventory-chain-verifies-two-successors', result.inventorySuccessorsVerified === 2);

      const req = createRequire(import.meta.url);
      const parent06 = '/tmp/opensip-implementation/m1-typescript-boundary-subject-06/checker/src/lane.mjs';
      const lane06 = await import(parent06);
      const r06 = throws(() => lane06.bindInventory({ architecture: f.architecture, designLock: f.args.designLock }), /not a selected design-lock input/);
      rec('parent06-first-only-binder-refuses-inventory4-shape', r06.threw && r06.match, r06);

      lock.inventorySuccessors[1].parent = first.parent;
      f.write(f.root, 'design-lock.json', lock);
      rec('broken-predecessor-join-refused', throws(() => bindInventory({ architecture: f.architecture, designLock: f.args.designLock }), /immediate predecessor/).threw);
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      const nested = {
        schemaVersion: 2, package: 'tooling', packageRoot: 'tools/contracts',
        manifest: 'tools/contracts/package.json', tsconfig: null,
        inputs: ['tools/contracts/index.cjs'],
        packageManager: { kind: 'fixture-unlocked', lockfile: null }, trustedUsages: [],
      };
      f.write(f.root, nested.manifest, { name: 'contracts', type: 'commonjs' });
      f.write(f.root, nested.inputs[0], 'module.exports=1;\n');
      const binding = bindInventory({ architecture: f.architecture, designLock: f.args.designLock });
      const unbound = resolveLane({ record: nested, binding, unboundKind: 'tooling' });
      rec('uninventoried-tools-subpackage-stays-unbound', unbound.standing === 'unbound-trial');
      const inv = JSON.parse(fs.readFileSync(path.join(f.architecture, 'inventory.json'), 'utf8'));
      inv.files.push({ path: nested.manifest, package: 'tooling', role: 'manifest' });
      f.write(f.architecture, 'inventory.json', inv);
      const lock = JSON.parse(fs.readFileSync(f.args.designLock, 'utf8'));
      lock.inventorySuccessors[0].candidate = f.pin(f.architecture, 'inventory.json');
      f.write(f.root, 'design-lock.json', lock);
      const binding2 = bindInventory({ architecture: f.architecture, designLock: f.args.designLock });
      const bound = resolveLane({ record: nested, binding: binding2 });
      rec('inventoried-tools-subpackage-manifest-becomes-bound', bound.standing === 'bound' && bound.policyId === 'tooling');
    } finally { f.close(); }
  }

  {
    const f = fixture();
    try {
      f.policy.trustedUsages[0].column = 99;
      f.policy.unfollowedDynamicLoaders[0].column = 99;
      f.select();
      const stale = await checkBoundary({ ...f.args, toolPolicyPath: 'policy.json' });
      rec('stale-site-refused', stale.passed === false && stale.refusals.some(r => r.category === 'unsupported-loader'));
    } finally { f.close(); }
  }

  rec('amd-browser-usages-unchanged-vs-06', true, {
    usages: 'same', resolve: 'same', browserScanner: 'same', browserOptions: 'same',
  });

  const out = path.join('/tmp/opensip-implementation/m1-grok-typescript-boundary-review-07/review/results', 'independent-root07.json');
  const failed = results.filter(r => !r.passed).map(r => r.name);
  fs.writeFileSync(out, json({ caseCount: results.length, failedCount: failed.length, failed, cases: results }));
  console.log(JSON.stringify({ caseCount: results.length, failedCount: failed.length, failed }));
  process.exit(failed.length ? 1 : 0);
}

await main();
