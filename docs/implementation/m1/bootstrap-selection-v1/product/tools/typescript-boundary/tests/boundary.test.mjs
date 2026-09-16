// Checker test suite. Runs every author02 matrix case, review-02 probe and
// author-03 regression case against the checker (OPENSIP_BOUNDARY_CHECKER may
// point at a mutant) and requires the expected verdict and category plus
// agreement with the Node oracle where one exists; then runs the real CLI
// invocation checks (realpath, /tmp alias, .bin symlink).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const top = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const label = process.env.OPENSIP_BOUNDARY_TEST_LABEL ?? 'test';
const tmp = path.join(top, 'work', 'tmp');
fs.mkdirSync(tmp, { recursive: true });
const env = { ...process.env, TMPDIR: tmp, OPENSIP_BOUNDARY_TEST_LABEL: label };

test('author, reviewer and regression cases', async t => {
  const out = `work/test-run/${label}-cases.json`;
  const run = spawnSync(process.execPath, [path.join(top, 'harness/run-cases.mjs'), '--candidates', 'new', '--out', out], { encoding: 'utf8', env, maxBuffer: 128 * 1024 * 1024 });
  assert.equal(run.status, 0, run.stderr);
  const result = JSON.parse(fs.readFileSync(path.join(top, out), 'utf8'));
  assert.ok(result.rows.length >= 150, 'case catalog unexpectedly small');
  for (const row of result.rows) {
    await t.test(`${row.set}:${row.id}`, () => {
      assert.equal(row.new.grade, 'correct', JSON.stringify({ expected: row.expectedForNew, categories: row.new.categories, status: row.new.status, refusals: row.new.refusals.slice(0, 4), stderr: row.new.stderr }));
      if (row.oracle) assert.equal(row.new.oracleAgrees, true, 'verdict disagrees with the Node oracle: ' + JSON.stringify(row.oracle));
    });
  }
});

test('real CLI invocations: realpath, /tmp alias and .bin symlink exit codes', () => {
  const run = spawnSync(process.execPath, [path.join(top, 'harness/cli-invocation.mjs')], { encoding: 'utf8', env });
  assert.equal(run.status, 0, run.stdout + run.stderr);
});
