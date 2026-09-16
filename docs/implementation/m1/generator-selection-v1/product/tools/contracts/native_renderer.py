"""Inert native carrier rendering trial; no wire decoder or admission claim."""
from pathlib import Path
import argparse
import hashlib
import json
import re


SELECTOR_KEYS = {
    'negotiated-target-attribution-v2': ('false', 'true'),
    'host-phase': ('WAIT_NATIVE_CONTEXT_VERIFIED', 'ANALYZING'),
}


def rust_string(value):
    return '"' + ''.join('\\"' if c == '"' else '\\\\' if c == '\\' else
                         '\\u{' + format(ord(c), 'x') + '}' if ord(c) < 32 else c
                         for c in value) + '"'


def pascal(value):
    result = ''.join(x[:1].upper() + x[1:] for x in re.split('[^A-Za-z0-9]+', value) if x)
    if not result or result[0].isdigit():
        result = 'Value' + result
    if result == 'Self':
        result = 'ValueSelf'
    return result


def snake(value):
    result = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', value)
    result = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', result).lower()
    if result in {'self', 'super', 'crate', 'Self'}:
        return result + '_value'
    if result in {'type', 'ref', 'match', 'use', 'mod', 'pub', 'fn', 'struct', 'enum',
                  'const', 'static', 'move', 'async', 'await', 'loop', 'in', 'where',
                  'impl', 'trait', 'let', 'for', 'as', 'return', 'yield', 'dyn', 'gen',
                  'if', 'else', 'while', 'true', 'false', 'try', 'box', 'break', 'continue',
                  'extern', 'mut', 'unsafe', 'where', 'abstract', 'become', 'do', 'final',
                  'macro', 'override', 'priv', 'typeof', 'unsized', 'virtual'}:
        return 'r#' + result
    return result


RUST_HELPERS = r'''
/// Owned inert byte carrier. The bounded CBOR decoder must check major type 2
/// and declared lengths before allocation; this serde bridge is not that codec.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ByteString(Vec<u8>);
impl ByteString {
    pub fn from_vec(value: Vec<u8>) -> Self { Self(value) }
    pub fn as_slice(&self) -> &[u8] { &self.0 }
    pub fn into_vec(self) -> Vec<u8> { self.0 }
}
impl serde::Serialize for ByteString {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        serializer.serialize_bytes(&self.0)
    }
}
impl<'de> serde::Deserialize<'de> for ByteString {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Bytes;
        impl<'de> serde::de::Visitor<'de> for Bytes {
            type Value = ByteString;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                f.write_str("a byte string, not a sequence or text")
            }
            fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
                Ok(ByteString(value.to_vec()))
            }
            fn visit_byte_buf<E: serde::de::Error>(self, value: Vec<u8>) -> Result<Self::Value, E> {
                Ok(ByteString(value))
            }
        }
        // CBOR is self-describing. deserialize_byte_buf lets serde_json coerce
        // a text value into bytes; deserialize_any preserves the source kind.
        deserializer.deserialize_any(Bytes)
    }
}
fn required_value<'de, D, T>(deserializer: D) -> Result<T, D::Error>
where D: serde::Deserializer<'de>, T: serde::Deserialize<'de> {
    T::deserialize(deserializer)
}
// Tagged records do not use serde's Content buffer: it coerces empty maps to
// unit and byte strings to text. Keep each input's scalar kind until the actual
// text discriminator is known. Complex variant members are unselected here.
struct StrictMapKey(String);
impl<'de> serde::Deserialize<'de> for StrictMapKey {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Key;
        impl<'de> serde::de::Visitor<'de> for Key {
            type Value = StrictMapKey;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str("a text map key") }
            fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> { Ok(StrictMapKey(v.to_owned())) }
            fn visit_string<E: serde::de::Error>(self, v: String) -> Result<Self::Value, E> { Ok(StrictMapKey(v)) }
        }
        deserializer.deserialize_any(Key)
    }
}
enum WireScalar { Text(String), Unsigned(u64), Bytes(ByteString), Bool(bool), Null }
impl<'de> serde::Deserialize<'de> for WireScalar {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Scalar;
        impl<'de> serde::de::Visitor<'de> for Scalar {
            type Value = WireScalar;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str("a native wire scalar") }
            fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> { Ok(WireScalar::Text(v.to_owned())) }
            fn visit_string<E: serde::de::Error>(self, v: String) -> Result<Self::Value, E> { Ok(WireScalar::Text(v)) }
            fn visit_u64<E: serde::de::Error>(self, v: u64) -> Result<Self::Value, E> { Ok(WireScalar::Unsigned(v)) }
            fn visit_bytes<E: serde::de::Error>(self, v: &[u8]) -> Result<Self::Value, E> { Ok(WireScalar::Bytes(ByteString::from_vec(v.to_vec()))) }
            fn visit_byte_buf<E: serde::de::Error>(self, v: Vec<u8>) -> Result<Self::Value, E> { Ok(WireScalar::Bytes(ByteString::from_vec(v))) }
            fn visit_bool<E: serde::de::Error>(self, v: bool) -> Result<Self::Value, E> { Ok(WireScalar::Bool(v)) }
            fn visit_unit<E: serde::de::Error>(self) -> Result<Self::Value, E> { Ok(WireScalar::Null) }
        }
        deserializer.deserialize_any(Scalar)
    }
}
impl WireScalar {
    fn into_text<E: serde::de::Error>(self) -> Result<String, E> {
        match self { Self::Text(v) => Ok(v), _ => Err(E::custom("expected text scalar")) }
    }
    fn into_unsigned<E: serde::de::Error>(self) -> Result<u64, E> {
        match self { Self::Unsigned(v) => Ok(v), _ => Err(E::custom("expected unsigned scalar")) }
    }
    fn into_bytes<E: serde::de::Error>(self) -> Result<ByteString, E> {
        match self { Self::Bytes(v) => Ok(v), _ => Err(E::custom("expected byte string scalar")) }
    }
    fn into_bool<E: serde::de::Error>(self) -> Result<bool, E> {
        match self { Self::Bool(v) => Ok(v), _ => Err(E::custom("expected boolean scalar")) }
    }
    fn into_null<E: serde::de::Error>(self) -> Result<(), E> {
        match self { Self::Null => Ok(()), _ => Err(E::custom("expected null scalar")) }
    }
}
'''


