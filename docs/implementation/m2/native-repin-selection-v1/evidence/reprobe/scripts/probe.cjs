// Adapted for the macOS 27 reprobe (confinement-reprobe-01) from
// opensip_arch/docs/implementation/m1/reviews/generator-confinement-01/scripts/probe.cjs.
// Untrusted generator-input stand-in. Runs inside the same profile as a Node
// generation step and reports what each effect attempt actually did.
const fs = require('node:fs');
const net = require('node:net');
const dgram = require('node:dgram');
const os = require('node:os');
const cp = require('node:child_process');
const cfg = JSON.parse(process.argv[2]);
const result = {};
function attempt(key, action) {
  try { const value = action(); result[key] = value === undefined ? 'ALLOWED' : {ALLOWED: value}; }
  catch (e) { result[key] = e.code || e.message; }
}
attempt('allowedScratchWrite', () => fs.writeFileSync(cfg.scratch + '/probe-ok', 'ok'));
attempt('allowedOutputWrite', () => fs.writeFileSync(cfg.output + '/probe-ok', 'ok'));
attempt('allowedInputRead', () => fs.readFileSync(cfg.input).length);
for (const [name, path] of Object.entries(cfg.outsideReads)) attempt('outsideRead:' + name, () => fs.readFileSync(path).length);
for (const [name, path] of Object.entries(cfg.outsideStats)) attempt('outsideStat:' + name, () => fs.statSync(path).size);
for (const [name, path] of Object.entries(cfg.outsideLists)) attempt('outsideList:' + name, () => fs.readdirSync(path).length);
for (const [name, path] of Object.entries(cfg.outsideWrites)) attempt('outsideWrite:' + name, () => fs.writeFileSync(path, 'no'));
attempt('symlinkEscapeCreate', () => fs.symlinkSync(cfg.outsideReads.canary, cfg.scratch + '/escape'));
attempt('symlinkEscapeRead', () => fs.readFileSync(cfg.scratch + '/escape').length);
attempt('hardlinkEscape', () => fs.linkSync(cfg.outsideReads.canary, cfg.scratch + '/hard'));
attempt('spawnShell', () => cp.spawnSync('/bin/sh', ['-c', 'echo x'], {encoding: 'utf8'}).error?.code ?? 'RAN');
attempt('execSelf', () => cp.execFileSync(process.execPath, ['-e', '1'], {encoding: 'utf8'}));
attempt('envKeys', () => Object.keys(process.env).sort());
attempt('openDescriptors', () => fs.readdirSync('/dev/fd'));
attempt('hostname', () => os.hostname());
attempt('userInfo', () => os.userInfo().username);
attempt('cpuCount', () => os.cpus().length);
attempt('etcPasswdRead', () => fs.readFileSync('/etc/passwd').length);
attempt('tmpdirList', () => fs.readdirSync('/private/tmp').length);
// macOS 27 reprobe additions (not in the macOS 26 matrix): the current rendered
// profile grants writes only strictly below each write root, and denies syslog.
attempt('writeRootRename', () => fs.renameSync(cfg.output, cfg.output + '-renamed'));
const pending = [];
pending.push(new Promise(done => {
  const socket = net.connect({path: '/private/var/run/syslog'});
  socket.on('connect', () => { result.syslogUnixConnect = 'ALLOWED'; socket.destroy(); });
  socket.on('error', e => { result.syslogUnixConnect = e.code; });
  socket.on('close', done);
  setTimeout(() => socket.destroy(), 3000).unref();
}));
pending.push(new Promise(done => {
  const socket = net.connect({host: '127.0.0.1', port: cfg.tcpPort});
  socket.on('connect', () => { result.loopbackTcp = 'ALLOWED'; socket.destroy(); });
  socket.on('error', e => { result.loopbackTcp = e.code; });
  socket.on('close', done);
  setTimeout(() => socket.destroy(), 3000).unref();
}));
pending.push(new Promise(done => {
  const socket = dgram.createSocket('udp4');
  socket.on('error', e => { result.loopbackUdp = e.code; socket.close(); done(); });
  socket.send('probe', cfg.udpPort, '127.0.0.1', e => { result.loopbackUdp = e ? e.code : 'SENT'; socket.close(); done(); });
}));
pending.push(new Promise(done => {
  const server = net.createServer();
  server.on('error', e => { result.listen = e.code; done(); });
  server.listen(0, '127.0.0.1', () => { result.listen = 'ALLOWED'; server.close(done); });
}));
Promise.all(pending).then(() => process.stdout.write(JSON.stringify(result) + '\n'));
