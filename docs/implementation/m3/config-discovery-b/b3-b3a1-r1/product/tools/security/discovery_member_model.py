"""The D15 cost terms of the T2 census (M3-B r9 item 12; unit B3-b3a1, B3-b plan r2 sections 4.1 and 4.2, amendment A5).

Developer tool module, loaded by tools/security/discovery_census.py, which verifies the cost closure and reads every
constant this module uses by its anchor (`c`). It adds three terms to the walker model, each separate, each charge in
exactly one (plan amendment A2-3 step 4):
  * the reader term, paid at n = 0: the carriers' lookups, directory and file custody, bounded reads and their
    post-read checks, and the declaration rows;
  * the member term, at n members: placement, the visible-repository listing, candidate checks, member custody, item 6b
    (the member session's pass-level sources once, then each member's layout) and the provider-manifest reads for links.
    Placement and listing are paid at n = 0 over the declaring entries and the listed population;
  * member descent: the composition walk's binding records (one per observed path not already bound), with the walk over
    admitted members and their gitlinks in the walker model itself.

The bound is the ledger's (item 12; plan amendment A5-3): what the native code charges. The decision core's parses are
not charged, so no term has a parse component; item 6b's config parse and index decode are charged, and the member term
carries them. `Native` mirrors workspace_observation.rs's `NativeObservation` charge by charge: the reused directory
stack, one owned record per new binding in the shared table, the per-phase memo of entries and custody entries, the
custody capture at its dearer branch (always taken, and the larger of its ACL record and the premise check), the bounded
read at its envelope with the post-read status and capture, and each kept-read copy. `Member` mirrors git_tracking.rs's
item 6b at its ceilings: every member admitted with `.git`, its config at 64 KiB and its index at 4 MiB. `decide` mirrors
workspace_declarations.rs's phase one, branch A and the link stage over a census tree, so the requests and their order
are the core's. Unknowns take their dearer branch: custody passes, ACLs are captured, item 6b admits, no gitlinks bound
the walk. Bytes are affine in the root spelling's length R; these terms keep no root spelling (perRootByte 0).
"""
import json
import tomllib

READERS = ('cargo-config-patch', 'npm-workspaces-members')
VCS = ('.git', '.hg', '.svn', '.jj')
GLOB = set('*?[]{}!')


def blen(text):
    return len(text.encode())


def join(parent, name):
    return parent + '/' + name if parent else name


def parent_of(rel):
    return rel.rsplit('/', 1)[0] if '/' in rel else ''


class Cost:
    """One term's accumulator: (objects, edges, bytes, perRootByte)."""

    def __init__(self):
        self.v = [0, 0, 0, 0]

    def add(self, cost, times=1):
        cost = tuple(cost) + (0,) * (4 - len(cost))
        for i in range(4):
            self.v[i] += cost[i] * times

    def tuple(self):
        return tuple(self.v)


def read_envelope(c, length, cap):
    """`read_charged` over a regular file of `length` bytes, capped at `cap`, under the D15 terms' explicit read-retry
    envelope (law M3-B r9 item 12): POSIX regular-file reads, uninterrupted, so each attempt fills the buffer's free
    space or reaches end of file (interrupted retries are excluded, as the B2-b4 census excludes them). Every D15 read is
    of a regular file opened no-follow (custody requires it). One object; one edge per attempt: each growth's attempt,
    and the end-of-file attempt unless the ceiling (cap + 1) is reached first; and every growth's full requested size.
    The walker's B2-b4 envelope (one byte per attempt) is unchanged for its own reads."""
    ceiling = cap + 1
    used = size = grown = attempts = 0
    while used != ceiling:
        if used == size:
            size = min(c['CHUNK'] if size == 0 else size * c['GROWTH'], ceiling)
            grown += size
        attempts += 1
        available = min(length, size) - used
        if available == 0:
            break  # end of file: the attempt returns 0
        used += available
    return (c['READ_OBJECT'], c['READ_ATTEMPT_EDGE'] * attempts, grown, 0)


class Ledger:
    """The three terms, and the binding table shared by the decision phases and the walk."""

    def __init__(self):
        self.terms = {'reader': Cost(), 'member': Cost(), 'descent': Cost()}
        self.bound = set()


