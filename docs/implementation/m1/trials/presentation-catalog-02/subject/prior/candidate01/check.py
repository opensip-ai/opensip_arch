import copy
import hashlib
import json
from pathlib import Path
import types
import unittest
from jsonschema import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

HERE = Path(__file__).resolve().parent
pins = json.loads((HERE / 'input-pins.json').read_bytes())['files']
raws = {}
for pin in pins:
    raw = Path(pin['path']).read_bytes()
    assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'], pin['path']
    raws[pin['role']] = raw
ref = types.ModuleType('pinned_canonical')
exec(compile(raws['canonical'], 'pinned-canonical-owner', 'exec'), ref.__dict__)
modules = {}
for name in ('catalog', 'build_schema'):
    module = types.ModuleType(name)
    module.__file__ = str(HERE / (name + '.py'))
    exec(compile((HERE / (name + '.py')).read_bytes(), module.__file__, 'exec'), module.__dict__)
    modules[name] = module
catalog = modules['catalog']
schema = json.loads((HERE / 'presentation-catalog.schema.json').read_bytes())
docs = {k: json.loads(v) for k, v in raws.items() if k in ('common', 'legacy-common', 'policy', 'repair', 'invocation')}
assert modules['build_schema'].build(docs) == schema
all_docs = [*docs.values(), schema]
registry = Registry().with_resources((d['$id'], Resource(contents={k:v for k,v in d.items() if k != '$schema'}, specification=DRAFT202012)) for d in all_docs)


def fixture():
    display = {'name': 'Unused symbol', 'description': 'Static reachability; unknown callers remain explicit.', 'tags': ['static', 'unused']}
    rule = {'contributionId': 'acme.rules', 'ruleStableId': 'unused', 'semanticsMajor': 1, 'programDigest': '1'*64}
    recipe = {'contributionId': 'acme.rules', 'recipeId': 'remove-unused', 'recipeVersion': '1.0.0'}
    data = {'schemaFamily': 'opensip.presentation-catalog', 'schemaMajor': 1,
            'capabilities': [{'capabilityId': 'reachability', **copy.deepcopy(display)}],
            'rules': [{'ruleProgramRef': rule, **copy.deepcopy(display)}],
            'recipes': [{'recipeKey': recipe, **copy.deepcopy(display),
                         'selector': {'kind': 'finding-fingerprints', 'minimumTargets': 1, 'maximumTargets': 4096},
                         'parameterDescriptions': {'evidenceSource': 'Select the exact evidence Run or earlier step.', 'targets': 'Select the finding fingerprints to preview.'}}]}
    return data


