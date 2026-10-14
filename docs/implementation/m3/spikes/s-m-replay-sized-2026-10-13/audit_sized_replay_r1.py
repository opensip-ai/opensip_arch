from pathlib import Path
import json, hashlib, math, statistics, subprocess, os, difflib
# Read-only audit of the workload-sized synthetic replay scaling unit (two series). Series r1 ran the CLOSED accepted release
# image e82a4e2f over each selected packet and is retained as history: it completed sizes whose packet fits the product
# canonical MAX_BYTES (4 MiB) and refused the first larger packet (678) with ByteLimit while parsing the whole packet as
# one document. Series r2 ran the rows-transport variant 7635c002 (input loading only; built from the git-archive export
# of product 37581132, the closed image's product, with the accepted lock and recipe) over all 14 sizes.
# Checks: closed generator, schema, image and variant pins; the variant source diff; the export tree against
# `git ls-tree 37581132`; every packet and rows hash; packet-193 reproduction; each set's 3+7 shape, priority and full
# replay of exactly `count` findings; r1/r2 agreement where both ran; monotonicity of r2 medians. Per workload row it
# reports the synthetic scenario at that row's source count (one exists/file fact, finding and fingerprint per source).
# These are NOT a lower bound on SM-9 for the real workload (Codex SM-REPLAY-SIZED-R1-RF-01): real rules can emit zero
# findings for a source, and no work-dominance relation to real graphs is established. No F, T, 2 s comparison or
# outcome is derived. Writes sized-replay-checks-r1.json.
H = Path(__file__).resolve().parent; V = Path('/tmp/opensip-implementation/sm-replay-native-rows-2026-10-13').resolve()
P = Path('/Users/sb/code/opensip-ai/opensip')
N = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes/s-m-full-replay-partial-2026-10-09/native')
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E.pop(k, None)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
MAX_BYTES = 4 * 1024 * 1024  # opensip-identity canonical.rs MAX_BYTES at 37581132 (unchanged at the current head)
PRODUCT = '37581132d8099b8fb4ad9ef8fb2f90ff8b89d02d'
# Closed pieces.
closed = json.loads((N / 'build-release.json').read_text()); assert closed['sha256'] == 'e82a4e2f5f487c7c9d272f4a9af5c337d61ff6868eaa165c8ea277f876b8a843' and sha(closed['executable']) == closed['sha256']
for n in ['prepare_packet.py', 'remint_selected_schema.py']: assert (H / n).read_bytes() == (N / n).read_bytes(), n
assert b'pub const MAX_BYTES: usize = 4 * 1024 * 1024;' in subprocess.check_output(['/usr/bin/git', 'show', PRODUCT + ':crates/identity/src/canonical.rs'], cwd=P, env=E)
# Variant: source diff confined to input loading; build pin; export equals the product tree at 37581132.
variant = json.loads((V / 'build-release.json').read_text()); assert variant['sha256'] == '7635c002b2ed877f89582360b6eae54e8de1a6c91811a4f188b083919609fc24' and sha(variant['executable']) == variant['sha256'] and variant['productCommit'] == PRODUCT
assert (V / 'closed-main.rs').read_bytes() == (N / 'src/main.rs').read_bytes() and (V / 'Cargo.lock').read_bytes() == (N / 'Cargo.lock').read_bytes()
a = (V / 'closed-main.rs').read_text().split('\n'); b = (V / 'src/main.rs').read_text().split('\n')
changed = [(op, i1, i2, j1, j2) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if op != 'equal']
assert changed == [('replace', 8, 11, 8, 12)], changed
assert all(('parse_json' in l or 'objects' in l or 'blobs' in l) for l in b[8:12]) and 'replay_run' not in '\n'.join(b[8:12])
cn = (N / 'Cargo.toml').read_text().replace('/Users/sb/code/opensip-ai/opensip/crates', str(V / 'product-37581132/crates').replace('/private/tmp', '/tmp'))
assert (V / 'Cargo.toml').read_text() == cn
tree = {}
for line in subprocess.check_output(['/usr/bin/git', 'ls-tree', '-r', '-z', PRODUCT], cwd=P, env=E).split(b'\0'):
    if line: meta, path = line.split(b'\t', 1); mode, kind, obj = meta.split(b' '); tree[path.decode()] = (mode.decode(), obj.decode())
