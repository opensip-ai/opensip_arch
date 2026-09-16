"""Phase 0: input custody, five-contract index, source-map scope, CVE1 type availability."""
import hashlib
import json
import os
import sys

sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/output/tools')
import status as S

ROOT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/'
SUBJ = ROOT + 'subject/'
# HC-43 (source41): the ported tool asserted the source39 kit hashes; the source41 expectations are the user-supplied values
EXPECT_MANIFEST = '31369cc8c3b71e559c50f107104daff4d6d428e20fb75dc1e3914a2acc1ec6dd'
EXPECT_PARENT = 'eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236'

mb = open(SUBJ + 'consumer-input-manifest.json', 'rb').read()
m = json.loads(mb)
rows, failures = [], []
listed = set()
for f in m['files']:
    b = open(SUBJ + f['path'], 'rb').read()
    ok_sha = hashlib.sha256(b).hexdigest() == f['sha256']
    ok_len = len(b) == f['bytes']
    rows.append({"path": f['path'], "sha256": f['sha256'], "bytes": f['bytes'], "shaOk": ok_sha, "lengthOk": ok_len})
    if not (ok_sha and ok_len):
        failures.append(f['path'])
    listed.add(f['path'])
unlisted = []
for d, _, fs in os.walk(SUBJ):
    for x in fs:
        rel = os.path.relpath(os.path.join(d, x), SUBJ)
        if rel != 'consumer-input-manifest.json' and rel not in listed:
            unlisted.append(rel)
manifest_sha = hashlib.sha256(mb).hexdigest()
assert manifest_sha == EXPECT_MANIFEST, manifest_sha
assert m['parentSubjectSha256'] == EXPECT_PARENT
assert not failures and not unlisted

ri = json.load(open(SUBJ + 'docs/coop/artifacts/resolved-inputs.v2.json'))
cve1 = ri['planIdContract']['canonicalValueEncoding']
assert cve1['name'] == 'CVE1' and len(cve1['closedTypes']) == 8
assert set(cve1['closedTypes']) == set(cve1['encodings'].keys())

readme = open(SUBJ + 'docs/v2/contracts/product-v1/README.md').read()
five = ['identity-and-evidence.md', 'security-and-lifecycle.md', 'native-evidence.md',
        'workflows-and-surfaces.md', 'admission-and-qualification.md']
for n in five:
    assert n in readme, n
    assert os.path.exists(SUBJ + 'docs/v2/contracts/product-v1/' + n)
excluded_governance = ['docs/coop/design-corrections/README.md', 'docs/v2/architecture/08-decision-and-readiness-register.md']
governance_absent = {p: not os.path.exists(SUBJ + p) for p in excluded_governance}

