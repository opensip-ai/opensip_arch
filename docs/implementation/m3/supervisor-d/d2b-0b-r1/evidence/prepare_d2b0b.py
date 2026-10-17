"""Prepare the D2b-0b candidate (D2b plan r3 amendment A1, LD-D2B0-A): the successor schemas' generation, in a detached
worktree at product main. No commit, no push.
  1. The generator's pattern profile, extended by the M1 method (trials/ts-runtime-02/subject/pattern-profile.py, as
     grok-schema-pattern-trials-01 reviewed it): the two accepted successor schema documents join the profile's sources;
     every pattern of the sources is collected by the method's own visit(), translated by its own translate()
     (unescaped `.` and `$` outside classes rewritten, all else verbatim), and rendered by its own patterns.ts template.
     Asserted: the existing profile reproduces from its existing sources; exactly one pattern is new
     (symbol-census-v1's SubjectIdV1); every existing table entry is unchanged.
  2. The generator rows (LD-D2B0b-1 to LD-D2B0b-4, re-making D2b-0's deferred LD-D2B0-1 to 4): source-map, generation
     registry, options owners, source mappings and entry points; no providerEntryPoints.
  3. The generator closure re-pinned (the two sources added; source-map, options and the two runtime pattern files
     re-pinned), and the registry recipe (source set, closure digest, options digest).
The generation itself is run_d2b0b_generation.py."""
from pathlib import Path
import copy, hashlib, json, os, stat, subprocess

B = Path('/tmp/opensip-implementation'); A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'
W = A.parent / 'opensip-d2b0b'; D = B / 'd2b0b-materialization-r1'
FA = 'docs/implementation/m3/native-successors-fa/'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def git(root, *a): return subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
def read(p): return json.loads(p.read_bytes())
def write(p, j): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(j, indent=2) + '\n')
def pin(root, path): b = (root / path).read_bytes(); return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def insert_sorted(rows, row, key):
    assert all(r[key] != row[key] for r in rows), row[key]
    at = next((i for i, r in enumerate(rows) if r[key] > row[key]), len(rows)); rows.insert(at, row); return at

# The M1 method's own functions (trials/ts-runtime-02/subject/pattern-profile.py), verbatim but for visit's accumulator.
def visit(schema, patterns):
    if not isinstance(schema, dict):
        return
    if 'pattern' in schema:
        patterns.add(schema['pattern'])
    patterns.update(schema.get('patternProperties', {}))
    for key in ('properties', 'patternProperties', '$defs', 'definitions'):
        for child in schema.get(key, {}).values():
            visit(child, patterns)
    for key in ('additionalProperties', 'propertyNames', 'items', 'contains', 'if', 'then', 'else', 'not'):
        if key in schema:
            visit(schema[key], patterns)
    for key in ('allOf', 'anyOf', 'oneOf'):
        for child in schema.get(key, []):
            visit(child, patterns)
def translate(pattern):
    result = []
    escaped = False
    in_class = False
    for char in pattern:
        if escaped:
            result.append(char)
            escaped = False
        elif char == '\\':
            result.append(char)
            escaped = True
        elif char == '[':
            in_class = True
            result.append(char)
        elif char == ']':
            in_class = False
            result.append(char)
        elif not in_class and char == '.':
            result.append('[^\\n]')
        elif not in_class and char == '$':
            result.append('(?=\\n?(?![\\s\\S]))')
        else:
            result.append(char)
    assert not escaped and not in_class
    return ''.join(result)
def render(table):
    return ('/** Generated trial table from pattern-profile.py; reviewed source profile required. */\n'
            + 'const patterns = new Map<string, string>(' + json.dumps(table, indent=2) + ');\n'
            + 'export const selectedPattern = (pattern: string): string | undefined => patterns.get(pattern);\n')
def table_of(text):
    m = text[text.index('new Map<string, string>(') + len('new Map<string, string>('):]; return json.loads(m[:m.index(']);') + 1])

# The two accepted successor documents (FA-2 and RUST3-LIM contract successors; D2b-0 admitted them).
NEW = []
for unit, namespace in (('fa-2', 'SymbolCensus1'), ('rust3-lim', 'RustSubjectScope1')):   # LD-D2B0b-1
    m = read(A / FA / unit / 'materialization-map.json'); r = [x for x in m['files'] if x['before'] is None][0]
    arch = pin(A, r['candidatePath']); assert {k: arch[k] for k in ('bytes', 'sha256')} == r['after']
    doc = read(A / r['candidatePath'])
    NEW.append(dict(unit=unit, schemaId=doc['$id'], path=r['productPath'], arch=arch, namespace=namespace,
                    major=int(doc['$id'].rsplit('.', 1)[1]), defs=sorted(doc['$defs'])))
