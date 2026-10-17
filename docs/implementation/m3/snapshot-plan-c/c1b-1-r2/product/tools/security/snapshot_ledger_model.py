"""The snapshot walk's charge model (M3-C r8 item 2; unit C1a1, C1a plan r5 section 2).

Developer tool only. It writes or checks crates/security/src/snapshot_ledger_vectors.json: for each tree, its description
(the discovery walk vectors' format), its admitted boundaries, and the model's predicted charge of the snapshot extent
walk (`crates/security/src/snapshot_walk.rs`, with its opener helpers in `snapshot_source.rs`) as (objects, edges,
bytes). The security tests walk each tree natively on a fresh ledger and assert the walk used no more
(`snapshot_walk_tests.rs`, the soundness control).

Unit C1b-1 (C1b plan r6, LD-C1B-6) adds the VCS term: `VcsModel` prices `crates/security/src/snapshot_vcs.rs`'s Git reads
step by step, under each step's owner's pricing, and writes crates/security/src/snapshot_vcs_vectors.json. Its cases are
repositories the security tests build and observe natively, each charge asserted equal; `vcs_envelope` is the term at its
dearest shapes, from which the cap derivation is taken.

The cost constants are the bound census's: this tool imports tools/security/discovery_census.py unchanged (its `costs`,
which verifies the census's whole cost closure and reads every constant by anchor, its `Tree` and its tree reading of
the walk vectors), so a change to any shared charge refuses here too. The snapshot modules' own shapes are pinned by
anchors below, and both files are pinned whole: any change to them refuses until this model is revised. Unknowns are
charged at their dearer branch: every judged object captures its ACL and takes the larger of a full entry list and the
filesystem premise.

The snapshot ledger's caps are `WorkLedger::snapshot_profile`'s (crates/platform/src/work_ledger.rs; M3-C r9 item 2,
unit C1a4), read by anchor (`snapshot_caps`); tools/security/snapshot_ledger_census.py classifies the lead-readable T2
census against them. No network, process or environment input.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import sys

OUTPUT = 'crates/security/src/snapshot_ledger_vectors.json'
# Unit C1a2: the host capture session's read, retention and custody terms, beyond the walk's own charges.
SESSION_OUTPUT = 'crates/host/src/snapshot_session_vectors.json'
HOST_SESSION = 'crates/host/src/snapshot.rs'
HOST_CUSTODY = 'crates/host/src/candidate_custody.rs'
HOST_TESTS = 'crates/host/src/snapshot_tests.rs'
PLATFORM_ENTRY = 'crates/platform/src/custody_entry.rs'
PLATFORM_EFFECTS = 'crates/platform/src/filesystem/file_effects.rs'
# r2 (Codex C1A2-R1-RF-1): custody's admission is security's private-directory judgment, one ACL capture.
SECURITY_SOURCE = 'crates/security/src/snapshot_source.rs'
SECURITY_PRIVATE = 'crates/security/src/private_access.rs'
SESSION_FILES = (HOST_SESSION, HOST_CUSTODY, PLATFORM_ENTRY, SECURITY_PRIVATE)
_COST = r'WorkCost \{\n\s+objects: (\d+),\n\s+edges: (\d+),\n\s+bytes: (\d+),\n\s*\}'
# Each (name, path, pattern, count): the session's own charge shapes and sites.
SESSION_ANCHORS = (
    ('READ_CHUNK', HOST_SESSION, r'\npub\(crate\) const READ_CHUNK: usize = ([\d_]+);', 1),
    ('FIRST_GROWTH', HOST_SESSION, r'\nconst FIRST_GROWTH: usize = ([\d_]+);', 1),
    ('ATTEMPT', HOST_SESSION, r'\nconst ATTEMPT: WorkCost = ' + _COST, 1),
    ('BUFFER_SITE', HOST_SESSION, r'work\.charge::<ReadError>\(buffer_cost\(\)\)\?;()', 1),
    # Unit C1c-0: the pruned-tree capture is a third site, at the same price.
    ('CAPTURE_SITE', HOST_SESSION, r'work\.charge::<ReadError>\(owned_record\(std::mem::size_of::<Capture>\(\)\)\)\?;()', 3),
    ('READ_SAMPLE', HOST_SESSION, r'work\.run\(STATUS_COST, \|_\| \{()', 1),
    ('READ_SAMPLES_TAKEN', HOST_SESSION, r'let (?:before|after) = sample\(source\.file\(\), work\)\?;()', 2),
    ('ATTEMPT_SITE', HOST_SESSION, r'work\.charge::<ReadError>\(ATTEMPT\)\?;()', 1),
    ('LISTING', HOST_CUSTODY, r'\nconst LISTING: WorkCost = ' + _COST, 1),
    ('VISIT', HOST_CUSTODY, r'\nconst VISIT: WorkCost = ' + _COST, 1),
    ('WRITE', HOST_CUSTODY, r'\nconst WRITE: WorkCost = ' + _COST, 1),
    ('NEW_ADMISSION', HOST_CUSTODY, r'admit_custody_directory\(dir\.as_file\(\), uid, work\)()', 1),
    ('ADMISSION_OBSERVES', SECURITY_SOURCE, r'crate::private_access::observe_private_directory\(directory, invoking_uid, work\)()', 1),
    # The private-directory judgment charges one ACL capture and nothing else.
    ('OBSERVE_CAPTURES', SECURITY_PRIVATE, r'pub\(crate\) fn observe_private_directory\([^{]*\{\n\s+use opensip_platform::\{WorkFailure, capture_descriptor_acl_accounted\};\n\s+let sample = capture_descriptor_acl_accounted\(directory, work\)\.map_err\(lift_capture\)\?;\n\s+assess_private_descendant_capture\(PrivateObjectKind::Directory, invoking_uid, &sample\)\n\s+\.map_err\(\|error\| WorkFailure::Operation\(PreparePrivateError::Access\(error\)\)\)\?;\n\s+Ok\(sample\)\n\}()', 1),
    ('ACL_CAPTURE', HOST_TESTS, r'opensip_platform::descriptor_acl_capture_cost\(\),\n\s+WorkCost \{\n\s+objects: (\d+),\n\s+edges: (\d+),\n\s+bytes: (\d+),\n\s+\}', 1),
    ('NEW_LISTING', HOST_CUSTODY, r'work\.charge::<CustodyError>\(LISTING\)\?;()', 1),
    ('NEW_VISIT', HOST_CUSTODY, r'work\.charge::<CustodyError>\(VISIT\)\?;()', 1),
    ('BEGIN_NAME', HOST_CUSTODY, r'let name_bytes = "pending-"\.len\(\) \+ decimal_len\(self\.next\);\n\s+work\.charge::<CustodyError>\(owned_record\(name_bytes\)\)\?;\n\s+let name = format!\("pending-\{\}", self\.next\);()', 1),
    ('BEGIN_CREATE', HOST_CUSTODY, r'\.create_exclusive_regular_accounted\(&name, work\)()', 1),
    ('WRITE_SITE', HOST_CUSTODY, r'work\.charge::<CustodyError>\(WRITE\)\?;()', 1),
    ('COMMIT_SAMPLE', HOST_CUSTODY, r'return refuse\(CustodyError::Digest\);\n\s+\};\n\s+let sample = work\.run\(STATUS_COST, \|_\| \{()', 1),
    ('COMMIT_UNLINK', HOST_CUSTODY, r'\.unlink_entry_accounted\(&name, work\)()', 1),
    ('COMMIT_HEX', HOST_CUSTODY, r'work\.charge::<CustodyError>\(owned_record\(64\)\)\?;\n\s+let hex = digest_hex\(&sha256\);()', 1),
    ('COMMIT_RENAME', HOST_CUSTODY, r'\.rename_exclusive_accounted\(&name, &hex, work\)()', 1),
    ('COMMIT_SET', HOST_CUSTODY, r'work\.charge::<CustodyError>\(owned_record\(std::mem::size_of::<\(\[u8; 32\], u64\)>\(\)\)\)\?;()', 1),
    ('RENAME_COST', PLATFORM_ENTRY, r'pub fn rename_exclusive_cost\(from: &str, to: &str\) -> WorkCost \{\n\s+WorkCost \{\n\s+objects: (\d+),\n\s+edges: (\d+),\n\s+bytes: from\.len\(\)\.saturating_add\(to\.len\(\)\)\.saturating_add\((\d+)\),', 1),
    ('UNLINK_COST', PLATFORM_ENTRY, r'pub fn unlink_entry_cost\(name: &str\) -> WorkCost \{\n\s+WorkCost \{\n\s+objects: (\d+),\n\s+edges: (\d+),\n\s+bytes: name\.len\(\)\.saturating_add\((\d+)\),', 1),
    ('CREATE_COST', PLATFORM_EFFECTS, r'pub fn create_exclusive_regular_cost\(name: &str\) -> WorkCost \{\n\s+WorkCost \{\n\s+objects: (\d+),\n\s+edges: (\d+),\n\s+bytes: name\.len\(\)\.saturating_add\((\d+)\),', 1),
    ('CAPTURE_SIZE', HOST_TESTS, r'assert_eq!\(std::mem::size_of::<Capture>\(\), (\d+)\);', 1),
    ('SET_ENTRY_SIZE', HOST_TESTS, r'assert_eq!\(std::mem::size_of::<\(\[u8; 32\], u64\)>\(\), (\d+)\);', 1),
)
# Unit C1b-1 (C1b plan r6): the VCS observation's own charge shapes, in snapshot_vcs.rs, pinned whole in its vectors.
VCS_SOURCE = 'crates/security/src/snapshot_vcs.rs'
VCS_TESTS = 'crates/security/src/snapshot_vcs_tests.rs'
VCS_OUTPUT = 'crates/security/src/snapshot_vcs_vectors.json'
VCS_ANCHORS = (
    ('PARSE', VCS_SOURCE, r'\nfn parse_cost\(len: usize\) -> WorkCost \{\n    WorkCost \{\n        objects: (\d+),\n        edges: (\d+),\n        bytes: len,\n'),
    ('READ_SITE', VCS_SOURCE, r'        let raw = git::snapshot_read\(&file, INDEX_CAP, reasons\.oversized, work\)\?;\n'
     r'        work\.charge::<TrackingRefusal>\(parse_cost\(raw\.len\(\)\)\)\?;\n()'),
    ('COMMIT_SITE', VCS_SOURCE, r'        work\.charge::<TrackingRefusal>\(owned_record\(COMMIT_HEX\)\)\?;\n()'),
    ('COMMIT_HEX', VCS_SOURCE, r'\npub const COMMIT_HEX: usize = (\d+);'),
    ('MEMBERS_SITE', VCS_SOURCE, r'        work\.charge::<VcsRefusal>\(owned_record\(\n            members\n                \.len\(\)\n'
     r'                \.saturating_mul\(std::mem::size_of::<MemberCommit<\'_>>\(\)\),\n        \)\)\?;\n()'),
    ('MEMBER_SIZE', VCS_TESTS, r'    assert_eq!\(std::mem::size_of::<MemberCommit<\'_>>\(\), (\d+)\);'),
    ('W_STATUS', VCS_SOURCE, r'        let device = git::snapshot_metadata\(w\.as_file\(\), work\)\n()'),
    ('RECORD_GIT', VCS_SOURCE, r'            Self::Git\(_\) => Some\((\d+)\),'),
    ('RECORD_NONE', VCS_SOURCE, r'            Self::None => Some\((\d+)\),'),
    ('RECORD_MEMBER', VCS_SOURCE, r'                    \.map\(\|m\| (\d+) \+ payload_len\(m\.path\)\)\n'),
    ('RECORD_TOP', VCS_SOURCE, r'                    \.saturating_add\((\d+)\)\n'),
)
CENSUS = 'tools/security/discovery_census.py'
WALK_VECTORS = 'crates/security/src/custody/discovery_walk_vectors.json'
READ_SET = 'crates/security/src/snapshot_read_set.rs'
# Unit C1c-0: the pruned-tree opener's module joins the pinned snapshot modules.
SNAPSHOT_FILES = ('crates/security/src/snapshot_walk.rs', 'crates/security/src/snapshot_source.rs', READ_SET)
# The snapshot modules' own charge shapes (each must match exactly once).
SNAPSHOT_ANCHORS = (
    ('RECORD', 'crates/security/src/snapshot_walk.rs', r'\nconst RECORD: usize = (\d+);'),
    # r2 (Codex C1A1-R1-RF-4): the classification's own form, counted from the shared rule's source. C1a4 (M3-C r9 item
    # 2, remedy (b-prime)): no member term, since the rule compares member roots in place.
    ('CLASSIFY', 'crates/security/src/snapshot_walk.rs',
     r'fn classify_cost\(rel: &str\) -> WorkCost \{\n'
     r'    let segments = rel\.split\(\'/\'\)\.count\(\);\n'
     r'    let targets = rel\.split\(\'/\'\)\.filter\(\|part\| \*part == "target"\)\.count\(\);\n'
     r'    let objects = (\d+) \+ targets;\n    WorkCost \{\n        objects,\n        edges: (\d+),\n'
     r'        bytes: segments\n'
     r'            \.saturating_mul\((\d+) \* std::mem::size_of::<usize>\(\)\)\n'
     r'            \.saturating_add\(rel\.len\(\)\.saturating_mul\((\d+) \+ targets\)\)\n'
     r'            \.saturating_add\(objects\.saturating_mul\(RECORD\)\),\n'),
    ('ANCHOR_CLASSIFY', 'crates/security/src/snapshot_walk.rs',
     r'    if last_segment\(path\) != rule::OPENSIP_CUSTODY_STATE \{\n        return Ok\(OpensipName::Other\);\n    \}\n'
     r'    work\.charge::<SnapshotStop<E>>\(classify_cost\(path\)\)\?;\n'
     r'    Ok\(match rule::classify_path\(path, known, members\) \{\n()'),
    # C1a4 (M3-C r9 item 2, remedy (a)): a kept `.opensip`'s anchor-question classification is recorded, and the walk
    # loop reuses it instead of classifying that name again.
    ('ANCHOR_RECORDED', 'crates/security/src/snapshot_walk.rs',
     r'            OpensipName::Classified \{ pruned \} => opensip = Some\(\(index, pruned\)\),\n()'),
    ('ANCHOR_REUSED', 'crates/security/src/snapshot_walk.rs',
     r'        let recorded = top\.opensip\.filter\(\|\(at, _\)\| \*at == index\);\n(?:[^\n]*\n){1,30}?'
     r'        let pruned = match recorded \{\n            Some\(\(_, pruned\)\) => pruned,\n            None => \{\n'
     r'                work\.charge::<SnapshotStop<E>>\(classify_cost\(&rel\)\)\?;\n'
     r'                rule::classify_path\(&rel, &known, extent\.member_roots\)\.is_some\(\)\n            \}\n        \};\n()'),
    ('ANCHOR_DROP', 'crates/security/src/snapshot_walk.rs',
     r'    if let Some\(index\) = anchor \{\n        drop\(paths\.remove\(index\)\);\n    \}\n    work\.charge::<SnapshotStop<E>>\(owned\(\n()'),
    # (C1a3) The three exclusions are one predicate, judged before any kind-dependent step; the root's carrier is
    # classified from it, with no charge.
    ('KIND_FREE_BOUNDARY', 'crates/security/src/snapshot_walk.rs',
     r'        let excluded = pruned \|\| extent\.ignored\(&rel\) \|\| extent\.boundaries\.is_boundary\(&rel\);\n'
     r'(?:[^\n]*\n){1,14}?        if excluded \{\n            continue;\n        \}\n        let parent_dir = levels\n()'),
    ('ROOT_STATUS', 'crates/security/src/snapshot_source.rs',
     r'    let sample = work\.run\(STATUS, \|_\| \{\n        opensip_platform::observe_descriptor_metadata\(lent\.as_file\(\)\)()'),
    ('ROOT_FRAME', 'crates/security/src/snapshot_walk.rs',
     r'    // The root frame\'s own slot\.\n    work\.charge::<SnapshotStop<E>>\(owned\(0\)\)\?;()'),
    ('FRAME', 'crates/security/src/snapshot_walk.rs', r'                work\.charge::<SnapshotStop<E>>\(owned\(0\)\)\?;()'),
    ('LISTING', 'crates/security/src/snapshot_walk.rs', r'    work\.charge::<SnapshotStop<E>>\(LISTING\)\?;()'),
    ('SLOTS', 'crates/security/src/snapshot_walk.rs',
     r'    work\.charge::<SnapshotStop<E>>\(owned\(\n        paths\n            \.len\(\)\n            \.saturating_mul\(std::mem::size_of::<ChildObservation>\(\)\),\n    \)\)\?;()'),
    ('CARGO_KEY', 'crates/security/src/snapshot_walk.rs', r'        work\.charge::<SnapshotStop<E>>\(key_cost\(&rel, ""\)\)\?;()'),
    ('SYMLINK', 'crates/security/src/snapshot_walk.rs',
     r'                work\.charge::<SnapshotStop<E>>\(owned\(rel\.len\(\)\)\)\?;\n                report\.symlinks\.push\(rel\);()'),
    ('SPECIAL', 'crates/security/src/snapshot_walk.rs',
     r'                work\.charge::<SnapshotStop<E>>\(owned\(rel\.len\(\)\)\)\?;\n                report\.special\.push\(rel\);()'),
    ('ACL_ENTRIES', 'crates/security/src/snapshot_source.rs',
     r'count\.saturating_mul\(std::mem::size_of::<opensip_platform::CapturedAclEntry>\(\)\),()'),
    ('OPEN_DIR_SAMPLE', 'crates/security/src/snapshot_source.rs',
     r'    let sample = work\.run\(STATUS, \|_\| \{\n        opensip_platform::observe_descriptor_metadata\(directory\.as_file\(\)\)()'),
    ('OPEN_REG_SAMPLE', 'crates/security/src/snapshot_source.rs',
     r'    let sample = work\.run\(STATUS, \|_\| \{\n        opensip_platform::observe_descriptor_metadata\(&file\)()'),
    # r3 (Codex C1A1-R2-RF-1): the pre-walk opener's charges, in its order.
    ('OPENER_VALIDATE', 'crates/security/src/snapshot_source.rs',
     r'        work\.charge::<SnapshotRefusal>\(owned\(path\.len\(\)\)\)\?;\n        let Ok\(validated\) = opensip_identity::LogicalPath::parse\(path\) else \{()'),
    ('OPENER_ROOT', 'crates/security/src/snapshot_source.rs', r'        judge_root\(self, custody, work\)\?;()'),
    ('OPENER_KEY', 'crates/security/src/snapshot_source.rs', r'            work\.charge::<SnapshotRefusal>\(key_cost\(&rel, part\)\)\?;()'),
    ('OPENER_PATH_KEPT', 'crates/security/src/snapshot_source.rs', r'            path: validated\.into_string\(\),()'),
    ('KEY_COST', 'crates/security/src/snapshot_source.rs',
     r'pub\(crate\) fn key_cost\(dir: &str, name: &str\) -> WorkCost \{\n    owned\(dir\.len\(\) \+ 1 \+ name\.len\(\)\)\n\}()'),
    # Unit C1c-0 (C1c plan r4, LD-C1C-13): a finished frame's Cargo root stays known and moves into the walk's evidence
    # (no charge), and each admitted member root is copied out of the extent, charged first.
    ('CARGO_KEPT', 'crates/security/src/snapshot_walk.rs',
     r'        if top\.next == top\.paths\.len\(\) \{\n(?:            //[^\n]*\n)*            drop\(levels\.pop\(\)\);\n            continue;\n()'),
    ('CARGO_MOVED', 'crates/security/src/snapshot_walk.rs', r'            cargo_roots: known,\n()'),
    ('MEMBER_COPY', 'crates/security/src/snapshot_walk.rs',
     r'    for member in extent\.member_roots \{\n        work\.charge::<SnapshotStop<E>>\(owned\(member\.len\(\)\)\)\?;\n'
     r'        member_roots\.insert\(member\.clone\(\)\);\n    \}\n()'),
    # Unit C1c-0 (LD-C1C-2): the pruned-tree opener's charges, in its order.
    ('PRUNED_VALIDATE', READ_SET,
     r'    work\.charge::<SnapshotRefusal>\(owned\(path\.len\(\)\)\)\?;\n    let Ok\(validated\) = opensip_identity::LogicalPath::parse\(path\) else \{()'),
    ('PRUNED_CAPTURE', READ_SET,
     r'fn pruned_capture_cost\(path: &str\) -> WorkCost \{\n    let segments = path\.split\(\'/\'\)\.count\(\);\n    WorkCost \{\n'
     r'        objects: (\d+),\n        edges: (\d+),\n        bytes: segments\n'
     r'            \.saturating_mul\((\d+) \* std::mem::size_of::<usize>\(\)\)\n'
     r'            \.saturating_add\(path\.len\(\)\)\n            \.saturating_add\((\d+) \* RECORD\),\n'),
    ('PRUNED_CAPTURE_SITE', READ_SET, r'    work\.charge::<SnapshotRefusal>\(pruned_capture_cost\(path\)\)\?;()'),
    ('PRUNED_ROOT', READ_SET, r'    judge_root\(root, custody, work\)\?;()'),
    ('PRUNED_KEY', READ_SET, r'        work\.charge::<SnapshotRefusal>\(key_cost\(&rel, part\)\)\?;()'),
    ('PRUNED_CUSTODY_ABOVE', READ_SET, r'        if index < anchor\n            && let Err\(reason\) = judge_opened\(()'),
    ('PRUNED_NO_MARKER', READ_SET, r'    Ok\(source_file\(validated\.into_string\(\), file, metadata, false\)\)()'),
    ('READ_SET_RECORD', READ_SET, r'\nconst RECORD: usize = (\d+);'),
)
# Item 5's bounds.
MAX_ROWS = 100_000
MAX_DESCRIPTOR = 4 * 1024 * 1024
# C1a4 (M3-C r9 item 2): the snapshot ledger's caps are the profile's, read by anchor, never restated here.
WORK_LEDGER = 'crates/platform/src/work_ledger.rs'
CAP_ANCHORS = (
    ('objects', r'\nconst SNAPSHOT_OBJECT_LIMIT: usize = 1 << (\d+);'),
    ('edges', r'\nconst SNAPSHOT_EDGE_LIMIT: usize = 1 << (\d+);'),
    ('bytes', r'\nconst SNAPSHOT_BYTE_LIMIT: usize = 1 << (\d+);'),
)
PROFILE = (r'    pub fn snapshot_profile\(\) -> Self \{\n        Self \{\n            limits: Cost \{\n'
           r'                objects: SNAPSHOT_OBJECT_LIMIT,\n                edges: SNAPSHOT_EDGE_LIMIT,\n'
           r'                bytes: SNAPSHOT_BYTE_LIMIT,\n            \},\n            used: Cost::default\(\),\n')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def snapshot_costs(product, dc):
    c = dc.costs(product)
    shapes = {}
    for name, path, pattern in SNAPSHOT_ANCHORS:
        hits = list(re.finditer(pattern, (product / path).read_text()))
        require(len(hits) == 1, 'snapshot anchor %s matched %d times' % (name, len(hits)))
        shapes[name] = tuple(int(g) for g in hits[0].groups() if g)
    require(shapes['RECORD'] == (c['RECORD'],), 'the snapshot walk prices records unlike the census')
    require(shapes['READ_SET_RECORD'] == (c['RECORD'],), 'the read set prices records unlike the census')
    # Unit C1c-0: a frame's exit never drops its Cargo root (the evidence keeps it).
    require('known.remove' not in (product / SNAPSHOT_FILES[0]).read_text(), 'a Cargo root is dropped at its frame\'s exit')
    po, pe, ptwo, precords = shapes['PRUNED_CAPTURE']
    c = dict(c, PRUNED_CAPTURE=(po, pe, ptwo * c['SIZES']['usize'], precords * c['RECORD']))
    o, e, two, anchors = shapes['CLASSIFY']
    c = dict(c, SNAPSHOT_CLASSIFY=(o, e, two * c['SIZES']['usize'], anchors))
    pins = [dc.pin_row(product, p) for p in SNAPSHOT_FILES]
    return c, pins


def snapshot_caps(product):
    """`WorkLedger::snapshot_profile`'s (objects, edges, bytes), each a power of two read by anchor."""
    text = (product / WORK_LEDGER).read_text()
    require(len(re.findall(PROFILE, text)) == 1, 'the snapshot profile does not take its three caps')
    caps = []
    for name, pattern in CAP_ANCHORS:
        hits = re.findall(pattern, text)
        require(len(hits) == 1, 'snapshot cap anchor %s matched %d times' % (name, len(hits)))
        caps.append(1 << int(hits[0]))
    return tuple(caps)