class Renderer:
    def __init__(self, owner):
        self.owner = owner
        self.names = set(owner['scalars']) | set(owner['records'])
        if len(self.names) != len(owner['scalars']) + len(owner['records']):
            raise ValueError('duplicate named scalar/record')
        self.rust = []
        self.ts = []
        self.externs = set()
        self.aux = set()
        self.selector_mappings = []
        self.validate_layout()

    def validate_layout(self):
        if any(not re.fullmatch(r'(Ts2|Rust3)[A-Z][A-Za-z0-9]*', n) for n in self.names):
            raise ValueError('invalid native type name')
        allowed_payloads = set()
        for protocol_id, protocol in self.owner['protocols'].items():
            envelope = self.owner['records'].get(protocol['envelope'])
            if not envelope or envelope['kind'] != 'record':
                raise ValueError('protocol envelope is not a declared record')
            members = {m['name']: m for m in envelope['members']}
            expected_members = {'protocolMajor', 'frameType', 'sequence', 'payload'}
            if protocol_id == 'rust-semantic':
                expected_members.add('direction')
            if set(members) != expected_members or len(members) != len(envelope['members']) or any(m['presence'] != 'required' for m in members.values()):
                raise ValueError('unselected protocol envelope members')
            if members['sequence']['type'] != {'t': 'uint64'}:
                raise ValueError('unselected envelope sequence type')
            frame_names = [f['frameType'] for f in protocol['frames']]
            expected = members.get('frameType', {}).get('type', {}).get('enum', [])
            if len(frame_names) != len(set(frame_names)) or sorted(frame_names) != sorted(expected):
                raise ValueError('frameType header does not match frame table')
            if members.get('protocolMajor', {}).get('type') != {'t': 'uint64', 'const': protocol['major']}:
                raise ValueError('protocol major header differs')
            if members.get('payload', {}).get('type') != {'t': 'frame-payload', 'protocol': protocol_id}:
                raise ValueError('protocol payload header differs')
            if 'direction' in members:
                expected = members['direction']['type'].get('enum', [])
                if set(expected) != {f['direction'] for f in protocol['frames']}:
                    raise ValueError('protocol direction header differs')
            index = next(i for i, m in enumerate(envelope['members']) if m['name'] == 'payload')
            allowed_payloads.add(('records', protocol['envelope'], 'members', index, 'type'))
        def walk(value, location=()):
            if isinstance(value, dict):
                if value.get('t') == 'frame-payload' and location not in allowed_payloads:
                    raise ValueError('frame-payload outside declared envelope')
                if value.get('t') == 'text' and 'const' in value and 'enum' in value:
                    raise ValueError('unselected simultaneous text const and enum')
                if value.get('t') == 'text' and 'enum' in value:
                    choices = value['enum']
                    if not isinstance(choices, list) or not choices or any(not isinstance(v, str) for v in choices) or len(set(choices)) != len(choices):
                        raise ValueError('invalid text enum')
                if value.get('t') == 'bool' and 'const' in value and type(value['const']) is not bool:
                    raise ValueError('invalid bool const')
                if value.get('t') == 'uint64':
                    bounds = {}
                    for key in ('min', 'max', 'const'):
                        if key in value:
                            v = value[key]
                            if not isinstance(v, str) or not re.fullmatch(r'0|[1-9][0-9]*', v) or int(v) > 2**64 - 1:
                                raise ValueError('uint64 literal outside selected domain')
                            bounds[key] = int(v)
                    low, high = bounds.get('min', 0), bounds.get('max', 2**64 - 1)
                    if low > high or ('const' in bounds and not low <= bounds['const'] <= high):
                        raise ValueError('inconsistent uint64 bounds')
                for k, v in value.items():
                    walk(v, (*location, k))
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    walk(v, (*location, i))
        # Instance data outside the declarative type tables is not interpreted.
        for table in ('scalars', 'records'):
            walk(self.owner[table], (table,))
        for protocol_id, protocol in self.owner['protocols'].items():
            for index, frame in enumerate(protocol['frames']):
                payload = frame['payload']
                if not isinstance(payload, dict):
                    raise ValueError('frame payload must be a type or selection object')
                if 't' not in payload:
                    selectors = SELECTOR_KEYS
                    if set(payload) != {'select', 'alternatives'} or payload.get('select') not in selectors:
                        raise ValueError('invalid frame selection shape')
                    alternatives = payload['alternatives']
                    if not isinstance(alternatives, dict) or set(alternatives) != set(selectors[payload['select']]):
                        raise ValueError('invalid frame selection alternatives')
                    if any(not isinstance(t, dict) or 't' not in t for t in alternatives.values()):
                        raise ValueError('selection alternative must be a type object')
                elif 'alternatives' in payload or 'select' in payload or 'selector' in payload:
                    raise ValueError('type object cannot contain frame selection members')
                walk(payload, ('protocols', protocol_id, 'frames', index, 'payload'))

    def reserve(self, name):
        if name in self.names or name in self.aux:
            raise ValueError('generated type name collision: ' + name)
        self.aux.add(name)

    def kind(self, ty, context):
        tag = ty['t']
        if tag == 'ref':
            if ty['ref'] not in self.names:
                raise ValueError('unresolved native reference: ' + ty['ref'])
            return ty['ref'], ty['ref']
        if tag == 'extern':
            self.externs.add(ty['generatedType'])
            return ty['generatedType'], ty['generatedType']
        if tag == 'text':
            choices = ty.get('enum', [ty['const']] if 'const' in ty else None)
            if choices:
                name = context + 'Value'
                self.reserve(name)
                variants = [pascal(v) for v in choices]
                if len(set(variants)) != len(variants):
                    raise ValueError('enum variant collision: ' + name)
                self.rust.append('#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]\n'
                                 + 'pub enum ' + name + ' {\n' + ''.join(
                                     '#[serde(rename = ' + rust_string(v) + ')]\n' + n + ',\n'
                                     for v, n in zip(choices, variants)) + '}\n')
                return name, ' | '.join(json.dumps(v, ensure_ascii=False) for v in choices)
            return 'String', 'string'
        if tag == 'uint64':
            return 'u64', ty['const'] + 'n' if 'const' in ty else 'bigint'
        if tag == 'bytes':
            return 'ByteString', 'Uint8Array'
        if tag == 'bool':
            return 'bool', json.dumps(ty['const']) if 'const' in ty else 'boolean'
        if tag == 'null':
            return '()', 'null'
        if tag == 'nullable':
            r, t = self.kind(ty['of'], context + 'Present')
            return 'Option<' + r + '>', '(' + t + ') | null'
        if tag == 'array':
            r, t = self.kind(ty['items'], context + 'Item')
            return 'Vec<' + r + '>', 'ReadonlyArray<' + t + '>'
        if tag == 'frame-payload':
            name = self.owner['protocols'][ty['protocol']]['envelope'] + 'Payload'
            return name, name
        raise ValueError('unsupported type operator: ' + tag)

    def nullable(self, ty, seen=()):
        if ty['t'] in ('nullable', 'null'):
            return True
        if ty['t'] == 'ref' and ty['ref'] in self.owner['scalars']:
            if ty['ref'] in seen:
                raise ValueError('recursive scalar')
            return self.nullable(self.owner['scalars'][ty['ref']]['type'], (*seen, ty['ref']))
        return False

    def fields(self, members, context, serde=True, public=True, decode=True):
        names = [snake(m['name']) for m in members]
        if len(set(names)) != len(names):
            raise ValueError('field name collision: ' + context)
        rr, tt = [], []
        for i, m in enumerate(members):
            r, t = self.kind(m['type'], context + 'Field' + str(i))
            optional = m['presence'] == 'optional'
            attrs = ['rename = ' + rust_string(m['name'])]
            if optional:
                r = 'FieldPresence<' + r + '>'
                attrs += ['default', 'skip_serializing_if = "FieldPresence::is_missing"']
            elif decode and self.nullable(m['type']):
                attrs += ['deserialize_with = "required_value"']
            rr.append(('#[serde(' + ', '.join(attrs) + ')]\n' if serde else '') +
                      ('pub ' if public else '') + names[i] + ': ' + r + ',\n')
            tt.append('readonly ' + json.dumps(m['name']) + ('?' if optional else '') + ': ' + t + ';')
        return ''.join(rr), '\n'.join(tt)

    def scalar_type(self, ty, seen=()):
        if ty['t'] == 'ref' and ty['ref'] in self.owner['scalars']:
            if ty['ref'] in seen:
                raise ValueError('recursive scalar')
            return self.scalar_type(self.owner['scalars'][ty['ref']]['type'], (*seen, ty['ref']))
        if ty['t'] not in ('text', 'uint64', 'bytes', 'bool', 'null'):
            raise ValueError('unselected complex tagged-record member')
        return ty['t']

    def tagged_deserializer(self, name, record):
        members = record['memberOrder']
        discriminator = record['discriminator']
        variants = record['variants']
        if discriminator not in members:
            raise ValueError('missing discriminator in member order')
        for body in variants.values():
            if discriminator in body:
                raise ValueError('variant body redeclares discriminator')
        allowed = '&[' + ','.join(rust_string(n) for n in members) + ']'
        tag_values = '&[' + ','.join(rust_string(n) for n in variants) + ']'
        cases = []
        for tag, body in variants.items():
            assignments = []
            for field in members:
                if field == discriminator:
                    continue
                kind = self.scalar_type(body[field])
                value = ('values[' + str(members.index(field)) + '].take().ok_or_else(|| '
                         'serde::de::Error::missing_field(' + rust_string(field) + '))?')
                method = {'text': 'text', 'uint64': 'unsigned', 'bytes': 'bytes', 'bool': 'bool', 'null': 'null'}[kind]
                converted = value + '.into_' + method + '::<A::Error>()?'
                if kind == 'text':
                    converted = ('serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new('
                                 + converted + '))?')
                assignments.append(snake(field) + ': ' + converted)
            cases.append(rust_string(tag) + ' => Ok(' + name + '::' + pascal(tag) + ' { ' + ','.join(assignments) + ' }),')
        indexes = ','.join(rust_string(n) + ' => ' + str(i) for i, n in enumerate(members))
        return f'''
impl<'de> serde::Deserialize<'de> for {name} {{
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {{
        struct Record;
        impl<'de> serde::de::Visitor<'de> for Record {{
            type Value = {name};
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {{ f.write_str("a tagged native record with text keys") }}
            fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {{
                let mut values: [Option<WireScalar>; {len(members)}] = std::array::from_fn(|_| None);
                while let Some(key) = map.next_key::<StrictMapKey>()? {{
                    let index = match key.0.as_str() {{ {indexes}, _ => return Err(serde::de::Error::unknown_field(&key.0, {allowed})) }};
                    if values[index].is_some() {{ return Err(serde::de::Error::custom("duplicate native record member")); }}
                    values[index] = Some(map.next_value::<WireScalar>()?);
                }}
                let tag = values[{members.index(discriminator)}].take().ok_or_else(|| serde::de::Error::missing_field({rust_string(discriminator)}))?.into_text::<A::Error>()?;
                match tag.as_str() {{ {''.join(cases)} _ => Err(serde::de::Error::unknown_variant(&tag, {tag_values})) }}
            }}
        }}
        deserializer.deserialize_map(Record)
    }}
}}
'''

    def run(self):
        for name, scalar in self.owner['scalars'].items():
            r, t = self.kind(scalar['type'], name)
            self.rust.append('pub type ' + name + ' = ' + r + ';\n')
            self.ts.append('export type ' + name + ' = ' + t + ';\n')
        for name, record in self.owner['records'].items():
            kind = record['kind']
            if kind == 'alias':
                r, t = self.kind(record['target'], name)
                self.rust.append('pub type ' + name + ' = ' + r + ';\n')
                self.ts.append('export type ' + name + ' = ' + t + ';\n')
            elif kind == 'record':
                frame = any(m['type']['t'] == 'frame-payload' for m in record['members'])
                r, t = self.fields(record['members'], name, serde=not frame)
                attrs = '#[derive(Clone, Debug)]\n' if frame else (
                    '#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]\n'
                    '#[serde(deny_unknown_fields)]\n')
                self.rust.append(attrs + 'pub struct ' + name + ' {\n' + r + '}\n')
                if not frame:
                    self.ts.append('export interface ' + name + ' {\n' + t + '\n}\n')
            elif kind == 'variant-record':
                rr, tt = [], []
                if len(record['variants']) < 2:
                    raise ValueError('variant record requires at least two variants')
                if len(record['memberOrder']) != len(set(record['memberOrder'])):
                    raise ValueError('duplicate member order entry')
                variant_names = [pascal(x) for x in record['variants']]
                if len(set(variant_names)) != len(variant_names):
                    raise ValueError('record variant collision: ' + name)
                for index, (tag, body) in enumerate(record['variants'].items()):
                    if set(body) | {record['discriminator']} != set(record['memberOrder']):
                        raise ValueError('variant member order mismatch: ' + name)
                    members = [dict(name=n, type=body[n], presence='required')
                               for n in record['memberOrder'] if n != record['discriminator']]
                    r, t = self.fields(members, name + 'Variant' + str(index), public=False, decode=False)
                    rr.append('#[serde(rename = ' + rust_string(tag) + ')]\n' +
                              variant_names[index] + ' {\n' + r + '},\n')
                    tt.append('{ readonly ' + json.dumps(record['discriminator']) + ': ' +
                              json.dumps(tag) + ';\n' + t + '\n}')
                self.rust.append('#[derive(Clone, Debug, serde::Serialize)]\n'
                                 '#[serde(tag = ' + rust_string(record['discriminator']) +
                                 ', deny_unknown_fields)]\npub enum ' + name + ' {\n' + ''.join(rr) + '}\n')
                self.rust.append(self.tagged_deserializer(name, record))
                self.ts.append('export type ' + name + ' = ' + ' | '.join(tt) + ';\n')
            else:
                raise ValueError('unsupported record kind')
        for protocol in self.owner['protocols'].values():
            name = protocol['envelope'] + 'Payload'
            self.reserve(name)
            rr, tt, frames, names = [], [], [], set()
            header = self.owner['records'][protocol['envelope']]['members']
            for frame in protocol['frames']:
                payload = frame['payload']
                if 'select' in payload:
                    alternatives = [(key, payload['alternatives'][key]) for key in SELECTOR_KEYS[payload['select']]]
                    if len({json.dumps(ty, sort_keys=True) for _, ty in alternatives}) != 2:
                        raise ValueError('identical selection alternative declarations')
                else:
                    alternatives = [('', payload)]
                emitted_types = set()
                for index, (selector, ty) in enumerate(alternatives):
                    variant = pascal(frame['frameType']) + (str(index) if selector else '')
                    if variant in names:
                        raise ValueError('frame variant collision')
                    names.add(variant)
                    r, t = self.kind(ty, name + variant)
                    if (r, t) in emitted_types:
                        raise ValueError('identical emitted selection alternative types')
                    emitted_types.add((r, t))
                    selected_comment = ''
                    if selector:
                        self.selector_mappings.append(dict(envelope=protocol['envelope'], frameType=frame['frameType'],
                                                           mechanism=payload['select'], key=selector, rustVariant=variant, rustType=r, typescriptType=t))
                        selected_comment = '/// Host selector ' + payload['select'] + ' = ' + selector + '; not a wire tag.\n'
                    rr.append(selected_comment + variant + '(Box<' + r + '>),\n')
                    tt.append(t)
                    fields = []
                    for m in header:
                        mt = (json.dumps(frame['frameType']) if m['name'] == 'frameType'
                              else t if m['name'] == 'payload'
                              else json.dumps(frame['direction']) if m['name'] == 'direction'
                              else self.kind(m['type'], name + variant + pascal(m['name']))[1])
                        fields.append('readonly ' + json.dumps(m['name']) + ': ' + mt + ';')
                    frames.append('{ ' + ' '.join(fields) + ' }')
            self.rust.append('/// Inert selection only. No serde: decoding requires frameType and admitted host selector.\n'
                             '#[derive(Clone, Debug)]\npub enum ' + name + ' {\n' + ''.join(rr) + '}\n')
            self.ts.append('export type ' + name + ' = ' + ' | '.join(dict.fromkeys(tt)) + ';\n')
            self.ts.append('export type ' + protocol['envelope'] + ' = ' + '\n | '.join(frames) + ';\n')
        return '\n'.join(self.rust), '\n'.join(self.ts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--owner', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.owner.read_bytes()
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate input member: ' + key)
            result[key] = value
        return result
    def noninteger(value):
        raise ValueError('noninteger JSON number in carrier input: ' + value)
    owner = json.loads(raw, object_pairs_hook=pairs, parse_float=noninteger, parse_constant=noninteger)
    renderer = Renderer(owner)
    rust, ts = renderer.run()
    args.output.mkdir(parents=True, exist_ok=True)
    header = '// INERT GENERATION TRIAL. Owner SHA256 ' + hashlib.sha256(raw).hexdigest() + '\n'
    imports = '\n'.join('use opensip_contracts::generated::' + m + '::*;'
                        for m in ['evidence', 'identity', 'invocation', 'output', 'protocol'])
    (args.output / 'wire.rs').write_text(header + '#![allow(unused_imports)]\n' + imports + '\n' + RUST_HELPERS + rust)
    (args.output / 'wire.ts').write_text(header + 'import type { ' + ', '.join(sorted(renderer.externs)) +
                                        ' } from "./externs.js";\n' + ts)
    (args.output / 'render-result.json').write_text(json.dumps(dict(
        standing='inert trial, unaccepted owner; no wire codec/admission/product integration',
        ownerSha256=hashlib.sha256(raw).hexdigest(), scalars=len(owner['scalars']),
        records=len(owner['records']), protocols=len(owner['protocols']),
        externalTypes=sorted(renderer.externs), privateTypes=sorted(renderer.aux), selectorMappings=renderer.selector_mappings), indent=2) + '\n')


if __name__ == '__main__':
    main()
