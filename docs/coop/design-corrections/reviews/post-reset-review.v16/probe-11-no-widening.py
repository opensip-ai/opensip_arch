#!/usr/bin/env python3
"""Probe 11 (independent): confirm NO unintended grammar / authority / admission
widening across the exact v15 -> v16 source delta, and that the retained
before-images really are the frozen v15 bytes.

Method:
  1. Verify each retained before-image against the FROZEN v15 manifest digest.
     (The before-images are the candidate's own claim; the v15 manifest is the
     independent authority.)
  2. For the four changed JSON schema/registry documents, diff every structural
     constraint that can widen admission: enum / const members, pattern, required,
     additionalProperties, min/max bounds, $ref targets, and registry membership.
     `description` text is EXCLUDED from the widening test and reported separately,
     because prose is exactly what these corrections were meant to change.
  3. For the two changed Python models, diff every executable line (comments and
     docstrings excluded) so a behavioural change cannot hide behind a prose diff.
"""
import ast, difflib, hashlib, json, os, sys

OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
NEW = '/tmp/opensip-design-corrections/post-reset-review.v16/copy-B-probes'
BEFORE = os.path.join(NEW, 'docs/coop/design-corrections/reviews/'
                           'bv5-corrections-author.v2/before-images/frozen-v15')
V15_MANIFEST = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/'
                'reviews/candidate-subject.v15.json')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

v15 = {r['path']: r['sha256'] for r in json.load(open(V15_MANIFEST))['files']}

FILES = [
    'docs/coop/design-corrections/foundation/identity-model.py',
    'docs/coop/design-corrections/foundation/identity-schemas.v2.json',
    'docs/coop/design-corrections/native/capability-manifest-domains.v2.json',
    'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
    'docs/coop/design-corrections/native/native_evidence_model.v2.py',
    'docs/coop/design-corrections/workflows/schemas/repair.schema.json',
    'docs/coop/design-corrections/workflows/workflow-cases.v1.json',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/v2/contracts/product-v1/identity-and-evidence.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
]

# ---- 1. before-images are the frozen v15 bytes -------------------------------
custody = []
for f in FILES:
    b = os.path.join(BEFORE, f)
    ok = os.path.isfile(b)
    got = sha256(b) if ok else None
    custody.append({'path': f, 'beforeImagePresent': ok, 'beforeImageSha256': got,
                    'frozenV15Sha256': v15.get(f),
                    'beforeImageIsFrozenV15': got == v15.get(f),
                    'currentV16Sha256': sha256(os.path.join(NEW, f))})

# ---- 2. structural (non-prose) constraint diff for JSON documents -----------
CONSTRAINT_KEYS = {'enum', 'const', 'pattern', 'required', 'additionalProperties', 'type',
                   'minLength', 'maxLength', 'minItems', 'maxItems', 'minimum', 'maximum',
                   'uniqueItems', '$ref', 'items', 'properties', 'oneOf', 'anyOf', 'allOf',
                   'not', 'propertyNames', 'patternProperties', 'x-opensip-order',
                   'x-opensip-digest'}
PROSE_KEYS = {'description', 'title', 'standing', 'note', 'source', 'rule', 'order',
              'purpose', 'comment', '$comment'}

def strip_prose(o):
    """Keep everything that can affect admission; drop free prose."""
    if isinstance(o, dict):
        return {k: strip_prose(v) for k, v in sorted(o.items())
                if k not in PROSE_KEYS and not (isinstance(v, str) and k.startswith('why'))
                and not k.endswith('Note') and not k.startswith('what')
                and not k.startswith('inherited') and not k.startswith('accounted')}
    if isinstance(o, list):
        return [strip_prose(v) for v in o]
    return o

json_reports = []
for f in FILES:
    if not f.endswith('.json'):
        continue
    a = json.load(open(os.path.join(BEFORE, f)))
    b = json.load(open(os.path.join(NEW, f)))
    sa = json.dumps(strip_prose(a), indent=1, sort_keys=True).splitlines()
    sb = json.dumps(strip_prose(b), indent=1, sort_keys=True).splitlines()
    diff = [l for l in difflib.unified_diff(sa, sb, lineterm='', n=2)]
    added = [l for l in diff if l.startswith('+') and not l.startswith('+++')]
    removed = [l for l in diff if l.startswith('-') and not l.startswith('---')]
    # prose-only change?
    prose_only = (sa == sb)
    json_reports.append({'path': f, 'structuralChangeCount': len(added) + len(removed),
                         'proseOnlyChange': prose_only,
                         'structuralAdded': added[:80], 'structuralRemoved': removed[:80],
                         'wholeDocChanged': sha256(os.path.join(BEFORE, f)) != sha256(os.path.join(NEW, f))})