def blen(text):
    return len(text.encode())


def join_rel(parent, name):
    return parent + '/' + name if parent else name


class Boundaries:
    """`AdmittedBoundaries`, as the walk asks it: nested repositories and projects, and custody rows (a marker-custody
    row excludes its marker only; any other row its directory and below)."""

    def __init__(self, inventory):
        self.repos = list(inventory.get('nestedRepositories', []))
        self.projects = list(inventory.get('nestedProjects', []))
        self.rows = [(r['path'], r['reason']) for r in inventory.get('custodyExcludedUnits', [])]

    @staticmethod
    def at_or_below(rel, anchor):
        """The shared rule's `at_or_below` exactly: the root anchor `''` covers only the root."""
        stem = anchor.rstrip('/')
        return rel == anchor or (rel.startswith(stem) and rel[len(stem):].startswith('/'))

    def anchor(self, rel, marker=None):
        """`AdmittedBoundaries::boundary_anchor`: repositories, then projects, then the first covering custody row."""
        for b in self.repos + self.projects:
            if self.at_or_below(rel, b):
                return b
        for p, reason in self.rows:
            if reason.startswith('MARKER_CUSTODY:'):
                if p == rel and marker is not None and reason[len('MARKER_CUSTODY:'):].split(':')[0] == marker:
                    return p
            elif self.at_or_below(rel, p):
                return p
        return None

    def is_boundary(self, rel):
        return self.anchor(rel) is not None

    def marker_row(self, parent, name):
        return self.anchor(parent, name) == parent


