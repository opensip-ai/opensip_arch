# S10-TSC preparation (M3-B r8 item 14a, successor S10): the architecture copies and the product source edits.
# Generation (run_s10_tsc_generation.py) and the hand-written product carrier follow; nothing here is accepted.
from pathlib import Path
import copy, hashlib, json, os, re, stat

ARCH = Path('/Users/sb/code/opensip-ai/opensip_arch')
W = Path('/Users/sb/code/opensip-ai/opensip-s10tsc')
MAIN = W.parent / 'opensip'
PRE = 'docs/implementation/m3/config-discovery-b/s10-tsc'
U = ARCH / PRE
D = Path('/tmp/opensip-implementation/s10-tsc')
CODE = 'native.typescript-config-unresolved'
KEYS = ['native.typescript-config-bound', 'native.typescript-config-extends-cycle',
        'native.typescript-config-extends-unresolved', 'native.typescript-config-malformed']
REMEDY = ("the TypeScript configuration could not be read before the Plan: make every extends base of the named "
          "configuration file present as a regular file inside the project, named by a well-formed ./ or ../ relative "
          "path or a lower-case package name, with no symbolic link the snapshot does not admit on its path, installing "
          "its package outside OpenSIP if needed; break any extends cycle; keep each file within 64 KiB and the graph "
          "within 32 files; or correct the file's syntax, so that it is JSONC with extends a string or an array of "
          "strings and allowJs and checkJs booleans")
LAW = 'docs/implementation/m3/config-discovery-b/PROPOSAL-r8.md item 14a'

# Parents (each the head of its accepted line; none carries a bound passage override except SD-7's line 1159).
X4TC = 'docs/implementation/m2/continuation-diagnostics-x4tc-r1/reference/public-detail-registry.json'
NMM = 'docs/implementation/m3/snapshot-plan-c/native-metadata-missing-r1/completion/public-detail-registry.v1.json'
NMM_DESIGN = 'docs/implementation/m3/snapshot-plan-c/native-metadata-missing-r1/completion/design/common.schema.json'
MODEL = 'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py'
MODEL_V2 = 'docs/implementation/m3/native-g/rustflags-long-lint-r1/reference/native_evidence_model.v2.py'
SD7 = 'docs/implementation/m3/supervisor-d/sd-7/successor.json'
ADMISSION = 'docs/implementation/m3/config-discovery-b/b-s10/admission-registry.json'
COMMON = [f'schemas/sources/common-v{v}.schema.json' for v in (1, 3, 4)]


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def dump(j):
    return (json.dumps(j, indent=2) + '\n').encode()


def write(p, j):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_bytes(dump(j))


