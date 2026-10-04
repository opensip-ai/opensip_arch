"""Count the Rust3 request subjects of every Rust-bearing T2 repository, at its pinned tree, offline.

Rust3's subject rule (rust-provider-protocol.v2 planAndDomainProjection.subjectsAlgorithm, steps 1-2) selects
every file-kind snapshot entry whose path ends in ".rs" and whose byteLength is greater than zero. The sealed
snapshot is M3-C r7 item 6's: every regular file the walk reaches, minus pruned trees (node_modules, .git, .hg,
.svn, .jj, a Cargo target beside a Cargo.toml, the root .opensip), ignorePaths, symlinks and special files.
With no ignorePaths, a fetched tree's regular non-empty .rs blobs outside pruned trees are exactly that set.

Two read-only sources, both already on this machine; nothing is fetched:
  A. the E0 probe's bare repositories (scratchpad e0/t2a/git/<id>.git): `git ls-tree -r -l -z --full-tree`
     at the pinned commit, after checking that the commit's tree equals the manifest's gitTree. It gives
     exact byte lengths, so the inline subjects array's deterministic-CBOR size is exact.
  B. the T2b measurement's per-blob listings (scratchpad t2b/results/<owner>__<repo>.{json,blobs.tsv}),
     after checking that the listing's commit, tree and QD-22 tree digest equal the manifest's. A listed
     .rs blob is non-empty exactly when its physical line count is positive. Symlinks are not listed.
     It has no byte lengths, so the encoded size there is an estimate (endByte taken as a 3-byte uint).
Source B covers all 22 entries; source A covers the 9 T2a medium Rust-bearing entries and must agree.

Usage: python3.14 -I -B count_rust_subjects.py [--e0-git DIR] [--t2b-results DIR] [--check]
Writes (or with --check compares) rust-subject-counts.json beside this script. No git command here runs
hooks, fetches or writes: ls-tree and rev-parse only, with core.hooksPath=/dev/null.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
MANIFEST = 'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json'
OUT = HERE / 'rust-subject-counts.json'
SCRATCH = Path('/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad')
PRUNED_SEGMENTS = {'node_modules', '.git', '.hg', '.svn', '.jj'}
CAP = 256                       # ProtocolLimitsV3.maxSubjectsPerStage (RPP:106; NE:2934)
MAX_SNAPSHOT_ENTRIES = 200000   # ProtocolLimitsV3.maxSnapshotEntries (RPP:99)
SNAPSHOT2_ROWS = 100000         # source-inventory maxItems (IDS:2739; MC item 5)
FRAME = 67108864                # maxFramePayloadBytes (RPP:97)
SUBJECT_ID_CHARS = len('rust-file:sha256:') + 64


def uint_len(n):
    return 1 if n < 24 else 2 if n < 256 else 3 if n < 65536 else 5 if n < 2 ** 32 else 9


def text_len(s):
    n = len(s.encode('utf-8'))
    return uint_len(n) + n


# SubjectV2 {subjectOrdinal, subjectId, path, startByte, endByte}: a 5-entry map header plus its five text keys.
KEYS = sum(text_len(k) for k in ('subjectOrdinal', 'subjectId', 'path', 'startByte', 'endByte'))


def row_len(ordinal, path, byte_length):
    return 1 + KEYS + uint_len(ordinal) + text_len('x' * SUBJECT_ID_CHARS) + text_len(path) + uint_len(0) \
        + uint_len(byte_length)


def array_len(rows):
    return uint_len(len(rows)) + sum(row_len(i, p, b) for i, (p, b) in enumerate(rows))


def pruned(path, cargo_dirs):
    segs = path.split('/')
    if segs[0] == '.opensip' or any(s in PRUNED_SEGMENTS for s in segs[:-1]):
        return True
    return any(s == 'target' and '/'.join(segs[:i]) in cargo_dirs for i, s in enumerate(segs[:-1]))


def git(repo, *args):
    return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(repo), *args], check=True,
                          capture_output=True).stdout


def source_a(e0, entry):
    repo = e0 / f"{entry['id']}.git"
    if not repo.is_dir():
        return None
    tree = git(repo, 'rev-parse', entry['commit'] + '^{tree}').decode().strip()
    if tree != entry['gitTree']:
        raise SystemExit(f"{entry['id']}: E0 tree {tree} differs from the manifest")
    rows, cargo_dirs = [], set()
    for item in git(repo, 'ls-tree', '-r', '-l', '-z', '--full-tree', entry['commit']).split(b'\0'):
        if not item:
            continue
        meta, path = item.split(b'\t', 1)
        mode, kind, _, size = meta.split()
        path = path.decode('utf-8')
        if kind == b'blob' and path.rsplit('/', 1)[-1] == 'Cargo.toml':
            cargo_dirs.add(path.rsplit('/', 1)[0] if '/' in path else '')
        rows.append((mode.decode(), kind.decode(), path, None if size == b'-' else int(size)))
    rs = [r for r in rows if r[1] == 'blob' and r[2].endswith('.rs') and not pruned(r[2], cargo_dirs)]
    regular = [r for r in rs if r[0] in ('100644', '100755')]
    subjects = sorted(((r[2], r[3]) for r in regular if r[3] > 0), key=lambda x: x[0].encode('utf-8'))
    return {'source': 'A: E0 bare repository, git ls-tree at the pinned commit (tree checked)',
            'rsBlobs': len(rs), 'symlinkRs': len(rs) - len(regular),
            'emptyRs': sum(1 for r in regular if r[3] == 0), 'subjects': len(subjects),
            'pathBytes': sum(len(p.encode('utf-8')) for p, _ in subjects),
            'inlineArrayBytes': array_len(subjects), 'inlineArrayBytesExact': True}


def source_b(results, entry):
    owner, repo = entry['url'].rstrip('/').split('/')[-2:]
    meta = json.loads((results / f'{owner}__{repo}.json').read_text())
    if (meta['commit'], meta['tree'], meta['qd22TreeDigest']) != (entry['commit'], entry['gitTree'],
                                                                  entry['treeDigest']['value']):
        raise SystemExit(f"{entry['id']}: T2b listing is not at the manifest pin")
    cargo_dirs = set()
    for p in meta['filesOfInterest'].get('Cargo.toml', []):
        if p.startswith('... '):
            raise SystemExit(f"{entry['id']}: Cargo.toml list truncated")
        cargo_dirs.add(p.rsplit('/', 1)[0] if '/' in p else '')
    rs = []
    for line in (results / f'{owner}__{repo}.blobs.tsv').read_text(encoding='utf-8').splitlines():
        cols = line.split('\t')
        if cols[2] == 'rust' and cols[7].endswith('.rs') and not pruned(cols[7], cargo_dirs):
            rs.append((cols[7], int(cols[1])))
    subjects = sorted((p for p, n in rs if n > 0), key=lambda p: p.encode('utf-8'))
    return {'source': 'B: T2b per-blob listing at the pinned commit (commit, tree and QD-22 digest checked)',
            'rsBlobs': len(rs), 'emptyRs': sum(1 for _, n in rs if n == 0), 'subjects': len(subjects),
            'pathBytes': sum(len(p.encode('utf-8')) for p in subjects),
            'inlineArrayBytes': array_len([(p, 1000) for p in subjects]), 'inlineArrayBytesExact': False}


def build(e0, results):
    manifest = json.loads((ARCH / MANIFEST).read_text())
    rows = []
    for entry in manifest['repositories']:
        if 'rust' not in entry.get('lines', {}):
            continue
        b = source_b(results, entry)
        a = source_a(e0, entry)
        if a is not None and (a['subjects'], a['pathBytes']) != (b['subjects'], b['pathBytes']):
            raise SystemExit(f"{entry['id']}: sources A and B disagree")
        best = a or b
        per_row = best['inlineArrayBytes'] / best['subjects']
        rows.append({
            'id': entry['id'], 'role': entry['role'],
            'rustClass': entry.get('languageClasses', {}).get('rust', {}).get('class'),
            'commit': entry['commit'], 'gitTree': entry['gitTree'],
            'manifestRustFiles': entry['lines']['rust']['files'], 'treeBlobEntries': entry['treeDigest']['blobEntries'],
            'nonEmptyRsSubjects': best['subjects'], 'emptyRs': best['emptyRs'],
            'measuredBy': 'A and B (agree)' if a else 'B',
            'overCap256': best['subjects'] > CAP,
            'overSnapshot2Rows': entry['treeDigest']['blobEntries'] > SNAPSHOT2_ROWS,
            'overMaxSnapshotEntries': entry['treeDigest']['blobEntries'] > MAX_SNAPSHOT_ENTRIES,
            'inlineSubjectsArrayBytesPerStage': best['inlineArrayBytes'],
            'inlineSubjectsArrayBytesExact': best['inlineArrayBytesExact'],
            'meanInlineRowBytes': round(per_row, 1),
            'stagesFittingOneAnalyzeFrame': FRAME // best['inlineArrayBytes'],
        })
    rows.sort(key=lambda r: (r['nonEmptyRsSubjects'], r['id']))
    over = [r['id'] for r in rows if r['overCap256']]
    return {
        'standing': ('Measured offline at each entry\'s pinned tree; nothing fetched. Counts are of non-empty regular '
                     '.rs blobs outside pruned trees, which is Rust3\'s subject set for the whole repository as the '
                     'project root with no ignorePaths. "Inline" bytes are the deterministic-CBOR length of the '
                     'StageAnalysisDomainV2.subjects array that one stage carries in Analyze today; each stage repeats '
                     'it. Bytes are exact under source A and estimated under B (endByte as a 3-byte uint).'),
        'manifest': MANIFEST,
        'limits': {'maxSubjectsPerStage': CAP, 'maxSnapshotEntries': MAX_SNAPSHOT_ENTRIES,
                   'snapshot2SourceInventoryRows': SNAPSHOT2_ROWS, 'maxFramePayloadBytes': FRAME,
                   'maxAnalyzeStages': 256},
        'summary': {'rustBearingEntries': len(rows), 'overCap256': len(over), 'overCap256Ids': over,
                    'measuredByBothSources': sum(1 for r in rows if r['measuredBy'].startswith('A')),
                    'differsFromManifestFiles': [r['id'] for r in rows
                                                 if r['nonEmptyRsSubjects'] != r['manifestRustFiles']]},
        'repositories': rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--e0-git', default=str(SCRATCH / 'e0/t2a/git'))
    parser.add_argument('--t2b-results', default=str(SCRATCH / 't2b/results'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    out = (json.dumps(build(Path(args.e0_git), Path(args.t2b_results)), indent=2) + '\n').encode('ascii')
    if args.check:
        if OUT.read_bytes() != out:
            raise SystemExit('rust-subject-counts.json differs')
        print('rust-subject-counts.json reproduces')
    else:
        OUT.write_bytes(out)
        print(out.decode())


if __name__ == '__main__':
    main()
