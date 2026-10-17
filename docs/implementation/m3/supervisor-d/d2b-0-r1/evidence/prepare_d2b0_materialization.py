"""Prepare the D2b-0 candidate (D2b plan r3, sub-unit D2b-0, as amended by LD-D2B0-A): FA-2's and RUST3-LIM's two new
schema sources materialized admission-only in a detached worktree at product main: the admission registry (and its
architecture copy) and the admission source map, the identity crate's compiled SOURCE_PINS, the host's and storage's
embeddings, and a host control. No generator table (source map, generation registry, options, closure) changes, so no
generated output changes (LD-D2B0-A). LD-D2B-13's handshake re-derivation is recorded. No commit, no push."""
from pathlib import Path
import copy, hashlib, json, os, re, stat, subprocess

B = Path('/tmp/opensip-implementation'); A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'
W = A.parent / 'opensip-d2b0'; D = B / 'd2b0-materialization-r1'
PRE = 'docs/implementation/m3/supervisor-d/d2b-0-r1'; U = A / PRE
FA = 'docs/implementation/m3/native-successors-fa/'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def git(root, *a): return subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
def read(p): return json.loads(p.read_bytes())
def write(p, j): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(j, indent=2) + '\n')
def pin(root, path): b = (root / path).read_bytes(); return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def insert_sorted(rows, row, key):
    """Insert before the first row whose key is greater: the tables are sorted, with later appended rows at the end."""
    assert all(r[key] != row[key] for r in rows), row[key]
    at = next((i for i, r in enumerate(rows) if r[key] > row[key]), len(rows))
    rows.insert(at, row); return at

# The accepted sources: each map's new file, at its recorded after-pin (FA-2 and RUST3-LIM are bound contract successors).
NEW = []
for unit in ('fa-2', 'rust3-lim'):
    m = read(A / FA / unit / 'materialization-map.json')
    rows = [r for r in m['files'] if r['before'] is None]; assert len(rows) == 1
    r = rows[0]; arch = pin(A, r['candidatePath']); assert {k: arch[k] for k in ('bytes', 'sha256')} == r['after']
    doc = read(A / r['candidatePath'])
    NEW.append(dict(unit=unit, schemaId=doc['$id'], path=r['productPath'], arch=arch,
                    major=int(doc['$id'].rsplit('.', 1)[1]), defs=sorted(doc.get('$defs', {}))))
assert [n['schemaId'] for n in NEW] == ['opensip.product.symbol-census.1', 'opensip.product.rust-subject-scope.1']
assert all(n['major'] == 1 for n in NEW)

base = git(P, 'rev-parse', 'HEAD'); assert git(P, 'status', '--porcelain') == ''
lock = read(P / 'design-lock.json'); accepted = {}
for binding in lock['contractSuccessors']:
    rec = read(A / binding['record']['path'])
    for c in rec['candidates']: accepted[c['path']] = c
for n in NEW: assert accepted.get(n['arch']['path']) == n['arch'], n['arch']['path']
assert not W.exists() and not D.exists() and not (U / 'admission-registry.json').exists()
git(P, 'worktree', 'add', '--detach', str(W), base); D.mkdir(parents=True)

# LD-D2B-13: the handshake. RUST3-LIM's handshake candidate (which contains FA-2's) merged three ways onto the current
# product bytes (RCA-1's), against the maps' common before-image, must equal the current bytes.
hs = 'schemas/sources/handshake-v1.schema.json'
lim = read(A / FA / 'rust3-lim/materialization-map.json')['files'][0]; assert lim['productPath'] == hs
before = subprocess.check_output(['/usr/bin/git', 'show', '436d615:' + hs], cwd=P, env=E)
assert hashlib.sha256(before).hexdigest() == lim['before']['sha256']
work = D / 'handshake-merge'; work.mkdir()
(work / 'current.json').write_bytes((W / hs).read_bytes()); (work / 'base.json').write_bytes(before)
(work / 'successor.json').write_bytes((A / lim['candidatePath']).read_bytes())
merge = subprocess.run(['/usr/bin/git', 'merge-file', '-p', str(work / 'current.json'), str(work / 'base.json'), str(work / 'successor.json')],
                       env=E, capture_output=True)
handshake = dict(current=pin(W, hs), mapsBefore=lim['before'], mapsAfterFa2=lim['afterFa2'], mapsAfter=lim['after'],
                 mergeExit=merge.returncode, mergedEqualsCurrent=merge.stdout == (W / hs).read_bytes(),
                 differencesFromMapsAfter=dict(bytes=len(merge.stdout) - lim['after']['bytes'],
                                               sha256Differs=hashlib.sha256(merge.stdout).hexdigest() != lim['after']['sha256']))
