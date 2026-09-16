"""Artifact manifest for the author remint delivery, plus input re-verification."""
import hashlib
import json
import os
from pathlib import Path

R = Path('/private/tmp/opensip-design-corrections/claude-author-remint.v1')
S = R / 'scratch'
NEW_SCHEMA = '673a9bf8b3d1d0d3643d0fdd75813a6fa14d362d792e90d0ddd5f63e16a6bbe2'
INCLUDE = ['portable', 'out-a', 'evidence', 'portability-proof', 'harness', 'COMMANDS.md']
SKIP_DIRS = {'helpers-two-binding', 'helpers-two-binding-distinct', 'exports-view', '__pycache__'}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verify(manifest, root):
    m = json.loads(Path(manifest).read_bytes())
    ok = bad = miss = 0
    for e in m['files']:
        p = Path(root) / e['path']
        if not p.is_file():
            miss += 1
            continue
        if sha(p) == e['sha256']:
            ok += 1
        else:
            bad += 1
    return {'manifest': os.path.basename(manifest), 'manifestSha256': sha(manifest),
            'files': len(m['files']), 'verified': ok, 'mismatched': bad, 'missing': miss}


def main():
    files = []
    for item in INCLUDE:
        p = S / item
        if p.is_file():
            files.append({'path': item, 'bytes': p.stat().st_size, 'sha256': sha(p)})
            continue
        for dp, dn, fn in os.walk(p):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            for f in sorted(fn):
                fp = Path(dp) / f
                rel = str(fp.relative_to(S))
                files.append({'path': rel, 'bytes': fp.stat().st_size, 'sha256': sha(fp)})
    files.sort(key=lambda r: r['path'])

    claims = {}
    for group, rel in [('checkpoint3', 'out-a/a-checkpoint3/checkpoint3'),
                       ('normalized-examples6', 'out-a/b-normalized/normalized-examples6'),
                       ('rust-selection-examples1', 'out-a/c-rust-selection/rust-selection-examples1'),
                       ('semantic-controls1', 'out-a/d-controls/semantic-controls1'),
                       ('binding-controls', 'out-a/e-binding-controls')]:
        cp = S / rel / 'claims.json'
        if cp.is_file():
            claims[group] = json.loads(cp.read_text())

    man = {
        'standing': 'AUTHOR delivery: portable construction path plus a full remint of the seven '
                    'positive Runs, three reminted semantic negatives and the F-05/F-06 binding '
                    'controls on the merged native reference bytes. This is author-assisted '
                    'reference work, NOT independent reconstruction, NOT blind acceptance, NOT '
                    'application acceptance and NOT product qualification. Do not supply these '
                    'examples or oracles to a blind consumer. The original 123/8/3 charter '
                    'remains independent and pending.',
        'boundSourceManifestSha256': sha(R / 'source-manifest.json'),
        'boundPackageManifestSha256': sha(R / 'package-manifest.json'),
        'registeredNativeSchemaSha256': NEW_SCHEMA,
        'notCandidate26': 'The merged source is an intermediate root integration input, not the '
                          'final whole-design candidate. Evidence here is bound to these exact '
                          'bytes only and does not carry to future changed bytes.',
        'inputVerification': [verify(R / 'source-manifest.json', R / 'source'),
                              verify(R / 'package-manifest.json', R / 'package')],
        'claims': claims,
        'artifacts': files,
        'artifactCount': len(files),
    }
    (S / 'artifact-manifest.json').write_text(json.dumps(man, indent=1) + '\n')
    for v in man['inputVerification']:
        print('%-24s files=%-6s verified=%-6s mismatched=%s missing=%s'
              % (v['manifest'], v['files'], v['verified'], v['mismatched'], v['missing']))
    print('artifacts:', len(files))
    print('artifact-manifest.json sha256:', sha(S / 'artifact-manifest.json'))


if __name__ == '__main__':
    main()
