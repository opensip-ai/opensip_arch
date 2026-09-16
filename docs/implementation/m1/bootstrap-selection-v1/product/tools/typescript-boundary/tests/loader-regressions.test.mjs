// Permanent counterexamples from the substantive partial actual-Claude review03.
// This checks a proposed policy, not independent approval of that policy.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const top = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
test('actual review03 counterexamples and positive controls', async t => {
  const label = process.env.OPENSIP_BOUNDARY_TEST_LABEL ?? 'review03';
  const out = path.join(top, 'work/test-run', label + '-review03.json');
  const run = spawnSync(process.execPath, [path.join(top, 'harness/review03-regressions.mjs'), '--out', out], { encoding: 'utf8', maxBuffer: 128 * 1024 * 1024 });
  const result = JSON.parse(fs.readFileSync(out, 'utf8'));
  assert.equal(result.rows.length, 33);
  for (const row of result.rows) await t.test(row.id, () => assert.equal(row.grade, 'correct', JSON.stringify(row)));
  assert.equal(run.status, 0, run.stdout + run.stderr);
});