class Native:
    """One decision phase's native observation (`NativeObservation`) over a census tree, charging `ledger.terms[term]`
    for each request made while `term` is current."""

    def __init__(self, c, tree, ledger):
        self.c, self.t, self.ledger = c, tree, ledger
        self.term = 'reader'
        self.stack = []  # the opened directory paths, W excluded
        self.seen, self.custodied, self.read, self.files = {}, {}, {}, set()
        self.session = None

    def add(self, cost, times=1):
        self.ledger.terms[self.term].add(cost, times)

    def owned(self, length):
        o, e = self.c['OWNED']
        self.add((o, e, length + self.c['RECORD'], 0))

    def bind(self, rel):
        if rel not in self.ledger.bound:
            self.owned(blen(rel) + self.c['DESCRIPTOR_METADATA'])
            self.ledger.bound.add(rel)

    def status(self):
        self.add(self.c['STATUS'])

    def open_dir(self, name):
        o, e, b = self.c['OPEN_DIR']
        self.add((o, e, b + blen(name), 0))

    def obs(self, name):
        o, e, b = self.c['OBS']
        self.add((o, e, b + blen(name), 0))

    def open_regular(self, name):
        o, e, b = self.c['OPEN_REG_1']
        self.add((o, e, b + blen(name), 0))

    def capture(self):
        """`capture`: the platform capture, then the larger of the ACL entries' record (at MAX_ENTRIES) and the
        premise's filesystem check."""
        self.add(self.c['CAP'])
        o, e = self.c['OWNED']
        acl = (o, e, self.c['MAX_ENTRIES'] * self.c['ACL_ENTRY'] + self.c['RECORD'], 0)
        self.add(tuple(max(x, y) for x, y in zip(acl, self.c['FS'])))

    def directory(self, rel):
        """`directory`: reuse the stack's common prefix, open and bind the rest; None when a component is not a
        directory (nothing past it is opened)."""
        if rel == '':
            return True
        parts = rel.split('/')
        keep = 0
        while keep < min(len(parts), len(self.stack)) and self.stack[keep] == '/'.join(parts[:keep + 1]):
            keep += 1
        del self.stack[keep:]
        for depth in range(keep, len(parts)):
            path = '/'.join(parts[:depth + 1])
            self.open_dir(parts[depth])
            if self.t.kind(path) != 'dir':
                return None
            self.status()
            self.bind(path)
            self.stack.append(path)
        return True

    def observe(self, rel):
        if rel == '':
            self.status()
            self.bind('')
            return dict(kind='dir')
        if self.directory(parent_of(rel)) is None:
            return None
        self.obs(rel.rsplit('/', 1)[-1])
        node = self.t.node(rel)
        if node is None:
            return None
        self.bind(rel)
        self.owned(blen(rel) + self.c['ENTRY'])
        return node

    def entry(self, rel):
        if rel not in self.seen:
            self.seen[rel] = self.observe(rel)
        return self.seen[rel]

    def custody_entry(self, rel):
        """`custody_entry` at its dearer branch: the judgment needs the ACL, so it is captured from the bound object."""
        if rel in self.custodied:
            return self.custodied[rel]
        node = self.entry(rel)
        if node is not None:
            if node['kind'] == 'dir':
                self.directory(rel)
            else:
                self.directory(parent_of(rel))
                self.open_regular(rel.rsplit('/', 1)[-1])
                self.files.add(rel)
            self.capture()
        self.custodied[rel] = node
        return node

    def markers(self, rel):
        if self.directory(rel) is None:
            return []
        found = []
        for marker in VCS:
            self.obs(marker)
            m = join(rel, marker)
            if self.t.node(m) is not None:
                self.bind(m)
                found.append((marker, self.t.kind(m) == 'dir'))
        return found

    def children(self, rel):
        self.add(self.c['LISTING'])
        if self.directory(rel) is None:
            return []
        names = self.t.children.get(rel, [])
        self.add(self.c['VISIT'], len(names) + 2)
        o, e, two, records = self.c['CONVERTED_NAME']
        for name in names:
            self.add((o, e, two * (blen(rel) + 1 + blen(name)) + records * self.c['RECORD'], 0))
        return list(names)

    def bytes(self, rel):
        """`bytes`: a kept read's charged copy, or the custody-bound read at its envelope, its post-read status and
        capture, and the kept record."""
        size = self.t.node(rel).get('size', 0)
        if rel in self.read:
            self.owned(size)
            return self.read[rel]
        self.add(read_envelope(self.c, min(size, self.c['CARRIER_CAP'] + 1), self.c['CARRIER_CAP']))
        self.status()
        self.capture()
        self.owned(blen(rel) + size)
        self.read[rel] = self.t.node(rel).get('text', '')
        return self.read[rel]

    def member_verdict(self, member_model, candidate):
        if self.session is None:
            self.session = True
            member_model.begin(self)
        for path in member_model.observe_identified(self, candidate):
            self.bind(path)
        return True


