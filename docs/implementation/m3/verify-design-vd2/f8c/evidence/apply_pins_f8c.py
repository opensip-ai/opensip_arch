"""F8c step 4 (law VD2, "F8c"): re-pin the selected registries onto VD2-a's tools/verify_design.py.

F8b's apply_pins.py without the receipt and toolchain: verify_design.py is not a build input
(adapter.py validate_build_receipt joins Cargo.lock, Cargo.toml, three Rust sources and
build_contracts.py only), so rebuild-02 stays selected. Changes, on a worktree at product main carrying
VD2-a's two files (4c761e8 in r1, cca4fe4 in r2; these three files are byte-identical at both):
- tools/contracts/generator-closure.json: the one tools/verify_design.py files row;
- schemas/registry.json: recipes[0].generatorClosureSha256 only;
- tools/typescript-lanes.json: the one tools/verify_design.py files row.
report.ts header lines 2-3 follow from generation (run_generation_f8c.py).
Refuses unless every changed value still holds its 4c761e8 (= cca4fe4) value and every file round-trips
through json.dumps(indent=2) + newline, so no other byte moves. Afterwards all 349 closure rows
and the lane registry's 12 tracked rows are checked against the worktree.
Usage: apply_pins_f8c.py WORKTREE [REPORT_JSON]"""
import hashlib, json, sys
from pathlib import Path
W = Path(sys.argv[1]).resolve(strict=True)
OLD_VD = (40714, 'c13d231eb755a08a33fae674426861145758c5ec136ba2cd6dd4b0f1020f8f08')
OLD_CLOSURE = '9dc40660270212c8391cf4efe6276aae233bee3b00092b7aa966f76535947e73'
OLD_REGISTRY = 'ca65e1b2f8c8ec3f4aa1397e4003ffec962572608f6fd412b04ff027863e30d5'
OLD_LANES = '4d27f6d7c711c8471717da36b931fbcbd7466ef96a34a2d9bba494cd8ef15db1'
def pin(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def load(p):
    raw = (W / p).read_bytes(); v = json.loads(raw)
    assert (json.dumps(v, indent=2) + '\n').encode() == raw, 'round trip: ' + p
    return raw, v
def save(p, v): (W / p).write_bytes((json.dumps(v, indent=2) + '\n').encode())
vd = pin((W / 'tools/verify_design.py').read_bytes())
assert vd['sha256'] != OLD_VD[1], 'the worktree does not carry VD2-a'
def repin(rows):
    hit = [row for row in rows if row['path'] == 'tools/verify_design.py']
    assert len(hit) == 1 and (hit[0]['bytes'], hit[0]['sha256']) == OLD_VD, hit
    hit[0]['bytes'], hit[0]['sha256'] = vd['bytes'], vd['sha256']
report = {'tools/verify_design.py': {'before': dict(zip(('bytes', 'sha256'), OLD_VD)), 'after': vd}}
# Closure.
raw, cl = load('tools/contracts/generator-closure.json')
assert pin(raw)['sha256'] == OLD_CLOSURE
toolchain = json.dumps(cl['toolchain'], sort_keys=True)
repin(cl['files'])
assert json.dumps(cl['toolchain'], sort_keys=True) == toolchain
for row in cl['files']:
    assert pin((W / row['path']).read_bytes()) == {'bytes': row['bytes'], 'sha256': row['sha256']}, row['path']
save('tools/contracts/generator-closure.json', cl)
closure_raw = (W / 'tools/contracts/generator-closure.json').read_bytes()
assert len(closure_raw) == len(raw), 'closure length moved'
report['tools/contracts/generator-closure.json'] = {'before': pin(raw), 'after': pin(closure_raw), 'rowsChanged': ['tools/verify_design.py'],
                                                    'rows': len(cl['files']), 'toolchainUnchanged': True}
# Registry.
raw, reg = load('schemas/registry.json')
assert pin(raw)['sha256'] == OLD_REGISTRY and len(reg['recipes']) == 1
assert reg['recipes'][0]['generatorClosureSha256'] == OLD_CLOSURE
reg['recipes'][0]['generatorClosureSha256'] = pin(closure_raw)['sha256']
save('schemas/registry.json', reg)
registry_raw = (W / 'schemas/registry.json').read_bytes()
assert len(registry_raw) == len(raw)
report['schemas/registry.json'] = {'before': pin(raw), 'after': pin(registry_raw), 'changed': 'recipes[0].generatorClosureSha256'}
# Lane registry.
raw, ln = load('tools/typescript-lanes.json')
assert pin(raw)['sha256'] == OLD_LANES
repin(ln['files'])
tracked = [row for row in ln['files'] if '/node_modules/' not in row['path']]
for row in tracked:
    assert pin((W / row['path']).read_bytes()) == {'bytes': row['bytes'], 'sha256': row['sha256']}, row['path']
save('tools/typescript-lanes.json', ln)
lanes_raw = (W / 'tools/typescript-lanes.json').read_bytes()
assert len(lanes_raw) == len(raw)
report['tools/typescript-lanes.json'] = {'before': pin(raw), 'after': pin(lanes_raw), 'rowsChanged': ['tools/verify_design.py'],
                                         'rows': len(ln['files']), 'trackedRowsChecked': len(tracked)}
out = json.dumps(report, indent=2) + '\n'
if len(sys.argv) > 2:
    Path(sys.argv[2]).write_text(out)
print(out, end='')
