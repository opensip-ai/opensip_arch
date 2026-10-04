"""F8b step 3 (evidence, not a gate): compare rebuild-01 and rebuild-02 executables.

Both binaries are pinned, copied to a private directory, and their ad-hoc code signatures
removed with `codesign --remove-signature` (native-repin-selection-v1's sigequiv method).
Every `opensip-generator-build-XXXXXXXX` suffix is then masked, and the 16-byte LC_UUID
payload is zeroed. The result says whether the normalized bytes are equal. The build logs
are compared with the suffix masked, then as sorted lines with Cargo's elapsed time normalized. Read-only for both binaries.
This compares two observed builds only; it says nothing about rebuild403."""
import hashlib, json, re, shutil, struct, subprocess, sys, tempfile
from pathlib import Path
B1, B2 = Path(sys.argv[1]), Path(sys.argv[2])
PINS = {'rebuild-01': {'bytes': 7202304, 'sha256': '4388e707035e0ea4b0c3dcd9206e55fd7045e58658a443fb13e04a12847a6959'},
        'rebuild-02': json.loads((B2 / 'receipt.json').read_bytes())['executable']}
SUFFIX = re.compile(rb'opensip-generator-build-([a-z0-9_]{8})')
TIMING = re.compile(rb'in [0-9]+(?:[.][0-9]+)?s')
def pin(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def lc_uuid(raw):
    magic, _, _, _, ncmds, _, _, _ = struct.unpack_from('<IiiIIIII', raw, 0)
    assert magic == 0xfeedfacf, 'expected a thin 64-bit Mach-O'
    off, found = 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', raw, off)
        if cmd == 0x1b: found.append(off + 8)
        off += size
    assert len(found) == 1, 'expected exactly one LC_UUID'
    return found[0]
def normalize(raw):
    raw = bytearray(raw); suffixes = [m.group(1).decode() for m in SUFFIX.finditer(raw)]
    for m in SUFFIX.finditer(bytes(raw)): raw[m.start(1):m.end(1)] = b'XXXXXXXX'
    u = lc_uuid(raw); uuid = raw[u:u + 16].hex(); raw[u:u + 16] = bytes(16)
    return bytes(raw), sorted(set(suffixes)), len(suffixes), uuid
result = {'standing': 'comparison evidence for two observed builds (rebuild-01, rebuild-02); not a gate; no rebuild403 claim; no reproducible-build claim', 'binaries': {}}
work = Path(tempfile.mkdtemp(prefix='f8b-exe-'))
norm = {}
for label, d in (('rebuild-01', B1), ('rebuild-02', B2)):
    exe = d / 'opensip-contract-generator'; raw = exe.read_bytes()
    assert pin(raw) == PINS[label], label
    copy = work / label; shutil.copyfile(exe, copy); copy.chmod(0o600)
    subprocess.run(['/usr/bin/codesign', '--remove-signature', str(copy)], check=True, capture_output=True)
    unsigned = copy.read_bytes()
    n, suffixes, count, uuid = normalize(unsigned)
    norm[label] = n
    result['binaries'][label] = {'path': str(exe), 'signed': pin(raw), 'unsigned': pin(unsigned), 'normalized': pin(n),
                                 'buildPathSuffixes': suffixes, 'buildPathOccurrences': count, 'lcUuid': uuid}
a, b = norm['rebuild-01'], norm['rebuild-02']
result['unsignedLengthsEqual'] = result['binaries']['rebuild-01']['unsigned']['bytes'] == result['binaries']['rebuild-02']['unsigned']['bytes']
result['normalizedEqual'] = a == b
if not result['normalizedEqual'] and len(a) == len(b):
    diffs = [i for i in range(len(a)) if a[i] != b[i]]
    result['differingBytes'] = len(diffs); result['firstDifferingOffsets'] = diffs[:32]
logs = {}
for name in ('build.stdout.jsonl', 'build.stderr.log'):
    x, y = (B1 / name).read_bytes(), (B2 / name).read_bytes()
    mx, my = SUFFIX.sub(b'opensip-generator-build-XXXXXXXX', x), SUFFIX.sub(b'opensip-generator-build-XXXXXXXX', y)
    # Cargo compiles in parallel, so message order varies; the Finished line carries elapsed time.
    tx, ty = (TIMING.sub(rb'in Ns', v) for v in (mx, my))
    logs[name] = {'rebuild-01': pin(x), 'rebuild-02': pin(y), 'equalAfterMasking': mx == my,
                  'equalAsSortedLinesAfterMaskingAndTiming': sorted(tx.splitlines()) == sorted(ty.splitlines())}
result['buildLogs'] = logs
for label, d in (('rebuild-01', B1), ('rebuild-02', B2)):
    assert pin((d / 'opensip-contract-generator').read_bytes()) == PINS[label], label + ' changed during comparison'
shutil.rmtree(work)
print(json.dumps(result, indent=2))