# ---- 3. executable-line diff for Python models ------------------------------
def code_only(path):
    """Source with docstrings and comments removed, normalised by ast.unparse."""
    tree = ast.parse(open(path, encoding='utf-8').read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree).splitlines()

py_reports = []
for f in FILES:
    if not f.endswith('.py'):
        continue
    a, b = code_only(os.path.join(BEFORE, f)), code_only(os.path.join(NEW, f))
    diff = list(difflib.unified_diff(a, b, lineterm='', n=3))
    added = [l for l in diff if l.startswith('+') and not l.startswith('+++')]
    removed = [l for l in diff if l.startswith('-') and not l.startswith('---')]
    py_reports.append({'path': f, 'executableLinesBefore': len(a), 'executableLinesAfter': len(b),
                       'executableLinesAdded': len(added), 'executableLinesRemoved': len(removed),
                       'behaviouralChange': bool(added or removed),
                       'added': added, 'removed': removed})

# ---- 4. registry membership: nothing may gain a member ----------------------
def registries(path):
    d = json.load(open(path))
    out = {}
    for name, reg in d.get('registries', {}).items():
        if isinstance(reg, dict):
            if isinstance(reg.get('members'), list):
                out[name + '.members'] = sorted(reg['members'])
            if isinstance(reg.get('ladders'), dict):
                for k, v in reg['ladders'].items():
                    out[name + '.ladders.' + k] = list(v)
    return out
cap = 'docs/coop/design-corrections/native/capability-manifest-domains.v2.json'
ra, rb = registries(os.path.join(BEFORE, cap)), registries(os.path.join(NEW, cap))
reg_delta = {'onlyInV15': sorted(set(ra) - set(rb)), 'onlyInV16': sorted(set(rb) - set(ra)),
             'changed': {k: {'v15': ra[k], 'v16': rb[k]} for k in set(ra) & set(rb) if ra[k] != rb[k]}}

# ---- 5. digest-preimage honesty --------------------------------------------
# Prose/description edits DO change the document sha256, and those digests are
# consumed as identity preimages / pinned sources. Record that truthfully.
digest_moves = [{'path': c['path'], 'v15Sha256': c['frozenV15Sha256'],
                 'v16Sha256': c['currentV16Sha256'],
                 'documentDigestChanged': c['frozenV15Sha256'] != c['currentV16Sha256']}
                for c in custody]

res = {
    'probe': 'probe-11-no-widening',
    'copyName': 'copy-B-probes',
    'beforeImageCustody': custody,
    'allBeforeImagesAreFrozenV15': all(c['beforeImageIsFrozenV15'] for c in custody),
    'jsonStructuralReports': json_reports,
    'jsonDocumentsWithNoStructuralChange': [r['path'] for r in json_reports if r['proseOnlyChange']],
    'jsonDocumentsWithStructuralChange': [r['path'] for r in json_reports if not r['proseOnlyChange']],
    'pythonReports': py_reports,
    'registryMembershipDelta': reg_delta,
    'documentDigestMoves': digest_moves,
    'documentDigestsThatMoved': sum(1 for d in digest_moves if d['documentDigestChanged']),
    'honestyNote': 'Every one of these eleven documents changed bytes, so every document digest '
                   'derived from them moved. These are TRUTHFUL source-bound digest changes; they '
                   'are NOT identical exact semantic inputs and must not be described as such.',
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'probe-11-no-widening.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in res.items()
                  if k not in ('jsonStructuralReports', 'pythonReports', 'beforeImageCustody')},
                 indent=2, sort_keys=True))
print('\n--- json structural ---')
for r in json_reports:
    print(r['path'], 'proseOnly=', r['proseOnlyChange'], 'structuralDiffLines=', r['structuralChangeCount'])
    for l in (r['structuralAdded'] + r['structuralRemoved'])[:30]:
        print('   ', l)
print('\n--- python executable ---')
for r in py_reports:
    print(r['path'], '+%d/-%d' % (r['executableLinesAdded'], r['executableLinesRemoved']))
