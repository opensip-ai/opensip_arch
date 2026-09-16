// node --test suite for the proposed dependency-cruiser lane checker. Every
// case starts from the shared complete positive payload; refusals must carry
// an intended diagnostic category, not merely a nonzero exit.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { baseFiles, baseLanes, writeTree } from '../harness/fixture.mjs';
import { cases } from '../harness/cases.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const checker = process.env.OPENSIP_TRIAL_CHECKER ?? path.join(here, 'check-lane.mjs');
const scratch = path.join(here, '..', 'work', 'tests');

function run(t, { id, files, lanes: editLanes, lane }) {
  fs.mkdirSync(scratch, { recursive: true });
  const dir = fs.mkdtempSync(path.join(scratch, id + '-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const root = path.join(dir, 'root');
  writeTree(root, baseFiles());
  writeTree(root, files ?? {});
  const lanes = baseLanes();
  editLanes?.(lanes);
  const lanesFile = path.join(dir, 'lanes.json');
  fs.writeFileSync(lanesFile, JSON.stringify(lanes));
  const child = spawnSync(process.execPath, [checker, '--root', root, '--lanes', lanesFile, '--lane', lane], { encoding: 'utf8' });
  assert.ok(child.stdout, 'checker produced no report: ' + child.stderr);
  const report = JSON.parse(child.stdout);
  assert.equal(child.status, report.passed ? 0 : 1, 'exit status must match verdict');
  return report;
}

const edgesOf = (report, group) => report.graphs.find(g => g.name === group).edges;

for (const testCase of cases) {
  test(`${testCase.id}: ${testCase.requirement}`, t => {
    const report = run(t, testCase);
    if (testCase.expect === 'accept') {
      assert.deepEqual(report.refusals, [], 'positive case refused');
    } else {
      assert.equal(report.passed, false, 'negative case accepted (edge silently treated as absent)');
      const categories = report.refusals.map(r => r.category);
      assert.ok(categories.some(c => testCase.refuse.includes(c)), `refused for ${categories.join(',')} instead of ${testCase.refuse.join('|')}`);
      assert.ok(!categories.includes('tool-error'), 'checker crashed instead of diagnosing: ' + JSON.stringify(report.refusals));
    }
  });
}

test('runtime and declaration graphs resolve conditional exports per module format', t => {
  const report = run(t, { id: 'conditions', lane: 'report' });
  assert.match(edgesOf(report, 'browser-esm').find(e => e.module === 'dep').resolved, /^node_modules\/dep\/browser\.mjs$/);
  assert.match(edgesOf(report, 'browser-esm:types').find(e => e.module === 'dep').resolved, /^node_modules\/dep\/types\/import\.d\.mts$/);
  const provider = run(t, { id: 'conditions-provider', lane: 'provider' });
  assert.match(edgesOf(provider, 'node-cjs').find(e => e.module === 'dep').resolved, /^node_modules\/dep\/require\.cjs$/);
  assert.match(edgesOf(provider, 'node-cjs:types').find(e => e.module === 'dep').resolved, /^node_modules\/dep\/types\/require\.d\.cts$/);
  assert.match(edgesOf(provider, 'node-esm').find(e => e.module === 'dep').resolved, /^node_modules\/dep\/import\.mjs$/);
});

test('tsconfig paths without baseUrl resolve from the config directory', t => {
  const report = run(t, { id: 'paths', lane: 'report' });
  const alias = edgesOf(report, 'browser-esm:types').find(e => e.module === '@report/generated/report.js');
  assert.equal(alias.resolved, 'apps/report/src/generated/report.ts');
  assert.ok(alias.dependencyTypes.includes('aliased-tsconfig-paths'));
});

test('lane declaration errors refuse before analysis', t => {
  const duplicate = run(t, { id: 'duplicate', lane: 'report', lanes: l => { l.lanes.report.inputs.push('apps/report/src/index.ts'); } });
  assert.ok(duplicate.refusals.some(r => r.category === 'input-path' && /duplicate/.test(r.message)));
  const partition = run(t, { id: 'partition', lane: 'provider', lanes: l => { l.lanes.provider.runtimeGroups[1].files.pop(); } });
  assert.ok(partition.refusals.some(r => r.category === 'input-path' && /partition/.test(r.message)));
  const outside = run(t, { id: 'outside', lane: 'report', lanes: l => { l.lanes.report.inputs.push('providers/typescript/src/index.ts'); l.lanes.report.runtimeGroups[0].files.push('providers/typescript/src/index.ts'); } });
  assert.ok(outside.refusals.some(r => r.category === 'input-path' && /outside lane/.test(r.message)));
});

test('reports make no purity or closure qualification', t => {
  const report = run(t, { id: 'standing', lane: 'provider' });
  assert.equal(report.sourcePurityQualified, false);
  assert.equal(report.dependencyClosureQualified, false);
  assert.equal(report.tools.dependencyCruiser, '18.3.1');
  assert.equal(report.tools.typescript, '6.0.3');
});
