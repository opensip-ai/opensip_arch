import { spawn } from 'node:child_process';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url));
const profile = path.join(root, 'chrome-profile');
await mkdir(profile);
const source = await readFile(path.join(root, 'emitted/help-view.js'), 'utf8');
const css = await readFile('/Users/sb/code/opensip-ai/opensip/apps/report/src/report.css', 'utf8');
const html = `<!doctype html><html lang="en"><meta charset="utf-8"><title>Help control test</title><style>${css}</style><body><main><h1>Evidence</h1><button id="before">Before help</button><div id="mount"></div><button id="after">After help</button></main><script type="module">${source}
window.fixture = createHelpView(document, 'Evidence scope', ['Unknown callers remain unknown.', '<img src=x onerror="window.untrustedExecuted=true">']);
document.getElementById('mount').append(window.fixture.element);
window.ready = true;
</script></body></html>`;
await writeFile(path.join(root, 'fixture.html'), html);
const server = createServer((req, res) => {
  res.writeHead(req.url === '/' ? 200 : 404, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(req.url === '/' ? html : 'Not found');
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless=new', '--no-first-run', '--no-default-browser-check',
  '--disable-background-networking', '--disable-component-update',
  '--remote-debugging-port=0', `--user-data-dir=${profile}`, 'about:blank',
], { stdio: ['ignore', 'pipe', 'pipe'] });
let stderr = ''; chrome.stderr.on('data', data => { stderr += data; });
chrome.stdout.resume();
const rows = [];
let ws;
try {
  let port;
  for (let i = 0; i < 200; i++) {
    try { port = Number((await readFile(path.join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]); break; }
    catch { await new Promise(resolve => setTimeout(resolve, 100)); }
  }
  if (!port) throw new Error('Chrome did not start');
  const tab = await (await fetch(`http://127.0.0.1:${port}/json/new?${encodeURIComponent(`http://127.0.0.1:${server.address().port}/`)}`, { method: 'PUT' })).json();
  ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => { ws.addEventListener('open', resolve, { once: true }); ws.addEventListener('error', reject, { once: true }); });
  let next = 1;
  const pending = new Map();
  ws.addEventListener('message', event => {
    const message = JSON.parse(event.data);
    const call = pending.get(message.id);
    if (call) { pending.delete(message.id); message.error ? call.reject(message.error) : call.resolve(message.result); }
  });
  function send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = next++; pending.set(id, { resolve, reject }); ws.send(JSON.stringify({ id, method, params }));
    });
  }
  async function evaluate(expression) {
    const result = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
    return result.result.value;
  }
  async function check(name, expression) {
    const passed = await evaluate(expression);
    rows.push({ name, passed });
    if (passed !== true) { await writeFile(path.join(root, 'failure-dom.json'), JSON.stringify(await evaluate(`({html:document.body.innerHTML,active:document.activeElement.outerHTML,focused:document.hasFocus(),events:window.keyEvents})`), null, 2)); throw new Error(name); }
  }
  async function key(key, code, virtual) {
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key, code, windowsVirtualKeyCode: virtual, ...(key === 'Enter' ? {text: '\r', unmodifiedText: '\r'} : {}) });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key, code, windowsVirtualKeyCode: virtual });
    await evaluate('new Promise(resolve => setTimeout(resolve, 50))');
  }
  for (let i = 0; i < 100 && !await evaluate('window.ready === true'); i++) await new Promise(resolve => setTimeout(resolve, 50));
  await send('Page.bringToFront');
  await evaluate(`window.keyEvents=[]; for(const name of ['keydown','keyup','click','focusin']) document.addEventListener(name,e=>window.keyEvents.push({type:e.type,key:e.key,target:e.target.outerHTML}),true)`);
  const browser = await send('Browser.getVersion');
  await check('repository text stays text', `!window.untrustedExecuted && !document.querySelector('dialog img') && document.querySelector('dialog p:last-of-type').textContent.startsWith('<img')`);
  await evaluate(`document.querySelector('.report-help > button').focus()`);
  await key('Enter', 'Enter', 13);
  await check('keyboard opens labelled modal and focuses close', `document.querySelector('dialog').matches(':modal') && document.querySelector('dialog').getAttribute('aria-label') === 'About Evidence scope' && document.activeElement.textContent === 'Close help'`);
  await key('Tab', 'Tab', 9);
  // A modal may cycle through browser chrome; outside document controls remain inert.
  await check('tab cannot focus background buttons', `!['before', 'after'].includes(document.activeElement.id)`);
  await key('Escape', 'Escape', 27);
  await check('escape closes and returns focus', `!document.querySelector('dialog').open && document.activeElement === document.querySelector('.report-help > button')`);
  await key('Enter', 'Enter', 13);
  await evaluate(`document.querySelector('dialog button').click(); new Promise(resolve => setTimeout(resolve, 50))`);
  await check('close control returns focus', `!document.querySelector('dialog').open && document.activeElement === document.querySelector('.report-help > button')`);
  await key('Enter', 'Enter', 13);
  const ax = await send('Accessibility.getFullAXTree');
  await writeFile(path.join(root, 'accessibility-tree.json'), JSON.stringify(ax, null, 2));
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  await writeFile(path.join(root, 'help.png'), Buffer.from(shot.data, 'base64'));
  await evaluate(`window.fixture.dispose(); window.fixture.dispose()`);
  await check('dispose closes and removes controls idempotently', `!document.querySelector('dialog') && !document.querySelector('.report-help')`);
  await writeFile(path.join(root, 'result.json'), JSON.stringify({ passed: true, browser, checks: rows, limits: 'One Chrome headless DOM/keyboard lane only; not screen-reader, contrast, supported-browser, final CSP/bundle or report qualification.' }, null, 2));
  console.log(JSON.stringify({ passed: true, checks: rows.length, browser: browser.product }));
} catch (error) {
  await writeFile(path.join(root, 'failure.json'), JSON.stringify({ error: String(error), checks: rows }, null, 2));
  throw error;
} finally {
  ws?.close();
  chrome.kill('SIGTERM');
  await new Promise(resolve => { chrome.once('exit', resolve); setTimeout(resolve, 5000); });
  if (chrome.exitCode === null && chrome.signalCode === null) chrome.kill('SIGKILL');
  server.close();
  await writeFile(path.join(root, 'chrome.stderr'), stderr);
}
