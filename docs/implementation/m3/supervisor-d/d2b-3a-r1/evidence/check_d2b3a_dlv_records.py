"""LD-D2B3-1's lane check: each TS2 carrier record whose source is DLV (delivery.v2 wireSchema payloadSchemas,
definitions or frameEnvelope) carries exactly its DLV schema's constraints as data. Its member set is DLV's required
plus optional members, and it is closed as DLV's is; a variant record's memberOrder is DLV's required list; and every
count bound DLV states by a limit name (maxFactBatchFacts, maxCoverageEntriesPerFrame, ...) or by an "exactly" constant
is the carrier's. A DLV field naming no bound imposes none to compare. Usage: <worktree> <architecture> <out json>."""
from pathlib import Path
import json, re, sys
W, A, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
carriers = json.loads((W / 'schemas/wire/native-carriers-v1.json').read_bytes())
dlv = json.loads((A / 'docs/coop/artifacts/delivery.v2.json').read_bytes())
pin = next(p for p in carriers['sourcePins'] if p['key'] == 'delivery2')
import hashlib
pinned = hashlib.sha256((A / pin['path']).read_bytes()).hexdigest() == pin['sha256']
ws = dlv['typescriptSemanticSubstrate']['providerProtocol']['wireSchema']
limits = {k: v for k, v in ws['limits'].items() if isinstance(v, int)}
def select(selector):
    node = dlv
    for part in selector.removeprefix('$.').split('.'):
        node = node[part]
    return node
rows, failures = [], []
for name, record in sorted(carriers['records'].items()):
    src = record.get('source', {})
    if not name.startswith('Ts2') or src.get('pin') != 'delivery2':
        continue
    schema = select(src['selector'])
    want = list(schema.get('required', [])) + list(schema.get('optional', []))
    problems = []
    if schema.get('closed') is not True:
        problems.append('DLV schema not closed')
    if record['kind'] == 'record':
        got = [m['name'] for m in record['members']]
        if sorted(got) != sorted(want):
            problems.append(f'members {sorted(got)} != DLV {sorted(want)}')
        if any(m['presence'] != 'required' for m in record['members']) and not schema.get('optional'):
            problems.append('an optional carrier member DLV does not list')
        members = {m['name']: m['type'] for m in record['members']}
    else:
        if record['memberOrder'] != schema['required'] and sorted(record['memberOrder']) != sorted(schema['required']):
            problems.append('memberOrder != DLV required')
        members = {}
    for fname, text in schema.get('fields', {}).items():
        if not isinstance(text, str) or fname not in members:
            continue
        t = members[fname]
        for limit, value in limits.items():
            if limit in text and t.get('t') == 'array' and t.get('maxItems') != str(value):
                problems.append(f'{fname}: maxItems {t.get("maxItems")} != {limit} {value}')
        m = re.match(r'uint64 exactly (\d+)', text)
        if m and t.get('const') != m.group(1):
            problems.append(f'{fname}: const {t.get("const")} != DLV exactly {m.group(1)}')
        if text.startswith('non-empty') and t.get('t') == 'array' and t.get('minItems') not in ('1',):
            problems.append(f'{fname}: DLV non-empty but minItems {t.get("minItems")}')
    rows.append(dict(record=name, selector=src['selector'], members=len(want), problems=problems))
    if problems:
        failures.append(name)
out = dict(delivery2Pinned=pinned, records=rows, failures=failures, passed=pinned and not failures)
OUT.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(dict(passed=out['passed'], records=len(rows), failures=failures)))
sys.exit(0 if out['passed'] else 1)
