"""Prepare the C1b-0 candidate (C1b plan r3, sub-unit C1b-0; M3-B successor S4 as B-S2 defines it): B-S2's merge rule
applied to the product's identity-v3 source, in a detached worktree at product main. Re-runnable for a rebase: with
--rebuild it removes this script's own worktree and stage first, then rebuilds everything from the current main.
  1. identity-v3: `#/$defs/vcs-observation` replaced by B-S2's `oneOf`; `vcs-observation-v2` (asserted equal to the
     product's current `vcs-observation`), `vcs-observation-v3` and `vcs-member-observation` added after it. Nothing
     else changes. Serialized as the file is (indent 2, ASCII, a final newline). The bytes are also the package's
     architecture source (product/schemas/sources/identity-v3.schema.json).
  2. The source map and admission source map re-pointed to that source; the admission registry re-pinned, with its
     architecture copy; the identity crate's compiled SourcePin re-pinned.
  3. The generator options: one entry point per added definition, typeName `Identity3` + the definition's PascalCase
     spelling, the rule every identity-v3 entry point already follows (LD-C1B0-1).
  4. The generator closure re-pinned (identity-v3, source-map, options) and the registry recipe (source set, closure
     digest, options digest).
  5. The evaluator's member join beside VCS_KIND_JOIN, and the host control module (S4's vectors and negatives).
  6. rustfmt over the edited Rust files, each base-clean, through stdin.
The generation itself is run_c1b0_generation.py. No commit, no push."""
from pathlib import Path
import copy, hashlib, json, os, re, shutil, stat, subprocess, sys

B = Path('/tmp/opensip-implementation'); A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'
W = A.parent / 'opensip-c1b0'; D = B / 'c1b0-materialization-r2'
PRE = 'docs/implementation/m3/snapshot-plan-c/c1b-0-r2'; U = A / PRE
FRAGMENT = 'docs/implementation/m3/config-discovery-b/b-s2/schemas/identity-schemas.v3.b-s2-additions.json'
ID3 = 'schemas/sources/identity-v3.schema.json'; ID3_URN = 'urn:opensip:product-v1:identity:v3'
ARCH_ID3 = PRE + '/product/' + ID3; ARCH_REGISTRY = PRE + '/admission-registry.json'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def git(root, *a): return subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
def read(p): return json.loads(p.read_bytes())
def write(p, j): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(j, indent=2) + '\n')
def pin(root, path): b = (root / path).read_bytes(); return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def insert_sorted(rows, row, key):
    assert all(r[key] != row[key] for r in rows), row[key]
    at = next((i for i, r in enumerate(rows) if r[key] > row[key]), len(rows)); rows.insert(at, row); return at
def replace_once(text, old, new):
    assert text.count(old) == 1, old[:80]; return text.replace(old, new)
def pascal(name): return ''.join(w[:1].upper() + w[1:] for w in re.split('[-_]', name))

if '--rebuild' in sys.argv[1:]:
    if W.exists():
        assert git(W, 'rev-parse', '--show-toplevel') == str(W)
        git(P, 'worktree', 'remove', '--force', str(W))
    if D.exists(): shutil.rmtree(D)
base = git(P, 'rev-parse', 'HEAD'); assert git(P, 'status', '--porcelain') == ''
assert not W.exists() and not D.exists()
git(P, 'worktree', 'add', '--detach', str(W), base); D.mkdir(parents=True)

# 1. identity-v3, by B-S2's merge rule.
raw = (W / ID3).read_bytes(); doc = json.loads(raw)
assert (json.dumps(doc, indent=2) + '\n').encode() == raw, 'identity-v3 is not in its canonical file form'
frag = read(A / FRAGMENT)['$defs']
assert doc['$defs']['vcs-observation'] == frag['vcs-observation-v2'], "the product's vcs-observation is not B-S2's schema 2"
assert all(k not in doc['$defs'] for k in ('vcs-observation-v2', 'vcs-observation-v3', 'vcs-member-observation'))
for name in ('Hash', 'LogicalPath', 'Text'): assert name in doc['$defs'], name
ADDED = ['vcs-observation-v2', 'vcs-observation-v3', 'vcs-member-observation']
defs = {}
for k, v in doc['$defs'].items():
    if k == 'vcs-observation':
        defs[k] = frag['vcs-observation']
        for a in ADDED: defs[a] = frag[a]
    else:
        defs[k] = v
