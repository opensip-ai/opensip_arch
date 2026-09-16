// Translates the shared fixture's legacy lane records (author02 schema) and case
// edits into schema-2 lane records for the author-03 checker. Translation is
// mechanical and disclosed:
//  - package ids come from referenceInventoryId; tools/contracts is an unbound
//    tooling trial (no inventory package exists for it);
//  - a legacy edit that changes platforms, conditions or browser roots cannot be
//    expressed (policy is checker-owned), so it is passed through as a forbidden
//    "legacyPlatformOverride" key and the checker must exit 2;
//  - legacy acceptedUnresolved {from, module} entries become exact
//    optional-unresolved records bound to the first guarded runtime usage of that
//    request in that file (else the first usage; else a record that matches nothing).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const top = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const { baseLanes } = await import(path.join(top, 'baseline/subject-02-trial/harness/fixture.mjs'));
const { parse, runtimeUsages } = await import(path.join(top, 'checker/src/usages.mjs'));

const IDS = { report: 'report', provider: 'typescript-provider', contracts: 'tooling' };
const policyShape = lane => JSON.stringify({ browserRoots: lane.browserRoots, groups: lane.runtimeGroups.map(g => [g.name, g.platform, g.conditions]) });

export function laneRecordFor(root, lanes, laneId) {
  const lane = lanes.lanes[laneId];
  const base = baseLanes().lanes[laneId];
  const record = {
    schemaVersion: 2, package: IDS[laneId], packageRoot: lane.packageRoot, manifest: lane.manifest, tsconfig: lane.tsconfig,
    inputs: [...lane.inputs], packageManager: { kind: 'fixture-unlocked', lockfile: null }, trustedUsages: [],
  };
  if (policyShape(lane) !== policyShape(base)) record.legacyPlatformOverride = { browserRoots: lane.browserRoots, groups: lane.runtimeGroups.map(g => ({ name: g.name, platform: g.platform, conditions: g.conditions })) };
  for (const entry of lane.acceptedUnresolved ?? []) record.trustedUsages.push(exactOptional(root, entry));
  return { record, unbound: laneId === 'contracts' ? 'tooling' : undefined };
}

function exactOptional(root, { from, module, reason }) {
  const file = path.join(root, from);
  const text = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';
  const usages = text ? runtimeUsages(parse(file, text)).requests.filter(r => r.request === module) : [];
  const usage = usages.find(u => u.guarded) ?? usages[0];
  return {
    kind: 'optional-unresolved', file: from, sha256: crypto.createHash('sha256').update(text).digest('hex'),
    line: usage?.line ?? 1, column: usage?.column ?? 1, text: usage?.text ?? JSON.stringify(module),
    request: module, mode: usage?.mode ?? 'require', reason: reason || 'translated legacy acceptedUnresolved record',
  };
}