out = {
    "consumerId": "consumer-b.v24",
    "runtime": "consumer-b.v24-source41.v1",
    "freshOrigin": ("continuation of the same original fresh blind origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 in a new runtime over the source41 kit; "
                    "fresh-origin independence is NOT claimed anew. consumer-b.v24 and source39.v1/v2/v3 are read-only own history "
                    "(preserved/consumer-b.v24-output.manifest.json, preserved/source39-v3/manifest.json); no prior result is current-source conformance. "
                    "Own helper code ported from source39.v3 with only the runtime root rebound (port-manifest.json), executed unchanged first "
                    "(preserved/s41-original-state/manifest.json), then corrected as HC-39 onward (tools/hc_source41.py)"),
    "manifest": {"sha256": manifest_sha, "expected": EXPECT_MANIFEST, "bytes": len(mb),
                 "parentSubjectSha256Field": m['parentSubjectSha256'], "parentExpected": EXPECT_PARENT,
                 "parentBytesAvailable": False,
                 "fileCount": len(m['files']), "failures": failures, "unlistedFiles": unlisted,
                 "result": "PASS"},
    "fileRows": rows,
    "fiveContracts": {"index": "docs/v2/contracts/product-v1/README.md", "contracts": five,
                      "successorRule": "README: 'a current explicit successor wins over the named inherited selector only within its declared scope'; each contract's section 0 / superseded-selector table applied (native s0, workflows s0, security S1 table, identity s1)"},
    "sourceMapScope": {"document": "docs/coop/design-corrections/current-source-map.proposed.md",
                       "governanceRecordsExcludedFromKit": governance_absent,
                       "usedAsRecipe": False,
                       "note": "Readiness/review/correction-record governance files are absent from the kit and were not used as semantic recipes; links to them inside contract prose were not followed."},
    "cve1TypesAvailable": {"selector": "docs/coop/artifacts/resolved-inputs.v2.json#/planIdContract/canonicalValueEncoding",
                           "closedTypes": cve1['closedTypes'], "encodings": cve1['encodings'],
                           "constraints": cve1['constraints']},
    "profile": {"evaluatorOutputMajor": 3, "policy": "PolicyDocumentV2 / RuleProgramV2",
                "unchangedNativeInputMajors": ["snapshot2", "plan2", "closure2", "import2", "fact2", "coverage2", "view2", "exec-plan2", "finding-key2"],
                "outputMajors": ["subject3", "finding3", "proof3", "evidence3", "seal3", "run3", "policy-derivation3"],
                "selectedOwners": {"identity": "foundation/identity-schemas.v3.json",
                                   "workflow": "workflows/schemas/evaluator3/ + command-inventory.v3.json",
                                   "capabilityRegistry": "native/capability-manifest-domains.v2.json",
                                   "attribution": "foundation/target-attribution.schema.v2.json",
                                   "graphQuery": "workflows/query-projection-contract.v3.md + evaluator3/graph-query.schema.json"}},
    "custodyGaps": [],
    "countDiscrepancy": None,
    "kitDeltaFromPriorOwnCustodyRows": None,
}
prior_rows = S.OUT + 'preserved/source39-v3/vectors/phase0-custody.json'  # source41: prior own custody rows are the source39.v3 rows (read-only copy)
if os.path.exists(prior_rows):
    old = {r['path']: r['sha256'] for r in json.load(open(prior_rows))['fileRows']}
    new = {r['path']: r['sha256'] for r in rows}
    out["kitDeltaFromPriorOwnCustodyRows"] = {"added": sorted(set(new) - set(old)), "removed": sorted(set(old) - set(new)),
                                             "changed": sorted(p for p in set(new) & set(old) if new[p] != old[p]),
                                             "unchanged": sum(1 for p in set(new) & set(old) if new[p] == old[p]),
                                             "note": "orientation only: prior results do not establish current conformance"}
S.dump('vectors/phase0-custody.json', out)

st = S.load_status()
for rid in ['S-FRESH-ORIGIN', 'S-NOT-PRODUCT', 'S-KIT-ONLY', 'S-MANIFEST-VERIFY', 'S-NO-ORACLE',
            'S-MISSING-DEP-IS-CUSTODY', 'S-PROFILE-CURRENT', 'S-CONTINUATION',
            'R-FIVE-CONTRACTS-INDEX', 'R-SOURCE-MAP-SCOPE', 'R-CVE1-TYPES-AVAILABLE']:
    S.set_status(st, rid, 'executed', artifact='vectors/phase0-custody.json')
S.set_status(st, 'S-NOT-PRODUCT', 'executed', notes='Output confined to output/; kit re-hash repeated at final phase.')
S.set_status(st, 'S-FRESH-ORIGIN', 'executed', notes='Continuation of origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514; independence not claimed anew (notes/00-session-standing.md).')
S.set_status(st, 'S-CONTINUATION', 'executed', notes='Same origin continued in runtime source41.v1 over the source41 kit; own consumer-b.v24 and source39.v1-v3 outputs preserved read-only; unchanged ported helpers executed and preserved before any correction; checkpoints written per phase with unioned ID sets.')
S.save_status(st)
delta = out["kitDeltaFromPriorOwnCustodyRows"] or {}
cp = S.write_checkpoint(0, st, ['vectors/phase0-custody.json', 'notes/00-session-standing.md', 'notes/01-source41-law-deltas.md', 'port-manifest.json',
                                'preserved/source39-v3/manifest.json', 'preserved/consumer-b.v24-output.manifest.json',
                                'preserved/s41-original-state/manifest.json', 'preserved/pre-s41/manifest.json'], ['HC-43'],
                        f"Manifest PASS in runtime source41.v1 ({len(m['files'])} files; parent field equal to the supplied frozen manifest). Against my own "
                        f"source39.v3 custody rows: changed {delta.get('changed')}, added {delta.get('added')}, removed {delta.get('removed')} (orientation only). "
                        f"Five contracts, source map and CVE1 selector read from kit. Governance records absent and unused.")
print(json.dumps({"manifest": out['manifest']['result'], "executed": len(cp['requirementIdsExecuted']),
                  "unexecuted": len(cp['requirementIdsUnexecuted'])}))
