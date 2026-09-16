"""Dependency graph controls over captured Cargo metadata, no subprocesses."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('dependency_check',ROOT/'tools/check_dependencies.py');D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
FIXTURE=json.loads((Path(__file__).parent/'fixtures/contracts-dependencies.json').read_text())
POLICY=json.loads((ROOT/'tools/contracts/dependency-policy.json').read_text())
class DependencyTests(unittest.TestCase):
    def setUp(self):
        self.m=copy.deepcopy(FIXTURE['metadata']);self.lock=copy.deepcopy(FIXTURE['lock']);self.policy=copy.deepcopy(POLICY)
        self.root=next(row for row in self.m['packages'] if row['name']=='opensip-contracts')
        self.node=next(row for row in self.m['resolve']['nodes'] if row['id']==self.root['id'])
    def check(self):return D.check(self.m,self.lock,self.policy)
    def test_selected_closure(self):self.assertEqual(self.check()['dependencyCount'],11)
    def test_undeclared_development_dependency_even_inactive(self):
        row=copy.deepcopy(self.root['dependencies'][0]);row['kind']='dev';row['name']='unexpected';self.root['dependencies'].append(row)
        with self.assertRaisesRegex(D.DependencyError,'development dependency'):self.check()
    def test_undeclared_target_or_optional_dependency_even_inactive(self):
        for kind in ('normal','build'):
            row=copy.deepcopy(self.root['dependencies'][0]);row.update(kind=None if kind=='normal' else 'build',name='unexpected',optional=True,target='cfg(windows)');self.root['dependencies'].append(row)
            with self.assertRaisesRegex(D.DependencyError,'declared direct'):self.check()
            self.root['dependencies'].pop()
    def test_root_feature_and_external_feature_drift(self):
        self.node['features'].append('arbitrary')
        with self.assertRaisesRegex(D.DependencyError,'root features'):self.check()
        self.node['features'].clear();node=next(n for n in self.m['resolve']['nodes'] if n['id'].split('#')[-1].startswith('serde_json@'));node['features'].append('arbitrary_precision')
        with self.assertRaisesRegex(D.DependencyError,'resolved features'):self.check()
    def test_direct_feature_rename_and_source_changes(self):
        for key,value in [('features',['derive','rc']),('rename','other'),('source',None),('req','*')]:
            old=self.root['dependencies'][0][key];self.root['dependencies'][0][key]=value
            with self.assertRaisesRegex(D.DependencyError,'declared direct'):self.check()
            self.root['dependencies'][0][key]=old
    def test_inactive_forwarding_feature_refuses(self):
        self.root['features']['reviewer-rc'] = ['serde/rc']
        with self.assertRaisesRegex(D.DependencyError, 'declared contracts features'): self.check()
    def test_declared_features_policy_is_required(self):
        del self.policy['subjectDeclaredFeatures']
        with self.assertRaisesRegex(D.DependencyError, 'declared contracts features'): self.check()
    def test_checksum_substitution(self):
        next(row for row in self.lock['package'] if row['name']=='serde')['checksum']='0'*64
        with self.assertRaisesRegex(D.DependencyError,'checksum'):self.check()
    def test_build_script_or_binary_target(self):
        for kind in ['custom-build','bin']:
            self.root['targets'].append({'kind':[kind]})
            with self.assertRaisesRegex(D.DependencyError,'one library'):self.check()
            self.root['targets'].pop()
    def test_unreviewed_native_links(self):
        next(row for row in self.m['packages'] if row['name']=='serde')['links']='unexpected'
        with self.assertRaisesRegex(D.DependencyError,'native linked'):self.check()
    def test_policy_must_explicitly_declare_no_dev_dependencies(self):
        del self.policy['devDependencies']
        with self.assertRaisesRegex(D.DependencyError,'no development'):self.check()
if __name__=='__main__':unittest.main()
