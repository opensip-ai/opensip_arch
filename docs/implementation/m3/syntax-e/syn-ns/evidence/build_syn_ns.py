"""Build contract successor SYN-NS (law M3-E1 r3, item 19: the normalizer specification) deterministically.

Writes, under docs/implementation/m3/syntax-e/:
  syn-ns/closure/opensip-interface/grammar/normalizer.v1.json            (the native normalizer specification)
  syn-ns/closure/opensip-interface/normalization/levels/<level>.v1.json  (the four level specifications)
  syn-ns/closure/opensip-interface/normalization/specification-map.v1.json (IE's normalization map)
  syn-ns/readable/*.json        (the same documents pretty-printed; not normative, for review only)
  syn-ns/materialization-map.json, syn-ns/successor.json and syn-ns-subject.json;
  and, outside the subject, the lead's draft unit record syn-ns-unit.json (review path codex2-syn-ns-r2).

The closure members are canonical bytes under foundation/canonical.py's rule (sorted keys, no insignificant
whitespace, UTF-8, exact JSON types, depth at most 32), which `canonical` below restates; check_syn_ns.py
re-encodes every member with the real design encoder. The documents themselves are spec_syn_ns.py's data.
No candidate is a copy of an accepted file and no passage is overridden: SYN-NS adds new design files only.

Usage: python3.14 -I -B evidence/build_syn_ns.py [--product /path/to/opensip] [--check]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
sys.path.insert(0, str(HERE))
import spec_syn_ns as S  # noqa: E402

BASE = 'docs/implementation/m3/syntax-e'
UNIT = f'{BASE}/syn-ns'
BASE_REV = '218465f'   # product main with SYN-1 and SYN-1F bound (91 contract successors)
CLOSURE = f'{UNIT}/closure'
NORMALIZER_PATH = 'opensip-interface/grammar/normalizer.v1.json'
MAP_PATH = 'opensip-interface/normalization/specification-map.v1.json'
LEVEL_PATH = 'opensip-interface/normalization/levels/{}.v1.json'
PARENTS = [
    'docs/v2/contracts/product-v1/native-evidence.md',            # section 6 (bodies, levels, parameters, near)
    'docs/v2/contracts/product-v1/identity-and-evidence.md',      # section 3 (body identity, the normalization map)
    'docs/coop/artifacts/fact-identity-policy.v2.json',           # the inherited byte grammar and ladder
    # normalization-specification-map, in the selected identity copy (SYN-1F, bound at 218465f)
    'docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json',
    'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json',  # declares, literal, control-flow
]
STATIC = ['README.md', 'evidence/build_syn_ns.py', 'evidence/spec_syn_ns.py', 'evidence/check_syn_ns.py',
          'evidence/verify_scratch.py', 'evidence/kinds-report.json', 'evidence/reference_syn_ns.py',
          'evidence/fixtures.json']
REVIEW = 'docs/implementation/m3/reviews/codex2-syn-ns-r2/review.json'
STANDING = (
    'PROPOSED SYN-NS normalizer specification r2 (law M3-E1 r3, item 19, SYN-NS; items 13 and 14; answers CODEX2\'s '
    'r1 RF-SYNNS-1 to -6 and NB-SYNNS-1 and -2 under the rule that no transform is applied where the pinned grammar '
    'cannot prove it preserves the meaning): the identity-bearing '
    'normalization bytes of the syntax universe\'s grammar closure, as new design files at their closure tree paths. '
    'opensip-interface/grammar/normalizer.v1.json (the native normalizer: bodies and import-only exclusion, syntax '
    'subject identities, the declares, literal and intra-body control-flow tables, near-v1, and the section 6.2 '
    'parameters, per code grammar row); the four level specifications at '
    'opensip-interface/normalization/levels/<level>.v1.json, each complete for its level (the token law and '
    'token-kind registry, the comment and directive law, and the local-renaming law); and IE\'s normalization map '
    'at opensip-interface/normalization/specification-map.v1.json, whose rows name the level files by digest. Every '
    'node kind and field is checked against the pinned grammars of the E0 report, and hand-written fixtures run '
    'through a reference oracle. Written for native-linked-v1 and '
    'branch-neutral: both execution models carry the same bytes. No passage override, no copy of an accepted file. '
    'E2a places the bytes in the closure; E2c implements them. Exact frozen candidate requires actual independent '
    'review and root assent.')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}


def read(path):
    return (ARCH / path).read_bytes()


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def typed(value, depth=0):
    """foundation/canonical.py's typed(): exact JSON types, depth below 32."""
    if type(value) in (dict, list) and depth >= 32:
        raise SystemExit('DEPTH_LIMIT')
    if value is None or type(value) in (bool, str):
        return
    if type(value) is int:
        assert -(2 ** 63) <= value <= 2 ** 64 - 1
        return
    if type(value) is list:
        for child in value:
            typed(child, depth + 1)
        return
    if type(value) is dict:
        for key, child in value.items():
            assert type(key) is str
            typed(child, depth + 1)
        return
    raise SystemExit('EXACT_JSON_TYPE_REQUIRED')


