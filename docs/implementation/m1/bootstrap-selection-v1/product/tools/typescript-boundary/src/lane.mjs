// Lane records, the design-lock inventory join and checker-owned platform policy.
// A lane record is caller input: it lists inputs and exact trusted usages but
// cannot choose platforms, package ownership or dependency authority. Those come
// from the inventory selected by the product design lock (verified by pins) and
// from PLATFORM_POLICY below. Acceptance semantics of the selected inventory
// (review/assent chain) are owned upstream by tools/verify_design.py.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';

export class LaneError extends Error {}

export const canonical = value => typeof value === 'string' && value.length > 0 && !value.includes('\\') && !value.includes('\0') &&
  !path.posix.isAbsolute(value) && !value.split('/').some(part => part === '' || part === '.' || part === '..');

// JSON with duplicate-key refusal (same rule as tools/verify_design.py).
export function strictJson(input, label) {
  const s = typeof input === 'string' ? input : input.toString('utf8');
  let i = 0;
  const fail = message => { throw new LaneError(`${label}: ${message} at offset ${i}`); };
  const ws = () => { while (i < s.length && ' \t\n\r'.includes(s[i])) i++; };
  const string = () => {
    const start = i++;
    while (i < s.length && s[i] !== '"') { if (s[i] === '\\') i++; i++; }
    if (s[i] !== '"') fail('unterminated string');
    i++;
    return JSON.parse(s.slice(start, i));
  };
  const value = () => {
    ws();
    if (s[i] === '{') {
      i++;
      const object = {};
      ws();
      if (s[i] === '}') { i++; return object; }
      for (;;) {
        ws();
        if (s[i] !== '"') fail('expected key');
        const key = string();
        if (Object.hasOwn(object, key)) fail('duplicate key ' + key);
        ws();
        if (s[i++] !== ':') fail('expected colon');
        Object.defineProperty(object, key, { value: value(), enumerable: true, writable: true, configurable: true });
        ws();
        if (s[i] === ',') { i++; continue; }
        if (s[i] === '}') { i++; return object; }
        fail('expected comma or closing brace');
      }
    }
    if (s[i] === '[') {
      i++;
      const array = [];
      ws();
      if (s[i] === ']') { i++; return array; }
      for (;;) {
        array.push(value());
        ws();
        if (s[i] === ',') { i++; continue; }
        if (s[i] === ']') { i++; return array; }
        fail('expected comma or closing bracket');
      }
    }
    if (s[i] === '"') return string();
    const token = /^(?:-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null)/.exec(s.slice(i, i + 64));
    if (!token) fail('invalid token');
    i += token[0].length;
    return JSON.parse(token[0]);
  };
  const result = value();
  ws();
  if (i !== s.length) fail('trailing data');
  return result;
}

const exactKeys = (object, keys, label) => {
  if (!object || typeof object !== 'object' || Array.isArray(object)) throw new LaneError(`${label} must be an object`);
  const extra = Object.keys(object).filter(key => !keys.includes(key));
  const missing = keys.filter(key => !Object.hasOwn(object, key));
  if (extra.length || missing.length) throw new LaneError(`${label} keys must be exactly ${keys.join(', ')}` + (extra.length ? `; unexpected ${extra.join(', ')}` : '') + (missing.length ? `; missing ${missing.join(', ')}` : ''));
};
const positive = value => Number.isInteger(value) && value > 0;

