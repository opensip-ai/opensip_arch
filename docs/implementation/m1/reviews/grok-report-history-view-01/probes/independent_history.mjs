/** Independent history-view DOM probes. Not a restatement of check-browser03.mjs. */
import {spawn} from 'node:child_process';
import {readFile, writeFile, mkdir, rm} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const COPY = path.join(ROOT, 'history', 'copy');
const OUT = path.join(ROOT, 'results', 'independent-history-chrome');
await rm(OUT, {recursive: true, force: true});
await mkdir(OUT, {recursive: true});
const profile = path.join(OUT, 'profile'); await mkdir(profile);
const names = ['generated/report', 'report-data', 'help-view', 'history-view'];
const sources = {};
for (const name of names) sources[name] = await readFile(path.join(COPY, 'compiled02', name + '.js'), 'utf8');
const css = await readFile(path.join(COPY, 'apps/report/src/report.css'), 'utf8');
const cases = JSON.parse(await readFile(path.join(COPY, 'current-report-cases.json'), 'utf8')).filter(c => c.ref.endsWith('report-projection:1#'));
await writeFile(path.join(OUT, 'fixture.html'), '<!doctype html><html lang="en"><meta charset="utf-8"><title>independent history</title><style>' + css + '</style><body><main class="report-main"><div id="mount"></div></main></body></html>');
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
  await evaluate(`globalThis.D=overviewModules['report-data'];globalThis.V=overviewModules['history-view'];globalThis.mount=document.getElementById('mount');
    globalThis.reports=${JSON.stringify(cases.map(c => c.raw))}.map(raw=>{const r=D.decodeReportData(new TextEncoder().encode(raw));if(r.status!=='ready')throw Error(r.code);return r.report;});
    globalThis.view=null;globalThis.show=report=>{view?.dispose();view=V.createHistoryView(document,report);mount.replaceChildren(view.element);return view;};
    globalThis.present=reports.find(r=>r.panels.history?.state==='present'&&r.panels.history.data.runs?.length);
    true`);
  await check('automatic-vs-explicit-policy-labels', `(()=>{
    const r=structuredClone(present); r.panels.history.data.selection={policy:'explicit-run-ids.1',requestedRunIds:['run3:aaaa'],currentRunId:null};
    r.panels.history.data.runs=[{runId:'run3:aaaa',state:'unavailable',availability:'expired'}];
    show(r); const explicit=mount.textContent.includes('Explicit Run identifiers');
    show(present); const auto=present.panels.history.data.selection.policy!=='explicit-run-ids.1'?mount.textContent.includes('Baseline source, then earlier committed Runs'):true;
    return explicit&&auto;})()`);
  await check('unknown-run-does-not-substitute-newest', `(()=>{
    show(present); const first=present.panels.history.data.selection.requestedRunIds[0];
    const before=mount.querySelector('select').value; return !view.select('run3:not-present-zzzz') && mount.querySelector('select').value===before && before===first;})()`);
  await check('unavailable-row-shows-reason-not-latest', `(()=>{
    const r=structuredClone(present); r.panels.history.data.selection={policy:'explicit-run-ids.1',requestedRunIds:['run3:dead','run3:live'],currentRunId:'run3:live'};
    r.panels.history.data.runs=[
      {runId:'run3:dead',state:'unavailable',availability:'purged'},
      {runId:'run3:live',state:'current-run'}];
    show(r); view.select('run3:dead');
    return mount.textContent.includes('purged') && mount.textContent.includes('Requested Run unavailable') && !mount.textContent.includes('historical copy');})()`);
  await check('current-run-does-not-invent-historical-copy', `(()=>{
    const r=structuredClone(present); r.panels.history.data.selection={policy:'explicit-run-ids.1',requestedRunIds:['run3:cur'],currentRunId:'run3:cur'};
    r.panels.history.data.runs=[{runId:'run3:cur',state:'current-run'}]; show(r);
    return mount.textContent.includes('current Run already represented') && !mount.querySelector('.history-findings');})()`);
  await check('xss-run-id-and-path-are-text', `(()=>{
    const r=structuredClone(present); const id='run3:<img src=x onerror=globalThis.xss=1>';
    r.panels.history.data.selection={policy:'explicit-run-ids.1',requestedRunIds:[id],currentRunId:null};
    r.panels.history.data.runs=[{runId:id,state:'present',commitSequence:1n,findings:[{findingId:'f',ruleId:'r',subjectPath:'<script>globalThis.xss=1</script>',subjectId:'s',messageCode:'m',severity:'error',waived:false,correspondence:{state:'unmatched'}}],findingsProjection:{total:1n,omitted:0n,omissionCause:'none'},run:{verdict:'fail',requiredCoverage:'complete',deficiency:'present'}}];
    show(r);
    return mount.textContent.includes('<img src=x onerror=globalThis.xss=1>') && mount.textContent.includes('<script>') && mount.querySelectorAll('img,a,script').length===0 && globalThis.xss!==1;})()`);
  await check('embedded-vs-omitted-vs-matching-counts', `(()=>{
    const r=structuredClone(present); const id='run3:dense';
    r.panels.history.data.selection={policy:'explicit-run-ids.1',requestedRunIds:[id],currentRunId:null};
    const findings=Array.from({length:30},(_,i)=>({findingId:'f'+i,ruleId:'r',subjectPath:'p',subjectId:'s',messageCode:'m',severity:'error',waived:false,correspondence:{state:'unmatched'}}));
    r.panels.history.data.runs=[{runId:id,state:'present',commitSequence:2n,findings,findingsProjection:{total:100n,omitted:70n,omissionCause:'item-cap'},run:{verdict:'fail',requiredCoverage:'complete',deficiency:'present'}}];
    show(r);
    const search=mount.querySelector('input[type=search]'); search.value='no-match-zzz'; search.dispatchEvent(new Event('input'));
    return mount.textContent.includes('30 embedded of 100') && mount.textContent.includes('70 omitted') && mount.textContent.includes('No embedded findings match this search.');})()`);
  await check('exactly-25-findings-next-disabled', `(()=>{
    const r=structuredClone(present); const id='run3:p25';
    r.panels.history.data.selection={policy:'explicit-run-ids.1',requestedRunIds:[id],currentRunId:null};
    const findings=Array.from({length:25},(_,i)=>({findingId:'f'+i,ruleId:'r',subjectPath:'p',subjectId:'s',messageCode:'m',severity:'error',waived:false,correspondence:{state:'unmatched'}}));
    r.panels.history.data.runs=[{runId:id,state:'present',commitSequence:1n,findings,findingsProjection:{total:25n,omitted:0n,omissionCause:'none'},run:{verdict:'fail',requiredCoverage:'complete',deficiency:'present'}}];
    show(r); const next=[...mount.querySelectorAll('button')].find(b=>b.textContent==='Next findings');
    return mount.querySelectorAll('.history-findings>li').length===25 && next.disabled;})()`);
  await check('caller-cannot-swap-mounted-row', `(()=>{
    const r=structuredClone(present); const id=r.panels.history.data.selection.requestedRunIds[0];
    show(r); r.panels.history.data.runs[0].runId='run3:mutated'; view.select(id);
    return !mount.textContent.includes('run3:mutated');})()`);
  await check('missing-panel-distinct', `(()=>{const r=structuredClone(present); delete r.panels.history; show(r); return mount.textContent.includes('not included') && !mount.querySelector('select');})()`);
  await check('empty-requested-runs-explicit', `(()=>{
    const r=structuredClone(present); r.panels.history.data.selection.requestedRunIds=[]; r.panels.history.data.runs=[]; show(r);
    return mount.textContent.includes('No historical Runs were requested') && mount.querySelector('select').disabled;})()`);
  await check('dispose-refuses-stale-select', `(()=>{show(present); const old=view, id=present.panels.history.data.selection.requestedRunIds[0]; old.dispose(); old.dispose(); return !old.select(id) && mount.children.length===0;})()`);
  await check('observation-time-and-automatic-snapshot-counts', `(()=>{
    const auto=reports.find(r=>r.panels.history?.state==='present'&&r.panels.history.data.selection.policy==='baseline-source-then-prior-commit-sequence.1');
    if(!auto) return false;
    show(auto);
    const s=auto.panels.history.data.selection;
    const options=[...mount.querySelectorAll('select option')].map(o=>o.value);
    return mount.textContent.includes(auto.reportObservedAt)
      && options.join('|')===s.requestedRunIds.join('|')
      && mount.textContent.includes(s.priorRunsInSnapshot.toString())
      && mount.textContent.includes(s.currentCommitSequence.toString())
      && mount.textContent.includes('not a live history list');
  })()`);
  await send('Emulation.setDeviceMetricsOverride', {width: 390, height: 844, deviceScaleFactor: 1, mobile: false});
  await check('narrow-long-run-id-no-page-overflow', `(()=>{
    const r=structuredClone(present);
    const long='run3:'+'a'.repeat(200);
    r.panels.history.data.selection={policy:'explicit-run-ids.1',requestedRunIds:[long],currentRunId:null};
    r.panels.history.data.runs=[{runId:long,state:'unavailable',availability:'expired'}];
    show(r);
    return document.documentElement.scrollWidth<=innerWidth && mount.querySelector('select').value===long
      && mount.textContent.includes(long);
  })()`);
  const failed = rows.filter(r => !r.passed).map(r => r.name);
  await writeFile(path.join(ROOT, 'results', 'independent-history.json'), JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed, cases: rows}, null, 2) + '\n');
  console.log(JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed}));
  if (failed.length) throw Error('history probes failed');
} catch (e) {
  await writeFile(path.join(OUT, 'failure.json'), JSON.stringify({error: String(e), checks: rows}, null, 2) + '\n'); throw e;
} finally {
  ws?.close(); chrome.kill('SIGTERM');
  await new Promise(r => { chrome.once('exit', r); setTimeout(r, 5000); });
  if (chrome.exitCode === null && chrome.signalCode === null) chrome.kill('SIGKILL');
  await writeFile(path.join(OUT, 'chrome.stderr'), stderr);
}
