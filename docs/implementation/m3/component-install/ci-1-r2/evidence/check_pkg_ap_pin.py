"""CI-1's pin by reference (LAW item 3): the codec's profile constants equal PKG-AP's own text in PKG at its pinned
SHA-256. Checks: PKG's bytes hash to PROFILE_SOURCE_SHA256; the codec's LAYOUT table equals headerLayout.fields
(name, offset, length) in order; the capacities equal numericCapacity, pathBytes and linkTargetBytes; the four
Capacity tokens are doesNotMintSchemaCaps' four; the typeflag bytes are typeflagBytes'; the profile id is PKG-AP's
id; and CI-T1's tests are exactly PKG-AP's 15 goldenAndNegativeCases, one test each.
Usage: check_pkg_ap_pin.py PRODUCT_WORKTREE ARCHITECTURE OUT_JSON"""
import hashlib, json, re, sys
from pathlib import Path
W, A, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
src = (W / 'crates/security/src/archive_profile.rs').read_text()
tests = (W / 'crates/security/src/archive_profile_tests.rs').read_text()
def const(name):
    return re.search(r'pub const ' + name + r': [^=]+= *\n? *"?([^";]+)"?;', src).group(1).strip()
rel = const('PROFILE_SOURCE'); raw = (A / rel).read_bytes(); pkg = json.loads(raw); ap = pkg['archiveProfile']; ba = ap['byteAlgorithm']
rows = []
def check(name, ok, detail=None): rows.append(dict(check=name, passed=bool(ok), detail=detail))
check('pkg-sha256', hashlib.sha256(raw).hexdigest() == const('PROFILE_SOURCE_SHA256'), const('PROFILE_SOURCE_SHA256'))
check('profile-id', ap['id'] == const('PROFILE_ID'), ap['id'])
layout = [(n, int(o), int(l)) for n, o, l in re.findall(r'\(HeaderField::\w+, "(\w+)", (\d+), (\d+)\)', src)]
check('header-layout', layout == [(f['name'], f['off'], f['len']) for f in ba['headerLayout']['fields']], layout)
check('block-size', ba['headerLayout']['blockSize'] == 512 and 'const BLOCK: usize = 512;' in src)
cap = ba['headerLayout']['numericCapacity']
num = lambda s: int(s.replace('_', ''), 8) if s.startswith('0o') else int(s.replace('_', ''))
check('mode-capacity', '0..2097151' in cap['mode'] and num(const('MAX_MODE')) == 2097151, const('MAX_MODE'))
check('size-capacity', '0..8589934591' in cap['size'] and num(const('MAX_SIZE')) == 8589934591, const('MAX_SIZE'))
check('path-bytes', 'name[0:100]' in ba['pathBytes'] and const('MAX_PATH_BYTES') == '100')
check('link-bytes', 'linkname[0:100]' in ba['linkTargetBytes'] and const('MAX_LINK_TARGET_BYTES') == '100')
tokens = re.findall(r'[A-Z]+(?:-[A-Z]+)+', ba['doesNotMintSchemaCaps'])
check('capacity-tokens', sorted(tokens) == sorted(re.findall(r'=> "([A-Z-]+)",', src)), tokens)
tf = ba['typeflagBytes']
check('typeflags', tf['file'].startswith("0x30") and tf['dir'].startswith('0x35') and tf['symlink'].startswith('0x32')
      and "RowKind::File { length, .. } => (length, b'0')" in src and "RowKind::Dir => (0, b'5')" in src and "(0, b'2')" in src)
check('archive-length-formula', ba['archiveLength'] == '512 * N_members + sum over file members of 512*ceil(length/512) + 1024.')
cases = [c.split(':')[0] for c in ba['goldenAndNegativeCases']]
names = [c.lower().replace('-', '_') for c in cases]
defined = re.findall(r'#\[test\]\nfn (at_archive_\w+)\(', tests)
check('ci-t1-cases', len(cases) == 15 and sorted(defined) == sorted(names) and all(tests.count(f'fn {n}(') == 1 for n in names), dict(cases=cases, tests=defined))
ok = all(r['passed'] for r in rows)
OUT.write_text(json.dumps(dict(pkg=dict(path=rel, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()), rows=rows, passed=ok), indent=2) + '\n')
for r in rows: print(r['check'], r['passed'])
sys.exit(0 if ok else 1)
