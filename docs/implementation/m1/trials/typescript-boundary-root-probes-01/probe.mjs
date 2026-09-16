import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { baseFiles, baseLanes, writeTree } from '/tmp/opensip-implementation/m1-typescript-boundary-comparison-01/trial/harness/fixture.mjs';
import { checkLane } from '/tmp/opensip-implementation/m1-typescript-boundary-comparison-01/trial/candidate/check-lane.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const cases = ['positive-report', 'external-browser-node', 'external-unresolved', 'cjs-dynamic-import-condition'];
if (process.argv[2]) {
  const name = process.argv[2];
  const root = path.join(here, name, 'root');
  fs.mkdirSync(root, {recursive:true});
  const files = baseFiles();
  let laneId = 'report';
  if (name === 'external-browser-node') files['node_modules/dep/browser.mjs'] = 'import {readFileSync} from "node:fs"; export const parseMode=typeof readFileSync;\n';
  if (name === 'external-unresolved') files['node_modules/dep/browser.mjs'] = 'import "./missing.mjs"; export const parseMode="browser";\n';
  if (name === 'cjs-dynamic-import-condition') {
    laneId = 'contracts';
    files['tools/contracts/generate.cjs'] = 'module.exports = async () => import("compiler-api");\n';
    const pkg = JSON.parse(files['node_modules/compiler-api/package.json']);
    pkg.exports = {'.':{types:'./index.d.ts',import:'./missing.mjs',require:'./index.js'}};
    files['node_modules/compiler-api/package.json'] = JSON.stringify(pkg);
  }
  writeTree(root, files);
  const result = await checkLane({root, lanes:baseLanes(), laneId});
  let oracle;
  if (name === 'cjs-dynamic-import-condition') {
    const r = spawnSync(process.execPath,['--input-type=commonjs','-e','import("compiler-api").then(()=>process.stdout.write("resolved"),e=>{process.stdout.write(e.code);process.exitCode=1;})'],{cwd:path.join(root,'tools/contracts'),encoding:'utf8'});
    oracle = {status:r.status,stdout:r.stdout,stderr:r.stderr};
  }
  fs.writeFileSync(path.join(here,name,'full-result.json'),JSON.stringify(result,null,2)+'\n');
  process.stdout.write(JSON.stringify({name,passed:result.passed,refusals:result.refusals,oracle})+'\n');
} else {
  const results = cases.map(name => {
    const r=spawnSync(process.execPath,[fileURLToPath(import.meta.url),name],{encoding:'utf8',maxBuffer:16*1024*1024});
    if (r.status !== 0) throw new Error(r.stderr || r.stdout);
    return JSON.parse(r.stdout);
  });
  fs.writeFileSync(path.join(here,'result.json'),JSON.stringify(results,null,2)+'\n');
  process.stdout.write(JSON.stringify(results,null,2)+'\n');
}