def pin(p, path):
    raw = Path(p).read_bytes()
    return dict(path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


assert len(REMEDY) <= 1024 and REMEDY.isascii(), len(REMEDY)
for p in (X4TC, NMM_DESIGN, ADMISSION):  # the merged copy takes X4TC's form
    assert dump(read(ARCH / p)) == (ARCH / p).read_bytes(), p
D.mkdir(parents=True, exist_ok=False)
report = dict(standing='UNREVIEWED S10-TSC PREPARATION; NOT ACCEPTED', copies=[])

# 1. The public detail registry: the union of the two accepted lines, plus the new record and its four aliases.
m2, m3 = read(ARCH / X4TC), read(ARCH / NMM)
for key in ('schemaVersion', 'internalAliases', 'aliasRule', 'newInThisCorrection', 'scopeBindingDetailsRegistered'):
    assert m2[key] == m3[key], key
codes2 = {r['code']: r for r in m2['records']}
codes3 = {r['code']: r for r in m3['records']}
assert all(codes2[c] == r for c, r in codes3.items() if c in codes2)
assert CODE not in codes2 and CODE not in codes3
added3 = sorted(set(codes3) - set(codes2))
merged = copy.deepcopy(m2)
merged['standing'] = (
    'Proposed current closed public domain-detail registry (M3-B r8 successor S10, unit S10-TSC). It is the union of '
    'the two accepted registry lines: the m2 line at continuation-diagnostics-x4tc-r1 and the M3 snapshot-plan-c line '
    'at native-metadata-missing-r1, whose records are disjoint additions to one common base and whose shared fields '
    'are equal; plus native.typescript-config-unresolved and its four context-free internal aliases. Existing D9 '
    'class/code/exit unchanged. Historical correction fields retain their original provenance and do not enumerate '
    'later successors.')
merged['records'] = sorted([*m2['records'], *(codes3[c] for c in added3),
                            dict(code=CODE, owner='native',
                                 selector=LAW + '; the pre-Plan TypeScript configuration graph; request-rejected exit 2 '
                                 'CONFIG.INVALID, typed detail carrier request rejection detail')],
                           key=lambda r: r['code'])
assert len({r['code'] for r in merged['records']}) == len(merged['records'])
for key in KEYS:
    assert key not in {a['internalCode'] for a in merged['internalAliases']}
merged['internalAliases'] = sorted([*merged['internalAliases'],
                                    *(dict(internalCode=k, publicCode=CODE, selector=LAW) for k in KEYS)],
                                   key=lambda a: a['internalCode'])
merged['snapshotPlanCCorrections'] = m3['standing']
merged['typescriptConfigRefusalCorrection'] = (
    'M3-B r8 item 14a adds exactly one public detail, native.typescript-config-unresolved, and four internal decision '
    'keys aliased to it: native.typescript-config-extends-unresolved, native.typescript-config-extends-cycle, '
    'native.typescript-config-bound and native.typescript-config-malformed. Each key arises only from a project '
    'configuration file read before the Plan, so its public detail is the same at every originating boundary and the '
    'context-free alias rule admits it. Its D9 row is request-rejected, exit 2, CONFIG.INVALID; its remedy is keyed by '
    'this public detail, not by CONFIG.INVALID, in the selected native model copies of this unit.')
registry = U / 'registry/public-detail-registry.v1.json'
write(registry, merged)
report['copies'].append(dict(candidate=pin(registry, PRE + '/registry/public-detail-registry.v1.json'),
                             parents=[pin(ARCH / X4TC, X4TC), pin(ARCH / NMM, NMM)], recordsFromSnapshotPlanC=added3,
                             recordsAdded=[CODE], aliasesAdded=KEYS))

# 2. The design mirror of the closed enum (workflows common schema), the M3 line's selected copy plus the code.
design = read(ARCH / NMM_DESIGN)
enum = design['$defs']['DomainDetailCode']['enum']
assert CODE not in enum
enum.append(CODE)
target = U / 'design/common.schema.json'
write(target, design)
report['copies'].append(dict(candidate=pin(target, PRE + '/design/common.schema.json'),
                             parents=[pin(ARCH / NMM_DESIGN, NMM_DESIGN)], enumAppended=[CODE]))

# 3. The two native model copies: the effective parent (SD-7's bound line-1159 meaning applied), then one D9_MAP
#    row and one PUBLIC_ROUTE_REMEDIES entry, both keyed by the public detail.
sd7 = [o for o in read(ARCH / SD7)['passageOverrides'] if o['parent']['path'].endswith('native_evidence_model.py')]
assert len(sd7) == 1 and sd7[0]['selector'] == {'line': 1159}
SD7_BEFORE, SD7_AFTER = sd7[0]['before'], sd7[0]['after']
REMEDY_LINES = [
    '    # M3-B r8 item 14a (successor S10): the pre-Plan TypeScript configuration refusal. Its four internal keys\n',
    '    # alias, context-free, to this one public detail, so this one string is true for every one of them.\n',
    f'    "{CODE}": "{REMEDY}",\n',
]
D9_LINES = [
    '    # M3-B r8 item 14a (successor S10): the pre-Plan TypeScript configuration refusal, keyed by its public detail.\n',
    '    # CONFIG.INVALID is its D9 code, not its public detail: CONFIG.INVALID\'s own remedy does not apply to it.\n',
    f'    "{CODE}": {{"class": "request-rejected", "exitCode": 2, "code": "CONFIG.INVALID", "successorCode": None, '
    '"interim": False, "typedDetailCarrier": "request rejection detail"},\n',
]


def model_copy(parent, name):
    lines = (ARCH / parent).read_text(encoding='utf-8').splitlines(keepends=True)
    assert lines[1158].rstrip('\n') == SD7_BEFORE, parent
    lines[1158] = SD7_AFTER + '\n'
    host = [i for i, l in enumerate(lines) if l.startswith('    "HOST.INVARIANT_VIOLATED": ')]
    assert len(host) == 1 and lines[host[0] + 1] == '}\n'
    lines[host[0] + 1:host[0] + 1] = REMEDY_LINES
    anchor = [i for i, l in enumerate(lines) if l.startswith('    "native.boundary-inventory-mismatch": {"class"')]
    assert len(anchor) == 1 and lines[anchor[0] + 1].startswith('    "native.framework-unrecognized": ')
    lines[anchor[0] + 1:anchor[0] + 1] = D9_LINES
    out = U / 'reference' / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(''.join(lines), encoding='utf-8')
    report['copies'].append(dict(candidate=pin(out, f'{PRE}/reference/{name}'), parents=[pin(ARCH / parent, parent)],
                                 boundMeaningApplied=dict(record=SD7, line=1159),
                                 inserted=dict(publicRouteRemedies=len(REMEDY_LINES), d9Map=len(D9_LINES))))


model_copy(MODEL, 'native_evidence_model.py')
model_copy(MODEL_V2, 'native_evidence_model.v2.py')

# 4. Product sources: the closed DomainDetailCode enum gains the member in common v1, v3 and v4 (appended, as the
#    accepted materializations did); every other value unchanged.
for path in COMMON:
    p = W / path
    raw = p.read_bytes()
    j = json.loads(raw)
    assert dump(j) == raw
    before = copy.deepcopy(j)
    en = j['$defs']['DomainDetailCode']['enum']
    assert CODE not in en
    en.append(CODE)
    before['$defs']['DomainDetailCode']['enum'] = list(en)
    assert before == j
    p.write_bytes(dump(j))
    arch_copy = U / 'product' / path
    arch_copy.parent.mkdir(parents=True, exist_ok=True)
    arch_copy.write_bytes(dump(j))

# 5. The generation and admission source maps select the S10 architecture copies of the three changed sources.
for name in ('schemas/source-map.json', 'schemas/admission-source-map.json'):
    m = read(W / name)
    for path in COMMON:
        rows = [r for r in m['sources'] if r['implementationPath'] == path]
        assert len(rows) == 1, (name, path)
        rows[0]['architectureSource'] = pin(U / 'product' / path, f'{PRE}/product/{path}')
    write(W / name, m)

# 6. The admission registry: re-pin the three changed sources (and any alias rows on them); select an S10 copy.
adm = read(W / 'schemas/admission-registry.json')
assert dump(adm) == (ARCH / ADMISSION).read_bytes(), 'product admission registry is not the selected B-S10 copy'
before = copy.deepcopy(adm)
repinned = []
for group in ('sources', 'aliases'):
    for row in adm.get(group, []):
        if row['sourcePath'] in COMMON:
            raw = (W / row['sourcePath']).read_bytes()
            row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
            repinned.append(dict(group=group, **row))
for group in ('sources', 'aliases'):
    for a, b in zip(before.get(group, []), adm.get(group, [])):
        assert {k: v for k, v in a.items() if k not in ('bytes', 'sha256')} == \
            {k: v for k, v in b.items() if k not in ('bytes', 'sha256')}
write(W / 'schemas/admission-registry.json', adm)
write(U / 'admission-registry.json', adm)
m = read(W / 'schemas/admission-source-map.json')
m['registryArchitectureSource'] = pin(U / 'admission-registry.json', PRE + '/admission-registry.json')
write(W / 'schemas/admission-source-map.json', m)
report['admissionRegistry'] = dict(parent=pin(ARCH / ADMISSION, ADMISSION), repinnedRows=repinned,
                                   candidate=pin(U / 'admission-registry.json', PRE + '/admission-registry.json'))

# 7. The identity crate's compiled full-document SOURCE_PINS for the three sources.
p = W / 'crates/identity/src/schema_registry.rs'
text = p.read_text()
pins = []
for source in COMMON:
    raw = (W / source).read_bytes()
    digest = hashlib.sha256(raw).digest()
    pattern = (r'(SourcePin \{\s*id: "[^"]+",\s*path: "' + re.escape(source) +
               r'",\s*bytes: )\d+(,\s*sha256: \[)[\d,\s]+(\],\s*\})')
    text, count = re.subn(pattern, lambda mm: mm[1] + str(len(raw)) + mm[2] + ', '.join(str(v) for v in digest) +
                          ',\n        ' + mm[3], text)
    assert count == 1, source
    pins.append(dict(path=source, bytes=len(raw), sha256=digest.hex()))
p.write_text(text)
report['sourcePins'] = pins

# 8. The generator closure: copy its pinned untracked inputs from the main checkout (exact bytes, no link), then
#    re-pin the changed rows; the registry recipe follows.
closure = read(W / 'tools/contracts/generator-closure.json')
copied = 0
for row in closure['files']:
    q = W / row['path']
    if q.exists():
        continue
    assert row['path'].startswith(('tools/contracts/node_modules/', 'tools/contracts/python-packages/')), row['path']
    src = MAIN / row['path']
    st = src.lstat()
    assert stat.S_ISREG(st.st_mode)
    fd = os.open(src, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    with os.fdopen(fd, 'rb') as f:
        raw = f.read()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes(raw)
    copied += 1
changed = []
for row in closure['files']:
    raw = (W / row['path']).read_bytes()
    after = dict(path=row['path'], bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    if after != row:
        changed.append(dict(before=dict(row), after=after))
        row.update(after)
allowed = {'schemas/source-map.json', 'schemas/admission-source-map.json', *COMMON}
assert {c['after']['path'] for c in changed} <= allowed, changed
write(W / 'tools/contracts/generator-closure.json', closure)
reg = read(W / 'schemas/registry.json')
for row in reg['sources']:
    if row['sourcePath'] in COMMON:
        row['sourceSha256'] = hashlib.sha256((W / row['sourcePath']).read_bytes()).hexdigest()
reg['recipes'][0]['sourceSha256s'] = sorted({row['sourceSha256'] for row in reg['sources']})
reg['recipes'][0]['generatorClosureSha256'] = hashlib.sha256((W / 'tools/contracts/generator-closure.json').read_bytes()).hexdigest()
write(W / 'schemas/registry.json', reg)
report.update(generatorInputsCopied=copied, generatorClosureChangedRows=changed, remedy=dict(text=REMEDY,
              characters=len(REMEDY), sha256=hashlib.sha256(REMEDY.encode()).hexdigest()))
write(D / 'preparation.json', report)
print('S10-TSC prepared: registry, design mirror, two model copies, three sources, maps, admission, pins, closure;',
      copied, 'pinned generator inputs copied. Unreviewed.')
