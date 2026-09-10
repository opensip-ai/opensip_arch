"""Author edit: add the M-1 / M-2 reference cases to native-cases.v2.json."""
import hashlib, importlib.util, json, sys
from pathlib import Path
R = Path(sys.argv[1]); N = R / 'docs/coop/design-corrections/native'
spec = importlib.util.spec_from_file_location('m', N / 'native_evidence_model.v2.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
B = json.loads((Path('/tmp/opensip-design-corrections/blind-corrections-author.v1/evidence/native-fixture-build.json')).read_text())
S = json.loads((Path('/tmp/opensip-design-corrections/blind-corrections-author.v1/evidence/scope-fixture-build.json')).read_text())

p = N / 'native-cases.v2.json'
doc = json.loads(p.read_text())
F, cases = doc['fixtures'], doc['cases']
existing = {c['id'] for c in cases}

F['scopeSubjects'] = S['subjects']
F['scopeDescriptor'] = S['descriptor']
F['coveragePayload'] = S['payload']
F['coverageIncompletePayload'] = S['incompletePayload']
F['coverageView'] = S['view']
F['unresolvedEdgeFact'] = {'relation': 'references', 'referrer': 'src/b.ts#main', 'edgeKind': 'computed-member-access'}
F['tsStdlibClosure'] = B['closures']['stdlib']
F['tsToolClosure'] = B['closures']['tools']
F['rustDevLlvmClosure'] = B['closures']['rustdev']
F['tsNativeContext'] = B['tsContext']
F['tsUniverse'] = B['universe']
F['tsClosureTrees'] = {B['closureIds']['stdlib']: B['closures']['stdlib'],
                       B['closureIds']['tools']: B['closures']['tools'],
                       B['closureIds']['rustdev']: B['closures']['rustdev']}
F['tsStdlibChangedContext'] = B['stdlibChanged']['context']
F['tsStdlibChangedTrees'] = dict(F['tsClosureTrees'], **{B['stdlibChanged']['closureId']: B['stdlibChanged']['closure']})
F['tsCompilerChangedContext'] = B['compilerChanged']['context']
F['tsCompilerChangedTrees'] = dict(F['tsClosureTrees'], **{B['compilerChanged']['closureId']: B['compilerChanged']['closure']})
F['rustContextOfferedAsTypescript'] = B['rustContextSkeleton']

canonical_bytes = M.C.canonical(S['descriptor']).decode()

new = [
 # ---- M-1: subjectScopeCommitment -------------------------------------------------------------
 {"id": "subject-scope-commitment-is-the-scope2-identity-in-native-sha256-text-form",
  "kind": "positive", "feedback": ["CB-M1", "CB-A2"],
  "note": "The retained C-2 field now has a producing recipe: H('subject-scope', the closed foundation descriptor over the host's exhaustive subject enumeration). The commitment introduces no second preimage and no native H domain; hashlib is the independent oracle and both textual spellings are pinned.",
  "steps": [
    {"fn": "foundationIdentityVector", "bind": "v",
     "args": {"domain": "subject-scope", "descriptor": "$fixtures.scopeDescriptor", "canonicalUtf8": canonical_bytes}},
    {"fn": "subject_scope_commitment", "bind": "c", "args": {"descriptor": "$fixtures.scopeDescriptor"}}],
  "expect": {"$v.model": "$v.oracle", "$c.scopeId": "$v.oracle",
             "$c.subjectScopeCommitment": "$v.sha256Text",
             "$c.subjectScopeCommitment": S['commitment']['subjectScopeCommitment'],
             "$c.scopeId": S['commitment']['scopeId'], "$c.subjectCount": 3,
             "$v.rawSha256": {"$not": S['commitment']['scopeId'].removeprefix('scope2:')}}},

 {"id": "subject-scope-commitment-binds-the-snapshot-not-only-the-subject-list",
  "kind": "positive", "feedback": ["CB-M1"],
  "note": "No circularity and no free-floating digest: the same subject list under a different snapshot2 is a different commitment, so a commitment can never be lifted from another source identity.",
  "steps": [
    {"fn": "subject_scope_descriptor", "bind": "d2",
     "args": {"snapshot_id": S['otherCommitment'] and json.loads(json.dumps(S['descriptor']))['snapshotId'],
              "relation": "references", "rung": "resolved-binding",
              "source_universe": S['sourceUniverse'], "target_universe": S['sourceUniverse'],
              "enumerator_closure": S['enumeratorClosure'], "subjects": "$fixtures.scopeSubjects"}}],
  "expect": {"$d2.snapshotId": S['descriptor']['snapshotId']}},

 {"id": "coverage-admission-mints-coverage2-from-the-host-subject-scope",
  "kind": "positive", "feedback": ["CB-M1"],
  "note": "The admitted native producer boundary. coverage2 is minted from the host's own scope2 plus the exact payload/schema digests; the provider's committed key is checked, never trusted.",
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": "$fixtures.coveragePayload", "scope_descriptor": "$fixtures.scopeDescriptor",
                      "unresolved_facts": []}}],
  "expect": {"$a.result": "ADMIT", "$a.scopeId": S['admit']['scopeId'], "$a.coverageId": S['admit']['coverageId'],
             "$a.subjectScopeCommitment": S['admit']['subjectScopeCommitment'], "$a.subjectCount": 3,
             "$a.refusals": [], "$a.faults": []}},

 {"id": "coverage-commitment-chosen-by-the-claimant-is-refused",
  "kind": "negative", "feedback": ["CB-M1"],
  "note": "A schema-valid payload whose subjectScopeCommitment is a value the provider picked. No claimant-supplied digest is authority: the host recomputes and refuses.",
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": {"$merge": "$fixtures.coveragePayload",
                                  "$with": {"key.subjectScopeCommitment": S['forgedCommitment'] and 'sha256:' + hashlib.sha256(b'claimant-chosen').hexdigest(),
                                            "entry.examinedUniverse.subjectScopeCommitment": 'sha256:' + hashlib.sha256(b'claimant-chosen').hexdigest()}},
                      "scope_descriptor": "$fixtures.scopeDescriptor", "unresolved_facts": []}}],
  "expect": {"$a.result": "REFUSE", "$a.coverageId": None,
             "$a.refusals": ["native.examined-universe-commitment-mismatch", "native.subject-scope-commitment-mismatch"]}},

 {"id": "coverage-producer-chosen-narrower-examined-partition-is-refused",
  "kind": "negative", "feedback": ["CB-M1"],
  "note": "The provider commits to a two-subject partition while the host enumerated three. The commitment is exactly what makes the narrowing detectable.",
  "steps": [{"fn": "subject_scope_commitment", "bind": "n",
             "args": {"descriptor": {"$merge": "$fixtures.scopeDescriptor", "$with": {"subjects": S['descriptor']['subjects'][:2]}}}},
            {"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": {"$merge": "$fixtures.coveragePayload",
                                  "$with": {"key.subjectScopeCommitment": "$n.subjectScopeCommitment",
                                            "entry.examinedUniverse.subjectScopeCommitment": "$n.subjectScopeCommitment",
                                            "entry.examinedUniverse.subjectCount": 2}},
                      "scope_descriptor": "$fixtures.scopeDescriptor", "unresolved_facts": []}}],
  "expect": {"$a.result": "REFUSE", "$a.refusals": S['producerSubset']['refusals']}},

 {"id": "coverage-examined-subject-count-that-disagrees-with-the-enumeration-is-refused",
  "kind": "negative", "feedback": ["CB-M1"],
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": {"$merge": "$fixtures.coveragePayload",
                                  "$with": {"entry.examinedUniverse.subjectCount": 99}},
                      "scope_descriptor": "$fixtures.scopeDescriptor", "unresolved_facts": []}}],
  "expect": {"$a.result": "REFUSE", "$a.refusals": ["native.examined-universe-subject-count-mismatch"]}},

 {"id": "coverage-key-naming-a-universe-outside-the-host-scope-is-refused",
  "kind": "negative", "feedback": ["CB-M1"],
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": {"$merge": "$fixtures.coveragePayload",
                                  "$with": {"key.targetUniverse": hashlib.sha256(b'other-universe').hexdigest()}},
                      "scope_descriptor": "$fixtures.scopeDescriptor", "unresolved_facts": []}}],
  "expect": {"$a.result": "REFUSE", "$a.refusals": ["native.coverage-key-scope-mismatch:targetUniverse"]}},

 {"id": "coverage-complete-claimed-over-an-admitted-unresolved-edge-is-refused-at-the-boundary",
  "kind": "negative", "feedback": ["CB-M1"],
  "note": "RC-2 is rechecked at the same boundary that checks the commitment; a zero-count claim over an admitted edge is a protocol violation, not an honest entry.",
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": "$fixtures.coveragePayload", "scope_descriptor": "$fixtures.scopeDescriptor",
                      "unresolved_facts": ["$fixtures.unresolvedEdgeFact"]}}],
  "expect": {"$a.result": "REFUSE", "$a.refusals": [], "$a.faults": S['lyingComplete']['faults']}},

 {"id": "coverage-incomplete-over-an-exhaustive-partition-admits-with-the-same-commitment",
  "kind": "positive", "feedback": ["CB-M1"],
  "note": "RC-3: examined-exhaustive and resolution-incomplete is the honest entry, and it commits to the same examined partition as the complete one.",
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": "$fixtures.coverageIncompletePayload", "scope_descriptor": "$fixtures.scopeDescriptor",
                      "unresolved_facts": ["$fixtures.unresolvedEdgeFact"]}}],
  "expect": {"$a.result": "ADMIT", "$a.subjectScopeCommitment": S['commitment']['subjectScopeCommitment'],
             "$a.coverageId": S['incomplete']['coverageId'], "$a.faults": []}},

 {"id": "coverage-use-requires-the-subject-scope-to-be-in-the-evaluated-view",
  "kind": "positive", "feedback": ["CB-M1"],
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": "$fixtures.coveragePayload", "scope_descriptor": "$fixtures.scopeDescriptor",
                      "unresolved_facts": []}},
            {"fn": "coverage_view_use", "bind": "u", "args": {"view": "$fixtures.coverageView", "admissions": ["$a"]}}],
  "expect": {"$u.result": "ADMIT", "$u.refusals": []}},

 {"id": "coverage2-whose-subject-scope-is-outside-the-view-is-refused",
  "kind": "negative", "feedback": ["CB-M1"],
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": "$fixtures.coveragePayload", "scope_descriptor": "$fixtures.scopeDescriptor",
                      "unresolved_facts": []}},
            {"fn": "coverage_view_use", "bind": "u",
             "args": {"view": {"$merge": "$fixtures.coverageView", "$with": {"scopeIds": [S['otherCommitment']['scopeId']]}},
                      "admissions": ["$a"]}}],
  "expect": {"$u.result": "REFUSE", "$u.refusals": S['useForeign']['refusals']}},

 {"id": "coverage2-never-admitted-at-the-producer-boundary-is-refused-in-a-view",
  "kind": "negative", "feedback": ["CB-M1"],
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": "$fixtures.coveragePayload", "scope_descriptor": "$fixtures.scopeDescriptor",
                      "unresolved_facts": []}},
            {"fn": "coverage_view_use", "bind": "u",
             "args": {"view": {"$merge": "$fixtures.coverageView",
                               "$with": {"coverageIds": ['coverage2:' + hashlib.sha256(b'unadmitted').hexdigest()]}},
                      "admissions": ["$a"]}}],
  "expect": {"$u.result": "REFUSE", "$u.refusals": S['useUnadmitted']['refusals']}},

 {"id": "subject-scope-duplicate-subject-refuses-rather-than-silently-deduping",
  "kind": "negative", "feedback": ["CB-M1"],
  "steps": [{"fn": "subject_scope_descriptor", "expectError": "SUBJECT_SCOPE_DUPLICATE_SUBJECT",
             "args": {"snapshot_id": S['snapshot'], "relation": "references", "rung": "resolved-binding",
                      "source_universe": S['sourceUniverse'], "target_universe": S['sourceUniverse'],
                      "enumerator_closure": S['enumeratorClosure'],
                      "subjects": [S['subjects'][0], S['subjects'][0]]}}],
  "expect": {}},

 # ---- M-2: TypeScript native context ------------------------------------------------------------
 {"id": "typescript-native-context-admits-against-retained-stdlib-and-compiler-closures",
  "kind": "positive", "feedback": ["CB-M2", "CB-A1", "CB-A2"],
  "note": "The record that holds typescriptStdlibMerkleRoot now exists, with its own H domain native.context.typescript.v2. Every digest is recomputed from the retained closure descriptors and trees; none is read from a worker claim.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}},
            {"fn": "bind_typescript_universe", "bind": "u",
             "args": {"universe": "$fixtures.tsUniverse", "admission": "$a"}},
            {"fn": "plan_native_context_digests", "bind": "p", "args": {"admissions": ["$a"]}}],
  "expect": {"$a.refusals": [], "$a.domain": "native.context.typescript.v2",
             "$a.nativeContextId": B['admission']['nativeContextId'],
             "$a.planNativeContextDigest": B['admission']['planNativeContextDigest'],
             "$u.result": "ADMIT", "$u.universeId": B['bound']['universeId'],
             "$p": [B['admission']['planNativeContextDigest']]}},

 {"id": "typescript-standard-library-change-alone-changes-the-context-and-the-universe",
  "kind": "positive", "feedback": ["CB-M2"],
  "note": "Independent test of the stdlib input: one declaration-file byte moves the kind=stdlib closure2, hence typescriptStdlibMerkleRoot, hence nativeContextId, hence the typescript-v2 universe id and PlanId. Nothing else changed.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsStdlibChangedContext",
                      "closure_trees": "$fixtures.tsStdlibChangedTrees"}},
            {"fn": "bind_typescript_universe", "bind": "u",
             "args": {"universe": {"$merge": "$fixtures.tsUniverse", "$with": {"nativeContextId": B['stdlibChanged']['admission']['nativeContextId']}},
                      "admission": "$a"}}],
  "expect": {"$a.refusals": [], "$a.nativeContextId": B['stdlibChanged']['admission']['nativeContextId'],
             "$a.nativeContextId": {"$not": B['admission']['nativeContextId']},
             "$u.result": "ADMIT", "$u.universeId": {"$not": B['bound']['universeId']}}},

 {"id": "typescript-compiler-change-alone-changes-the-context-and-the-universe",
  "kind": "positive", "feedback": ["CB-M2"],
  "note": "Independent test of the compiler input: a new signed compiler closure with a new semanticVersion and new member digests. compilerVersion must come from the admitted manifest, so the two cannot drift apart.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsCompilerChangedContext",
                      "closure_trees": "$fixtures.tsCompilerChangedTrees"}}],
  "expect": {"$a.refusals": [], "$a.nativeContextId": B['compilerChanged']['admission']['nativeContextId'],
             "$a.nativeContextId": {"$not": B['admission']['nativeContextId']},
             "$a.nativeContextId": {"$not": B['stdlibChanged']['admission']['nativeContextId']}}},

 {"id": "typescript-stdlib-merkle-root-that-names-no-retained-closure-refuses",
  "kind": "negative", "feedback": ["CB-M2", "CB-A1"],
  "note": "Malformed closure join: `closure2:` + typescriptStdlibMerkleRoot must name a retained kind=stdlib closure whose recomputed identity equals it.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript",
                      "descriptor": {"$merge": "$fixtures.tsNativeContext",
                                     "$with": {"toolchain.typescriptStdlibMerkleRoot": hashlib.sha256(b'not-a-closure').hexdigest()}},
                      "closure_trees": "$fixtures.tsClosureTrees"}}],
  "expect": {"$a.refusals": B['malformed']['refusals']}},

 {"id": "typescript-tool-digest-outside-the-named-closure-tree-refuses",
  "kind": "negative", "feedback": ["CB-M2"],
  "note": "Mismatched closure: every executable the adapter may select is a member of the signed closure named by closureId. No PATH lookup and no system node.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript",
                      "descriptor": {"$merge": "$fixtures.tsNativeContext",
                                     "$with": {"toolClosure.compiler": hashlib.sha256(b'some/other/tsc.js').hexdigest()}},
                      "closure_trees": "$fixtures.tsClosureTrees"}}],
  "expect": {"$a.refusals": B['toolMismatch']['refusals']}},

 {"id": "typescript-stdlib-component-digest-disagreeing-with-the-retained-tree-refuses",
  "kind": "negative", "feedback": ["CB-M2"],
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript",
                      "descriptor": {"$merge": "$fixtures.tsNativeContext",
                                     "$with": {"toolchain.standardLibraryComponentDigests.0.sha256": hashlib.sha256(b'tampered').hexdigest()}},
                      "closure_trees": "$fixtures.tsClosureTrees"}}],
  "expect": {"$a.refusals": B['treeMismatch']['refusals']}},

 {"id": "rust-native-context-offered-as-the-typescript-context-refuses",
  "kind": "negative", "feedback": ["CB-M2"],
  "note": "No fake Rust context. NativeContextV2 is the Rust record; a typescript-v2 universe never binds it.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.rustContextOfferedAsTypescript",
                      "closure_trees": "$fixtures.tsClosureTrees"}}],
  "expect": {"$a.refusals": ["native.native-context-language-mismatch:not-TypeScriptNativeContextV2"]}},

 {"id": "typescript-universe-bound-to-a-context-this-host-did-not-mint-refuses",
  "kind": "negative", "feedback": ["CB-M2"],
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}},
            {"fn": "bind_typescript_universe", "bind": "u",
             "args": {"universe": {"$merge": "$fixtures.tsUniverse",
                                   "$with": {"nativeContextId": 'sha256:' + hashlib.sha256(b'foreign-context').hexdigest()}},
                      "admission": "$a"}}],
  "expect": {"$u.result": "REFUSE", "$u.refusals": ["native.universe-context-binding-mismatch"]}},

 {"id": "worker-recomputed-typescript-context-mismatch-is-unavailable-before-analyze",
  "kind": "negative", "feedback": ["CB-M2"],
  "note": "Section 9.5 for TypeScript exactly as for Rust: the worker recomputes the context from its own sealed inputs and any differing byte faults before Analyze.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}},
            {"fn": "verify_native_context", "bind": "ok",
             "args": {"language": "typescript", "host_admission": "$a", "worker_descriptor": "$fixtures.tsNativeContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}},
            {"fn": "verify_native_context", "bind": "bad",
             "args": {"language": "typescript", "host_admission": "$a",
                      "worker_descriptor": "$fixtures.tsCompilerChangedContext",
                      "closure_trees": "$fixtures.tsCompilerChangedTrees"}}],
  "expect": {"$ok.equal": True, "$ok.frame": "NativeContextVerified", "$ok.unavailableReason": None,
             "$bad.equal": False, "$bad.frame": "Unavailable", "$bad.unavailableReason": "native-context-mismatch",
             "$bad.recomputedNativeContextId": B['compilerChanged']['admission']['nativeContextId']}},

 {"id": "plan-native-context-digests-are-bare-hex-while-native-records-use-sha256-text",
  "kind": "positive", "feedback": ["CB-M2", "CB-A2"],
  "note": "Blind consumer A-2: one digest, three admitted textual forms. plan.nativeContextDigests takes the bare 64 hex; a native record field typed Sha256Text takes `sha256:`+hex; a foundation identity takes its typed prefix.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}},
            {"fn": "plan_native_context_digests", "bind": "p", "args": {"admissions": ["$a"]}}],
  "expect": {"$p": [B['admission']['planNativeContextDigest']],
             "$a.nativeContextId": "sha256:" + B['admission']['planNativeContextDigest'],
             "$p.0": {"$not": "sha256:" + B['admission']['planNativeContextDigest']}}},
]

for c in new:
    if c['id'] in existing:
        raise SystemExit('duplicate case id ' + c['id'])
cases.extend(new)
doc['revision'] = doc.get('revision', '') + (' ' if doc.get('revision') else '') + \
    'Blind-consumer corrections: M-1 subjectScopeCommitment producing recipe and admitted producer boundary; M-2 closed TypeScript native context.'
p.write_text(json.dumps(doc, indent=1) + '\n')
print('cases now', len(cases))
