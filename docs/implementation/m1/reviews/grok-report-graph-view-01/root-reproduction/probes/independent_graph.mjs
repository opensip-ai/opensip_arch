/** Independent graph-view DOM probes. Not a restatement of check-browser02.mjs. */
import {spawn} from 'node:child_process';
import {readFile, writeFile, mkdir, rm} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const COPY = path.join(ROOT, 'copy');
const OUT = path.join(ROOT, 'results', 'independent-chrome');
await rm(OUT, {recursive: true, force: true});
await mkdir(OUT, {recursive: true});
const profile = path.join(OUT, 'profile');
await mkdir(profile);
const names = ['generated/report', 'report-data', 'help-view', 'graph-view'];
const sources = {};
for (const name of names) sources[name] = await readFile(path.join(COPY, 'compiled01', name + '.js'), 'utf8');
const css = await readFile(path.join(COPY, 'apps/report/src/report.css'), 'utf8');
const cases = JSON.parse(await readFile(path.join(COPY, 'current-report-cases.json'), 'utf8')).filter(c => c.ref.endsWith('report-projection:1#'));
const html = '<!doctype html><html lang="en"><meta charset="utf-8"><title>independent graph probes</title><style>' + css + '</style><body><main class="report-main"><div id="mount"></div></main></body></html>';
await writeFile(path.join(OUT, 'fixture.html'), html);
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless=new', '--no-first-run', '--no-default-browser-check', '--disable-background-networking',
  '--disable-component-update', '--window-size=1100,800', '--remote-debugging-port=0',
  `--user-data-dir=${profile}`, 'about:blank',
], {stdio: ['ignore', 'pipe', 'pipe']});
let stderr = '', ws;
chrome.stderr.on('data', d => { stderr += d; });
chrome.stdout.resume();
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
    pending.set(next, {resolve, reject, timer});
    ws.send(JSON.stringify({id: next, method, params}));
  });
  const evaluate = async expression => {
    const r = await send('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
    if (r.exceptionDetails) throw Error(JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };
  const check = async (name, expression) => {
    const passed = await evaluate(expression);
    rows.push({name, passed: passed === true, observed: passed});
    console.log(passed === true ? 'PASS' : 'FAIL', name);
  };
  await send('Page.enable');
  await send('Page.navigate', {url: pathToFileURL(path.join(OUT, 'fixture.html')).href});
  for (let i = 0; i < 100; i++) { if (await evaluate('!!document.getElementById("mount")')) break; await new Promise(r => setTimeout(r, 50)); }
  await send('Network.enable'); await send('Network.setBlockedURLs', {urls: ['*']});
  for (const name of names) {
    await evaluate(`globalThis.overviewModules??={};overviewModules[${JSON.stringify(name)}]={};((exports,require)=>{${sources[name]}\n})(overviewModules[${JSON.stringify(name)}],id=>{const key=id.replace(/^\\.\\//,'').replace(/\\.js$/,'');if(!overviewModules[key])throw Error('unselected module');return overviewModules[key];});true`);
  }
  await evaluate(`globalThis.D=overviewModules['report-data'];globalThis.GV=overviewModules['graph-view'];globalThis.mount=document.getElementById('mount');
    globalThis.rawReports=${JSON.stringify(cases.map(c => c.raw))};
    globalThis.reports=rawReports.map(raw=>{const r=D.decodeReportData(new TextEncoder().encode(raw));if(r.status!=='ready')throw Error(r.code);return r.report;});
    globalThis.view=null;globalThis.show=report=>{view?.dispose();view=GV.createGraphView(document,report);mount.replaceChildren(view.element);return view;};
    globalThis.present=reports.find(r=>r.panels.graph?.state==='present'&&r.panels.graph.data.slots.length);
    true`);

  await check('fixtures-are-not-claimed-as-retained-runs', `reports.length===32 && !document.body.innerHTML.includes('retained Run')`);
  await check('missing-panel-distinct-from-empty-slots', `(()=>{const r=structuredClone(present); r.panels.graph.data.slots=[]; show(r);
    const empty=mount.textContent.includes('No query slots are embedded') && !mount.textContent.includes('panel is not included');
    delete r.panels.graph; show(r);
    const missing=mount.textContent.includes('panel is not included') && !mount.textContent.includes('No query slots are embedded');
    return empty&&missing;})()`);
  await check('omitted-unavailable-corrupt-incompatible-states-distinct', `(()=>{
    const states=[['omitted','not-selected'],['unavailable','no-admitted-result'],['corrupt','retained-bytes-corrupt'],['incompatible','retained-schema-major-unsupported']];
    return states.every(([state,reason])=>{
      const r=structuredClone(present); r.panels.graph={state,reason}; show(r);
      return mount.textContent.includes(state) && !mount.querySelector('select') && mount.textContent.includes('Relationship data is not included');
    });
  })()`);
  await check('omitted-items-same-row-list-as-empty-but-not-included-label-for-items', `(()=>{
    const r=structuredClone(present); const s=structuredClone(r.panels.graph.data.slots[0]);
    delete s.response.items; r.panels.graph.data.slots=[s]; show(r);
    const omitted=mount.textContent.includes('zero rows alone do not prove absence');
    s.response.items=[]; show(r);
    const empty=mount.textContent.includes('zero rows alone do not prove absence');
    return omitted&&empty;
  })()`);
  await check('bigint-over-float-precision-displayed-exactly', `(()=>{
    const r=structuredClone(present); const s=structuredClone(r.panels.graph.data.slots[0]);
    s.ordinal=9007199254740993n; s.response.context.totalItems=9007199254740993n; s.response.context.producedItems=9007199254740993n;
    s.response.items=[{depth:9007199254740993n}]; r.panels.graph.data.slots=[s]; show(r);
    return mount.textContent.includes('9007199254740993') && !mount.textContent.includes('9007199254740992');
  })()`);
  await check('xss-in-purpose-project-and-cursor-stays-text', `(()=>{
    const r=structuredClone(present); const s=structuredClone(r.panels.graph.data.slots[0]);
    s.purpose='neighborhood'; s.request.operation='graph.neighbors';
    s.response.context.projectId='<img src=x onerror=globalThis.xss=1>';
    s.response.context.nextCursor='javascript:alert(1)';
    s.response.items=[{label:'<script>globalThis.xss=1</script>', href:'https://evil.example/x'}];
    r.panels.graph.data.slots=[s]; show(r);
    return mount.textContent.includes('<img src=x onerror=globalThis.xss=1>')
      && mount.textContent.includes('javascript:alert(1)')
      && mount.querySelectorAll('img,a,script').length===0 && globalThis.xss!==1;
  })()`);
  await check('producedItems-mismatch-does-not-invent-rows-or-hide-recorded-count', `(()=>{
    const r=structuredClone(present); const s=structuredClone(r.panels.graph.data.slots[0]);
    s.response.context.producedItems=10n; s.response.context.totalItems=10n; s.response.context.availability='partial';
    s.response.context.truncated=true; s.response.context.traversalCoverage='truncated-bound'; s.response.context.countBasis='lower-bound';
    s.response.items=[]; r.panels.graph.data.slots=[s]; show(r);
    return mount.textContent.includes('10') && mount.textContent.includes('partial') && mount.textContent.includes('lower-bound')
      && mount.textContent.includes('truncated-bound') && mount.textContent.includes('zero rows alone do not prove absence')
      && mount.querySelectorAll('.graph-rows>li').length===1;
  })()`);
  await check('exactly-25-rows-disables-next', `(()=>{
    const r=structuredClone(present); const s=structuredClone(r.panels.graph.data.slots[0]);
    s.response.items=Array.from({length:25},(_,i)=>({i})); r.panels.graph.data.slots=[s]; show(r);
    const next=[...mount.querySelectorAll('button')].find(x=>x.textContent==='Next embedded rows');
    return mount.querySelectorAll('.graph-rows>li').length===25 && next.disabled && mount.textContent.includes('Page 1 of 1');
  })()`);
  await check('twenty-six-rows-second-page-has-one', `(()=>{
    const r=structuredClone(present); const s=structuredClone(r.panels.graph.data.slots[0]);
    s.response.items=Array.from({length:26},(_,i)=>({i})); r.panels.graph.data.slots=[s]; show(r);
    [...mount.querySelectorAll('button')].find(x=>x.textContent==='Next embedded rows').click();
    return mount.textContent.includes('Page 2 of 2') && mount.querySelectorAll('.graph-rows>li').length===1
      && mount.querySelector('.graph-rows>li').textContent.includes('"i": 25');
  })()`);
  await check('continuation-and-cursor-are-display-only', `(()=>{
    const r=structuredClone(present); const s=structuredClone(r.panels.graph.data.slots[0]);
    s.hostProjection.continuation='not-embedded'; s.response.context.nextCursor='cursor-token';
    r.panels.graph.data.slots=[s]; show(r);
    return mount.textContent.includes('not-embedded') && mount.textContent.includes('Next cursor (not followed)')
      && mount.textContent.includes('cursor-token') && mount.querySelectorAll('a').length===0;
  })()`);
  await check('unknown-negative-ordinal-does-not-select', `(()=>{
    show(present); const before=mount.innerHTML;
    const zeros=present.panels.graph.data.slots.filter(s=>s.ordinal===0n).length;
    const zeroOk=zeros===1?view.select(0n)===true:!view.select(0n);
    show(present); const before2=mount.innerHTML;
    return zeroOk && !view.select(-1n) && mount.innerHTML===before2;
  })()`);
  await check('no-source-location-or-checkout-query-controls', `(()=>{
    show(present);
    return !mount.textContent.toLowerCase().includes('source location')
      && mount.querySelectorAll('input[type=url],a[href]').length===0
      && [...mount.querySelectorAll('button')].every(b=>!/query|fetch|follow cursor/i.test(b.textContent));
  })()`);
  await check('structuredClone-defends-nested-row-mutation', `(()=>{
    const r=structuredClone(present); const s=structuredClone(r.panels.graph.data.slots[0]);
    s.ordinal=7n; s.response.items=[{keep:'original'}]; r.panels.graph.data.slots=[s]; show(r);
    r.panels.graph.data.slots[0].response.items[0].keep='mutated';
    view.select(7n);
    return mount.textContent.includes('original') && !mount.textContent.includes('mutated');
  })()`);

  const failed = rows.filter(r => r.passed !== true).map(r => r.name);
  const out = {caseCount: rows.length, failedCount: failed.length, failed, cases: rows, fixtureCount: cases.length};
  await writeFile(path.join(ROOT, 'results', 'independent-graph.json'), JSON.stringify(out, null, 2) + '\n');
  console.log(JSON.stringify({caseCount: out.caseCount, failedCount: out.failedCount, failed}));
  if (failed.length) throw Error('independent probes failed');
} catch (e) {
  await writeFile(path.join(OUT, 'failure.json'), JSON.stringify({error: String(e), checks: rows}, null, 2) + '\n');
  throw e;
} finally {
  ws?.close();
  chrome.kill('SIGTERM');
  await new Promise(r => { chrome.once('exit', r); setTimeout(r, 5000); });
  if (chrome.exitCode === null && chrome.signalCode === null) chrome.kill('SIGKILL');
  await writeFile(path.join(OUT, 'chrome.stderr'), stderr);
}
