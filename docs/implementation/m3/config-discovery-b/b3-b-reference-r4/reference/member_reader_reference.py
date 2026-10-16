"""B3-b0 r4: the members-and-readers reference (M3-B r9 items 19 to 24; B3-b plan r2 section 1, amendment A4). PROPOSED,
design reference, contract successor 169 (it succeeds B3-b0 r3, successor 168, whose bytes are unchanged).

The B2-b0 discovery reference (contract successor 164) leaves `workspaceDeclarations` pending and members empty. This
module completes D15 over it WITHOUT editing a byte of B2-b0, SLM or the B2-a rule:

  * `discover(ctx, inp)` is the current discovery with members. Its input is SLM's synthetic observation plus four side
    tables, removed before SLM sees the input:
      - `contents`: {absolute path: text | {"hex": ...}}, the bytes of reader carriers and provider manifests;
      - `vcsMarkers`: {absolute directory: [marker, ...]} for directories holding more than SLM's one `vcs` flag says
        (default: a directory with `vcs` true holds `.git` as a directory; an `indirection` holds `.git` as a file);
      - `memberObservations`: {absolute directory: "admitted" | "<subject>"}, item 6b's verdict for a counted
        candidate (default "admitted"). Item 6b is X2 r9's member observation over item 6a's reviewed decoders,
        unchanged (law item 21); this reference takes its verdict, it does not re-model Git (plan r2 LD-B3B-2).
      - (r4) `memberGitlinks`: {absolute directory: [member-relative path, ...]}, the index gitlinks item 6b reports for a
        candidate it admits (default none). Each is a nested repository (law items 21 and 22): never entered, recorded in
        `nestedRepositories` when it is a directory, a crossing for an exact root, and no link is read at or below it.
  * Pass one is SLM over the unchanged input: selection, the upward walk and the unit source, exactly B2-b0's.
  * The readers (`cargo-config-patch@1`, `npm-workspaces-members@1`) then read their carriers at W as data, and the
    registry's rules decide placement, the member cap, membership (branch A from the `workspaceRoots` array or
    `--workspace-root`; branch B from the readers; nothing when W is in a repository), dispositions and links.
    (r4, plan amendment A4-2) Branch A decides its members before any walk: a pure array gate (size, then grammar),
    then the member decisions in path order, then one walk with the admitted members and their gitlinks.
  * Pass two is B2-b0's downward population and SLM's `finish` with every admitted member's VCS evidence and its own
    root `opensip.json` withheld, so a member is entered as an ordinary directory (S3: "A member is neither a nested
    repository nor a boundary"), with the shared rule bound to the member roots (SX-1 at each member root). Nested
    repositories and projects inside a member keep their evidence and stay boundaries.
  * The result is a complete `DiscoveryResultV3`: `memberRepositories`, `workspaceDeclarations` and `memberConfigs`
    filled, validated against the SLS bundle merged with B-S1's additions; and `AdmittedBoundaryInventoryV3`.

The registry (`b-s1/registry/workspace-declaration-readers.v1.json`) is the text this code follows; every reason it
lists has a checker case. Design evidence: synthetic inputs only, no filesystem tree, product code or qualification.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import json
import tomllib
from pathlib import Path

B2B0 = ('docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py', None, None)
CANONICAL = ('docs/coop/design-corrections/foundation/canonical.py', 6465,
             'd47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442')
REGISTRY = 'docs/implementation/m3/config-discovery-b/b-s1/registry/workspace-declaration-readers.v1.json'
READERS = ('cargo-config-patch', 'npm-workspaces-members')
VCS = ('.git', '.hg', '.svn', '.jj')
MAX_MEMBERS = 64
MAX_DEPTH = 256
CARRIER_CAP = 4 * 1024 * 1024
GLOB = set('*?[]{}!')
SIDE = ('contents', 'vcsMarkers', 'memberObservations', 'memberGitlinks')


def _pinned(arch, row):
    path, size, digest = row
    raw = (arch / path).read_bytes()
    if (size is not None and len(raw) != size) or (digest is not None and hashlib.sha256(raw).hexdigest() != digest):
        raise ValueError('pin mismatch: ' + path)
    return arch / path


def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Context:
    """The loaded references: B2-b0 (with SLM and the B2-a rule), the foundation's exact JSON parser, the registry."""

    def __init__(self, arch: Path, b2b0_pin=None):
        arch = Path(arch)
        self.b2b0 = _module('b2b0_reference', _pinned(arch, b2b0_pin or B2B0))
        self.slm, self.rule = self.b2b0.load(arch)
        self.C = _module('foundation_canonical', _pinned(arch, CANONICAL))
        self.registry = json.loads((arch / REGISTRY).read_bytes())


