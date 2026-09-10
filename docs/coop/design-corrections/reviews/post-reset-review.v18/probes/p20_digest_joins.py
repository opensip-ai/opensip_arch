"""p20: verify every declared {path, sha256} join inside the v18 governance records resolves
to the actual frozen bytes. Distinguishes review-file digests from subject-manifest digests
and from historical as-of references."""
import hashlib, json, os

F = '/tmp/opensip-design-corrections/candidate-subject.v18'
DOCS = [
    'docs/coop/design-corrections/post-reset-dispositions.v18.proposed.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/successor-source-assessment.v18.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/advisory-application-account.v18.proposed.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/review-assessment.v17.json',
    'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-source-account.v18.json',
    'docs/coop/design-corrections/reviews/v18-checker-coauthor.v1/handoff.json',
    'docs/coop/design-corrections/historical-preservation-report.v18.json',
]
MANIFESTS = {'8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c': 'candidate-subject.v17.json',
             'cd6e828c22c6bc0ecf07ab8fe1f4bd5d1a5a8726708e0deffac99960bdc25a44': 'candidate-subject.v18.json'}
cache = {}


def sha_of(rel):
    if rel not in cache:
        p = os.path.join(F, rel)
        cache[rel] = hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.isfile(p) else None
    return cache[rel]


def joins(obj, path=''):
    if isinstance(obj, dict):
        p = obj.get('path')
        s = obj.get('sha256')
        if isinstance(p, str) and isinstance(s, str):
            yield path, p, s
        for k, v in obj.items():
            yield from joins(v, path + '.' + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from joins(v, path + '[%d]' % i)


tot = ok = manifest = missing = 0
bad = []
for d in DOCS:
    doc = json.load(open(os.path.join(F, d)))
    n = o = 0
    for jp, p, s in joins(doc):
        tot += 1
        n += 1
        if s in MANIFESTS:
            manifest += 1
            o += 1
            continue  # subject-manifest digest, not a snapshot file digest
        rel = p if p.startswith('docs/') else os.path.join('docs/coop/design-corrections', p)
        a = sha_of(rel)
        if a is None:
            missing += 1
            bad.append((d, jp, p, 'FILE-NOT-IN-SNAPSHOT'))
        elif a == s:
            ok += 1
            o += 1
        else:
            bad.append((d, jp, p, 'DIGEST-MISMATCH decl=%s actual=%s' % (s[:16], a[:16])))
    print('%-72s joins=%-3d resolved=%d' % (d.split('design-corrections/')[1], n, o))

print('\ntotalJoins=%d resolvedToActualBytes=%d subjectManifestDigests=%d fileNotInSnapshot=%d mismatched=%d'
      % (tot, ok, manifest, missing, len(bad) - missing))
for b in bad:
    print('  ISSUE', b[0].split('/')[-1], b[1], b[2], '|', b[3])
