"""Renderer refusal and exact-label probes, not owner semantic conformance."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('renderer', HERE / 'render.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
OWNER = json.loads((HERE / 'inputs/wire-carriers.v1.json').read_bytes())


class Rendering(unittest.TestCase):
    def test_repeated_generation_and_namespace_coverage(self):
        a = renderer.Renderer(OWNER)
        b = renderer.Renderer(copy.deepcopy(OWNER))
        self.assertEqual(a.run(), b.run())
        self.assertEqual(len(a.externs), 23)
        self.assertEqual(len(a.names), 67)

    def test_reference_and_operator_refusal(self):
        for ty in [{'t': 'float'}, {'t': 'ref', 'ref': 'Unknown'}]:
            with self.assertRaises(ValueError):
                renderer.Renderer(OWNER).kind(ty, 'Probe')

    def test_generated_names_cannot_alias(self):
        r = renderer.Renderer(OWNER)
        r.reserve('Ts2Private')
        for name in ['Ts2Private', 'Ts2FrameV2']:
            with self.assertRaises(ValueError):
                r.reserve(name)
        with self.assertRaises(ValueError):
            r.kind({'t': 'text', 'enum': ['a-b', 'a b']}, 'Enum')

    def test_field_names_cannot_alias(self):
        members = [dict(name=n, type={'t': 'uint64'}, presence='required') for n in ['fooBar', 'fooBAR']]
        with self.assertRaises(ValueError):
            renderer.Renderer(OWNER).fields(members, 'Record')

    def test_variant_fields_are_complete(self):
        owner = copy.deepcopy(OWNER)
        owner['records']['Ts2SnapshotEntryV1']['variants']['file'].pop('linkTarget')
        with self.assertRaises(ValueError):
            renderer.Renderer(owner).run()

    def test_rust_label_escape_and_keyword(self):
        self.assertEqual(renderer.rust_string('\b\f\n"\\'), '"\\u{8}\\u{c}\\u{a}\\"\\\\"')
        self.assertEqual(renderer.snake('type'), 'r#type')
        for keyword in ['if', 'true', 'else', 'while', 'try', 'box']:
            self.assertEqual(renderer.snake(keyword), 'r#' + keyword)
        self.assertEqual(renderer.pascal('self'), 'ValueSelf')

    def test_variant_may_not_redeclare_tag_or_add_complex_member(self):
        for replacement in ['tag', 'complex']:
            owner = copy.deepcopy(OWNER)
            body = owner['records']['Ts2SnapshotEntryV1']['variants']['file']
            if replacement == 'tag':
                body['kind'] = {'t': 'text', 'nfc': True}
            else:
                body['path'] = {'t': 'array', 'items': {'t': 'text', 'nfc': True}, 'minItems': '0', 'order': 'sequence'}
            with self.assertRaisesRegex(ValueError, 'redeclares discriminator|complex tagged-record'):
                renderer.Renderer(owner).run()

    def test_uint_literals_and_text_choice_ambiguity_refuse(self):
        for value in ['18446744073709551616', '-1', '01', 0, True]:
            owner = copy.deepcopy(OWNER)
            owner['records']['Ts2SnapshotSealV1']['members'][2]['type'] = {'t': 'uint64', 'const': value}
            with self.assertRaisesRegex(ValueError, 'uint64 literal'):
                renderer.Renderer(owner)
        owner = copy.deepcopy(OWNER)
        owner['scalars']['Ts2NfcText']['type'].update(const='a', enum=['a'])
        with self.assertRaisesRegex(ValueError, 'simultaneous text'):
            renderer.Renderer(owner)

    def test_envelope_layout_and_payload_position_refuse(self):
        for change in ['tag', 'outside', 'optional', 'table']:
            owner = copy.deepcopy(OWNER)
            members = owner['records']['Ts2FrameV2']['members']
            if change == 'tag':
                members[1]['name'] = 'renamedTag'
            elif change == 'outside':
                owner['records']['Ts2SnapshotSealV1']['members'][0]['type'] = {'t': 'frame-payload', 'protocol': 'typescript-semantic'}
            elif change == 'optional':
                members[0]['presence'] = 'optional'
            else:
                members[1]['type']['enum'].remove('Hello')
            with self.assertRaisesRegex(ValueError, 'envelope members|outside declared|header does not match'):
                renderer.Renderer(owner)

    def test_frame_and_record_variants_cannot_alias(self):
        owner = copy.deepcopy(OWNER)
        frames = owner['protocols']['typescript-semantic']['frames']
        frames.append(dict(frameType='FactBatch0', direction='worker-to-host', workerTerminal=False,
                           payload={'t': 'ref', 'ref': 'Ts2FactBatchV1'}))
        owner['records']['Ts2FrameV2']['members'][1]['type']['enum'].append('FactBatch0')
        with self.assertRaisesRegex(ValueError, 'frame variant collision'):
            renderer.Renderer(owner).run()
        owner = copy.deepcopy(OWNER)
        variants = owner['records']['Ts2AnchorRefV1']['variants']
        variants['source span'] = variants.pop('fact-ref')
        with self.assertRaisesRegex(ValueError, 'record variant collision'):
            renderer.Renderer(owner).run()

    def test_all_frame_payload_positions_use_scalar_validation(self):
        malformed = [
            {'t': 'uint64', 'const': '18446744073709551616'},
            {'t': 'uint64', 'const': '-1'},
            {'t': 'frame-payload', 'protocol': 'typescript-semantic'},
            {'t': 'text', 'const': 'a', 'enum': ['a']},
            {'t': 'text', 'enum': []},
            {'t': 'bool', 'const': 1},
        ]
        for payload in malformed:
            for selected in [False, True]:
                owner = copy.deepcopy(OWNER)
                owner['protocols']['typescript-semantic']['frames'][0]['payload'] = (
                    {'select': 'negotiated-target-attribution-v2', 'alternatives': {'false': payload, 'true': {'t': 'null'}}}
                    if selected else payload)
                with self.assertRaises(ValueError):
                    renderer.Renderer(owner)

    def test_tagged_member_order_variant_count_and_envelope_sequence(self):
        for change in ['order', 'variant', 'sequence']:
            owner = copy.deepcopy(OWNER)
            record = owner['records']['Ts2SnapshotEntryV1']
            if change == 'order':
                record['memberOrder'].append(record['discriminator'])
            elif change == 'variant':
                record['variants'].pop('symlink')
            else:
                owner['records']['Ts2FrameV2']['members'][2]['type'] = {'t': 'text'}
            with self.assertRaisesRegex(ValueError, 'duplicate member order|two variants|sequence type'):
                renderer.Renderer(owner).run()

    def test_selection_shape_is_closed_and_frames_cannot_disappear(self):
        good = {'select': 'negotiated-target-attribution-v2', 'alternatives': {
            'false': {'t': 'ref', 'ref': 'Ts2FactBatchV1'},
            'true': {'t': 'ref', 'ref': 'Ts2FactBatchV3'}}}
        cases = [
            None, [], {}, {'alternatives': good['alternatives']},
            {'select': 'unknown', 'alternatives': good['alternatives']},
            {**good, 'selector': 'ignored'},
            {**good, 'alternatives': {}},
            {**good, 'alternatives': {'false': {'t': 'null'}}},
            {**good, 'alternatives': {**good['alternatives'], 'extra': {'t': 'null'}}},
            {**good, 'alternatives': {'a': {'t': 'null'}, 'b': {'t': 'null'}}},
            {**good, 'alternatives': {'false': good, 'true': {'t': 'null'}}},
            {**good, 't': 'null'},
            {**good, 'alternatives': []},
        ]
        for payload in [good, *cases]:
            owner = copy.deepcopy(OWNER)
            frame = next(f for f in owner['protocols']['typescript-semantic']['frames'] if f['frameType'] == 'FactBatch')
            frame['payload'] = payload
            if payload is good:
                rust, ts = renderer.Renderer(owner).run()
                self.assertIn('FactBatch0(Box<Ts2FactBatchV1>)', rust)
                self.assertIn('FactBatch1(Box<Ts2FactBatchV3>)', rust)
                self.assertEqual(ts.split('export type Ts2FrameV2 = ', 1)[1].split('\nexport ', 1)[0].count('"frameType": "FactBatch"'), 2)
            else:
                with self.assertRaisesRegex(ValueError, 'selection'):
                    renderer.Renderer(owner).run()

    def test_selector_meaning_does_not_follow_json_object_order(self):
        ordinary = renderer.Renderer(OWNER)
        expected = ordinary.run()
        reversed_owner = copy.deepcopy(OWNER)
        for protocol in reversed_owner['protocols'].values():
            for frame in protocol['frames']:
                payload = frame['payload']
                if 'alternatives' in payload:
                    payload['alternatives'] = dict(reversed(list(payload['alternatives'].items())))
        reversed_renderer = renderer.Renderer(reversed_owner)
        self.assertEqual(reversed_renderer.run(), expected)
        self.assertEqual(reversed_renderer.selector_mappings, ordinary.selector_mappings)
        self.assertEqual(len(ordinary.selector_mappings), 8)
        ts_rows = [r for r in ordinary.selector_mappings if r['envelope'] == 'Ts2FrameV2' and r['frameType'] == 'FactBatch']
        self.assertEqual([(r['key'], r['rustVariant'], r['rustType']) for r in ts_rows],
                         [('false', 'FactBatch0', 'Ts2FactBatchV1'), ('true', 'FactBatch1', 'Ts2FactBatchV3')])
        for protocol in OWNER['protocols']:
            owner = copy.deepcopy(OWNER)
            frame = next(f for f in owner['protocols'][protocol]['frames'] if f['frameType'] == 'FactBatch')
            frame['payload']['alternatives']['true'] = copy.deepcopy(frame['payload']['alternatives']['false'])
            with self.assertRaisesRegex(ValueError, 'identical selection'):
                renderer.Renderer(owner).run()


if __name__ == '__main__':
    unittest.main()
