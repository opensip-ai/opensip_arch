import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
test('browser scanner physical targets and transitive boundaries',()=>{
 const r=spawnSync(process.execPath,[path.join(root,'harness/root06-browser.mjs')],{encoding:'utf8',cwd:root});
 assert.equal(r.status,0,r.stdout+r.stderr);
 const result=JSON.parse(fs.readFileSync(path.join(root,'results/root06-browser04.json')));
 assert.equal(result.rows.length,15);assert.ok(result.rows.every(x=>x.grade==='correct'));
});
test('literal disabled prefix remains a physical target',()=>{
 const r=spawnSync(process.execPath,[path.join(root,'harness/root06-disabled-collision.mjs')],{encoding:'utf8',cwd:root});
 assert.equal(r.status,0,r.stdout+r.stderr);
});