class _BoundRule:
    """The B2-a rule with `member_roots` defaulted to this discovery's admitted members (SX-1 at member roots)."""

    def __init__(self, rule, members):
        self._rule, self._members = rule, tuple(members)

    def __getattr__(self, name):
        value = getattr(self._rule, name)
        if not callable(value) or isinstance(value, type):
            return value
        try:
            takes = 'member_roots' in inspect.signature(value).parameters
        except (TypeError, ValueError):
            takes = False
        if not takes:
            return value

        def call(*args, **kwargs):
            if 'member_roots' not in kwargs and len(args) < list(inspect.signature(value).parameters).index('member_roots') + 1:
                kwargs['member_roots'] = self._members
            return value(*args, **kwargs)
        return call


class _PopulationRule:
    """For B2-b0's `walker_population`, which passes `()` as the member roots: its pruning sees the admitted members, so
    the population never observes inside `M/.opensip` (SX-1 at each member root), as the walker never does."""

    def __init__(self, rule, members):
        self._rule, self._members = rule, tuple(members)

    def __getattr__(self, name):
        return getattr(self._rule, name)

    def classify_path(self, relpath, cargo_roots, member_roots=()):
        return self._rule.classify_path(relpath, cargo_roots, self._members)


# ------------------------------------------------------------------ the synthetic tree

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


# The reader code's every metadata lookup goes through `_entry` (r3, B3B0REF-R2-RF-1), so a checker can record exactly
# which paths the readers consulted. SLM and B2-b0 keep their own access to the tree.
OBSERVED = None


def _entry(inp, path):
    if OBSERVED is not None:
        OBSERVED.append(path)
    return inp['fs'].get(path)


def _bytes(inp, path):
    v = inp.get('contents', {}).get(path)
    if v is None:
        return None
    return bytes.fromhex(v['hex']) if isinstance(v, dict) else v.encode('utf-8')


def _markers(inp, d):
    """The VCS markers directory `d` holds, each as (name, is_directory)."""
    side = inp.get('vcsMarkers', {}).get(d)
    if side is not None:
        return [(m, (_entry(inp, _join(d, m)) or {}).get('kind') == 'dir') for m in side]
    v = (_entry(inp, d) or {}).get('vcs')
    if v is True:
        return [('.git', True)]
    if isinstance(v, dict):
        return [('.git', False)]
    return []


def _project_vcs(inp):
    """One VCS representation (r2, B3B0REF-R1-RF-3). The side table `vcsMarkers` must agree with the tree: every marker it
    lists exists as an entry of that directory, and a directory it lists with markers carries SLM's `vcs` evidence (added
    here when absent), so the same positive observation that excludes a candidate also keeps it a nested repository
    for selection and for every boundary decision. A listed directory with no marker, or with legacy `vcs` evidence and
    an empty list, is an inconsistent observation and refuses before discovery."""
    fs = copy.deepcopy(inp['fs'])
    for d, markers in inp.get('vcsMarkers', {}).items():
        if not isinstance(markers, list) or not markers or any(m not in VCS for m in markers):
            raise ValueError('VCS_SIDE_TABLE_INCONSISTENT:' + d)
        if any(_join(d, m) not in fs for m in markers) or fs.get(d, {}).get('kind') != 'dir':
            raise ValueError('VCS_SIDE_TABLE_INCONSISTENT:' + d)
        if not fs[d].get('vcs'):
            fs[d] = dict(fs[d], vcs=True)
    return fs


def _member_gitlinks(inp):
    """(r4) The `memberGitlinks` side table, checked as an observation of a Git index: each key a directory of the tree,
    each value a list of distinct canonical member-relative paths (the entry grammar), none at or below another (an
    index holds nothing below a gitlink). Anything else is an inconsistent observation and refuses before discovery:
    `MEMBER_GITLINKS_INCONSISTENT` for a table that is not a mapping with string keys, else
    `MEMBER_GITLINKS_INCONSISTENT:<dir>` for the first key (in table order) whose entry is not consistent. (r4 round 2,
    B3B0REF-R4-RF-1) Every value's shape, every element's type and every element's own grammar are checked before any
    two elements are compared, so the rejection never depends on element order."""
    table = inp.get('memberGitlinks', {})
    if not isinstance(table, dict) or not all(isinstance(d, str) for d in table):
        raise ValueError('MEMBER_GITLINKS_INCONSISTENT')
    for d, links in table.items():
        if inp['fs'].get(d, {}).get('kind') != 'dir' or not isinstance(links, list):
            raise ValueError('MEMBER_GITLINKS_INCONSISTENT:' + d)
        if not all(isinstance(g, str) and _entry_path(g)[1] is None for g in links):
            raise ValueError('MEMBER_GITLINKS_INCONSISTENT:' + d)
        # Only validated strings are related: no repeat, and none at or below another.
        if len(set(links)) != len(links) or any(h != g and _within(g, h) for g in links for h in links):
            raise ValueError('MEMBER_GITLINKS_INCONSISTENT:' + d)
    return table


# ------------------------------------------------------------------ the readers

