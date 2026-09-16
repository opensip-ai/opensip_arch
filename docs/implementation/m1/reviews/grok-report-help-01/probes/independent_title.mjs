/** Extra CDP case: HTML in the title stays text. Copy of harness pattern; writes only under probes/results. */
import { spawn } from 'node:child_process';
import { readFile, writeFile, mkdir, rm } from 'node:fs/promises';
import { createServer } from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const copy = path.resolve(here, '../copy');
const results = path.resolve(here, '../results');
const profile = path.join(results, 'chrome-profile-title');
await rm(profile, { recursive: true, force: true });
await mkdir(profile, { recursive: true });
const source = await readFile(path.join(copy, 'emitted/help-view.js'), 'utf8');
const css = await readFile(path.join(copy, 'report.css'), 'utf8');
const html = `<!doctype html><html lang="en"><meta charset="utf-8"><title>Title inert</title><style>${css}</style><body><div id="mount"></div><script type="module">${source}
window.fixture = createHelpView(document, '<img src=x onerror="window.titleExecuted=true">', ['plain']);
document.getElementById('mount').append(window.fixture.element);
window.ready = true;
</script></body></html>`;
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
  for (let i = 0; i < 100 && !await evaluate('window.ready === true'); i++) await new Promise(resolve => setTimeout(resolve, 50));
  const observed = await evaluate(`({
    titleExecuted: window.titleExecuted === true,
    img: !!document.querySelector('dialog img, .report-help img'),
    opener: document.querySelector('.report-help > button').textContent,
    label: document.querySelector('dialog').getAttribute('aria-label'),
    heading: document.querySelector('dialog h2').textContent
  })`);
  const passed = observed.titleExecuted === false && observed.img === false
    && observed.opener.includes('<img') && observed.label.includes('<img') && observed.heading.includes('<img');
  await writeFile(path.join(results, 'independent-title.json'), JSON.stringify({ passed, observed }, null, 2) + '\n');
  console.log(JSON.stringify({ passed, observed }));
  if (!passed) process.exit(1);
} finally {
  ws?.close();
  chrome.kill('SIGTERM');
  await new Promise(resolve => { chrome.once('exit', resolve); setTimeout(resolve, 3000); });
  if (chrome.exitCode === null && chrome.signalCode === null) chrome.kill('SIGKILL');
  server.close();
}
