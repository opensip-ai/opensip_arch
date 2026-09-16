import copy
import hashlib
import json
from pathlib import Path
import types
import unittest

HERE = Path(__file__).resolve().parent


def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


pins = json.loads((HERE / 'input-pins.json').read_bytes())['files']
for pin in pins:
    raw = Path(pin['path']).read_bytes()
    assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'], pin['role']
by_role = {pin['role']: Path(pin['path']) for pin in pins}
reference = load(by_role['canonical'], 'canonical_reference')
identity = json.loads(by_role['identity'].read_bytes())
schema = json.loads((HERE / 'configuration-disclosure.schema.json').read_bytes())
policy = json.loads((HERE / 'field-policy.json').read_bytes())
disclosure = load(HERE / 'disclosure.py', 'disclosure')
builder = load(HERE / 'build_schema.py', 'schema_builder')


def source():
    return {'analysis': {'profileId': 'secret-profile', 'capabilities': ['secret-capability'],
                         'budget': {'unit': 'work-units', 'limit': 9007199254740991}},
            'components': {}, 'discovery': {}, 'policy': {}, 'evidence': {}}


def project(config, selected_policy=None, plan=None, plan_id=None):
    if plan is None:
        plan = {'resolvedConfigDigest': hashlib.sha256(reference.canonical(config)).hexdigest()}
    return disclosure.project(plan_id or 'plan2:'+'1'*64, plan, config,
                              selected_policy or policy, reference, identity, schema)


