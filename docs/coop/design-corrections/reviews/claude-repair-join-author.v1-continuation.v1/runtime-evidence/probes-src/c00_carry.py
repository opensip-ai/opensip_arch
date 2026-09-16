"""c00: carry the original runtime's stable files into this continuation runtime by regular copy. Nothing original is written.

Records sha256/bytes/mtime and provenance for:
- INTERRUPTED: the four jobs launched in the original runtime with no completion record when the original main process
  exited (p02_battery source, p02_battery hybrid-baseline-owner, p03_rootprobe source, p04_semantic source). Their absent
  receipts/results are asserted and their leftovers copied under interrupted/ (the symlink is recorded, not followed);
- completed original receipts -> receipts/ (same names; later probes read them by name);
- original probes -> probes/original/ verbatim; continuation probes (run, p02_battery, p03_rootprobe, p04_semantic,
  p06_compare) -> probes/ with ONLY the BASE path literal replaced (exactly one replacement each);
- work/source and work/hybrid-baseline-owner -> work/ (regular, byte-equal, distinct inodes, nlink 1), verified against the
  captured baseline hashes and the original p05 after-hashes; work/baseline verified in place, not copied;
- delta and the completed baseline root-probe directory -> carried/;
- a full manifest of the original runtime (receipts/c00-original-manifest.json) for the later unchanged check.
Output: receipts/c00-carry.json.
"""
import hashlib, json, os, shutil, sys
from pathlib import Path

ORIG = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1')
BASE = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1-continuation.v1')
R = BASE / 'receipts'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
if any((BASE / n).exists() for n in ('receipts', 'probes', 'work', 'interrupted', 'carried')):
    print('continuation outputs exist; refusing'); sys.exit(2)
R.mkdir(parents=True)


def manifest(root):
    files, links = {}, {}
    for dirpath, dirnames, filenames in os.walk(root):
        for n in dirnames + filenames:
            p = Path(dirpath) / n
            if p.is_symlink(): links[str(p.relative_to(root))] = os.readlink(p)
        for n in filenames:
            p = Path(dirpath) / n
            if not p.is_symlink(): files[str(p.relative_to(root))] = sha(p)
    return {'files': files, 'symlinks': links}