class _Entry:
    def __init__(self, reader, entry, directory=None, cargo=None):
        self.reader, self.entry, self.directory, self.cargo = reader, entry, directory, cargo  # directory: rel or None


def _carrier(ctx, inp, W, reader, uid, groups, waive):
    """(row, entries): the reader's declaration row (state, path, digest, subject) and its parsed entries."""
    slm = ctx.slm
    row = dict(readerId=reader, readerVersion=1, state='absent', path=None, contentSha256=None, stateSubject=None, unresolved=[])
    if reader == 'cargo-config-patch':
        names = [p for p in (_join(W, '.cargo/config.toml'), _join(W, '.cargo/config')) if _entry(inp, p) is not None]
        if len(names) == 2:
            row.update(state='refused', stateSubject='carrier-ambiguous')
            return row, None
    else:
        names = [p for p in (_join(W, 'package.json'),) if _entry(inp, p) is not None]
    if not names:
        return row, None
    path = names[0]
    row['path'] = path
    # Carrier custody: every directory from W to it (directory custody), and the carrier (config-file custody).
    for d in [x for x in _ancestors(_parent(path)) if x == W or x.startswith(W.rstrip('/') + '/')]:
        why = slm._dir_custody(_entry(inp, d), uid, waive, groups)  # the owner waiver reaches directories, never files
        if why is not None:
            row.update(state='refused', stateSubject='custody:' + why)
            return row, None
    why = slm._file_custody(_entry(inp, path), uid, False, groups)
    raw = _bytes(inp, path)
    if why is None and raw is not None and len(raw) > CARRIER_CAP:
        why = 'TOO_LARGE'
    if why is not None:
        row.update(state='refused', stateSubject='custody:' + why)
        return row, None
    raw = raw if raw is not None else b''
    row['contentSha256'] = hashlib.sha256(raw).hexdigest()
    if reader == 'cargo-config-patch':
        try:
            doc = tomllib.loads(raw.decode('utf-8'))
        except (UnicodeDecodeError, tomllib.TOMLDecodeError):
            row.update(state='refused', stateSubject='parse')
            return row, None
        patch = doc.get('patch', {})
        if not isinstance(patch, dict) or not all(isinstance(v, dict) for v in patch.values()):
            row.update(state='refused', stateSubject='parse')
            return row, None
        entries = []
        for source, table in patch.items():
            for name, spec in table.items():
                e = _Entry(reader, 'patch.%s.%s' % (source, name), cargo=(source, name))
                e.spec = spec
                entries.append(e)
        row['state'] = 'read'
        return row, entries
    try:
        doc = ctx.C.parse(raw)
    except ctx.C.AdmissionError:
        row.update(state='refused', stateSubject='parse')
        return row, None
    if not isinstance(doc, dict):
        row.update(state='refused', stateSubject='parse')
        return row, None
    if 'workspaces' not in doc:
        row['state'] = 'read'
        return row, []
    ws = doc['workspaces']
    if not isinstance(ws, list) or not all(isinstance(x, str) for x in ws):
        row.update(state='refused', stateSubject='workspaces-shape-unsupported')
        return row, None
    row['state'] = 'read'
    return row, [_Entry(reader, x) for x in ws]


def _entry_path(text):
    """(rel, None) for a canonical relative directory, else (None, reason)."""
    if text.startswith('/') or any(s == '..' for s in text.split('/')):
        return None, 'entry-path-outside-root'
    segs = text.split('/')
    if not text or any(s in ('', '.') for s in segs) or '\x00' in text or '\\' in text:
        return None, 'entry-path-grammar'
    return text, None


def _is_glob(text):
    return any(c in GLOB for c in text)


# ------------------------------------------------------------------ placement and candidates

class _Placement:
    """The placement of one entry directory D = W/<rel> (registry `placement`; law item 19 M1 and M2).

    * `absent`: D is not reached from W segment by segment as directories with no symlink (entry-path-absent).
    * `candidate`: the first directory R on the path from W to D, D included, holding a VCS marker, or None.
    * `offvolume`: a device change on the path from W to D (member-excluded, member-outside-volume); `offvolume_at_or_before
      _candidate` says whether it also places the candidate on another volume.
    * `inner`: D lies at or below a boundary strictly inside its candidate (a nested repository or `opensip.json` project
      of the member, LD-B3B0-7), or at or below a pruned anchor (r2, B3B0REF-R1-RF-1): the walk never enters a pruned
      tree (the shared rule over the Cargo roots seen so far, with SX-1 at W and at the candidate), so nothing below it
      is consulted, no provider in it is read, and D is in no member's analyzed tree.
    No depth limit applies to D; M1's bound is the candidate's (r2, B3B0REF-R1-RF-4)."""

    def __init__(self):
        self.absent, self.candidate, self.offvolume, self.offvolume_at_or_before_candidate, self.inner = False, None, False, False, False