export function validateLaneRecord(record) {
  exactKeys(record, ['schemaVersion', 'package', 'packageRoot', 'manifest', 'tsconfig', 'inputs', 'packageManager', 'trustedUsages'], 'lane record');
  if (record.schemaVersion !== 2) throw new LaneError('lane record schemaVersion must be 2');
  if (typeof record.package !== 'string' || !record.package) throw new LaneError('lane record package must name an inventory package id');
  for (const key of ['packageRoot', 'manifest']) if (!canonical(record[key])) throw new LaneError(`lane record ${key} must be a canonical relative path`);
  if (record.tsconfig !== null && !canonical(record.tsconfig)) throw new LaneError('lane record tsconfig must be a canonical relative path or null');
  if (!Array.isArray(record.inputs) || !record.inputs.length || !record.inputs.every(canonical)) throw new LaneError('lane record inputs must be canonical relative paths');
  exactKeys(record.packageManager, ['kind', 'lockfile'], 'lane record packageManager');
  const { kind, lockfile } = record.packageManager;
  if (!['npm', 'pnpm', 'fixture-unlocked'].includes(kind)) throw new LaneError('packageManager kind must be npm, pnpm or fixture-unlocked');
  if (kind === 'fixture-unlocked' ? lockfile !== null : !canonical(lockfile)) throw new LaneError('packageManager lockfile must be a canonical path for npm/pnpm and null for fixture-unlocked');
  if (!Array.isArray(record.trustedUsages)) throw new LaneError('lane record trustedUsages must be an array');
  for (const usage of record.trustedUsages) {
    const common = ['kind', 'file', 'sha256', 'line', 'column', 'text', 'reason'];
    if (usage?.kind === 'dynamic-loader') exactKeys(usage, [...common, 'targets'], 'dynamic-loader trusted usage');
    else if (usage?.kind === 'optional-unresolved') exactKeys(usage, [...common, 'request', 'mode'], 'optional-unresolved trusted usage');
    else throw new LaneError('trusted usage kind must be dynamic-loader or optional-unresolved');
    if (!canonical(usage.file) || !/^[0-9a-f]{64}$/.test(usage.sha256) || !positive(usage.line) || !positive(usage.column) ||
      typeof usage.text !== 'string' || !usage.text || typeof usage.reason !== 'string' || !usage.reason) {
      throw new LaneError('trusted usage needs a canonical file, lowercase sha256, positive line/column, text and reason');
    }
    if (usage.kind === 'dynamic-loader' && (!Array.isArray(usage.targets) || !usage.targets.every(canonical))) throw new LaneError('dynamic-loader targets must be canonical paths');
    if (usage.kind === 'optional-unresolved' && (typeof usage.request !== 'string' || !usage.request || !['import', 'require'].includes(usage.mode))) {
      throw new LaneError('optional-unresolved usage needs a request and an import/require mode');
    }
  }
  return record;
}

export function pinnedFile(architecture, pin, label) {
  exactKeys(pin, ['path', 'sha256', 'bytes'], label);
  if (!canonical(pin.path) || !/^[0-9a-f]{64}$/.test(pin.sha256) || !Number.isInteger(pin.bytes) || pin.bytes < 0) throw new LaneError(`${label} pin is malformed`);
  let current = architecture;
  for (const part of pin.path.split('/')) {
    current = path.join(current, part);
    const stat = fs.lstatSync(current, { throwIfNoEntry: false });
    if (!stat) throw new LaneError(`${label} pinned file missing: ${pin.path}`);
    if (stat.isSymbolicLink()) throw new LaneError(`${label} pinned path contains a symlink: ${pin.path}`);
  }
  const raw = fs.readFileSync(current);
  if (raw.length !== pin.bytes || crypto.createHash('sha256').update(raw).digest('hex') !== pin.sha256) throw new LaneError(`${label} pinned bytes differ: ${pin.path}`);
  return raw;
}

export function bindInventory({ architecture, designLock }) {
  const lockRaw = fs.readFileSync(designLock);
  const lock = strictJson(lockRaw, 'design lock');
  const successors = lock.inventorySuccessors;
  if (!Array.isArray(successors) || !successors.length) throw new LaneError('design lock selects no inventory successor');
  let binding, raw, previous;
  const inputs = Array.isArray(lock.inputs) ? lock.inputs : [];
  for (const item of successors) {
    binding = item;
    exactKeys(binding, ['parent', 'candidate', 'record', 'review', 'assent'], 'inventory successor binding');
    raw = {};
    for (const key of Object.keys(binding)) raw[key] = pinnedFile(architecture, binding[key], `inventory ${key}`);
    if (previous ? !isDeepStrictEqual(binding.parent, previous) : !inputs.some(row => isDeepStrictEqual(row, binding.parent))) {
      throw new LaneError('inventory parent is not the selected base input or immediate predecessor');
    }
    previous = binding.candidate;
  }
  const inventory = strictJson(raw.candidate, 'selected inventory');
  if (!Array.isArray(inventory.packages) || !Array.isArray(inventory.files)) throw new LaneError('selected inventory lacks packages or files');
  return {
    designLockSha256: crypto.createHash('sha256').update(lockRaw).digest('hex'),
    selectedInventory: binding.candidate,
    pinsVerified: Object.keys(binding),
    inventorySuccessorsVerified: successors.length,
    inventoryStanding: inventory.standing,
    acceptanceChain: 'pins verified by bytes; review/assent semantics are owned by tools/verify_design.py and are not re-evaluated here',
    inventory,
  };
}

