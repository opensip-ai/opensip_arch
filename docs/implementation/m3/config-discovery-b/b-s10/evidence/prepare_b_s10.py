"""B-S10 (configuration schema admission materialization; B1-a plan r2 §2): prepare an isolated product candidate.
PCS (urn:opensip:product-configuration:2) joins generation (registry.json, source-map.json, options.json) and admission;
the preview v1 carrier (urn:opensip:preview-configuration:1) is admission-only (B1A-PLAN-R2-NBO-01). Follows the
rust3-identity-materialization-r1 precedent's mechanics. Generation runs separately (run_b_s10_generation.py)."""
from pathlib import Path
import json, hashlib, os, subprocess, copy, stat, re
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'; W = A.parent / 'opensip-b-s10'
D = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/b-s10'); S = D / 'architecture'
PRE = 'docs/implementation/m3/config-discovery-b/b-s10'; C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def git(root, *a): return subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
def read(p): return json.loads(p.read_bytes())
def write(p, j): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(j, indent=2) + '\n')
def pin(p, path): b = p.read_bytes(); return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
st = read(C / 'CURRENT-STATE.json'); base = git(P, 'rev-parse', 'HEAD'); assert base == st['productHead'] and git(P, 'status', '--porcelain') == ''
assert not W.exists() and not (D / 'preparation.json').exists()
git(P, 'worktree', 'add', '--detach', str(W), base)
NEW = [dict(schemaId='urn:opensip:product-configuration:2', arch='docs/coop/design-corrections/foundation/product-configuration.schema.v2.json',
            path='schemas/sources/product-configuration-v2.schema.json', sha='591a66e5dc35c4be516eaf68bacc62f9a82260b0c1698665dd85f7613b78e14d', generated=True, major=2),
       dict(schemaId='urn:opensip:preview-configuration:1', arch='docs/coop/completion/preview-configuration.schema.v1.json',
            path='schemas/sources/preview-configuration-v1.schema.json', sha='74b3a3f518ee8b0777dfebf0ea663a0a3c0e5bb0b2f649c393c7f0ac4917a207', generated=False, major=1)]
OWNER = 'crates/host/src/configuration.rs'
# Lead decision (B-S10): the product's exact schema profile (crates/identity/src/schema.rs) admits no `$comment`, and the accepted
# preview carrier has exactly one, a top-level prose note. B-S10 selects a profile-conformant successor copy that removes only that
# member (line 603, and the comma ending line 602); every validating keyword is byte-identical. The parent stays historical.
pv = NEW[1]; raw = (A / pv['arch']).read_bytes(); assert hashlib.sha256(raw).hexdigest() == pv['sha']
lines = raw.decode().split('\n'); assert lines[602].startswith('  "$comment": ') and lines[601] == '  },' and raw.count(b'$comment') == 1
lines[601] = '  }'; del lines[602]; copy_raw = '\n'.join(lines).encode()
a, b = json.loads(raw), json.loads(copy_raw); a.pop('$comment'); assert a == b
pv['parentArch'] = pin(A / pv['arch'], pv['arch']); pv['arch'] = PRE + '/preview-configuration.schema.v1.profiled.json'
(S / pv['arch']).parent.mkdir(parents=True, exist_ok=True); (S / pv['arch']).write_bytes(copy_raw); pv['sha'] = hashlib.sha256(copy_raw).hexdigest()
for n in NEW:
    root = S if n is pv else A
    raw = (root / n['arch']).read_bytes(); assert hashlib.sha256(raw).hexdigest() == n['sha'] and json.loads(raw)['$id'] == n['schemaId']
    assert not (W / n['path']).exists(); (W / n['path']).write_bytes(raw); n['archPin'] = pin(root / n['arch'], n['arch'])
