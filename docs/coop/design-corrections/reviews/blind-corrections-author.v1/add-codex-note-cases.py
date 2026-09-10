"""Author edit: regressions for the six Codex coauthor-note findings on the draft."""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
R = Path(sys.argv[1]); N = R / 'docs/coop/design-corrections/native'
spec = importlib.util.spec_from_file_location('m', N / 'native_evidence_model.v2.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
B = json.loads(Path('/tmp/opensip-design-corrections/blind-corrections-author.v1/evidence/native-fixture-build.json').read_text())
h = lambda s: hashlib.sha256(s.encode()).hexdigest()

p = N / 'native-cases.v2.json'
doc = json.loads(p.read_text()); F, cases = doc['fixtures'], doc['cases']
by = {c['id']: c for c in cases}

ctx = F['tsNativeContext']; trees = F['tsClosureTrees']
adm = M.admit_native_context('typescript', ctx, trees)
assert adm['refusals'] == [], adm

# the base positive case now supplies the context bytes too
base = by['typescript-native-context-admits-against-retained-stdlib-and-compiler-closures']
base['steps'][1]['args']['context'] = '$fixtures.tsNativeContext'
base['steps'][2] = {"fn": "plan_native_context_digests", "bind": "p", "args": {"admissions": ["$a", "$a"]}}
base['note'] = base['note'] + ' Two units sharing one context collapse to one plan.nativeContextDigests member.'

# a platform-specific tool closure: same source, different platform family, different context id
tools2 = copy.deepcopy(B['closures']['tools']); tools2['platform'] = 'macos-aarch64'
tools2['tree'] = sorted([{'path': 'bin/node', 'sha256': h('bin/node@macos'), 'bytes': 88000000},
                         {'path': 'lib/tsc.js', 'sha256': h('lib/tsc.js'), 'bytes': 8000000},
                         {'path': 'package/typescript.tgz', 'sha256': h('package/typescript.tgz'), 'bytes': 12000000}],
                        key=lambda b: b['path'].encode())
tools2_id = M.IM.identifier('closure', tools2)
ctx_mac = copy.deepcopy(ctx)
ctx_mac['toolClosure'] = {'compiler': h('lib/tsc.js'), 'runtime': h('bin/node@macos'), 'closureId': tools2_id}
trees_mac = dict(trees, **{tools2_id: tools2})
adm_mac = M.admit_native_context('typescript', ctx_mac, trees_mac)
assert adm_mac['refusals'] == [], adm_mac
F['tsMacToolClosure'] = tools2
F['tsMacNativeContext'] = ctx_mac
F['tsMacClosureTrees'] = trees_mac

# a stdlib tree with two paths sharing one basename
amb = copy.deepcopy(B['closures']['stdlib'])
amb['tree'] = sorted(amb['tree'] + [{'path': 'lib/legacy/lib.dom.d.ts', 'sha256': h('legacy/lib.dom.d.ts'), 'bytes': 2048}],
                     key=lambda b: b['path'].encode())
amb_id = M.IM.identifier('closure', amb)
ctx_amb = copy.deepcopy(ctx); ctx_amb['toolchain']['typescriptStdlibMerkleRoot'] = amb_id.removeprefix('closure2:')
F['tsAmbiguousStdlibClosure'] = amb
F['tsAmbiguousStdlibContext'] = ctx_amb
F['tsAmbiguousStdlibTrees'] = dict(trees, **{amb_id: amb})
amb_out = M.admit_native_context('typescript', ctx_amb, F['tsAmbiguousStdlibTrees'])

dropped = copy.deepcopy(ctx)
dropped['toolchain']['standardLibraryComponentDigests'] = [
    c for c in dropped['toolchain']['standardLibraryComponentDigests'] if c['component'] != 'lib.decorators.d.ts']
F['tsDroppedLibContext'] = dropped
dropped_out = M.admit_native_context('typescript', dropped, trees)

field_cases = []
for field, value, want in (('allowJs', True, 'allowJs'), ('checkJs', True, 'checkJs'),
                           ('lockfileKind', 'pnpm-lock', 'lockfileKind'),
                           ('nodeModulesInReadSet', False, 'nodeModulesInReadSet'),
                           ('languageMode', 'js-allowjs', 'languageMode')):
    u = copy.deepcopy(F['tsUniverse']); u[field] = value
    out = M.bind_typescript_universe(u, adm, ctx)
    assert out['result'] == 'REFUSE' and any(want in r for r in out['refusals']), (field, out)
    field_cases.append((field, value, out['refusals']))

new = [
 {"id": "typescript-universe-field-contradicting-the-admitted-context-refuses",
  "kind": "negative", "feedback": ["CB-M2"],
  "note": "A matching nativeContextId commits to the CONTEXT bytes, not to the universe's copy of them. Every "
          "field the two records both carry, and every universe flag that is a function of context bytes, must "
          "agree; five contradictions are checked here.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}}]
           + [{"fn": "bind_typescript_universe", "bind": "u%d" % i,
               "args": {"universe": {"$merge": "$fixtures.tsUniverse", "$with": {f: v}},
                        "admission": "$a", "context": "$fixtures.tsNativeContext"}}
              for i, (f, v, _) in enumerate(field_cases)],
  "expect": {**{"$u%d.result" % i: "REFUSE" for i in range(len(field_cases))},
             **{"$u%d.refusals" % i: r for i, (_, _, r) in enumerate(field_cases)}}},

 {"id": "typescript-universe-agreeing-with-the-admitted-context-admits",
  "kind": "positive", "feedback": ["CB-M2"],
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}},
            {"fn": "bind_typescript_universe", "bind": "u",
             "args": {"universe": "$fixtures.tsUniverse", "admission": "$a",
                      "context": "$fixtures.tsNativeContext"}}],
  "expect": {"$u.result": "ADMIT", "$u.refusals": []}},

 {"id": "typescript-context-bytes-that-are-not-the-admitted-ones-refuse",
  "kind": "negative", "feedback": ["CB-M2"],
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}},
            {"fn": "bind_typescript_universe", "bind": "u",
             "args": {"universe": "$fixtures.tsUniverse", "admission": "$a",
                      "context": "$fixtures.tsCompilerChangedContext"}}],
  "expect": {"$u.result": "REFUSE",
             "$u.refusals": ["native.universe-context-binding-mismatch:context-bytes-are-not-the-admitted-ones"]}},

 {"id": "typescript-stdlib-inventory-missing-an-unselected-declaration-library-refuses",
  "kind": "negative", "feedback": ["CB-M2"],
  "note": "The row set is the COMPLETE declaration inventory of the retained tree, selected or not; otherwise "
          "two different standard libraries could mint one context.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsDroppedLibContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}}],
  "expect": {"$a.refusals": dropped_out['refusals']}},

 {"id": "typescript-stdlib-tree-with-two-paths-sharing-a-basename-refuses",
  "kind": "negative", "feedback": ["CB-M2"],
  "note": "The component join is by basename, so an ambiguous tree is refused rather than resolved arbitrarily.",
  "steps": [{"fn": "admit_native_context", "bind": "a",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsAmbiguousStdlibContext",
                      "closure_trees": "$fixtures.tsAmbiguousStdlibTrees"}}],
  "expect": {"$a.refusals": amb_out['refusals']}},

 {"id": "typescript-context-identity-is-platform-specific-through-its-signed-tool-closure",
  "kind": "positive", "feedback": ["CB-M2", "CB-A2"],
  "note": "The context carries no platform FIELD because TypeScript resolution semantics are platform-invariant "
          "by design; the identity is not, because toolClosure.closureId names a closure whose foundation "
          "descriptor includes `platform`. Two families running different executables mint two contexts, as "
          "they must, because different bytes ran. This corrects a same-id claim the draft made.",
  "steps": [{"fn": "admit_native_context", "bind": "linux",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsNativeContext",
                      "closure_trees": "$fixtures.tsClosureTrees"}},
            {"fn": "admit_native_context", "bind": "macos",
             "args": {"language": "typescript", "descriptor": "$fixtures.tsMacNativeContext",
                      "closure_trees": "$fixtures.tsMacClosureTrees"}}],
  "expect": {"$linux.refusals": [], "$macos.refusals": [],
             "$macos.nativeContextId": adm_mac['nativeContextId'],
             "$linux.nativeContextId": {"$not": "$macos.nativeContextId"}}},

 {"id": "coverage-payload-schema-digest-a-caller-chose-is-refused",
  "kind": "negative", "feedback": ["CB-M1"],
  "note": "payloadSchemaDigest is the raw SHA-256 of the exact registered schema DOCUMENT bytes; a caller may "
          "restate it but never choose it.",
  "steps": [{"fn": "admit_coverage_result_v3", "bind": "a",
             "args": {"payload": "$fixtures.coveragePayload", "scope_descriptor": "$fixtures.scopeDescriptor",
                      "unresolved_facts": [], "payload_schema_digest": h('a-schema-the-caller-preferred')}}],
  "expect": {"$a.result": "REFUSE", "$a.coverageId": None,
             "$a.refusals": ["native.coverage-payload-schema-not-registered"]}},
]
for c in new:
    if c['id'] in by:
        raise SystemExit('duplicate ' + c['id'])
cases.extend(new)
p.write_text(json.dumps(doc, indent=1) + '\n')
print('cases now', len(cases))