class DisclosureTests(unittest.TestCase):
    def test_schema_is_exact_closed_owner_projection(self):
        regenerated, rules = builder.build(identity)
        self.assertEqual(regenerated, schema)
        self.assertEqual(rules, policy['fields'])
        reference.ExactValidator.check_schema(schema)
        output = project(source())
        self.assertEqual(len(output['fields']), 13)
        self.assertEqual({k for k, row in output['fields'].items() if row['state'] == 'disclosed'}, {'analysis.budget'})
        for field in ('analysis.profileId', 'analysis.capabilities', 'analysis.budget'):
            changed = copy.deepcopy(output)
            changed['fields'][field] = {'field': field, 'state': 'not-present'}
            with self.assertRaises(reference.ValidationError):
                reference.validate(schema, changed)

    def test_source_digest_and_plan_id_must_match_owned_shape(self):
        config = source()
        with self.assertRaisesRegex(disclosure.DisclosureRefusal, 'SOURCE-DIGEST'):
            project(config, plan={'resolvedConfigDigest': '0'*64})
        for bad in ('run2:'+'1'*64, 'plan2:'+'g'*64, 'plan2:'+'1'*64+'\n'):
            with self.assertRaises(reference.ValidationError):
                project(config, plan_id=bad)
        output = project(config)
        self.assertEqual(output['source']['resolvedConfigDigest'], hashlib.sha256(reference.canonical(config)).hexdigest())

    def test_sensitive_values_do_not_enter_carrier(self):
        config = source()
        config['discovery'] = {'entryPoints': ['<script>secret-entry</script>'],
                               'workspaceRoots': ['private-workspace'], 'ignorePaths': ['secret-ignore']}
        config['components'] = {'request': [{'stableId': '00000000-0000-0000-0000-000000000001', 'version': '1.0.0+secret-build'}],
                                'allowedScopes': ['project', 'global']}
        config['policy'] = {'packIds': ['secret-pack'], 'waiverIds': ['secret-waiver']}
        config['evidence'] = {'importIds': ['import2:'+'a'*64]}
        raw = reference.canonical(project(config))
        for secret in ('secret-profile', 'secret-capability', 'secret-entry', 'private-workspace', 'secret-ignore', 'secret-build', 'secret-pack', 'secret-waiver', 'import2:'+'a'*64):
            self.assertNotIn(secret.encode(), raw)
        self.assertEqual(project(config)['fields']['components.allowedScopes']['value'], ['project', 'global'])

    def test_redacted_value_noninterference_except_existing_commitment(self):
        first = source()
        first['discovery']['entryPoints'] = ['private-a']
        second = copy.deepcopy(first)
        second['analysis']['profileId'] = 'a-completely-different-private-profile'
        second['analysis']['capabilities'] = ['different-capability']
        second['discovery']['entryPoints'] = ['a-much-longer-and-different-private-path']
        a, b = project(first), project(second)
        self.assertNotEqual(a['source']['resolvedConfigDigest'], b['source']['resolvedConfigDigest'])
        del a['source']['resolvedConfigDigest']; del b['source']['resolvedConfigDigest']
        self.assertEqual(a, b)

    def test_optional_missing_and_empty_are_distinct(self):
        config = source()
        field = 'discovery.entryPoints'
        self.assertEqual(project(config)['fields'][field], {'field': field, 'state': 'not-present'})
        config['discovery']['entryPoints'] = []
        self.assertEqual(project(config)['fields'][field], {'field': field, 'state': 'redacted', 'reason': 'configuration-value-not-public', 'itemCount': 0})
        config['discovery']['entryPoints'] = ['a', 'b']
        self.assertEqual(project(config)['fields'][field]['itemCount'], 2)

    def test_public_budget_requires_exact_owned_integer(self):
        for value in (True, 1.0, 0, 9007199254740992):
            config = source(); config['analysis']['budget']['limit'] = value
            with self.assertRaises((reference.AdmissionError, reference.ValidationError)):
                project(config)
        config = source(); config['analysis']['budget']['limit'] = 1
        self.assertEqual(project(config)['fields']['analysis.budget']['value']['limit'], 1)

    def test_private_policy_cannot_widen_disclosure(self):
        changed = copy.deepcopy(policy)
        changed['fields'][0]['policy'] = 'public-closed-value'
        with self.assertRaises(reference.ValidationError):
            project(source(), selected_policy=changed)
        for edit in ('drop', 'duplicate', 'unknown'):
            changed = copy.deepcopy(policy)
            if edit == 'drop': changed['fields'].pop()
            elif edit == 'duplicate': changed['fields'].append(changed['fields'][0])
            else: changed['fields'][0]['field'] = 'analysis.secret'
            with self.assertRaisesRegex(disclosure.DisclosureRefusal, 'POLICY-COVERAGE'):
                project(source(), selected_policy=changed)

    def test_malformed_sources_and_unavailable_do_not_become_empty(self):
        values = [None, {}, {'analysis': source()['analysis']}]
        unknown = source(); unknown['analysis']['secret'] = 'not-public'; values.append(unknown)
        duplicate = source(); duplicate['analysis']['capabilities'] *= 2; values.append(duplicate)
        unordered = source(); unordered['analysis']['capabilities'] = ['z', 'a']; values.append(unordered)
        for config in values:
            with self.assertRaises(reference.ValidationError):
                project(config)

    def test_projection_owns_its_copy_and_never_changes_source(self):
        config = source(); config['components']['allowedScopes'] = ['project', 'global']
        before = copy.deepcopy(config)
        output = project(config)
        output['fields']['analysis.budget']['value']['limit'] = 3
        output['fields']['components.allowedScopes']['value'].clear()
        self.assertEqual(config, before)
        self.assertEqual(project(config)['fields']['analysis.budget']['value']['limit'], 9007199254740991)

    def test_output_has_no_unowned_or_hidden_slots(self):
        good = project(source())
        edits = []
        altered = copy.deepcopy(good); altered['rawConfig'] = source(); edits.append(altered)
        altered = copy.deepcopy(good); del altered['fields']['evidence.importIds']; edits.append(altered)
        altered = copy.deepcopy(good); altered['fields']['analysis.profileId']['raw'] = 'secret'; edits.append(altered)
        for output in edits:
            with self.assertRaises(reference.ValidationError):
                reference.validate(schema, output)


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(DisclosureTests))
    print(json.dumps({'passed': result.wasSuccessful(), 'groups': result.testsRun, 'externalPins': len(pins),
                      'selected': False, 'productQualification': False,
                      'limits': 'Projection/reference checks; source Plan/Run custody, report carrier integration and final HTML leakage checks remain required.'}, indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
