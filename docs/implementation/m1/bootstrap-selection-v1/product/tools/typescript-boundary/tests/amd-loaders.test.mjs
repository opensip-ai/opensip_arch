import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const top=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
test('AMD implicit loader refusal and explicit local-array acceptance',()=>{
 const c=spawnSync(process.execPath,[path.join(top,'harness/root05-amd.mjs')],{encoding:'utf8'});
 const result=JSON.parse(fs.readFileSync(path.join(top,'results/root05-amd.json'),'utf8'));
 assert.equal(result.rows.length,9);
 for(const row of result.rows) assert.equal(row.grade,'correct',JSON.stringify(row));
 assert.equal(c.status,0,c.stdout+c.stderr);
});
