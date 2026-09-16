/** Independent comparison-view DOM probes. Not a restatement of check-browser02.mjs. */
import {spawn} from 'node:child_process';
import {readFile, writeFile, mkdir, rm} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const COPY = path.join(ROOT, 'comparison', 'copy');
const OUT = path.join(ROOT, 'results', 'independent-comparison-chrome');
await rm(OUT, {recursive: true, force: true});
await mkdir(OUT, {recursive: true});
const profile = path.join(OUT, 'profile'); await mkdir(profile);
const names = ['generated/report', 'report-data', 'help-view', 'comparison-view'];
const sources = {};
for (const name of names) sources[name] = await readFile(path.join(COPY, 'compiled01', name + '.js'), 'utf8');
const css = await readFile(path.join(COPY, 'apps/report/src/report.css'), 'utf8');
const cases = JSON.parse(await readFile(path.join(COPY, 'current-report-cases.json'), 'utf8')).filter(c => c.ref.endsWith('report-projection:1#'));
await writeFile(path.join(OUT, 'fixture.html'), '<!doctype html><html lang="en"><meta charset="utf-8"><title>independent comparison</title><style>' + css + '</style><body><main class="report-main"><div id="mount"></div></main></body></html>');
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless=new', '--no-first-run', '--no-default-browser-check', '--disable-background-networking',
  '--disable-component-update', '--window-size=1100,800', '--remote-debugging-port=0', `--user-data-dir=${profile}`, 'about:blank',
], {stdio: ['ignore', 'pipe', 'pipe']});
let stderr = '', ws; chrome.stderr.on('data', d => { stderr += d; }); chrome.stdout.resume();
const rows = [];
try {
  let port;
  for (let i = 0; i < 200; i++) {
    try { port = Number((await readFile(path.join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]); break; }
    catch { await new Promise(r => setTimeout(r, 100)); }
  }
  if (!port) throw Error('Chrome startup timeout');
  const tab = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: 'PUT'})).json();
  ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.addEventListener('open', r, {once: true}); ws.addEventListener('error', j, {once: true}); });
  let id = 0; const pending = new Map();
  ws.addEventListener('message', e => {
    const m = JSON.parse(e.data), p = pending.get(m.id);
    if (p) { pending.delete(m.id); clearTimeout(p.timer); m.error ? p.reject(Error(JSON.stringify(m.error))) : p.resolve(m.result); }
  });
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const next = ++id, timer = setTimeout(() => { pending.delete(next); reject(Error('CDP timeout ' + method)); }, 45000);
    pending.set(next, {resolve, reject, timer}); ws.send(JSON.stringify({id: next, method, params}));
  });
  const evaluate = async expression => {
    const r = await send('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
    if (r.exceptionDetails) throw Error(JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };
  const check = async (name, expression) => {
    const passed = await evaluate(expression);
    rows.push({name, passed: passed === true}); console.log(passed === true ? 'PASS' : 'FAIL', name);
  };
  await send('Page.enable'); await send('Page.navigate', {url: pathToFileURL(path.join(OUT, 'fixture.html')).href});
  for (let i = 0; i < 100; i++) { if (await evaluate('!!document.getElementById("mount")')) break; await new Promise(r => setTimeout(r, 50)); }
  await send('Network.enable'); await send('Network.setBlockedURLs', {urls: ['*']});
  for (const name of names) {
    await evaluate(`globalThis.overviewModules??={};overviewModules[${JSON.stringify(name)}]={};((exports,require)=>{${sources[name]}\n})(overviewModules[${JSON.stringify(name)}],id=>{const key=id.replace(/^\\.\\//,'').replace(/\\.js$/,'');if(!overviewModules[key])throw Error('unselected');return overviewModules[key];});true`);
  }
  await evaluate(`globalThis.D=overviewModules['report-data'];globalThis.V=overviewModules['comparison-view'];globalThis.mount=document.getElementById('mount');
    globalThis.reports=${JSON.stringify(cases.map(c => c.raw))}.map(raw=>{const r=D.decodeReportData(new TextEncoder().encode(raw));if(r.status!=='ready')throw Error(r.code);return r.report;});
    globalThis.view=null;globalThis.show=report=>{view?.dispose();view=V.createComparisonView(document,report);mount.replaceChildren(view.element);return view;};
    globalThis.present=reports.find(r=>r.panels.comparison?.state==='present'); true`);
  await check('missing-vs-unavailable-vs-present', `(()=>{
    const missing=(()=>{const r=structuredClone(present); delete r.panels.comparison; show(r); return mount.textContent.includes('not included');})();
    const unavailable=(()=>{const r=structuredClone(present); r.panels.comparison={state:'unavailable',reason:'no-admitted-result'}; show(r); return mount.textContent.includes('unavailable')&&!mount.querySelector('.comparison-entries');})();
    show(present); const shown=!!mount.querySelector('.comparison-entries')||mount.textContent.includes('comparison entries');
    return missing&&unavailable&&shown;})()`);
  await check('null-presence-is-unknown-not-no', `(()=>{
    const r=structuredClone(present); const d=r.panels.comparison.data.comparison.descriptor;
    if(!d.entries.length){ d.entries=[{classification:'UNCHANGED',ruleId:'r',fingerprint:'fp',detectorId:'det',gates:false,liveInCurrent:false,subsequentDeltas:[],presence:{baselineFinding:null,currentFinding:false}}]; d.counts={gating:0n,unchanged:1n,codeNetNew:0n,codeFixed:0n,detectionDelta:0n,policyDelta:0n,scopeDelta:0n,waiverDelta:0n,evidenceDelta:0n,indeterminate:0n}; }
    else { d.entries[0].presence={baselineFinding:null,currentFinding:false}; }
    show(r);
    const block=[...mount.querySelectorAll('details')].find(x=>x.textContent.includes('Unknown is not absent'));
    return block&&block.textContent.includes('Unknown')&&block.textContent.includes('No')&&!/baselineFinding:\\s*No/.test(block.textContent.replaceAll('\\n',' '));
  })()`);
  await check('xss-rule-and-fingerprint-text-only', `(()=>{
    const r=structuredClone(present); const d=r.panels.comparison.data.comparison.descriptor;
    const e={classification:'CODE-NET-NEW',ruleId:'<img src=x onerror=globalThis.xss=1>',fingerprint:'<script>globalThis.xss=1</script>',detectorId:'det',gates:true,liveInCurrent:true,subsequentDeltas:[],presence:{}};
    d.entries=[e]; d.counts.gating=1n; show(r);
    return mount.textContent.includes('<img src=x onerror=globalThis.xss=1>')&&mount.querySelectorAll('img,a,script').length===0&&globalThis.xss!==1;})()`);
  await check('classification-filter-keeps-recorded-gating-count', `(()=>{
    show(present); const gating=present.panels.comparison.data.comparison.descriptor.counts.gating.toString();
    const sel=[...mount.querySelectorAll('select')][0]; sel.value='CODE-NET-NEW'; sel.dispatchEvent(new Event('change'));
    return mount.textContent.includes(gating+' recorded gating');})()`);
  await check('empty-entries-do-not-imply-no-regressions', `(()=>{
    const r=structuredClone(present); r.panels.comparison.data.comparison.descriptor.entries=[]; show(r);
    return mount.textContent.includes('No comparison entries are embedded')&&mount.textContent.includes('consult the recorded verdict');})()`);
  await check('filter-no-match-distinct-from-empty-source', `(()=>{
    const r=structuredClone(present); const d=r.panels.comparison.data.comparison.descriptor;
    if(!d.entries.length) d.entries=[{classification:'UNCHANGED',ruleId:'keep',fingerprint:'fp',detectorId:'det',gates:false,liveInCurrent:false,subsequentDeltas:[],presence:{}}];
    show(r); const search=mount.querySelector('input[type=search]'); search.value='zzz-no-match'; search.dispatchEvent(new Event('input'));
    return mount.textContent.includes('No embedded entries match these filters.')&&mount.textContent.includes(d.entries.length+' comparison entries embedded');})()`);
  await check('exactly-25-entries-next-disabled', `(()=>{
    const r=structuredClone(present); const d=r.panels.comparison.data.comparison.descriptor;
    const base={classification:'UNCHANGED',ruleId:'r',fingerprint:'fp',detectorId:'det',gates:false,liveInCurrent:false,subsequentDeltas:[],presence:{}};
    d.entries=Array.from({length:25},(_,i)=>({...base,fingerprint:'fp'+i})); show(r);
    const next=[...mount.querySelectorAll('button')].find(b=>b.textContent==='Next entries');
    return mount.querySelectorAll('.comparison-entries>li').length===25&&next.disabled;})()`);
  await check('bigint-count-displays-exactly', `(()=>{
    const r=structuredClone(present); r.panels.comparison.data.comparison.descriptor.counts.gating=9007199254740993n; show(r);
    return mount.textContent.includes('9007199254740993');})()`);
  await check('caller-mutation-after-mount-ignored', `(()=>{
    const r=structuredClone(present); show(r);
    r.panels.comparison.data.comparison.descriptor.verdict='MUTATED-VERDICT';
    return !mount.textContent.includes('MUTATED-VERDICT');})()`);
  await check('no-links-and-help-unknown-not-absent', `(()=>{
    show(present); mount.querySelector('.report-help>button').click();
    return mount.querySelectorAll('a').length===0&&mount.textContent.includes('Indeterminate and unknown presence remain explicit');})()`);
  await check('dispose-idempotent', `(()=>{show(present); const old=view; old.dispose(); old.dispose(); return mount.children.length===0&&document.querySelectorAll('dialog:modal').length===0;})()`);
  const failed = rows.filter(r => !r.passed).map(r => r.name);
  await writeFile(path.join(ROOT, 'results', 'independent-comparison.json'), JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed, cases: rows}, null, 2) + '\n');
  console.log(JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed}));
  if (failed.length) throw Error('comparison probes failed');
} catch (e) {
  await writeFile(path.join(OUT, 'failure.json'), JSON.stringify({error: String(e), checks: rows}, null, 2) + '\n'); throw e;
} finally {
  ws?.close(); chrome.kill('SIGTERM');
  await new Promise(r => { chrome.once('exit', r); setTimeout(r, 5000); });
  if (chrome.exitCode === null && chrome.signalCode === null) chrome.kill('SIGKILL');
  await writeFile(path.join(OUT, 'chrome.stderr'), stderr);
}
