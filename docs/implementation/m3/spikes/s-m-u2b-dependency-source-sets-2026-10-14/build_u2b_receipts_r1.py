from pathlib import Path
import json, hashlib, os, re, tomllib
# U-2b step 1: per-workload dependency cache receipts for the accepted metadata harness (sealed_spike_metadata_tests
# opensip_spike_metadata_collect; receipt fields registryConfigPath, indexFiles[name,path,indexRelativePath], packages
# [name,version,checksum,archive]), built only from the accepted-in-U-2a template r117:
#  - archives: r117 cache files, each verified against the lock checksum;
#  - index lines: decoded byte-for-byte from r117's stock Cargo .cache files (format: 0x03, u32 LE index version 2,
#    "Unknown\0", then {version\0json\0}...), each line's name/vers checked against its entry; every locked
#    version+checksum must be present. Decoded lines are written as .jsonl per name.
# axum is included as the control: its resolved metadata must reproduce the accepted axum-resolved-metadata.json.
W = Path(__file__).resolve().parent; T = W / 'registry-intake-template-r117'; NAME = 'index.crates.io-1949cf8c6b5b557f'
C = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-owned-corpus-xw576l4w')
OUT = W / 'u2b-receipts'; assert not OUT.exists(); OUT.mkdir(); (OUT / 'index').mkdir()
CRATES = 'registry+https://github.com/rust-lang/crates.io-index'
ENTRIES = {'rs-medium-axum': 'rs-medium-axum', 'poly-medium-napi-rs': 'poly-medium-napi-rs', 'rs-medium-aws-lambda-rust-runtime': 'rs-medium-aws-lambda-rust-runtime', 'rs-medium-hyper': 'rs-medium-hyper',
           'rs-medium-serde': 'rs-medium-serde', 'rs-medium-serde-json': 'rs-medium-serde-json', 'rs-medium-tokio': 'rs-medium-tokio',
           'mr-rs-medium-serde-json/rs-medium-serde': 'mr-rs-medium-serde-json__rs-medium-serde', 'mr-rs-medium-serde-json/rs-medium-serde-json': 'mr-rs-medium-serde-json__rs-medium-serde-json'}
def pin(p): raw = Path(p).read_bytes(); return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def rel_for(name):
    n = name.lower()
    return '1/' + n if len(n) == 1 else '2/' + n if len(n) == 2 else '3/' + n[0] + '/' + n if len(n) == 3 else n[:2] + '/' + n[2:4] + '/' + n
def decode(path):
    raw = path.read_bytes(); assert raw[0] == 3 and int.from_bytes(raw[1:5], 'little') == 2, path
    i = raw.index(b'\0', 5); assert raw[5:i] == b'Unknown'; i += 1; out = []
    while i < len(raw):
        j = raw.index(b'\0', i); vers = raw[i:j].decode(); k = raw.index(b'\0', j + 1); line = raw[j + 1:k]
        rec = json.loads(line); assert rec['vers'] == vers; out.append(line); i = k + 1
    return out
decoded = {}
receipts = []
for entry, slug in ENTRIES.items():
    lock = C / entry / 'Cargo.lock'; data = tomllib.loads(lock.read_text()); assert data['version'] in (3, 4)
    pkgs = []; names = set()
    for p in data['package']:
        src = p.get('source')
        if src is None: continue  # path package: stays in the snapshot (NE:1687)
        assert src == CRATES, (entry, p['name'], src)
        arch = T / 'cache' / NAME / f"{p['name']}-{p['version']}.crate"; a = pin(arch); assert a['sha256'] == p['checksum'], (entry, p['name'])
        pkgs.append(dict(name=p['name'], version=p['version'], source=src, checksum=p['checksum'], archive=str(arch), bytes=a['bytes'], sha256=a['sha256'])); names.add(p['name'])
    index_files = []
    for name in sorted(names):
        if name not in decoded:
            rel = rel_for(name); cache = T / 'index' / NAME / '.cache' / rel; lines = decode(cache)
            for line in lines: assert json.loads(line)['name'] == name
            out = OUT / 'index' / (name + '.jsonl'); out.write_bytes(b'\n'.join(lines) + b'\n')
            decoded[name] = dict(name=name, path=str(out), indexRelativePath=rel, source=pin(cache), **{k: v for k, v in pin(out).items() if k != 'path'}, versionRecords=len(lines))
        index_files.append(decoded[name])
    for p in pkgs:
        rows = [json.loads(l) for l in Path(decoded[p['name']]['path']).read_bytes().splitlines() if l]
        assert any(r['vers'] == p['version'] and r['cksum'] == p['checksum'] for r in rows), (entry, p['name'], p['version'])
    receipt = dict(standing='U-2b DEPENDENCY CACHE RECEIPT FROM TEMPLATE r117 (accepted in U-2a); NO SOURCE AUTHENTICATION', workload=entry, originalLock=pin(lock), lockVersion=data['version'],
                   registryConfigPath=str(T / 'index' / NAME / 'config.json'), registryConfigSha256=pin(T / 'index' / NAME / 'config.json')['sha256'], packages=pkgs, indexFiles=index_files,
                   templateR117=pin(W / 'registry-intake-template-r117.json'))
    path = OUT / f'{slug}.receipt.json'; path.write_text(json.dumps(receipt, indent=1) + '\n'); receipts.append(dict(entry=entry, slug=slug, receipt=pin(path), packages=len(pkgs), names=len(names)))
    print(entry, 'packages', len(pkgs), 'names', len(names), flush=True)
(W / 'u2b-receipts.json').write_text(json.dumps(dict(standing='U-2b RECEIPTS', receipts=receipts, decodedIndexNames=len(decoded)), indent=1) + '\n')