def _place(ctx, inp, W, rel):
    out = _Placement()
    dev = (_entry(inp, W) or {}).get('dev')
    cargo = {''} if (_entry(inp, _join(W, 'Cargo.toml')) or {}).get('kind') == 'file' else set()
    parts = rel.split('/')
    d = W
    for i, part in enumerate(parts):
        prefix = '/'.join(parts[:i + 1])
        members = (out.candidate,) if out.candidate is not None else ()
        if ctx.rule.classify_path(prefix, cargo, members) is not None:
            out.inner = True  # a pruned anchor: never entered, nothing below it consulted
            return out
        d = _join(d, part)
        e = _entry(inp, d)
        if e is None or e.get('kind') != 'dir':
            out.absent = True
            return out
        if e.get('dev') != dev and not out.offvolume:
            out.offvolume = True
            out.offvolume_at_or_before_candidate = out.candidate is None
        if out.candidate is None:
            if _markers(inp, d):
                out.candidate = prefix
                if out.offvolume:
                    out.offvolume_at_or_before_candidate = True
        elif _markers(inp, d) or (_entry(inp, _join(d, 'opensip.json')) or {}).get('kind') == 'file':
            out.inner = True
        if (_entry(inp, _join(d, 'Cargo.toml')) or {}).get('kind') == 'file':
            cargo.add(prefix)
    return out


def _visible_repositories(ctx, inp, W):
    """The repositories a downward walk from W can lawfully see (r3, B3B0REF-R2-RF-1), for classifying npm globs: the
    walk lists ordinary directories parent-first to 256 segments, never enters a pruned anchor (the shared rule over the
    Cargo roots seen so far, SX-1 at W), and records a directory holding a VCS marker, or a nested `opensip.json`
    project, as a boundary without entering it. Nothing below an anchor or a boundary is consulted."""
    children = {}
    for q in inp['fs']:  # the directory listings; an entry's metadata is consulted only through `_entry`
        if q != '/':
            children.setdefault(_parent(q), []).append(q)
    cargo = {''} if (_entry(inp, _join(W, 'Cargo.toml')) or {}).get('kind') == 'file' else set()
    repos, queue = [], [(W, 0)]
    while queue:
        d, depth = queue.pop(0)
        for c in sorted(children.get(d, [])):
            rel = _rel(W, c)
            if ctx.rule.classify_path(rel, cargo, ()) is not None:
                continue  # a pruned anchor: never entered or consulted
            if (_entry(inp, c) or {}).get('kind') != 'dir' or depth + 1 > MAX_DEPTH:
                continue
            if _markers(inp, c):
                repos.append(rel)  # a nested repository: a boundary, seen but never entered
                continue
            if (_entry(inp, _join(c, 'opensip.json')) or {}).get('kind') == 'file':
                continue  # a nested project: a boundary, never entered
            if (_entry(inp, _join(c, 'Cargo.toml')) or {}).get('kind') == 'file':
                cargo.add(rel)
            queue.append((c, depth + 1))
    return repos


def _candidate_failure(ctx, inp, W, cand):
    """The placement verdict of candidate R (rel), before 6b: None when admissible, else (kind, subject). kind is
    'boundary' (the repository cannot become a member: a crossing SLM refuses in branch A, member-excluded in branch B)
    or 'placement' (branch A refuses, law item 24 row 2; branch B excludes)."""
    R = _join(W, cand)
    parts = cand.split('/')
    for i in range(1, len(parts)):
        between = _join(W, '/'.join(parts[:i]))
        if (_entry(inp, _join(between, 'opensip.json')) or {}).get('kind') == 'file':
            return 'boundary', 'JOIN_CROSSES_NESTED_PROJECT'
    if len(parts) > MAX_DEPTH:
        return 'placement', 'DEPTH'  # M1, at the candidate (r2, B3B0REF-R1-RF-4): S3's existing depth subject
    markers = _markers(inp, R)
    names = [m for m, _ in markers]
    if names != ['.git']:
        return 'placement', 'member-vcs-unsupported:vcs-other'
    if not markers[0][1]:
        return 'placement', 'member-vcs-unsupported:git-not-directory'
    return None


def _six_b(inp, W, cand, uid, groups, slm, waive):
    """Directory custody of every directory from W's child to R (the owner waiver, when given, applies to member
    directories), then item 6b's supplied verdict: None, ('custody', path, code) or ('6b', R, subject)."""
    R = _join(W, cand)
    parts = cand.split('/')
    for i in range(1, len(parts) + 1):
        d = _join(W, '/'.join(parts[:i]))
        why = slm._dir_custody(_entry(inp, d), uid, waive, groups)
        if why is not None:
            return 'custody', d, why
    verdict = inp.get('memberObservations', {}).get(R, 'admitted')
    return None if verdict == 'admitted' else ('6b', R, verdict)


def _gitlinks(inp, W, cand):
    """(r4) The W-relative index gitlinks item 6b reports with its admission of candidate R, from `memberGitlinks`."""
    return [cand + '/' + g for g in inp.get('memberGitlinks', {}).get(_join(W, cand), [])]


