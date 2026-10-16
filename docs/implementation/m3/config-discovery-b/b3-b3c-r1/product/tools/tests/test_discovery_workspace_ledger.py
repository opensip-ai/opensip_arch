"""Unit B3-b3c's workspace-ledger controls (B3-b plan r2 section 4.3): the D15 shape of a T2 workspace (each member a
conventional Git repository, the reader carrier rendered from the overlay, none for Python), both declaration branches
(branch A admitting every member), the full ledger as the bound census computes it, a failure returning the caps, and a
held-out workspace never read. Synthetic stores, overlays and rule; the real census model, member model and carrier
rendering; no T2 cache, network or environment input.
"""
from pathlib import Path
import copy
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_discovery_census import ROOT, census, entry, make_store, unlock  # noqa: E402


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ledger = load('discovery_workspace_ledger', 'tools/security/discovery_workspace_ledger.py')
links = load('t2_link_controls', 'tools/security/t2_link_controls.py')
C = census.costs(ROOT)
DM = census.load_member_model(ROOT)


class Rule:
    """A synthetic discovery rule: nothing is pruned, the reference's markers, and plain relative roots."""
    WORKSPACE_MARKERS = ('Cargo.toml', 'package.json', 'tsconfig.json', 'jsconfig.json')

    class RootGrammarError(ValueError):
        pass

    @staticmethod
    def classify_path(rel, cargo_roots, member_roots=()):
        return None

    @staticmethod
    def normalize_explicit_root(spec):
        if not isinstance(spec, str) or not spec or spec.startswith('/') or '..' in spec.split('/'):
            raise Rule.RootGrammarError('ROOT_GRAMMAR')
        return spec.rstrip('/')


# Three members: `lib` provides a Cargo and an npm package, `app` consumes them, `tool` provides nothing.
FILES = {
    'lib': {'Cargo.toml': b'[package]\nname = "lib"\nversion = "1.0.0"\n',
            'js/package.json': b'{"name": "lib", "version": "1.0.0"}\n', 'src/lib.rs': b''},
    'app': {'Cargo.toml': b'[package]\nname = "app"\nversion = "1.0.0"\n', 'src/main.rs': b''},
    'tool': {'setup.py': b''},
}


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.arch = Path(self.tmp, 'arch')
        self.cache = os.path.join(self.tmp, 'cache')
        self.store = os.path.join(self.cache, 'store')
        os.makedirs(self.store)
        self.entries = [entry(id_, files) for id_, files in FILES.items()]
        for e in self.entries:
            make_store(os.path.join(self.store, e['treeDigest']['value']), FILES[e['id']])
        self.workspaces = []

    def tearDown(self):
        unlock(self.tmp)
        shutil.rmtree(self.tmp)

    def workspace(self, id_, ecosystem, members, link_map, held_out=False, carrier=None):
        """A workspace overlay as the acquisition writes it: the canonical record in the cache and the archive, each
        member a symlink to its store, and (Cargo) the rendered carrier at W."""
        by_id = {e['id']: e for e in self.entries}
        overlay = dict(workspace=id_, members=[dict(entry=m, mount=m, treeDigest=by_id[m]['treeDigest']['value']) for m in members],
                       links={ecosystem: link_map} if link_map is not None else {})
        raw = census.canonical(overlay)
        ws = dict(id=id_, heldOut=held_out, ecosystem=ecosystem, memberIds=list(members), overlay=overlay,
                  overlayDigest=census.sha256(raw))
        self.workspaces.append(ws)
        if held_out:
            return ws
        root = Path(self.cache, 'workspaces', id_)
        root.mkdir(parents=True)
        (root / 'workspace-overlay.json').write_bytes(raw)
        for m in members:
            os.symlink(census.store_path(self.store, by_id[m]), root / m)
        if ecosystem == 'cargo':
            (root / '.cargo').mkdir()
            (root / '.cargo/config.toml').write_bytes(carrier if carrier is not None else links.carrier(ecosystem, link_map)[1])
        elif carrier is not None:
            (root / 'package.json').write_bytes(carrier)
        archived = self.arch / census.OVERLAYS / id_ / 'workspace-overlay.json'
        archived.parent.mkdir(parents=True, exist_ok=True)
        archived.write_bytes(raw)
        return ws

    def manifest(self):
        manifest = dict(repositories=self.entries, workspaces=self.workspaces)
        path = self.arch / census.MANIFEST
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(json.dumps(manifest, indent=1).encode())
        return manifest

    def row(self, ws, c=C):
        manifest = self.manifest()
        by_id = {e['id']: e for e in self.entries}
        trees = {m: census.verified_tree(census.store_path(self.store, by_id[m]), by_id[m]) for m in ws['memberIds']}
        return ledger.workspace_row(census, links, c, DM, Rule, self.cache, self.arch, self.store, manifest, ws, trees)

    def output(self, c=C):
        self.manifest()
        return json.loads(ledger.ledger_output(ROOT, self.arch, self.cache, c, census, links, DM, Rule))