const RUNTIME = ['dependencies', 'optionalDependencies', 'peerDependencies'];
const ALL = [...RUNTIME, 'devDependencies'];

// Checker-owned platform policy keyed by inventory package id (chapter 14 and
// the build plan's lane table). Groups are matched in order against the path
// relative to the package root; the first match wins.
export const PLATFORM_POLICY = {
  report: [
    { name: 'browser-runtime', platform: 'browser', match: rel => rel.startsWith('src/'), runtimeClasses: RUNTIME },
    { name: 'node-build-scripts', platform: 'node', match: () => true, runtimeClasses: ALL },
  ],
  'typescript-provider': [
    { name: 'node-build-scripts', platform: 'node', match: rel => rel.startsWith('scripts/'), runtimeClasses: ALL },
    { name: 'node-provider-runtime', platform: 'node', match: () => true, runtimeClasses: RUNTIME },
  ],
  tooling: [
    { name: 'node-tooling', platform: 'node', match: () => true, runtimeClasses: ALL },
  ],
};

export function resolveLane({ record, binding, unboundKind }) {
  const pkg = binding.inventory.packages.find(p => p && p.id === record.package);
  const toolingSubpackage = pkg?.id === 'tooling' && pkg.kind === 'tooling' &&
    record.packageRoot.startsWith(pkg.path + '/') &&
    binding.inventory.files.some(row => row.package === pkg.id && row.path === record.manifest && row.role === 'manifest');
  const boundMatch = pkg && (pkg.path === record.packageRoot || toolingSubpackage) && ['typescript-package', 'tooling'].includes(pkg.kind);
  let standing;
  let policyId;
  if (boundMatch && unboundKind) {
    throw new LaneError('--unbound-lane given for a lane the selected inventory binds');
  } else if (boundMatch) {
    standing = 'bound';
    policyId = pkg.id;
  } else if (unboundKind) {
    if (binding.inventory.packages.some(p => p && typeof p.path === 'string' && p.path !== '' && !(p.id === 'tooling' && p.path === 'tools' && record.package === 'tooling' && record.packageRoot.startsWith('tools/')) && (p.path === record.packageRoot || p.path.startsWith(record.packageRoot + '/') || record.packageRoot.startsWith(p.path + '/')))) throw new LaneError('unbound trial lanes cannot overlap an inventory package root');
    if (unboundKind !== 'tooling' || record.package !== 'tooling') throw new LaneError('only tooling lanes may run unbound, and they must name package tooling');
    standing = 'unbound-trial';
    policyId = 'tooling';
  } else {
    throw new LaneError(`lane ${record.package} at ${record.packageRoot} is not a typescript-package or tooling package of the selected inventory`);
  }
  if (!PLATFORM_POLICY[policyId]) throw new LaneError(`no platform policy for inventory package ${policyId}`);
  const inventoryDependencies = pkg && boundMatch ? pkg.dependencies : [];
  const rows = boundMatch ? binding.inventory.files.filter(f => f.package === pkg.id && f.path.startsWith(record.packageRoot + '/')).map(f => f.path) : [];
  return { standing, policyId, groups: PLATFORM_POLICY[policyId], inventoryDependencies, inventoryRows: rows };
}

export function localPackageNames(root, binding, ownManifest) {
  const names = new Set();
  for (const pkg of binding.inventory.packages) {
    if (!pkg || !['typescript-package', 'tooling'].includes(pkg.kind) || typeof pkg.path !== 'string') continue;
    const manifest = path.join(root, pkg.path, 'package.json');
    if (!fs.existsSync(manifest)) continue;
    try {
      const name = JSON.parse(fs.readFileSync(manifest, 'utf8')).name;
      if (typeof name === 'string') names.add(name);
    } catch { /* other lanes' malformed manifests do not block this lane */ }
  }
  if (typeof ownManifest.name === 'string') names.add(ownManifest.name);
  return names;
}
