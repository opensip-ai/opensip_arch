// Reviewed developer-tool exceptions. This verifies byte selection, not the full
// approval chain; orchestration MUST first run the owned design-lock verifier.
// No repository JavaScript or compiler plugin is executed by this module.
import fs from 'node:fs';
import { isDeepStrictEqual } from 'node:util';
import { canonical, LaneError, pinnedFile, strictJson, validateLaneRecord } from './lane.mjs';

const exact = (value, keys, label) => {
  if (!value || typeof value !== 'object' || Array.isArray(value) ||
      !isDeepStrictEqual(Object.keys(value).sort(), [...keys].sort())) throw new LaneError(`${label}: unexpected fields`);
};
const site = usage => JSON.stringify([usage.file, usage.line, usage.column]);

export function bindToolPolicy({ architecture, designLock, policyPath, root, record, lane }) {
  if (policyPath === undefined) return undefined;
  if (!canonical(policyPath)) throw new LaneError('tool policy path must be architecture-relative');
  if (lane.standing !== 'bound' || lane.policyId !== 'tooling' || record.trustedUsages.length) {
    throw new LaneError('selected tool policy is only for bound tooling with no caller exceptions');
  }
  const lock = strictJson(fs.readFileSync(designLock), 'design lock');
  const selected = [];
  for (const binding of lock.contractSuccessors ?? []) {
    exact(binding, ['record', 'subjectManifest', 'review', 'assent'], 'contract binding');
    const documents = Object.fromEntries(Object.entries(binding).map(([key, pin]) =>
      [key, strictJson(pinnedFile(architecture, pin, `tool policy ${key}`), key)]));
    const member = documents.subjectManifest.files?.find(row => row.path === policyPath);
    if (!member) continue;
    const candidate = documents.record.candidates?.find(row => row.path === policyPath);
    if (!isDeepStrictEqual(member, candidate)) throw new LaneError('tool policy is not a selected candidate member');
    selected.push(member);
  }
  if (selected.length !== 1) throw new LaneError('tool policy must be selected exactly once by contract successors');
  const pin = selected[0];
  const policy = strictJson(pinnedFile(architecture, pin, 'selected tool policy'), 'tool policy');
  exact(policy, ['schemaVersion', 'kind', 'lane', 'files', 'trustedUsages', 'unfollowedDynamicLoaders'], 'tool policy');
  if (policy.schemaVersion !== 1 || policy.kind !== 'reviewed-developer-tool-loaders') throw new LaneError('unsupported tool policy');
  if (!isDeepStrictEqual(policy.lane, record)) throw new LaneError('tool policy lane differs from checked lane');
  // Reuse the closed usage grammar. Caller records remain exception-free.
  validateLaneRecord({ ...record, trustedUsages: policy.trustedUsages });
  if (!policy.trustedUsages.length) throw new LaneError('tool policy must select at least one exact exception');
  const required = [...new Set([...record.inputs, record.manifest, record.tsconfig,
    record.packageManager.lockfile, ...policy.trustedUsages.map(u => u.file)].filter(Boolean))].sort();
  if (!Array.isArray(policy.files) || !isDeepStrictEqual(policy.files.map(p => p.path), required)) {
    throw new LaneError('tool policy must pin exact sorted lane inputs/configuration/lock and exception files');
  }
  for (const file of policy.files) {
    if (!file.path.startsWith(record.packageRoot + '/')) throw new LaneError('tool policy file escapes package');
    pinnedFile(root, file, 'tool policy input');
  }
  const sites = policy.trustedUsages.map(site);
  if (new Set(sites).size !== sites.length) throw new LaneError('duplicate tool policy site');
  for (const usage of policy.trustedUsages) {
    if (policy.files.find(p => p.path === usage.file)?.sha256 !== usage.sha256) throw new LaneError('tool usage file pin differs');
  }
  const unfollowed = policy.trustedUsages.filter(u => u.kind === 'dynamic-loader' && u.targets.length === 0);
  if (!Array.isArray(policy.unfollowedDynamicLoaders) || !isDeepStrictEqual(policy.unfollowedDynamicLoaders.map(site), unfollowed.map(site))) {
    throw new LaneError('unfollowed tool loaders must be explicitly disclosed in usage order');
  }
  for (const declaration of policy.unfollowedDynamicLoaders) {
    exact(declaration, ['file', 'line', 'column', 'limitation'], 'unfollowed loader');
    if (!declaration.file.startsWith(record.packageRoot + '/node_modules/') ||
        declaration.limitation !== 'reviewed-tool-code-outside-statically-enumerated-closure') {
      throw new LaneError('unfollowed loaders are only permitted in pinned external developer-tool code');
    }
  }
  return { pin, trustedUsages: policy.trustedUsages, unfollowedDynamicLoaders: policy.unfollowedDynamicLoaders,
    acceptanceChain: 'Selected member and input bytes verified; tools/verify_design.py owns approval-chain validation.' };
}
