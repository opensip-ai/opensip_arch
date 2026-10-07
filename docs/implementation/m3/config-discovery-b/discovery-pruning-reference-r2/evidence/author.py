from pathlib import Path
import hashlib,json
b=Path('/tmp/opensip-implementation/discovery-pruning-reference-authoring');a=Path('/Users/sb/code/opensip-ai/opensip_arch');source=a/'docs/coop/design-corrections/discovery-defaults.py';raw=source.read_bytes();s=raw.decode();(b/'discovery-defaults.original.py').write_bytes(raw)
old='''    roots = set()
    for mp in marker_relpaths:
        if mp.rpartition('/')[2] == CARGO_MARKER and _segment_prune(mp) is None:
            roots.add(_dir_of(mp))
    return roots
'''
new='''    roots = set()
    # Parents precede descendants: a marker in an already pruned Cargo
    # target tree cannot establish a second Cargo root.
    for mp in sorted(marker_relpaths, key=lambda p: (p.count('/'), p.encode('utf-8'))):
        if mp.rpartition('/')[2] == CARGO_MARKER and classify_path(mp, roots) is None:
            roots.add(_dir_of(mp))
    return roots
'''
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace('dependency or VCS tree. A `Cargo.toml` under `node_modules/` never makes a Cargo root.', 'pruned tree. A `Cargo.toml` under `node_modules/` never makes a Cargo root.')
old2='''    hit = _segment_prune(relpath)
    if hit is not None:
        return hit
    parts = relpath.split('/')
    cargo = set(cargo_roots)
    for i, seg in enumerate(parts):
        if seg == CARGO_BUILD_OUTPUT_SEGMENT and '/'.join(parts[:i]) in cargo:
            return '/'.join(parts[:i + 1]), 'cargo-build-output'
    return None
'''
new2='''    hit = _segment_prune(relpath)
    parts = relpath.split('/')
    cargo = set(cargo_roots)
    for i, seg in enumerate(parts):
        if seg == CARGO_BUILD_OUTPUT_SEGMENT and '/'.join(parts[:i]) in cargo:
            target = '/'.join(parts[:i + 1]), 'cargo-build-output'
            # The outermost anchor wins across all reasons, not merely
            # within the dependency/VCS subset.
            if hit is None or i < hit[0].count('/'):
                return target
            break
    return hit
'''
assert s.count(old2)==1;s=s.replace(old2,new2);(b/'discovery-defaults.pruning-r1.py').write_text(s)
(b/'authority.json').write_text(json.dumps(dict(original=dict(path=str(source.relative_to(a)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),scope='Prospective reference-only correction against normative NE U-4a; no B2-a/product authoring or L effect',edits=2,qualification=False),indent=2)+'\n')
(b/'authority-notes.md').write_text('''Reference-only correction. Normative NE U-4a explicitly outranks DD when they disagree and requires outermost pruned segment and no marker inside any pruned tree becoming a Cargo root. Two algorithm sites fixed: choose earliest Cargo versus dependency/VCS anchor, and derive Cargo roots parent-first through that full classification. Original reference stays untouched. Version2 record algorithms, other normalizers/classifiers and schema shapes remain unchanged. No selected V3/SX1 materialization or boundary authentication claim, no B2-a start/integration/inventory while L in-effect gate pending. Python-only bounded synthetic/reference controls, no repository code/compiler/provider/native acquisition/private413/real installation. Admitted parent is NE itself plus selected inventory context; original DD is evidence, not asserted accepted parent.\n''')
print(json.dumps(dict(originalBytes=len(raw),originalSha256=hashlib.sha256(raw).hexdigest(),candidateBytes=len(s.encode()))))
