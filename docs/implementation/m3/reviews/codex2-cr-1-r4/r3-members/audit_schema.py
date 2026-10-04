"""Audit CR-1's successor copy of the completed manifest schema with an independent JSON Schema
engine (r2, RF-CR1-1). Read-only; with --write it writes evidence/schema-audit.json, otherwise it
compares with that file.

Usage: audit_schema.py --deps DIR [--product PATH] [--rev REV] [--write]
- DIR holds jsonschema 4.25.1 and its dependencies, installed offline, for example
  python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels
  --target DIR jsonschema==4.25.1
- PATH (default /Users/sb/code/opensip-ai/opensip) and REV (default 392499e) name the product
  fixture crates/security/tests/fixtures/manifest268-shape.ndjson, read with `git show`.

It shows four things with Draft202012Validator:
1. the parent schema reproduces every verdict of the product's 11,010-case shape fixture, which is
   the oracle the generated Rust shape is tested against;
2. the copy gives the same verdict as the parent on every one of those cases, so no existing case
   flips;
3. for each of the fixture's five valid base manifests: an analyzer still needs a non-empty
   command tree; each closure-only role admits with `commands` absent, and refuses with `commands`
   present as a tree, as `[]` or as null; and the parent refuses every closure-only role;
4. the copy uses only the keywords the product's shape generator accepts.
Run with python3 -I -B at nice -n 19.
"""
import copy, hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


DEPS = opt('--deps', None)
W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', '392499e')
WRITE = '--write' in args
assert DEPS, '--deps DIR is required'
sys.path.insert(0, DEPS)
import jsonschema  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402
from importlib.metadata import version  # noqa: E402

M = 'docs/implementation/m3/snapshot-plan-c/'
PARENT = 'docs/coop/completion/manifest-schema.completed.v1.json'
COPY = M + 'cr-1/completion/manifest-schema.completed.v1.json'
OUT = A / M / 'cr-1/evidence/schema-audit.json'
FIXTURE = 'crates/security/tests/fixtures/manifest268-shape.ndjson'
CLOSURE_ONLY = ['toolchain', 'stdlib', 'rust-dev-llvm', 'grammar']
GENERATOR_KEYWORDS = {'$schema', '$id', '$comment', '$defs', '$ref', 'type', 'properties', 'required',
                      'additionalProperties', 'oneOf', 'const', 'enum', 'pattern', 'minimum', 'maximum', 'minLength',
                      'maxLength', 'minItems', 'maxItems', 'uniqueItems', 'items', 'propertyNames', 'x-maxUtf8Bytes'}


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def nodes(v):
    if isinstance(v, dict):
        yield v
        for key, x in v.items():
            if key in ('properties', '$defs'):
                for y in x.values():
                    yield from nodes(y)
            elif key == 'oneOf':
                for y in x:
                    yield from nodes(y)
            elif key in ('items', 'propertyNames', 'additionalProperties') and isinstance(x, dict):
                yield from nodes(x)


parent_raw, copy_raw = (A / PARENT).read_bytes(), (A / COPY).read_bytes()
parent, child = json.loads(parent_raw), json.loads(copy_raw)
keywords = sorted(set().union(*(set(n) for n in nodes(child))))
assert set(keywords) <= GENERATOR_KEYWORDS, set(keywords) - GENERATOR_KEYWORDS
vp, vc = Draft202012Validator(parent), Draft202012Validator(child)
fixture_raw = subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, FIXTURE)], check=True,
                             capture_output=True).stdout
cases = parent_fixture = flips = 0
mismatches, changed, bases = [], [], {}
for line in fixture_raw.decode('utf-8').splitlines():
    q = json.loads(line)
    cases += 1
    p, c = vp.is_valid(q['value']), vc.is_valid(q['value'])
    if p != q['valid']:
        mismatches.append(q['label'])
    if p != c:
        changed.append(q['label'])
    if q['valid'] and '/' not in q['label']:
        bases[q['label']] = q['value']
assert not mismatches and not changed and len(bases) == 5, (mismatches[:5], changed[:5], sorted(bases))


def variant(base, role, commands):
    v = copy.deepcopy(base)
    v['role'] = role
    if role != 'analyzer':
        v['capabilities'], v['permissions'] = [], []
    if commands == 'absent':
        v.pop('commands', None)
    elif commands == 'empty':
        v['commands'] = []
    elif commands == 'null':
        v['commands'] = None
    else:
        assert commands == 'tree' and base['commands']
    return v


EXPECT = {('analyzer', 'tree'): (True, True), ('analyzer', 'absent'): (False, False),
          ('analyzer', 'empty'): (False, False), ('analyzer', 'null'): (False, False)}
for role in CLOSURE_ONLY:
    EXPECT.update({(role, 'absent'): (False, True), (role, 'tree'): (False, False),
                   (role, 'empty'): (False, False), (role, 'null'): (False, False)})
variants = []
for label in sorted(bases):
    for role in ['analyzer'] + CLOSURE_ONLY:
        for commands in ('absent', 'tree', 'empty', 'null'):
            v = variant(bases[label], role, commands)
            got = (vp.is_valid(v), vc.is_valid(v))
            assert got == EXPECT[(role, commands)], (label, role, commands, got)
            variants.append({'base': label, 'role': role, 'commands': commands,
                             'parentValid': got[0], 'copyValid': got[1]})
report = {
    'schemaVersion': 1,
    'standing': 'CR-1 r2 schema audit, by an engine independent of the product generator (jsonschema'
                ' Draft202012Validator). The parent reproduces every product shape-fixture verdict; the copy changes'
                ' none of them; on the five valid base manifests, analyzer still needs a non-empty command tree and'
                ' each closure-only role admits only with commands absent; the copy stays inside the generator keyword'
                ' set.',
    'engine': {'package': 'jsonschema', 'version': version('jsonschema'), 'validator': 'Draft202012Validator'},
    'productRev': REV,
    'parent': pin(PARENT, parent_raw),
    'copy': pin(COPY, copy_raw),
    'copyKeywords': keywords,
    'shapeFixture': {'file': pin(FIXTURE, fixture_raw), 'cases': cases, 'parentDisagreesWithFixture': 0,
                     'copyDisagreesWithParent': 0, 'validBases': sorted(bases)},
    'roleVariants': {'count': len(variants), 'expected': 'analyzer: valid only with its tree; closure-only roles:'
                     ' invalid under the parent, valid under the copy only with commands absent',
                     'cases': variants},
}
text = json.dumps(report, indent=2) + '\n'
if WRITE:
    OUT.write_text(text)
    print(json.dumps({'written': str(OUT), 'cases': cases, 'variants': len(variants)}))
else:
    same = OUT.exists() and OUT.read_text() == text
    print(json.dumps({'check': 'identical' if same else 'DIFFERS', 'cases': cases, 'variants': len(variants)}))
    sys.exit(0 if same else 1)