class SnapshotModel:
    """The abstract walk of `walk_snapshot`: one charge per charge the code makes, in its order."""
    MARKERS = ('Cargo.toml', 'package.json', 'tsconfig.json', 'jsconfig.json')

    def __init__(self, c, rule, tree, boundaries, ignore=(), members=(), acl_paths=()):
        self.c, self.rule, self.t, self.b = c, rule, tree, boundaries
        self.ignore, self.members, self.acl_paths = tuple(ignore), tuple(members), frozenset(acl_paths)
        self.cost = [0, 0, 0]
        # C1a4 (remedy (a)): the kept `.opensip` names the anchor question classified, not classified again.
        self.reused = set()
        self.handed = []  # (path, bytes) of each regular file handed to the visitor, in order
        # Exact (r2, Codex C1A1-R1-NBO-2) while every capture takes the branch charged: on the APFS scratch an object
        # with no ACL entry returns none, so its capture takes the premise, which must be the dearer branch.
        o, e = self.c['OWNED']
        full = (o, e, self.c['MAX_ENTRIES'] * self.c['ACL_ENTRY'] + self.c['RECORD'])
        self.exact = all(f >= a for f, a in zip(self.c['FS'][:3], full))

    def add(self, cost, times=1):
        for i in range(3):
            self.cost[i] += cost[i] * times

    def owned(self, nbytes):
        o, e = self.c['OWNED']
        self.add((o, e, nbytes + self.c['RECORD']))

    def capture(self, rel):
        """`judge_opened` past its metadata-only rejection: CAP, then the dearer of a full entry list and the premise."""
        if rel in self.acl_paths:
            self.exact = False
        self.add(self.c['CAP'])
        o, e = self.c['OWNED']
        acl = (o, e, self.c['MAX_ENTRIES'] * self.c['ACL_ENTRY'] + self.c['RECORD'])
        self.add(tuple(max(x, y) for x, y in zip(acl, self.c['FS'][:3])))

    def classify(self, rel):
        """`classify_cost`: the segment list, a prefix per `target`, and the anchors; no member term (C1a4)."""
        o, e, two_usize, anchors = self.c['SNAPSHOT_CLASSIFY']
        segments = rel.count('/') + 1
        targets = rel.split('/').count('target')
        objects = o + targets
        self.add((objects, e, segments * two_usize + blen(rel) * (anchors + targets) + objects * self.c['RECORD']))

    def custody_anchor(self, rel, known):
        """An exact `.opensip` anchor, asked of `.opensip` names only, and charged as a classification. A kept one's
        classification is reused by the walk loop (C1a4, remedy (a))."""
        if rel.split('/')[-1] != '.opensip':
            return False
        self.classify(rel)
        hit = self.rule.classify_path(rel, set(known), self.members)
        anchor = hit is not None and hit[1] == 'opensip-custody-state'
        if not anchor:
            self.reused.add(rel)
        return anchor

    def ignored(self, rel):
        return any(rel == p or rel.startswith(p + '/') for p in self.ignore)

    def enter(self, rel, known):
        self.add(self.c['LISTING'][:3])
        names = self.t.children.get(rel, [])
        vo, ve, vb = self.c['VISIT']
        self.add((vo, ve, vb), len(names) + 2)  # `.` and `..` are visited too
        co, ce, two, tworec = self.c['CONVERTED_NAME']
        for name in names:
            self.add((co, ce, two * (blen(rel) + 1 + blen(name)) + tworec * self.c['RECORD']))
        # The exact `.opensip` anchors leave the listing before any observation (Codex C1A1-R1-RF-1).
        names = [n for n in names if not self.custody_anchor(join_rel(rel, n), known)]
        self.owned(len(names) * self.c['SLOT'])
        oo, oe, ob = self.c['OBS']
        for name in names:
            self.add((oo, oe, ob + blen(name)))
        pushed = False
        if 'Cargo.toml' in names and self.t.kind(join_rel(rel, 'Cargo.toml')) == 'file' and rel not in known:
            self.owned(blen(rel) + 1)
            known.add(rel)
            pushed = True
        return names, pushed

    def walk(self):
        """The predicted (objects, edges, bytes); `self.exact` after it says whether the native walk must equal it."""
        self.add(self.c['STATUS'][:3])  # the root's sample
        self.capture('')                # the root's custody
        known = set()
        stack = []
        self.owned(0)                   # the root frame
        names, pushed = self.enter('', known)
        stack.append(['', names, 0, pushed])
        while stack:
            top = stack[-1]
            rel, names, index, pushed = top
            if index == len(names):
                stack.pop()             # unit C1c-0: its Cargo root stays known (the evidence), at no charge
                continue
            top[2] += 1
            name = names[index]
            child = join_rel(rel, name)
            if child in self.reused:
                self.reused.discard(child)  # remedy (a): the anchor question's classification stands
            else:
                self.classify(child)
            if self.rule.classify_path(child, set(known), self.members) is not None or self.ignored(child):
                continue
            if self.b.is_boundary(child):  # whatever the entry now is (Codex C1A1-R1-RF-2)
                continue
            kind = self.t.kind(child)
            if kind == 'dir':
                o, e, b = self.c['OPEN_DIR']
                self.add((o, e, b + blen(name)))
                self.add(self.c['STATUS'][:3])
                self.capture(child)
                self.owned(0)
                child_names, child_pushed = self.enter(child, known)
                stack.append([child, child_names, 0, child_pushed])
            elif kind == 'file':
                if name in self.MARKERS and self.b.marker_row(rel, name):
                    continue
                o, e, b = self.c['OPEN_REG_1']
                self.add((o, e, b + blen(name)))
                self.add(self.c['STATUS'][:3])
                if name in self.MARKERS:
                    self.capture(child)
                self.handed.append((child, self.t.node(child)['text'].encode()))
            else:
                self.owned(blen(child))
        # Unit C1c-0 (LD-C1C-13): the member roots copied into the walk's evidence; the Cargo roots move.
        for member in sorted(self.members):
            self.owned(blen(member))
        self.cargo_roots = set(known)
        return tuple(self.cost)