merged = copy.deepcopy(doc); merged['$defs'] = defs
assert {k: v for k, v in merged.items() if k != '$defs'} == {k: v for k, v in doc.items() if k != '$defs'}
assert [k for k in merged['$defs'] if k not in ADDED] == list(doc['$defs'])
assert all(merged['$defs'][k] == doc['$defs'][k] for k in doc['$defs'] if k != 'vcs-observation')
out = (json.dumps(merged, indent=2) + '\n').encode()
(W / ID3).write_bytes(out); (A / ARCH_ID3).parent.mkdir(parents=True, exist_ok=True); (A / ARCH_ID3).write_bytes(out)
arch_id3 = pin(A, ARCH_ID3)

# 2. The maps, the admission registry (and its architecture copy) and the compiled pin.
sm = read(W / 'schemas/source-map.json'); am = read(W / 'schemas/admission-source-map.json'); ar = read(W / 'schemas/admission-registry.json')
for m in (sm, am):
    rows = [r for r in m['sources'] if r['implementationPath'] == ID3]; assert len(rows) == 1
    rows[0]['architectureSource'] = arch_id3
before_ar = copy.deepcopy(ar); hit = 0
for group in ('sources', 'aliases'):
    for row in ar[group]:
        if row['sourcePath'] == ID3: row.update(bytes=arch_id3['bytes'], sha256=arch_id3['sha256']); hit += 1
    for old, new in zip(before_ar[group], ar[group]):
        assert {k: v for k, v in old.items() if k not in ('bytes', 'sha256')} == {k: v for k, v in new.items() if k not in ('bytes', 'sha256')}
        if old['sourcePath'] != ID3: assert old == new
assert hit == 1, hit
write(W / 'schemas/source-map.json', sm); write(W / 'schemas/admission-registry.json', ar); write(A / ARCH_REGISTRY, ar)
am['registryArchitectureSource'] = pin(A, ARCH_REGISTRY); write(W / 'schemas/admission-source-map.json', am)
p = W / 'crates/identity/src/schema_registry.rs'; text = p.read_text()
digest = hashlib.sha256(out).digest()
pattern = r'(SourcePin \{\s*id: "' + re.escape(ID3_URN) + r'",\s*path: "' + re.escape(ID3) + r'",\s*bytes: )\d+(,\s*sha256: \[)[\d,\s]+(\],\s*\})'
text, count = re.subn(pattern, lambda m: m[1] + str(len(out)) + m[2] + ', '.join(str(v) for v in digest) + ',\n        ' + m[3], text); assert count == 1
p.write_text(text)

# 3. The generator options: the added definitions' entry points.
opt = read(W / 'tools/contracts/options.json'); before_opt = copy.deepcopy(opt)
existing = [e for e in opt['entryPoints'] if e['ref'].startswith(ID3_URN + '#/$defs/') and '/' not in e['ref'].split('#/$defs/')[1]]
assert all(e['typeName'] == 'Identity3' + pascal(e['ref'].split('#/$defs/')[1]) and e['module'] == 'identity' for e in existing)
for a in ADDED:
    insert_sorted(opt['entryPoints'], dict(ref=ID3_URN + '#/$defs/' + a, typeName='Identity3' + pascal(a), module='identity'), 'ref')
assert [r['ref'] for r in opt['entryPoints']] == sorted(r['ref'] for r in opt['entryPoints'])
assert {k: v for k, v in opt.items() if k != 'entryPoints'} == {k: v for k, v in before_opt.items() if k != 'entryPoints'}
write(W / 'tools/contracts/options.json', opt)