# ------------------------------------------------------------------ links

def _manifest(ctx, inp, path, uid, groups):
    """(doc, None) or (None, subject) for a provider manifest read as data under config-file custody."""
    e = _entry(inp, path)
    if e is None:
        return None, 'absent'
    why = ctx.slm._file_custody(e, uid, False, groups)
    if why is not None:
        return None, 'custody:' + why
    raw = _bytes(inp, path) or b''
    try:
        if path.endswith('.toml'):
            return tomllib.loads(raw.decode('utf-8')), None
        doc = ctx.C.parse(raw)
        return (doc, None) if isinstance(doc, dict) else (None, 'parse')
    except (UnicodeDecodeError, tomllib.TOMLDecodeError, ctx.C.AdmissionError):
        return None, 'parse'


def _link(ctx, inp, W, e, member, uid, groups):
    """('link', row) or ('unresolved', reason, subject)."""
    d = _join(W, e.directory)
    if e.reader == 'cargo-config-patch':
        doc, why = _manifest(ctx, inp, _join(d, 'Cargo.toml'), uid, groups)
        if doc is None:
            return 'unresolved', 'link-manifest-unusable', why
        pkg = doc.get('package')
        if not isinstance(pkg, dict) or not isinstance(pkg.get('name'), str):
            return 'unresolved', 'link-manifest-unusable', 'name-absent'
        if pkg['name'] != e.cargo[1]:
            return 'unresolved', 'patch-target-name-mismatch', None
        if not isinstance(pkg.get('version'), str):
            return 'unresolved', 'provided-version-unusable', None
        return 'link', dict(ecosystem='cargo', packageName=e.cargo[1], providerMember=member, packageDir=e.directory,
                            providedVersion=pkg['version'], cargoPatchSource=e.cargo[0], declaredBy=e.reader)
    doc, why = _manifest(ctx, inp, _join(d, 'package.json'), uid, groups)
    if doc is None:
        return 'unresolved', 'link-manifest-unusable', why
    if not isinstance(doc.get('name'), str):
        return 'unresolved', 'link-manifest-unusable', 'name-absent'
    if not isinstance(doc.get('version'), str):
        return 'unresolved', 'provided-version-unusable', None
    return 'link', dict(ecosystem='npm', packageName=doc['name'], providerMember=member, packageDir=e.directory,
                        providedVersion=doc['version'], declaredBy=e.reader)


# ------------------------------------------------------------------ discovery

# The D9 branch of the D15 member cap, which SLM's map predates: PROJECT.SCOPE_LIMIT is request-rejected, exit 2,
# REQUEST.UNSATISFIABLE (law M3-B item 24 row 5; B-S1 DiscoveryD9V1; security S12).
D9_SCOPE_LIMIT = {'class': 'request-rejected', 'exit': 2, 'code': 'REQUEST.UNSATISFIABLE'}


def _refuse(slm, prov, code, path, detail):
    d9 = D9_SCOPE_LIMIT if code == 'PROJECT.SCOPE_LIMIT' else slm.d9(code)
    return {'status': 'REFUSE', 'refusal': code, 'path': path, 'detail': detail, 'd9': d9, 'provenance': prov}


def _within(rel, base):
    """rel is at or below base; every path is below the empty base (W itself)."""
    return base == '' or rel == base or rel.startswith(base + '/')


