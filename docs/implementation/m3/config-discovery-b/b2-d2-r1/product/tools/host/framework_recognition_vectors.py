"""Cross-implementation vectors for host-side framework recognition (M3-B r9 item 16; unit B2-d2, B2-d plan r3 sections 3
and 4).

Developer tool only. It writes or checks crates/host/src/framework_recognition_vectors.json, which the host's
`framework_recognition_tests.rs` replays against `framework_recognition.rs`.

  * **The oracle.** The bound B2-d0 reference (contract successor 171), pinned by bytes, loaded with the selected
    native model (contract successor 81) and its closure: `recognize`, `unit_recognition`, `cargo_workspace_fact` and
    `discovered_provenance`. Every expected result is the reference's.
  * **The unit cases.** Each is a unit's files (paths and bytes, unit-root-relative) and its explicit entry points
    (absent, `[]` or a list); the expected `FrameworkRecognitionV1` and the `UnitRecognitionV1` row (its
    `recognitionId`) for a given ordinal, root and marker. They cover every recognizer, its configuration-requiring
    or parse-failure case, the parsers' edges (exact JSON admission, JSONC within 64 KiB, the YAML subset, the TOML
    profile with inline tables, long integers and a byte order mark), observed hints, route selection and the
    explicit override.
  * **The bound cases.** Units of 65,536 and 65,537 Next.js routes (with and without a Vite `index.html`), each with no
    override, explicit `[]` and an explicit list: described by parameters, with the expected `recognitionId`, entry
    state and the results' unresolved choices, since the trees are large.
  * **The Cargo-workspace fact** and **the provenance rendering**.

No network, process or repository write except the output with --write.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/host/src/framework_recognition_vectors.json'
# The bound B2-d0 reference (contract successor 171): path, bytes, SHA-256.
REFERENCE = ('docs/implementation/m3/config-discovery-b/b2-d-reference/reference/framework_recognition_reference.py', 19933,
             'ed9858b0de1035ac95cde38743066a2e7a6df1740c3a30523021c715255b6a89')
PKG = b'{"name": "a", "version": "1.0.0"}'
CARGO = b'[package]\nname = "a"\n'
ABSENT = 'absent'

# (name, files, explicit, (ordinal, root, marker))
UNITS = [
    ('node-package', {'package.json': PKG}, ABSENT, (0, '', 'package.json')),
    ('node-package-unparseable', {'package.json': b'{"name": '}, ABSENT, (0, '', 'package.json')),
    ('node-package-not-utf8', {'package.json': b'\xff\xfe'}, ABSENT, (0, '', 'package.json')),
    ('node-package-array', {'package.json': b'[1, 2]'}, ABSENT, (0, '', 'package.json')),
    ('node-package-float', {'package.json': b'{"version": 1.5}'}, ABSENT, (0, '', 'package.json')),
    ('node-package-duplicate-key', {'package.json': b'{"a": 1, "a": 2}'}, ABSENT, (0, '', 'package.json')),
    ('npm-workspaces-list', {'package.json': b'{"workspaces": ["p/*"]}'}, ABSENT, (0, '', 'package.json')),
    ('npm-workspaces-object', {'package.json': b'{"workspaces": {"packages": ["p/*"]}}'}, ABSENT, (0, '', 'package.json')),
    ('npm-workspaces-string', {'package.json': b'{"workspaces": "p/*"}'}, ABSENT, (0, '', 'package.json')),
    ('vitest-jest-key', {'package.json': b'{"jest": {"testMatch": ["x"]}}'}, ABSENT, (0, '', 'package.json')),
    ('vitest-jest-config', {'package.json': PKG, 'vitest.config.ts': b'export default {}'}, ABSENT, (0, '', 'package.json')),
    ('vitest-jest-config-order', {'package.json': b'{"jest": {}}', 'vitest.config.js': b'x', 'jest.config.js': b'y'}, ABSENT, (0, '', 'package.json')),
    ('vitest-jest-config-without-package', {'vitest.config.ts': b'x', 'tsconfig.json': b'{}'}, ABSENT, (0, '', 'tsconfig.json')),
    ('hints', {'package.json': b'{"dependencies": {"svelte": "4", "react": "18"}, "devDependencies": {"astro": "4", "svelte": "4"}, "peerDependencies": {"@nestjs/core": "1"}, "optionalDependencies": {"vue": "3"}}'}, ABSENT, (0, '', 'package.json')),
    ('hints-not-objects', {'package.json': b'{"dependencies": ["vue"], "devDependencies": "astro"}'}, ABSENT, (0, '', 'package.json')),
    ('typescript-config', {'tsconfig.json': b'{"compilerOptions": {}}'}, ABSENT, (0, '', 'tsconfig.json')),
    ('typescript-config-jsconfig', {'jsconfig.json': b'{}'}, ABSENT, (0, '', 'jsconfig.json')),
    ('typescript-config-both', {'tsconfig.json': b'{', 'jsconfig.json': b'{}'}, ABSENT, (0, '', 'tsconfig.json')),
    ('typescript-config-comments', {'tsconfig.json': b'// c\n{ /* x */ "a": [1,], }'}, ABSENT, (0, '', 'tsconfig.json')),
    ('typescript-config-empty', {'tsconfig.json': b''}, ABSENT, (0, '', 'tsconfig.json')),
    ('typescript-config-not-jsonc', {'tsconfig.json': b'{"compilerOptions": '}, ABSENT, (0, '', 'tsconfig.json')),
    ('typescript-config-at-64-kib', {'tsconfig.json': b'{}' + b' ' * (64 * 1024 - 2)}, ABSENT, (0, '', 'tsconfig.json')),
    ('typescript-config-past-64-kib', {'tsconfig.json': b'{}' + b' ' * (64 * 1024 - 1)}, ABSENT, (0, '', 'tsconfig.json')),
    ('pnpm-workspace', {'pnpm-workspace.yaml': b'packages:\n  - "packages/*"\n'}, ABSENT, (0, '', 'package.json')),
    ('pnpm-workspace-outside', {'pnpm-workspace.yaml': b'packages:\n  - a\ncatalog:\n  x: 1\n'}, ABSENT, (0, '', 'package.json')),
    ('pnpm-workspace-null', {'pnpm-workspace.yaml': b'packages:\n'}, ABSENT, (0, '', 'package.json')),
    ('cargo-package', {'Cargo.toml': CARGO, 'src/main.rs': b'', 'src/lib.rs': b''}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-package-lib-only', {'Cargo.toml': CARGO, 'src/lib.rs': b''}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-workspace', {'Cargo.toml': b'[workspace]\nmembers = ["a"]\n'}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-both', {'Cargo.toml': b'[workspace]\n[package]\nname = "a"\n', 'src/main.rs': b''}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-workspace-dependencies-alone', {'Cargo.toml': b'[workspace.dependencies]\nserde = "1"\n'}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-inline-tables', {'Cargo.toml': b'workspace = {}\npackage = { name = "a" }\n', 'src/main.rs': b''}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-package-not-a-table', {'Cargo.toml': b'package = "a"\nworkspace = 1\n'}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-header-in-a-string', {'Cargo.toml': b'x = """\n[workspace]\n"""\n[package]\nname = "a"\n'}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-not-toml', {'Cargo.toml': b'[package\n'}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-bom', {'Cargo.toml': b'\xef\xbb\xbf' + CARGO}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-long-integer', {'Cargo.toml': CARGO + b'x = ' + b'9' * 5000 + b'\n', 'src/main.rs': b''}, ABSENT, (0, '', 'Cargo.toml')),
    ('cargo-large-float', {'Cargo.toml': CARGO + b'f = 1e9999\n', 'src/lib.rs': b''}, ABSENT, (0, '', 'Cargo.toml')),
    ('nextjs-routes', {'next.config.js': b'module.exports = {}', 'app/page.tsx': b'', 'app/a/route.js': b'', 'app/xpage.tsx': b'', 'app/a/layout.tsx': b'',
                       'pages/index.tsx': b'', 'pages/api/x.ts': b'', 'pages/readme.md': b'', 'src/pages/x.tsx': b''}, ABSENT, (0, '', 'package.json')),
    ('nextjs-config-order', {'next.config.ts': b'a', 'next.config.mjs': b'b'}, ABSENT, (0, '', 'package.json')),
    ('nextjs-without-routes', {'next.config.js': b'x'}, ABSENT, (0, '', 'package.json')),
    ('vite-with-index', {'vite.config.ts': b'export default {}', 'index.html': b''}, ABSENT, (0, '', 'package.json')),
    ('vite-without-index', {'vite.config.mjs': b'x'}, ABSENT, (0, '', 'package.json')),
    ('mixed', {'package.json': b'{"workspaces": ["p"], "jest": {}, "devDependencies": {"vue": "3"}}', 'tsconfig.json': b'{}', 'pnpm-workspace.yaml': b'packages: []\n',
               'Cargo.toml': CARGO, 'src/main.rs': b'', 'next.config.js': b'x', 'pages/a.tsx': b'', 'vite.config.ts': b'x', 'index.html': b''}, ABSENT, (4, 'apps/web', 'package.json')),
    ('canary-configs', {'package.json': b'{"scripts": {"postinstall": "touch /tmp/opensip-canary-1"}}', 'next.config.js': b'require("/tmp/opensip-canary-2")',
                        'vite.config.ts': b'import "/tmp/opensip-canary-3"', 'jest.config.js': b'require("/tmp/opensip-canary-4")', 'build.rs': b'fn main() {}',
                        '.npmrc': b'x', 'pnpmfile.cjs': b'require("/tmp/opensip-canary-5")', '.cargo/config.toml': b'[build]\nrustc-wrapper = "/tmp/opensip-canary-6"\n'},
     ABSENT, (0, '', 'package.json')),
    ('explicit-empty', {'Cargo.toml': CARGO, 'src/main.rs': b''}, [], (0, '', 'Cargo.toml')),
    ('explicit-list', {'Cargo.toml': CARGO, 'src/main.rs': b''}, ['src/main.rs'], (0, '', 'Cargo.toml')),
    ('explicit-over-unresolved', {'vite.config.ts': b'x'}, [], (0, '', 'package.json')),
    ('nothing', {'README.md': b'x'}, ABSENT, (2, 'crates/a', 'Cargo.toml')),
]
# (name, routes, vite with index.html, explicit)
BOUNDS = [(n, r, v, e) for (n, r, v) in (('65536-split', 65535, True), ('65537-split', 65536, True), ('65536-alone', 65536, False), ('65537-alone', 65537, False))
          for e in (ABSENT, [], ['src/main.ts'])]
FACTS = [b'[workspace]\n', CARGO, b'[', b'workspace = {}\n', b'workspace = 1\n', b'\xef\xbb\xbf[workspace]\n', b'[workspace.dependencies]\n']


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


def route_tree(routes, vite):
    files = {'next.config.js': b'x'}
    files.update({'pages/r%05d.tsx' % i: b'' for i in range(routes)})
    if vite:
        files.update({'vite.config.ts': b'x', 'index.html': b''})
    return files


def vectors(arch, packages):
    M = reference(arch)
    ref = M.load(arch, packages)
    explicit = lambda e: None if e == ABSENT else e
    units = []
    for name, files, e, (ordinal, root, marker) in UNITS:
        rec = ref.recognize(files, explicit(e))
        row = ref.unit_recognition(ordinal, root, marker, rec)
        if name == 'canary-configs':
            require('opensip-canary' not in json.dumps(rec), 'a canary path reached the recognition')
        units.append(dict(name=name, files={p: b.hex() for p, b in sorted(files.items())}, explicit=e,
                          unit=dict(unitOrdinal=ordinal, rootPath=root, markerPath=marker), recognition=rec, recognitionId=row['recognitionId']))
    bounds = []
    for name, routes, vite, e in BOUNDS:
        rec = ref.recognize(route_tree(routes, vite), explicit(e))
        row = ref.unit_recognition(0, '', 'package.json', rec)
        bounds.append(dict(name=name + '-' + ('absent' if e == ABSENT else 'explicit-empty' if e == [] else 'explicit-list'), routes=routes, vite=vite,
                           explicit=e, recognitionId=row['recognitionId'], entryPoints=rec['entryPoints'],
                           unresolved={r['recognizerId']: r['unresolvedChoices'] for r in rec['recognized']},
                           entryCounts={r['recognizerId']: len(r['effects']['entryPoints']) for r in rec['recognized']}))
    facts = [dict(hex=raw.hex(), fact=ref.cargo_workspace_fact(raw)) for raw in FACTS]
    provenance = [dict(recognizerId=r, recognizerVersion=1, rendered=M.discovered_provenance({'recognizerId': r, 'recognizerVersion': 1}))
                  for r in ('cargo-package', 'nextjs', 'vitest-jest')]
    body = {'schemaVersion': 1,
            'standing': 'Host framework recognition vectors (M3-B r9 item 16; B2-d plan r3 sections 3 and 4; unit B2-d2). Generated by '
                        'tools/host/framework_recognition_vectors.py from the bound B2-d0 reference (contract successor 171). '
                        '`explicit` is "absent" (no resolved discovery.entryPoints field) or the explicit list. Design evidence, not '
                        'product qualification.',
            'reference': dict(path=REFERENCE[0], bytes=REFERENCE[1], sha256=REFERENCE[2]),
            'units': units, 'bounds': bounds, 'cargoWorkspaceFacts': facts, 'provenance': provenance}
    return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout holding the reference')
    parser.add_argument('--packages-root', type=Path, required=True, help='checkout holding the provisioned python-packages snapshot')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    packages = args.packages_root.resolve(strict=True) / 'tools/contracts/python-packages'
    raw = vectors(args.architecture.resolve(strict=True), packages)
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the B2-d0 reference.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Framework recognition vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
