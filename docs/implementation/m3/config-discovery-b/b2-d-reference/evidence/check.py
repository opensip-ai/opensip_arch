"""B2-d0 checker (B2-d plan r3 section 1): the framework recognition reference against hand-written expectations and
against the unwrapped B-S9 model. Writes `checks.json` beside itself; exits nonzero on any failure.

  python3 -I -B check.py <architecture checkout> <python-packages snapshot> [<reference file> <output>]

The optional reference and output let `mutants.py` run this checker on a mutated copy without touching checks.json.

Groups:
  * recognizers: one positive case per recognizer, and its config-requires-evaluation or parse-failure case;
  * changes: each of the plan's five changes, its effect against the unwrapped model, and model equality elsewhere;
  * bounds: the FR-4 validator at the bound and one past it, called directly; the per-unit entry bound at 65,536
    and 65,537 split across results, with overlap, alone in one result, and under explicit overrides;
  * toml: parse_toml's profile at its byte and node bounds and one past, usable tables beside unrelated fields;
  * yaml: the closed subset's grammar table (every production accepted, every exclusion refused);
  * explicit: absent, explicit [] and explicit non-empty;
  * identity: the recognitionId preimage and the DISCOVERED provenance rendering.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = HERE.parent / 'reference' / 'framework_recognition_reference.py'


def load_ref(path=REF):
    spec = importlib.util.spec_from_file_location('framework_recognition_reference', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    arch, packages = Path(sys.argv[1]), Path(sys.argv[2])
    ref_path = Path(sys.argv[3]) if len(sys.argv) > 3 else REF
    output = Path(sys.argv[4]) if len(sys.argv) > 4 else HERE / 'checks.json'
    M = load_ref(ref_path)
    ref = M.load(arch, packages)
    model = ref.model
    rows, failures = [], []

    def check(group, name, ok, detail=None):
        rows.append(dict(group=group, name=name, passed=bool(ok), **({'detail': detail} if detail is not None else {})))
        if not ok:
            failures.append(group + '/' + name)

    def ids(rec):
        return [r['recognizerId'] for r in rec['recognized']]

    def by(rec, rid):
        return next(r for r in rec['recognized'] if r['recognizerId'] == rid)

    def unwrapped(files):
        return model.recognize_frameworks({p: b.decode('utf-8') for p, b in files.items()})

    def strip_hashes(rec):
        rec = copy.deepcopy(rec)
        for r in rec['recognized']:
            for e in r['evidence']:
                e.pop('contentSha256')
        return rec

    PKG = b'{"name": "a", "version": "1.0.0"}'
    # ------------------------------------------------------------------ recognizers
    r = ref.recognize({'package.json': PKG})
    check('recognizers', 'node-package-positive', ids(r) == ['node-package'] and by(r, 'node-package')['assurance'] == 'declared')
    r = ref.recognize({'package.json': b'{"name": '})
    check('recognizers', 'node-package-unparseable', by(r, 'node-package')['unresolvedChoices'] == ['package.json-not-strict-json'] and r['entryPoints'] == {'state': 'partial', 'source': 'recognized'})
    r = ref.recognize({'package.json': b'{"name": "a", "workspaces": ["p/*"]}'})
    check('recognizers', 'npm-workspaces-positive', ids(r) == ['node-package', 'npm-workspaces'])
    r = ref.recognize({'package.json': b'{"name": "a", "workspaces": "p/*"}'})
    check('recognizers', 'npm-workspaces-not-a-list', ids(r) == ['node-package'])
    r = ref.recognize({'package.json': b'{"jest": {}}'})
    check('recognizers', 'vitest-jest-positive', by(r, 'vitest-jest')['unresolvedChoices'] == [] and by(r, 'vitest-jest')['effects']['testGlobs'] == ['**/*.test.*', '**/*.spec.*', '**/__tests__/**'])
    r = ref.recognize({'package.json': PKG, 'vitest.config.ts': b'export default {}'})
    check('recognizers', 'vitest-jest-config-requires-evaluation', by(r, 'vitest-jest')['unresolvedChoices'] == ['config-requires-evaluation'] and r['entryPoints']['state'] == 'partial')
    r = ref.recognize({'tsconfig.json': b'{"compilerOptions": {}}'})
    check('recognizers', 'typescript-config-positive', by(r, 'typescript-config')['assurance'] == 'declared')
    r = ref.recognize({'tsconfig.json': b'{'})
    check('recognizers', 'typescript-config-not-jsonc', by(r, 'typescript-config')['unresolvedChoices'] == ['tsconfig-not-jsonc'] and by(r, 'typescript-config')['assurance'] == 'inferred')
    r = ref.recognize({'pnpm-workspace.yaml': b'packages:\n  - "packages/*"\n'})
    check('recognizers', 'pnpm-workspace-positive', by(r, 'pnpm-workspace')['unresolvedChoices'] == [])
    r = ref.recognize({'pnpm-workspace.yaml': b'packages:\n  - a\ncatalog:\n  x: 1\n'})
    check('recognizers', 'pnpm-workspace-config-requires-evaluation', by(r, 'pnpm-workspace')['unresolvedChoices'] == ['config-requires-evaluation'] and r['entryPoints']['state'] == 'partial')
    r = ref.recognize({'Cargo.toml': b'[package]\nname = "a"\n', 'src/main.rs': b'', 'src/lib.rs': b''})
    check('recognizers', 'cargo-package-positive', by(r, 'cargo-package')['effects']['entryPoints'] == ['src/main.rs', 'src/lib.rs'] and r['entryPoints'] == {'state': 'all', 'source': 'recognized'})
    r = ref.recognize({'Cargo.toml': b'[package\n'})
    check('recognizers', 'cargo-package-not-toml', ids(r) == ['cargo-package'] and by(r, 'cargo-package')['unresolvedChoices'] == ['Cargo.toml-not-toml'] and r['entryPoints']['state'] == 'partial')
    r = ref.recognize({'Cargo.toml': b'[workspace]\nmembers = ["a"]\n'})
    check('recognizers', 'cargo-workspace-positive', ids(r) == ['cargo-workspace'])
    r = ref.recognize({'next.config.js': b'module.exports = {}', 'pages/index.tsx': b'', 'app/a/page.tsx': b''})
    check('recognizers', 'nextjs-config-requires-evaluation', by(r, 'nextjs')['effects']['entryPoints'] == ['app/a/page.tsx', 'pages/index.tsx'] and by(r, 'nextjs')['unresolvedChoices'] == ['config-requires-evaluation'] and r['entryPoints']['state'] == 'partial')
    r = ref.recognize({'vite.config.ts': b'export default {}', 'index.html': b''})
    check('recognizers', 'vite-config-requires-evaluation', by(r, 'vite')['effects']['entryPoints'] == ['index.html'] and r['entryPoints']['state'] == 'partial')
    r = ref.recognize({'package.json': b'{"dependencies": {"svelte": "4", "react": "18"}, "devDependencies": {"astro": "4"}}'})
    check('recognizers', 'observed-hints', r['observedHints'] == [{'dependencyName': 'astro'}, {'dependencyName': 'svelte'}] and r['entryPoints']['state'] == 'none')
    # ------------------------------------------------------------------ changes against the unwrapped model
    same = [{'package.json': PKG}, {'package.json': b'{"jest": {}, "workspaces": ["x"]}'}, {'tsconfig.json': b'{}', 'jsconfig.json': b'{}'},
            {'next.config.mjs': b'x', 'pages/a.ts': b''}, {'vite.config.js': b'x', 'index.html': b''}, {'Cargo.toml': b'[package]\nname="a"\n', 'src/lib.rs': b''},
            {'Cargo.toml': b'[workspace]\n[package]\nname="a"\n', 'src/main.rs': b''}, {'pnpm-workspace.yaml': b'packages:\n  - a\n'}]
    for i, files in enumerate(same):
        a, b = strip_hashes(ref.recognize(files)), strip_hashes(unwrapped(files))
        check('changes', 'model-equal-%d' % i, a == b, None if a == b else dict(reference=a, model=b))
    files = {'Cargo.toml': b'[workspace.dependencies]\nserde = "1"\n'}
    check('changes', 'cargo-1-workspace-dependencies-alone', ids(ref.recognize(files)) == ['cargo-workspace'] and ids(unwrapped(files)) == [])
    files = {'Cargo.toml': b'x = """\n[workspace]\n"""\n[package]\nname = "a"\n'}
    check('changes', 'cargo-1-header-inside-a-string', ids(ref.recognize(files)) == ['cargo-package'] and ids(unwrapped(files)) == ['cargo-package', 'cargo-workspace'])
    files = {'Cargo.toml': b'[package]\nname = \n[workspace]\n'}
    check('changes', 'cargo-1-unparseable', by(ref.recognize(files), 'cargo-package')['unresolvedChoices'] == ['Cargo.toml-not-toml'] and ids(unwrapped(files)) == ['cargo-package', 'cargo-workspace'])
    files = {'tsconfig.json': b'{"compilerOptions": '}
    check('changes', 'tsconfig-2-not-jsonc', by(ref.recognize(files), 'typescript-config')['unresolvedChoices'] == ['tsconfig-not-jsonc'] and by(unwrapped(files), 'typescript-config')['unresolvedChoices'] == [])
    files = {'tsconfig.json': b'{"a": 1}' + b' ' * (64 * 1024)}
    check('changes', 'tsconfig-2-over-64-kib', by(ref.recognize(files), 'typescript-config')['unresolvedChoices'] == ['tsconfig-not-jsonc'])
    files = {'pnpm-workspace.yaml': b'packages:\n  - foo:\n'}
    check('changes', 'pnpm-3-outside', by(ref.recognize(files), 'pnpm-workspace')['unresolvedChoices'] == ['config-requires-evaluation'] and by(unwrapped(files), 'pnpm-workspace')['unresolvedChoices'] == [])
    files = {'vite.config.ts': b'x'}
    check('changes', 'state-5-config-without-entries', ref.recognize(files)['entryPoints']['state'] == 'partial' and unwrapped(files)['entryPoints']['state'] == 'none')
    files = {'next.config.js': b'x'}
    check('changes', 'state-5-next-without-routes', ref.recognize(files)['entryPoints']['state'] == 'partial' and unwrapped(files)['entryPoints']['state'] == 'none')
    files = {'pnpm-workspace.yaml': b'packages: x\n'}
    check('changes', 'state-5-outside-pnpm-alone', ref.recognize(files)['entryPoints']['state'] == 'partial')
    files = {'Cargo.toml': b'[package]\nname = "a"\n', 'src/main.rs': b'', 'vitest.config.ts': b'x', 'package.json': PKG}
    check('changes', 'state-5-mixed', ref.recognize(files)['entryPoints']['state'] == 'partial' and unwrapped(files)['entryPoints']['state'] == 'partial')
    files = {'package.json': b'\xff\xfe'}
    check('changes', 'bytes-non-utf8-package-json', by(ref.recognize(files), 'node-package')['unresolvedChoices'] == ['package.json-not-strict-json']
          and by(ref.recognize(files), 'node-package')['evidence'][0]['contentSha256'] == hashlib.sha256(b'\xff\xfe').hexdigest())
    # ------------------------------------------------------------------ bounds
    def result(rid, evidence=1, entries=()):
        return {'recognizerId': rid, 'recognizerVersion': 1, 'evidence': [{'path': 'p%d' % i, 'contentSha256': '0' * 64, 'field': 'f'} for i in range(evidence)],
                'assurance': 'declared', 'effects': {'entryPoints': list(entries), 'testGlobs': [], 'ignoreConventions': []}, 'unresolvedChoices': []}

    def raises(fn):
        try:
            fn()
        except ValueError:
            return True
        return False
    check('bounds', 'recognizers-at-32', not raises(lambda: M.bound_check([result('node-package')] * 32)))
    check('bounds', 'recognizers-at-33', raises(lambda: M.bound_check([result('node-package')] * 33)))
    check('bounds', 'evidence-at-64', not raises(lambda: M.bound_check([result('vite', 64)])))
    check('bounds', 'evidence-at-65', raises(lambda: M.bound_check([result('vite', 65)])))
    check('bounds', 'evidence-at-0', raises(lambda: M.bound_check([result('vite', 0)])))
    for name, split, expect_over in (('union-65536-split', (65535, 1), False), ('union-65537-split', (65536, 1), True)):
        rs = [result('nextjs', entries=['r%d' % i for i in range(split[0])]), result('vite', entries=['index.html'] * split[1])]
        M.entry_bound(rs)
        check('bounds', name, all((r['effects']['entryPoints'] == []) == expect_over for r in rs) and all((M.ENTRY_POINTS_OVER_BOUND in r['unresolvedChoices']) == expect_over for r in rs))
    rs = [result('nextjs', entries=['r%d' % i for i in range(65536)]), result('cargo-package', entries=['r0', 'r1'])]
    M.entry_bound(rs)
    check('bounds', 'union-overlap-65536-distinct', all(r['effects']['entryPoints'] for r in rs))
    routes = {'next.config.js': b'x', 'index.html': b'', 'vite.config.ts': b'x'}
    routes.update({'pages/r%05d.tsx' % i: b'' for i in range(65536)})
    for label, explicit in (('none', None), ('explicit-empty', []), ('explicit-nonempty', ['src/main.ts'])):
        rec = ref.recognize(routes, explicit)
        over = all(r['effects']['entryPoints'] == [] for r in rec['recognized']) and M.ENTRY_POINTS_OVER_BOUND in by(rec, 'nextjs')['unresolvedChoices'] and M.ENTRY_POINTS_OVER_BOUND in by(rec, 'vite')['unresolvedChoices']
        expected = {'state': 'partial', 'source': 'recognized'} if explicit is None else {'state': 'all', 'source': 'explicit'}
        check('bounds', 'unit-65537-across-results-' + label, over and rec['entryPoints'] == expected)
    alone = {'next.config.js': b'x'}
    alone.update({'pages/r%05d.tsx' % i: b'' for i in range(65537)})
    for label, explicit in (('none', None), ('explicit-empty', [])):
        rec = ref.recognize(alone, explicit)
        check('bounds', 'one-result-65537-' + label, by(rec, 'nextjs')['effects']['entryPoints'] == [] and M.ENTRY_POINTS_OVER_BOUND in by(rec, 'nextjs')['unresolvedChoices'])
    at = {'next.config.js': b'x'}
    at.update({'pages/r%05d.tsx' % i: b'' for i in range(65536)})
    check('bounds', 'one-result-65536', len(by(ref.recognize(at), 'nextjs')['effects']['entryPoints']) == 65536)
    # ------------------------------------------------------------------ toml profile
    pkg = b'[package]\nname = "a"\n'
    pad = lambda n: pkg + b'#' * (n - len(pkg) - 1) + b'\n'
    check('toml', 'bytes-at-4-mib', ref.parse_cargo(pad(M.TOML_MAX_BYTES)) is not None)
    check('toml', 'bytes-past-4-mib', ref.parse_cargo(pad(M.TOML_MAX_BYTES + 1)) is None and by(ref.recognize({'Cargo.toml': pad(M.TOML_MAX_BYTES + 1)}), 'cargo-package')['unresolvedChoices'] == ['Cargo.toml-not-toml'])
    # package (1) + name (1) + x (1) + k elements: the walk's count.
    nodes = lambda k: pkg + b'x = [' + b'0,' * k + b']\n'
    check('toml', 'nodes-at-1000000', ref.parse_cargo(nodes(M.TOML_MAX_NODES - 3)) is not None)
    check('toml', 'nodes-past-1000000', ref.parse_cargo(nodes(M.TOML_MAX_NODES - 2)) is None)
    check('toml', 'usable-table-beside-deep-field', ids(ref.recognize({'Cargo.toml': pkg + b'deep = ' + b'[' * 40 + b']' * 40 + b'\n'})) == ['cargo-package'])
    check('toml', 'usable-table-beside-wide-field', ids(ref.recognize({'Cargo.toml': pkg + b'wide = {' + b','.join(b'k%d = 1' % i for i in range(5000)) + b'}\n'})) == ['cargo-package'])
    # r2 (B2D0REF-R1-RF-3): long decimal integers beside usable tables, below and above Python's 4300-digit limit.
    for digits in (4300, 4301, 100000):
        doc = pkg + b'x = ' + b'9' * digits + b'\n'
        rec = ref.recognize({'Cargo.toml': doc, 'src/main.rs': b''})
        check('toml', 'decimal-%d-digits-package' % digits, by(rec, 'cargo-package')['effects']['entryPoints'] == ['src/main.rs'] and rec['entryPoints'] == {'state': 'all', 'source': 'recognized'})
        check('toml', 'decimal-%d-digits-workspace-fact' % digits, ref.cargo_workspace_fact(b'[workspace]\nx = ' + b'9' * digits + b'\n') is True)
    check('toml', 'python-digit-limit-restored', sys.get_int_max_str_digits() == 4300)
    check('toml', 'bom-refused', ref.parse_cargo(b'\xef\xbb\xbf' + pkg) is None)
    check('toml', 'workspace-fact', [ref.cargo_workspace_fact(b'[workspace]\n'), ref.cargo_workspace_fact(pkg), ref.cargo_workspace_fact(b'[')] == [True, False, None])
    # ------------------------------------------------------------------ yaml subset
    accepted = [
        ('block-plain', b'packages:\n  - packages/*\n  - apps/*\n', ['packages/*', 'apps/*']),
        ('single-quoted-with-escape', b"packages:\n  - 'it''s/*'\n", ["it's/*"]),
        ('double-quoted-with-escapes', b'packages:\n  - "a\\"b\\\\c"\n', ['a"b\\c']),
        ('quoted-colon-and-hash', b'packages:\n  - "a:b#c"\n  - \'d: e\'\n', ['a:b#c', 'd: e']),
        ('quoted-negation', b'packages:\n  - "!**/test/**"\n', ['!**/test/**']),
        ('comments-and-blank-lines', b'# head\n\npackages: # key\n  # inside\n  - a # tail\n\n', ['a']),
        ('crlf', b'packages:\r\n  - a\r\n', ['a']),
        ('empty-flow', b'packages: []\n', []),
        ('empty-flow-with-comment', b'packages: [] # none\n', []),
        ('no-final-newline', b'packages:\n  - a', ['a']),
        ('crlf-no-final-newline', b'packages:\r\n  - a', ['a']),
        ('wider-indent', b'packages:\n    - a\n    - b\n', ['a', 'b']),
        ('plain-hash-inside', b'packages:\n  - a#b\n', ['a#b']),
        ('plain-trailing-spaces', b'packages:\n  - a  \n', ['a']),
    ]
    for name, raw, expect in accepted:
        try:
            got = M.parse_pnpm_packages(raw)
        except M.OutsideSubset as e:
            got = 'outside: %s' % e
        check('yaml', 'accept-' + name, got == expect, got if got != expect else None)
    refused = [
        ('terminal-colon', b'packages:\n  - foo:\n'), ('colon-space', b'packages:\n  - foo: bar\n'), ('colon-tab', b'packages:\n  - foo:\tbar\n'),
        ('dash-without-separation', b'packages:\n  -foo\n'), ('bare-dash', b'packages:\n  -\n'), ('zero-indent', b'packages:\n- a\n'),
        ('inconsistent-indent', b'packages:\n  - a\n    - b\n'), ('other-key-before', b'catalog:\n  a: 1\npackages:\n  - a\n'),
        ('other-key-after', b'packages:\n  - a\ncatalog:\n  a: 1\n'), ('flow-sequence', b'packages: [a, b]\n'), ('document-marker', b'---\npackages:\n  - a\n'),
        ('anchor', b'packages:\n  - &x a\n'), ('alias', b'packages:\n  - *x\n'), ('tag', b'packages:\n  - !x a\n'), ('block-scalar', b'packages:\n  - |\n    a\n'),
        ('nested-sequence', b'packages:\n  - - a\n'), ('tab-indent', b'packages:\n\t- a\n'), ('bom', b'\xef\xbb\xbfpackages:\n  - a\n'),
        ('not-utf8', b'packages:\n  - \xff\n'), ('integer', b'packages:\n  - 123\n'), ('float', b'packages:\n  - 1.5\n'), ('boolean-yes', b'packages:\n  - yes\n'),
        ('null-tilde', b'packages:\n  - ~\n'), ('date', b'packages:\n  - 2024-01-02\n'), ('unterminated-single', b"packages:\n  - 'a\n"),
        ('unterminated-double', b'packages:\n  - "a\n'), ('bad-escape', b'packages:\n  - "a\\n"\n'), ('text-after-quote', b'packages:\n  - "a" b\n'),
        ('no-key', b'# only\n'), ('key-twice', b'packages:\n  - a\npackages:\n  - b\n'), ('content-after-empty-flow', b'packages: []\n  - a\n'),
        ('bare-cr', b'packages:\n  - a\rb\n'), ('over-64-kib', b'packages:\n  - a\n' + b'#' * (64 * 1024) + b'\n'),
        # r2 (B2D0REF-R1-RF-1): a null packages value.
        ('bare-key', b'packages:\n'), ('comments-only-value', b'packages:\n  # none yet\n\n'),
        # r2 (B2D0REF-R1-RF-2): characters outside the subset, in scalars and in comments.
        ('nul-plain', b'packages:\n  - a\x00b\n'), ('nul-single', b"packages:\n  - 'a\x00b'\n"), ('nul-double', b'packages:\n  - "a\x00b"\n'),
        ('nul-comment', b'packages:\n  - a # x\x00\n'), ('del-plain', b'packages:\n  - a\x7fb\n'), ('c1-control', 'packages:\n  - "a\u0090b"\n'.encode()),
        ('nel', 'packages:\n  - "a\u0085b"\n'.encode()), ('line-separator', 'packages:\n  - "a\u2028b"\n'.encode()),
        ('paragraph-separator', 'packages:\n  - a\u2029\n'.encode()), ('bom-inside', 'packages:\n  - "a\ufeffb"\n'.encode()),
        # r3 (B2D0REF-R2-RF-1): an unseparated empty flow sequence is a plain scalar.
        ('unseparated-empty-flow', b'packages:[]\n'), ('unseparated-empty-flow-with-comment', b'packages:[] # none\n'),
        # r3 (B2D0REF-R2-RF-2): a bare CR at the end of input.
        ('eof-cr-block-item', b'packages:\n  - a\r'), ('eof-cr-empty-flow', b'packages: []\r'), ('eof-cr-comment', b'packages:\n  - a # c\r'),
    ]
    for name, raw in refused:
        try:
            got = M.parse_pnpm_packages(raw)
            ok = False
        except M.OutsideSubset:
            got, ok = None, True
        check('yaml', 'refuse-' + name, ok, got)
    check('yaml', 'accept-unicode-scalars', M.parse_pnpm_packages('packages:\n  - "caf\u00e9/*"\n  - \u30a2\u30d7\u30ea/*\n  - "\U0001f600"\n'.encode()) == ['caf\u00e9/*', '\u30a2\u30d7\u30ea/*', '\U0001f600'])
    for name, raw in (('bare-key', b'packages:\n'), ('nul-double', b'packages:\n  - "a\x00b"\n'), ('unseparated-empty-flow', b'packages:[]\n'),
                      ('unseparated-empty-flow-with-comment', b'packages:[] # none\n'), ('eof-cr-block-item', b'packages:\n  - a\r'), ('eof-cr-empty-flow', b'packages: []\r')):
        rec = ref.recognize({'pnpm-workspace.yaml': raw})
        check('yaml', 'recognition-discloses-' + name, by(rec, 'pnpm-workspace')['unresolvedChoices'] == ['config-requires-evaluation'] and rec['entryPoints'] == {'state': 'partial', 'source': 'recognized'})
    check('yaml', 'at-64-kib', M.parse_pnpm_packages(b'packages:\n  - a\n' + b'#' * (64 * 1024 - 17) + b'\n') == ['a'])
    # ------------------------------------------------------------------ explicit
    base = {'Cargo.toml': pkg, 'src/main.rs': b''}
    check('explicit', 'absent', ref.recognize(base, None)['entryPoints'] == {'state': 'all', 'source': 'recognized'})
    check('explicit', 'explicit-empty', ref.recognize(base, [])['entryPoints'] == {'state': 'all', 'source': 'explicit'})
    check('explicit', 'explicit-nonempty', ref.recognize(base, ['src/main.rs'])['entryPoints'] == {'state': 'all', 'source': 'explicit'})
    check('explicit', 'recognized-results-kept', by(ref.recognize(base, []), 'cargo-package')['effects']['entryPoints'] == ['src/main.rs'])
    # ------------------------------------------------------------------ identity
    rec = ref.recognize(base)
    row = ref.unit_recognition(0, '', 'Cargo.toml', rec)
    canonical = json.dumps(rec, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    preimage = b'opensip.product.v1\0native.framework-recognition.v1\0' + len(canonical).to_bytes(8, 'big') + canonical
    check('identity', 'recognition-id-preimage', row['recognitionId'] == 'sha256:' + hashlib.sha256(preimage).hexdigest())
    bumped = copy.deepcopy(rec)
    bumped['recognized'][0]['recognizerVersion'] = 2
    check('identity', 'version-bump-changes-recognition-id', ref.model.C.identity(M.DOMAIN, bumped) != ref.model.C.identity(M.DOMAIN, rec))
    check('identity', 'discovered-provenance', M.discovered_provenance(by(rec, 'cargo-package')) == 'DISCOVERED:cargo-package@1')
    out = dict(schemaVersion=1, standing='PROPOSED B2-d0 checker output (B2-d plan r3 section 1); design evidence only',
               reference=dict(path=str(REF.relative_to(arch.resolve())) if REF.is_relative_to(arch.resolve()) else REF.name,
                              sha256=hashlib.sha256(REF.read_bytes()).hexdigest()),
               groups=sorted({r['group'] for r in rows}), total=len(rows), failed=failures, rows=rows)
    output.write_text(json.dumps(out, indent=1) + '\n')
    print('%d checks, %d failed' % (len(rows), len(failures)))
    for f in failures:
        print('FAILED', f)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
