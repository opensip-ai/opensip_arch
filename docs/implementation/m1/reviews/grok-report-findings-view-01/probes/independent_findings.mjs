/** Independent findings-view DOM probes. Not a restatement of check-browser01.mjs. */
import {spawn} from 'node:child_process';
import {readFile, writeFile, mkdir, rm} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const COPY = path.join(ROOT, 'findings', 'copy');
const OUT = path.join(ROOT, 'results', 'independent-findings-chrome');
await rm(OUT, {recursive: true, force: true});
await mkdir(OUT, {recursive: true});
const profile = path.join(OUT, 'profile'); await mkdir(profile);
const names = ['generated/report', 'report-data', 'help-view', 'findings-view'];
const sources = {};
for (const name of names) sources[name] = await readFile(path.join(COPY, 'compiled01', name + '.js'), 'utf8');
const css = await readFile(path.join(COPY, 'apps/report/src/report.css'), 'utf8');
const cases = JSON.parse(await readFile(path.join(COPY, 'current-report-cases.json'), 'utf8')).filter(c => c.ref.endsWith('report-projection:1#'));
await writeFile(path.join(OUT, 'fixture.html'), '<!doctype html><html lang="en"><meta charset="utf-8"><title>independent findings</title><style>' + css + '</style><body><main class="report-main"><div id="mount"></div></main></body></html>');
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
  await evaluate(`globalThis.D=overviewModules['report-data'];globalThis.V=overviewModules['findings-view'];globalThis.mount=document.getElementById('mount');
    globalThis.reports=${JSON.stringify(cases.map(c => c.raw))}.map(raw=>{const r=D.decodeReportData(new TextEncoder().encode(raw));if(r.status!=='ready')throw Error(r.code);return r.report;});
    globalThis.view=null;globalThis.show=report=>{view?.dispose();view=V.createFindingsView(document,report);mount.replaceChildren(view.element);return view;};
    globalThis.withFindings=reports.find(r=>Array.isArray(r.envelope.findings)&&r.envelope.findings.length); true`);
  await check('missing-vs-empty-findings-distinct', `(()=>{const r=structuredClone(withFindings); r.envelope.findings=[]; show(r);
    const empty=mount.textContent.includes('contains no findings')&&!mount.textContent.includes('not included in this report');
    delete r.envelope.findings; show(r);
    return empty&&mount.textContent.includes('not included in this report')&&!mount.textContent.includes('contains no findings');})()`);
  await check('filter-does-not-change-recorded-verdict', `(()=>{
    const r=structuredClone(withFindings); const v=r.envelope.run?.verdict; show(r);
    const before=v&&mount.textContent.includes(v);
    mount.querySelector('select').value='error'; mount.querySelector('select').dispatchEvent(new Event('change'));
    return before&&v&&mount.textContent.includes(v);})()`);
  await check('xss-path-and-id-are-text', `(()=>{
    const r=structuredClone(withFindings); const f=structuredClone(r.envelope.findings[0]);
    f.findingId='id-<img src=x onerror=globalThis.xss=1>'; f.subjectPath='<script>globalThis.xss=1</script>'; f.fingerprint=null;
    f.correspondence={state:'unmatched'}; r.envelope.findings=[f]; show(r);
    return mount.textContent.includes('<img src=x onerror=globalThis.xss=1>')&&mount.textContent.includes('<script>')
      &&mount.textContent.includes('Unavailable')&&mount.querySelectorAll('img,a,script').length===0&&globalThis.xss!==1;})()`);
  await check('duplicate-ids-refuse-select', `(()=>{
    const r=structuredClone(withFindings); const f=structuredClone(r.envelope.findings[0]); f.findingId='dup';
    r.envelope.findings=[f, structuredClone(f)]; show(r); const before=mount.innerHTML;
    return !view.select('dup')&&mount.innerHTML===before;})()`);
  await check('unknown-id-refuses', `(()=>{show(withFindings); const before=mount.innerHTML; return !view.select('no-such-finding')&&mount.innerHTML===before;})()`);
  await check('exact-25-disables-next', `(()=>{
    const r=structuredClone(withFindings); const base=structuredClone(r.envelope.findings[0]);
    r.envelope.findings=Array.from({length:25},(_,i)=>({...base,findingId:'f'+i})); show(r);
    const next=[...mount.querySelectorAll('button')].find(b=>b.textContent==='Next findings');
    return mount.querySelectorAll('.findings-list>li').length===25&&next.disabled;})()`);
  await check('no-match-filter-distinct-from-empty-source', `(()=>{
    show(withFindings); const search=mount.querySelector('input[type=search]'); search.value='zzz-no-match-zzz'; search.dispatchEvent(new Event('input'));
    return mount.textContent.includes('No embedded findings match these filters.')&&mount.textContent.includes(String(withFindings.envelope.findings.length)+' finding rows embedded');})()`);
  await check('caller-mutation-of-cloned-rows-ignored', `(()=>{
    const r=structuredClone(withFindings); const id=r.envelope.findings[0].findingId; show(r);
    r.envelope.findings[0].ruleId='MUTATED-RULE'; view.select(id);
    return !mount.textContent.includes('MUTATED-RULE');})()`);
  await check('no-path-links-or-source-spans', `(()=>{show(withFindings); return mount.querySelectorAll('a').length===0 && mount.textContent.includes('no source spans');})()`);
  await check('dispose-refuses-stale-select', `(()=>{show(withFindings); const old=view, id=withFindings.envelope.findings[0].findingId; old.dispose(); old.dispose(); return !old.select(id)&&mount.children.length===0;})()`);
  const failed = rows.filter(r => !r.passed).map(r => r.name);
  await writeFile(path.join(ROOT, 'results', 'independent-findings.json'), JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed, cases: rows}, null, 2) + '\n');
  console.log(JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed}));
  if (failed.length) throw Error('findings probes failed');
} catch (e) {
  await writeFile(path.join(OUT, 'failure.json'), JSON.stringify({error: String(e), checks: rows}, null, 2) + '\n'); throw e;
} finally {
  ws?.close(); chrome.kill('SIGTERM');
  await new Promise(r => { chrome.once('exit', r); setTimeout(r, 5000); });
  if (chrome.exitCode === null && chrome.signalCode === null) chrome.kill('SIGKILL');
  await writeFile(path.join(OUT, 'chrome.stderr'), stderr);
}