class Shape(Fixture):
    def test_a_cargo_workspace_is_composed_as_d15_discovers_it(self):
        ws = self.workspace('ws-cargo', 'cargo', ['app', 'lib', 'tool'], {'lib': 'lib'})
        row = self.row(ws)
        raw = links.carrier('cargo', {'lib': 'lib'})[1]
        self.assertEqual(row['carrier'], dict(path='.cargo/config.toml', bytes=len(raw), sha256=census.sha256(raw)))
        self.assertEqual(row['members'], ['app', 'lib', 'tool'])
        # Branch B admits the provider its carrier places; branch A every member.
        self.assertEqual(row['branches']['automatic']['admitted'], ['lib'])
        self.assertEqual(row['branches']['configWorkspaceRoots']['admitted'], ['app', 'lib', 'tool'])
        for branch in row['branches'].values():
            self.assertGreater(branch['terms']['reader']['edges'], 0)  # the carrier was read
            self.assertGreater(branch['terms']['member']['edges'], 0)  # item 6b ran
            full, walker = branch['fullLedger'], branch['walker']
            self.assertEqual(full['objects'], walker['objects'] + sum(t['objects'] for t in branch['terms'].values()))
            self.assertEqual(full['edges'], walker['edges'] + sum(t['edges'] for t in branch['terms'].values()))
        self.assertTrue(row['passes2x'])

    def test_item_6b_is_paid_per_admitted_member(self):
        ws = self.workspace('ws-cargo', 'cargo', ['app', 'lib', 'tool'], {'lib': 'lib'})
        row = self.row(ws)
        one, three = (row['branches'][k]['terms']['member']['bytes'] for k in ('automatic', 'configWorkspaceRoots'))
        self.assertGreater(three, 2 * one)

    def test_an_npm_workspace_gains_its_rendered_carrier(self):
        ws = self.workspace('ws-npm', 'npm', ['app', 'lib'], {'lib': 'lib/js'})
        row = self.row(ws)
        raw = links.carrier('npm', {'lib': 'lib/js'})[1]
        self.assertEqual(row['carrier'], dict(path='package.json', bytes=len(raw), sha256=census.sha256(raw)))
        self.assertEqual(row['branches']['automatic']['admitted'], ['lib'])
        self.assertEqual(row['branches']['configWorkspaceRoots']['admitted'], ['app', 'lib'])

    def test_a_python_workspace_has_no_carrier_and_branch_b_admits_none(self):
        ws = self.workspace('ws-py', 'python', ['app', 'tool'], None)
        row = self.row(ws)
        self.assertIsNone(row['carrier'])
        self.assertEqual(row['branches']['automatic']['admitted'], [])
        self.assertEqual(row['branches']['automatic']['terms']['member']['edges'], 0)
        self.assertEqual(row['branches']['configWorkspaceRoots']['admitted'], ['app', 'tool'])

    def test_a_cargo_carrier_differing_from_its_rendering_refuses(self):
        ws = self.workspace('ws-cargo', 'cargo', ['app', 'lib'], {'lib': 'lib'}, carrier=b'[patch.crates-io]\n')
        with self.assertRaisesRegex(ValueError, 'differs from the cache rendering'):
            self.row(ws)

    def test_an_npm_overlay_holding_a_carrier_refuses(self):
        ws = self.workspace('ws-npm', 'npm', ['app', 'lib'], {'lib': 'lib/js'}, carrier=b'{}\n')
        with self.assertRaisesRegex(ValueError, 'holds a carrier already'):
            self.row(ws)

    def test_a_member_holding_git_or_unadmitted_in_branch_a_refuses(self):
        tree = census.Tree({'': dict(kind='dir'), 'app': dict(kind='dir'), 'app/.git': dict(kind='dir')})
        root = census.Tree({'': dict(kind='dir')})
        with self.assertRaisesRegex(ValueError, 'holds .git'):
            ledger.d15_shape(census, links, self.cache, dict(id='x', ecosystem='python'), root, [('app', census.Tree(
                {'': dict(kind='dir'), '.git': dict(kind='dir')}))])
        # Branch A must reach item 6b for every member: a mount that is not a repository refuses.
        bare = census.Tree({'': dict(kind='dir'), 'app': dict(kind='dir'), 'lib': dict(kind='dir'), 'lib/.git': dict(kind='dir')})
        with self.assertRaisesRegex(ValueError, 'did not admit every member'):
            ledger.branch_row(census, C, DM, Rule, bare, ['app', 'lib'], 'config-workspace-roots')
        self.assertEqual(ledger.branch_row(census, C, DM, Rule, tree, ['app'], 'config-workspace-roots')['admitted'], ['app'])