X = V / 'product-37581132'; seen = set()
for dirpath, dirnames, filenames in os.walk(X):
    for f in filenames + [d for d in dirnames if (Path(dirpath) / d).is_symlink()]:
        p = Path(dirpath) / f; rel = p.relative_to(X).as_posix(); seen.add(rel)
        raw = os.readlink(p).encode() if p.is_symlink() else p.read_bytes()
        assert hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest() == tree[rel][1], rel
assert seen == {k for k, (m, _) in tree.items() if m != '160000'}
assert sha(X / 'schemas/sources/native-v2.schema.json') == sha(H / 'selected-native-v2-at-2fbb75c-parent.schema.json') == 'e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773'
# Packets and rows.
packets = json.loads((H / 'sized-packets-r1.json').read_text())
assert sha(H / 'packet-193-selected.json') == sha(N / 'packet-193-selected.json') == 'f33da67037c8bf6d67b2694ce7f4833f70f78549ace1bcf6ca4cded88d593e32' and sha(H / 'packet-193.json') == sha(N / 'packet-193.json')
conv = {json.loads(l)['sourceSha256']: json.loads(l) for l in (V / 'convert.log').read_text().splitlines()}
for c, row in packets['packets'].items():
    assert sha(row['path']) == row['sha256'] and sha(row['raw']['path']) == row['raw']['sha256']
    r = conv[row['sha256']]; assert sha(r['rows']) == r['sha256'] and r['reassemblesEqual'] is True and r['maxLineBytes'] <= MAX_BYTES
def check_set(s, count):
    runs = s['runs']; assert [r['ordinal'] for r in runs] == list(range(10)) and [r['warmup'] for r in runs] == [True] * 3 + [False] * 7
    for r in runs: assert r['fullReplayPassed'] is True and r['findings'] == count and r['observedChildNiceness'] == 10
    vals = [r['completeReplayNanos'] for r in runs if not r['warmup']]
    assert statistics.median(vals) == s['medianReplayNanos'] and max(vals) == s['maxReplayNanos'] and len({(r['objects'], r['blobs']) for r in runs}) == 1
    return dict(count=count, objects=runs[0]['objects'], blobs=runs[0]['blobs'], medianReplayMs=s['medianReplayNanos'] / 1e6, maxReplayMs=s['maxReplayNanos'] / 1e6,
                minReplayMs=min(vals) / 1e6, medianWholeProcessMs=s['medianWholeProcessNanos'] / 1e6, maxRssBytes=max(r['rssBytes'] for r in runs))
# Series r1 (closed image): completed sets, then the retained ByteLimit refusal.
r1 = json.loads((H / 'sized-replay-results-r1.json').read_text()); assert r1['binary'] == closed
s1 = {s['count']: check_set(s, s['count']) for s in r1['sets']}
fits = sorted(int(c) for c, row in packets['packets'].items() if row['bytes'] <= MAX_BYTES); over = sorted(int(c) for c, row in packets['packets'].items() if row['bytes'] > MAX_BYTES)
assert sorted(s1) == fits and over[0] == 678
assert sorted(p.name for p in H.glob('replay-678-*')) == ['replay-678-0.stderr', 'replay-678-0.stdout'] and (H / 'replay-678-0.stdout').read_bytes() == b''
assert 'called `Result::unwrap()` on an `Err` value: ByteLimit' in (H / 'replay-678-0.stderr').read_text() and 'src/main.rs:9:' in (H / 'replay-678-0.stderr').read_text()
assert "AssertionError: (678, 0," in (H / 'replay.log').read_text()
# Series r2 (rows variant): every size.
r2 = json.loads((H / 'sized-replay-results-r2.json').read_text()); assert r2['binary'] == variant and r2['sizes'] == packets['sizes']
s2 = {}
for s in r2['sets']:
    c = s['count']; row = packets['packets'][str(c)]; assert s['packet'] == row and s['rows'] == conv[row['sha256']]; s2[c] = check_set(s, c)
    s2[c].update(packetSha256=row['sha256'], packetBytes=row['bytes'], rowsSha256=s['rows']['sha256'], rowsBytes=s['rows']['bytes'], maxRowBytes=s['rows']['maxLineBytes'])
