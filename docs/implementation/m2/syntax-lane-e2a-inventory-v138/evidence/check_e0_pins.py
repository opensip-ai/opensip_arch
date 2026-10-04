"""Read-only: cross-check unit E2a's lane pins and SymbolTableV1 records against
E0's accepted record (docs/implementation/m3/syntax-e/E0-REPORT.md, accepted
by GROK2) and SYN-NS's bound materialization map, independently of the lane.

1. Upstream releases. Each upstream's tag and commit in tools/grammar/lane.json
   equal E0's resolved tag line in e0-probe/pins/PINS.txt, and the runtime
   crate's checksum equals E0's harness Cargo.lock.
2. Members. Every lane member (runtime and code rows) has E0's per-file tag pin
   at the same upstream path: the same sha256, byte length and git blob.
3. Symbol tables. Each retained tools/grammar/symbol-tables/<g>.v1.json has
   the digest prefix of E0-REPORT's P3 table; where E0's SCRATCH still holds
   them, its bytes equal E0's SymbolTableV1 recomputed from the natively linked
   Language (<g>.symtab.native.json) and decoded from the module
   (<g>.symtab.wasm.json).
4. SYN-NS. The lane's normalization members and manifest normalizer equal
   syn-ns/materialization-map.json.
5. The law. lane.json's law pin is PROPOSAL-r4.md's bytes.

Usage: check_e0_pins.py [WORKTREE] [E0-SCRATCH]. It prints a JSON report and
writes it to evidence/e0-crosscheck.json beside this script."""
import hashlib, json, re, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
E = A / 'docs/implementation/m3/syntax-e'
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-e2a').resolve(strict=True)
SCRATCH = Path(sys.argv[2] if len(sys.argv) > 2 else
               '/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/e0/out/symtab')
P3 = {'javascript': '5a0738c3', 'rust': '0363b059', 'tsx': 'c8759474', 'typescript': 'daa3b998'}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

lane = json.loads((W / 'tools/grammar/lane.json').read_bytes())
pins_txt = (E / 'e0-probe/pins/PINS.txt').read_text()
report = {'readOnly': True, 'upstreams': {}, 'members': 0, 'symbolTables': {}, 'synNs': None, 'law': None}
for upstream in lane['upstreams']:
    line = re.search(r'^' + re.escape(upstream['id']) + r'\s+(v\S+)\s.*commit=([0-9a-f]{40})', pins_txt, re.M)
    assert line and line.group(1) == upstream['tag'] and line.group(2) == upstream['commit'], upstream['id']
    report['upstreams'][upstream['id']] = {'tag': upstream['tag'], 'commit': upstream['commit'],
                                           'crateVcsCommit': upstream['crate']['vcsCommit'],
                                           'crateFromTagCommit': upstream['crate']['vcsCommit'] == upstream['commit']}
harness_lock = (E / 'e0-probe/harness/Cargo.lock').read_text()
runtime_crate = next(u['crate'] for u in lane['upstreams'] if u['id'] == lane['runtime']['upstream'])
block = re.search(r'name = "tree-sitter"\nversion = "' + re.escape(runtime_crate['version']) + r'"\n[^\[]*?checksum = "([0-9a-f]{64})"', harness_lock)
assert block and block.group(1) == runtime_crate['checksum'], 'runtime crate checksum differs from E0'
for row in [lane['runtime'], *[g for g in lane['grammars'] if g['syntaxClass'] == 'code']]:
    pins = {}
    for line in (E / f"e0-probe/pins/{row['upstream']}.pins.tsv").read_text().splitlines():
        if line.startswith('#') or not line.strip():
            continue
        path, digest, size, blob = line.split('\t')
        pins[path] = (digest, int(size), blob)
    for member in row['members']:
        assert pins.get(member['path']) == (member['sha256'], member['bytes'], member['gitBlob']), (row['upstream'], member['path'])
        report['members'] += 1
for grammar, prefix in P3.items():
    raw = (W / f'tools/grammar/symbol-tables/{grammar}.v1.json').read_bytes()
    digest = sha(raw)
    assert digest.startswith(prefix), grammar
    entry = {'sha256': digest, 'e0P3Prefix': prefix}
    for leg in ('native', 'wasm'):
        e0 = SCRATCH / f'{grammar}.symtab.{leg}.json'
        entry[leg] = (e0.read_bytes() == raw) if e0.is_file() else 'E0 SCRATCH absent'
        assert entry[leg] in (True, 'E0 SCRATCH absent'), (grammar, leg)
    definition = json.loads((W / f'tools/grammar/closure/opensip-interface/grammar/{grammar}/definition.v1.json').read_bytes())
    assert definition['symbolTableSha256'] == digest, grammar
    report['symbolTables'][grammar] = entry
mm = json.loads((E / 'syn-ns/materialization-map.json').read_bytes())
assert lane['normalization']['manifestNormalizer'] == mm['normalizer']
assert lane['normalization']['members'] == sorted(({'path': r['treePath'], 'bytes': r['bytes'], 'sha256': r['sha256']} for r in mm['tree']),
                                                  key=lambda r: r['path'])
report['synNs'] = {'members': len(mm['tree']), 'normalizer': mm['normalizer']['specificationDigest']}
law = (A / lane['law']['path']).read_bytes()
assert (len(law), sha(law)) == (lane['law']['bytes'], lane['law']['sha256'])
report['law'] = {'path': lane['law']['path'], 'sha256': sha(law)}
out = json.dumps(report, indent=1, sort_keys=True) + '\n'
(Path(__file__).resolve().parent / 'e0-crosscheck.json').write_text(out)
print(out, end='')
