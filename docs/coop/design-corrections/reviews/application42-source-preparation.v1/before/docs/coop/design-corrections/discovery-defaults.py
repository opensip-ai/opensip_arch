"""Shared zero-config discovery defaults (PROPOSED, not self-accepted).

ONE rule, consumed by the security discovery instrument (`security/security_lifecycle_model_v1.py`
`discovery`), the native unit instrument (`native/native_evidence_model.v2.py` `discover_units`,
`assign_membership`, `unit_scope_descriptor`, `typescript_mode`) and available to the integration host
model. Pure functions over relative logical paths; no filesystem access. Design reference only.

Why this exists (post-reset review MUST-3): the security marker scan and the native unit discovery each
enumerated every `node_modules/<pkg>/package.json` as a workspace unit, the native file-membership rule
matched ignore conventions as path substrings (so `packages/target/index.ts` was erased), and the two
instruments normalized the explicit root sentinel `.` differently. The rule below is stated once:

  * Pruned trees, by ACTUAL path segment (never substring), anywhere under the admitted root:
      - dependency trees: a directory segment named `node_modules`;
      - VCS trees: a directory segment named `.git`, `.hg`, `.svn` or `.jj`;
      - Cargo build output: a directory segment named `target` whose PARENT directory holds `Cargo.toml`
        (an actual Cargo root: package or workspace). `packages/target/`, `src/target/` and any other
        directory merely called `target` are ordinary source directories.
    A pruned tree contributes no workspace unit, no marker, no program member and no custody walk. The
    anchor of each pruned tree that discovery actually observed is recorded once (`prunedTrees`), so 4200
    installed package manifests produce one record, not 4200 units and not a cap refusal.
  * Workspace units are the directories that hold a language marker (`Cargo.toml`, `package.json`,
    `tsconfig.json`, `jsconfig.json`) and are not inside a pruned tree. The first-party unit cap is 4096
    directories; exceeding it is a typed refusal (`WORKSPACE_UNIT_LIMIT`, D9 `REQUEST.UNSATISFIABLE`)
    without truncation. Installed dependencies never count toward it.
  * Explicit roots (CLI `--workspace-root`, Config2 `discovery.workspaceRoots`) use the identity contract's
    sentinel: `.` alone denotes the admitted project root and normalizes to the internal root `""`; every
    other value is a strict logical path (no absolute, empty, `.` or `..` segment, no backslash, no NUL).
    Both instruments call `normalize_explicit_root`, so one Config2 value has one meaning.
  * Explicit roots are EXACT roots, never scan roots: security admits their custody (recording a unit with
    the markers found, possibly none, plus a warning) and the native language-unit layer refuses an explicit
    root without a language marker as CONFIG.INVALID (`native.explicit-root-without-marker`). That is the
    already selected truthful behaviour; the two layers now agree on the path they are talking about.

  * Admitted boundary inventory (post-reset review v2, P3): the security discovery instrument decides the
    project's AUTHORITY boundaries (nested repositories = other custody roots; nested `opensip.json` =
    deliberate nested projects; custody-excluded unit directories) in absolute custody locators. The
    native language-unit instrument must never re-derive them from caller-supplied ignores. The host
    converts the ACCEPTed `DiscoveryProvenanceV1` once, with `boundary_inventory_from_provenance`, into
    the closed `AdmittedBoundaryInventoryV1` (relative scope paths under the selected root) and passes it
    to `discover_units(markers, explicit_roots, boundaries)`. Both instruments apply the same
    `classify_boundary` prefix rule: a marker directory or file at or below a nested boundary is outside
    this project (no unit, no membership, explicit root crossing refuses), and each boundary anchor
    enters the Plan scope descriptor's `excludedPathPrefixes`.

Interface for integration (Codex): `enumerate_units(marker_relpaths)`, `classify_path(relpath, cargo_roots)`,
`boundary_inventory_from_provenance(provenance)` and `classify_boundary(path, nestedRepositories,
nestedProjects)` are the entry points a host composition needs; all are total and deterministic.
"""
from __future__ import annotations

from collections.abc import Iterable