assert sorted(s2) == sorted(int(c) for c in packets['packets'])
agreement = [dict(count=c, r1MedianMs=s1[c]['medianReplayMs'], r2MedianMs=s2[c]['medianReplayMs'], ratio=s2[c]['medianReplayMs'] / s1[c]['medianReplayMs'], sameObjectsBlobs=(s1[c]['objects'], s1[c]['blobs']) == (s2[c]['objects'], s2[c]['blobs'])) for c in fits]
assert all(x['sameObjectsBlobs'] for x in agreement)
order = sorted(s2); medians = [s2[c]['medianReplayMs'] for c in order]; monotone = all(x <= y for x, y in zip(medians, medians[1:]))
xs = [math.log(c) for c in order]; ys = [math.log(m) for m in medians]; mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
accepted193 = json.loads((N / 'release-results.json').read_text())
rows = []
for wid, c in packets['sizes'].items():
    s = s2[c]
    rows.append(dict(workload=wid, sizingSources=c, syntheticScenarioMedianMs=s['medianReplayMs'], syntheticScenarioMaxMs=s['maxReplayMs'], syntheticScenarioMinMs=s['minReplayMs'],
                     boundsRealWorkloadSM9=False))
result = dict(standing='UNREVIEWED READONLY AUDIT OF THE WORKLOAD-SIZED SYNTHETIC REPLAY SCALING UNIT r1 ROUND 2 (SERIES r1 CLOSED IMAGE, SERIES r2 ROWS VARIANT); LEAD macOS PRELIMINARY, NOT D12; NOT A BOUND ON REAL SM-9; NO F, T OR OUTCOME',
              leadDecision='LD-SM9-BOUNDARY-AND-LOWER-BOUND-SIZING as corrected 2026-10-13: boundary kept; sizing is a synthetic scaling scenario, not a lower bound (SM-REPLAY-SIZED-R1-RF-01)', closedImage=closed, variantImage=variant, productCommitMeasured=PRODUCT, exportTreeEqualsProductCommit=True,
              variantDiffConfinedToInputLoading=True, closedGeneratorBytesUnchanged=True, acceptedPacket193Reproduced=True, canonicalMaxBytes=MAX_BYTES,
              selectedSchema=dict(path='selected-native-v2-at-2fbb75c-parent.schema.json', sha256=sha(H / 'selected-native-v2-at-2fbb75c-parent.schema.json')),
              series1=dict(image='closed e82a4e2f', completedSizes=fits, refusedFirstAt=678, refusal='ByteLimit at src/main.rs:9 (parse_json of the whole packet)', packetSizesOverMaxBytes=over, sets=[s1[c] for c in fits]),
              series2=dict(image='rows variant 7635c002', sets=[s2[c] for c in order]), seriesAgreement=agreement,
              accepted193ReleaseMedianMs=accepted193['medianReplayNanos'] / 1e6, mediansMonotoneInSize=monotone, logLogSlopeDescriptive=slope,
              largestRowBytes=max(s2[c]['maxRowBytes'] for c in order),
              syntheticFamily='closed prepare_packet.py: one exists/relation=file/minResolution=enumerated predicate; exactly one fact, one finding and one finding fingerprint per synthetic source',
              notABound='Real rules can emit zero findings for a source (evaluator composition.rs at 37581132 emits a finding only when the predicate is true) and real graph shape, predicate work and retained bytes are not ordered by this family; these scenarios bound neither real SM-9 nor F, and outcome (A) remains unestablished for all 14 rows.',
              workloads=rows, lowerBoundEstablished=False, realWorkloadInference=False, comparedWithEditTarget=False, round1Finding='SM-REPLAY-SIZED-R1-RF-01', SM9LowerBoundOnly=False, SM9FigureComplete=False, SM9PlaceholderFilled=False, FComputed=False, TComputed=False, outcomeRecorded=False,
              SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(H / 'sized-replay-checks-r1.json').write_text(json.dumps(result, indent=1) + '\n')
for x in agreement: print('agree', x['count'], round(x['r1MedianMs'], 1), round(x['r2MedianMs'], 1), round(x['ratio'], 4))
for c in order: print(c, s2[c]['objects'], s2[c]['blobs'], round(s2[c]['medianReplayMs'], 3), round(s2[c]['maxReplayMs'], 3))
for r in rows: print(r['workload'], r['sizingSources'], round(r['syntheticScenarioMedianMs'], 1))
print('monotone', monotone, 'slope', round(slope, 3))