def canonical(value):
    typed(value)
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
    assert len(raw) <= 4 * 1024 * 1024
    return raw


def git_show(product, rev, path):
    return subprocess.run(['git', '-C', str(product), 'show', f'{rev}:{path}'], check=True,
                          capture_output=True).stdout


def accepted_set(product):
    lock = json.loads(git_show(product, BASE_REV, 'design-lock.json'))
    accepted = {}
    for name in ('sourceManifest', 'applicationManifest'):
        for row in json.loads(read(lock['approvals'][name]['path']))['files']:
            accepted[row['path']] = row
    for binding in lock['inventorySuccessors']:
        accepted[binding['parent']['path']] = binding['parent']
        accepted[binding['candidate']['path']] = binding['candidate']
    for binding in lock['contractSuccessors']:
        accepted[binding['record']['path']] = binding['record']
        for row in json.loads(read(binding['record']['path']))['candidates']:
            accepted[row['path']] = row
    return lock, accepted


def build(product):
    lock, accepted = accepted_set(product)
    files = {}
    levels = {}
    for level in S.LEVELS:
        raw = canonical(S.level_doc(level))
        levels[level] = raw
        files[f'{CLOSURE}/{LEVEL_PATH.format(level)}'] = raw
    spec_map = {'schemaVersion': 1, 'normalizerId': S.NORMALIZER_ID,
                'levels': [{'level': level, 'specificationDigest': sha(levels[level])} for level in S.LEVELS]}
    assert [r['level'].encode() for r in spec_map['levels']] == sorted(r['level'].encode() for r in spec_map['levels'])
    files[f'{CLOSURE}/{MAP_PATH}'] = canonical(spec_map)
    files[f'{CLOSURE}/{NORMALIZER_PATH}'] = canonical(S.normalizer_doc())
    bounds = {NORMALIZER_PATH: 4 << 20, MAP_PATH: 1 << 20}
    tree = []
    for path in sorted(p for p in files if p.startswith(CLOSURE + '/')):
        tree_path = path[len(CLOSURE) + 1:]
        assert len(files[path]) <= bounds.get(tree_path, 4 << 20), tree_path
        tree.append({'treePath': tree_path, 'candidatePath': path, 'bytes': len(files[path]),
                     'sha256': sha(files[path])})
        files[f'{UNIT}/readable/{tree_path.split("/")[-1]}'] = dumps(json.loads(files[path]))
    files[f'{UNIT}/materialization-map.json'] = dumps({
        'schemaVersion': 1,
        'standing': ('Exact closure member bytes for the grammar closure lane (unit E2a, SYN-LANE): each candidate is '
                     'placed at its tree path in the kind=grammar closure, unchanged. The bundle manifest\'s '
                     'normalizer is {normalizerId, normalizerVersion, specificationPath, specificationDigest} = '
                     '{opensip.syntax.normalizer, 1, opensip-interface/grammar/normalizer.v1.json, the sha256 below}; '
                     'the map is the tree\'s second root (law M3-E1 item 4, A6). Both execution models carry the same '
                     'bytes. Independent review and root assent are required before selection.'),
        'baseProductRev': BASE_REV,
        'normalizer': {'normalizerId': S.NORMALIZER_ID, 'normalizerVersion': S.NORMALIZER_VERSION,
                       'specificationPath': NORMALIZER_PATH,
                       'specificationDigest': sha(files[f'{CLOSURE}/{NORMALIZER_PATH}'])},
        'tree': tree,
    })
    for name in STATIC:
        files[f'{UNIT}/{name}'] = read(f'{UNIT}/{name}')
    for path in PARENTS:
        row = accepted.get(path)
        assert row and row['sha256'] == sha(read(path)) and row['bytes'] == len(read(path)), path
    record = {'schemaVersion': 1, 'standing': STANDING, 'parents': [pin(p, read(p)) for p in sorted(PARENTS)],
              'passageOverrides': [], 'candidates': [pin(p, files[p]) for p in sorted(files)]}
    files[f'{UNIT}/successor.json'] = dumps(record)
    subject = {'schemaVersion': 1, 'files': [pin(p, files[p]) for p in sorted(files)]}
    files[f'{BASE}/syn-ns-subject.json'] = dumps(subject)
    paths = [r['path'] for r in subject['files']]
    assert paths == sorted(set(paths))
    for p in paths:
        assert p not in accepted, f'candidate reuses an accepted path: {p}'
    assert all(b['record']['path'] != f'{UNIT}/successor.json' for b in lock['contractSuccessors'])
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = build(args.product.resolve())
    generated = [p for p in files if p.startswith(UNIT + '/') and not p.endswith(('README.md', '.py'))
                 and not p.endswith(('kinds-report.json', 'fixtures.json'))]
    generated.append(f'{BASE}/syn-ns-subject.json')
    for path in sorted(set(generated)):
        target = ARCH / path
        if args.check:
            if target.read_bytes() != files[path]:
                raise SystemExit(f'differs: {path}')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(files[path])
    record = json.loads(files[f'{UNIT}/successor.json'])
    unit = {'schemaVersion': 1, 'unit': 'syntax-e-syn-ns', 'status': 'DRAFT-PENDING-REVIEW',
            'subjectManifest': pin(f'{BASE}/syn-ns-subject.json', files[f'{BASE}/syn-ns-subject.json']),
            'independentReview': {'path': REVIEW, 'bytes': None, 'sha256': None},
            'rootSubstantiveAssent': False, 'requiredUnitFindings': [],
            'acceptedSuccessor': pin(f'{UNIT}/successor.json', files[f'{UNIT}/successor.json']),
            'rootAssessment': ('DRAFT (r2). Completed by the lead after CODEX2\'s r2 review: status ACCEPTED-DESIGN-UNIT, '
                               'the review pin, rootSubstantiveAssent true. SYN-NS is law M3-E1 r3\'s normalizer '
                               'specification: six canonical closure members (normalizer.v1.json; the L0 to L3 level '
                               'specifications, each self-contained; IE\'s normalization map). r2 answers RF-SYNNS-1 to '
                               '-6: JavaScript-family line terminators kept as line-break tokens; Rust bindings only by '
                               'explicit binding forms; macro token trees atomic and macro or attribute bodies not '
                               'renamed; an explicit flow-node traversal; do...while entered at its body; control-flow '
                               'identities under the owner\'s full subject. No passage override and no copy; it binds on '
                               'product ' + BASE_REV + ' (91 to 92).'),
            'fullM2Complete': False, 'productQualification': False}
    unit_raw = dumps(unit)
    unit_path = ARCH / f'{BASE}/syn-ns-unit.json'
    if args.check:
        if unit_path.read_bytes() != unit_raw:
            raise SystemExit('differs: syn-ns-unit.json')
    else:
        unit_path.write_bytes(unit_raw)
    print(json.dumps({'subject': pin(f'{BASE}/syn-ns-subject.json', files[f'{BASE}/syn-ns-subject.json']),
                      'successor': pin(f'{UNIT}/successor.json', files[f'{UNIT}/successor.json']),
                      'candidates': len(record['candidates']),
                      'closure': {p[len(CLOSURE) + 1:]: pin(p, files[p])['sha256'] for p in sorted(files)
                                  if p.startswith(CLOSURE + '/')},
                      'checked': args.check}, indent=1))


if __name__ == '__main__':
    main()
