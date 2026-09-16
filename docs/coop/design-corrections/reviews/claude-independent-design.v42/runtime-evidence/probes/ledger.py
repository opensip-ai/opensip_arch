"""Append read-ledger rows: python ledger.py KIND NOTE PATH[:RANGE] [PATH[:RANGE] ...]
KIND is fresh42Read (source42 bytes; a whole-file read only when the recorded ranges cover every line), delta41to42Read or
delta40to42Read (a complete diff read of that delta; not a whole-file read) or evidenceRead (non-source evidence; absolute path;
ranges as for fresh reads). The current SHA-256 and line count are recomputed at append time."""
import datetime, hashlib, json, os, sys

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v42'
S42 = '/tmp/opensip-design-corrections/candidate-subject.v42'
kind, note = sys.argv[1], sys.argv[2]
assert kind in ('fresh42Read', 'delta41to42Read', 'delta40to42Read', 'evidenceRead'), kind
with open(RT + '/receipts/read-ledger.jsonl', 'a', encoding='utf-8') as out:
    for spec in sys.argv[3:]:
        path, _, rng = spec.rpartition(':') if ':' in spec else (spec, '', 'complete')
        full = path if path.startswith('/') else os.path.join(S42, path)
        b = open(full, 'rb').read()
        row = {'kind': kind, 'path': path, 'range': rng, 'sha256': hashlib.sha256(b).hexdigest(),
               'lines': b.count(b'\n') + (0 if not b or b.endswith(b'\n') else 1), 'note': note,
               'at': datetime.datetime.now().isoformat(timespec='seconds')}
        if kind.startswith('delta'):
            key = kind[len('delta'):-len('Read')]
            d = RT + '/receipts/delta-diffs-' + key + '/' + path.replace('/', '__') + '.diff'
            row['diff'] = d.replace(RT + '/', '')
            row['diffSha256'] = hashlib.sha256(open(d, 'rb').read()).hexdigest()
        out.write(json.dumps(row) + '\n')
        print(json.dumps(row))
