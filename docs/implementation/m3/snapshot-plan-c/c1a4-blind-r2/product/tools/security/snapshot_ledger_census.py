"""The snapshot ledger's T2 census (M3-C r8 item 2, as M3-C r9 amends it; C1a plan r6, units C1a4 and C1a4-blind).

Developer tool only. It writes or checks one generated file, crates/security/src/snapshot_ledger_census.json: each
LEAD-READABLE T2 repository entry and workspace of the corpus manifest, priced on the snapshot ledger (the walk, the
session, and sealing's and the leftover capture's upper bound) and classified against `WorkLedger::snapshot_profile`'s
caps at the 2x margin, with the held-out entries' rows composed from the companion blind receipt. The security tests
classify it again against the compiled profile (`snapshot_walk_tests.rs`). This is B2-b's T2 census margin test
extended to the snapshot ledger's object, edge and byte caps (item 2).

It imports tools/security/discovery_census.py unchanged (its integrity-verified stores, its workspace overlays and
composition, its D15 decision path, its discovery walk model and reference population, its cost closure, its reference
rule and its one held-out join) and tools/security/snapshot_ledger_model.py unchanged (the snapshot walk's and the
capture session's charge model, and the profile's caps read by anchor). Item 5's bounds and sealing's charges are read
by anchor from crates/host/src/snapshot_seal.rs and the identity crate.

Pricing and eligibility are separate (M3-C r9, Codex M3CR9-R1-RF-3).
  - Pricing is conservative: no admitted boundary is applied; every handed file takes the session's dearer branch (a
    new blob); the walk model charges every capture at its dearer branch; sealing is charged at its 4 MiB envelope.
    The D15 member roots are the ones discovery_census.d15_terms admits over the entry's tree or the composed workspace.
  - Eligibility is decided on the admitted extent: the boundaries the discovery walk model itself derives over the
    same tree, and, as a lower bound on the rows, with every marker removed (a MARKER_CUSTODY row excludes only its
    marker) and every row below a directory deeper than discovery_scan.rs's MAX_UNIT_DEPTH removed (a DEPTH row
    excludes its unit and below). An entry is `over-item-5` only when that lower bound exceeds an item-5 bound.
  - The discovery walk model's observed scope must equal the reference population, as discovery's own census
    requires of every row (unit C1a4-blind: one computation path for the lead-readable and the blind rows).

The ordinary modes (--check, --write, --report) never open a held-out store: every store is reached through
discovery_census.store_path, which refuses a held-out entry before any filesystem call. The blind mode
(--held-out-blind; unit C1a4-blind, C1a plan r6 RF-3 step 3, the owner's decision of 2026-10-16) is the companion of
discovery's B2-b4c mode, with its allowlist and lifecycle (B2-b4 plan r6 section 2.5):
  - it reaches each held-out store only through discovery_census.held_out_store_path, the one held-out join;
  - its only effects are the receipt crates/security/src/snapshot_ledger_census_held_out.json and one line of counts;
  - each row is closed: measured {id, status, integrity, population, marginPermille, passes2x}, over item 5
    {id, status, integrity, population}, or an error {id, status, errorClass} with INTEGRITY, POPULATION, MODEL or IO;
    every exception is discarded unprinted;
  - the receipt binds the complete snapshot cost-source closure (Codex C1A4-R1-NBO-1): discovery's own receipt
    bindings, every product source the snapshot model and this tool read by pin or anchor, the tools' bytes, the
    profile's caps, item 5's bounds and the sealing bound. The ordinary mode composes the held-out rows only when every
    binding equals the current inputs; any drift makes the receipt stale.

Usage: snapshot_ledger_census.py (--check | --write | --report | --held-out-blind) --architecture <arch>
       --packages-root <checkout> --t2-cache <cache> [--caps NAME:OBJECTS,EDGES,BYTES ...]
  --report prints the record to standard output, with any further cap sets given (a cap given as - is not tested).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

PRODUCT = Path(__file__).resolve().parent.parent.parent
OUTPUT = 'crates/security/src/snapshot_ledger_census.json'
OUTPUT_RECEIPT = 'crates/security/src/snapshot_ledger_census_held_out.json'
TOOL = 'tools/security/snapshot_ledger_census.py'
MODEL = 'tools/security/snapshot_ledger_model.py'
DISCOVERY = 'tools/security/discovery_census.py'
MEMBER_MODEL = 'tools/security/discovery_member_model.py'
SEAL = 'crates/host/src/snapshot_seal.rs'
CANONICAL = 'crates/identity/src/canonical.rs'
DESCRIPTORS = 'crates/identity/src/descriptors.rs'
DISCOVERY_SCAN = 'crates/security/src/custody/discovery_scan.rs'
# The product sources this tool itself reads by anchor (besides the model's and discovery's own).
ANCHORED = (SEAL, CANONICAL, DESCRIPTORS, DISCOVERY_SCAN)
VCS = ('.git', '.hg', '.svn', '.jj')
# Sealing's charge sites (C1a3), each matched exactly once: the leftover's path copy, the inventory, the VCS record,
# the inventory blob's custody, the descriptor and the id.
SEAL_SITES = (r'work\.charge::<SealError>\(owned_record\(leftover\.len\(\)\)\)\?;',
              r'work\.charge::<SealError>\(owned_record\(inventory_len\)\)\?;',
              r'work\.charge::<SealError>\(owned_record\(160\)\)\?;',
              r'\.begin\(inventory\.len\(\) as u64, work\)', r'pending\.write\(chunk, work\)', r'pending\.commit\(work\)',
              r'work\.charge::<SealError>\(owned_record\(descriptor_bytes\)\)\?;',
              r'work\.charge::<SealError>\(owned_record\("snapshot2:"\.len\(\) \+ 64\)\)\?;')
# The companion receipt's closed formats (B2-b4 plan r6 section 2.5; unit C1a4-blind).
ERROR_CLASSES = ('INTEGRITY', 'POPULATION', 'MODEL', 'IO')
MEASURED_KEYS = {'id', 'status', 'integrity', 'population', 'marginPermille', 'passes2x'}
OVER_KEYS = {'id', 'status', 'integrity', 'population'}
ERROR_KEYS = {'id', 'status', 'errorClass'}
RECEIPT_KEYS = {'schemaVersion', 'standing', 'bindings', 'rows', 'state'}
PROFILE = 'snapshotProfile'
KEYS = ('objects', 'edges', 'bytes')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def require(condition, message):
    if not condition:
        raise ValueError(message)


def anchor(product, path, pattern):
    hits = re.findall(pattern, (product / path).read_text())
    if len(hits) != 1:
        raise ValueError('anchor %r matched %d times in %s' % (pattern, len(hits), path))
    return hits[0]


def canonical(value):
    """The identity crate's canonical JSON for strings, integers, objects and arrays (sorted keys, no whitespace,
    non-ASCII raw, control characters escaped)."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def bounds5(product):
    """Item 5's bounds, as sealing enforces them: rows, the canonical descriptor and total bytes."""
    rows = int(anchor(product, SEAL, r'\npub\(crate\) const MAX_ROWS: u64 = ([\d_]+);').replace('_', ''))
    total = int(anchor(product, SEAL, r'\npub\(crate\) const MAX_TOTAL_BYTES: u64 = ([\d_]+);').replace('_', ''))
    x, y, z = (int(v) for v in anchor(product, CANONICAL, r'\npub const MAX_BYTES: usize = (\d+) \* (\d+) \* (\d+);'))
    return rows, x * y * z, total


