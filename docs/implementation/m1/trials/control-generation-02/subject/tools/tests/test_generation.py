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
    def test_control_bodies_have_distinct_private_types(self):
        _, sources, recipes, _ = self.registry()
        documents = {v[0]['schemaId']: v[2] for v in sources.values()}
        flat = P.flatten(documents, recipes[0][1])
        original = copy.deepcopy(flat)
        projection = P.name_variant_objects(P.schema_map(flat, P.rust))
        self.assertEqual(flat, original)
        bodies = [b['properties']['body'] for b in projection['definitions']['Control3Root']['oneOf']]
        self.assertEqual(len(bodies), 16)
        self.assertEqual(len({b['title'] for b in bodies}), 16)
        for body in bodies:
            self.assertIn('required', body)
        P.refuse_ambiguous_union_properties(projection)

    def test_unhandled_union_property_aliases_refuse(self):
        shapes = [
            ({'type': 'array', 'items': {'type': 'string'}}, {'type': 'array', 'items': {'type': 'integer'}}),
            ({'enum': ['a']}, {'enum': ['b']}),
            ({'type': 'string', 'maxLength': 3}, {'type': 'string', 'maxLength': 4}),
            ({'anyOf': [{'type': 'string'}]}, {'anyOf': [{'type': 'integer'}]}),
        ]
        for combiner in ('oneOf', 'anyOf'):
            for a, b in shapes:
                node = {combiner: [{'properties': {'value': a}}, {'properties': {'value': b}}]}
                for wrapped in (node, {'properties': {'nested': node}}):
                    with self.assertRaisesRegex(ValueError, 'ambiguous inline union'):
                        P.name_variant_objects({'definitions': {'Root': wrapped}})
        # Identical shapes can share a name; explicitly distinct names are safe
        # for this guarded alias class, without claiming universal Typify safety.
        for a, b in [(shapes[0][0], shapes[0][0]),
                     (dict(shapes[0][0], title='Left'), dict(shapes[0][1], title='Right'))]:
            P.name_variant_objects({'definitions': {'Root': {'oneOf': [
                {'properties': {'value': a}}, {'properties': {'value': b}}]}}})

    def test_variant_title_cannot_shadow_existing_owner(self):
        node = {'definitions': {'Root': {'oneOf': [
            {'properties': {'body': {'type': 'object', 'required': ['a']}}},
            {'properties': {'body': {'type': 'object', 'required': ['b']}}},
        ]}, 'RootVariant0Property0': {'type': 'integer'}}}
        with self.assertRaisesRegex(ValueError, 'private variant title collides'):
            P.name_variant_objects(node)

    def test_utf8_byte_bounds_on_runtime_template(self):
        import subprocess
        node = shutil.which('node')
        self.assertIsNotNone(node, 'Node is required to execute runtime regression tests')
        script = r'''
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const [root,out]=process.argv.slice(1);
const ts=require(path.join(root,'tools/contracts/node_modules/typescript'));
for(const name of ['exact-json','patterns','schema']){
 const source=fs.readFileSync(path.join(root,'tools/contracts/runtime',name+'.ts'),'utf8');
 const compiled=ts.transpileModule(source,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS},reportDiagnostics:true});
 assert.equal(compiled.diagnostics.filter(d=>d.category===ts.DiagnosticCategory.Error).length,0);
 fs.writeFileSync(path.join(out,name+'.js'),compiled.outputText);
}
const {SchemaRegistry}=require(path.join(out,'schema.js'));
const id='urn:opensip:test:utf8', dialect='https://json-schema.org/draft/2020-12/schema';let checks=0;
for(const character of ['a','é','界','🦀']){
 for(const length of [0,1,4,128]){
  const value=character.repeat(length), bytes=Buffer.byteLength(value,'utf8');
  for(const bound of [...new Set([Math.max(0,bytes-1),bytes,bytes+1])]){
   const registry=new SchemaRegistry([{$id:id,$schema:dialect,type:'string','x-maxUtf8Bytes':BigInt(bound)}]);
   assert.equal(registry.matches(id+'#',value),bytes<=bound);checks++;
  }
 }
}
for(const bound of [-1n,true,'128',null,{},[]]){
 assert.throws(()=>new SchemaRegistry([{$id:id,$schema:dialect,type:'string','x-maxUtf8Bytes':bound}]).checkEntryPoints([id+'#']), /nonnegative integer keyword required: x-maxUtf8Bytes/);checks++;
}
const scalar=new SchemaRegistry([{$id:id,$schema:dialect,type:'string',maxLength:2n,'x-maxUtf8Bytes':8n}]);
assert.equal(scalar.matches(id+'#','🦀🦀'),true);
assert.equal(scalar.matches(id+'#','aaa'),false);
assert.throws(()=>scalar.matches(id+'#','\ud800'));
console.log(JSON.stringify({checks:checks+3,passed:true}));
'''
        with tempfile.TemporaryDirectory() as output:
            result = subprocess.run([node, '-e', script, str(ROOT), output], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)['passed'])

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
        self.assertEqual(len(prepared['definitions']),587)
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
    def test_superseded_subtree_refuses(self):
        _, sources, recipes, _ = self.registry()
        options = copy.deepcopy(recipes[0][1])
        denied = next(ref for ref in options['deniedRefs'] if ref.endswith('/HelloV3'))
        owner = next(row for row in options['owners'] if row['schemaId'] == denied.split('#')[0])
        subref = denied + '/properties/protocolMajor'
        options['entryPoints'].append({'ref': subref, 'typeName': owner['namespace'] + 'ForbiddenProtocolMajor', 'module': owner['module']})
        options['entryPoints'].sort(key=lambda row: row['ref'])
        docs = {v[0]['schemaId']: copy.deepcopy(v[2]) for v in sources.values()}
        with self.assertRaisesRegex(ValueError, 'superseded'): A.validate_options(options, sources)
        with self.assertRaisesRegex(ValueError, 'superseded'): P.flatten(docs, options)
        options = copy.deepcopy(recipes[0][1])
        first = options['entryPoints'][0]['ref'].split('#')[0]
        docs[first] = {'$ref': subref}
        with self.assertRaisesRegex(ValueError, 'superseded'): P.flatten(docs, options)
    def test_nested_identity_and_dialect_refuse(self):
        _, sources, recipes, _ = self.registry()
        for key, value in [('$id', 'urn:unexpected'), ('$schema', 'http://json-schema.org/draft-07/schema#')]:
            docs = {v[0]['schemaId']: copy.deepcopy(v[2]) for v in sources.values()}
            first = recipes[0][1]['entryPoints'][0]['ref'].split('#')[0]
            docs[first] = {'properties': {'nested': {key: value}}}
            with self.assertRaisesRegex(ValueError, 'nested schema'): P.flatten(docs, recipes[0][1])
    def test_missing_ref_never_fetches(self):
        options=self.options();docs={v[0]['schemaId']:v[2] for v in self.registry()[1].values()};root=options['entryPoints'][0]['ref'].split('#')[0];docs[root]={'$ref':'https://unregistered.invalid/schema#'}
        with self.assertRaisesRegex(ValueError,'missing explicit type owner'):P.flatten(docs,options)
    def test_pattern_projection_refuses_unknown_map(self):
        with self.assertRaisesRegex((AssertionError,ValueError),''):
            P.rust({'type':'object','patternProperties':{'unknown':{}},'additionalProperties':False})
    def test_dependency_tree_changes_detected(self):
        package=self.root/'package';package.mkdir();p=package/'index.js';p.write_text('one');before=A.tree_files(package);p.write_text('two');self.assertNotEqual(before,A.tree_files(package));p.unlink();p.symlink_to(ROOT/'README.md')
        with self.assertRaisesRegex(ValueError,'symlink'):A.tree_files(package)

    def test_unknown_keywords_and_hidden_remote_refs_refuse(self):
        _,sources,recipes,_=self.registry()
        for keyword, value in [('prefixItems',[{'$ref':'https://unregistered.invalid/#'}]),
            ('dependentSchemas',{'x':{'$ref':'https://unregistered.invalid/#'}}),
            ('unevaluatedProperties',{'$ref':'https://unregistered.invalid/#'}),
            ('$dynamicRef','https://unregistered.invalid/#')]:
            docs={v[0]['schemaId']:copy.deepcopy(v[2]) for v in sources.values()}
            first=recipes[0][1]['entryPoints'][0]['ref'].split('#')[0];docs[first][keyword]=value
            with self.assertRaisesRegex(ValueError,'unsupported schema keyword'):
                P.flatten(docs,recipes[0][1])
    def test_exact_output_roles_are_required(self):
        for path,roles in [('crates/contracts/src/generated/mod.rs',['carrier','shape-validator']),
            ('apps/report/src/generated/report.ts',['module-index']),
            ('providers/typescript/src/generated/protocol.ts',['carrier','shape-validator'])]:
            doc=json.loads((ROOT/'schemas/registry.json').read_text())
            next(o for o in doc['recipes'][0]['outputs'] if o['path']==path)['roles']=roles;self.save_registry(doc)
            with self.assertRaisesRegex(G.GenerationError,'roles differ'):self.registry()
    def test_nonisolated_and_optimized_invocations_refuse(self):
        import subprocess,sys
        for flags in [[],['-I','-O'],['-I','-OO']]:
            p=subprocess.run([sys.executable,*flags,str(ROOT/'tools/generate_contracts.py'),
                '--root',str(self.root),'--generator','/nonexistent','--node','/nonexistent'],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0);self.assertIn('invoke Python with -I',p.stderr)
    def test_nested_numeric_enum_is_projected_exactly(self):
        node=P.typescript({'enum':[{'a':18446744073709551615},[1,-1]]})
        self.assertIn('18446744073709551615n',node['tsType']);self.assertIn('-1n',node['tsType'])

    def test_source_map_and_supersession_are_bound(self):
        _,sources,recipes,_=self.registry();options=recipes[0][1]
        mapping=json.loads((ROOT/'schemas/source-map.json').read_text())
        A.validate_source_map(mapping,sources,options)
        for field,value in [('declaredMajor',7),('semanticValidatorOwner','crates/host/src/wrong.rs'),('module','identity')]:
            changed=copy.deepcopy(mapping);changed['sources'][0][field]=value
            with self.assertRaisesRegex(ValueError,'source map .* differs'):A.validate_source_map(changed,sources,options)
        changed=copy.deepcopy(options);changed['deniedRefs']=[]
        with self.assertRaisesRegex(ValueError,'must remain superseded'):A.validate_options(changed,sources)
    def test_source_prefix_and_semantic_owner_path_refuse(self):
        doc=self.registry()[0];doc['sources'][0]['semanticValidatorOwner']='../../outside';self.save_registry(doc)
        with self.assertRaisesRegex(G.GenerationError,'noncanonical'):self.registry()
        doc=json.loads((ROOT/'schemas/registry.json').read_text());doc['sources'][0]['sourcePath']='schemas/registry.json';self.save_registry(doc)
        with self.assertRaisesRegex(G.GenerationError,'outside schemas/sources'):self.registry()

    def test_python_runtime_grants_are_exact(self):
        profile=json.loads((ROOT/'tools/contracts/python-profile.json').read_text())
        G.verify_python_profile(profile)
        for change, reason in [
            (lambda d:d.update(executable=None),'Python executable/library pin'),
            (lambda d:d['files'][0].update(sha256='0'*64),'runtime changed'),
            (lambda d:d['files'][0].update(path='/private/tmp/unselected.py'),'module paths|outside selected'),
            (lambda d:d['directories'].append('/private/tmp'),'directory grants'),
            (lambda d:d.update(metadataLandmark='/private/etc/passwd'),'landmark'),
            (lambda d:d.update(schemaVersion=True),'unselected Python'),
        ]:
            changed=copy.deepcopy(profile);change(changed)
            with self.assertRaisesRegex(G.GenerationError,reason):G.verify_python_profile(changed)

    def test_confinement_runtime_is_selected_and_pinned(self):
        value=json.loads((ROOT/'tools/contracts/generator-closure.json').read_text())['confinement']
        G.verify_confinement(value)
        for change,reason in [
            (lambda d:d.update(runtimeFiles=None),'must be a list'),
            (lambda d:d['runtimeFiles'][0].update(sha256='0'*64),'runtime changed'),
            (lambda d:d.update(sandboxExecutable=None),'confinement runtime pin'),
            (lambda d:d.update(timeoutSeconds=0),'unselected generator child'),
        ]:
            changed=copy.deepcopy(value);change(changed)
            with self.assertRaisesRegex(G.GenerationError,reason):G.verify_confinement(changed)

if __name__=='__main__':unittest.main()
