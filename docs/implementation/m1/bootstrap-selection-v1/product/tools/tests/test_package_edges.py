"""Isolated and real-Cargo controls for declared internal package boundaries."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

FILE = Path(__file__).resolve().parents[1] / 'check_package_edges.py'
spec = importlib.util.spec_from_file_location('edges', FILE)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


class PackageEdgesTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.inventory = {'packages': [
            {'id': 'opensip-contracts', 'kind': 'rust-library', 'path': 'crates/contracts', 'dependencies': []},
            {'id': 'opensip-host', 'kind': 'rust-library', 'path': 'crates/host', 'dependencies': ['opensip-contracts']},
            {'id': 'opensip-rust-provider', 'kind': 'rust-binary', 'path': 'providers/rust', 'dependencies': ['opensip-contracts']},
        ]}
        self.packages = []
        for row in self.inventory['packages']:
            path = self.root / row['path']
            (path / 'src').mkdir(parents=True)
            (path / 'src/lib.rs').write_text('pub fn value() -> u8 { 1 }\n')
            (path / 'Cargo.toml').write_text(f'[package]\nname="{row["id"]}"\nversion="0.1.0"\nedition="2024"\n')
            self.packages.append({'id': row['id'], 'name': row['id'], 'source': None, 'manifest_path': str(path / 'Cargo.toml'), 'targets': [{'src_path': str(path / 'src/lib.rs')}], 'dependencies': []})
        self.meta = {'packages': self.packages[:2], 'workspace_members': ['opensip-contracts', 'opensip-host'], 'workspace_default_members': ['opensip-host'], 'workspace_root': str(self.root), 'resolve': {'nodes': [{'id': x['id'], 'deps': []} for x in self.packages[:2]]}}

    def dep(self, owner, **changes):
        row = next(p for p in self.packages if p['name'] == owner)
        return {'name': owner, 'path': str(Path(row['manifest_path']).parent), 'kind': None, 'target': None, 'rename': None, 'optional': False, **changes}

    def run_check(self, lane='host'):
        return M.check(self.root, self.meta, self.inventory, lane)

    def test_allowed_declaration_and_resolution(self):
        self.packages[1]['dependencies'] = [self.dep('opensip-contracts', rename='dto')]
        with Path(self.packages[1]['manifest_path']).open('a') as stream:
            stream.write('[dependencies]\ndto={package="opensip-contracts",path="../contracts"}\n')
        self.meta['resolve']['nodes'][1]['deps'] = [{'pkg': 'opensip-contracts', 'dep_kinds': [{'kind': None, 'target': None}]}]
        result = self.run_check()
        self.assertEqual(result['declaredInternalEdges'][0]['rename'], 'dto')
        self.assertEqual(result['resolvedInternalEdges'][0]['to'], 'opensip-contracts')
        self.assertFalse(result['sourcePurityQualified'])

    def test_forbidden_normal_dev_build_optional_target_and_renamed_edges(self):
        for changes in ({}, {'kind': 'dev'}, {'kind': 'build'}, {'optional': True}, {'target': 'cfg(windows)'}, {'rename': 'harmless'}):
            with self.subTest(changes=changes):
                self.packages[0]['dependencies'] = [self.dep('opensip-host', **changes)]
                with self.assertRaisesRegex(M.BoundaryError, 'forbidden declared internal edge'):
                    self.run_check()

    def test_resolved_edge_is_checked_independently(self):
        self.meta['resolve']['nodes'][0]['deps'] = [{'pkg': 'opensip-host', 'dep_kinds': [{'kind': 'build', 'target': None}]}]
        with self.assertRaisesRegex(M.BoundaryError, 'forbidden resolved internal edge'):
            self.run_check()

    def test_workspace_inheritance_refuses(self):
        path = Path(self.packages[0]['manifest_path'])
        path.write_text('[package]\nname="opensip-contracts"\nversion.workspace=true\n')
        with self.assertRaisesRegex(M.BoundaryError, 'must not inherit workspace values'):
            self.run_check()

    def test_target_source_cannot_escape_own_package(self):
        self.packages[0]['targets'][0]['src_path'] = self.packages[1]['targets'][0]['src_path']
        with self.assertRaisesRegex(M.BoundaryError, 'target crosses package source boundary'):
            self.run_check()

    def test_registry_shadow_and_nonlocal_internal_owner_refuse(self):
        original = copy.deepcopy(self.packages[0])
        self.packages[0]['source'] = 'registry+https://github.com/rust-lang/crates.io-index'
        with self.assertRaisesRegex(M.BoundaryError, 'shadows an internal owner'):
            self.run_check()
        self.packages[0].update(original)
        self.packages[1]['dependencies'] = [self.dep('opensip-contracts', path=None)]
        with self.assertRaisesRegex(M.BoundaryError, 'local owner path'):
            self.run_check()

    def test_unknown_dependency_and_relocated_package_refuse(self):
        self.packages[1]['dependencies'] = [self.dep('opensip-contracts', name='lookalike')]
        with self.assertRaisesRegex(M.BoundaryError, 'unknown or aliased local dependency owner'):
            self.run_check()
        self.packages[1]['dependencies'] = []
        self.packages[0]['manifest_path'] = self.packages[1]['manifest_path']
        with self.assertRaisesRegex(M.BoundaryError, 'unknown or relocated local package'):
            self.run_check()

    def test_provider_workspace_is_separate(self):
        self.meta['packages'].append(self.packages[2])
        self.meta['resolve']['nodes'].append({'id': 'opensip-rust-provider', 'deps': []})
        self.meta['workspace_members'].append('opensip-rust-provider')
        with self.assertRaisesRegex(M.BoundaryError, 'host/provider boundary'):
            self.run_check()
        self.meta['workspace_members'] = ['opensip-rust-provider']
        self.meta['workspace_default_members'] = ['opensip-rust-provider']
        self.meta['workspace_root'] = str(self.root / 'providers/rust')
        self.assertTrue(self.run_check('rust-provider')['passed'])

    def test_unknown_resolve_node_and_external_local_edge_refuse(self):
        self.meta['resolve']['nodes'][0]['deps'] = [{'pkg': 'unknown', 'dep_kinds': []}]
        with self.assertRaisesRegex(M.BoundaryError, 'unresolved Cargo package id'):
            self.run_check()
        self.meta['resolve']['nodes'][0]['deps'] = []
        external = {'id': 'external', 'name': 'external', 'source': 'registry+https://github.com/rust-lang/crates.io-index'}
        self.meta['packages'].append(external)
        self.meta['resolve']['nodes'].append({'id': 'external', 'deps': [{'pkg': 'opensip-contracts', 'dep_kinds': []}]})
        with self.assertRaisesRegex(M.BoundaryError, 'external package imports a local product owner'):
            self.run_check()

    def test_stale_metadata_cannot_hide_manifest_only_dependency(self):
        with Path(self.packages[0]['manifest_path']).open('a') as stream:
            stream.write('[target.\'cfg(windows)\'.dev-dependencies]\nopensip-host={path="../host"}\n')
        with self.assertRaisesRegex(M.BoundaryError, 'forbidden manifest internal edge'):
            self.run_check()

    def test_stale_allowed_declaration_still_requires_fresh_metadata(self):
        with Path(self.packages[1]['manifest_path']).open('a') as stream:
            stream.write('[dependencies]\nopensip-contracts={path="../contracts",optional=true}\n')
        with self.assertRaisesRegex(M.BoundaryError, 'metadata internal declarations differ'):
            self.run_check()

    def test_stale_metadata_cannot_hide_legacy_dependency_tables(self):
        path = Path(self.packages[0]['manifest_path'])
        base = '[package]\nname="opensip-contracts"\nversion="0.1.0"\nedition="2021"\n'
        for table in ('build_dependencies', 'dev_dependencies', "target.'cfg(windows)'.build_dependencies", "target.'cfg(windows)'.dev_dependencies"):
            with self.subTest(table=table):
                path.write_text(base + '[' + table + ']\nopensip-host={path="../host"}\n')
                with self.assertRaisesRegex(M.BoundaryError, 'forbidden manifest internal edge'):
                    self.run_check()

    def test_real_cargo_legacy_table_with_stale_metadata(self):
        cargo = shutil.which('cargo')
        if cargo is None:
            self.skipTest('Cargo required for real metadata negative controls')
        (self.root / 'Cargo.toml').write_text('[workspace]\nresolver="3"\nmembers=["crates/contracts","crates/host"]\nexclude=["providers/rust"]\n')
        path = self.root / 'crates/contracts/Cargo.toml'
        base = '[package]\nname="opensip-contracts"\nversion="0.1.0"\nedition="2021"\n'
        path.write_text(base)
        command = [cargo, 'metadata', '--offline', '--format-version', '1', '--manifest-path', str(self.root / 'Cargo.toml')]
        before = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(before.returncode, 0, before.stderr)
        self.meta = json.loads(before.stdout)
        self.assertTrue(self.run_check()['passed'])
        path.write_text(base + "[target.'cfg(windows)'.build_dependencies]\nopensip-host={path=\"../host\"}\n")
        with self.assertRaisesRegex(M.BoundaryError, 'forbidden manifest internal edge'):
            self.run_check()
        after = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(after.returncode, 0, after.stderr)
        self.meta = json.loads(after.stdout)
        with self.assertRaisesRegex(M.BoundaryError, 'forbidden declared internal edge'):
            self.run_check()

    def test_real_cargo_disabled_feature_and_target_edges(self):
        cargo = shutil.which('cargo')
        if cargo is None:
            self.skipTest('Cargo required for real metadata negative controls')
        (self.root / 'Cargo.toml').write_text('[workspace]\nresolver="3"\nmembers=["crates/contracts","crates/host"]\nexclude=["providers/rust"]\n')
        (self.root / 'crates/host/Cargo.toml').write_text('[package]\nname="opensip-host"\nversion="0.1.0"\nedition="2024"\n')
        manifest = self.root / 'crates/contracts/Cargo.toml'
        base = '[package]\nname="opensip-contracts"\nversion="0.1.0"\nedition="2024"\n'
        cases = [
            '[dependencies]\nhidden={package="opensip-host",path="../host",optional=true}\n[features]\nreviewer-feature=["dep:hidden"]\n',
            '[target.\'cfg(windows)\'.dependencies]\nopensip-host={path="../host"}\n',
            '[build-dependencies]\nopensip-host={path="../host"}\n',
            '[dev-dependencies]\nopensip-host={path="../host"}\n',
        ]
        for fragment in cases:
            with self.subTest(fragment=fragment):
                manifest.write_text(base + fragment)
                # Disposable dependency-free fixture; resolution never touches product locks.
                run = subprocess.run([cargo, 'metadata', '--offline', '--format-version', '1', '--manifest-path', str(self.root / 'Cargo.toml')], capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.meta = json.loads(run.stdout)
                with self.assertRaisesRegex(M.BoundaryError, 'forbidden declared internal edge'):
                    self.run_check()


if __name__ == '__main__':
    unittest.main()
