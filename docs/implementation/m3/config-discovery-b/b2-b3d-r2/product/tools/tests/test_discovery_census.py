"""Unit B2-b4a's census-tool controls (B2-b4 plan r2 section 1.4): the pinned cost closure refuses a delegated-cost
drift and a planted charge, integrity refuses a `.git` component, the read envelope is the uninterrupted bound, and
a held-out entry's store is never opened. Synthetic inputs only; no T2 cache, network or environment input.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('discovery_census', ROOT / 'tools/security/discovery_census.py')
census = importlib.util.module_from_spec(spec)
spec.loader.exec_module(census)


def closure_copy(tmp):
    """A product copy holding exactly the pinned cost closure."""
    for path, _, _ in census.CLOSURE:
        target = Path(tmp) / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, target)
    return Path(tmp)


def make_store(root, files, gitlinks=()):
    """A store as the acquisition materializes it (directories 0555, files 0444, gitlinks as empty directories)."""
    for rel in gitlinks:
        (Path(root) / rel).mkdir(parents=True, exist_ok=True)
    for rel, data in files.items():
        path = Path(root) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        os.chmod(path, 0o444)
    for dirpath, dirnames, _ in os.walk(root, topdown=False):
        for name in dirnames:
            os.chmod(os.path.join(dirpath, name), 0o555)
    os.chmod(root, 0o555)


def unlock(root):
    for dirpath, dirnames, _ in os.walk(root):
        os.chmod(dirpath, 0o755)


def pins(files, gitlinks=None):
    """`gitTree` and the QD-22 digest of a file map with gitlinks, computed independently of the tool."""
    gitlinks = gitlinks or {}

    def tree(prefix):
        entries = {}
        for rel, data in list(files.items()) + [(g, None) for g in gitlinks]:
            if not rel.startswith(prefix):
                continue
            head, _, rest = rel[len(prefix):].partition('/')
            if rest:
                entries[head] = (b'40000', bytes.fromhex(tree(prefix + head + '/')), True)
            elif data is None:
                entries[head] = (b'160000', bytes.fromhex(gitlinks[rel]), False)
            else:
                entries[head] = (b'100644', hashlib.sha1(b'blob %d\0' % len(data) + data).digest(), False)
        rows = sorted(entries.items(), key=lambda kv: kv[0].encode() + (b'/' if kv[1][2] else b''))
        body = b''.join(m + b' ' + n.encode() + b'\0' + h for n, (m, h, _) in rows)
        return hashlib.sha1(b'tree %d\0' % len(body) + body).hexdigest()
    blobs = sorted(([rel, '100644', hashlib.sha256(data).hexdigest()] for rel, data in files.items()), key=lambda r: r[0].encode())
    digest = hashlib.sha256(json.dumps(blobs, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return tree(''), digest, len(blobs)


def entry(id_, files, held_out=False, gitlinks=None):
    git_tree, digest, count = pins(files, gitlinks)
    return dict(id=id_, heldOut=held_out, gitTree=git_tree, treeDigest=dict(value=digest, blobEntries=count),
                submodulePolicy=dict(policy='exclude-pinned' if gitlinks else 'none', gitlinks=[dict(path=p, commit=c) for p, c in (gitlinks or {}).items()]))


class CostClosure(unittest.TestCase):
    def test_the_pinned_closure_reads_every_constant(self):
        c = census.costs(ROOT)
        self.assertEqual(c['OBS'], (1, 1, 1 + 144))
        self.assertEqual(c['OPEN_DIR'], (2, 2, 1 + 144))
        self.assertEqual(c['LIMITS'], (1 << 20, 1 << 21, 1 << 30))

    # B2-b4b1 (plan r4 section 2.1, RF-1): the size inventory is closed by rule.
    def test_the_anchors_name_exactly_the_size_inventory(self):
        named = set()
        for _, path, pattern in census.ANCHORS:
            hit = census.re.search(pattern, (ROOT / path).read_text())
            named |= set(census.SIZE_OF.findall(hit.group(0)))
        self.assertEqual(named, set(census.SIZES))

    def test_a_formula_naming_an_unpinned_size_refuses(self):
        sizes = {k: v for k, v in census.SIZES.items() if k != 'usize'}
        with self.assertRaisesRegex(ValueError, 'cost anchor CLASSIFY names an unpinned size: usize'):
            census.costs(ROOT, sizes)

    def test_a_delegated_status_cost_drift_refuses(self):
        # `status_read_cost` changes; the calling expression in directory_open.rs does not.
        with tempfile.TemporaryDirectory() as tmp:
            product = closure_copy(tmp)
            path = product / 'crates/platform/src/filesystem/path_binding.rs'
            text = path.read_text()
            old = 'pub(super) fn status_read_cost() -> crate::WorkCost {\n    crate::WorkCost {\n        objects: 0,\n        edges: 1,'
            self.assertEqual(text.count(old), 1)
            path.write_text(text.replace(old, old.replace('edges: 1,', 'edges: 2,')))
            with self.assertRaisesRegex(ValueError, 'cost closure changed: crates/platform/src/filesystem/path_binding.rs'):
                census.costs(product)

    def test_a_planted_charge_outside_every_anchor_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            product = closure_copy(tmp)
            path = product / 'crates/security/src/custody/discovery_walk.rs'
            text = path.read_text()
            old = '        self.listed.insert(start.rel.clone());\n'
            self.assertEqual(text.count(old), 1)
            path.write_text(text.replace(old, old + '        work.charge::<WalkRefusal>(owned(0))?;\n'))
            with self.assertRaisesRegex(ValueError, 'cost closure changed: crates/security/src/custody/discovery_walk.rs'):
                census.costs(product)

    def test_an_anchor_that_stops_matching_refuses(self):
        # With the pin bypassed, a changed anchor alone still refuses: no constant is ever guessed.
        with tempfile.TemporaryDirectory() as tmp:
            product = closure_copy(tmp)
            path = product / 'crates/security/src/custody/discovery_walk.rs'
            text = path.read_text()
            path.write_text(text.replace('    objects: 2,\n    edges: 3,\n    bytes: 1024,', '    objects: 2,\n    edges: 4,\n    bytes: 1024,'))
            saved = census.CLOSURE
            census.CLOSURE = tuple((p, len((product / p).read_bytes()), hashlib.sha256((product / p).read_bytes()).hexdigest()) for p, _, _ in saved)
            try:
                self.assertEqual(census.costs(product)['LISTING'], (2, 4, 1024, 0))
                path.write_text(text.replace('const LISTING: WorkCost', 'const LISTING_COST: WorkCost'))
                census.CLOSURE = tuple((p, len((product / p).read_bytes()), hashlib.sha256((product / p).read_bytes()).hexdigest()) for p, _, _ in saved)
                with self.assertRaisesRegex(ValueError, 'cost anchor LISTING matched 0 times'):
                    census.costs(product)
            finally:
                census.CLOSURE = saved


class ReadEnvelope(unittest.TestCase):
    def test_the_uninterrupted_envelope(self):
        c = census.costs(ROOT)
        ceiling = c['MAX_CONFIG_BYTES'] + 1
        # Bytes: each growth's full size, 4096 doubling to the ceiling (4 MiB + 1): 4096 * (2^11 - 1) = 8,384,512
        # through 4 MiB, then the ceiling itself.
        top = 8384512 + ceiling
        for length, attempts, grown in [(0, 1, 4096), (1, 2, 4096), (4095, 4096, 4096), (4096, 4097, 4096 + 8192), (ceiling - 1, ceiling, top),
                                        (ceiling, ceiling + 1, top), (ceiling + 10, ceiling + 1, top)]:
            self.assertEqual(census.read_envelope(c, length), (1, attempts, grown, 0), length)


class Integrity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        unlock(self.tmp)
        shutil.rmtree(self.tmp)

    def test_a_verified_store_gives_its_tree(self):
        files = {'Cargo.toml': b'[package]\n', 'src/lib.rs': b''}
        root = os.path.join(self.tmp, 's')
        make_store(root, files)
        tree = census.verified_tree(root, entry('e', files))
        self.assertEqual(sorted(tree.nodes), ['', 'Cargo.toml', 'src', 'src/lib.rs'])

    def test_a_git_component_refuses(self):
        files = {'a/.git': b'gitdir: x\n', 'Cargo.toml': b''}
        root = os.path.join(self.tmp, 's')
        make_store(root, files)
        with self.assertRaisesRegex(ValueError, 'a .git path component in a T2 tree: a/.git'):
            census.verified_tree(root, entry('e', files))

    def test_an_extra_file_or_a_changed_byte_refuses(self):
        files = {'Cargo.toml': b'[package]\n'}
        root = os.path.join(self.tmp, 's')
        make_store(root, dict(files, extra=b''))
        with self.assertRaisesRegex(ValueError, 'gitTree mismatch'):
            census.verified_tree(root, entry('e', files))

    # r2 (Codex B2B4A-R1-RF-2): a gitlink placeholder is an empty 0555 store directory.
    def gitlink_store(self):
        files, links = {'Cargo.toml': b''}, {'ext/sub': 'ab' * 20}
        root = os.path.join(self.tmp, 's')
        make_store(root, files, links)
        return root, entry('e', files, gitlinks=links)

    def test_an_empty_0555_gitlink_placeholder_passes(self):
        root, e = self.gitlink_store()
        self.assertEqual(census.verified_tree(root, e).kind('ext/sub'), 'dir')

    def test_a_writable_nonempty_or_symlink_gitlink_placeholder_refuses(self):
        for change in ('writable', 'nonempty', 'symlink'):
            with self.subTest(change):
                root, e = self.gitlink_store()
                place = os.path.join(root, 'ext/sub')
                os.chmod(os.path.join(root, 'ext'), 0o755)
                if change == 'writable':
                    os.chmod(place, 0o755)
                elif change == 'nonempty':
                    os.chmod(place, 0o755)
                    Path(place, 'x').write_bytes(b'')
                    os.chmod(place, 0o555)
                else:
                    os.rmdir(place)
                    os.symlink('/tmp', place)
                os.chmod(os.path.join(root, 'ext'), 0o555)
                with self.assertRaisesRegex(ValueError, 'gitlink placeholder is not an empty 0555 directory: ext/sub'):
                    census.verified_tree(root, e)
                unlock(self.tmp)
                shutil.rmtree(root)

    def test_a_held_out_store_is_never_opened(self):
        readable = {'Cargo.toml': b'[package]\n'}
        store = os.path.join(self.tmp, 'store')
        os.mkdir(store)
        good = entry('readable', readable)
        make_store(os.path.join(store, good['treeDigest']['value']), readable)
        # A held-out entry whose digest names a planted directory: never stat'ed, listed or joined.
        planted = entry('held', {'secret': b'x'}, held_out=True)
        os.mkdir(os.path.join(store, planted['treeDigest']['value']))
        with self.assertRaisesRegex(ValueError, 'held-out entries are never opened: held'):
            census.store_path(store, planted)
        seen = []
        real = (os.lstat, os.scandir, os.listdir, os.readlink, open)

        def spy(fn):
            def call(path, *a, **k):
                seen.append(os.fspath(path))
                return fn(path, *a, **k)
            return call
        os.lstat, os.scandir, os.listdir, os.readlink = (spy(f) for f in real[:4])
        census.open = spy(open)
        try:
            for e in [good, planted]:
                if e['heldOut'] is False:
                    census.verified_tree(census.store_path(store, e), e)
        finally:
            os.lstat, os.scandir, os.listdir, os.readlink = real[:4]
            del census.open
        self.assertTrue(seen)
        self.assertFalse([p for p in seen if planted['treeDigest']['value'] in p])


class Workspaces(unittest.TestCase):
    """r2 (Codex B2B4A-R1-RF-1): the overlay record, its pins, and the exact mount-to-store mapping."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.cache = os.path.join(self.tmp, 'cache')
        self.store = os.path.join(self.cache, 'store')
        os.makedirs(self.store)
        fa, fb = {'Cargo.toml': b'[package]\n'}, {'package.json': b'{}'}
        self.ea, self.eb = entry('ea', fa), entry('eb', fb)
        for e, files in ((self.ea, fa), (self.eb, fb)):
            make_store(census.store_path(self.store, e), files)
        overlay = dict(workspace='ws', members=[dict(entry='ea', mount='a', treeDigest=self.ea['treeDigest']['value']),
                                                dict(entry='eb', mount='b', treeDigest=self.eb['treeDigest']['value'])], links={})
        self.raw = census.canonical(overlay)
        self.ws = dict(id='ws', heldOut=False, memberIds=['ea', 'eb'], overlay=overlay, overlayDigest=hashlib.sha256(self.raw).hexdigest())
        self.manifest = dict(repositories=[self.ea, self.eb], workspaces=[self.ws])
        self.arch = Path(self.tmp, 'arch')
        archived = self.arch / census.OVERLAYS / 'ws/workspace-overlay.json'
        archived.parent.mkdir(parents=True)
        archived.write_bytes(self.raw)
        self.root = os.path.join(self.cache, 'workspaces/ws')
        os.makedirs(self.root)
        Path(self.root, 'workspace-overlay.json').write_bytes(self.raw)
        os.symlink(census.store_path(self.store, self.ea), os.path.join(self.root, 'a'))
        os.symlink(census.store_path(self.store, self.eb), os.path.join(self.root, 'b'))
        self.trees = {e['id']: census.verified_tree(census.store_path(self.store, e), e) for e in (self.ea, self.eb)}

    def tearDown(self):
        unlock(self.tmp)
        shutil.rmtree(self.tmp)

    def verify(self):
        return census.verified_workspace(self.cache, self.arch, self.store, self.ws, self.manifest, self.trees)

    def test_a_pinned_overlay_gives_its_members_in_mount_order(self):
        _, members, raw = self.verify()
        self.assertEqual([m for m, _ in members], ['a', 'b'])
        self.assertEqual(raw, self.raw)

    def test_a_renamed_mount_refuses(self):
        os.rename(os.path.join(self.root, 'a'), os.path.join(self.root, 'node_modules'))
        with self.assertRaisesRegex(ValueError, 'the overlay mounts differ from its record: ws'):
            self.verify()

    def test_swapped_mount_targets_refuse(self):
        for m, e in (('a', self.eb), ('b', self.ea)):
            os.remove(os.path.join(self.root, m))
            os.symlink(census.store_path(self.store, e), os.path.join(self.root, m))
        with self.assertRaisesRegex(ValueError, 'an overlay mount links elsewhere: a'):
            self.verify()

    def test_an_altered_overlay_record_refuses(self):
        Path(self.root, 'workspace-overlay.json').write_bytes(self.raw.replace(b'"links":{}', b'"links":{"x":{}}'))
        with self.assertRaisesRegex(ValueError, 'the overlay record differs from its pins: ws'):
            self.verify()

    def test_a_symlink_overlay_root_refuses(self):
        real = os.path.join(self.cache, 'workspaces/real')
        os.rename(self.root, real)
        os.symlink(real, self.root)
        with self.assertRaisesRegex(ValueError, 'the overlay root is not a directory'):
            self.verify()


if __name__ == '__main__':
    unittest.main()
