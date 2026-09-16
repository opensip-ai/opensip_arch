import copy, json, importlib.util, sys
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('r', 'render.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
O = json.load(open('inputs/wire-carriers.v1.json'))


def run(o):
    try:
        rs, ts = r.Renderer(o).run()
        return 'ok', rs, ts
    except Exception as e:
        return 'refused:' + str(e)[:70], '', ''


def member(rec, name):
    return [m for m in rec['members'] if m['name'] == name][0]


for pn, p in O['protocols'].items():
    env = O['records'][p['envelope']]
    ft = member(env, 'frameType')['type']['enum']
    print(pn, 'header enum == frames:', sorted(ft) == sorted(f['frameType'] for f in p['frames']), len(ft), len(p['frames']))
    d = [m for m in env['members'] if m['name'] == 'direction']
    print('  direction header', bool(d), bool(d) and sorted({f['direction'] for f in p['frames']}) == sorted(d[0]['type']['enum']))

o = copy.deepcopy(O); member(o['records']['Ts2FrameV2'], 'frameType')['type']['enum'].remove('Cancel')
s, rs, ts = run(o); print('P1 header enum lacks rendered frame:', s, '"frameType": "Cancel"' in ts)
o = copy.deepcopy(O); fs = o['protocols']['typescript-semantic']['frames']; d = copy.deepcopy(fs[0]); d['direction'] = 'worker-to-host'; fs.append(d)
print('P2 duplicate frameType other direction:', run(o)[0])
o = copy.deepcopy(O); o['records']['Ts2CancelV1']['members'].append(dict(name='inner', type={'t': 'frame-payload', 'protocol': 'typescript-semantic'}, presence='required'))
s, rs, ts = run(o); print('P3 frame-payload in non-envelope:', s, 'TS Ts2CancelV1 emitted:', 'Ts2CancelV1 {' in ts or 'Ts2CancelV1 =' in ts)
o = copy.deepcopy(O); o['records']['Ts2CancelV1']['members'].append(dict(name='inner', type={'t': 'array', 'items': {'t': 'frame-payload', 'protocol': 'typescript-semantic'}, 'minItems': '0', 'order': 'x'}, presence='required'))
s, rs, ts = run(o); print('P4 nested frame-payload:', s, 'Vec<Ts2FrameV2Payload> emitted with serde:', 'Vec<Ts2FrameV2Payload>' in rs)
o = copy.deepcopy(O); o['records']['Ts2SnapshotEntryV1']['variants']['file']['kind'] = {'t': 'text', 'nfc': True, 'const': 'directory'}
s, rs, ts = run(o); print('P5 discriminator redeclared in body:', s, 'silently dropped:', 'directory' not in ts)
print('P6 keywords:', {k: r.snake(k) for k in ['if', 'true', 'else', 'while', 'try', 'box', 'crate', 'loop']})
print('P7 enum+const both:', r.Renderer(O).kind({'t': 'text', 'nfc': True, 'enum': ['a'], 'const': 'b'}, 'Ts2ProbeA')[1])
print('P8 uint const unchecked:', r.Renderer(O).kind({'t': 'uint64', 'const': '18446744073709551616'}, 'X')[1], r.Renderer(O).kind({'t': 'uint64', 'const': '-1'}, 'X')[1])
print('P9 rust escapes:', ascii(r.rust_string('a\x7f "\\\x00é')))
print('P9 ts escapes:', ascii(r.Renderer(O).kind({'t': 'text', 'enum': ['a"\\\n ', 'b\x00']}, 'Ts2Esc')[1]))
try:
    r.rust_string('\ud800').encode('utf-8'); print('P10 lone surrogate encodes')
except UnicodeEncodeError:
    print('P10 lone surrogate: write_text raises (fail closed)')
o = copy.deepcopy(O); o['records']['Ts2CancelV1']['members'].append(dict(name='maybeBytes', type={'t': 'nullable', 'of': {'t': 'bytes', 'minBytes': '0', 'maxBytes': '1'}}, presence='optional'))
s, rs, ts = run(o); print('P11 optional nullable:', s, [l for l in rs.splitlines() if 'maybe' in l.lower()], [l for l in ts.splitlines() if 'maybeBytes' in l])
o = copy.deepcopy(O); o['scalars']['Ts2NullAlias'] = {'type': {'t': 'null'}, 'source': {'pin': 'x', 'selector': 'y'}}
o['records']['Ts2CancelV1']['members'].append(dict(name='nullViaAlias', type={'t': 'ref', 'ref': 'Ts2NullAlias'}, presence='required'))
s, rs, ts = run(o); i = rs.find('null_via_alias'); print('P12 required null via scalar alias:', s, rs[i - 80:i + 30].replace('\n', ' | '))
o = copy.deepcopy(O); o['records']['ByteString'] = copy.deepcopy(o['records']['Ts2CancelV1']); print('P13 helper-name record accepted by renderer:', run(o)[0])
o = copy.deepcopy(O); member(o['records']['Rust3ProviderFrameV3'], 'frameType')['name'] = 'kind'
s, rs, ts = run(o); line = [l for l in ts.splitlines() if 'Rust3ProviderFrameV3 =' in l]; print('P14 renamed tag member:', s, line[0][:200] if line else None)
o = copy.deepcopy(O); v = o['records']['Ts2SnapshotEntryV1']['variants']; v['File'] = v['file']; o['records']['Ts2SnapshotEntryV1']['memberOrder'] = o['records']['Ts2SnapshotEntryV1']['memberOrder']
print('P15 variant pascal collision:', run(o)[0])
o = copy.deepcopy(O); o['records']['Ts2FrameV2Payload'] = copy.deepcopy(o['records']['Ts2CancelV1']); print('P16 payload name collision:', run(o)[0])
o = copy.deepcopy(O); o['records']['Ts2CancelV1Field2Value'] = copy.deepcopy(o['records']['Ts2CompleteV1']); print('P17 private enum collision:', run(o)[0])
print('P18 snake:', r.snake('selfValue'), r.snake('self'), r.snake('HTTPServer'), r.snake('sha256Hex'), r.snake('aB'), r.snake('a_b'))
o = copy.deepcopy(O); del o['protocols']['rust-semantic']
s, rs, ts = run(o); print('P19 envelope w/o protocol:', s, 'serde derive on Rust3ProviderFrameV3:', 'serde::Serialize, serde::Deserialize)]\n#[serde(deny_unknown_fields)]\npub struct Rust3ProviderFrameV3' in rs, 'TS emitted:', 'Rust3ProviderFrameV3 ' in ts)
o = copy.deepcopy(O); member(o['records']['Ts2FrameV2'], 'sequence')['type'] = {'t': 'text', 'nfc': True, 'enum': ['x', 'y']}
s, rs, ts = run(o); print('P20 text-enum header member: private enums emitted', rs.count('pub enum Ts2FrameV2Payload'), s)
