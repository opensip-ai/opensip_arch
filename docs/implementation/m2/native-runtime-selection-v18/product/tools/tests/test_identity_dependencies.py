"""Exact identity closure controls, including inactive optional Cargo edges."""
from pathlib import Path
import argparse
import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
import tomllib
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'check_identity_dependencies.py'
SPEC = importlib.util.spec_from_file_location('identity_dependency_check', TOOL)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class IdentityDependencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='opensip-identity-policy-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name) / 'product'
        def ignore(directory, names):
            return [n for n in names if (Path(directory) / n).is_dir() and
                    (n in ('.git', 'target', 'node_modules', '__pycache__', 'dist') or n.startswith('target-'))]
        shutil.copytree(Path(__file__).resolve().parents[2], cls.root, ignore=ignore)
        cls.policy = json.loads((cls.root / 'tools/identity/dependency-policy.json').read_bytes())
        cls.lock_bytes = (cls.root / 'Cargo.lock').read_bytes()

    def metadata(self):
        raw = subprocess.check_output([CARGO, 'metadata', '--locked', '--offline',
            '--format-version', '1', '--filter-platform', TARGET,
            '--manifest-path', str(self.root / 'Cargo.toml')], stderr=subprocess.PIPE, timeout=120)
        self.assertEqual((self.root / 'Cargo.lock').read_bytes(), self.lock_bytes)
        return json.loads(raw)

    def check(self, policy=None):
        return CHECKER.check(self.metadata(), tomllib.loads(self.lock_bytes.decode()),
                             self.policy if policy is None else policy, ARCHIVES)

    def test_selected_closure_excludes_only_inactive_optional_edges(self):
        result = self.check()
        self.assertTrue(result['passed'])
        self.assertEqual(result['dependencyCount'], 8)
        self.assertNotIn('serde_core', [r[0] for r in result['registryTuples']])
        metadata = self.metadata()
        for name in ('serde_spanned', 'toml_datetime'):
            package = next(p for p in metadata['packages'] if p['name'] == name)
            node = next(n for n in metadata['resolve']['nodes'] if n['id'] == package['id'])
            self.assertEqual(node['features'], ['alloc'])
            self.assertIn('serde_core', [edge['name'] for edge in node['deps']])

    def test_no_implicit_optional_exception(self):
        policy = copy.deepcopy(self.policy)
        for row in policy['dependencies']:
            row.pop('inactiveOptionalDependencies', None)
        with self.assertRaisesRegex(CHECKER.DependencyError, 'build/proc-macro target not selected'):
            self.check(policy)

    def test_another_workspace_member_cannot_enable_parser_serde(self):
        path = self.root / 'crates/reporting/Cargo.toml'
        before = path.read_bytes()
        try:
            # A separate table avoids depending on manifest section order.
            path.write_bytes(before + b'\n[dependencies.toml]\nversion="=0.9.9"\ndefault-features=false\nfeatures=["serde"]\n')
            # The new workspace edge changes the lock graph. Resolve only in
            # this private control, then check the exact selected source policy.
            raw = subprocess.check_output([CARGO, 'metadata', '--offline',
                '--format-version', '1', '--filter-platform', TARGET,
                '--manifest-path', str(self.root / 'Cargo.toml')], stderr=subprocess.PIPE, timeout=120)
            with self.assertRaisesRegex(CHECKER.DependencyError, 'resolved features differ'):
                CHECKER.check(json.loads(raw), tomllib.loads((self.root / 'Cargo.lock').read_text()), self.policy, ARCHIVES)
        finally:
            path.write_bytes(before)
            (self.root / 'Cargo.lock').write_bytes(self.lock_bytes)

    def test_added_identity_source_refuses(self):
        path = self.root / 'crates/identity/src/unselected.rs'
        try:
            path.write_text('pub const EXTRA: bool = true;\n')
            with self.assertRaisesRegex(CHECKER.DependencyError, 'source census differs'):
                self.check()
        finally:
            path.unlink()

    def test_only_disabled_optional_declarations_can_be_omitted(self):
        metadata = self.metadata()
        package = next(p for p in metadata['packages'] if p['name'] == 'toml_datetime')
        node = next(n for n in metadata['resolve']['nodes'] if n['id'] == package['id'])
        selected = {'inactiveOptionalDependencies': ['serde_core']}
        self.assertEqual(CHECKER.inactive_optional_edges(package, node, selected), {'serde_core'})
        for feature, expansion in [('serde', ['dep:serde_core']), ('force', ['serde_core/alloc']), ('alias', ['serde'])]:
            p, n = copy.deepcopy(package), copy.deepcopy(node)
            p['features'][feature] = expansion
            n['features'].append(feature)
            with self.subTest(feature=feature), self.assertRaisesRegex(CHECKER.DependencyError, 'is enabled'):
                CHECKER.inactive_optional_edges(p, n, selected)
        for field, value in [('optional', False), ('kind', 'build'), ('target', 'cfg(unix)')]:
            p = copy.deepcopy(package)
            next(d for d in p['dependencies'] if d['name'] == 'serde_core')[field] = value
            with self.subTest(field=field), self.assertRaises(CHECKER.DependencyError):
                CHECKER.inactive_optional_edges(p, node, selected)
        for change in ('absent', 'duplicate', 'renamed', 'build', 'target'):
            n = copy.deepcopy(node)
            edge = next(e for e in n['deps'] if e['name'] == 'serde_core')
            if change == 'absent':
                n['deps'].remove(edge)
            elif change == 'duplicate':
                n['deps'].append(copy.deepcopy(edge))
            elif change == 'renamed':
                edge['name'] = 'different_name'
            elif change == 'build':
                edge['dep_kinds'][0]['kind'] = 'build'
            else:
                edge['dep_kinds'][0]['target'] = 'cfg(unix)'
            with self.subTest(resolve=change), self.assertRaisesRegex(CHECKER.DependencyError, 'must match one unconditional normal resolve edge'):
                CHECKER.inactive_optional_edges(package, n, selected)
        for package_name, dependency in [('toml', 'serde_core'), ('winnow', 'memchr')]:
            p = next(p for p in metadata['packages'] if p['name'] == package_name)
            n = next(n for n in metadata['resolve']['nodes'] if n['id'] == p['id'])
            with self.subTest(package=package_name), self.assertRaisesRegex(CHECKER.DependencyError, 'must match one unconditional normal resolve edge'):
                CHECKER.inactive_optional_edges(p, n, {'inactiveOptionalDependencies': [dependency]})
        for names in [['serde_core', 'serde_core'], ['absent'], [None]]:
            with self.subTest(names=names), self.assertRaises(CHECKER.DependencyError):
                CHECKER.inactive_optional_edges(package, node, {'inactiveOptionalDependencies': names})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cargo', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--archives', required=True, type=Path)
    args, remaining = parser.parse_known_args()
    CARGO = str(Path(args.cargo).resolve(strict=True))
    TARGET = args.target
    ARCHIVES = args.archives
    unittest.main(argv=[__file__, *remaining])
