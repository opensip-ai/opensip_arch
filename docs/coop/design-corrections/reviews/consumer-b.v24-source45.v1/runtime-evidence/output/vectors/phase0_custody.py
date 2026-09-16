"""Phase 0: input custody, five-contract index, source-map scope, CVE1 type availability."""
import hashlib
import json
import os
import sys

sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/tools')
import status as S

ROOT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/'
SUBJ = ROOT + 'subject/'
# HC-43 (source41), HC-49 (source42), HC-55 (source43), HC-56 (source44) and HC-59 (source45): the ported tool asserted the prior kit hashes; the
# source45 expectations are the user-supplied values (source44: a3a5fba8... / e873c8db...; source43: 6d8912f4... / db43ee76...)
EXPECT_MANIFEST = '707715363ac6249e22a4eb30a628ac61f6e951d2d8de71cc8641cfdeb7a6ee69'
EXPECT_PARENT = '8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155'

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
    "runtime": "consumer-b.v24-source45.v1",
    "copiedFromRuntime": ("consumer-b.v24-source44.v1 (completed pass on the source44 kit; its output/ copied exactly by the root; exact source44 final bytes "
                          "preserved at preserved/s44-final/ before executable code was rebound by rebind_s45.py). That output descended from "
                          "consumer-b.v24-source43.v1 (rebind_s44.py), consumer-b.v24-source42.v3 (rebind_s43.py), consumer-b.v24-source42.v2 (rebind_v3.py) "
                          "and consumer-b.v24-source42.v1 (rebind_v2.py)"),
    "freshOrigin": ("continuation of the same original fresh blind origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 in a new runtime over the source42 kit; "
                    "fresh-origin independence is NOT claimed anew. consumer-b.v24, source39.v1-v3 and source41.v1 are read-only own history "
                    "(preserved/source41-v1/manifest.json and the histories preserved inside it); no prior result is current-source conformance. "
                    "Own helper code ported from source41.v1 with only the runtime root rebound (port-manifest.json), executed unchanged first "
                    "(preserved/s42-original-state/manifest.json), then corrected as HC-47 onward (tools/hc_source42.py)"),
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
prior_rows = S.OUT + 'preserved/s44-final/vectors/phase0-custody.json'  # source45: prior own custody rows are my source44 rows (read-only copy)
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
S.set_status(st, 'S-CONTINUATION', 'executed', notes='Same origin continued over the source42 kit in runtime source42.v1 (incomplete: no checkpoint or review written), completed in source42.v2 from its byte-identical copied output, and continued in source42.v3 from the byte-identical v2 output for the bounded provider-trace payload obligation (HC-53); then continued on the source43 kit in runtime source43.v1 from the exact source42.v3 output (one changed kit member, the query projection contract; HC-54/HC-55); then continued on the source44 kit in runtime source44.v1 from the exact source43.v1 output (six changed and three added kit members, all provider wire/startup owners; HC-56..HC-58); then continued on the source45 kit in runtime source45.v1 from the exact source44.v1 output (three changed kit members: native-evidence.md, provider-startup.schemas.v1.json and the provider return schema; HC-59/HC-60); source42.v1/v2/v3, source43.v1 and source44.v1 runtimes and own consumer-b.v24, source39.v1-v3 and source41.v1 outputs preserved read-only; unchanged ported helpers executed and preserved before any correction; checkpoints written per phase with unioned ID sets.')
S.save_status(st)
delta = out["kitDeltaFromPriorOwnCustodyRows"] or {}
cp = S.write_checkpoint(0, st, ['vectors/phase0-custody.json', 'notes/00-session-standing.md', 'notes/01-source42-law-deltas.md', 'port-manifest.json',
                                'preserved/source41-v1/manifest.json', 'preserved/s42-original-state/manifest.json', 'preserved/pre-s42/manifest.json',
                                'rebind-v3-manifest.json', 'preserved/s42-v2-final/manifest.json', 'rebind-s43-manifest.json', 'preserved/s42-v3-final/manifest.json',
                                's43-kit-delta.json', 'rebind-s44-manifest.json', 'preserved/s43-final/manifest.json', 'preserved/s43-final/results-manifest.json',
                                's44-kit-delta.json', 'preserved/s44-final/manifest.json', 'preserved/s44-final/results-manifest.json', 'rebind-s45-manifest.json',
                                's45-kit-delta.json', 'selfcheck/s45-s44-arithmetic-reconciliation.json'], ['HC-49', 'HC-52', 'HC-55', 'HC-56', 'HC-59'],
                        f"Manifest PASS in runtime source45.v1 ({len(m['files'])} files; parent field equal to the supplied frozen manifest). Against my own "
                        f"source44 custody rows: changed {delta.get('changed')}, added {delta.get('added')}, removed {delta.get('removed')} (orientation only). "
                        f"Five contracts, source map and CVE1 selector read from kit. Governance records absent and unused.")
print(json.dumps({"manifest": out['manifest']['result'], "executed": len(cp['requirementIdsExecuted']),
                  "unexecuted": len(cp['requirementIdsUnexecuted'])}))