class Record(Fixture):
    def test_the_record_holds_and_carries_the_census_inputs(self):
        self.workspace('ws-cargo', 'cargo', ['app', 'lib', 'tool'], {'lib': 'lib'})
        self.workspace('ws-py', 'python', ['app', 'tool'], None)
        body = self.output()
        self.assertEqual([w['id'] for w in body['workspaces']], ['ws-cargo', 'ws-py'])
        self.assertEqual(body['failingWorkspaces'], [])
        self.assertEqual(body['caps'], 'recorded-margin-holds')
        self.assertEqual([t['path'] for t in body['tools']], [ledger.TOOL, ledger.CENSUS_TOOL, census.MEMBER_MODEL, ledger.LINK_TOOL])
        self.assertEqual(body['closure'], [census.pin_row(ROOT, p) for p, _, _ in census.CLOSURE])
        self.assertEqual(body['branches'], [dict(key='automatic', source='automatic'),
                                            dict(key='configWorkspaceRoots', source='config-workspace-roots')])

    def test_a_failing_branch_fails_the_workspace_and_returns_the_caps(self):
        self.workspace('ws-cargo', 'cargo', ['app', 'lib', 'tool'], {'lib': 'lib'})
        self.workspace('ws-py', 'python', ['app', 'tool'], None)
        # An edge limit under twice an item-6b session (its environment envelope alone is ARG_MAX / 3 edges): Python's
        # branch B (no member, no session) still holds; every branch that admits a member fails.
        tight = copy.deepcopy(C)
        tight['LIMITS'] = (C['LIMITS'][0], census.ENVIRONMENT_ENVELOPE[0] * 2 - 1, C['LIMITS'][2])
        body = self.output(tight)
        self.assertEqual(body['failingWorkspaces'], ['ws-cargo', 'ws-py'])
        self.assertEqual(body['caps'], 'returned-to-law')
        py = body['workspaces'][1]
        self.assertTrue(py['branches']['automatic']['fullLedger']['passes2x'])
        self.assertFalse(py['branches']['configWorkspaceRoots']['fullLedger']['passes2x'])
        self.assertFalse(py['passes2x'])

    def test_a_held_out_workspace_is_never_read(self):
        self.workspace('ws-cargo', 'cargo', ['app', 'lib'], {'lib': 'lib'})
        self.workspace('ws-held', 'cargo', ['app', 'tool'], {'app': 'app'}, held_out=True)
        body = self.output()
        self.assertEqual(body['workspaces'][1], dict(id='ws-held', status='outstanding: held-out'))
        self.assertEqual(body['failingWorkspaces'], [])


if __name__ == '__main__':
    unittest.main()