OWNER = 'crates/components/src/provider_protocol.rs'                                         # LD-D2B0b-2
STANDING = 'Proposed current or retained schema source; no semantic implementation claim'     # LD-D2B0b-2, verbatim
base = git(P, 'rev-parse', 'HEAD'); assert git(P, 'status', '--porcelain') == ''
for n in NEW: assert (P / n['path']).read_bytes() == (A / n['arch']['path']).read_bytes(), 'D2b-0 is not on main'
assert not W.exists() and not D.exists()
git(P, 'worktree', 'add', '--detach', str(W), base); D.mkdir(parents=True)

# 1. The pattern profile.
PF = 'tools/contracts/runtime/pattern-profile.json'; PT = 'tools/contracts/runtime/patterns.ts'
profile = read(W / PF); old_table = table_of((W / PT).read_text()); assert render(old_table) == (W / PT).read_text()
old_patterns = set()
for s in profile['sources']: assert pin(A, s['path']) == {**s}, s['path']; visit(read(A / s['path']), old_patterns)
assert old_patterns == {r['source'] for r in profile['patterns']} and all(r['ecma262Unicode'] == translate(r['source']) for r in profile['patterns'])
assert [s['path'] for s in profile['sources']] == sorted(s['path'] for s in profile['sources'])
new_profile = copy.deepcopy(profile)
for n in NEW: insert_sorted(new_profile['sources'], dict(path=n['arch']['path'], sha256=n['arch']['sha256'], bytes=n['arch']['bytes']), 'path')
patterns = set()
for s in new_profile['sources']: visit(read(A / s['path']), patterns)
new_profile['patterns'] = [dict(source=p, ecma262Unicode=translate(p)) for p in sorted(patterns)]
added = sorted(patterns - old_patterns)
assert added == ['^[a-z][a-z0-9-]*:[^\\u0000-\\u001f\\u007f-\\u009f]+(?![\\s\\S])'], added
assert [r for r in new_profile['patterns'] if r['source'] in old_patterns] == profile['patterns']
table = sorted(old_table + [[r['source'], r['ecma262Unicode']] for r in new_profile['patterns'] if r['source'] in added and r['source'] not in {t[0] for t in old_table}])
assert [t for t in table if t[0] not in added] == old_table and len(table) == len(old_table) + 1
write(W / PF, new_profile); (W / PT).write_text(render(table))
assert json.dumps(new_profile, indent=2) + '\n' == (W / PF).read_text()

# 2. The generator rows.
sm = read(W / 'schemas/source-map.json'); reg = read(W / 'schemas/registry.json'); opt = read(W / 'tools/contracts/options.json'); before_opt = copy.deepcopy(opt)
arch_pin = lambda n: dict(path=n['arch']['path'], bytes=n['arch']['bytes'], sha256=n['arch']['sha256'])
for n in NEW:
    insert_sorted(sm['sources'], dict(schemaId=n['schemaId'], implementationPath=n['path'], declaredMajor=n['major'], semanticValidatorOwner=OWNER,
        profile='opensip-exact-schema-reference-1', architectureSource=arch_pin(n), namespace=n['namespace'], module='protocol', standing=STANDING), 'schemaId')
    insert_sorted(reg['sources'], dict(schemaId=n['schemaId'], declaredMajor=n['major'], profile='opensip-exact-schema-reference-1',
        semanticValidatorOwner=OWNER, sourcePath=n['path'], sourceSha256=n['arch']['sha256']), 'sourcePath')
    insert_sorted(opt['owners'], dict(schemaId=n['schemaId'], namespace=n['namespace'], module='protocol'), 'schemaId')
    insert_sorted(opt['sourceMappings'], dict(schemaId=n['schemaId'], declaredMajor=n['major'], profile='opensip-exact-schema-reference-1',
                  semanticValidatorOwner=OWNER), 'schemaId')
    # LD-D2B0b-3: every $def, typeName = namespace + definition name; no Root (common-v4, graph-query-v4).
    for d in n['defs']:
        insert_sorted(opt['entryPoints'], dict(ref=n['schemaId'] + '#/$defs/' + d.replace('~', '~0').replace('/', '~1'), typeName=n['namespace'] + d, module='protocol'), 'ref')
