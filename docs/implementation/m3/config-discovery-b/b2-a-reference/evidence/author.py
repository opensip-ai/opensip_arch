"""Author the B2-a reference refresh: the corrected pruning copy plus SX-1 and the V3 boundary inventory.

Reads the accepted pruning copy at its pinned bytes and writes discovery-defaults.sx1-r1.py beside this script.
Every edit is an exact, asserted replacement; nothing else in the copy changes."""
from pathlib import Path
import hashlib

HERE = Path(__file__).resolve().parent
BASE = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/config-discovery-b/discovery-pruning-reference-r2/reference/discovery-defaults.pruning-r1.py')
raw = BASE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '7817a4adba5d86d47c8197116ea2293c938cc2fa9fd24f823fc249c0472f2fc5', 'base pin'
s = raw.decode()


def rep(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


# Module docstring: one added paragraph, before the integration interface paragraph.
rep('''Interface for integration (Codex):''', '''  * OpenSIP custody state (successor SX-1, contract successor B-S1; reference refresh owed by BS1-F3): the exact
    path `.opensip` at the project root `` and at each admitted D15 member root is a pruned anchor with reason
    `opensip-custody-state`, never a segment matched at any other depth (`src/.opensip` is ordinary source). The
    outermost anchor still wins across every reason. `conventional_excluded_prefixes` always lists it (B-S1 LD-3).
    Version 3 (B-S1): the boundary inventory adds the members, which are not boundaries and add no prefix.

Interface for integration (Codex):''')
# Constants.
rep("DISCOVERY_DEFAULTS_VERSION = 2   # 2: admitted boundary inventory API (P3); interface of version 1 unchanged",
    "DISCOVERY_DEFAULTS_VERSION = 3   # 3: SX-1 anchor and V3 boundary inventory (B-S1); 2: admitted boundary inventory API (P3)")
rep("CARGO_MARKER = 'Cargo.toml'\n", "CARGO_MARKER = 'Cargo.toml'\nOPENSIP_CUSTODY_STATE = '.opensip'\n")
rep("PRUNE_REASONS = ('dependency-tree', 'vcs-tree', 'cargo-build-output')",
    "PRUNE_REASONS = ('dependency-tree', 'vcs-tree', 'cargo-build-output', 'opensip-custody-state')")
# pruned_anchors_from_directories: member roots pass through.
rep("def pruned_anchors_from_directories(dir_relpaths, cargo_roots):", "def pruned_anchors_from_directories(dir_relpaths, cargo_roots, member_roots=()):")
rep("    Returns {(anchor, reason): None} over the shared rule's existing reason vocabulary.\n    \"\"\"\n    out = {}\n",
    "    Returns {(anchor, reason): None} over the shared rule's existing reason vocabulary.\n    \"\"\"\n    # Both are forwarded once per directory: materialize them (Codex B2AREF-1).\n    cargo_roots, member_roots = tuple(cargo_roots), tuple(member_roots)\n    out = {}\n")
rep("        hit = classify_path(rel, cargo_roots)\n        if hit is not None:\n            out[hit] = None",
    "        hit = classify_path(rel, cargo_roots, member_roots)\n        if hit is not None:\n            out[hit] = None")
# cargo_roots_from_markers.
rep("def cargo_roots_from_markers(marker_relpaths: Iterable[str]) -> set[str]:",
    "def cargo_roots_from_markers(marker_relpaths: Iterable[str], member_roots: Iterable[str] = ()) -> set[str]:")
rep("    roots = set()\n    # Parents precede descendants",
    "    roots = set()\n    member_roots = tuple(member_roots)  # forwarded once per marker (Codex B2AREF-1)\n    # Parents precede descendants")
rep("        if mp.rpartition('/')[2] == CARGO_MARKER and classify_path(mp, roots) is None:",
    "        if mp.rpartition('/')[2] == CARGO_MARKER and classify_path(mp, roots, member_roots) is None:")
# classify_path: the SX-1 anchor joins the outermost comparison.
rep('''def classify_path(relpath: str, cargo_roots: Iterable[str]):
    """Return (anchor, reason) when `relpath` (a file or directory, internal relative form) lies inside a pruned
    tree, else None. `cargo_roots` are the directories holding Cargo.toml (see cargo_roots_from_markers)."""
    hit = _segment_prune(relpath)
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
''', '''def _custody_state(parts, member_roots):
    """SX-1: the outermost `.opensip` anchor at the root or directly under an admitted member root, else None."""
    best = None
    for base in [INTERNAL_ROOT, *member_roots]:
        prefix = base.split('/') if base else []
        k = len(prefix)
        if len(parts) > k and parts[:k] == prefix and parts[k] == OPENSIP_CUSTODY_STATE and (best is None or k < best):
            best = k
    return None if best is None else ('/'.join(parts[:best + 1]), 'opensip-custody-state')


def classify_path(relpath: str, cargo_roots: Iterable[str], member_roots: Iterable[str] = ()):
    """Return (anchor, reason) when `relpath` (a file or directory, internal relative form) lies inside a pruned
    tree, else None. `cargo_roots` are the directories holding Cargo.toml (see cargo_roots_from_markers);
    `member_roots` are the admitted D15 member roots, under each of which `.opensip` is an anchor (SX-1)."""
    hit = _segment_prune(relpath)
    parts = relpath.split('/')
    cargo = set(cargo_roots)
    for i, seg in enumerate(parts):
        if seg == CARGO_BUILD_OUTPUT_SEGMENT and '/'.join(parts[:i]) in cargo:
            target = '/'.join(parts[:i + 1]), 'cargo-build-output'
            # The outermost anchor wins across all reasons, not merely
            # within the dependency/VCS subset.
            if hit is None or i < hit[0].count('/'):
                hit = target
            break
    state = _custody_state(parts, member_roots)
    if state is not None and (hit is None or state[0].count('/') < hit[0].count('/')):
        return state
    return hit
''')
# enumerate_units: member roots pass through.
rep("                    unreadable_anchors: Iterable[str] = ()) -> dict:",
    "                    unreadable_anchors: Iterable[str] = (), member_roots: Iterable[str] = ()) -> dict:")
rep("    cargo_roots = cargo_roots_from_markers(markers)\n", "    member_roots = tuple(member_roots)  # forwarded repeatedly (Codex B2AREF-1)\n    cargo_roots = cargo_roots_from_markers(markers, member_roots)\n")
rep("        hit = classify_path(mp, cargo_roots)\n        if hit is not None:\n            pruned[hit] = pruned.get(hit, 0) + 1",
    "        hit = classify_path(mp, cargo_roots, member_roots)\n        if hit is not None:\n            pruned[hit] = pruned.get(hit, 0) + 1")
rep("        for key in pruned_anchors_from_directories(observed_directories, cargo_roots):",
    "        for key in pruned_anchors_from_directories(observed_directories, cargo_roots, member_roots):")
# Pruned-tree row version 3 (B-S1 PrunedTreeRowV3; Codex NBO-1 on the B2-a plan).
rep("PRUNED_TREE_ROW_VERSION = 2\n", "PRUNED_TREE_ROW_VERSION = 3   # 3: adds only the reason opensip-custody-state (B-S1 SX-1)\n")
# Version 3 boundary inventory.
rep("CURRENT_PROVENANCE_VERSION = 2\nSUPPORTED_PROVENANCE_VERSIONS = (1, 2)\nSUPPORTED_BOUNDARY_INVENTORY_VERSIONS = (1, 2)\nBOUNDARY_INVENTORY_VERSION = 2   # row-2 pruned trees (XA-02 / CR-25); version 1 stays a historical record",
    "CURRENT_PROVENANCE_VERSION = 3\nSUPPORTED_PROVENANCE_VERSIONS = (1, 2, 3)\nSUPPORTED_BOUNDARY_INVENTORY_VERSIONS = (1, 2, 3)\nBOUNDARY_INVENTORY_VERSION = 3   # 3: SX-1 rows and D15 members (B-S1); 2: row-2 pruned trees (XA-02 / CR-25); 1 historical")
rep("    pruned.sort(key=lambda t: (_bytes_key(t['path']), t['reason']))\n    return {'schemaVersion': BOUNDARY_INVENTORY_VERSION, 'source': BOUNDARY_INVENTORY_SOURCE, 'selectedRoot': root,\n            'nestedRepositories': repos, 'nestedProjects': projects, 'custodyExcludedUnits': custody, 'prunedTrees': pruned}",
    "    pruned.sort(key=lambda t: (_bytes_key(t['path']), t['reason']))\n    # Version 3 (B-S1): admitted D15 members as relative paths. They are not boundaries and add no prefix.\n    members = sorted({relative_locator(root, m['path']) for m in provenance.get('memberRepositories', [])}, key=_bytes_key)\n    return {'schemaVersion': BOUNDARY_INVENTORY_VERSION, 'source': BOUNDARY_INVENTORY_SOURCE, 'selectedRoot': root,\n            'nestedRepositories': repos, 'nestedProjects': projects, 'custodyExcludedUnits': custody, 'prunedTrees': pruned,\n            'memberRepositories': members}")
# conventional_excluded_prefixes: SX-1 always.
rep('''def conventional_excluded_prefixes(unit_roots: Iterable[str], cargo_roots: Iterable[str]) -> list[str]:''',
    '''def conventional_excluded_prefixes(unit_roots: Iterable[str], cargo_roots: Iterable[str],
                                   member_roots: Iterable[str] = ()) -> list[str]:''')
rep("under every unit\n    root and `target` under every Cargo root only.", "under every unit\n    root, `target` under every Cargo root only, and `.opensip` at the root and each member root (SX-1).")
rep("""    for r in cargo_roots:
        out.add(((r + '/') if r else '') + CARGO_BUILD_OUTPUT_SEGMENT)
    return sorted(out, key=lambda s: s.encode('utf-8'))""", """    for r in cargo_roots:
        out.add(((r + '/') if r else '') + CARGO_BUILD_OUTPUT_SEGMENT)
    # SX-1 (B-S1 LD-3): always, whether or not `.opensip` was observed.
    for r in [INTERNAL_ROOT, *member_roots]:
        out.add(((r + '/') if r else '') + OPENSIP_CUSTODY_STATE)
    return sorted(out, key=lambda s: s.encode('utf-8'))""")
(HERE / 'discovery-defaults.sx1-r1.py').write_text(s)
print('written', len(s.encode()))
