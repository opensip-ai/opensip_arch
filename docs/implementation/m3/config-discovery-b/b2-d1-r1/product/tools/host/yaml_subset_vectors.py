"""Cross-implementation vectors for the closed YAML subset of `pnpm-workspace.yaml` (M3-B r9 item 16; unit B2-d1, B2-d
plan r3 section 2).

Developer tool only. It writes or checks crates/host/src/yaml_subset_vectors.json, which the host's
`yaml_subset_tests.rs` replays against `yaml_subset.rs`.

  * **The grammar table.** Each case is a document and its result written here by hand from the plan: the package
    globs, or outside the subset. Every production is accepted at least once and every exclusion refused at least
    once.
  * **The oracle.** The bound B2-d0 reference (contract successor 171), whose `parse_pnpm_packages` is the YAML
    reading, pinned by bytes. It must give every hand-written result, or generation fails.
  * **The substitution sweep.** For three seed documents, every single-byte substitution from a fixed alphabet of
    structural, quoting, control and non-ASCII bytes; the expected result of each is the reference's. The Rust must
    agree on every one.

No network, process or repository write except the output with --write.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/host/src/yaml_subset_vectors.json'
# The bound B2-d0 reference (contract successor 171): path, bytes, SHA-256.
REFERENCE = ('docs/implementation/m3/config-discovery-b/b2-d-reference/reference/framework_recognition_reference.py', 19933,
             'ed9858b0de1035ac95cde38743066a2e7a6df1740c3a30523021c715255b6a89')
OUT = None  # "outside the subset"

ACCEPTED = [
    ('block-plain', b'packages:\n  - packages/*\n  - apps/*\n', ['packages/*', 'apps/*']),
    ('single-quoted-with-escape', b"packages:\n  - 'it''s/*'\n", ["it's/*"]),
    ('double-quoted-with-escapes', b'packages:\n  - "a\\"b\\\\c"\n', ['a"b\\c']),
    ('quoted-colon-and-hash', b'packages:\n  - "a:b#c"\n  - \'d: e\'\n', ['a:b#c', 'd: e']),
    ('quoted-negation', b'packages:\n  - "!**/test/**"\n', ['!**/test/**']),
    ('quoted-empty', b'packages:\n  - ""\n  - \'\'\n', ['', '']),
    ('quoted-reserved', b'packages:\n  - "yes"\n  - \'123\'\n', ['yes', '123']),
    ('comments-and-blank-lines', b'# head\n\npackages: # key\n  # inside\n  - a # tail\n\n', ['a']),
    ('comment-at-column-0-between-items', b'packages:\n  - a\n# between\n  - b\n', ['a', 'b']),
    ('crlf', b'packages:\r\n  - a\r\n', ['a']),
    ('no-final-newline', b'packages:\n  - a', ['a']),
    ('crlf-no-final-newline', b'packages:\r\n  - a', ['a']),
    ('empty-flow', b'packages: []\n', []),
    ('empty-flow-with-comment', b'packages: [] # none\n', []),
    ('empty-flow-trailing-spaces', b'packages: []   \n', []),
    ('wider-indent', b'packages:\n    - a\n    - b\n', ['a', 'b']),
    ('several-spaces-after-dash', b'packages:\n  -   a\n', ['a']),
    ('plain-hash-inside', b'packages:\n  - a#b\n', ['a#b']),
    ('plain-trailing-spaces', b'packages:\n  - a  \n', ['a']),
    ('plain-flow-characters-inside', b'packages:\n  - a[b]{c},d\n', ['a[b]{c},d']),
    ('plain-sign-not-numeric', b'packages:\n  - +\n  - +x\n', ['+', '+x']),
    ('plain-near-numeric', b'packages:\n  - 2024-app\n  - 1.2.x/y\n', ['2024-app', '1.2.x/y']),
    ('plain-near-date', b'packages:\n  - 2024-01-02z\n  - 202-01-02/x\n', ['2024-01-02z', '202-01-02/x']),
    ('unicode-scalars', 'packages:\n  - "café/*"\n  - アプリ/*\n  - "\U0001f600"\n  -  a\n'.encode(),
     ['café/*', 'アプリ/*', '\U0001f600', ' a']),
]
REFUSED = [
    ('terminal-colon', b'packages:\n  - foo:\n'), ('colon-space', b'packages:\n  - foo: bar\n'), ('colon-inside', b'packages:\n  - a:b\n'),
    ('colon-tab', b'packages:\n  - foo:\tbar\n'), ('dash-without-separation', b'packages:\n  -foo\n'), ('bare-dash', b'packages:\n  -\n'),
    ('dash-then-spaces-only', b'packages:\n  -   \n'), ('zero-indent', b'packages:\n- a\n'), ('inconsistent-indent', b'packages:\n  - a\n    - b\n'),
    ('continuation-line', b'packages:\n  - a\n    b\n'), ('other-key-before', b'catalog:\n  a: 1\npackages:\n  - a\n'),
    ('other-key-after', b'packages:\n  - a\ncatalog:\n  a: 1\n'), ('quoted-key', b'"packages":\n  - a\n'), ('indented-key', b'  packages:\n  - a\n'),
    ('key-trailing-space', b'packages: \n  - a\n'), ('key-hash-without-space', b'packages:#x\n  - a\n'), ('flow-sequence', b'packages: [a, b]\n'),
    ('document-marker', b'---\npackages:\n  - a\n'), ('document-end', b'packages:\n  - a\n...\n'), ('anchor', b'packages:\n  - &x a\n'),
    ('alias', b'packages:\n  - *x\n'), ('tag', b'packages:\n  - !x a\n'), ('block-scalar', b'packages:\n  - |\n    a\n'),
    ('folded-scalar', b'packages:\n  - >\n    a\n'), ('nested-sequence', b'packages:\n  - - a\n'), ('mapping-item', b'packages:\n  - ? a\n'),
    ('directive', b'%YAML 1.2\npackages:\n  - a\n'), ('tab-indent', b'packages:\n\t- a\n'), ('tab-in-quotes', b'packages:\n  - "a\tb"\n'),
    ('bom', b'\xef\xbb\xbfpackages:\n  - a\n'), ('not-utf8', b'packages:\n  - \xff\n'), ('integer', b'packages:\n  - 123\n'),
    ('signed-integer', b'packages:\n  - +7\n'), ('hex', b'packages:\n  - 0x1F\n'), ('octal', b'packages:\n  - 0o17\n'),
    ('underscored', b'packages:\n  - 1_000\n'), ('float', b'packages:\n  - 1.5\n'), ('leading-dot-float', b'packages:\n  - .5\n'),
    ('exponent', b'packages:\n  - 1e3\n'), ('infinity', b'packages:\n  - .Inf\n'), ('nan', b'packages:\n  - .NaN\n'),
    ('boolean-yes', b'packages:\n  - yes\n'), ('boolean-true-mixed-case', b'packages:\n  - True\n'), ('boolean-off', b'packages:\n  - OFF\n'),
    ('boolean-y', b'packages:\n  - y\n'), ('null-word', b'packages:\n  - Null\n'), ('null-tilde', b'packages:\n  - ~\n'), ('date', b'packages:\n  - 2024-01-02\n'),
    ('datetime', b'packages:\n  - 2024-1-2 10\n'), ('digit-led-run', b'packages:\n  - 2024-01-02x\n'), ('unterminated-single', b"packages:\n  - 'a\n"), ('unterminated-double', b'packages:\n  - "a\n'),
    ('bad-escape', b'packages:\n  - "a\\n"\n'), ('trailing-backslash', b'packages:\n  - "a\\\n'), ('text-after-quote', b'packages:\n  - "a" b\n'),
    ('hash-after-quote-without-space', b'packages:\n  - "a"#b\n'), ('no-key', b'# only\n'), ('empty-document', b''),
    ('key-twice', b'packages:\n  - a\npackages:\n  - b\n'), ('content-after-empty-flow', b'packages: []\n  - a\n'), ('bare-cr', b'packages:\n  - a\rb\n'),
    ('bare-key', b'packages:\n'), ('comments-only-value', b'packages:\n  # none yet\n\n'), ('nul-plain', b'packages:\n  - a\x00b\n'),
    ('nul-single', b"packages:\n  - 'a\x00b'\n"), ('nul-double', b'packages:\n  - "a\x00b"\n'), ('nul-comment', b'packages:\n  - a # x\x00\n'),
    ('del-plain', b'packages:\n  - a\x7fb\n'), ('c1-control', 'packages:\n  - "a\u0090b"\n'.encode()), ('nel', 'packages:\n  - "a\u0085b"\n'.encode()),
    ('line-separator', 'packages:\n  - "a b"\n'.encode()), ('paragraph-separator', 'packages:\n  - a \n'.encode()),
    ('bom-inside', 'packages:\n  - "a﻿b"\n'.encode()), ('unseparated-empty-flow', b'packages:[]\n'),
    ('unseparated-empty-flow-with-comment', b'packages:[] # none\n'), ('empty-flow-hash-without-space', b'packages: []#x\n'),
    ('eof-cr-block-item', b'packages:\n  - a\r'), ('eof-cr-empty-flow', b'packages: []\r'), ('eof-cr-comment', b'packages:\n  - a # c\r'),
]
BOUND = 64 * 1024
SEEDS = [b'packages:\n  - packages/*\n', b"packages:\n  - 'a''b'\n  - \"c\\\\d\" # x\n", b'packages: [] # e\n']
ALPHABET = [b' ', b':', b'#', b"'", b'"', b'-', b'\\', b'[', b']', b'\t', b'\r', b'\n', b'\x00', b'\x7f', b'a', b'1', b'~', b'\xc3', b'\xff']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reference(arch):
    path = arch / REFERENCE[0]
    raw = path.read_bytes()
    require(len(raw) == REFERENCE[1] and hashlib.sha256(raw).hexdigest() == REFERENCE[2], 'reference pin mismatch: ' + REFERENCE[0])
    spec = importlib.util.spec_from_file_location('framework_recognition_reference', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def vectors(arch):
    ref = reference(arch)

    def run(raw):
        try:
            return ref.parse_pnpm_packages(raw)
        except ref.OutsideSubset:
            return OUT
    cases = []

    def case(kind, name, raw, expected):
        got = run(raw)
        require(got == expected, '%s %s: the reference gives %r, not %r' % (kind, name, got, expected))
        cases.append(dict(kind=kind, name=name, hex=raw.hex(), packages=expected))
    for name, raw, expected in ACCEPTED:
        case('grammar', 'accept-' + name, raw, expected)
    for name, raw in REFUSED:
        case('grammar', 'refuse-' + name, raw, OUT)
    at = b'packages:\n  - a\n'
    case('bound', 'at-64-kib', at + b'#' * (BOUND - len(at) - 1) + b'\n', ['a'])
    case('bound', 'past-64-kib', at + b'#' * (BOUND - len(at)) + b'\n', OUT)
    for s, seed in enumerate(SEEDS):
        for i in range(len(seed)):
            for byte in ALPHABET:
                if seed[i:i + 1] == byte:
                    continue
                raw = seed[:i] + byte + seed[i + 1:]
                cases.append(dict(kind='sweep', name='seed%d-at%d-%s' % (s, i, byte.hex()), hex=raw.hex(), packages=run(raw)))
    body = {'schemaVersion': 1,
            'standing': 'The closed YAML subset vectors (M3-B r9 item 16; B2-d plan r3 section 2; unit B2-d1). Generated by '
                        'tools/host/yaml_subset_vectors.py from the hand-written grammar table, checked against the bound B2-d0 '
                        'reference (contract successor 171), and a single-byte substitution sweep whose results are the '
                        "reference's. `packages: null` means outside the subset. Design evidence, not product qualification.",
            'reference': dict(path=REFERENCE[0], bytes=REFERENCE[1], sha256=REFERENCE[2]),
            'maxBytes': BOUND,
            'cases': cases}
    return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout holding the reference')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raw = vectors(args.architecture.resolve(strict=True))
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the grammar table and the B2-d0 reference.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'YAML subset vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
