"""Author edit: repair three cases whose expect maps had colliding paths (a repeated key asserts once)."""
import hashlib, json, sys
from pathlib import Path
R = Path(sys.argv[1]); p = R / 'docs/coop/design-corrections/native/native-cases.v2.json'
B = json.loads(Path('/tmp/opensip-design-corrections/blind-corrections-author.v1/evidence/native-fixture-build.json').read_text())
S = json.loads(Path('/tmp/opensip-design-corrections/blind-corrections-author.v1/evidence/scope-fixture-build.json').read_text())
doc = json.loads(p.read_text()); by = {c['id']: c for c in doc['cases']}

c = by['subject-scope-commitment-is-the-scope2-identity-in-native-sha256-text-form']
c['expect'] = {
    "$v.model": "$v.oracle",
    "$c.scopeId": S['commitment']['scopeId'],
    "$c.subjectScopeCommitment": S['commitment']['subjectScopeCommitment'],
    "$c.subjectCount": 3,
    "$v.sha256Text": S['commitment']['subjectScopeCommitment'],
    "$v.rawSha256": {"$not": S['commitment']['scopeId'].removeprefix('scope2:')}}

other_snapshot = 'snapshot2:' + hashlib.sha256(b'other-snapshot').hexdigest()
by['subject-scope-commitment-binds-the-snapshot-not-only-the-subject-list']['steps'] = [
    {"fn": "subject_scope_commitment", "bind": "c", "args": {"descriptor": "$fixtures.scopeDescriptor"}},
    {"fn": "subject_scope_descriptor", "bind": "d2",
     "args": {"snapshot_id": other_snapshot, "relation": "references", "rung": "resolved-binding",
              "source_universe": S['sourceUniverse'], "target_universe": S['sourceUniverse'],
              "enumerator_closure": S['enumeratorClosure'], "subjects": "$fixtures.scopeSubjects"}},
    {"fn": "subject_scope_commitment", "bind": "c2", "args": {"descriptor": "$d2"}}]
by['subject-scope-commitment-binds-the-snapshot-not-only-the-subject-list']['expect'] = {
    "$d2.subjects": S['descriptor']['subjects'],
    "$c2.subjectScopeCommitment": S['otherCommitment']['subjectScopeCommitment'],
    "$c2.subjectScopeCommitment": {"$not": "$c.subjectScopeCommitment"}}
# a repeated key would drop the first assertion; spell the two claims on different paths instead
by['subject-scope-commitment-binds-the-snapshot-not-only-the-subject-list']['expect'] = {
    "$d2.subjects": S['descriptor']['subjects'],
    "$c2.scopeId": S['otherCommitment']['scopeId'],
    "$c2.subjectScopeCommitment": {"$not": "$c.subjectScopeCommitment"}}

sl = by['typescript-standard-library-change-alone-changes-the-context-and-the-universe']
sl['steps'] = [
    {"fn": "admit_native_context", "bind": "base",
     "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext", "closure_trees": "$fixtures.tsClosureTrees"}},
    {"fn": "admit_native_context", "bind": "a",
     "args": {"language": "typescript", "descriptor": "$fixtures.tsStdlibChangedContext", "closure_trees": "$fixtures.tsStdlibChangedTrees"}},
    {"fn": "bind_typescript_universe", "bind": "ubase", "args": {"universe": "$fixtures.tsUniverse", "admission": "$base"}},
    {"fn": "bind_typescript_universe", "bind": "u",
     "args": {"universe": {"$merge": "$fixtures.tsUniverse",
                           "$with": {"nativeContextId": B['stdlibChanged']['admission']['nativeContextId']}},
              "admission": "$a"}}]
sl['expect'] = {"$a.refusals": [], "$a.nativeContextId": B['stdlibChanged']['admission']['nativeContextId'],
                "$base.nativeContextId": {"$not": "$a.nativeContextId"},
                "$u.result": "ADMIT", "$u.universeId": B['stdlibChanged'] and None}
sl['expect']["$u.universeId"] = {"$not": "$ubase.universeId"}

cc = by['typescript-compiler-change-alone-changes-the-context-and-the-universe']
cc['steps'] = [
    {"fn": "admit_native_context", "bind": "base",
     "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext", "closure_trees": "$fixtures.tsClosureTrees"}},
    {"fn": "admit_native_context", "bind": "stdlib",
     "args": {"language": "typescript", "descriptor": "$fixtures.tsStdlibChangedContext", "closure_trees": "$fixtures.tsStdlibChangedTrees"}},
    {"fn": "admit_native_context", "bind": "a",
     "args": {"language": "typescript", "descriptor": "$fixtures.tsCompilerChangedContext", "closure_trees": "$fixtures.tsCompilerChangedTrees"}}]
cc['expect'] = {"$a.refusals": [], "$a.nativeContextId": B['compilerChanged']['admission']['nativeContextId'],
                "$base.nativeContextId": {"$not": "$a.nativeContextId"},
                "$stdlib.nativeContextId": {"$not": "$a.nativeContextId"}}

pd = by['plan-native-context-digests-are-bare-hex-while-native-records-use-sha256-text']
pd['expect'] = {"$p": [B['admission']['planNativeContextDigest']],
                "$a.nativeContextId": "sha256:" + B['admission']['planNativeContextDigest'],
                "$a.planNativeContextDigest": B['admission']['planNativeContextDigest'],
                "$p.0": {"$not": "$a.nativeContextId"}}

fc = by['coverage-commitment-chosen-by-the-claimant-is-refused']
claim = 'sha256:' + hashlib.sha256(b'claimant-chosen').hexdigest()
fc['steps'][0]['args']['payload']['$with'] = {"key.subjectScopeCommitment": claim,
                                              "entry.examinedUniverse.subjectScopeCommitment": claim}
p.write_text(json.dumps(doc, indent=1) + '\n')
print('repaired 5 cases')