# admission registry (+2 rows, sorted by schemaId), its accepted architecture copy, admission source map
ar = read(W / 'schemas/admission-registry.json'); before = copy.deepcopy(ar)
for n in NEW: ar['sources'].append(dict(schemaId=n['schemaId'], sourcePath=n['path'], bytes=n['archPin']['bytes'], sha256=n['sha']))
ar['sources'].sort(key=lambda r: r['schemaId']); assert [r for r in ar['sources'] if r['schemaId'] not in {n['schemaId'] for n in NEW}] == before['sources']
write(W / 'schemas/admission-registry.json', ar); target = S / PRE / 'admission-registry.json'; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes((W / 'schemas/admission-registry.json').read_bytes())
am = read(W / 'schemas/admission-source-map.json'); parentRegistry = am['registryArchitectureSource']
for n in NEW: am['sources'].append(dict(schemaId=n['schemaId'], implementationPath=n['path'], architectureSource={k: n['archPin'][k] for k in ('path', 'bytes', 'sha256')}))
am['registryArchitectureSource'] = pin(target, PRE + '/admission-registry.json'); write(W / 'schemas/admission-source-map.json', am)
# generation: PCS only (registry.json, source-map.json, options.json)
pcs = NEW[0]
reg = read(W / 'schemas/registry.json')
reg['sources'].append(dict(schemaId=pcs['schemaId'], declaredMajor=2, profile='opensip-exact-schema-reference-1', semanticValidatorOwner=OWNER, sourcePath=pcs['path'], sourceSha256=pcs['sha']))
assert [r['sourcePath'] for r in reg['sources'][:-1]] == sorted(r['sourcePath'] for r in reg['sources'][:-1]); reg['sources'].sort(key=lambda r: r['sourcePath'])  # admission.registry(): sorted unique source paths (attempt 4)
sm = read(W / 'schemas/source-map.json')
sm['sources'].append(dict(schemaId=pcs['schemaId'], implementationPath=pcs['path'], declaredMajor=2, semanticValidatorOwner=OWNER, profile='opensip-exact-schema-reference-1',
                          architectureSource={k: pcs['archPin'][k] for k in ('path', 'sha256', 'bytes')}, namespace='ProductConfiguration2', module='invocation',
                          standing='Accepted product configuration input carrier v2 (MB item 8, FW-13); resolver semantics are B1-a'))
write(W / 'schemas/source-map.json', sm)
opt = read(W / 'tools/contracts/options.json')
opt['owners'].append(dict(schemaId=pcs['schemaId'], namespace='ProductConfiguration2', module='invocation'))
opt['entryPoints'].append(dict(ref=pcs['schemaId'] + '#', typeName='ProductConfiguration2Root', module='invocation'))
opt['sourceMappings'].append(dict(schemaId=pcs['schemaId'], declaredMajor=2, profile='opensip-exact-schema-reference-1', semanticValidatorOwner=OWNER))
opt['sourceMappings'].sort(key=lambda r: r['schemaId']); opt['entryPoints'].sort(key=lambda r: r['ref'])  # adapter.validate_options ordering (attempt 0 refused)
write(W / 'tools/contracts/options.json', opt)
# identity SOURCE_PINS and host SOURCES (sorted by id; same order as the admission registry)
def pin_rs(n):
    d = hashlib.sha256((W / n['path']).read_bytes()).digest(); nums = ', '.join(str(v) for v in d)
    return f'    SourcePin {{\n        id: "{n["schemaId"]}",\n        path: "{n["path"]}",\n        bytes: {n["archPin"]["bytes"]},\n        sha256: [{nums}],\n    }},\n'