def opener_cost(c, tree, path, acl):
    """`SnapshotRoot::open(path)`: the validator's copy (kept as the source file's path), the root's sample and
    custody, then per directory component its key, observation, open, sample and custody, then the leaf's observation,
    open and sample, and a marker's custody."""
    m = SnapshotModel(c, None, tree, None, acl_paths=acl)
    m.owned(blen(path))
    m.add(c['STATUS'][:3])
    m.capture('')
    parts, rel = path.split('/'), ''
    oo, oe, ob = c['OBS']
    for part in parts[:-1]:
        m.owned(blen(rel) + 1 + blen(part))
        sub = join_rel(rel, part)
        m.add((oo, oe, ob + blen(part)))
        o, e, b = c['OPEN_DIR']
        m.add((o, e, b + blen(part)))
        m.add(c['STATUS'][:3])
        m.capture(sub)
        rel = sub
    leaf = parts[-1]
    m.add((oo, oe, ob + blen(leaf)))
    o, e, b = c['OPEN_REG_1']
    m.add((o, e, b + blen(leaf)))
    m.add(c['STATUS'][:3])
    if leaf in SnapshotModel.MARKERS:
        m.capture(path)
    return tuple(m.cost), m.exact


def pruned_opener_cost(c, tree, path, acl):
    """Unit C1c-0 (LD-C1C-2): `open_pruned(path)`: the validator's copy (kept as the source file's path), the rule's
    temporaries, the root's sample and custody, then per directory component its key, observation, open and sample, and
    its custody only above the dependency anchor, then the leaf's observation, open and sample, with no marker custody."""
    m = SnapshotModel(c, None, tree, None, acl_paths=acl)
    m.owned(blen(path))
    parts = path.split('/')
    po, pe, ptwo, precords = c['PRUNED_CAPTURE']
    m.add((po, pe, len(parts) * ptwo + blen(path) + precords))
    m.add(c['STATUS'][:3])
    m.capture('')
    anchor = parts[:-1].index('node_modules')
    rel = ''
    oo, oe, ob = c['OBS']
    for index, part in enumerate(parts[:-1]):
        m.owned(blen(rel) + 1 + blen(part))
        sub = join_rel(rel, part)
        m.add((oo, oe, ob + blen(part)))
        o, e, b = c['OPEN_DIR']
        m.add((o, e, b + blen(part)))
        m.add(c['STATUS'][:3])
        if index < anchor:
            m.capture(sub)
        rel = sub
    leaf = parts[-1]
    m.add((oo, oe, ob + blen(leaf)))
    o, e, b = c['OPEN_REG_1']
    m.add((o, e, b + blen(leaf)))
    m.add(c['STATUS'][:3])
    return tuple(m.cost), m.exact