DISCOVERY_DEFAULTS_VERSION = 2   # 2: admitted boundary inventory API (P3); interface of version 1 unchanged
ROOT_SENTINEL = '.'
INTERNAL_ROOT = ''
WORKSPACE_MARKERS = ('Cargo.toml', 'package.json', 'tsconfig.json', 'jsconfig.json')
DEPENDENCY_TREE_SEGMENTS = ('node_modules',)
VCS_TREE_SEGMENTS = ('.git', '.hg', '.svn', '.jj')
CARGO_BUILD_OUTPUT_SEGMENT = 'target'
CARGO_MARKER = 'Cargo.toml'
MAX_WORKSPACE_UNITS = 4096
PRUNE_REASONS = ('dependency-tree', 'vcs-tree', 'cargo-build-output')


class RootGrammarError(ValueError):
    """An explicit root value violates the logical path grammar (detail is the exception text)."""


def normalize_explicit_root(spec) -> str:
    """`.` -> `` (the admitted project root); otherwise a strict logical relative directory path with any
    single trailing `/` removed. Raises RootGrammarError('ROOT_GRAMMAR') for anything else."""
    if not isinstance(spec, str) or spec == '':
        raise RootGrammarError('ROOT_GRAMMAR')
    if spec == ROOT_SENTINEL:
        return INTERNAL_ROOT
    if spec.startswith('/') or '\\' in spec or '\x00' in spec:
        raise RootGrammarError('ROOT_GRAMMAR')
    body = spec[:-1] if spec.endswith('/') and len(spec) > 1 else spec
    if any(seg in ('', '.', '..') for seg in body.split('/')):
        raise RootGrammarError('ROOT_GRAMMAR')
    return body


def spell_root(internal_root: str) -> str:
    """Inverse of normalize_explicit_root for records whose grammar needs a non-empty text (`.`)."""
    return ROOT_SENTINEL if internal_root == INTERNAL_ROOT else internal_root


def _dir_of(relpath: str) -> str:
    return relpath.rpartition('/')[0]


def cargo_roots_from_markers(marker_relpaths: Iterable[str]) -> set[str]:
    """Directories (internal relative form, `` = root) that hold `Cargo.toml` and are not themselves inside a
    dependency or VCS tree. A `Cargo.toml` under `node_modules/` never makes a Cargo root."""
    roots = set()
    for mp in marker_relpaths:
        if mp.rpartition('/')[2] == CARGO_MARKER and _segment_prune(mp) is None:
            roots.add(_dir_of(mp))
    return roots


def _segment_prune(relpath: str):
    """Dependency/VCS pruning by exact segment. Returns (anchor, reason) for the OUTERMOST pruned segment or None."""
    parts = relpath.split('/')
    for i, seg in enumerate(parts):
        if seg in DEPENDENCY_TREE_SEGMENTS:
            return '/'.join(parts[:i + 1]), 'dependency-tree'
        if seg in VCS_TREE_SEGMENTS:
            return '/'.join(parts[:i + 1]), 'vcs-tree'
    return None


def classify_path(relpath: str, cargo_roots: Iterable[str]):
    """Return (anchor, reason) when `relpath` (a file or directory, internal relative form) lies inside a pruned
    tree, else None. `cargo_roots` are the directories holding Cargo.toml (see cargo_roots_from_markers)."""
    hit = _segment_prune(relpath)
    if hit is not None:
        return hit
    parts = relpath.split('/')
    cargo = set(cargo_roots)
    for i, seg in enumerate(parts):
        if seg == CARGO_BUILD_OUTPUT_SEGMENT and '/'.join(parts[:i]) in cargo:
            return '/'.join(parts[:i + 1]), 'cargo-build-output'
    return None