class Member:
    """Item 6b (`MemberSession`) at its ceilings, charged on the current phase's term."""

    def __init__(self, c, environment, sources, home_sources=True):
        self.c = c
        self.environment = environment  # (entries, bytes) of the process environment
        self.sources = tuple(sources)  # the fixed system sources: SYSTEM_SOURCES in production, a test's own
        self.home_sources = home_sources

    def judge(self, n):
        """`judge_decided`: the capture, then the premise check (its dearer branch)."""
        n.add(self.c['CAP'])
        n.add(self.c['FS'])

    def judge_file(self, n):
        n.add(self.c['FS'])
        self.judge(n)
        n.add(self.c['GIT_STATUS'])

    def config(self, n, cap):
        """A capped read at its dearer branch (one byte past the cap: the most attempts and the final buffer), then the
        charged parse at the cap (`config_decided`: one object, one edge, the config's length)."""
        n.add(read_envelope(self.c, cap + 1, cap))
        n.add((1, 1, cap, 0))

    def begin(self, n):
        """`MemberSession::begin`: the environment check, the global sources under H and the fixed system sources,
        each present, admitted and at its cap."""
        entries, total = self.environment
        n.add((0, max(entries, 1), total, 0))
        cap = self.c['CONFIG_CAP']
        if self.home_sources:
            for name in ('.gitconfig',):
                n.open_regular(name)
                n.add(self.c['FS'])
                self.judge(n)
                n.add(self.c['GIT_STATUS'])
                self.config(n, cap)
            for name in ('.config', 'git'):
                n.open_dir(name)
                n.add(self.c['FS'])
                self.judge(n)
                n.add(self.c['GIT_STATUS'])
            n.open_regular('config')
            n.add(self.c['FS'])
            self.judge(n)
            n.add(self.c['GIT_STATUS'])
            self.config(n, cap)
        for source in self.sources:
            o, e, b = self.c['OPEN_FIXED']  # `open_fixed_regular_following_cost`: + |path|
            n.add((o, e, b + blen(source), 0))
            self.config(n, cap)
        n.add(self.c['GIT_STATUS'])  # W's status, for the session's device

    def observe_identified(self, n, candidate):
        """`observe_identified` for one admitted member: the reserved identity list, each directory from W's child to M
        opened, sampled, recorded and checked for markers, then the layout at its ceilings. Returns the identities."""
        parts = candidate.split('/')
        slots = len(parts) + self.c['GIT_IDENTITIES']
        n.owned(slots * self.c['IDENTITY_SLOT'])
        identities = []
        for i, part in enumerate(parts):
            n.open_dir(part)
            n.add(self.c['GIT_STATUS'])
            prefix = '/'.join(parts[:i + 1])
            n.owned(blen(prefix))
            identities.append(prefix)
            for marker in VCS:
                n.obs(marker)
        git = candidate + '/.git'
        n.open_dir('.git')
        n.add(self.c['FS'])
        self.judge(n)
        n.add(self.c['GIT_STATUS'])
        for linked in ('commondir', 'config.worktree'):
            n.obs(linked)
        n.open_regular('config')
        self.judge_file(n)
        self.config(n, self.c['CONFIG_CAP'])
        n.open_regular('index')
        self.judge_file(n)
        n.add(read_envelope(self.c, self.c['INDEX_CAP'] + 1, self.c['INDEX_CAP']))
        for path in (git, git + '/config', git + '/index'):
            n.owned(blen(path))
            identities.append(path)
        n.add((1, 1, 2 * self.c['INDEX_CAP'], 0))  # the decode: twice the index's length
        return identities