def pruned_opener_cases():
    """Unit C1c-0: an installed manifest at the root's dependency tree, one under a first-party directory (custody judged
    above the anchor only), and a nested package's."""
    tree = [dict(kind='dir', path='node_modules', mode='0755'), dict(kind='dir', path='node_modules/a', mode='0775'),
            dict(kind='file', path='node_modules/a/package.json', mode='0644', text='{}'),
            dict(kind='dir', path='web', mode='0755'), dict(kind='dir', path='web/node_modules', mode='0755'),
            dict(kind='dir', path='web/node_modules/b', mode='0755'),
            dict(kind='file', path='web/node_modules/b/package.json', mode='0644', text='{}'),
            dict(kind='dir', path='node_modules/a/node_modules', mode='0755'),
            dict(kind='dir', path='node_modules/a/node_modules/c', mode='0755'),
            dict(kind='file', path='node_modules/a/node_modules/c/package.json', mode='0644', text='{}')]
    return [('pruned-opener-' + p.replace('/', '-'), tree, p)
            for p in ('node_modules/a/package.json', 'web/node_modules/b/package.json', 'node_modules/a/node_modules/c/package.json')]


def opener_cases():
    """r3 (Codex C1A1-R2-RF-1): a root-level file, a nested one and a nested marker, each opened before any walk."""
    tree = [dict(kind='file', path='a.txt', mode='0644', text='a'),
            dict(kind='dir', path='src', mode='0755'), dict(kind='dir', path='src/lib', mode='0755'),
            dict(kind='file', path='src/lib/main.rs', mode='0644', text='fn main() {}'),
            dict(kind='dir', path='pkg', mode='0755'), dict(kind='file', path='pkg/package.json', mode='0644', text='{}')]
    return [('opener-' + p.replace('/', '-'), tree, p) for p in ('a.txt', 'src/lib/main.rs', 'pkg/package.json')]


def session_shapes(product):
    """The session's anchored shapes: each anchor must match its count exactly."""
    out = {}
    for name, path, pattern, count in SESSION_ANCHORS:
        hits = list(re.finditer(pattern, (product / path).read_text()))
        require(len(hits) == count, 'session anchor %s matched %d times, not %d' % (name, len(hits), count))
        out[name] = tuple(int(g.replace('_', '')) for g in hits[0].groups() if g)
    return out


def session_costs(product, c):
    """The session's terms: the shared prices must be the census's, and the rest are read from their anchors."""
    s = session_shapes(product)
    require(s['LISTING'] == c['LISTING'][:3] and s['VISIT'] == tuple(c['VISIT']), 'custody prices differ from the census')
    require(s['ATTEMPT'] == (0, 1, 0) and s['WRITE'] == (0, 1, 0), 'an attempt or a write is not one edge')
    chunk, first = s['READ_CHUNK'][0], s['FIRST_GROWTH'][0]
    current, grown = 0, 0
    while current < chunk:
        current = min(first if current == 0 else current * 2, chunk)
        grown += current
    s['BUFFER'] = (1, 0, grown)
    return s