def bound(data, raw=None):
    raw = ref.canonical(data) if raw is None else raw
    blob = {'path': catalog.CATALOG_PATH, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    # Synthetic already-admitted host context, NOT a signed release fixture.
    context = {'closureId': 'closure2:'+'2'*64, 'closure': {'manifestDigest': '3'*64, 'tree': [blob]},
               'tree': [{'type': 'file', 'path': blob['path'], 'sha256': blob['sha256'], 'length': blob['bytes']}],
               'trustOrigin': 'retained-generation'}
    declared = {g: {catalog.entry_key(g, row) for row in data[g]} for g in ('capabilities','rules','recipes')}
    return context, raw, declared


def admit(ctx, raw, declared):
    return catalog.admit_catalog(ctx, raw, declared, ref, schema, registry)


class CatalogTests(unittest.TestCase):
    def test_owner_schema_and_complete_positive(self):
        ref.ExactValidator.check_schema(schema)
        data = fixture(); ctx, raw, declared = bound(data)
        receipt = admit(ctx, raw, declared)
        self.assertEqual(receipt['catalog'], data)
        self.assertEqual(receipt['listing']['sha256'], hashlib.sha256(raw).hexdigest())
        selected = {g: list(keys) for g, keys in declared.items()}
        out = catalog.select_descriptions(receipt, selected, ctx['closureId'])
        self.assertEqual(out['recipes'][0]['descriptor']['recipeKey'], data['recipes'][0]['recipeKey'])
        self.assertNotIn('closureId', data['recipes'][0]['recipeKey'])

    def test_absence_empty_and_unassociated_bytes_distinct(self):
        ctx, raw, declared = bound(fixture()); ctx['tree'] = [];ctx['closure']['tree'] = []
        self.assertIsNone(admit(ctx, None, declared))
        with self.assertRaisesRegex(catalog.CatalogRefusal, 'UNASSOCIATED-BYTES'):
            admit(ctx, raw, declared)
        data = fixture()
        for group in ('capabilities','rules','recipes'):data[group] = []
        ctx, raw, declared = bound(data)
        receipt = admit(ctx, raw, declared)
        self.assertEqual(receipt['catalog']['rules'], [])
        self.assertEqual(catalog.select_descriptions(None, {}, ctx['closureId'])['reason'], 'catalog-not-retained')

    def test_selected_closure_has_no_latest_fallback(self):
        ctx, raw, declared = bound(fixture()); receipt = admit(ctx, raw, declared)
        selected = {g:list(keys) for g,keys in declared.items()}
        with self.assertRaisesRegex(catalog.CatalogRefusal, 'SELECTED-CLOSURE'):
            catalog.select_descriptions(receipt, selected, 'closure2:'+'9'*64)
        selected['capabilities'] = [('imports',)]
        out = catalog.select_descriptions(receipt, selected, ctx['closureId'])
        self.assertEqual(out['capabilities'][0]['reason'], 'descriptor-not-retained')

    def test_blob_tree_and_nonregular_refusals(self):
        for mutate, error in [
            (lambda c:c['tree'][0].update(type='symlink'), 'LISTING-TYPE'),
            (lambda c:c['tree'].append(copy.deepcopy(c['tree'][0])), 'LISTING-TYPE'),
            (lambda c:c['tree'][0].update(length=0), 'BLOB'),
            (lambda c:c['tree'][0].update(sha256='0'*64), 'BLOB'),
            (lambda c:c['closure']['tree'].clear(), 'CLOSURE-TREE'),
            (lambda c:c.update(trustOrigin='caller-verified'), 'ORIGIN')]:
            ctx, raw, declared = bound(fixture()); mutate(ctx)
            with self.assertRaisesRegex(catalog.CatalogRefusal, error):admit(ctx, raw, declared)
        ctx, raw, declared = bound(fixture())
        with self.assertRaisesRegex(catalog.CatalogRefusal, 'BYTES-UNAVAILABLE'):admit(ctx, None, declared)

    def test_present_invalid_does_not_downgrade(self):
        data = fixture()
        for raw in (b'{}', b'{"schemaMajor":1,"schemaMajor":1}', b'\xff', b'1.0', b'-0'):
            ctx, raw, declared = bound(data, raw)
            with self.assertRaises((ref.AdmissionError, ValidationError)):
                admit(ctx, raw, declared)

    def test_duplicate_and_undeclared_keys(self):
        data = fixture(); duplicate = copy.deepcopy(data['rules'][0]);duplicate['description'] = 'Different text, same rule identity.'
        data['rules'].append(duplicate);data['rules'].sort(key=ref.canonical)
        ctx, raw, declared = bound(data)
        with self.assertRaisesRegex(catalog.CatalogRefusal, 'DUPLICATE-KEY'):admit(ctx, raw, declared)
        ctx, raw, declared = bound(fixture());declared['rules'] = set()
        with self.assertRaisesRegex(catalog.CatalogRefusal, 'UNDECLARED-KEY'):admit(ctx, raw, declared)

    def test_existing_recipe_fields_only_and_no_recursive_closure_id(self):
        for mutate in [
            lambda d:d['recipes'][0]['recipeKey'].update(closureId='closure2:'+'2'*64),
            lambda d:d['recipes'][0]['parameterDescriptions'].update(force='Bypass safety'),
            lambda d:d['recipes'][0]['selector'].update(maximumTargets=4097),
            lambda d:d['recipes'][0].update(execute='rm -rf'),
            lambda d:d['recipes'][0].update(defaults={'force':True})]:
            data=fixture();mutate(data);ctx,raw,declared=bound(data)
            with self.assertRaises(ValidationError):admit(ctx,raw,declared)

    def test_text_is_preserved_and_output_owns_its_copy(self):
        data=fixture();data['rules'][0]['description']='</script><img src=x onerror=bad> 😀 e\u0301'
        ctx,raw,declared=bound(data);receipt=admit(ctx,raw,declared)
        out=catalog.select_descriptions(receipt,{g:list(k) for g,k in declared.items()},ctx['closureId'])
        self.assertEqual(out['rules'][0]['descriptor']['description'],data['rules'][0]['description'])
        out['rules'][0]['descriptor']['description']='changed'
        self.assertEqual(receipt['catalog']['rules'][0]['description'],data['rules'][0]['description'])

    def test_exact_raw_bytes_not_canonicalized_signature(self):
        data=fixture();raw=json.dumps(data,indent=2).encode();ctx,raw,declared=bound(data,raw)
        receipt=admit(ctx,raw,declared)
        self.assertNotEqual(hashlib.sha256(raw).hexdigest(),hashlib.sha256(ref.canonical(data)).hexdigest())
        self.assertEqual(receipt['listing']['sha256'],hashlib.sha256(raw).hexdigest())

    def test_profile_and_field_bounds(self):
        data=fixture();data['rules'][0]['description']='😀'*8192
        ctx,raw,declared=bound(data);admit(ctx,raw,declared)
        data['rules'][0]['description']+='x';ctx,raw,declared=bound(data)
        with self.assertRaises(ValidationError):admit(ctx,raw,declared)
        raw=b' '*(4*1024*1024+1);ctx,raw,declared=bound(fixture(),raw)
        with self.assertRaises(ref.AdmissionError):admit(ctx,raw,declared)


if __name__ == '__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CatalogTests))
    print(json.dumps({'passed':result.wasSuccessful(),'groups':result.testsRun,'pins':len(pins),'selected':False,'productQualification':False,
                      'limits':'Synthetic admitted host contexts only. No signature, manifest/platform admission, execution, renderer escaping, report integration or retention qualified.'},indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
