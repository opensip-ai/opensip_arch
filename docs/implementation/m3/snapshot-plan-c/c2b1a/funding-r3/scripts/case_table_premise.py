#!/usr/bin/env python3
"""The generated Unicode case table's price-relevant premises (RF-2; r2 adds the range-order checks, REVIEW-r1 NBO-3), read at the pin: the table version,
the three populations the fold searches, and the largest expansion of one input scalar.
The drift control C2b-1a carries recomputes exactly these from the same file."""
import re, subprocess, sys, hashlib, json

PIN = '98159381648b0ddad022f1c7fffe678ce0e27208'
PRODUCT = sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip'
PATH = 'crates/evaluator/src/generated/unicode_case_tables.rs'
raw = subprocess.run(['git', '-C', PRODUCT, 'show', f'{PIN}:{PATH}'], capture_output=True, check=True).stdout
text = raw.decode()


def block(name):
    return re.search(rf'pub\(super\) const {name}: &\[[^\]]*\] = &\[(.*?)\n\];', text, re.S).group(1)


version = tuple(int(x) for x in re.search(r'VERSION: \(u8, u8, u8\) = \((\d+), (\d+), (\d+)\);', text).groups())
lower = [(int(c, 16), json.loads('"' + s + '"'.replace('\\u{', '\\u{')) if False else s)
         for c, s in re.findall(r'\(0x([0-9a-f]+), "((?:[^"\\]|\\.)*)"\)', block('LOWER'))]


def rust_unescape(s):
    return re.sub(r'\\u\{([0-9a-fA-F]+)\}', lambda m: chr(int(m.group(1), 16)), s)


rows = [(code, rust_unescape(s)) for code, s in lower]
cased = re.findall(r'\(0x([0-9a-f]+),\s*0x([0-9a-f]+)\)', block('CASED'))
ignorable = re.findall(r'\(0x([0-9a-f]+),\s*0x([0-9a-f]+)\)', block('CASE_IGNORABLE'))
expansion = max(len(out.encode()) for _, out in rows)
ratio = max(len(out.encode()) / len(chr(code).encode()) for code, out in rows)
worst = max(rows, key=lambda r: len(r[1].encode()) / len(chr(r[0]).encode()))
sigma = len('\u03c2'.encode())
assert all(rows[i][0] < rows[i + 1][0] for i in range(len(rows) - 1))


def ranges_ordered(rs):
    """partition_point (unicode_case.rs:11-15) needs sorted, non-overlapping, well-formed ranges."""
    rs = [(int(x, 16), int(y, 16)) for x, y in rs]
    return all(lo <= hi for lo, hi in rs) and all(rs[i][1] < rs[i + 1][0] for i in range(len(rs) - 1))


assert ranges_ordered(cased) and ranges_ordered(ignorable)
result = {
    'path': PATH, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'version': version,
    'LOWER': len(rows), 'CASED': len(cased), 'CASE_IGNORABLE': len(ignorable),
    'maxOutputBytesPerScalar': max(expansion, sigma),
    'maxExpansionRatioNumerator': max(len(out.encode()) * 1 for _, out in rows),
    'worstRatio': [hex(worst[0]), len(chr(worst[0]).encode()), len(worst[1].encode()), ratio],
    'ordered': {'LOWER': True, 'CASED': ranges_ordered(cased), 'CASE_IGNORABLE': ranges_ordered(ignorable)},
    'searchComparisons': {k: (n.bit_length() + 1) for k, n in
                          (('LOWER', len(rows)), ('CASED', len(cased)), ('CASE_IGNORABLE', len(ignorable)))},
}
print(json.dumps(result, indent=1))
