"""B2-b0: the current discovery reference (M3-B r5 item 13; B2-b plan r4 section 1.0). PROPOSED, design reference only.

The accepted SLM `discovery` (security_lifecycle_model_v1.py) predates the shared-rule corrections, SX-1 and
version 3. This module makes it the current oracle WITHOUT editing a byte of SLM:

  * `load(arch)` imports SLM at its accepted bytes and replaces its module global `DD` with the bound B2-a
    reference copy (contract successor 163). SLM calls `DD.*` at call time, so its algorithm then runs with the
    outermost rule across all four reasons, parent-first Cargo roots and the SX-1 `.opensip` anchor.
  * `walker_population(inp, selected_root, unit_source)` restricts SLM's synthetic `fs` to exactly what the
    native walker observes. SL S3 says nested repositories and projects are recorded and never entered, and a
    pruned tree is never descended (SL:146-168, SL:187-216); SLM's whole-`fs` collection over-observes. The
    restriction removes those never-observed paths and nothing else.
  * `current(inp)` runs SLM twice. Pass one, on the full input, gives the selected root, the unit source (the
    walker chooses its source before traversal) and the UPWARD provenance: what selection observed. Pass two runs on
    the DOWNWARD population plus pass one's walked rows at or above the selected root, with `cwd` set to the selected
    root, and gives the DOWNWARD provenance. Upward evidence never enters the downward population (r2, B2B0REF-1):
    a `cwd` below the root, under `.opensip` or in an unrelated sibling contributes nothing to what `finish` sees.
  * `project_v3(result)` gives the version-3 shape WITHOUT `workspaceDeclarations`, which only B3-b's readers
    can observe; `boundary_inventory_v3(result)` gives the complete `AdmittedBoundaryInventoryV3`.

Population rules (plan r4; r2):
  * Upward evidence (pass two only): pass one's walked rows that lie at or above the selected root, plus the
    explicit path and its resolved spelling when not below the root, each with its `opensip.json` entry. Walked
    rows below the root (the part of the `cwd` chain under it) are not downward observations and are excluded.
  * Downward, automatic: parent-first from the selected root. A child of an ordinary listed directory enters. A
    pruned anchor (any reason) enters as its own entry only and is never listed or probed. A directory of at most
    256 segments other than the selected root holding `vcs` or `opensip.json` is a boundary: it is probed for that
    evidence, enters with its `opensip.json` entry only and is never otherwise listed. Directories of at most 256
    segments are listed; a directory of exactly 257 segments is never listed or probed for boundaries, and only its
    four marker names are observed (for SLM's `DEPTH` exclusion, Codex NBO-1); nothing deeper is observed.
  * Observed evidence only (r3): an entry keeps `vcs` only if its directory is probed (the root, a listed
    directory, a probed boundary, a chain directory). A pruned anchor or a 257-segment directory never carries it.
  * Downward, explicit or config: for each named root, the chain from the selected root, parent-first. Each chain
    directory enters with its `Cargo.toml` and `opensip.json` entries. A chain directory below the root that is a
    boundary stops the chain (SLM's crossing refusal). The next component is classified with the Cargo roots
    known so far; a pruned prefix enters as its own entry only and stops the chain. At the named root, its
    subtree enters under the automatic rule. Nothing else enters.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path

SLM = ('docs/coop/design-corrections/security/security_lifecycle_model_v1.py', 208076,
       'd0ef9814d27b86f10bdc1aa9a9a4781124c93c3dd92eeecdfe3090fe21d18bb9')
RULE = ('docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py', 25293,
        '4a104209af0ba89c76826ba7f6be4c4085f1eb7db90410f6bb731041562fdcc8')
MAX_LISTED_DEPTH = 256
READERS = ('cargo-config-patch', 'npm-workspaces-members')


def _pinned(arch, row):
    path, size, digest = row
    raw = (arch / path).read_bytes()
    if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('pin mismatch: ' + path)
    return arch / path


def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(arch: Path, historical: bool = False):
    """SLM at its accepted bytes. Current (default): its `DD` global replaced by the bound B2-a reference."""
    slm = _module('slm_historical' if historical else 'slm_current', _pinned(arch, SLM))
    rule = _module('shared_rule_sx1', _pinned(arch, RULE))
    if not historical:
        slm.DD = rule
    return slm, rule


def _parent(p):
    return p.rsplit('/', 1)[0] or '/'


def _join(d, name):
    return d.rstrip('/') + '/' + name


def _rel(root, p):
    return '' if p == root else p[len(root.rstrip('/')) + 1:]


def _ancestors(p):
    out = [p]
    while p != '/':
        p = _parent(p)
        out.append(p)
    return out


def walker_population(rule, inp, selected_root, unit_source):
    """The DOWNWARD population only: what the native walker observes at or below the selected root."""
    fs = inp['fs']
    keep = {}
    probed = set()  # directories whose interior the walker observes (listed, boundary-probed or chain)

    def admit(p):
        if p in fs:
            keep[p] = fs[p]

    children = {}
    for p in fs:
        if p != '/':
            children.setdefault(_parent(p), []).append(p)
    root = selected_root

    def is_dir(p):
        return fs.get(p, {}).get('kind') == 'dir'

    def boundary(p):
        return p != root and is_dir(p) and (fs[p].get('vcs') or fs.get(_join(p, 'opensip.json'), {}).get('kind') == 'file')

    def subtree(start, cargo):
        """Automatic rule from `start` (an ordinary directory already admitted), breadth-first, parent-first."""
        queue = [start]
        while queue:
            d = queue.pop(0)
            depth = len(_rel(root, d).split('/')) if d != root else 0
            if depth > MAX_LISTED_DEPTH:
                # A 257-segment directory: only its four marker names are observed (NBO-1). It is not probed:
                # no `opensip.json`, no VCS evidence (r3, B2B0REF-4).
                for m in rule.WORKSPACE_MARKERS:
                    admit(_join(d, m))
                continue
            probed.add(d)
            kids = sorted(children.get(d, []))
            if fs.get(_join(d, 'Cargo.toml'), {}).get('kind') == 'file':
                cargo.add(_rel(root, d))
            for c in kids:
                admit(c)
            for c in kids:
                if not is_dir(c):
                    continue
                hit = rule.classify_path(_rel(root, c), cargo, ())
                if hit is not None:
                    continue  # a pruned anchor: its own entry only, never probed (r3, B2B0REF-3)
                if depth + 1 > MAX_LISTED_DEPTH:
                    queue.append(c)  # the depth policy comes before any boundary evidence (r3, B2B0REF-4)
                    continue
                if boundary(c):
                    probed.add(c)
                    admit(_join(c, 'opensip.json'))
                    continue
                queue.append(c)

    if root is None:
        return dict(inp, fs=keep)
    admit(root)
    probed.add(root)
    cargo = set()
    if unit_source == 'automatic':
        subtree(root, cargo)
    else:
        named = inp.get('explicitJoins') if unit_source == 'explicit-joins' else inp.get('configWorkspaceRoots')
        for spec in named or []:
            try:
                rel = rule.normalize_explicit_root(spec)
            except (rule.RootGrammarError, TypeError):
                continue
            parts = rel.split('/') if rel else []
            d = root
            known = set()
            admit(_join(root, 'Cargo.toml'))
            admit(_join(root, 'opensip.json'))
            if fs.get(_join(root, 'Cargo.toml'), {}).get('kind') == 'file':
                known.add('')
            reached = True
            for i, part in enumerate(parts):
                nxt = _join(d, part)
                admit(nxt)
                if not is_dir(nxt):
                    reached = False
                    break
                if rule.classify_path(_rel(root, nxt), known, ()) is not None:
                    reached = False  # a pruned prefix: its own entry only
                    break
                admit(_join(nxt, 'Cargo.toml'))
                admit(_join(nxt, 'opensip.json'))
                probed.add(nxt)
                if boundary(nxt):
                    reached = False  # the crossing refusal applies
                    break
                if fs.get(_join(nxt, 'Cargo.toml'), {}).get('kind') == 'file':
                    known.add(_rel(root, nxt))
                d = nxt
            if reached:
                subtree(d, set(known))
    # r3 (B2B0REF-3): every entry carries only the evidence the walker observed. `vcs` is evidence from inside a
    # directory (its `.git` entry), so only a probed directory keeps it; a pruned anchor or a 257-segment
    # directory keeps its own kind, identity and custody fields only.
    return dict(inp, fs={p: (e if p in probed or 'vcs' not in e else {k: v for k, v in e.items() if k != 'vcs'}) for p, e in keep.items()})


UPWARD_FIELDS = ('mode', 'configPath', 'walked', 'stopReason', 'custodyWaiver', 'vcs', 'explicitPathWasSymlink')


def _below(p, root):
    return p.startswith(root.rstrip('/') + '/')


def upward_evidence(inp, first):
    """Pass one's selection evidence that is not below the selected root (r2, B2B0REF-1): its walked rows and the
    explicit path with its resolved spelling, each with its `opensip.json` entry. Anything below the root (the part
    of the `cwd` chain under it, or a config file inside it) is downward territory and comes only from
    `walker_population`."""
    fs = inp['fs']
    root = first['provenance']['selectedRoot']
    keep = {}
    paths = [w['path'] for w in first['provenance']['walked']]
    paths += [p for p in (inp.get('explicitProject'), inp.get('explicitResolved')) if isinstance(p, str)]
    for p in paths:
        for q in (p, _join(p, 'opensip.json')):
            if q in fs and not _below(q, root):
                keep[q] = fs[q]
    return keep


def current(slm, rule, inp):
    """The current oracle. Returns (result, downward population, pass-two input)."""
    first = slm.discovery(copy.deepcopy(inp))
    prov = first['provenance']
    if prov.get('selectedRoot') is None or prov.get('unitSource') is None:
        return first, None, None
    root = prov['selectedRoot']
    downward = walker_population(rule, inp, root, prov['unitSource'])
    second_input = dict(downward, fs={**upward_evidence(inp, first), **downward['fs']}, cwd=root)
    second = slm.discovery(copy.deepcopy(second_input))
    p2 = second['provenance']
    if p2.get('selectedRoot') != root or p2.get('unitSource') != prov['unitSource']:
        raise ValueError('pass two changed the selected root or unit source')
    for field in UPWARD_FIELDS:
        p2[field] = copy.deepcopy(prov[field])
    return second, downward, second_input


def project_v3(result):
    """The version-3 shape, partial: `workspaceDeclarations` is pending (B3-b's readers)."""
    out = copy.deepcopy(result)
    prov = out['provenance']
    prov['schemaVersion'] = 3
    prov['memberRepositories'] = []
    prov['memberConfigs'] = []
    out['pendingFields'] = ['workspaceDeclarations']
    return out


def shape_fill(partial):
    """SHAPE-ONLY: the partial provenance with each reader's `absent` row, for schema validation of the other
    fields. Never an observation and never emitted."""
    prov = copy.deepcopy(partial['provenance'])
    prov['workspaceDeclarations'] = [dict(readerId=r, readerVersion=1, state='absent', path=None, contentSha256=None,
                                          stateSubject=None, unresolved=[]) for r in READERS]
    return prov


def boundary_inventory_v3(rule, partial):
    """The complete AdmittedBoundaryInventoryV3 of an ACCEPTed partial result."""
    if partial.get('status') != 'ACCEPT':
        raise ValueError('BOUNDARY_INVENTORY_REQUIRES_ACCEPT')
    return rule.boundary_inventory_from_provenance(partial['provenance'])
