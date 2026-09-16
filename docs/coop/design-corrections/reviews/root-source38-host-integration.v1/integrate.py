from pathlib import Path
import json, hashlib, difflib, shutil
BASE = Path('/tmp/opensip-design-corrections')
REPO = Path('/Users/sb/code/opensip-ai/opensip_arch')
SOURCE = BASE / 'termination-exclusivity-successor.v1/source'
AUTHOR = BASE / 'claude-source37-host-finalizer-author.v2'
FROZEN = BASE / 'candidate-subject.v37'
OUT = BASE / 'root-source38-host-integration.v1'
assert not OUT.exists()
sha = lambda raw: hashlib.sha256(raw).hexdigest()
manifest = json.loads((AUTHOR / 'after-manifest.json').read_bytes())
assert len(manifest['files']) == 8
prepared = []
for row in manifest['files']:
    rel = row['path']
    raw = (AUTHOR / 'source' / rel).read_bytes()
    assert sha(raw) == row['sha256'] and len(raw) == row['bytes']
    target = SOURCE / rel
    before = target.read_bytes() if target.exists() else None
    frozen = (FROZEN / rel).read_bytes() if (FROZEN / rel).exists() else None
    assert (sha(frozen) if frozen is not None else None) == row['frozen37Sha256']
    merge = False
    if rel == 'docs/v2/contracts/product-v1/workflows-and-surfaces.md':
        assert sha(before) == 'b71cdd6ee978fe3badae91a197fb663e4c7842413e6d827c97257624e7daeb2c'
        baseline = frozen.decode().splitlines(True)
        authored = raw.decode().splitlines(True)
        changes = [op for op in difflib.SequenceMatcher(None, baseline, authored, autojunk=False).get_opcodes() if op[0] != 'equal']
        assert len(changes) == 1
        kind, i, j, k, l = changes[0]
        assert kind == 'insert' and i == j and l - k == 13
        insertion = ''.join(authored[k:l])
        anchor = ''.join(baseline[i:i+3])
        current = before.decode()
        assert current.count(anchor) == 1 and insertion not in current
        merged = current.replace(anchor, insertion + anchor, 1)
        assert merged.replace(insertion, '', 1) == current
        raw = merged.encode()
        merge = True
    else:
        assert before == frozen, 'Unexpected root change: ' + rel
    prepared.append((rel, before, raw, row['sha256'], merge))
OUT.mkdir()
rows = []
for rel, before, raw, authored_sha, merge in prepared:
    if before is not None:
        saved = OUT / 'before' / rel
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(before)
    target = SOURCE / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    after = OUT / 'after' / rel
    after.parent.mkdir(parents=True, exist_ok=True)
    after.write_bytes(raw)
    diff = ''.join(difflib.unified_diff((before or b'').decode().splitlines(True), raw.decode().splitlines(True), fromfile='before/' + rel, tofile='after/' + rel))
    patch = OUT / 'diffs' / (rel + '.diff')
    patch.parent.mkdir(parents=True, exist_ok=True)
    patch.write_text(diff)
    rows.append({'path': rel, 'beforeSha256': sha(before) if before is not None else None, 'afterSha256': sha(raw), 'authorAfterSha256': authored_sha, 'mergedWithRootR1R2': merge})
report = {'standing': 'Root assessed and integrated exact completed actual Claude host-finalizer v2 proposal into mutable successor. Not independent source acceptance or readiness. Global checks/pins/freeze pending.', 'authorAfterManifestSha256': sha((AUTHOR / 'after-manifest.json').read_bytes()), 'authorDiffSha256': sha((AUTHOR / 'frozen37-to-final.diff').read_bytes()), 'files': rows, 'limits': ['Projection admission leaves delegated attribution/detail owner validation required', 'Closed goldens cover the documented native/work-budget combinations, not all cross-owner combinations', 'No product qualification or acceptance']}
(OUT / 'integration.json').write_text(json.dumps(report, indent=2) + '\n')
shutil.copyfile(Path(__file__), OUT / 'integrate.py')
shutil.copytree(OUT, REPO / 'docs/coop/design-corrections/reviews' / OUT.name)
print('Integrated 8 host files, including 3 additions and one exact W section9 merge; no pins/freeze')