def enumerate_units(marker_relpaths: Iterable[str]) -> dict:
    """Zero-config unit enumeration over the relative paths of marker FILES found under the admitted root.

    Returns {'unitDirs': [...sorted internal relative dirs...], 'prunedTrees': [{'path', 'reason',
    'markerCount'}], 'refusal': None | {'detail': 'WORKSPACE_UNIT_LIMIT', 'unitCount': n, 'limit': 4096}}.
    On refusal `unitDirs` is empty (no truncation). Marker paths must be relative (no leading `/`); a path
    whose file name is not a marker is ignored so callers may pass any inventory."""
    markers = sorted({p for p in marker_relpaths if isinstance(p, str) and not p.startswith('/') and p.rpartition('/')[2] in WORKSPACE_MARKERS},
                     key=lambda s: s.encode('utf-8'))
    cargo_roots = cargo_roots_from_markers(markers)
    pruned: dict[tuple[str, str], int] = {}
    unit_dirs: set[str] = set()
    for mp in markers:
        hit = classify_path(mp, cargo_roots)
        if hit is not None:
            pruned[hit] = pruned.get(hit, 0) + 1
            continue
        unit_dirs.add(_dir_of(mp))
    pruned_trees = [{'path': anchor, 'reason': reason, 'markerCount': n}
                    for (anchor, reason), n in sorted(pruned.items(), key=lambda kv: (kv[0][0].encode('utf-8'), kv[0][1]))]
    if len(unit_dirs) > MAX_WORKSPACE_UNITS:
        return {'unitDirs': [], 'prunedTrees': pruned_trees,
                'refusal': {'detail': 'WORKSPACE_UNIT_LIMIT', 'unitCount': len(unit_dirs), 'limit': MAX_WORKSPACE_UNITS}}
    return {'unitDirs': sorted(unit_dirs, key=lambda s: s.encode('utf-8')), 'prunedTrees': pruned_trees, 'refusal': None}


# ---------------------------------------------------------------------------------------------------
# Admitted boundary inventory (P3): security's authority boundaries, converted once for the native instrument
# ---------------------------------------------------------------------------------------------------
BOUNDARY_INVENTORY_VERSION = 1
BOUNDARY_INVENTORY_SOURCE = 'security.discovery'
BOUNDARY_REASONS = ('nested-repository', 'nested-project', 'custody-excluded')
_MARKER_CUSTODY_PREFIX = 'MARKER_CUSTODY:'


class BoundaryError(ValueError):
    """A custody locator cannot be converted into a relative scope path (detail is the exception text)."""


def _bytes_key(s: str) -> bytes:
    return s.encode('utf-8')


def relative_locator(selected_root: str, absolute: str) -> str:
    """Absolute custody locator at or below `selected_root` -> internal relative form (`` for the root itself).
    Raises BoundaryError('LOCATOR_OUTSIDE_ROOT') for a locator outside the root and
    BoundaryError('LOCATOR_GRAMMAR') for one whose relative segments violate the logical path grammar."""
    if not isinstance(selected_root, str) or not selected_root or not isinstance(absolute, str):
        raise BoundaryError('LOCATOR_OUTSIDE_ROOT')
    if absolute == selected_root:
        return INTERNAL_ROOT
    base = selected_root.rstrip('/') + '/'
    if not absolute.startswith(base):
        raise BoundaryError('LOCATOR_OUTSIDE_ROOT')
    rel = absolute[len(base):]
    if rel == '' or '\\' in rel or '\x00' in rel or any(seg in ('', '.', '..') for seg in rel.split('/')):
        raise BoundaryError('LOCATOR_GRAMMAR')
    return rel


