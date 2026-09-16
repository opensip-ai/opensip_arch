"""Apply an independently accepted documentation package; never product implementation.
The external activation receipt breaks the content/review self-hash cycle.
No edits occur until all review, frozen after-image and live before-image checks pass.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def safe_relative(value):
    p = Path(value)
    if p.is_absolute() or '..' in p.parts or not p.parts or (p.parts[0] != 'docs' and value != 'README.md'):
        raise ValueError('Application path must be a reviewed documentation path: ' + value)
    return p

def apply(root, package, manifest_path, expected_manifest_sha, review_path, expected_review_sha, check_only=False):
    root = root.resolve(); package = package.resolve()
    assert sha(manifest_path) == expected_manifest_sha, 'Application manifest drift'
    assert sha(review_path) == expected_review_sha, 'Independent application review drift'
    manifest = json.loads(manifest_path.read_text())
    review = json.loads(review_path.read_text())
    assert review['verdict'] == 'ACCEPT', 'Independent application ACCEPT required'
    assert review['subjectManifestSha256'] == expected_manifest_sha, 'Review names different application bytes'
    assert manifest['implementationAuthorized'] is False
    activation_rel = safe_relative('docs/coop/design-corrections/application-activation.v1.json')
    assert (root / activation_rel).resolve().is_relative_to(root), 'Escaping activation path'
    assert not (root / activation_rel).exists(), 'Existing activation requires verification, never replacement'
    targets = []
    for row in manifest['files']:
        rel = safe_relative(row['path']); src = package / 'files' / rel; dst = root / rel
        assert src.resolve().is_relative_to(package), 'Escaping staged path'
        assert dst.resolve().is_relative_to(root) and not dst.is_symlink(), 'Escaping live path'
        assert sha(src) == row['sha256'] and src.stat().st_size == row['bytes'], 'Staged content drift: ' + str(rel)
        before = row['beforeSha256']
        current = sha(dst) if dst.is_file() else None
        admissible = (not dst.exists() and before is None) or (dst.is_file() and current in (before, row['sha256']))
        assert admissible, 'Working-tree change since review: ' + str(rel)
        # An interrupted copy may already have installed this exact reviewed after-image.
        # Any other bytes still refuse; no activation is written until the full set matches.
        targets.append((src, dst, row))
    for rel, expected in [(manifest['retainedManifestPath'], expected_manifest_sha),
                          (manifest['retainedReviewPath'], expected_review_sha)]:
        assert sha(root / safe_relative(rel)) == expected, 'Review custody must be retained before application'
    if check_only:
        print(json.dumps({'checksPassed':True,'files':len(targets),'writes':False}))
        return
    for src, dst, row in targets:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    assert all(sha(dst) == row['sha256'] for _, dst, row in targets)
    receipt = {
        'standing': 'D-372 application activation; design acceptance only',
        'applicationManifest': {'path': manifest['retainedManifestPath'], 'sha256': expected_manifest_sha},
        'independentApplicationReview': {'path': manifest['retainedReviewPath'], 'sha256': expected_review_sha, 'verdict': 'ACCEPT'},
        'implementationAuthorized': False,
        'qualificationClaimed': False,
        'appliedFileCount': len(targets),
        'bindingRule': 'Verify both pinned artifacts and each current applied file against the application manifest; this receipt alone is not acceptance evidence.'
    }
    (root / activation_rel).parent.mkdir(parents=True, exist_ok=True)
    (root / activation_rel).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'appliedFiles':len(targets), 'activation':str(activation_rel), 'implementationAuthorized':False}))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ('root','package','manifest','review'):
        p.add_argument('--'+name, required=True, type=Path)
    p.add_argument('--manifest-sha', required=True)
    p.add_argument('--review-sha', required=True)
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    apply(a.root, a.package, a.manifest, a.manifest_sha, a.review, a.review_sha, a.check)
