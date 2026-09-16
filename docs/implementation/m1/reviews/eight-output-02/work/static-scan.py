"""Review02 static scans: projection transformations and generated Rust carrier properties."""
import collections
import glob
import json
import re

W = '/tmp/opensip-implementation/m1-eight-output-review-02/work'
S = W + '/subject'
old = json.load(open('/tmp/opensip-implementation/m1-eight-output-subject-01/rust-projection.json'))['definitions']
new = json.load(open(S + '/rust-projection.json'))['definitions']
named = json.load(open(S + '/named-schemas.json'))['definitions']
targets = json.load(open(S + '/targets.json'))
out = {}


def nodes(v, path=()):
    if isinstance(v, dict):
        yield path, v
        for k, x in v.items():
            if k in ('properties', 'patternProperties', 'definitions', '$defs'):
                for n, y in x.items():
                    yield from nodes(y, path + (k, n))
            elif k in ('additionalProperties', 'propertyNames', 'items', 'not', 'contains', 'if', 'then', 'else'):
                yield from nodes(x, path + (k,))
            elif k in ('allOf', 'anyOf', 'oneOf'):
                for i, y in enumerate(x):
                    yield from nodes(y, path + (k, i))


kw_old = collections.Counter(k for n, d in old.items() for _, v in nodes(d) for k in v)
kw_new = collections.Counter(k for n, d in new.items() for _, v in nodes(d) for k in v)
out['keywordDelta'] = {k: [kw_old.get(k, 0), kw_new.get(k, 0)] for k in sorted(set(kw_old) | set(kw_new)) if kw_old.get(k, 0) != kw_new.get(k, 0)}
out['emptyNot'] = sum(1 for n, d in new.items() for _, v in nodes(d) if v.get('not') == {})
out['emptyAllOfBranch'] = sum(1 for n, d in new.items() for _, v in nodes(d) for b in v.get('allOf', []) if b == {})
out['residualContainsOrPatternOrIf'] = sum(1 for n, d in new.items() for _, v in nodes(d) for k in ('contains', 'pattern', 'if', 'then', 'else') if k in v)
exact = [('/'.join(map(str, (n,) + p))) for n, d in new.items() for p, v in nodes(d) if v == {'type': 'integer'}]
out['exactIntegerProjectionNodes'] = len(exact)
# Integer nodes in the ORIGINAL named schemas and their allowed domain vs carrier choice.
dom = collections.Counter()
typelists = []
for n, d in named.items():
    for p, v in nodes(d):
        t = v.get('type')
        ints = [x for x in ([v['const']] if 'const' in v else []) + list(v.get('enum', [])) if type(x) is int]
        if isinstance(t, list) and 'integer' in t:
            typelists.append(('/'.join(map(str, (n,) + p)), t, v.get('minimum'), v.get('maximum')))
        if t == 'integer' or ints:
            lo, hi = v.get('minimum', -(2**63)), v.get('maximum', 2**64 - 1)
            if ints:
                lo, hi = min(ints), max(ints)
            dom['fits-i64' if lo >= -(2**63) and hi <= 2**63 - 1 else 'fits-u64' if lo >= 0 else 'mixed']
            dom['fits-i64' if lo >= -(2**63) and hi <= 2**63 - 1 else 'fits-u64' if lo >= 0 else 'mixed'] += 1
out['originalIntegerDomains'] = dict(dom)
out['integerTypeLists'] = typelists
rust = {f.split('/')[-1]: open(f).read() for f in sorted(glob.glob(S + '/output-e/crates/contracts/src/generated/*.rs'))}
src = '\n'.join(rust.values())
out['rustCounts'] = {p: len(re.findall(p, src)) for p in [r'\bf64\b', r'\bf32\b', 'BTreeSet', 'HashSet', r'\bi64\b', r'\bu64\b', 'ExactInteger', 'FieldPresence<', 'deny_unknown_fields', r'serde\(untagged\)', 'NonZero', r'\bi128\b', r'pub enum \w+ \{\}']}
structs = list(re.finditer(r'pub struct (\w+) \{', src))
out['structsWithoutDenyUnknownFields'] = [m.group(1) for m in structs if 'deny_unknown_fields' not in src[max(0, m.start() - 200):m.start()]]
# i64/u64 used in untagged integer variants (the RF-2 site shape) and as direct field types
out['untaggedIntegerVariants'] = re.findall(r'(\w+)\((i64|u64|ExactInteger)\),', src)[:40]
out['identityFindingParametersValue'] = re.search(r'pub enum Identity3FindingParametersParametersValue \{[^}]*\}', src).group(0)
out['sarifMessagePropertiesValue'] = re.search(r'pub enum Sarif2ResultMessagePropertiesValue \{[^}]*\}', src).group(0)
out['exactIntegerHelperCopies'] = src.count('pub struct ExactInteger(i128);')
print(json.dumps(out, indent=1))
json.dump(out, open(W + '/logs/static-scan.json', 'w'), indent=1)