assert merge.returncode == 0 and handshake['mergedEqualsCurrent'], 'the successors are not contained in the current handshake'

# 1. The two documents at their product paths.
for n in NEW:
    assert not (W / n['path']).exists(); (W / n['path']).write_bytes((A / n['arch']['path']).read_bytes())
    assert pin(W, n['path'])['sha256'] == n['arch']['sha256']
arch_pin = lambda n: dict(path=n['arch']['path'], bytes=n['arch']['bytes'], sha256=n['arch']['sha256'])

# 4. The admission registry and its architecture copy, and the admission source map.
ar = read(W / 'schemas/admission-registry.json'); am = read(W / 'schemas/admission-source-map.json')
for n in NEW:
    insert_sorted(ar['sources'], dict(schemaId=n['schemaId'], sourcePath=n['path'], bytes=n['arch']['bytes'], sha256=n['arch']['sha256']), 'schemaId')
    insert_sorted(am['sources'], dict(schemaId=n['schemaId'], implementationPath=n['path'], architectureSource=arch_pin(n)), 'schemaId')
assert [r['schemaId'] for r in ar['sources']] == sorted(r['schemaId'] for r in ar['sources'])
write(W / 'schemas/admission-registry.json', ar); write(U / 'admission-registry.json', ar)
am['registryArchitectureSource'] = pin(A, PRE + '/admission-registry.json'); write(W / 'schemas/admission-source-map.json', am)
order = [r['schemaId'] for r in ar['sources']]

# 5. The compiled pins (identity SOURCE_PINS) and the two embeddings (host, storage), in the admission registry's order.
p = W / 'crates/identity/src/schema_registry.rs'; text = p.read_text()
for n in NEW:
    nxt = order[order.index(n['schemaId']) + 1]
    anchor = '    SourcePin {\n        id: "' + nxt + '",\n'; assert text.count(anchor) == 1, nxt
    raw = (W / n['path']).read_bytes()
    block = ('    SourcePin {\n        id: "' + n['schemaId'] + '",\n        path: "' + n['path'] + '",\n        bytes: ' + str(len(raw)) +
             ',\n        sha256: [' + ', '.join(str(v) for v in hashlib.sha256(raw).digest()) + '],\n    },\n')
    text = text.replace(anchor, block + anchor)
p.write_text(text)
paths = {r['schemaId']: r['sourcePath'] for r in ar['sources']}
for rel in ('crates/host/src/schema_sources.rs', 'crates/storage/src/schema_sources.rs'):
    p = W / rel; text = p.read_text()
    for n in NEW:
        nxt = paths[order[order.index(n['schemaId']) + 1]]
        anchor = '    include_bytes!(concat!(\n        env!("CARGO_MANIFEST_DIR"),\n        "/../../' + nxt + '"\n    )),\n'
        assert text.count(anchor) == 1, (rel, nxt)
        text = text.replace(anchor, anchor.replace(nxt, n['path']) + anchor)
    p.write_text(text)

# 5b. The identity schema compiler's annotation set gains the two root law keywords (LD-D2B0-7), as it holds every other
# admitted schema's law keyword (x-opensip-join-law, x-opensip-law, x-opensip-file-membership-extent-law, ...). They are
# annotations: no evaluation changes.
p = W / 'crates/identity/src/schema.rs'; text = p.read_text()
anchor = '            | "x-opensip-join-law"\n    )\n}\n'; assert text.count(anchor) == 1
laws = sorted({k for n in NEW for k in read(W / n['path']) if k.startswith('x-opensip-') and k.endswith('-law')})
assert laws == ['x-opensip-subject-scope-law', 'x-opensip-symbol-census-law'], laws
text = text.replace(anchor, '            | "x-opensip-join-law"\n' + ''.join('            | "' + k + '"\n' for k in laws) + '    )\n}\n')
p.write_text(text)

# 6b. The host integration test that pins storage's and host's source count (50) follows the registry (52).
p = W / 'crates/host/tests/admission_tests.rs'; text = p.read_text(); count = len(order); assert count == 52
for old, new in (('compiles the same 50 pinned\n', 'compiles the same %d pinned\n' % count),
                 ('list the same 50 files, in order.', 'list the same %d files, in order.' % count),
                 ('    assert_eq!(storage.len(), 50);\n', '    assert_eq!(storage.len(), %d);\n' % count)):
    assert text.count(old) == 1, old; text = text.replace(old, new)
p.write_text(text)