def copy(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    a, b = src.stat(), dst.stat()
    return {'from': str(src), 'to': str(dst), 'sha256': sha(dst), 'bytes': b.st_size, 'sourceMtime': a.st_mtime,
            'regularByteEqual': a.st_ino != b.st_ino and b.st_nlink == 1 and src.read_bytes() == dst.read_bytes()}


orig_manifest = manifest(ORIG)
(R / 'c00-original-manifest.json').write_text(json.dumps(orig_manifest, indent=1) + '\n')
out = {'original': str(ORIG), 'continuation': str(BASE), 'originalManifestSha256': sha(R / 'c00-original-manifest.json'),
       'originalFileCount': len(orig_manifest['files']), 'originalSymlinks': orig_manifest['symlinks']}
problems = []

JOBS = {
    'p02_battery source': {'receipt': 'receipts/p02_battery.source.receipt.json', 'result': 'receipts/p02-source.json',
                           'leftovers': ['receipts/p02-source-checker-stdout.json', 'receipts/p02-source-checker-stderr.txt']},
    'p02_battery hybrid-baseline-owner': {'receipt': 'receipts/p02_battery.hybrid-baseline-owner.receipt.json', 'result': 'receipts/p02-hybrid-baseline-owner.json',
                                          'leftovers': ['receipts/p02-hybrid-baseline-owner-checker-stdout.json', 'receipts/p02-hybrid-baseline-owner-checker-stderr.txt']},
    'p03_rootprobe source': {'receipt': 'receipts/p03_rootprobe.source.receipt.json', 'result': 'receipts/p03-rootprobe-source.json',
                             'leftovers': ['work/rootprobe-source/checker-stdout.json', 'work/rootprobe-source/checker-stderr.txt', 'work/rootprobe-source/probe.py']},
    'p04_semantic source': {'receipt': 'receipts/p04_semantic.source.receipt.json', 'result': 'receipts/p04-semantic-source.json', 'leftovers': []},
}
interrupted, leftover_set = {}, set()
for job, spec in JOBS.items():
    row = {'receiptPresent': (ORIG / spec['receipt']).exists(), 'resultPresent': (ORIG / spec['result']).exists(),
           'leftovers': [copy(ORIG / rel, BASE / 'interrupted' / rel) for rel in spec['leftovers']]}
    if row['receiptPresent'] or row['resultPresent']: problems.append('job has a completion record: ' + job)
    leftover_set |= set(spec['leftovers'])
    interrupted[job] = row
interrupted['p03_rootprobe source']['sourceSymlink'] = os.readlink(ORIG / 'work/rootprobe-source/source')
interrupted['p03_rootprobe source']['reportPresent'] = (ORIG / 'work/rootprobe-source/report.json').exists()
out['interrupted'] = interrupted

out['receipts'] = [copy(p, R / p.name) for p in sorted((ORIG / 'receipts').iterdir())
                   if p.is_file() and 'receipts/' + p.name not in leftover_set]

out['probesOriginal'] = [copy(p, BASE / 'probes/original' / p.name) for p in sorted((ORIG / 'probes').glob('*.py'))]
OLD, NEW = "Path('%s')" % ORIG, "Path('%s')" % BASE
derived = []
for name in ('run.py', 'p02_battery.py', 'p03_rootprobe.py', 'p04_semantic.py', 'p06_compare.py'):
    text = (ORIG / 'probes' / name).read_text()
    count = text.count(OLD)
    if count != 1: problems.append('BASE literal count %d in %s' % (count, name))
    (BASE / 'probes' / name).write_text(text.replace(OLD, NEW))
    derived.append({'probe': name, 'originalSha256': sha(ORIG / 'probes' / name), 'continuationSha256': sha(BASE / 'probes' / name),
                    'replaced': [OLD, NEW], 'count': count})
out['probesDerived'] = derived

baseline = json.loads((ORIG / 'receipts/baseline-file-hashes.json').read_text())
p05 = json.loads((ORIG / 'receipts/p05-summary.json').read_text())
after = {r['path']: r['after'] for r in p05['changedFiles']}
CHECKER = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
expected = {'source': dict(baseline, **after), 'hybrid-baseline-owner': dict(baseline, **{CHECKER: after[CHECKER]})}
trees = {}
for tree, want in expected.items():
    src = ORIG / 'work' / tree
    m = manifest(src)
    rows = [copy(src / rel, BASE / 'work' / tree / rel) for rel in sorted(m['files'])]
    got = manifest(BASE / 'work' / tree)['files']
    trees[tree] = {'files': len(rows), 'symlinks': m['symlinks'], 'allRegularByteEqual': all(r['regularByteEqual'] for r in rows),
                   'originalMatchesExpected': m['files'] == want, 'copyMatchesExpected': got == want,
                   'differsFromBaseline': sorted(p for p in want if want[p] != baseline[p])}
    if not (trees[tree]['allRegularByteEqual'] and trees[tree]['originalMatchesExpected'] and trees[tree]['copyMatchesExpected'] and not m['symlinks']):
        problems.append('tree custody: ' + tree)
trees['baseline(verified in place, not copied)'] = {'matchesCapturedBaseline': manifest(ORIG / 'work/baseline')['files'] == baseline}
if not trees['baseline(verified in place, not copied)']['matchesCapturedBaseline']: problems.append('baseline tree drift')
out['trees'] = trees

out['carried'] = [copy(ORIG / 'delta-vs-captured-source.diff', BASE / 'carried/delta-vs-captured-source.diff')]
if out['carried'][0]['sha256'] != p05['delta']['sha256']: problems.append('carried delta differs from p05')
rp = ORIG / 'work/rootprobe-baseline'
out['carried'] += [copy(p, BASE / 'carried/rootprobe-baseline' / p.name) for p in sorted(rp.iterdir()) if p.is_file() and not p.is_symlink()]
out['carriedRootprobeBaselineSymlink'] = os.readlink(rp / 'source')
out['problems'] = problems
out['ok'] = not problems and all(r['regularByteEqual'] for r in out['receipts'] + out['probesOriginal'] + out['carried'])
(R / 'c00-carry.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('receipts', 'probesOriginal', 'carried')}, indent=1))
print('receipts carried', len(out['receipts']), 'probes', len(out['probesOriginal']), 'carried', len(out['carried']))
sys.exit(0 if out['ok'] else 1)