p = W / 'crates/identity/src/schema_registry.rs'; text = p.read_text()
block_start = text.index('pub(crate) const SOURCE_PINS: &[SourcePin] = &['); block_end = text.index('\n];', block_start)
entries = re.findall(r'    SourcePin \{.*?\n    \},\n', text[block_start:block_end + 1], re.S); assert len(entries) == 48
ids = [re.search(r'id: "([^"]+)"', e)[1] for e in entries]; assert ids == sorted(ids)
allent = sorted([(i, e) for i, e in zip(ids, entries)] + [(n['schemaId'], pin_rs(n)) for n in NEW]); assert [i for i, _ in allent] == [r['schemaId'] for r in ar['sources']]
head = text[:block_start] + 'pub(crate) const SOURCE_PINS: &[SourcePin] = &[\n'; text = head + ''.join(e for _, e in allent) + text[block_end + 1:]
p.write_text(text)
p = W / 'crates/host/src/schema_sources.rs'; text = p.read_text()
s0 = text.index('const SOURCES: &[&[u8]] = &['); s1 = text.index('\n];', s0)
inc = re.findall(r'    include_bytes!\(concat!\(\n        env!\("CARGO_MANIFEST_DIR"\),\n        "/\.\./\.\./(schemas/sources/[^"]+)"\n    \)\),\n', text[s0:s1 + 1]); assert len(inc) == 48
bypath = {r['sourcePath']: r['schemaId'] for r in ar['sources']}
paths = sorted(inc + [n['path'] for n in NEW], key=lambda x: bypath[x])
body = ''.join(f'    include_bytes!(concat!(\n        env!("CARGO_MANIFEST_DIR"),\n        "/../../{x}"\n    )),\n' for x in paths)
text = text[:s0] + 'const SOURCES: &[&[u8]] = &[\n' + body + text[s1 + 1:]; p.write_text(text)
# storage keeps its own identical SOURCES list (host admission_tests: the_candidate_registry_is_storages_selected_registry)
p = W / 'crates/storage/src/schema_sources.rs'; text = p.read_text(); s0 = text.index('const SOURCES: &[&[u8]] = &['); s1 = text.index('\n];', s0)
inc2 = re.findall(r'"/\.\./\.\./(schemas/sources/[^"]+)"', text[s0:s1 + 1]); assert inc2 == inc, 'storage SOURCES differ from host before the change'
text = text[:s0] + 'const SOURCES: &[&[u8]] = &[\n' + body + text[s1 + 1:]; p.write_text(text)
p = W / 'crates/host/tests/admission_tests.rs'; text = p.read_text()
for old, new in [('    assert_eq!(storage.len(), 48);', '    assert_eq!(storage.len(), 50);'), ("compiles the same 48 pinned", "compiles the same 50 pinned"), ("list the same 48 files, in order.", "list the same 50 files, in order.")]:
    assert text.count(old) == 1, old; text = text.replace(old, new)
p.write_text(text)
# generator closure repin (copy ignored pinned inputs from main checkout, as the precedent did) and registry recipe
closure = read(W / 'tools/contracts/generator-closure.json'); old = copy.deepcopy(closure); repinned = []
allowed = {'schemas/source-map.json', 'schemas/admission-source-map.json', 'schemas/admission-registry.json', 'tools/contracts/options.json', 'schemas/registry.json'}
for row in closure['files']:
    q = W / row['path']
    if not q.exists():
        assert row['path'].startswith(('tools/contracts/node_modules/', 'tools/contracts/python-packages/')); src = P / row['path']; s = src.lstat(); assert stat.S_ISREG(s.st_mode)
        raw = src.read_bytes(); assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']; q.parent.mkdir(parents=True, exist_ok=True); q.write_bytes(raw)
    new = pin(q, row['path'])
    if new != row: assert row['path'] in allowed, row['path']; repinned.append(dict(before=dict(row), after=new)); row.update(new)
paths0 = [r['path'] for r in closure['files']]; assert paths0 == sorted(paths0), 'closure not sorted'
assert set(closure) >= {'files'}; newrow = pin(W / pcs['path'], pcs['path']); assert newrow['path'] not in paths0
closure['files'].append(newrow); closure['files'].sort(key=lambda r: r['path']); added = [newrow]
write(W / 'tools/contracts/generator-closure.json', closure)
reg['recipes'][0]['sourceSha256s'] = sorted({r['sourceSha256'] for r in reg['sources']})
reg['recipes'][0]['generatorClosureSha256'] = pin(W / 'tools/contracts/generator-closure.json', 'x')['sha256']
reg['recipes'][0]['optionsSha256'] = pin(W / 'tools/contracts/options.json', 'x')['sha256']  # r2 (Codex B-S10-R1-RF-01): recipe options pin follows the candidate options
assert reg['recipes'][0]['optionsPath'] == 'tools/contracts/options.json'; write(W / 'schemas/registry.json', reg)
subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt', '--edition', '2024', 'crates/identity/src/schema_registry.rs', 'crates/host/src/schema_sources.rs', 'crates/storage/src/schema_sources.rs'], cwd=W, check=True)  # inserted rows to rustfmt layout
write(D / 'preparation.json', dict(productBase=base, architectureBase=git(A, 'rev-parse', 'HEAD'), worktree=str(W), archive=PRE, newSources=NEW, parentAdmissionRegistry=parentRegistry,
                                    generatorRepins=repinned, generatorClosureAdded=added, standing='UNREVIEWED B-S10 PREPARATION; GENERATION NOT YET RUN'))
print(json.dumps(dict(worktree=str(W), changed=git(W, 'diff', '--name-only').splitlines(), untracked=git(W, 'ls-files', '--others', '--exclude-standard').splitlines(), repinned=[r['after']['path'] for r in repinned]), indent=1))
