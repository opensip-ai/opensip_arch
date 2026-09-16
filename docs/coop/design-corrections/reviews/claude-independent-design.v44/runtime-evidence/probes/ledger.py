"""Append read-ledger rows: python ledger.py KIND NOTE PATH[:RANGE] [PATH[:RANGE] ...]
KIND is fresh44Read (source44 bytes; a whole-file read only when the recorded ranges cover every line), delta43to44Read (a
complete 43->44 diff or creation diff read; not a whole-file read of a changed file) or evidenceRead (non-source evidence;
absolute path). The current SHA-256 and line count are recomputed at append time."""
import datetime, hashlib, json, os, sys

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v44'
S44 = '/tmp/opensip-design-corrections/candidate-subject.v44'
kind, note = sys.argv[1], sys.argv[2]
assert kind in ('fresh44Read', 'delta43to44Read', 'evidenceRead'), kind
os.makedirs(RT + '/receipts', exist_ok=True)
with open(RT + '/receipts/read-ledger.jsonl', 'a', encoding='utf-8') as out:
    for spec in sys.argv[3:]:
        path, _, rng = spec.rpartition(':') if ':' in spec else (spec, '', 'complete')
        full = path if path.startswith('/') else os.path.join(S44, path)
        b = open(full, 'rb').read()
        row = {'kind': kind, 'path': path, 'range': rng, 'sha256': hashlib.sha256(b).hexdigest(),
               'lines': b.count(b'\n') + (0 if not b or b.endswith(b'\n') else 1), 'note': note, 'at': datetime.datetime.now().isoformat(timespec='seconds')}
        if kind == 'delta43to44Read':
            d = RT + '/receipts/delta-diffs-43to44/' + path.replace('/', '__') + '.diff'
            row['diff'] = d.replace(RT + '/', '')
            row['diffSha256'] = hashlib.sha256(open(d, 'rb').read()).hexdigest()
        out.write(json.dumps(row) + '\n')
        print(json.dumps(row))