# ------------------------------------------------------------------ the decision core's requests

class Entry:
    def __init__(self, reader, entry, cargo_path=None, cargo=None):
        self.reader, self.entry, self.cargo_path, self.cargo = reader, entry, cargo_path, cargo
        self.directory = self.placement = None


def entry_path(text):
    if text.startswith('/') or any(s == '..' for s in text.split('/')):
        return None
    if not text or any(s in ('', '.') for s in text.split('/')) or '\x00' in text or '\\' in text:
        return None
    return text


def carrier(n, reader):
    """`carrier`: the lookups, directory and file custody up to W, the bounded read, and the parsed entries (the
    parse is not charged)."""
    names = [p for p in (('.cargo/config.toml', '.cargo/config') if reader == READERS[0] else ('package.json',))
             if n.entry(p) is not None]
    if len(names) != 1:
        return None
    path = names[0]
    directory = parent_of(path)
    while True:
        n.custody_entry(directory)
        if directory == '':
            break
        directory = parent_of(directory)
    n.custody_entry(path)
    if n.t.node(path).get('size', 0) > n.c['MAX_CONFIG_BYTES']:
        return None  # custody refuses an oversize carrier on its size, before any read
    raw = n.bytes(path)
    if raw is None:
        return None  # not UTF-8: the parse refuses
    try:
        if reader == READERS[0]:
            doc = tomllib.loads(raw)
            patch = doc.get('patch', {})
            if not isinstance(patch, dict) or not all(isinstance(t, dict) for t in patch.values()):
                return None
            out = []
            for source, table in patch.items():
                for name, spec in table.items():
                    path_spec = spec.get('path') if isinstance(spec, dict) and set(spec) == {'path'} and isinstance(spec.get('path'), str) else None
                    out.append(Entry(reader, 'patch.%s.%s' % (source, name), path_spec, (source, name)))
            return out
        doc = json.loads(raw)
    except (ValueError, tomllib.TOMLDecodeError, UnicodeDecodeError):
        return None
    if not isinstance(doc, dict):
        return None
    items = doc.get('workspaces', [])
    if not isinstance(items, list) or not all(isinstance(x, str) for x in items):
        return None
    return [Entry(reader, x) for x in items]


class Placement:
    def __init__(self):
        self.absent, self.candidate, self.inner = False, None, False


def place(n, rule, rel):
    out = Placement()
    n.entry('')
    cargo = {''} if (n.entry('Cargo.toml') or {}).get('kind') == 'file' else set()
    parts = rel.split('/')
    for i in range(len(parts)):
        prefix = '/'.join(parts[:i + 1])
        members = (out.candidate,) if out.candidate is not None else ()
        if rule.classify_path(prefix, cargo, members) is not None:
            out.inner = True
            return out
        node = n.entry(prefix)
        if node is None or node['kind'] != 'dir':
            out.absent = True
            return out
        if out.candidate is None:
            if n.markers(prefix):
                out.candidate = prefix
        elif n.markers(prefix) or (n.entry(join(prefix, 'opensip.json')) or {}).get('kind') == 'file':
            out.inner = True
        if (n.entry(join(prefix, 'Cargo.toml')) or {}).get('kind') == 'file':
            cargo.add(prefix)
    return out


def visible_repositories(n, rule, max_depth):
    cargo = {''} if (n.entry('Cargo.toml') or {}).get('kind') == 'file' else set()
    repos, queue = [], [('', 0)]
    while queue:
        directory, depth = queue.pop(0)
        for name in sorted(n.children(directory), key=lambda s: s.encode()):
            rel = join(directory, name)
            if rule.classify_path(rel, cargo, ()) is not None:
                continue
            node = n.entry(rel)
            if node is None or node['kind'] != 'dir' or depth + 1 > max_depth:
                continue
            if n.markers(rel):
                repos.append(rel)
                continue
            if (n.entry(join(rel, 'opensip.json')) or {}).get('kind') == 'file':
                continue
            if (n.entry(join(rel, 'Cargo.toml')) or {}).get('kind') == 'file':
                cargo.add(rel)
            queue.append((rel, depth + 1))
    return repos