def item5(handed, sizes, limits):
    """Rows, total bytes and the canonical descriptor's length (C1a3's record, with placeholder digests)."""
    rows = len(handed)
    total = sum(sizes)
    inventory = 2 + max(0, rows - 1)
    for path, size in zip(handed, sizes):
        inventory += len(canonical(dict(bytes=size, path=path, sha256='0' * 64)))
    envelope = canonical(dict(projectId='prj1-' + '0' * 64, resolvedConfigDigest='0' * 64, schemaVersion=2,
                              scopeDigest='0' * 64, sourceInventory=[], vcsDigest='0' * 64))
    descriptor = len(envelope) - 2 + inventory
    over = [f for f, v, limit in zip(('rows', 'descriptor', 'totalBytes'), (rows, descriptor, total), limits) if v > limit]
    return dict(rows=rows, totalBytes=total, descriptorBytes=descriptor), over


def sealing_bound(product, c, s, limits):
    """Sealing's charge at its envelope, and the first leftover's path copy (C1a3's sites, each anchored): the
    inventory and the descriptor at 4 MiB each, the VCS record, the id, and the inventory blob's custody (its pending
    entry, its chunk writes, its commit's sample and the dearer of a new digest name and a duplicate's unlink)."""
    for pattern in SEAL_SITES:
        anchor(product, SEAL, pattern)
    vcs_record = int(anchor(product, SEAL, r'work\.charge::<SealError>\(owned_record\((\d+)\)\)\?;'))
    path_scalars = int(anchor(product, DESCRIPTORS, r'if value\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{'))
    row_path = path_scalars * 4  # bytes per Unicode scalar in UTF-8 at most (RFC 3629)
    rows, descriptor, _ = limits
    o, e = c['OWNED']
    owned = lambda n: (o, e, n + c['RECORD'])
    add = lambda *xs: tuple(sum(x[i] for x in xs) for i in range(3))
    name_len = len('pending-%d' % rows)
    unique = add(owned(64), (s['RENAME_COST'][0], s['RENAME_COST'][1], name_len + 64 + s['RENAME_COST'][2]), owned(s['SET_ENTRY_SIZE'][0]))
    dup = (s['UNLINK_COST'][0], s['UNLINK_COST'][1], name_len + s['UNLINK_COST'][2])
    chunks = -(-descriptor // s['READ_CHUNK'][0])
    writes = tuple(x * chunks for x in s['WRITE'])
    return add(owned(descriptor), owned(vcs_record), owned(descriptor), owned(len('snapshot2:') + 64), owned(name_len),
               (s['CREATE_COST'][0], s['CREATE_COST'][1], name_len + s['CREATE_COST'][2]), writes, c['STATUS'][:3],
               tuple(max(x, y) for x, y in zip(unique, dup)), owned(row_path))


def parse_caps(text):
    name, _, values = text.partition(':')
    return name, tuple(None if v == '-' else int(v) for v in values.split(','))


def permille(cap, cost):
    return {k: limit * 1000 // max(v, 1) for k, v, limit in zip(KEYS, cost, cap)}


def receipt_state(rows):
    if any(r['status'] == 'error' for r in rows):
        return 'incomplete (blind census)'
    return 'holds (blind census)' if all(r['status'] == 'over-item-5' or r['passes2x'] for r in rows) else 'fails (blind census)'


def is_count(value):
    return type(value) is int and value >= 0


def validated_receipt(receipt):
    """A companion receipt in its closed format, its ids unique; returns its state. Coverage of the held-out ids is
    checked against the manifest it is bound to, by `compose_held_out`."""
    require(isinstance(receipt, dict) and set(receipt) == RECEIPT_KEYS and receipt['schemaVersion'] == 1, 'receipt shape')
    require(isinstance(receipt['bindings'], dict) and isinstance(receipt['standing'], str), 'receipt shape')
    rows = receipt['rows']
    require(isinstance(rows, list) and rows and all(isinstance(r, dict) and isinstance(r.get('id'), str) for r in rows), 'receipt rows')
    require(len({r['id'] for r in rows}) == len(rows), 'a receipt id is duplicated')
    for r in rows:
        if r.get('status') == 'measured':
            require(set(r) == MEASURED_KEYS and r['integrity'] is True and r['population'] is True, 'measured row shape: ' + r['id'])
            mp = r['marginPermille']
            require(isinstance(mp, dict) and set(mp) == set(KEYS) and all(is_count(v) for v in mp.values()), 'margins: ' + r['id'])
            require(r['passes2x'] is all(v >= 2000 for v in mp.values()), 'passes2x disagrees with the margins: ' + r['id'])
        elif r.get('status') == 'over-item-5':
            require(set(r) == OVER_KEYS and r['integrity'] is True and r['population'] is True, 'over-item-5 row shape: ' + r['id'])
        elif r.get('status') == 'error':
            require(set(r) == ERROR_KEYS and r['errorClass'] in ERROR_CLASSES, 'error row shape: ' + r['id'])
        else:
            raise ValueError('receipt row status: ' + r['id'])
    require(receipt['state'] == receipt_state(rows), 'receipt state differs from its rows')
    return receipt['state']


def compose_held_out(held_ids, receipt, current):
    """The record's held-out rows and `heldOutMargin`, from the receipt only (never a held-out store). No receipt leaves
    them outstanding; an invalid one refuses; one bound to other inputs is stale; a current one must cover exactly the
    manifest's held-out ids."""
    if receipt is None:
        return [dict(id=i, status='outstanding: held-out') for i in held_ids], 'outstanding'
    state = validated_receipt(receipt)
    if receipt['bindings'] != current:
        return [dict(id=i, status='outstanding: held-out (blind receipt stale)') for i in held_ids], 'outstanding'
    got = [r['id'] for r in receipt['rows']]
    require(sorted(got) == sorted(held_ids), 'receipt coverage differs from the held-out entries')
    rows = {r['id']: r for r in receipt['rows']}
    return [dict(id=i, status='blind-census', result={k: v for k, v in rows[i].items() if k != 'id'}) for i in held_ids], state


class Census:
    """The census over one product checkout: its models, costs, caps and bounds, and the shared measure of one tree.
    `reference`, when given, is (rule, population) in place of the bound reference rule and population (the hermetic
    controls' synthetic rule); the ordinary and blind modes load the bound reference."""

    def __init__(self, product, arch, packages_root=None, reference=None, extra_caps=()):
        self.product, self.arch = product, arch
        dc = self.dc = load('discovery_census', product / DISCOVERY)
        slm = self.slm = load('snapshot_ledger_model', product / MODEL)
        self.dm = dc.load_member_model(product)
        c, pins = slm.snapshot_costs(product, dc)
        require(pins == [dc.pin_row(product, p) for p in slm.SNAPSHOT_FILES], 'the snapshot source pins differ')
        self.c, self.s = c, slm.session_costs(product, c)
        if reference is None:
            wv, ref, slm_ref, rule = dc.load_reference(product, arch, packages_root)
            self.rule, self.population = rule, (lambda tree: dc.reference_population(wv, ref, slm_ref, rule, tree))
        else:
            self.rule, self.population = reference
        self.limits = bounds5(product)
        self.unit_depth = int(anchor(product, DISCOVERY_SCAN, r'\nconst MAX_UNIT_DEPTH: usize = (\d+);'))
        self.caps = dict([(PROFILE, slm.snapshot_caps(product))] + list(extra_caps))
        self.after = sealing_bound(product, c, self.s, self.limits)
        chunk = self.chunk = self.s['READ_CHUNK'][0]
        one = slm.session_cost(c, self.s, [('a', b'\x01' * chunk)])
        two = slm.session_cost(c, self.s, [('a', b'\x01' * (2 * chunk))])
        self.step = tuple(y - x for x, y in zip(one, two))

        class Textless(dc.Tree):
            """A verified tree as the walk model reads it: a regular file's text is never needed, only its identity."""

            def node(self, rel):
                n = super().node(rel)
                if n is not None and n['kind'] == 'file' and 'text' not in n:
                    return dict(n, text='')
                return n

        class Boundaried(dc.Model):
            """The discovery walk model, recording each child directory it makes a boundary: the boundary is counted
            just after the child's `opensip.json` observation (discovery_census.Model.subtree)."""

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.found, self.last = [], None
                outer = self

                class Counts(dict):
                    def __setitem__(self, key, value):
                        if key == 'boundaries' and value > self.get(key, 0):
                            outer.found.append(outer.last.rsplit('/', 1)[0])
                        super().__setitem__(key, value)

                self.counts = Counts(self.counts)

            def observe(self, rel):
                self.last = rel
                super().observe(rel)

        self.Textless, self.Boundaried = Textless, Boundaried

    def sources(self):
        """Every product source the snapshot cost depends on, beyond discovery's own receipt bindings: the snapshot
        modules the model pins whole, every file its walk and session anchors read, the session files it pins, the
        ledger it reads the caps from, and the sources this tool reads by anchor (sealing, the identity bound and
        encoding, the depth bound). Codex C1A4-R1-NBO-1."""
        slm = self.slm
        paths = set(slm.SNAPSHOT_FILES) | {p for _, p, _ in slm.SNAPSHOT_ANCHORS} | {p for _, p, _, _ in slm.SESSION_ANCHORS}
        paths |= set(slm.SESSION_FILES) | {slm.WORK_LEDGER} | set(ANCHORED)
        return sorted(paths)

    def bindings(self):
        """The companion receipt's bindings: any drift in them makes the receipt stale."""
        dc, p = self.dc, self.product
        return dict(discovery=dc.receipt_bindings(p, self.arch, self.c),
                    tools=[dc.pin_row(p, x) for x in (TOOL, MODEL, DISCOVERY, MEMBER_MODEL)],
                    snapshotSources=[dc.pin_row(p, x) for x in self.sources()],
                    caps=dict(zip(KEYS, self.caps[PROFILE])), item5=dict(zip(('rows', 'descriptorBytes', 'totalBytes'), self.limits)),
                    maxUnitDepth=self.unit_depth, afterWalk=dict(zip(KEYS, self.after)))

    def snapshot(self, tree, boundaries, members):
        model = self.slm.SnapshotModel(self.c, self.rule, tree, boundaries, members=members)
        walk = model.walk()
        paths = [p for p, _ in model.handed]
        sizes = [tree.nodes[p]['size'] for p in paths]
        # The session at its dearer branch: every file a new blob of one chunk (distinct stand-ins), then each
        # file's chunks beyond one (or none, for an empty file) by the model's own per-chunk charge.
        session = list(self.slm.session_cost(self.c, self.s, [(p, b'%d' % i) for i, p in enumerate(paths)]))
        for size in sizes:
            for i in range(3):
                session[i] += self.step[i] * (-(-size // self.chunk) - 1)
        return walk, tuple(session), paths, sizes

    def measure(self, tree):
        """One tree, as both the lead-readable and the blind rows price it."""
        dc, slm = self.dc, self.slm
        tree = self.Textless(tree.nodes)
        member = self.dm.Member(self.c, dc.ENVIRONMENT_ENVELOPE, self.c['SYSTEM_SOURCES'])
        _, _, members = dc.d15_terms(self.c, self.dm, self.rule, tree, member)
        members = tuple(members)
        disc = self.Boundaried(self.c, self.rule, tree, 'automatic', [], members)
        disc.walk()
        found = sorted(set(disc.found))
        repos = [b for b in found if any(tree.kind(slm.join_rel(b, v)) is not None for v in VCS)]
        admitted = slm.Boundaries(dict(nestedRepositories=repos, nestedProjects=[b for b in found if b not in repos]))
        walk, session, paths, sizes = self.snapshot(tree, slm.Boundaries({}), members)
        cost = tuple(w + x for w, x in zip(walk, session))
        full = tuple(x + y for x, y in zip(cost, self.after))
        conservative, _ = item5(paths, sizes, self.limits)
        if found:
            _, _, a_paths, a_sizes = self.snapshot(tree, admitted, members)
        else:
            a_paths, a_sizes = paths, sizes
        keep = [(p, z) for p, z in zip(a_paths, a_sizes)
                if p.rsplit('/', 1)[-1] not in slm.SnapshotModel.MARKERS and p.count('/') <= self.unit_depth]
        lower, over = item5([p for p, _ in keep], [z for _, z in keep], self.limits)
        return dict(tree=tree, members=members, found=found, disc=disc, walk=walk, session=session, full=full,
                    conservative=conservative, admittedRows=len(a_paths), removed=len(a_paths) - len(keep), lower=lower, over=over)

    def margins(self, cost):
        out = {}
        for name, cap in self.caps.items():
            m = {}
            for k, v, limit in zip(KEYS, cost, cap):
                if limit is not None:
                    m[k] = dict(cap=limit, marginPermille=limit * 1000 // max(v, 1), passes2x=2 * v <= limit)
            out[name] = dict(m, passes2x=all(x['passes2x'] for x in m.values()))
        return out

    def price(self, tree, label, mounts=()):
        """A lead-readable row: the measure, with its population checked as discovery's census checks it."""
        x = self.measure(tree)
        require(x['disc'].observed == self.population(x['tree']), 'model population differs from the reference: ' + label)
        walk, session, full = x['walk'], x['session'], x['full']
        row = dict(id=label, members=len(x['members']), admittedBoundaries=len(x['found']),
                   discoveryDepthLimitDirectories=x['disc'].counts['depthLimitDirectories'],
                   item5Conservative=x['conservative'],
                   eligibility=dict(admittedRows=x['admittedRows'], markerOrDeepRowsRemoved=x['removed'], lowerBound=x['lower']),
                   walk=dict(zip(KEYS, walk)), session=dict(zip(KEYS, session)), fullLedger=dict(zip(KEYS, full)))
        if x['over']:
            row.update(status='over-item-5', overFields=x['over'])
        else:
            row.update(status='measured', margins=self.margins(full))
        if mounts:
            w2, s2, _, _ = self.snapshot(x['tree'], self.slm.Boundaries({}), tuple(mounts))
            alt = tuple(a + b + c for a, b, c in zip(w2, s2, self.after))
            row['allMountsAsMembers'] = dict(members=len(mounts), objects=alt[0], edges=alt[1], bytes=alt[2], margins=self.margins(alt))
        return row

    def blind_row(self, entry, store, token):
        """One held-out entry, measured blind: a closed row, or an error row with its class only. Every exception is
        discarded unprinted. The measure is the lead-readable rows' (`measure`), and the population check theirs."""
        dc = self.dc

        def error(kind):
            return dict(id=entry['id'], status='error', errorClass=kind)
        try:
            tree = dc.verified_tree(dc.held_out_store_path(store, entry, token), entry)
        except OSError:
            return error('IO')
        except (Exception, SystemExit):  # noqa: BLE001 (reduced to its class, as discovery's blind rows)
            return error('INTEGRITY')
        try:
            x = self.measure(tree)
            require(not x['members'], 'a held-out tree admitted a member')
            expected = self.population(x['tree'])
        except OSError:
            return error('IO')
        except (Exception, SystemExit):  # noqa: BLE001
            return error('MODEL')
        if x['disc'].observed != expected:
            return error('POPULATION')
        if x['over']:
            return dict(id=entry['id'], status='over-item-5', integrity=True, population=True)
        try:
            margins = permille(self.caps[PROFILE], x['full'])
            passes = all(v >= 2000 for v in margins.values())
            require(passes is all(2 * v <= cap for v, cap in zip(x['full'], self.caps[PROFILE])), 'the margins disagree with the caps')
        except (Exception, SystemExit):  # noqa: BLE001
            return error('MODEL')
        return dict(id=entry['id'], status='measured', integrity=True, population=True, marginPermille=margins, passes2x=passes)

    def record(self, cache, log=True):
        """The census record: the lead-readable rows from their stores, the held-out rows from the receipt only."""
        dc, arch, product = self.dc, self.arch, self.product
        manifest_raw = (arch / dc.MANIFEST).read_bytes()
        manifest = json.loads(manifest_raw)
        store = os.path.join(cache, 'store')
        entries, trees = [], {}
        for entry in manifest['repositories']:
            if entry['heldOut'] is not False:
                continue
            tree = dc.verified_tree(dc.store_path(store, entry), entry)
            trees[entry['id']] = tree
            entries.append(self.price(tree, entry['id']))
            if log:
                print('priced', entry['id'], file=sys.stderr, flush=True)
        workspaces = []
        for ws in manifest['workspaces']:
            if ws['heldOut'] is not False:
                continue
            root_tree, members, _ = dc.verified_workspace(cache, arch, store, ws, manifest, trees)
            workspaces.append(self.price(dc.compose(root_tree, members), ws['id'], [mount for mount, _ in members]))
            if log:
                print('priced', ws['id'], file=sys.stderr, flush=True)
        receipt_path = product / OUTPUT_RECEIPT
        receipt = json.loads(receipt_path.read_bytes()) if receipt_path.is_file() else None
        held, held_state = compose_held_out(dc.held_out_ids(manifest), receipt, self.bindings())
        rows = entries + workspaces
        measured = [r for r in rows if r['status'] == 'measured']
        blind_failing = sorted(r['id'] for r in held if r['status'] == 'blind-census' and r['result']['status'] == 'measured'
                               and not r['result']['passes2x'])
        failing = {n: sorted(r['id'] for r in measured if not r['margins'][n]['passes2x']) for n in self.caps}
        failing[PROFILE] = sorted(failing[PROFILE] + blind_failing)
        pins = [dc.pin_row(product, p) for p in (TOOL, MODEL, DISCOVERY, MEMBER_MODEL, SEAL, self.slm.WORK_LEDGER)]
        body = dict(schemaVersion=1,
                    standing='The T2 census on the snapshot ledger (M3-C r8 item 2 as M3-C r9 amends it; units C1a4 and '
                             'C1a4-blind). Generated by tools/security/snapshot_ledger_census.py from integrity-verified '
                             'stores; held-out entries are never read here: their rows are composed from the companion '
                             'blind receipt, and only while it is current. Priced with no boundary, every blob new and '
                             'sealing at its envelope (all conservative), with the D15 members discovery admits; '
                             'over-item-5 decided on the admitted extent\'s lower bound. Counts and ids only. Design '
                             'evidence, not product qualification.',
                    manifest=dict(path=dc.MANIFEST, bytes=len(manifest_raw), sha256=hashlib.sha256(manifest_raw).hexdigest()),
                    pins=pins, item5=dict(zip(('rows', 'descriptorBytes', 'totalBytes'), self.limits)), maxUnitDepth=self.unit_depth,
                    afterWalk=dict(zip(KEYS, self.after)), caps={n: dict(zip(KEYS, v)) for n, v in self.caps.items()}, margin=2,
                    marginUnit='cap * 1000 // cost, floored (per mille); the margin holds at 2000 or more',
                    counts=dict(entries=len(entries), workspaces=len(workspaces), measured=len(measured),
                                overItem5=len(rows) - len(measured), withMembers=sum(1 for r in rows if r['members']),
                                withAdmittedBoundaries=sum(1 for r in rows if r['admittedBoundaries']), heldOut=len(held)),
                    maximaMeasured={k: max((r['fullLedger'][k] for r in measured), default=0) for k in KEYS},
                    failing2x=failing, entries=entries, workspaces=workspaces,
                    heldOutEntries=held, heldOutMargin=held_state,
                    capsStatus='returned-to-law' if failing[PROFILE] else 'recorded-margin-holds')
        return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode()

    def blind(self, cache, token):
        """The blind receipt over every held-out entry (no held-out workspace exists)."""
        dc = self.dc
        manifest = json.loads((self.arch / dc.MANIFEST).read_bytes())
        require(all(ws['heldOut'] is False for ws in manifest['workspaces']), 'a held-out workspace is outside the blind mode')
        store = os.path.join(cache, 'store')
        ids = dc.held_out_ids(manifest)
        by_id = {e['id']: e for e in manifest['repositories']}
        require(ids, 'no held-out entries')
        rows = [self.blind_row(by_id[i], store, token) for i in ids]
        body = {'schemaVersion': 1,
                'standing': 'The companion snapshot blind held-out receipt (C1a plan r6 RF-3; unit C1a4-blind; the owner '
                            'decision of 2026-10-16): per held-out T2 entry only its id, its integrity and population '
                            'verdicts and its per-mille margins on the snapshot ledger\'s full ledger against the '
                            'snapshot profile\'s caps, its over-item-5 verdict, or an error class. Generated by '
                            'tools/security/snapshot_ledger_census.py --held-out-blind; no held-out content is emitted. '
                            'Bound to the complete snapshot cost-source closure; any drift makes it stale.',
                'bindings': self.bindings(),
                'rows': rows,
                'state': receipt_state(rows)}
        return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode(), rows


def run_blind(census, cache):
    """The blind run's only effects: the receipt, and one line of counts on stdout."""
    raw, rows = census.blind(cache, census.dc._BLIND)
    (census.product / OUTPUT_RECEIPT).write_bytes(raw)
    measured = [r for r in rows if r['status'] == 'measured']
    over = [r for r in rows if r['status'] == 'over-item-5']
    print('Blind held-out snapshot census: %d entries, %d measured, %d passing, %d over item 5, %d errors.'
          % (len(rows), len(measured), sum(1 for r in measured if r['passes2x']), len(over), len(rows) - len(measured) - len(over)))


def run(a):
    if a.caps and not a.report:
        raise ValueError('further cap sets are for --report only')
    census = Census(PRODUCT, a.architecture.resolve(strict=True), a.packages_root.resolve(strict=True), extra_caps=a.caps)
    cache = str(a.t2_cache.resolve(strict=True))
    if a.held_out_blind:
        run_blind(census, cache)
        return
    raw = census.record(cache)
    target = PRODUCT / OUTPUT
    if a.report:
        sys.stdout.write(raw.decode())
    elif a.check:
        if not (target.is_file() and target.read_bytes() == raw):
            raise ValueError('output differs: ' + OUTPUT)
        print('Verified ' + OUTPUT)
    else:
        target.write_bytes(raw)
        print('Generated ' + OUTPUT)


def main():
    # As discovery's: no abbreviated options, and the blind mode's redaction chosen from the parsed arguments. Parser
    # exits (usage, help) come before any store is touched and echo only the command line.
    ap = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing it')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    mode.add_argument('--report', action='store_true', help='print the record, with any further cap sets')
    mode.add_argument('--held-out-blind', action='store_true', help='the blind held-out census: write only the receipt')
    ap.add_argument('--architecture', type=Path, required=True)
    ap.add_argument('--packages-root', type=Path, required=True)
    ap.add_argument('--t2-cache', type=Path, required=True)
    ap.add_argument('--caps', action='append', type=parse_caps, default=[])
    a = ap.parse_args()
    if not a.held_out_blind:
        try:
            run(a)
        except (ValueError, KeyError, OSError) as error:
            print('Snapshot ledger census failed: ' + str(error), file=sys.stderr)
            raise SystemExit(1)
        return
    try:
        run(a)
    except BaseException:  # noqa: BLE001
        # Every failure of a blind run, an exit or an interrupt included, is this one line: any exception text could
        # name a held-out path (B2-b4 plan r6 section 2.5).
        print('Snapshot ledger census blind run failed.', file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == '__main__':
    main()