def boundary_inventory_from_provenance(provenance: dict) -> dict:
    """Convert an ACCEPTed security `DiscoveryProvenanceV1` into the closed `AdmittedBoundaryInventoryV1`:
    {schemaVersion: 1, source: 'security.discovery', selectedRoot, nestedRepositories: [rel dirs],
     nestedProjects: [rel dirs], custodyExcludedUnits: [{path: rel dir, reason}], prunedTrees: [{path: rel, reason,
     markerCount}]}. Lists are sorted by UTF-8 bytes. `custodyExcludedUnits` carries the security `excludedUnits`
    rows whose reason is a custody/depth exclusion (`DIRECTORY_CUSTODY:*`, `MARKER_CUSTODY:*`, `DEPTH`); rows already
    explained by a nested boundary (`INSIDE_NESTED_*`) are not repeated. The result is TRUSTED OUTPUT of the security
    instrument, never a caller-authored ignore list; a host passes it unchanged to the native `discover_units`."""
    if not isinstance(provenance, dict):
        raise BoundaryError('PROVENANCE_SHAPE')
    root = provenance.get('selectedRoot')
    if not isinstance(root, str) or not root:
        raise BoundaryError('NO_SELECTED_ROOT')
    repos = sorted({relative_locator(root, p) for p in provenance.get('nestedRepositories', [])}, key=_bytes_key)
    projects = sorted({relative_locator(root, p) for p in provenance.get('nestedProjects', [])}, key=_bytes_key)
    custody = []
    for row in provenance.get('excludedUnits', []):
        reason = row.get('reason', '')
        if reason.startswith('INSIDE_NESTED_'):
            continue
        custody.append({'path': relative_locator(root, row['path']), 'reason': reason})
    custody.sort(key=lambda r: (_bytes_key(r['path']), _bytes_key(r['reason'])))
    pruned = [{'path': relative_locator(root, t['path']), 'reason': t['reason'], 'markerCount': t['markerCount']}
              for t in provenance.get('prunedTrees', [])]
    pruned.sort(key=lambda t: (_bytes_key(t['path']), t['reason']))
    return {'schemaVersion': BOUNDARY_INVENTORY_VERSION, 'source': BOUNDARY_INVENTORY_SOURCE, 'selectedRoot': root,
            'nestedRepositories': repos, 'nestedProjects': projects, 'custodyExcludedUnits': custody, 'prunedTrees': pruned}


def _at_or_below(path: str, anchor: str) -> bool:
    return path == anchor or path.startswith(anchor.rstrip('/') + '/')


def classify_boundary(path: str, nested_repositories: Iterable[str], nested_projects: Iterable[str]):
    """Return (anchor, reason) when `path` (absolute or relative; the same prefix rule serves both instruments) lies
    at or below a nested repository or nested project anchor, else None. Repositories are tested first: a nested
    project inside a nested repository belongs to that repository."""
    for n in nested_repositories:
        if _at_or_below(path, n):
            return n, 'nested-repository'
    for n in nested_projects:
        if _at_or_below(path, n):
            return n, 'nested-project'
    return None


def classify_custody_exclusion(unit_dir: str, marker_name, custody_excluded: Iterable[dict]):
    """Return (anchor, 'custody-excluded') when the security instrument excluded `unit_dir` (or an ancestor) for
    directory custody/depth, or excluded exactly `marker_name` in that directory for marker custody; else None."""
    for row in custody_excluded:
        reason = row.get('reason', '')
        if reason.startswith(_MARKER_CUSTODY_PREFIX):
            if marker_name is not None and row['path'] == unit_dir and reason[len(_MARKER_CUSTODY_PREFIX):].split(':', 1)[0] == marker_name:
                return row['path'], 'custody-excluded'
        elif _at_or_below(unit_dir, row['path']):
            return row['path'], 'custody-excluded'
    return None


def boundary_excluded_prefixes(inventory: dict) -> list[str]:
    """Anchors a Plan scope descriptor must list for an admitted boundary inventory: every nested repository, every
    nested project and every directory-custody exclusion (marker-custody rows exclude a file, not a prefix)."""
    out = set(inventory.get('nestedRepositories', [])) | set(inventory.get('nestedProjects', []))
    for row in inventory.get('custodyExcludedUnits', []):
        if not row.get('reason', '').startswith(_MARKER_CUSTODY_PREFIX) and row['path'] != INTERNAL_ROOT:
            out.add(row['path'])
    return sorted(out, key=_bytes_key)


def conventional_excluded_prefixes(unit_roots: Iterable[str], cargo_roots: Iterable[str]) -> list[str]:
    """Prefixes a scope descriptor lists for the conventions above: `.git`, `node_modules` under every unit
    root and `target` under every Cargo root only. Sorted by UTF-8 bytes; the root is spelled ``."""
    out = set()
    for r in unit_roots:
        base = (r + '/') if r else ''
        for seg in DEPENDENCY_TREE_SEGMENTS + ('.git',):
            out.add(base + seg)
    for r in cargo_roots:
        out.add(((r + '/') if r else '') + CARGO_BUILD_OUTPUT_SEGMENT)
    return sorted(out, key=lambda s: s.encode('utf-8'))


__all__ = [n for n in dir() if not n.startswith('_')]