def candidate_failure(n, candidate, max_depth):
    parts = candidate.split('/')
    for i in range(1, len(parts)):
        if (n.entry(join('/'.join(parts[:i]), 'opensip.json')) or {}).get('kind') == 'file':
            return 'boundary'
    if len(parts) > max_depth:
        return 'placement'
    markers = n.markers(candidate)
    if [m for m, _ in markers] != ['.git'] or not markers[0][1]:
        return 'placement'
    return None


def member_custody(n, candidate):
    parts = candidate.split('/')
    for i in range(1, len(parts) + 1):
        n.custody_entry('/'.join(parts[:i]))


def link(n, e, member):
    rel = join(e.directory, 'Cargo.toml' if e.reader == READERS[0] else 'package.json')
    if n.custody_entry(rel) is None:
        return
    if n.t.node(rel).get('size', 0) <= n.c['MAX_CONFIG_BYTES']:
        n.bytes(rel)


def decide(c, rule, tree, ledger, member_model, array=(), w2=True):
    """The decision core over `tree` with W at its root, charging each request to its term. Returns the admitted
    members (their gitlinks are none, the dearer branch for the walk), the placed entries, and the phase."""
    max_depth = c['MAX_DEPTH']
    n = Native(c, tree, ledger)
    n.term = 'reader'
    entries = {}
    for reader in READERS:
        entries[reader] = carrier(n, reader) or []
    n.term = 'member'
    placed, visible = [], None
    for reader in READERS:
        seen = set()
        for e in entries[reader]:
            if e.entry in seen:
                continue
            seen.add(e.entry)
            if reader == READERS[0]:
                if e.cargo_path is None:
                    continue
                text = e.cargo_path
            else:
                text = e.entry
                if any(ch in GLOB for ch in text):
                    if w2 and visible is None:
                        visible = visible_repositories(n, rule, max_depth)
                    continue
            rel = entry_path(text)
            if rel is None:
                continue
            p = place(n, rule, rel)
            if p.absent:
                continue
            e.directory, e.placement = rel, p
            placed.append(e)
    if not w2:
        return [], placed, n
    members = []
    if array:
        cands = {}
        for spec in array:
            try:
                rel = rule.normalize_explicit_root(spec)
            except (rule.RootGrammarError, TypeError):
                return [], placed, n
            if not rel:
                continue
            p = place(n, rule, rel)
            if p.absent or p.candidate is None:
                continue
            cands.setdefault(p.candidate, [])
        provisional = [x for x in sorted(cands, key=lambda s: s.encode()) if candidate_failure(n, x, max_depth) != 'boundary']
        for cand in provisional:
            if candidate_failure(n, cand, max_depth) is not None:
                return [], placed, n
        if len(provisional) > c['MAX_MEMBERS']:
            return [], placed, n
        for cand in provisional:
            member_custody(n, cand)
            n.member_verdict(member_model, cand)
            members.append(cand)
        # The links run on a fresh observation after the walk (A4-2 step 3): `links_phase` below.
        return members, placed, n
    cands = set(e.placement.candidate for e in placed if e.placement.candidate is not None)
    ok = []
    for cand in sorted(cands, key=lambda s: s.encode()):
        if candidate_failure(n, cand, max_depth) is None:
            ok.append(cand)
    if len(ok) > c['MAX_MEMBERS']:
        return [], placed, n
    for cand in ok:
        member_custody(n, cand)
        n.member_verdict(member_model, cand)
        members.append(cand)
    links_stage(n, placed, members)
    return members, placed, n


def links_stage(n, placed, members):
    n.term = 'member'
    for e in placed:
        cand = e.placement.candidate
        if cand is None or cand not in members or e.placement.inner:
            continue
        link(n, e, cand)


def links_phase(c, tree, ledger, placed, members):
    """Branch A's links, on a fresh observation over the same binding table (`links`)."""
    n = Native(c, tree, ledger)
    links_stage(n, placed, members)
    return n


def descent(c, ledger, observed):
    """The composition walk's binding records: one per observed path the decision did not bind."""
    term = ledger.terms['descent']
    o, e = c['OWNED']
    for rel in sorted(observed):
        if rel not in ledger.bound:
            term.add((o, e, blen(rel) + c['DESCRIPTOR_METADATA'] + c['RECORD'], 0))
            ledger.bound.add(rel)
