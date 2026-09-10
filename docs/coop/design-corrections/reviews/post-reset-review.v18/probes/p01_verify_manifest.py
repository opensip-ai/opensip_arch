"""p01: verify every declared hash/length in the frozen v18 manifest against the snapshot,
and verify the snapshot inventory has no undeclared extra files."""
import hashlib, json, os, sys

MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v18.json'
man = json.load(open(MAN))
root = man['snapshotRoot']
files = man['files']

print('manifest fileCount=%d totalBytes=%d' % (man['fileCount'], man['totalBytes']))
print('declared entry keys sample:', sorted(files[0].keys()))

declared = {}
bad_hash, bad_len, missing = [], [], []
total = 0
for e in files:
    rel = e['path']
    declared[rel] = e
    p = os.path.join(root, rel)
    if not os.path.isfile(p):
        missing.append(rel)
        continue
    b = open(p, 'rb').read()
    total += len(b)
    if len(b) != e['bytes']:
        bad_len.append((rel, e['bytes'], len(b)))
    h = hashlib.sha256(b).hexdigest()
    if h != e['sha256']:
        bad_hash.append((rel, e['sha256'], h))

actual = set()
for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        actual.add(os.path.relpath(os.path.join(dirpath, fn), root))

extra = sorted(actual - set(declared))
print('declared=%d actualOnDisk=%d' % (len(declared), len(actual)))
print('missing=%d badLen=%d badHash=%d extra=%d' % (len(missing), len(bad_len), len(bad_hash), len(extra)))
print('summedActualBytes=%d declaredTotalBytes=%d match=%s' % (total, man['totalBytes'], total == man['totalBytes']))
for label, arr in (('MISSING', missing), ('BADLEN', bad_len), ('BADHASH', bad_hash), ('EXTRA', extra)):
    for x in arr[:20]:
        print(label, x)

# transitive pin inventory declared in the manifest
pins = [f for f in files if '/pins/' in f['path'] or f['path'].startswith('pins/')]
print('pinPathEntries=%d' % len(pins))
sys.exit(0 if not (missing or bad_len or bad_hash or extra) else 1)
