/** Independent composition DOM probes. Not a restatement of check-browser04.mjs. */
import {spawn} from 'node:child_process';
import {readFile, writeFile, mkdir, rm} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const COPY = path.join(ROOT, 'composition', 'copy');
const OUT = path.join(ROOT, 'results', 'independent-composition-chrome');
await rm(OUT, {recursive: true, force: true});
await mkdir(OUT, {recursive: true});
const profile = path.join(OUT, 'profile'); await mkdir(profile);
const names = ['generated/report', 'report-data', 'help-view', 'overview-view', 'evidence-view', 'catalog-view', 'navigation'];
const sources = {};
for (const name of names) sources[name] = await readFile(path.join(COPY, 'compiled', name + '.js'), 'utf8');
const css = await readFile(path.join(COPY, 'apps/report/src/report.css'), 'utf8');
const cases = JSON.parse(await readFile(path.join(COPY, 'current-report-cases.json'), 'utf8')).filter(c => c.ref.endsWith('report-projection:1#'));
await writeFile(path.join(OUT, 'fixture.html'), '<!doctype html><html lang="en"><meta charset="utf-8"><title>independent composition</title><style>' + css + '</style><body><main class="report-main"><div id="mount"></div></main></body></html>');
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
  await evaluate(`globalThis.D=overviewModules['report-data'];
    globalThis.N=overviewModules.navigation; globalThis.mount=document.getElementById('mount');
    globalThis.absent={state:'omitted',reason:'not-selected'};
    globalThis.rawReports=${JSON.stringify(cases.map(c => c.raw))};
    globalThis.reports=rawReports.map(raw=>{const r=D.decodeReportData(new TextEncoder().encode(raw));if(r.status!=='ready')throw Error(r.code);return r.report;});
    globalThis.views=[]; globalThis.nav=null;
    globalThis.show=report=>{
      nav?.dispose(); for (const v of views) v.dispose(); views=[];
      history.replaceState(null,'','#view=overview');
      const add=(id,v)=>views.push({...v,id,label:id[0].toUpperCase()+id.slice(1),panel:v.element});
      add('overview',overviewModules['overview-view'].createOverviewView(document,report));
      if(report.supportedReportViews.includes('evidence')) add('evidence',overviewModules['evidence-view'].createEvidenceView(document,report.panels.evidence??absent));
      if(report.supportedReportViews.includes('catalog')) add('catalog',overviewModules['catalog-view'].createCatalogView(document,report.panels.catalog??absent,report.panels.descriptions??absent));
      nav=N.createReportNavigation(document,report.supportedReportViews,views);
      mount.replaceChildren(nav.element,...views.map(v=>v.element));
      return true;
    };
    true`);
  await check('all-32-decode-ready', `reports.length===32 && reports.every(r=>{show(r); return views.length>=1 && Object.isFrozen(r);})`);
  await check('old-profile-refuses-without-partial-object', `(()=>{
    const r=D.decodeReportData(new TextEncoder().encode(rawReports[0].replace('opensip.report-projection.development-caps.6','opensip.report-projection.development-caps.5')));
    return r.status==='unavailable' && r.code==='incompatible-profile' && !('report' in r);
  })()`);
  await check('decoded-report-frozen-against-mutation', `(()=>{
    const before=reports[0].schemaFamily;
    reports[0].schemaFamily='mutated';
    return reports[0].schemaFamily===before && Object.isFrozen(reports[0]) && Object.isFrozen(reports[0].panels)
      && Object.isFrozen(reports[0].supportedReportViews);
  })()`);
  await check('only-supported-implemented-views-mounted', `(()=>{
    return reports.every(r=>{
      show(r);
      const mounted=views.map(v=>v.id);
      if(!mounted.includes('overview')) return false;
      if(mounted.includes('evidence')!==r.supportedReportViews.includes('evidence')) return false;
      if(mounted.includes('catalog')!==r.supportedReportViews.includes('catalog')) return false;
      return !mounted.some(id=>id==='findings'||id==='comparison'||id==='graph'||id==='history');
    });
  })()`);
  await check('retained-vs-ephemeral-identity', `(()=>{
    const retained=reports.find(r=>r.panels.evidence?.state==='present' && r.panels.evidence.data.entries.length && 'runId' in r.panels.evidence.data.source);
    const ephemeral=reports.find(r=>r.panels.evidence?.state==='present' && 'planId' in r.panels.evidence.data.source);
    if(!retained||!ephemeral) return false;
    show(retained); nav.select('evidence');
    const a=views.find(v=>v.id==='evidence').element.textContent.includes('Source Run') && !views.find(v=>v.id==='evidence').element.textContent.includes('ephemeral analysis');
    show(ephemeral); nav.select('evidence');
    const t=views.find(v=>v.id==='evidence').element.textContent;
    return a && t.includes('Ephemeral source Plan') && t.includes('no retained Run identifier') && !t.includes('Source Run');
  })()`);
  await check('retained-row-identities-and-recorded-counts', `(()=>{
    const r=reports.find(x=>x.panels.evidence?.state==='present'&&x.panels.evidence.data.entries.length&&'runId' in x.panels.evidence.data.source);
    show(r); nav.select('evidence');
    const d=r.panels.evidence.data; const panel=views.find(v=>v.id==='evidence').element; const row=d.entries[0];
    return panel.textContent.includes(d.source.runId) && panel.textContent.includes(d.source.evidenceId)
      && panel.textContent.includes(row.coverageId)
      && panel.textContent.includes(row.result.entry.confidenceMillionths.toString())
      && panel.textContent.includes(d.entries.length+' of '+d.entriesProjection.total.toString())
      && panel.textContent.includes('do not authorize a repair')
      && Object.isFrozen(d);
  })()`);
  await check('catalog-and-overview-compose-exact-limitations', `(()=>{
    const r=reports.find(x=>x.supportedReportViews.includes('catalog')&&x.panels.catalog?.state==='present');
    if(!r) return false;
    show(r);
    const switched=nav.select('catalog');
    const cat=views.find(v=>v.id==='catalog').element;
    const ov=views.find(v=>v.id==='overview').element;
    return switched && !cat.hidden && ov.hidden && cat.textContent.includes('do not grant permission to execute')
      && ov.textContent.includes(r.reportObservedAt);
  })()`);
  await check('empty-included-rows-not-empty-collection', `(()=>{
    const r=reports.find(x=>x.panels.evidence?.state==='present');
    const state=structuredClone(r.panels.evidence);
    state.data.entries=[];
    state.data.entriesProjection={total:5n,omitted:5n,omissionCause:'item-cap'};
    const v=overviewModules['evidence-view'].createEvidenceView(document,state);
    const t=v.element.textContent; v.dispose();
    return t.includes('No coverage rows are included') && t.includes('source collection is not empty')
      && t.includes('0 of 5') && t.includes('5 source coverage results omitted')
      && t.includes('report item limit');
  })()`);
  await check('zero-collection-distinct-from-omitted-rows', `(()=>{
    const r=reports.find(x=>x.panels.evidence?.state==='present');
    const state=structuredClone(r.panels.evidence);
    state.data.entries=[];
    state.data.entriesProjection={total:0n,omitted:0n,omissionCause:'none'};
    const v=overviewModules['evidence-view'].createEvidenceView(document,state);
    const t=v.element.textContent; v.dispose();
    return t.includes('contains no coverage results') && !t.includes('source collection is not empty');
  })()`);
  await check('exact-integer-examined-subject-count', `(()=>{
    const r=reports.find(x=>x.panels.evidence?.state==='present'&&x.panels.evidence.data.entries.length);
    const state=structuredClone(r.panels.evidence);
    state.data.entries[0].result.entry.examinedUniverse.subjectCount=9007199254740993n;
    const v=overviewModules['evidence-view'].createEvidenceView(document,state);
    const ok=v.element.textContent.includes('9007199254740993'); v.dispose();
    return ok;
  })()`);
  await check('hostile-closed-world-reason-is-text', `(()=>{
    const r=reports.find(x=>x.panels.evidence?.state==='present'&&x.panels.evidence.data.entries.length);
    const state=structuredClone(r.panels.evidence);
    state.data.entries[0].result.entry.closedWorld.reasons=['<img src=x onerror=globalThis.xss=1>'];
    const v=overviewModules['evidence-view'].createEvidenceView(document,state);
    const t=v.element.textContent; const extra=v.element.querySelectorAll('img,a,script').length; v.dispose();
    return t.includes('<img src=x onerror=globalThis.xss=1>') && extra===0 && globalThis.xss!==1;
  })()`);
  await check('unknown-select-does-not-substitute', `(()=>{
    show(reports.find(r=>r.supportedReportViews.includes('evidence')));
    const visible=views.filter(v=>!v.element.hidden).map(v=>v.id);
    const ok=!nav.select('findings');
    return ok && visible.length===1 && visible[0]==='overview';
  })()`);
  await check('unknown-hash-shows-unavailable-without-substitution', `new Promise(r=>{
    show(reports.find(x=>x.supportedReportViews.includes('evidence')));
    location.hash='#view=does-not-exist';
    setTimeout(()=>{
      r(views.every(v=>v.element.hidden) && mount.textContent.includes('requested view is unavailable')
        && document.querySelectorAll('[role=tab][aria-selected=true]').length===0);
    }, 80);
  })`);
  await check('hash-route-closes-hidden-modal-and-restores-tab-focus', `new Promise(r=>{
    const report=reports.find(x=>x.supportedReportViews.includes('evidence'));
    show(report);
    const overview=views.find(v=>v.id==='overview');
    overview.element.querySelector('.report-help>button').click();
    const openBefore=overview.element.querySelectorAll('dialog[open]').length===1;
    const other=views.find(v=>v.id==='evidence');
    location.hash='#view=evidence';
    setTimeout(()=>{
      const tab=document.querySelector('[role=tab][aria-selected=true]');
      r(openBefore && overview.element.querySelectorAll('dialog[open]').length===0 && overview.element.hidden===true
        && !other.element.hidden && document.activeElement===tab);
    }, 80);
  })`);
  await check('no-derived-authority-or-links', `(()=>{ show(reports[0]); return mount.querySelectorAll('a[href]').length===0; })()`);
  await check('dispose-removes-navigation-and-views', `(()=>{
    show(reports[0]); nav.dispose(); nav.dispose(); for (const v of views) { v.dispose(); v.dispose(); }
    return mount.children.length===0 && document.querySelectorAll('dialog:modal').length===0;
  })()`);
  const failed = rows.filter(r => !r.passed).map(r => r.name);
  await writeFile(path.join(ROOT, 'results', 'independent-composition.json'), JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed, cases: rows}, null, 2) + '\n');
  console.log(JSON.stringify({caseCount: rows.length, failedCount: failed.length, failed}));
  if (failed.length) throw Error('composition probes failed');
} catch (e) {
  await writeFile(path.join(OUT, 'failure.json'), JSON.stringify({error: String(e), checks: rows}, null, 2) + '\n'); throw e;
} finally {
  ws?.close(); chrome.kill('SIGTERM');
  await new Promise(r => { chrome.once('exit', r); setTimeout(r, 5000); });
  if (chrome.exitCode === null && chrome.signalCode === null) chrome.kill('SIGKILL');
  await writeFile(path.join(OUT, 'chrome.stderr'), stderr);
}
