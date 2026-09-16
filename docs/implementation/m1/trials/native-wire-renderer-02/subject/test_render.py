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


if __name__ == '__main__':
    unittest.main()