# 4. The generator closure and the registry recipe.
reg = read(W / 'schemas/registry.json')
rows = [r for r in reg['sources'] if r['sourcePath'] == ID3]; assert len(rows) == 1; rows[0]['sourceSha256'] = arch_id3['sha256']
closure = read(W / 'tools/contracts/generator-closure.json'); old_closure = copy.deepcopy(closure); copied = []; repinned = []
allowed = {ID3, 'schemas/source-map.json', 'tools/contracts/options.json'}
for row in closure['files']:
    q = W / row['path']
    if not q.exists():
        assert row['path'].startswith(('tools/contracts/node_modules/', 'tools/contracts/python-packages/')), row['path']
        src = P / row['path']; s = src.lstat(); assert stat.S_ISREG(s.st_mode)
        fd = os.open(src, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        with os.fdopen(fd, 'rb') as f:
            b4 = os.fstat(f.fileno()); data = f.read(); af = os.fstat(f.fileno())
        assert (s.st_dev, s.st_ino) == (b4.st_dev, b4.st_ino) and (b4.st_size, b4.st_mtime_ns, b4.st_ctime_ns) == (af.st_size, af.st_mtime_ns, af.st_ctime_ns)
        assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
        q.parent.mkdir(parents=True, exist_ok=True); q.write_bytes(data); q.chmod(stat.S_IMODE(s.st_mode)); copied.append(row['path'])
    new = pin(W, row['path'])
    if new != row: assert row['path'] in allowed, row['path']; repinned.append(dict(before=dict(row), after=new)); row.update(new)
assert [r['path'] for r in closure['files']] == [r['path'] for r in old_closure['files']]
assert sorted(r['before']['path'] for r in repinned) == sorted(allowed), repinned
write(W / 'tools/contracts/generator-closure.json', closure)
recipe = reg['recipes'][0]; old_recipe = copy.deepcopy(recipe)
recipe['sourceSha256s'] = sorted({r['sourceSha256'] for r in reg['sources']})
recipe['generatorClosureSha256'] = pin(W, 'tools/contracts/generator-closure.json')['sha256']
recipe['optionsSha256'] = pin(W, 'tools/contracts/options.json')['sha256']
write(W / 'schemas/registry.json', reg)

# 5a. The evaluator: the VCS joins as one helper, with the member join beside the top-level kind join (BS2-F2).
p = W / 'crates/evaluator/src/run_links.rs'; text = p.read_text()
text = replace_once(text, '''    require(
        (text(field(&vcs, "kind")?)? == "none") == (*field(&vcs, "commitId")? == V::Null),
        "VCS_KIND_JOIN",
    )?;
    Ok(imports)
}''', '''    vcs_joins(&vcs)?;
    Ok(imports)
}
/// The VCS observation's joins: at the top level, `kind: none` exactly when
/// `commitId` is null (VCS_KIND_JOIN, schema 2 and 3 alike); and, for schema
/// 3 (M3-B successor S4, unit C1b-0), each member is a Git repository with a
/// commit (VCS_MEMBER_JOIN). Identity admission already enforces the member
/// shape; the join states the Run closure's own reading of it.
fn vcs_joins(vcs: &V) -> Result<(), RunLinkError> {
    require(
        (text(field(vcs, "kind")?)? == "none") == (*field(vcs, "commitId")? == V::Null),
        "VCS_KIND_JOIN",
    )?;
    if let V::Object(record) = vcs
        && let Some(members) = record.get("members")
    {
        for member in array(members)? {
            require(
                text(field(member, "kind")?)? == "git" && *field(member, "commitId")? != V::Null,
                "VCS_MEMBER_JOIN",
            )?;
        }
    }
    Ok(())
}''')
text = text.rstrip('\n') + '''

#[cfg(test)]
mod vcs_join_tests {
    use super::{RunLinkError, vcs_joins};
    use opensip_identity::JsonValue as V;

    fn parse(raw: &str) -> V {
        opensip_identity::parse_json(raw.as_bytes()).unwrap()
    }
    fn refused(raw: &str) -> Option<alloc::string::String> {
        match vcs_joins(&parse(raw)) {
            Err(RunLinkError::Refused(cause)) => Some(cause),
            _ => None,
        }
    }

    /// C1b-0 (S4): the top-level kind join holds for schema 2 and schema 3,
    /// and a schema-3 member must be a Git repository with a commit.
    #[test]
    fn the_vcs_joins_read_the_top_level_and_every_member() {
        let member = r#"{"commitId":"0123456789abcdef0123456789abcdef01234567","dirty":true,"kind":"git","path":"serde"}"#;
        for ok in [
            r#"{"commitId":null,"kind":"none"}"#,
            r#"{"commitId":"aaaa","kind":"git"}"#,
        ] {
            assert!(vcs_joins(&parse(ok)).is_ok(), "{ok}");
        }
        let with_member = alloc::format!(r#"{{"commitId":null,"kind":"none","members":[{member}]}}"#);
        assert!(vcs_joins(&parse(&with_member)).is_ok(), "{with_member}");
        assert_eq!(refused(r#"{"commitId":"aaaa","kind":"none"}"#).as_deref(), Some("VCS_KIND_JOIN"));
        assert_eq!(refused(r#"{"commitId":null,"kind":"git"}"#).as_deref(), Some("VCS_KIND_JOIN"));
        for bad in [
            member.replace(r#""kind":"git""#, r#""kind":"hg""#),
            member.replace(r#""commitId":"0123456789abcdef0123456789abcdef01234567""#, r#""commitId":null"#),
        ] {
            let raw = alloc::format!(r#"{{"commitId":null,"kind":"none","members":[{bad}]}}"#);
            assert_eq!(refused(&raw).as_deref(), Some("VCS_MEMBER_JOIN"), "{raw}");
        }
    }
}
'''
p.write_text(text)

# 5b. The host control: S4's vectors and negatives, through identity admission and the Run closure's record check.
p = W / 'crates/host/src/schema_sources.rs'
p.write_text(p.read_text().rstrip('\n') + '\n' + (Path(__file__).parent / 's4_controls.rs').read_text())

# 6. rustfmt over the edited Rust files (each base-clean), through stdin.
for rel in ('crates/identity/src/schema_registry.rs', 'crates/host/src/schema_sources.rs', 'crates/evaluator/src/run_links.rs'):
    base_raw = subprocess.run(['/usr/bin/git', 'show', 'HEAD:' + rel], cwd=W, env=E, capture_output=True, check=True).stdout
    clean = subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt', '--edition', '2024', '--emit', 'stdout'], input=base_raw, capture_output=True, env=E)
    assert clean.returncode == 0 and clean.stdout == base_raw, rel + ' is not base-clean'
    fmt = subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt', '--edition', '2024', '--emit', 'stdout'], input=(W / rel).read_bytes(), capture_output=True, env=E)
    assert fmt.returncode == 0, fmt.stderr; (W / rel).write_bytes(fmt.stdout)

write(D / 'preparation.json', dict(
    productBase=base, architectureBase=git(A, 'rev-parse', 'HEAD'), candidateWorktree=str(W), archive=PRE,
    identityV3=dict(before=dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()), after=arch_id3, definitionsAdded=ADDED,
                    vcsObservationReplacedByOneOf=True, otherDefinitionsUnchanged=True, bS2Fragment=pin(A, FRAGMENT)),
    admissionRegistryArchitectureCopy=am['registryArchitectureSource'], entryPointsAdded=[e for e in opt['entryPoints'] if e['ref'].split('#/$defs/')[-1] in ADDED],
    closureRepins=repinned, exactPinnedIgnoredInputsCopied=len(copied),
    recipeBefore={k: old_recipe[k] for k in ('generatorClosureSha256', 'optionsSha256')}, recipeAfter={k: recipe[k] for k in ('generatorClosureSha256', 'optionsSha256')},
    architectureIdsBundleUnchanged=True, HOMEOverride=False, productQualification=False))
print(json.dumps(dict(worktree=str(W), base=base, changed=git(W, 'status', '--porcelain').splitlines()), indent=2))