assert [r['ref'] for r in opt['entryPoints']] == sorted(r['ref'] for r in opt['entryPoints'])
assert [r['schemaId'] for r in opt['sourceMappings']] == sorted(r['schemaId'] for r in opt['sourceMappings'])
assert opt['providerEntryPoints'] == before_opt['providerEntryPoints'] and opt['deniedRefs'] == before_opt['deniedRefs']   # LD-D2B0b-4
added_eps = len(opt['entryPoints']) - len(before_opt['entryPoints']); assert added_eps == 25, added_eps
write(W / 'schemas/source-map.json', sm); write(W / 'tools/contracts/options.json', opt)

# 3. The generator closure and the registry recipe.
closure = read(W / 'tools/contracts/generator-closure.json'); old_closure = copy.deepcopy(closure); copied = []; repinned = []
for n in NEW: insert_sorted(closure['files'], dict(path=n['path'], bytes=n['arch']['bytes'], sha256=n['arch']['sha256']), 'path')
allowed = {'schemas/source-map.json', 'tools/contracts/options.json', PF, PT}
for row in closure['files']:
    q = W / row['path']
    if not q.exists():
        assert row['path'].startswith(('tools/contracts/node_modules/', 'tools/contracts/python-packages/')), row['path']
        src = P / row['path']; s = src.lstat(); assert stat.S_ISREG(s.st_mode)
        fd = os.open(src, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        with os.fdopen(fd, 'rb') as f:
            b4 = os.fstat(f.fileno()); raw = f.read(); af = os.fstat(f.fileno())
        assert (s.st_dev, s.st_ino) == (b4.st_dev, b4.st_ino) and (b4.st_size, b4.st_mtime_ns, b4.st_ctime_ns) == (af.st_size, af.st_mtime_ns, af.st_ctime_ns)
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
        q.parent.mkdir(parents=True, exist_ok=True); q.write_bytes(raw); q.chmod(stat.S_IMODE(s.st_mode)); copied.append(row['path'])
    new = pin(W, row['path'])
    if new != row: assert row['path'] in allowed, row['path']; repinned.append(dict(before=dict(row), after=new)); row.update(new)
assert [r['path'] for r in closure['files']] == sorted(r['path'] for r in closure['files'])
assert sorted(set(r['path'] for r in closure['files']) - set(r['path'] for r in old_closure['files'])) == sorted(n['path'] for n in NEW)
assert sorted(r['before']['path'] for r in repinned) == sorted(allowed)
write(W / 'tools/contracts/generator-closure.json', closure)
recipe = reg['recipes'][0]; old_recipe = copy.deepcopy(recipe)
recipe['sourceSha256s'] = sorted({r['sourceSha256'] for r in reg['sources']})
recipe['generatorClosureSha256'] = pin(W, 'tools/contracts/generator-closure.json')['sha256']
recipe['optionsSha256'] = pin(W, 'tools/contracts/options.json')['sha256']
write(W / 'schemas/registry.json', reg)
write(D / 'preparation.json', dict(
    productBase=base, architectureBase=git(A, 'rev-parse', 'HEAD'), candidateWorktree=str(W),
    patternProfile=dict(sourcesBefore=len(profile['sources']), sourcesAfter=len(new_profile['sources']), rowsBefore=len(profile['patterns']),
                        rowsAfter=len(new_profile['patterns']), tableBefore=len(old_table), tableAfter=len(table), added=[dict(source=p, ecma262Unicode=translate(p)) for p in added],
                        existingProfileReproducesFromItsSources=True, existingTableEntriesUnchanged=True,
                        tableEntriesOutsideProfile=sorted(t[0] for t in old_table if t[0] not in old_patterns)),
    newSources=[dict(unit=n['unit'], schemaId=n['schemaId'], productPath=n['path'], architectureSource=n['arch'], namespace=n['namespace'], definitions=len(n['defs'])) for n in NEW],
    entryPointsAdded=added_eps, providerEntryPointsUnchanged=True, deniedRefsUnchanged=True, closureRowsAdded=[n['path'] for n in NEW], closureRepins=repinned,
    exactPinnedIgnoredInputsCopied=len(copied), recipeBefore={k: old_recipe[k] for k in ('generatorClosureSha256', 'optionsSha256')},
    recipeAfter={k: recipe[k] for k in ('generatorClosureSha256', 'optionsSha256')}, nativeCarriersUnchanged=True, HOMEOverride=False, productQualification=False))
print(json.dumps(dict(worktree=str(W), changed=git(W, 'status', '--porcelain').splitlines()), indent=2))
