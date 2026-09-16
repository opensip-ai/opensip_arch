"""Exact before/after hashes and proposed-edits.diff of the coauthor tree against the immutable input overlay.

Before bytes are read from the reviewer's overlay copy and verified against the overlay manifest (overlay rows) or the
frozen37 manifest (all other rows). Proves that exactly the proposed files differ in the whole 12,900-file tree and that
the pristine baseline copy still equals the input. Writes proposed-edits.diff and receipts/edit-hashes.json.
"""
import difflib, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v2'
REVIEW = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
OVERLAY = REVIEW + '/work/source37-overlay'
MAN37 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
OVM = REVIEW + '/subject-manifest.json'
SUCC = '/tmp/opensip-design-corrections/termination-exclusivity-successor.v1/source'
AFTER = RT + '/work/source37-coauthor'
PRISTINE = RT + '/work/source37-pristine'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x


assert sha(MAN37) == '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
assert sha(OVM) == 'db9b7b3f3fbec833229fbd6e0c37cdc7bfed35ffabf3b6baabf709d35b380e52'
expect = {r['path']: r['sha256'] for r in rows(json.load(open(MAN37)))}
ovrows = {f['path']: f for f in json.load(open(OVM))['files']}
for p, f in ovrows.items():
    expect[p] = f['sha256']


def walk(root):
    out = set()
    for d, ds, fs in os.walk(root):
        for f in fs:
            out.add(os.path.relpath(os.path.join(d, f), root))
    return out


after_paths = walk(AFTER)
pristine_paths = walk(PRISTINE)
changed = sorted(p for p in expect if sha(os.path.join(AFTER, p)) != expect[p])
res = {'inputOverlayManifestSha256': sha(OVM), 'parentManifestSha256': sha(MAN37),
       'afterTreeExtra': sorted(after_paths - set(expect)), 'afterTreeMissing': sorted(set(expect) - after_paths),
       'pristineTreeMismatch': sorted(p for p in expect if sha(os.path.join(PRISTINE, p)) != expect[p]),
       'pristineTreeExtra': sorted(pristine_paths - set(expect)), 'files': []}
diff_parts = []
for p in changed:
    before_path = os.path.join(OVERLAY, p)
    assert sha(before_path) == expect[p], 'input overlay bytes changed: ' + p
    b = open(before_path, 'rb').read()
    a = open(os.path.join(AFTER, p), 'rb').read()
    sp = os.path.join(SUCC, p)
    ud = list(difflib.unified_diff(b.decode('utf-8').splitlines(keepends=True), a.decode('utf-8').splitlines(keepends=True),
                                   fromfile='a/' + p, tofile='b/' + p, n=3))
    diff_parts.append(''.join(ud) if ud and ud[-1].endswith('\n') else ''.join(ud) + '\n')
    res['files'].append({'path': p, 'overlayRow': p in ovrows, 'beforeSha256': expect[p], 'beforeBytes': len(b),
                         'afterSha256': hashlib.sha256(a).hexdigest(), 'afterBytes': len(a),
                         'added': sum(1 for l in ud if l.startswith('+') and not l.startswith('+++')),
                         'removed': sum(1 for l in ud if l.startswith('-') and not l.startswith('---')),
                         'rootSuccessorSha256': sha(sp) if os.path.isfile(sp) else None,
                         'rootSuccessorEqualsBefore': os.path.isfile(sp) and sha(sp) == expect[p]})
text = ''.join(diff_parts)
open(RT + '/proposed-edits.diff', 'w').write(text)
res['proposedEditsDiffSha256'] = hashlib.sha256(text.encode()).hexdigest()
res['proposedEditsDiffBytes'] = len(text.encode())
json.dump(res, open(RT + '/receipts/edit-hashes.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
