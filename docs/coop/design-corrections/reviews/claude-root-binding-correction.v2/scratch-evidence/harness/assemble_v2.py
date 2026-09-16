"""Assemble the v2 follow-up deliverable: minimal patch against completed v1, changed full
files, hashes and the evidence manifest. Writes only inside the v2 scratch output directory."""
import difflib
import hashlib
import json
import os
import shutil

V1 = '/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch/src25'
V2 = '/private/tmp/opensip-design-corrections/claude-root-binding-correction.v2/scratch'
SRC = V2 + '/src25'
OUT = V2 + '/output'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v25'

CHANGED = ['docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
           'docs/coop/design-corrections/native/native_evidence_model.v2.py']


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    for d in ['patches', 'files', 'evidence']:
        os.makedirs(os.path.join(OUT, d), exist_ok=True)

    lines = []
    for rel in CHANGED:
        a = open(os.path.join(V1, rel), encoding='utf-8').read().splitlines(keepends=True)
        b = open(os.path.join(SRC, rel), encoding='utf-8').read().splitlines(keepends=True)
        lines.extend(difflib.unified_diff(a, b, fromfile='v1/' + rel, tofile='v2/' + rel, n=3))
    patch = OUT + '/patch-10-f04-selector-segment-law-and-guard-bounds.diff'
    open(patch, 'w', encoding='utf-8').write(''.join(lines))
    print('patch lines:', len(lines), '| sha256', sha(patch))

    for rel in CHANGED:
        dst = os.path.join(OUT, 'files', rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(SRC, rel), dst)

    table = []
    for rel in CHANGED:
        table.append({'path': rel,
                      'frozen25Sha256': sha(os.path.join(FROZEN, rel)),
                      'v1Sha256': sha(os.path.join(V1, rel)),
                      'v2Sha256': sha(os.path.join(SRC, rel)),
                      'v2Bytes': os.path.getsize(os.path.join(SRC, rel))})

    ev = []
    for dp, dn, fn in os.walk(OUT):
        for f in sorted(fn):
            fp = os.path.join(dp, f)
            rel = os.path.relpath(fp, OUT)
            if rel == 'evidence-manifest-v2.json':
                continue
            ev.append({'path': rel, 'bytes': os.path.getsize(fp), 'sha256': sha(fp)})
    ev.sort(key=lambda r: r['path'])

    man = {
        'standing': 'AUTHORED v2 follow-up to the F-04 selector defect root demonstrated. '
                    'Author-assisted reference work by a reviewer acting as author; NOT '
                    'independent acceptance, NOT blind reconstruction, NOT product '
                    'implementation or readiness. frozen25, the 97-file author package and the '
                    'completed v1 scratch tree are unmodified; every write is inside this v2 '
                    'scratch directory.',
        'baseline': 'completed v1 scratch tree (unchanged)',
        'boundCandidateManifestSha256': 'fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d',
        'boundAuthorPackageManifestSha256': 'c533aa6ab8939e6ecf710d217233aea8818fd1783e770b0db5ba81e375d316c4',
        'frozen25FilesVerified': 12869,
        'author97FilesVerified': 97,
        'v1AuthoredEvidenceFilesVerifiedUnchanged': 158,
        'changedFiles': table,
        'pinRebindingPerformed': False,
        'pinRebindingNote': 'Deliberately NOT rebound here. The native schema bytes move again, '
                            'so root rebinds all six fixture/pin dependencies once when merging '
                            'this with completed discovery v2, and runs the integrated '
                            'reference/evaluator suites once at that point.',
        'authoredEvidence': ev,
        'fileCount': len(ev),
    }
    json.dump(man, open(OUT + '/evidence-manifest-v2.json', 'w'), indent=1)

    print()
    print('%-58s %-14s %-14s %-14s' % ('path', 'frozen25', 'v1', 'v2'))
    for t in table:
        print('%-58s %-14s %-14s %-14s'
              % (t['path'].replace('docs/coop/design-corrections/', 'DC/'),
                 t['frozen25Sha256'][:12], t['v1Sha256'][:12], t['v2Sha256'][:12]))
    print()
    print('evidence files:', len(ev))
    print('evidence-manifest-v2.json sha256:', sha(OUT + '/evidence-manifest-v2.json'))


if __name__ == '__main__':
    main()