def session_cost(c, s, handed):
    """The capture session's charge beyond the walk's, for `handed` (each (path, bytes) the walk hands, in order): the
    buffer once, the custody's opening (its ACL-judged admission and its listing), then per file its two samples, its pending entry's name and creation, its read
    attempts (one per chunk and the EOF read), its chunk writes, the commit's sample, then either the duplicate's
    unlink or the digest name, its exclusive rename and the committed set's entry, and the capture's record."""
    import hashlib as _h
    cost = [0, 0, 0]

    def add(t, k=1):
        for i in range(3):
            cost[i] += t[i] * k

    o, e = c['OWNED']
    owned = lambda n: (o, e, n + c['RECORD'])
    status = c['STATUS'][:3]
    chunk = s['READ_CHUNK'][0]
    add(s['BUFFER'])
    add(s['ACL_CAPTURE'])
    add(s['LISTING'])
    add(s['VISIT'], 2)  # `.` and `..`
    seen = set()
    for n, (_, data) in enumerate(handed):
        name = 'pending-%d' % n
        add(status)  # before
        add(owned(len(name)))
        co, ce, cb = s['CREATE_COST']
        add((co, ce, len(name) + cb))
        chunks = -(-len(data) // chunk)
        add(s['ATTEMPT'], chunks + 1)
        add(s['WRITE'], chunks)
        add(status)  # after
        add(status)  # the commit's sample
        digest = _h.sha256(data).digest()
        if digest in seen:
            uo, ue, ub = s['UNLINK_COST']
            add((uo, ue, len(name) + ub))
        else:
            seen.add(digest)
            add(owned(64))
            ro, re_, rb = s['RENAME_COST']
            add((ro, re_, len(name) + 64 + rb))
            add(owned(s['SET_ENTRY_SIZE'][0]))
        add(owned(s['CAPTURE_SIZE'][0]))
    return tuple(cost)


def generated_cases():
    """Trees that maximize single charge types: long names, a wide listing of excluded entries, a deep chain."""
    out = []
    long = 'n' * 200
    tree = [dict(kind='file', path='%s%03d' % (long, k), mode='0644', text='x') for k in range(40)]
    out.append(('wide-long-names', tree, {}))
    tree = [dict(kind='dir', path='node_modules', mode='0755')]
    tree += [dict(kind='dir', path='node_modules/%s%03d' % (long, k), mode='0755') for k in range(30)]
    tree += [dict(kind='file', path='kept.txt', mode='0644', text='k')]
    out.append(('wide-pruned-listing', tree, {}))
    tree, rel = [], ''
    for k in range(64):
        rel = join_rel(rel, 'd%02d' % k)
        tree.append(dict(kind='dir', path=rel, mode='0755'))
    tree.append(dict(kind='file', path=join_rel(rel, 'leaf.txt'), mode='0644', text='leaf'))
    out.append(('deep-chain', tree, {}))
    tree = [dict(kind='file', path='Cargo.toml', mode='0644', text='[package]\n'),
            dict(kind='dir', path='target', mode='0755'), dict(kind='file', path='target/x', mode='0644', text='x'),
            dict(kind='dir', path='src', mode='0755'), dict(kind='file', path='src/main.rs', mode='0644', text='fn main() {}'),
            dict(kind='file', path='package.json', mode='0644', text='{}'),
            dict(kind='symlink', path='link', mode='0755', target='src'),
            dict(kind='dir', path='r', mode='0755'), dict(kind='file', path='r/f', mode='0644', text='f')]
    out.append(('markers-pruned-boundary-and-link', tree, dict(nestedRepositories=['r'])))
    # r2 (Codex C1A1-R1-RF-1): the exact `.opensip` anchors at the root and a D15 member, never observed, beside an
    # ordinary nested `.opensip` that is walked.
    tree = [dict(kind='dir', path='.opensip', mode='0755'), dict(kind='file', path='.opensip/project-id.v1', mode='0644', text='p'),
            dict(kind='dir', path='m', mode='0755'), dict(kind='file', path='m/package.json', mode='0644', text='{}'),
            dict(kind='dir', path='m/.opensip', mode='0755'), dict(kind='file', path='m/.opensip/x', mode='0644', text='x'),
            dict(kind='dir', path='a', mode='0755'), dict(kind='dir', path='a/.opensip', mode='0755'),
            dict(kind='file', path='a/.opensip/kept.txt', mode='0644', text='k')]
    out.append(('opensip-anchors-root-and-member', tree, {}, ['m']))
    # r2 (Codex C1A1-R1-RF-2): boundaries that are now a file, a link and a FIFO, and a custody row that is now a file.
    tree = [dict(kind='file', path='r1', mode='0644', text='was a repository'),
            dict(kind='symlink', path='r2', mode='0755', target='r1'),
            dict(kind='fifo', path='r3', mode='0644'),
            dict(kind='file', path='c', mode='0644', text='was a custody-excluded directory'),
            dict(kind='file', path='kept.txt', mode='0644', text='k')]
    out.append(('boundaries-replaced-by-non-directories', tree,
                dict(nestedRepositories=['r1', 'r2', 'r3'],
                     custodyExcludedUnits=[dict(path='c', reason='DIRECTORY_CUSTODY:WRITABLE_BY_OTHERS')])))
    # r2 (Codex C1A1-R1-RF-4): long names three deep (about 640 bytes of path, within macOS's 1,024-byte path limit
    # under a lane's private TMPDIR), and 24 custody rows consulted for every entry.
    tree, rel = [], ''
    for k in range(3):
        rel = join_rel(rel, ('L%d' % k) + 'l' * 198)
        tree.append(dict(kind='dir', path=rel, mode='0755'))
    tree.append(dict(kind='file', path=join_rel(rel, 'package.json'), mode='0644', text='{}'))
    tree.append(dict(kind='file', path=join_rel(rel, 'f' * 40), mode='0644', text='f'))
    rows = []
    for k in range(12):
        tree.append(dict(kind='dir', path='p%02d' % k, mode='0755'))
        tree.append(dict(kind='file', path='p%02d/package.json' % k, mode='0644', text='{}'))
        tree.append(dict(kind='file', path='p%02d/s.ts' % k, mode='0644', text='s'))
        rows.append(dict(path='p%02d' % k, reason='MARKER_CUSTODY:package.json:HARD_LINKED'))
        tree.append(dict(kind='dir', path='c%02d' % k, mode='0755'))
        tree.append(dict(kind='file', path='c%02d/x' % k, mode='0644', text='x'))
        rows.append(dict(path='c%02d' % k, reason='DIRECTORY_CUSTODY:WRITABLE_BY_GROUP'))
    out.append(('long-deep-and-many-custody-rows', tree, dict(custodyExcludedUnits=rows)))
    return out


# ------------------------------------------------------------------ the VCS term (unit C1b-1; C1b plan r6, LD-C1B-6)

VCS_MARKERS = ('.git', '.hg', '.svn', '.jj')


def vcs_costs(product, c):
    shapes = {}
    for name, path, pattern in VCS_ANCHORS:
        hits = list(re.finditer(pattern, (product / path).read_text()))
        require(len(hits) == 1, 'vcs anchor %s matched %d times' % (name, len(hits)))
        shapes[name] = tuple(int(g) for g in hits[0].groups() if g)
    require(shapes['COMMIT_HEX'] == (40,), 'the commit is not 40 hexadecimal digits')
    return dict(c, VCS_PARSE=shapes['PARSE'], MEMBER_COMMIT=shapes['MEMBER_SIZE'][0],
                VCS_RECORD=dict(none=shapes['RECORD_NONE'][0], git=shapes['RECORD_GIT'][0],
                                member=shapes['RECORD_MEMBER'][0], top=shapes['RECORD_TOP'][0]))


def vcs_read_envelope(c, length, cap):
    """`read_bounded_observed` over a regular file of `length` bytes under `cap` (the D15 terms' envelope,
    `discovery_member_model.read_envelope`, over the same constants): one object, one edge per attempt, and every
    growth's full size."""
    ceiling = cap + 1
    used = size = grown = attempts = 0
    while used != ceiling:
        if used == size:
            size = min(c['CHUNK'] if size == 0 else size * c['GROWTH'], ceiling)
            grown += size
        attempts += 1
        available = min(length, size) - used
        if available == 0:
            break
        used += available
    return (c['READ_OBJECT'], c['READ_ATTEMPT_EDGE'] * attempts, grown)


class VcsModel:
    """`snapshot_vcs.rs` over one observation, each step under its owner's pricing, at the branch it takes on a scratch
    object with no ACL (the capture returns no list, so the omission premise samples a filesystem): equal to the native
    charge on the security tests' repositories."""

    def __init__(self, c):
        self.c, self.v = c, [0, 0, 0]

    def add(self, cost, times=1):
        for i in range(3):
            self.v[i] += cost[i] * times

    def open_dir(self, name_bytes):  # `open_child_directory_cost`: the name's UTF-8 bytes
        o, e, b = self.c['OPEN_DIR']
        self.add((o, e, b + name_bytes))

    def open_regular(self, name_bytes):  # `RetainedDirectory::open_regular_cost` of one component
        o, e, b = self.c['OPEN_REG_1']
        self.add((o, e, b + name_bytes))

    def status(self):
        self.add(self.c['GIT_STATUS'])

    def custody(self):
        """H's volume (`snapshot_filesystem`), then `judge_decided`: the capture and the premise's sample."""
        self.add(self.c['FS'])
        self.add(self.c['CAP'])
        self.add(self.c['FS'])

    def owned(self, length):
        o, e = self.c['OWNED']
        self.add((o, e, length + self.c['RECORD']))

    def read_file(self, name_bytes, length):
        """`read_file` of a present file: open, custody, the capped read and its charged parse."""
        self.open_regular(name_bytes)
        self.custody()
        cap = self.c['INDEX_CAP']
        self.add(vcs_read_envelope(self.c, length, cap))
        po, pe = self.c['VCS_PARSE']
        self.add((po, pe, min(length, cap)))

    def git_directory(self):
        """`.git`: opened, judged, and sampled (X2's evidence for the enclosing one, the device for a member)."""
        self.open_dir(len('.git'))
        self.custody()
        self.status()

    def resolve(self, repo):
        """`resolve` over a repository spec: `head`, `loose` {name: content} and `packed` (or absent)."""
        head = repo['head'].encode()
        self.read_file(len('HEAD'), len(head))
        if head.startswith(b'ref: '):
            target = head[5:-1].decode()
            parts = target.split('/')
            loose = repo.get('loose', {})
            # `refs` is always a directory of a test repository; the others are the loose refs' parents.
            prefixes = {'refs'} | {'/'.join(name.split('/')[:k]) for name in loose for k in range(1, name.count('/') + 1)}
            found = False
            for k in range(1, len(parts)):
                self.open_dir(blen(parts[k - 1]))
                if '/'.join(parts[:k]) not in prefixes:
                    break
                self.custody()
            else:
                if target in loose:
                    self.read_file(blen(parts[-1]), len(loose[target].encode()))
                    found = True
                else:
                    self.open_regular(blen(parts[-1]))
            if not found:
                packed = repo.get('packed')
                if packed is None:
                    self.open_regular(len('packed-refs'))
                else:
                    self.read_file(len('packed-refs'), len(packed.encode()))
        self.owned(40)  # the retained commit

    def reach(self, path):
        """`reach_member`: each segment opened, its device sampled, the four markers looked up."""
        for segment in path.split('/'):
            self.open_dir(blen(segment))
            self.status()
            for marker in VCS_MARKERS:
                o, e, b = self.c['OBS']
                self.add((o, e, b + len(marker)))

    def observe(self, case):
        if case['kind'] == 'enclosing':
            self.git_directory()
            self.resolve(case['repos'][0])
        elif case['repos']:
            self.status()  # W's device
            self.owned(len(case['repos']) * self.c['MEMBER_COMMIT'])
            for repo in case['repos']:
                self.reach(repo['at'])
                self.git_directory()
                self.resolve(repo)
        return tuple(self.v)


def vcs_payload_max(scalars, segment, widest, separator, max_segments):
    """The largest total of `widest`-byte scalars plus `separator`-byte separators over paths of at most `scalars`
    scalars, `segment` per segment and `max_segments` segments: exhaustive over the separator count."""
    return max(widest * min(scalars - s, segment * (s + 1)) + separator * s for s in range(min(scalars, max_segments)))


def vcs_record_max(c):
    """The largest `vcs-observation` record (C1b plan r6, R4-RF-1): schema 3 at 64 members, each path at the largest
    escaped payload a LogicalPath admits (4,096 scalars, 255 a segment, at most 6 bytes a scalar)."""
    r = c['VCS_RECORD']
    payload = vcs_payload_max(4096, 255, 6, 1, 4096)
    return max(r['top'] + c['MAX_MEMBERS'] * (r['member'] + payload) + c['MAX_MEMBERS'] - 1, r['git'], r['none'])


def vcs_envelope(c, head, dirs):
    """The VCS term at its dearest shapes (LD-C1B-6 as C1b plan r6 states it): 1 enclosing repository and 64 members,
    each with a `HEAD` of `head` bytes naming `dirs` directories (their names and the leaf's within `head`), the loose
    ref at its 41-byte form, `packed-refs` at INDEX_CAP and the retained commit; each member's reach at MAX_DEPTH
    segments with its names at their largest UTF-8 bytes (R5-RF-1); W's status, the member list, and the record at its
    largest canonical length. The model of what snapshot_vcs.rs charges, not a restatement of the plan's pricing."""
    m = VcsModel(c)
    reach_names = vcs_payload_max(4096, 255, 4, 0, c['MAX_DEPTH'])

    def repository(member):
        r = VcsModel(c)
        if member:
            segment = VcsModel(c)
            segment.open_dir(0)
            segment.status()
            for marker in VCS_MARKERS:
                o, e, b = c['OBS']
                segment.add((o, e, b + len(marker)))
            r.add(segment.v, c['MAX_DEPTH'])
            r.add((0, 0, reach_names))
        r.git_directory()
        r.read_file(len('HEAD'), head)
        directory = VcsModel(c)
        directory.open_dir(0)
        directory.custody()
        r.add(directory.v, dirs)
        r.read_file(0, 41)
        r.add((0, 0, head))  # the directories' and the leaf's names, within HEAD's bytes
        r.read_file(len('packed-refs'), c['INDEX_CAP'])
        r.owned(40)
        return r.v

    m.add(repository(False))
    m.add(repository(True), c['MAX_MEMBERS'])
    m.status()
    m.owned(c['MAX_MEMBERS'] * c['MEMBER_COMMIT'])
    m.owned(vcs_record_max(c))
    return tuple(m.v)


def vcs_cases():
    """The repositories snapshot_vcs_tests.rs builds and observes natively (the model control)."""
    a = '0123456789abcdef0123456789abcdef01234567'
    b = '89abcdef0123456789abcdef0123456789abcdef'
    k = 'fedcba9876543210fedcba9876543210fedcba98'
    main = 'ref: refs/heads/main\n'
    wide = '\U00010000'
    deep = '/'.join([wide * 15] * 255 + [wide * 16])
    tags = ''.join('%s refs/tags/t%06d\n' % (b, n) for n in range(400))
    return [
        dict(id='none', kind='members', repos=[], expect='none'),
        dict(id='enclosing-detached', kind='enclosing', repos=[dict(at='', head=b + '\n')], expect='git:' + b),
        dict(id='enclosing-loose', kind='enclosing',
             repos=[dict(at='', head=main, loose={'refs/heads/main': a + '\n'})], expect='git:' + a),
        dict(id='enclosing-packed-header-peel', kind='enclosing',
             repos=[dict(at='', head=main, packed='# pack-refs with: peeled fully-peeled sorted \n%s refs/heads/main\n'
                         '%s refs/tags/v1\n^%s\n' % (a, k, b))], expect='git:' + a),
        dict(id='enclosing-packed-after-absent-leaf', kind='enclosing',
             repos=[dict(at='', head=main, loose={'refs/heads/other': b + '\n'}, packed='%s refs/heads/main\n' % a)],
             expect='git:' + a),
        dict(id='enclosing-deep-loose', kind='enclosing',
             repos=[dict(at='', head='ref: refs/a/b/c/d/main\n', loose={'refs/a/b/c/d/main': k + '\n'})],
             expect='git:' + k),
        dict(id='enclosing-packed-large', kind='enclosing',
             repos=[dict(at='', head='ref: refs/tags/t000399\n', packed=tags)], expect='git:' + b),
        dict(id='members-two', kind='members',
             repos=[dict(at='crates/one', head=main, loose={'refs/heads/main': a + '\n'}),
                    dict(at='two', head=main, packed='%s refs/heads/main\n' % b)],
             expect='crates/one=%s,two=%s' % (a, b)),
        dict(id='members-deep-multibyte', kind='members',
             repos=[dict(at=deep, head=main, loose={'refs/heads/main': a + '\n'})], expect='%s=%s' % (deep, a)),
    ]


def vcs_vectors(product, c, dc):
    c = vcs_costs(product, c)
    cases = []
    for case in vcs_cases():
        predicted = VcsModel(c).observe(case)
        cases.append(dict(case, predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    # R5-RF-1: the reach's pricing over multibyte names. A path of 16 segments of 255 four-byte scalars cannot exist on
    # APFS (each name exceeds NAME_MAX's 255 bytes), so this is a pricing control: the model's reach equals the
    # platform's own cost functions over the segments.
    wide = '\U00010000'
    reach = []
    for path in ('/'.join([wide * 255] * 16), '/'.join([wide * 15] * 255 + [wide * 16])):
        m = VcsModel(c)
        m.reach(path)
        reach.append(dict(path=path, predicted=dict(objects=m.v[0], edges=m.v[1], bytes=m.v[2])))
    doc = dict(schemaVersion=1, standing='C1b-1 VCS observation charge predictions (tools/security/snapshot_ledger_model.py): '
               'the model of snapshot_vcs.rs over the repositories snapshot_vcs_tests.rs builds, each to equal the native '
               'charge, the reach pricing control, and the largest record. Design evidence, not qualification.',
               pins=[dc.pin_row(product, VCS_SOURCE)], cases=cases, reach=reach,
               recordMax=vcs_record_max(c))
    return (json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + '\n').encode()


def acl_paths(rows):
    """The tree's entries given an ACL entry: a capture of one may take the entry-list branch."""
    return {r['path'] for r in rows if r.get('acl')}


def vectors(product, arch, packages_root):
    dc = load('discovery_census', product / CENSUS)
    c, pins = snapshot_costs(product, dc)
    sc = session_costs(product, c)
    sessions = []
    wv, ref, slm, rule = dc.load_reference(product, arch, packages_root)
    body = json.loads((product / WALK_VECTORS).read_bytes())
    cases = []
    for case in body['cases']:
        if case['source'] != 'automatic' or case['expected']['status'] != 'ACCEPT':
            continue
        tree = dc.tree_of_vector(case)
        model = SnapshotModel(c, rule, tree, Boundaries(case['inventory']), acl_paths=acl_paths(case['tree']))
        predicted = model.walk()
        sessions.append((case['id'], session_cost(c, sc, model.handed), len(model.handed)))
        cases.append(dict(id=case['id'], origin='discovery-walk-vector', tree=case['tree'], inventory=case['inventory'],
                          groups=case['groups'], waive=case['waive'], foreign=case['foreign'], exact=model.exact,
                          predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    for cid, tree_rows, inventory, *rest in generated_cases():
        members = rest[0] if rest else []
        tree = dc.tree_of_vector(dict(tree=tree_rows))
        model = SnapshotModel(c, rule, tree, Boundaries(inventory), members=members, acl_paths=acl_paths(tree_rows))
        predicted = model.walk()
        sessions.append((cid, session_cost(c, sc, model.handed), len(model.handed)))
        cases.append(dict(id=cid, origin='generated', tree=tree_rows, inventory=inventory, members=members, exact=model.exact,
                          predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    require(len({x['id'] for x in cases}) == len(cases), 'duplicate case ids')
    openers = []
    for oid, tree_rows, path in opener_cases():
        predicted, exact = opener_cost(c, dc.tree_of_vector(dict(tree=tree_rows)), path, acl_paths(tree_rows))
        openers.append(dict(id=oid, tree=tree_rows, path=path, exact=exact,
                            predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    pruned_openers = []
    for oid, tree_rows, path in pruned_opener_cases():
        predicted, exact = pruned_opener_cost(c, dc.tree_of_vector(dict(tree=tree_rows)), path, acl_paths(tree_rows))
        pruned_openers.append(dict(id=oid, tree=tree_rows, path=path, exact=exact,
                                   predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    doc = dict(schemaVersion=1, standing='C1a1 snapshot walk charge predictions (tools/security/snapshot_ledger_model.py): '
               'the model of snapshot_walk.rs over the accepted automatic discovery walk vectors and generated trees, '
               'each to be an upper bound on the native walk, and equal to it where `exact` (every capture there takes '
               'the branch the model charges). Design evidence, not qualification.',
               pins=pins, cases=cases, openers=openers, prunedOpeners=pruned_openers)
    session_doc = dict(schemaVersion=1, standing='C1a2 capture-session charge predictions (tools/security/snapshot_ledger_model.py): '
                       'for each tree of ' + OUTPUT + ', the host session\'s charge beyond the walk\'s own (its buffer, '
                       'custody, reads, writes, commits and capture records), each to equal the native difference. Design '
                       'evidence, not qualification.',
                       pins=[dc.pin_row(product, p) for p in SESSION_FILES],
                       cases=[dict(id=cid, handed=handed, predicted=dict(objects=p[0], edges=p[1], bytes=p[2]))
                              for cid, p, handed in sessions])
    return ((json.dumps(doc, indent=1, sort_keys=True) + '\n').encode(),
            (json.dumps(session_doc, indent=1, sort_keys=True) + '\n').encode(),
            vcs_vectors(product, c, dc))


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    parser.add_argument('--architecture', type=Path, required=True)
    parser.add_argument('--packages-root', type=Path, required=True)
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raws = vectors(product, args.architecture.resolve(strict=True), args.packages_root.resolve(strict=True))
    for output, raw in zip((OUTPUT, SESSION_OUTPUT, VCS_OUTPUT), raws):
        target = product / output
        if args.check:
            require(target.is_file() and target.read_bytes() == raw, 'snapshot ledger vectors differ: ' + output)
        else:
            target.write_bytes(raw)
        print(('Verified ' if args.check else 'Generated ') + output)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print('Snapshot ledger model failed: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