def discover(ctx, inp):
    """The current discovery with D15. Returns (result, links): `result` a DiscoveryResultV3, `links` the declaration
    half of the link set (typed rows, plan r2 LD-B3B-3)."""
    slm, rule, b2b0 = ctx.slm, ctx.rule, ctx.b2b0
    base = {k: v for k, v in inp.items() if k not in SIDE}
    base['fs'] = _project_vcs(inp)  # r2 (RF-3): one VCS representation for SLM, placement and boundaries
    inp = dict(inp, fs=base['fs'])
    _member_gitlinks(inp)  # r4: an inconsistent index observation refuses before discovery
    first = slm.discovery(copy.deepcopy(base))
    prov1 = first['provenance']
    W, source = prov1.get('selectedRoot'), prov1.get('unitSource')
    if W is None or source is None:
        # Selection refused before a root existed: there is no W, so no carrier is observed at W (LD-B3B0-4).
        return _complete(b2b0, first, [], [], absent_rows()), []
    uid, groups = inp['invokingUid'], set(inp.get('authorizedGroupIds', []))
    # --trust-project-owner (with explicit --project W) waives the owner check on member directories only, never on
    # member Git evidence (law item 23): the waiver reaches directory custody here, and 6b's verdict is supplied.
    waive = bool(inp.get('trustProjectOwner', False)) and first['provenance'].get('mode') == 'explicit'
    w2 = not any(_markers(inp, a) for a in _ancestors(W))
    array = inp.get('explicitJoins') or inp.get('configWorkspaceRoots') or []
    array_source = 'explicit-joins' if inp.get('explicitJoins') else 'config-workspace-roots'

    rows, entries = {}, {}
    for reader in READERS:
        rows[reader], entries[reader] = _carrier(ctx, inp, W, reader, uid, groups, waive)
    unresolved = {r: [] for r in READERS}
    decided = {r: set() for r in READERS}

    def disclose(e, reason, subject=None):
        if e.entry in decided[e.reader]:
            return
        decided[e.reader].add(e.entry)
        unresolved[e.reader].append(dict(entry=e.entry, reason=reason, subject=subject))

    # Every entry's shape and placement.
    placed = []  # entries that reached their directory; each carries its _Placement
    visible = None  # the lawfully visible repositories, computed once for the first glob
    for reader in READERS:
        seen = set()
        for e in entries[reader] or []:
            if e.entry in seen:
                continue
            seen.add(e.entry)
            if reader == 'cargo-config-patch':
                spec = e.spec
                if not (isinstance(spec, dict) and set(spec) == {'path'} and isinstance(spec['path'], str)):
                    if w2:
                        disclose(e, 'patch-entry-not-path')
                    else:
                        decided[reader].add(e.entry)
                    continue
                text = spec['path']
            else:
                text = e.entry
                if _is_glob(text):
                    if w2:
                        lit = []
                        for seg in text.split('/'):
                            if any(c in GLOB for c in seg):
                                break
                            lit.append(seg)
                        prefix = '/'.join(lit)
                        if visible is None:
                            visible = _visible_repositories(ctx, inp, W)
                        crosses = any(_within(r, prefix) or (prefix and _within(prefix, r)) for r in visible)
                        if crosses:
                            disclose(e, 'workspace-glob-crosses-repository')
                        else:
                            decided[reader].add(e.entry)
                    else:
                        decided[reader].add(e.entry)
                    continue
            rel, why = _entry_path(text)
            if why is not None:
                if w2:
                    disclose(e, why)
                else:
                    decided[reader].add(e.entry)
                continue
            pl = _place(ctx, inp, W, rel)
            if pl.absent:
                if w2:
                    disclose(e, 'entry-path-absent')
                else:
                    decided[reader].add(e.entry)
                continue
            e.directory, e.placement = rel, pl
            placed.append(e)

    members, declared_by, links = [], {}, []
    if not w2:
        # Root in a repository: readers declare nothing and derive no link. A literal entry inside a nested repository
        # is disclosed; no other entry is recorded (law item 24 row 6). The array's crossing refuses in SLM (row 3).
        for e in placed:
            if e.placement.candidate is not None:
                disclose(e, 'member-excluded', 'workspace-root-inside-repository')
            else:
                decided[e.reader].add(e.entry)
        return _finish(ctx, inp, base, first, [], {}, rows, unresolved, [])

    def refused(code, path, detail):
        # A refusal decided by the member rules carries the provenance of the discovery without members: what the
        # walker observed up to the decision, with the readers' rows (LD-B3B0-5).
        plain, _ = _finish(ctx, inp, base, first, [], {}, rows, unresolved, [])
        return _refuse(slm, plain['provenance'], code, path, detail), []

    gitlinks = []  # r4: the admitted members' index gitlinks, W-relative
    if array:
        # Branch A (r4, plan amendment A4-2): the members are decided before any walk, so item 6b's index gitlinks
        # bound every descent. Public priority: the array's size, then grammar for the whole array, then the member
        # rules in path order, then the walk's refusals (this replaces r2's SLM-first order, LD-B3B0-6).
        #
        # 1. The array gate: pure, no observation, no walk, no member decided. It returns SLM's own records for its
        #    first two array checks (`_explicit_units`), with SLM's D9, and the provenance of the discovery without
        #    members (LD-B3B0-5); that walk supplies only the provenance, never the verdict.
        too_many = 'TOO_MANY_JOINS' if array_source == 'explicit-joins' else 'TOO_MANY_WORKSPACE_ROOTS'
        if len(array) > slm.MAX_EXPLICIT_JOINS:
            return refused('PROJECT.EXPLICIT_PATH_INVALID', None, too_many)
        for spec in array:
            try:
                rule.normalize_explicit_root(spec)
            except (rule.RootGrammarError, TypeError):
                return refused('PROJECT.EXPLICIT_PATH_INVALID', spec if isinstance(spec, str) else None, 'JOIN_PATH_GRAMMAR')
        # 2. The member decisions, in path order, each stopping at the first refusal: placement and other volumes
        #    (row 2), then the cap (row 5), then directory custody and item 6b per candidate (row 2). The placement
        #    lookups that form and count the candidates precede them (A4-2 step 2); nothing is listed, judged or read
        #    below a candidate before its admission. A candidate behind a nested project (LD-B3B0-7's boundary kind)
        #    stays withheld: a root inside it refuses in the walk.
        cands, offvolume = {}, {}
        for spec in array:
            rel = rule.normalize_explicit_root(spec)
            if not rel:
                continue
            pl = _place(ctx, inp, W, rel)
            if pl.absent or pl.candidate is None:
                continue
            cands.setdefault(pl.candidate, []).append(dict(source=array_source, path=_join(W, rel)))
            if pl.offvolume:
                offvolume.setdefault(pl.candidate, _join(W, rel))
        provisional = [c for c in sorted(cands, key=lambda c: c.encode())
                       if (_candidate_failure(ctx, inp, W, c) or ('',))[0] != 'boundary']
        for cand in provisional:
            bad = _candidate_failure(ctx, inp, W, cand)
            if bad is not None:
                return refused('PROJECT.ROOT_CUSTODY_REFUSED', _join(W, cand), bad[1])
            if cand in offvolume:
                return refused('PROJECT.ROOT_CUSTODY_REFUSED', offvolume[cand], 'member-outside-volume')
        if len(provisional) > MAX_MEMBERS:
            return refused('PROJECT.SCOPE_LIMIT', W, 'members:%d>%d' % (len(provisional), MAX_MEMBERS))
        for cand in provisional:
            why = _six_b(inp, W, cand, uid, groups, slm, waive)
            if why is not None:
                return refused('PROJECT.ROOT_CUSTODY_REFUSED', why[1], why[2])
            members.append(cand)
            declared_by[cand] = cands[cand]
            gitlinks += _gitlinks(inp, W, cand)
        # 3. The walk, once, with the admitted members entered and their gitlinks as nested repositories: absence,
        #    crossings (gitlinks included), pruned trees and chain custody, in SLM's array order. Its refusal is the
        #    result, with no members and the declaration rows as they stand.
        walk, _ = _finish(ctx, inp, base, first, members, declared_by, rows, unresolved, [], gitlinks)
        if walk['status'] != 'ACCEPT':
            plain = walk['provenance']
            plain['memberRepositories'], plain['memberConfigs'] = [], []
            return walk, []
        # Readers declare nothing; they link into array members only.
        for e in placed:
            cand = e.placement.candidate
            if e.placement.offvolume:
                disclose(e, 'member-excluded', 'member-outside-volume')
            elif cand is None:
                disclose(e, 'entry-not-in-a-member')
            elif cand not in members:
                disclose(e, 'dropped-workspace-roots-present')
    else:
        # Branch B: the readers declare members by placement alone (registry membershipByPlacementOnly).
        cands = {}
        for e in placed:
            pl = e.placement
            if pl.offvolume:
                continue  # an entry with a device change declares nothing (registry `placement`)
            if pl.candidate is not None:
                cands.setdefault(pl.candidate, []).append(e)
        offvol = {e.placement.candidate for e in placed if e.placement.offvolume and e.placement.offvolume_at_or_before_candidate and e.placement.candidate}
        placed_ok, excluded = [], {}
        for cand in sorted(set(cands) | offvol, key=lambda c: c.encode()):
            bad = _candidate_failure(ctx, inp, W, cand)
            if cand in offvol:
                excluded[cand] = 'member-outside-volume'
            elif bad is None:
                placed_ok.append(cand)
            else:
                excluded[cand] = bad[1]  # fails placement: not counted, excluded, disclosed
        if len(placed_ok) > MAX_MEMBERS:
            return refused('PROJECT.SCOPE_LIMIT', W, 'members:%d>%d' % (len(placed_ok), MAX_MEMBERS))  # row 5, either branch
        for cand in placed_ok:
            why = _six_b(inp, W, cand, uid, groups, slm, waive)
            if why is not None:
                excluded[cand] = ('DIRECTORY_CUSTODY:' + why[2]) if why[0] == 'custody' else why[2]
            else:
                members.append(cand)
                gitlinks += _gitlinks(inp, W, cand)
        for e in placed:
            cand = e.placement.candidate
            if e.placement.offvolume:
                disclose(e, 'member-excluded', 'member-outside-volume')
            elif cand is None:
                disclose(e, 'entry-not-in-a-member')
            elif cand in excluded:
                disclose(e, 'member-excluded', excluded[cand])
            else:
                declared_by.setdefault(cand, [])
                row = rows[e.reader]
                decl = dict(source='reader', readerId=e.reader, readerVersion=1, path=row['path'], contentSha256=row['contentSha256'])
                if decl not in declared_by[cand]:
                    declared_by[cand].append(decl)

    # Links: only after membership is final, only inside admitted members, and never from a directory the member's
    # analyzed tree excludes (an inner boundary or a pruned anchor, LD-B3B0-7; r2, RF-1): nothing there is read.
    # (r4) A directory at or below an admitted member's index gitlink is inside that nested repository.
    candidates = []
    for e in placed:
        cand = e.placement.candidate
        if e.entry in decided[e.reader] or cand not in members:
            continue
        if e.placement.inner or any(_within(e.directory, g) for g in gitlinks):
            disclose(e, 'entry-not-in-a-member')
            continue
        out = _link(ctx, inp, W, e, _join(W, cand), uid, groups)
        if out[0] == 'link':
            candidates.append((e, out[1]))
        else:
            disclose(e, out[1], out[2])
    for eco in ('cargo', 'npm'):
        by_name = {}
        for e, row in candidates:
            if row['ecosystem'] == eco:
                by_name.setdefault(row['packageName'], []).append((e, row))
        for name, group in by_name.items():
            if len({row['packageDir'] for _, row in group}) > 1:
                for e, _ in group:
                    disclose(e, 'ambiguous-provider')
            else:
                for e, row in group:
                    decided[e.reader].add(e.entry)
                    if row not in links:
                        links.append(row)
    for e in placed:
        decided[e.reader].add(e.entry)  # every remaining entry declared a member or linked: not recorded
    # The final record: in branch A the same pass two as step 3's walk (the reference recomputes it with the final rows).
    return _finish(ctx, inp, base, first, members, declared_by, rows, unresolved, links, gitlinks)