# 6. The host's control over the two new sources (appended, like RCA-1's shape module).
p = W / 'crates/host/src/schema_sources.rs'
p.write_text(p.read_text() + '''
/// D2b-0 (D2b plan r3): FA-2's and RUST3-LIM's sources are in the embedded
/// registry, each `$def` selected under its own full-document pin, and their
/// shapes admit and refuse as published. Shape is not semantic admission.
#[cfg(test)]
mod successor_source_tests {
    use super::embedded_schema_registry;
    use opensip_identity::{RegisteredSchemas, raw_sha256};

    const CENSUS: &str = "opensip.product.symbol-census.1";
    const SCOPE: &str = "opensip.product.rust-subject-scope.1";

    #[test]
    fn every_successor_definition_is_selected_under_its_document_pin() {
        let registry = embedded_schema_registry().unwrap();
        for (id, path, defs) in [
            (CENSUS, "schemas/sources/symbol-census-v1.schema.json", 20),
            (SCOPE, "schemas/sources/rust-subject-scope-v1.schema.json", 5),
        ] {
            let pin = RegisteredSchemas::source_requirements()
                .iter()
                .find(|p| p.schema_id() == id)
                .unwrap();
            assert_eq!(pin.source_path(), path);
            let raw = super::SOURCES
                .iter()
                .find(|raw| raw.len() == pin.bytes() && raw_sha256(raw) == pin.sha256())
                .unwrap();
            let document = opensip_identity::parse_json(raw).unwrap();
            let opensip_identity::JsonValue::Object(root) = &document else {
                panic!("{id}");
            };
            let Some(opensip_identity::JsonValue::Object(names)) = root.get("$defs") else {
                panic!("{id}");
            };
            assert_eq!(names.len(), defs);
            for name in names.keys() {
                let handle = registry.schema(id, &format!("/$defs/{name}")).unwrap();
                assert_eq!(handle.document_sha256(), pin.sha256());
            }
        }
    }

    #[test]
    fn the_successor_shapes_admit_and_refuse_as_published() {
        let registry = embedded_schema_registry().unwrap();
        let digest = format!("sha256:{}", "a".repeat(64));
        let scope = |count: &str, extra: &str| {
            format!(
                r#"{{"scopeKind":"nonempty-rs-files","subjectCount":{count},"subjectScopeCommitment":"{digest}"{extra}}}"#
            )
        };
        for (raw, accepted) in [
            (scope("1", ""), true),
            (scope("200000", ""), true),
            (scope("0", ""), false),
            (scope("200001", ""), false),
            (scope("1", r#","extra":true"#), false),
        ] {
            let admitted = registry
                .schema(SCOPE, "/$defs/RustSubjectScopeV1")
                .unwrap()
                .admit_json(raw.as_bytes(), 1_000_000)
                .is_ok();
            assert_eq!(admitted, accepted, "{raw}");
        }
        for (raw, accepted) in [
            (format!("\\"{digest}\\""), true),
            (format!("\\"sha256:{}\\"", "A".repeat(64)), false),
            (format!("\\"{}\\"", "a".repeat(64)), false),
        ] {
            let admitted = registry
                .schema(CENSUS, "/$defs/Sha256Text")
                .unwrap()
                .admit_json(raw.as_bytes(), 100_000)
                .is_ok();
            assert_eq!(admitted, accepted, "{raw}");
        }
    }
}
''')

# 7. Admission-only (LD-D2B0-A): every generator input is the base's bytes.
for rel in ('schemas/source-map.json', 'schemas/registry.json', 'tools/contracts/options.json', 'tools/contracts/generator-closure.json',
            'tools/contracts/runtime/schema.ts', 'tools/contracts/runtime/patterns.ts', 'schemas/wire/native-carriers-v1.json'):
    assert (W / rel).read_bytes() == (P / rel).read_bytes(), rel

# 9. rustfmt over the three edited Rust files (each base-clean), through stdin.
for rel in ('crates/identity/src/schema_registry.rs', 'crates/identity/src/schema.rs', 'crates/host/src/schema_sources.rs', 'crates/host/tests/admission_tests.rs', 'crates/storage/src/schema_sources.rs'):
    out = subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt', '--edition', '2024', '--emit', 'stdout'], input=(W / rel).read_bytes(), capture_output=True, env=E)
    assert out.returncode == 0, out.stderr; (W / rel).write_bytes(out.stdout)

write(D / 'preparation.json', dict(
    productBase=base, architectureBase=git(A, 'rev-parse', 'HEAD'), candidateWorktree=str(W), archive=PRE,
    newSources=[dict(unit=n['unit'], schemaId=n['schemaId'], productPath=n['path'], architectureSource=n['arch'],
                     definitions=len(n['defs'])) for n in NEW],
    handshake=handshake, generatorTablesUnchanged=True, admissionRegistryArchitectureCopy=am['registryArchitectureSource'], nativeCarriersUnchanged=True,
    HOMEOverride=False, productQualification=False))
print(json.dumps(dict(worktree=str(W), changed=git(W, 'status', '--porcelain').splitlines()), indent=2))
