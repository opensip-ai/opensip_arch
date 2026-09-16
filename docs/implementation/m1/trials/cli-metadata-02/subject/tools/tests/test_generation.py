"""Mutation checks for source/owner admission; never execute a generator."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
G=load(ROOT/'tools/generate_contracts.py','generator_check')
A=load(ROOT/'tools/contracts/adapter.py','generator_adapter')
P=load(ROOT/'tools/contracts/prepare.py','generator_prepare')

class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        shutil.copytree(ROOT/'schemas',self.root/'schemas')
        dst=self.root/'tools/contracts';dst.mkdir(parents=True)
        shutil.copyfile(ROOT/'tools/contracts/options.json',dst/'options.json')
    def registry(self):return G.registry(self.root)
    def options(self):return self.registry()[2][0][1]
    def save_registry(self,doc):
        (self.root/'schemas/registry.json').write_text(json.dumps(doc))
    def test_valid_source_and_options(self):
        _,sources,recipes,_=self.registry();A.validate_options(recipes[0][1],sources)
        prepared=P.flatten({v[0]['schemaId']:v[2] for v in sources.values()},recipes[0][1])
        self.assertEqual(len(prepared['definitions']),586)
    def test_source_byte_change_refuses(self):
        doc=self.registry()[0];path=self.root/doc['sources'][0]['sourcePath'];path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaisesRegex(G.GenerationError,'digest mismatch'):self.registry()
    def test_rebound_wrong_document_id_refuses(self):
        doc=self.registry()[0];row=doc['sources'][0];path=self.root/row['sourcePath'];body=json.loads(path.read_text());body['$id']='wrong';path.write_text(json.dumps(body));new=hashlib.sha256(path.read_bytes()).hexdigest();old=row['sourceSha256'];row['sourceSha256']=new
        doc['recipes'][0]['sourceSha256s']=sorted(new if x==old else x for x in doc['recipes'][0]['sourceSha256s']);self.save_registry(doc)
        with self.assertRaisesRegex(G.GenerationError,'identity/dialect'):self.registry()
    def test_rebound_major_and_owner_changes_refuse(self):
        _,sources,recipes,_=self.registry();options=recipes[0][1]
        for key,value in [('declaredMajor',99),('semanticValidatorOwner','crates/host/src/wrong.rs')]:
            changed=copy.deepcopy(sources);next(iter(changed.values()))[0][key]=value
            with self.assertRaisesRegex(ValueError,'major/profile/semantic owner'):A.validate_options(options,changed)
    def test_unknown_registry_and_duplicate_outputs_refuse(self):
        for mutate,reason in [(lambda d:d.update(extra=True),'registry fields'),(lambda d:d['recipes'][0]['outputs'].append(d['recipes'][0]['outputs'][0]),'duplicate output')]:
            original=json.loads((ROOT/'schemas/registry.json').read_text());mutate(original);self.save_registry(original)
            with self.assertRaisesRegex(G.GenerationError,reason):self.registry()
    def test_output_traversal_and_source_symlink_refuse(self):
        doc=self.registry()[0];doc['recipes'][0]['outputs'][0]['path']='../escape.ts';self.save_registry(doc)
        with self.assertRaisesRegex(G.GenerationError,'noncanonical'):self.registry()
        shutil.copyfile(ROOT/'schemas/registry.json',self.root/'schemas/registry.json');doc=self.registry()[0]
        p=self.root/doc['sources'][0]['sourcePath'];p.unlink();p.symlink_to(ROOT/doc['sources'][0]['sourcePath'])
        with self.assertRaisesRegex(G.GenerationError,'symlink'):self.registry()
    def test_duplicate_json_and_float_inputs_refuse(self):
        for raw in [b'{"x":1,"x":2}',b'{"x":1.0}',b'{"x":NaN}']:
            with self.assertRaises(G.GenerationError):G.decode(raw)
    def test_duplicate_names_and_wrong_module_refuse(self):
        _,sources,recipes,_=self.registry()
        for key,value in [('typeName',recipes[0][1]['entryPoints'][0]['typeName']),('module','invalid')]:
            options=copy.deepcopy(recipes[0][1]);options['entryPoints'][1][key]=value
            with self.assertRaisesRegex(ValueError,'ownership|unique'):A.validate_options(options,sources)
    def test_superseded_root_refuses(self):
        options=self.options();options['deniedRefs']=sorted([*options['deniedRefs'],options['entryPoints'][0]['ref']])
        with self.assertRaisesRegex(ValueError,'superseded'):A.validate_options(options,self.registry()[1])
    def test_missing_ref_never_fetches(self):
        options=self.options();docs={v[0]['schemaId']:v[2] for v in self.registry()[1].values()};root=options['entryPoints'][0]['ref'].split('#')[0];docs[root]={'$ref':'https://unregistered.invalid/schema#'}
        with self.assertRaisesRegex(ValueError,'missing explicit type owner'):P.flatten(docs,options)
    def test_pattern_projection_refuses_unknown_map(self):
        with self.assertRaisesRegex((AssertionError,ValueError),''):
            P.rust({'type':'object','patternProperties':{'unknown':{}},'additionalProperties':False})
    def test_dependency_tree_changes_detected(self):
        package=self.root/'package';package.mkdir();p=package/'index.js';p.write_text('one');before=A.tree_files(package);p.write_text('two');self.assertNotEqual(before,A.tree_files(package));p.unlink();p.symlink_to(ROOT/'README.md')
        with self.assertRaisesRegex(ValueError,'symlink'):A.tree_files(package)

if __name__=='__main__':unittest.main()