def absent_rows():
    return [dict(readerId=r, readerVersion=1, state='absent', path=None, contentSha256=None, stateSubject=None, unresolved=[]) for r in READERS]


def _declaration_rows(rows, unresolved):
    out = []
    for r in READERS:
        row = copy.deepcopy(rows[r])
        if row['state'] == 'read':
            row['unresolved'] = sorted(unresolved[r], key=lambda u: u['entry'].encode())
        out.append(row)
    return out


def _complete(b2b0, result, members, configs, declarations):
    out = b2b0.project_v3(result)
    out.pop('pendingFields', None)
    prov = out['provenance']
    prov['memberRepositories'] = members
    prov['memberConfigs'] = configs
    prov['workspaceDeclarations'] = declarations
    return out


def _finish(ctx, inp, base, first, members, declared_by, rows, unresolved, links, gitlinks=()):
    """Pass two with members entered as ordinary directories, then the complete V3 result."""
    slm, b2b0 = ctx.slm, ctx.b2b0
    W, source = first['provenance']['selectedRoot'], first['provenance']['unitSource']
    hidden = copy.deepcopy(base)
    configs = []
    for m in members:
        R = _join(W, m)
        hidden['fs'][R] = {k: v for k, v in hidden['fs'][R].items() if k != 'vcs'}
        cfg = _join(R, 'opensip.json')
        if hidden['fs'].get(cfg, {}).get('kind') == 'file':
            configs.append(cfg)
            del hidden['fs'][cfg]  # a member's own opensip.json: not a nested project, never read (law item 22)
    for g in gitlinks:
        # (r4) An admitted member's index gitlink that is a directory is a nested repository (law items 21 and 22):
        # SLM's one boundary representation, so the walk never enters it, records it in `nestedRepositories`, and an
        # exact root at or below it refuses JOIN_CROSSES_NESTED_REPOSITORY. It is the boundary's input, not VCS
        # evidence: the result records only its path. A gitlink with no directory there bounds nothing.
        G = _join(W, g)
        if hidden['fs'].get(G, {}).get('kind') == 'dir' and not hidden['fs'][G].get('vcs'):
            hidden['fs'][G] = dict(hidden['fs'][G], vcs=True)
    bound = _BoundRule(ctx.rule, sorted(members, key=lambda s: s.encode()))
    saved = slm.DD
    slm.DD = bound
    try:
        downward = b2b0.walker_population(_PopulationRule(ctx.rule, bound._members), hidden, W, source)
        second_input = dict(downward, fs={**b2b0.upward_evidence(base, first), **downward['fs']}, cwd=W)
        second = slm.discovery(copy.deepcopy(second_input))
    finally:
        slm.DD = saved
    p2 = second['provenance']
    if p2.get('selectedRoot') != W or p2.get('unitSource') != source:
        raise ValueError('pass two changed the selected root or unit source')
    for field in b2b0.UPWARD_FIELDS:
        p2[field] = copy.deepcopy(first['provenance'][field])
    member_rows = [dict(path=_join(W, m), declaredBy=sorted(declared_by.get(m, []), key=lambda d: (d['source'], d['path'])))
                   for m in sorted(members, key=lambda s: _join(W, s).encode())]
    result = _complete(b2b0, second, member_rows, sorted(configs, key=lambda s: s.encode()), _declaration_rows(rows, unresolved))
    return result, sorted(links, key=lambda r: (r['ecosystem'], r['packageName'].encode(), r['packageDir'].encode()))


def boundary_inventory_v3(ctx, result):
    """The complete AdmittedBoundaryInventoryV3 of an ACCEPTed result."""
    if result.get('status') != 'ACCEPT':
        raise ValueError('BOUNDARY_INVENTORY_REQUIRES_ACCEPT')
    return ctx.rule.boundary_inventory_from_provenance(result['provenance'])
