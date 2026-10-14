from pathlib import Path
import json, sys, hashlib
# Convert a selected native replay packet (one JSON document) to the rows transport of the rows variant driver: a header
# row {kind,runId,objects,blobs} then one row per object {kind,id,domain,descriptor} and per blob {kind,sha256,hex}, in
# packet order. Values are copied, never rebuilt: duplicate keys and floats are refused, every line must stay under the
# product canonical MAX_BYTES (4 MiB), and the rows must reassemble to a value equal to the source packet.
MAX = 4 * 1024 * 1024
def pairs(items):
    keys = [k for k, _ in items]; assert len(keys) == len(set(keys)), 'duplicate key'; return dict(items)
def nofloat(x): raise AssertionError('float')
src = Path(sys.argv[1]); dst = Path(sys.argv[2]); assert not dst.exists()
packet = json.loads(src.read_bytes(), object_pairs_hook=pairs, parse_float=nofloat)
assert set(packet) >= {'runId', 'objects', 'blobs'}, sorted(packet)  # the closed driver reads only these three keys
extra = sorted(set(packet) - {'runId', 'objects', 'blobs'})
dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':')).encode()
lines = [dump(dict(kind='header', runId=packet['runId'], objects=str(len(packet['objects'])), blobs=str(len(packet['blobs']))))]
for o in packet['objects']: assert set(o) == {'id', 'domain', 'descriptor'}, sorted(o); lines.append(dump(dict(kind='object', **o)))
for b in packet['blobs']: assert set(b) == {'sha256', 'hex'}, sorted(b); lines.append(dump(dict(kind='blob', **b)))
assert all(b'\n' not in l and len(l) <= MAX for l in lines)
dst.write_bytes(b'\n'.join(lines) + b'\n')
back = [json.loads(l, object_pairs_hook=pairs, parse_float=nofloat) for l in dst.read_bytes().split(b'\n') if l]
rebuilt = dict(runId=back[0]['runId'], objects=[{k: v for k, v in r.items() if k != 'kind'} for r in back if r['kind'] == 'object'], blobs=[{k: v for k, v in r.items() if k != 'kind'} for r in back if r['kind'] == 'blob'])
assert rebuilt == {k: packet[k] for k in ['runId', 'objects', 'blobs']}
raw = dst.read_bytes()
print(json.dumps(dict(source=str(src), sourceSha256=hashlib.sha256(src.read_bytes()).hexdigest(), rows=str(dst), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), objects=len(packet['objects']), blobs=len(packet['blobs']), maxLineBytes=max(len(l) for l in lines), ignoredTopLevelKeys=extra, reassemblesEqual=True)))
