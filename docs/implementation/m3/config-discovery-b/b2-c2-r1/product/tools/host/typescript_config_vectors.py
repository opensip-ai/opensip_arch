"""Cross-implementation vectors for the pre-Plan TypeScript configuration graph (M3-B r8 item 14a; unit B2-c2).

Developer tool only. It writes or checks crates/host/src/typescript_config_vectors.json, which the host's
`typescript_config_tests.rs` replays against `jsonc.rs` and `typescript_config.rs`.

  * **The law's controls.** Each case is a project tree (files, directories and symbolic links), an entry
    configuration file and the result item 14a gives it, written here by hand from the law: the effective
    `allowJs` and `checkJs` and the entry's resolved edges, or the refusal's internal key and the path of the file
    that refused. This module's own reading of item 14a (`Reference`, below; Python, independent of the Rust) must
    give every expected result, or generation fails. The vector records the reference's whole result: the graph,
    and every path the reader asked the source for, in order, so the Rust must consult the same candidates in the
    same order.
  * **The graph record.** Every graph validates as `TypeScriptConfigGraphV1` in the S10 native model copy (contract
    successor 167) and has no `typescript_config_graph_faults`; each node's kind is the model's `config_node_kind`.
  * **The units cases.** The seven `units-config-effective-allowjs-*` cases of native-cases.v2.json, reproduced from
    configuration bytes: discovery over the case's markers without their trusted `allowJs`, the effective value read
    from bytes, and discovery again, through the B2-c0 reference (contract successor 166). The result must equal the
    reference's discovery over the case's own trusted markers and meet the case's expectations.
  * **The termination.** Item 14a's four alias rows and the public record, from S10's registry copy; the public
    detail's D9 row and remedy from the S10 model copy; the bounded subject from the model's `bounded_subject`.

No network, process or repository write except the output with --write.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/host/src/typescript_config_vectors.json'
NATIVE = 'docs/coop/design-corrections/native/'
S10 = 'docs/implementation/m3/config-discovery-b/s10-tsc/'
B2C0 = 'docs/implementation/m3/config-discovery-b/b2-c-reference/reference/native_unit_reference.py'
# Architecture inputs: path, bytes, SHA-256.
ARCH = (
    ('docs/implementation/m3/config-discovery-b/PROPOSAL-r8.md', 133196, '58adf8f0879f56b4a6ed9b4b6955e087fdad4423cd8134581d023911f8fe0d3f'),
    (S10 + 'reference/native_evidence_model.py', 321895, '0e05bbf08b801009d786fec86a35aca83feb972a9f995b59ed64fe1edff59af5'),
    (S10 + 'registry/public-detail-registry.v1.json', 67246, '1cf1269298d056d07aa846ad8efe2af9a2859c10302dc8e726ded13c9c149c48'),
    (B2C0, None, None),
    (NATIVE + 'native-cases.v2.json', None, None),
)
PUBLIC = 'native.typescript-config-unresolved'
KEYS = {
    'bound': 'native.typescript-config-bound',
    'cycle': 'native.typescript-config-extends-cycle',
    'unresolved': 'native.typescript-config-extends-unresolved',
    'malformed': 'native.typescript-config-malformed',
}
MAX_BYTES = 64 * 1024
MAX_NODES = 32


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned(root, path, size, digest):
    raw = (root / path).read_bytes()
    require((size is None or len(raw) == size) and (digest is None or hashlib.sha256(raw).hexdigest() == digest), 'input pin mismatch: ' + path)
    return raw


def packages(product, packages_root):
    closure = json.loads((product / 'tools/contracts/generator-closure.json').read_bytes())
    rows = [r for r in closure['files'] if r['path'].startswith('tools/contracts/python-packages/')]
    require(rows, 'no pinned python packages')
    for row in rows:
        pinned(packages_root, row['path'], row['bytes'], row['sha256'])
    return packages_root / 'tools/contracts/python-packages'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- the reference reading of item 14a

class Malformed(Exception):
    pass


def parse_jsonc(raw):
    """JSON (RFC 8259) with // and /* */ comments and one trailing comma per container; a leading BOM ignored;
    a duplicate key keeps its last value. Returns the root, or `None` when only whitespace and comments remain.
    Iterative, so nesting depth is bounded only by the input."""
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        raise Malformed('not UTF-8')
    i = 1 if text.startswith('﻿') else 0
    n = len(text)

    def skip(i):
        while i < n:
            c = text[i]
            if c in ' \t\n\r':
                i += 1
            elif text.startswith('//', i):
                while i < n and text[i] not in '\n\r':
                    i += 1
            elif text.startswith('/*', i):
                end = text.find('*/', i + 2)
                if end < 0:
                    raise Malformed('unterminated block comment')
                i = end + 2
            elif c == '/':
                raise Malformed('lone /')
            else:
                return i
        return i

    def string(i):
        i += 1
        out = []
        while True:
            if i >= n:
                raise Malformed('unterminated string')
            c = text[i]
            if c == '"':
                return ''.join(out), i + 1
            if c == '\\':
                e = text[i + 1:i + 2]
                simple = {'"': '"', '\\': '\\', '/': '/', 'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t'}
                if e in simple:
                    out.append(simple[e]); i += 2; continue
                if e != 'u':
                    raise Malformed('escape')
                hi = hex4(i + 2)
                i += 6
                if 0xD800 <= hi <= 0xDBFF:
                    if text[i:i + 2] != '\\u':
                        raise Malformed('lone surrogate')
                    lo = hex4(i + 2)
                    if not 0xDC00 <= lo <= 0xDFFF:
                        raise Malformed('lone surrogate')
                    out.append(chr(0x10000 + ((hi - 0xD800) << 10) + (lo - 0xDC00))); i += 6
                elif 0xDC00 <= hi <= 0xDFFF:
                    raise Malformed('lone surrogate')
                else:
                    out.append(chr(hi))
                continue
            if ord(c) < 0x20:
                raise Malformed('control character')
            out.append(c); i += 1

    def hex4(i):
        h = text[i:i + 4]
        if len(h) != 4 or any(c not in '0123456789abcdefABCDEF' for c in h):
            raise Malformed('\\u escape')
        return int(h, 16)

    def number(i):
        start = i
        if text[i:i + 1] == '-':
            i += 1
        if text[i:i + 1] == '0':
            i += 1
        elif text[i:i + 1] in tuple('123456789'):
            while i < n and text[i].isascii() and text[i].isdigit():
                i += 1
        else:
            raise Malformed('number')
        for lead, signs in (('.', ''), ('eE', '+-')):
            if i < n and text[i] in lead:
                i += 1
                if signs and i < n and text[i] in signs:
                    i += 1
                d = i
                while i < n and text[i].isascii() and text[i].isdigit():
                    i += 1
                if i == d:
                    raise Malformed('number')
        return ('number', text[start:i]), i

    def scalar(i):
        c = text[i:i + 1]
        if c == '"':
            return string(i)
        if c == '-' or (c.isascii() and c.isdigit()):
            return number(i)
        for word, value in (('true', True), ('false', False), ('null', None)):
            if text.startswith(word, i):
                return value, i + len(word)
        raise Malformed('value')

    def key(i):
        if text[i:i + 1] != '"':
            raise Malformed('key')
        k, i = string(i)
        i = skip(i)
        if text[i:i + 1] != ':':
            raise Malformed(':')
        return k, skip(i + 1)

    i = skip(i)
    if i == n:
        return None
    stack = []  # [container, pending key or None]
    while True:
        c = text[i:i + 1]
        if c == '{':
            i = skip(i + 1)
            if text[i:i + 1] == '}':
                done, i = {}, i + 1
            else:
                k, i = key(i)
                stack.append([{}, k]); continue
        elif c == '[':
            i = skip(i + 1)
            if text[i:i + 1] == ']':
                done, i = [], i + 1
            else:
                stack.append([[], None]); continue
        else:
            done, i = scalar(i)
        while True:
            if not stack:
                i = skip(i)
                if i != n:
                    raise Malformed('content after the root')
                return done
            frame = stack[-1]
            container = frame[0]
            closer = '}' if isinstance(container, dict) else ']'
            if isinstance(container, dict):
                container[frame[1]] = done
            else:
                container.append(done)
            i = skip(i)
            if text[i:i + 1] == ',':
                i = skip(i + 1)
                if text[i:i + 1] != closer:
                    if isinstance(container, dict):
                        frame[1], i = key(i)
                    break
                i += 1
            elif text[i:i + 1] == closer:
                i += 1
            else:
                raise Malformed('separator')
            stack.pop()
            done = container


def fields(raw):
    root = parse_jsonc(raw)
    if root is None:
        root = {}
    if not isinstance(root, dict):
        raise Malformed('root')
    options = root.get('compilerOptions', {})
    if not isinstance(options, dict):
        raise Malformed('compilerOptions')
    for name in ('allowJs', 'checkJs'):
        if name in options and not isinstance(options[name], bool):
            raise Malformed(name)
    extends = root.get('extends', [])
    if isinstance(extends, str):
        extends = [extends]
    if not isinstance(extends, list) or not all(isinstance(s, str) for s in extends):
        raise Malformed('extends')
    return options.get('allowJs'), options.get('checkJs'), extends


FIRST = set('abcdefghijklmnopqrstuvwxyz0123456789~-')
REST = FIRST | set('._')


def name_len(s):
    i = 0
    if s.startswith('@'):
        i = 1
        if s[i:i + 1] not in FIRST or not s[i:i + 1]:
            return None
        i += 1
        while s[i:i + 1] and s[i] in REST:
            i += 1
        if s[i:i + 1] != '/':
            return None
        i += 1
    if not s[i:i + 1] or s[i] not in FIRST:
        return None
    i += 1
    while s[i:i + 1] and s[i] in REST:
        i += 1
    return i


def norm(directory, segments):
    out = [s for s in directory.split('/') if s]
    for s in segments:
        if s == '.':
            continue
        if s == '..':
            if not out:
                return None
            out.pop()
        else:
            out.append(s)
    return '/'.join(out)


def candidates(directory, s):
    """('malformed' | 'unresolved', None) or (None, [candidate paths])."""
    if not s or '\\' in s or any(ord(c) < 0x20 for c in s) or s.endswith('/') or '//' in s:
        return 'malformed', None
    if s.startswith('./') or s.startswith('../'):
        segments = s.split('/')
        spellings = [segments] if segments[-1].endswith('.json') else [segments, segments[:-1] + [segments[-1] + '.json']]
        out = [norm(directory, sp) for sp in spellings]
        return ('unresolved', None) if None in out else (None, out)
    if s.startswith('/'):
        return 'unresolved', None
    k = name_len(s)
    if k is None or k > 214:
        return 'malformed', None
    name, rest = s[:k], s[k:]
    if rest and (not rest.startswith('/') or any(seg in ('', '.', '..') for seg in rest[1:].split('/'))):
        return 'malformed', None
    sub = rest[1:]
    out = []
    e = directory
    while True:
        base = (e + '/' if e else '') + 'node_modules/' + name
        out += [base, base + '.json', base + '/tsconfig.json'] if not sub else [base + '/' + sub, base + '/' + sub + '.json']
        if not e:
            return None, out
        e = e.rpartition('/')[0]


class Refused(Exception):
    def __init__(self, key, path):
        super().__init__(key + ':' + path)
        self.key, self.path = KEYS[key], path


def kind(path):
    base = path.rpartition('/')[2]
    return {'tsconfig.json': 'tsconfig', 'jsconfig.json': 'jsconfig'}.get(base, 'other')


def effective(entry, source):
    """Item 14a and NE:527-545 over `source(path) -> ('file', bytes) | ('none', None) | ('link', None)`."""
    state, reads = {}, {}

    def resolve(frm, s):
        why, cands = candidates(frm.rpartition('/')[0], s)
        if why:
            raise Refused(why, frm)
        for c in cands:
            if c == '':
                continue
            what, raw = source(c)
            if what == 'file':
                return c, raw
            if what == 'link':
                raise Refused('unresolved', frm)
        raise Refused('unresolved', frm)

    def visit(path, raw):
        if len(raw) > MAX_BYTES:
            raise Refused('bound', path)
        try:
            allow, check, extends = fields(raw)
        except Malformed:
            raise Refused('malformed', path)
        state[path] = 'on-path'
        edges = []
        for s in extends:
            target, traw = resolve(path, s)
            if state.get(target) == 'on-path':
                raise Refused('cycle', path)
            if target not in state:
                if len(state) == MAX_NODES:
                    raise Refused('bound', path)
                visit(target, traw)
            edges.append(target)
        state[path] = 'done'
        reads[path] = dict(sha=hashlib.sha256(raw).hexdigest(), allow=allow, check=check, edges=edges)

    what, raw = source(entry)
    if what == 'link':
        raise Refused('unresolved', entry)
    require(what == 'file', 'entry is not a file: ' + entry)
    visit(entry, raw)

    def inherited(path):
        r = reads[path]
        allow = check = None
        for e in r['edges']:
            a, c = inherited(e)
            allow = a if a is not None else allow
            check = c if c is not None else check
        own = r['allow'] if r['allow'] is not None or kind(path) != 'jsconfig' else True
        return (own if own is not None else allow), (r['check'] if r['check'] is not None else check)

    allow, check = inherited(entry)
    check = bool(check)
    graph = {'schemaVersion': 1, 'entryConfigPath': entry,
             'nodes': [{'path': p, 'contentSha256': reads[p]['sha'], 'kind': kind(p), 'extendsResolved': reads[p]['edges']} for p in sorted(reads)]}
    return {'allowJs': check if allow is None else allow, 'checkJs': check, 'graph': graph}


# --------------------------------------------------------------------------- trees

def expand(entry):
    if 'text' in entry:
        return entry['text'].encode('utf-8')
    if 'hex' in entry:
        return bytes.fromhex(entry['hex'])
    pad = entry['pad']
    return (pad['prefix'] + pad['repeat'] * pad['count'] + pad['suffix']).encode('utf-8')


class Tree:
    """An in-memory project tree: files, directories and symbolic links, as the Rust test source reads it."""

    def __init__(self, entries):
        self.entries = {e['path']: e for e in entries}
        self.log = []

    def __call__(self, path):
        self.log.append(path)
        parts = path.split('/')
        for k in range(1, len(parts) + 1):
            e = self.entries.get('/'.join(parts[:k]))
            if e is not None and e.get('link'):
                return 'link', None
            if e is not None and k < len(parts) and not e.get('dir'):
                return 'none', None
        e = self.entries.get(path)
        if e is None or e.get('dir'):
            return 'none', None
        return 'file', expand(e)[:MAX_BYTES + 1]


def f(path, text):
    return {'path': path, 'text': text}


def link(path):
    return {'path': path, 'link': True}


def d(path):
    return {'path': path, 'dir': True}


def opts(allow=None, check=None, extends=None):
    o = {}
    if allow is not None:
        o['allowJs'] = allow
    if check is not None:
        o['checkJs'] = check
    body = {'compilerOptions': o}
    if extends is not None:
        body['extends'] = extends
    return json.dumps(body)


def ok(allow, check, edges=None):
    return {'allowJs': allow, 'checkJs': check, 'edges': edges}


def no(key, path):
    return {'refused': KEYS[key], 'path': path}


def ext(spec):
    return json.dumps({'extends': spec})


T = 'tsconfig.json'


def cases():
    """Item 14a's controls (B2-c2), each with the result the law gives it."""
    c = []

    def case(cid, tree, expect, entry=T):
        c.append({'id': cid, 'tree': tree, 'entry': entry, 'expect': expect})

    # JSONC: comments, trailing commas, BOM, empty documents, duplicate keys.
    case('jsonc-comments-and-trailing-commas', [f(T, '// header\n{ /* a */ "compilerOptions": { "checkJs": true, // c\n }, "extends": ["./b.json",], /* end */ }\n'), f('b.json', '{}')], ok(True, True, ['b.json']))
    case('jsonc-line-comment-ends-at-cr', [f(T, '{ // x\r"compilerOptions": {"allowJs": true}}')], ok(True, False))
    case('jsonc-bom-ignored', [{'path': T, 'hex': 'efbbbf' + opts(allow=True).encode().hex()}], ok(True, False))
    case('jsonc-empty-tsconfig-is-an-empty-object', [f(T, '')], ok(False, False))
    case('jsonc-comment-only-jsconfig-is-an-empty-object', [f('jsconfig.json', ' // nothing\n/* here */\n')], ok(True, False), entry='jsconfig.json')
    case('jsonc-duplicate-key-last-wins', [f(T, '{"compilerOptions": {"allowJs": false, "allowJs": true}}')], ok(True, False))
    case('jsonc-duplicate-object-replaced-whole', [f(T, '{"compilerOptions": {"allowJs": true}, "compilerOptions": {"checkJs": false}}')], ok(False, False))
    case('jsonc-other-fields-and-values-ignored', [f(T, '{"compilerOptions": {"target": "es2022", "paths": {"a/*": ["b/*"]}, "maxNodeModuleJsDepth": 2, "x": -1.5e+3, "y": null, "z": "\\u00e9\\ud83d\\ude00\\n"}, "include": ["src"], "references": []}')], ok(False, False))
    case('jsonc-deep-nesting-within-the-bound', [{'path': T, 'pad': {'prefix': '{"x": ' + '[' * 30000, 'repeat': '', 'count': 0, 'suffix': ']' * 30000 + ', "compilerOptions": {"allowJs": true}}'}}], ok(True, False))
    for name, text in (
        ('unterminated-block-comment', '{"compilerOptions": {}} /* x'),
        ('lone-slash', '{"compilerOptions": {}} /'),
        ('single-quoted-string', "{'compilerOptions': {}}"),
        ('leading-comma', '{"extends": [,"./b.json"]}'),
        ('double-trailing-comma', '{"compilerOptions": {},,}'),
        ('comma-only-object', '{,}'),
        ('missing-comma', '{"a": 1 "b": 2}'),
        ('content-after-root', '{} {}'),
        ('lone-high-surrogate', '{"a": "\\ud800"}'),
        ('lone-low-surrogate', '{"a": "\\udc00x"}'),
        ('raw-control-character', '{"a": "x\ty"}'),
        ('leading-zero-number', '{"a": 01}'),
        ('plus-number', '{"a": +1}'),
        ('nan', '{"a": NaN}'),
        ('unquoted-key', '{compilerOptions: {}}'),
        ('top-level-array', '[]'),
        ('top-level-string', '"tsconfig"'),
        ('compiler-options-array', '{"compilerOptions": []}'),
        ('compiler-options-null', '{"compilerOptions": null}'),
        ('allowjs-string', '{"compilerOptions": {"allowJs": "true"}}'),
        ('allowjs-null', '{"compilerOptions": {"allowJs": null}}'),
        ('checkjs-number', '{"compilerOptions": {"checkJs": 1}}'),
        ('extends-number', '{"extends": 1}'),
        ('extends-null', '{"extends": null}'),
        ('extends-object', '{"extends": {"path": "./b.json"}}'),
        ('extends-array-with-number', '{"extends": ["./b.json", 2]}'),
    ):
        case('malformed-' + name, [f(T, text), f('b.json', '{}')], no('malformed', T))
    case('malformed-invalid-utf-8', [{'path': T, 'hex': '7b22223a22ff227d'}], no('malformed', T))
    case('malformed-base-file', [f(T, ext('./b.json')), f('b.json', '{"compilerOptions": {"checkJs": "yes"}}')], no('malformed', 'b.json'))

    # Bounds.
    pad = lambda size: {'prefix': '{"compilerOptions": {"allowJs": true}, "pad": "', 'repeat': 'x', 'count': size - len('{"compilerOptions": {"allowJs": true}, "pad": ""}'), 'suffix': '"}'}  # noqa: E731
    case('bound-file-at-64-kib', [{'path': T, 'pad': pad(MAX_BYTES)}], ok(True, False))
    case('bound-file-over-64-kib', [{'path': T, 'pad': pad(MAX_BYTES + 1)}], no('bound', T))
    case('bound-base-over-64-kib', [f(T, ext('./b.json')), {'path': 'b.json', 'pad': pad(MAX_BYTES + 1)}], no('bound', 'b.json'))
    chain = lambda count: [f(T, ext('./c1.json'))] + [f(f'c{k}.json', ext(f'./c{k + 1}.json') if k < count - 1 else opts(allow=True)) for k in range(1, count)]  # noqa: E731
    case('bound-32-nodes', chain(32), ok(True, False, ['c1.json']))
    case('bound-33-nodes', chain(33), no('bound', 'c31.json'))

    # Path specifiers: candidate order, normalization, containment, no decoding.
    case('path-json-suffix-one-candidate', [f(T, ext('./base.json')), f('base.json', opts(allow=True)), f('base.json.json', opts(allow=False))], ok(True, False, ['base.json']))
    case('path-json-suffix-no-fallback', [f(T, ext('./base.json')), f('base.json.json', opts(allow=False))], no('unresolved', T))
    case('path-bare-file-first', [f(T, ext('./base')), f('base', opts(allow=True)), f('base.json', opts(allow=False))], ok(True, False, ['base']))
    case('path-bare-then-json', [f(T, ext('./base')), f('base.json', opts(allow=True))], ok(True, False, ['base.json']))
    case('path-directory-is-not-a-file', [f(T, ext('./base')), d('base'), f('base/tsconfig.json', opts(allow=False)), f('base.json', opts(allow=True))], ok(True, False, ['base.json']))
    case('path-parent-from-member', [f('packages/web/tsconfig.json', ext('../../tsconfig.base.json')), f('tsconfig.base.json', opts(check=True))], ok(True, True, ['tsconfig.base.json']), entry='packages/web/tsconfig.json')
    case('path-normalizes', [f(T, ext('./a/../b')), f('b.json', opts(allow=True))], ok(True, False, ['b.json']))
    case('path-escape-from-root', [f(T, ext('../x.json'))], no('unresolved', T))
    case('path-escape-after-descent', [f(T, ext('./a/../../x.json'))], no('unresolved', T))
    case('path-no-percent-decoding', [f(T, ext('./a%2Fb')), f('a/b.json', opts(allow=False)), f('a%2Fb.json', opts(allow=True))], ok(True, False, ['a%2Fb.json']))
    case('path-absolute-unresolved', [f(T, ext('/etc/tsconfig.json'))], no('unresolved', T))
    case('path-missing-base', [f(T, ext('./missing'))], no('unresolved', T))
    case('path-unresolved-refuses-whatever-own-options-settle', [f(T, '{"compilerOptions": {"allowJs": true}, "extends": "./missing.json"}')], no('unresolved', T))
    case('path-root-is-not-a-file', [f(T, ext('./a/..')), f('a/...json', opts(allow=True))], ok(True, False, ['a/...json']))

    # Package specifiers.
    case('package-bare-tsconfig', [f(T, ext('pkg')), f('node_modules/pkg/tsconfig.json', opts(allow=True))], ok(True, False, ['node_modules/pkg/tsconfig.json']))
    case('package-bare-file-first', [f(T, ext('pkg')), f('node_modules/pkg.json', opts(allow=False)), f('node_modules/pkg/tsconfig.json', opts(allow=True))], ok(False, False, ['node_modules/pkg.json']))
    case('package-subpath', [f(T, ext('pkg/base')), f('node_modules/pkg/base.json', opts(allow=True)), f('node_modules/pkg/tsconfig.json', opts(allow=False))], ok(True, False, ['node_modules/pkg/base.json']))
    case('package-subpath-json-first', [f(T, ext('pkg/tsconfig.json')), f('node_modules/pkg/tsconfig.json', opts(allow=True)), f('node_modules/pkg/tsconfig.json.json', opts(allow=False))], ok(True, False, ['node_modules/pkg/tsconfig.json']))
    case('package-subpath-json-then-json-json', [f(T, ext('pkg/strict.json')), f('node_modules/pkg/strict.json.json', opts(allow=True))], ok(True, False, ['node_modules/pkg/strict.json.json']))
    case('package-scoped-subpath', [f(T, ext('@scope/cfg/strict')), f('node_modules/@scope/cfg/strict.json', opts(check=True))], ok(True, True, ['node_modules/@scope/cfg/strict.json']))
    case('package-nearest-node-modules-first', [f('packages/web/tsconfig.json', ext('pkg')), f('packages/web/node_modules/pkg/tsconfig.json', opts(allow=True)), f('node_modules/pkg/tsconfig.json', opts(allow=False))], ok(True, False, ['packages/web/node_modules/pkg/tsconfig.json']), entry='packages/web/tsconfig.json')
    case('package-falls-back-to-the-root', [f('packages/web/tsconfig.json', ext('pkg')), d('packages/web/node_modules'), f('node_modules/pkg/tsconfig.json', opts(allow=False))], ok(False, False, ['node_modules/pkg/tsconfig.json']), entry='packages/web/tsconfig.json')
    case('package-base-extends-a-package', [f(T, ext('a')), f('node_modules/a/tsconfig.json', ext('b')), f('node_modules/a/node_modules/b/tsconfig.json', opts(allow=True)), f('node_modules/b/tsconfig.json', opts(allow=False))], ok(True, False, ['node_modules/a/tsconfig.json']))
    case('package-dots-in-name', [f(T, ext(['pkg..x', '@scope/a.b'])), f('node_modules/pkg..x/tsconfig.json', opts(allow=False)), f('node_modules/@scope/a.b/tsconfig.json', opts(check=True))], ok(False, True, ['node_modules/pkg..x/tsconfig.json', 'node_modules/@scope/a.b/tsconfig.json']))
    case('package-missing', [f(T, ext('pkg'))], no('unresolved', T))
    case('package-exports-not-evaluated', [f(T, ext('pkg/strict')), f('node_modules/pkg/package.json', '{"exports": {"./strict": "./configs/strict.json"}}'), f('node_modules/pkg/configs/strict.json', opts(allow=True))], no('unresolved', T))
    for spec in ('pkg/../base', 'pkg/./base', 'pkg//base', 'pkg\\base', './a//b', './a/', '.pkg', '_pkg', 'Pkg', '@Scope/x', '', 'pkg/', '@scope', '@scope/', 'pkg+x', '.', '..', './a\u0001', 'a' * 215):
        case('malformed-specifier-' + (spec.encode().hex() if spec else 'empty'), [f(T, ext(spec)), f('node_modules/pkg/tsconfig.json', '{}')], no('malformed', T))
    case('package-name-at-214', [f(T, ext('a' * 214)), f('node_modules/' + 'a' * 214 + '/tsconfig.json', opts(allow=True))], ok(True, False, ['node_modules/' + 'a' * 214 + '/tsconfig.json']))

    # Graph identity, cycles.
    case('node-identity-two-spellings', [f(T, ext(['./b.json', './x/../b.json'])), f('b.json', opts(allow=True))], ok(True, False, ['b.json', 'b.json']))
    case('diamond-one-node', [f(T, ext(['./a.json', './b.json'])), f('a.json', ext('./d.json')), f('b.json', ext('./d.json')), f('d.json', opts(check=True))], ok(True, True, ['a.json', 'b.json']))
    case('cycle-two-files', [f(T, ext('./a.json')), f('a.json', ext('./tsconfig.json'))], no('cycle', 'a.json'))
    case('cycle-self', [f(T, ext('./tsconfig.json'))], no('cycle', T))
    case('cycle-after-a-repetition', [f(T, ext(['./a.json', './a.json'])), f('a.json', ext('./b.json')), f('b.json', ext('./a.json'))], no('cycle', 'b.json'))

    # Symbolic links before C1.
    case('link-base-file', [f(T, ext('./b.json')), link('b.json')], no('unresolved', T))
    case('link-package-directory', [f(T, ext('pkg')), link('node_modules/pkg')], no('unresolved', T))
    case('link-node-modules', [f(T, ext('pkg')), link('node_modules')], no('unresolved', T))
    case('link-earlier-candidate', [f(T, ext('./base')), link('base'), f('base.json', opts(allow=True))], no('unresolved', T))
    case('link-entry', [link(T)], no('unresolved', T))
    case('link-entry-directory', [link('packages/web'), f('packages/web/tsconfig.json', '{}')], no('unresolved', 'packages/web/tsconfig.json'), entry='packages/web/tsconfig.json')

    # Inheritance (NE:527-545).
    two = lambda a, b: [f('a.json', opts(allow=a)), f('b.json', opts(allow=b))]  # noqa: E731
    case('inherit-later-extends-wins', [f(T, ext(['./a.json', './b.json']))] + two(True, False), ok(False, False, ['a.json', 'b.json']))
    case('inherit-later-extends-wins-reversed', [f(T, ext(['./b.json', './a.json']))] + two(True, False), ok(True, False, ['b.json', 'a.json']))
    case('inherit-own-beats-base', [f(T, opts(allow=False, extends='./a.json')), f('a.json', opts(allow=True))], ok(False, False, ['a.json']))
    case('inherit-checkjs-derives', [f(T, ext('./a.json')), f('a.json', opts(check=True))], ok(True, True, ['a.json']))
    case('inherit-own-checkjs-false', [f(T, opts(check=False, extends='./a.json')), f('a.json', opts(check=True))], ok(False, False, ['a.json']))
    case('inherit-written-false-beats-checkjs', [f(T, opts(allow=False, check=True))], ok(False, True))
    case('inherit-base-allowjs-beats-own-checkjs', [f(T, opts(check=True, extends='./a.json')), f('a.json', opts(allow=False))], ok(False, True, ['a.json']))
    case('inherit-jsconfig-entry-over-false-base', [f('jsconfig.json', ext('./base.json')), f('base.json', opts(allow=False))], ok(True, False, ['base.json']), entry='jsconfig.json')
    case('inherit-jsconfig-entry-written-false', [f('jsconfig.json', opts(allow=False))], ok(False, False), entry='jsconfig.json')
    case('inherit-tsconfig-over-jsconfig-base', [f(T, ext('./shared/jsconfig.json')), f('shared/jsconfig.json', '{}')], ok(True, False, ['shared/jsconfig.json']))
    case('inherit-jsconfig-named-base-is-other', [f(T, ext('./jsconfig.base.json')), f('jsconfig.base.json', '{}')], ok(False, False, ['jsconfig.base.json']))
    case('inherit-tsconfig-own-false-over-jsconfig-base', [f(T, opts(allow=False, extends='./shared/jsconfig.json')), f('shared/jsconfig.json', '{}')], ok(False, False, ['shared/jsconfig.json']))
    case('inherit-later-base-without-allowjs-keeps-earlier', [f(T, ext(['./a.json', './b.json'])), f('a.json', opts(allow=True)), f('b.json', opts(check=False))], ok(True, False, ['a.json', 'b.json']))
    case('inherit-empty-extends-array', [f(T, '{"extends": [], "compilerOptions": {"checkJs": true}}')], ok(True, True, []))
    return c


# Configuration bytes reproducing each units case's trusted observation (item 14a's controls: "The units cases").
UNITS = {
    'units-config-effective-allowjs-jsconfig-default': [f('jsconfig.json', '{}')],
    'units-config-effective-allowjs-jsconfig-false': [f('jsconfig.json', '// explicit\n{"compilerOptions": {"allowJs": false,},}')],
    'units-config-effective-allowjs-jsconfig-true': [f('jsconfig.json', '{"extends": "./base.json", "compilerOptions": {"allowJs": true}}'), f('base.json', opts(allow=False))],
    'units-config-effective-allowjs-tsconfig-false': [f(T, '{"extends": "./base.json"}'), f('base.json', opts(check=False))],
    'units-config-effective-allowjs-tsconfig-true': [f(T, '{"extends": "./tsconfig.base.json"}'), f('tsconfig.base.json', opts(check=True))],
    'units-config-effective-allowjs-package-only': [f('package.json', '{}')],
    'units-config-effective-allowjs-tsconfig-before-jsconfig': [f(T, opts(allow=False)), f('jsconfig.json', opts(allow=True))],
}


def run(entry, tree):
    try:
        return {'outcome': 'result', 'result': effective(entry, tree)}
    except Refused as r:
        return {'outcome': 'refused', 'key': r.key, 'path': r.path}


def vectors(arch, product, packages_root):
    pins = []
    for row in ARCH:
        raw = pinned(arch, *row)
        pins.append(dict(path=row[0], bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    nur = load('native_unit_reference', arch / B2C0)
    historical, current = nur.load(arch, packages(product, packages_root))
    del historical
    model = nur._module_at('s10_native_model', arch / ARCH[1][0], arch / NATIVE / 'native_evidence_model.py')

    def admit_graph(graph):
        model.validate_native('TypeScriptConfigGraphV1', graph)
        require(model.typescript_config_graph_faults(graph) == [], 'graph faults')
        require(all(model.config_node_kind(n['path']) == n['kind'] for n in graph['nodes']), 'kind law')
        require(model.typescript_config_origin(graph) == ('jsconfig' if kind(graph['entryConfigPath']) == 'jsconfig' else 'tsconfig'), 'origin')
        model.typescript_config_graph_digest(graph)

    out_cases = []
    for c in cases():
        tree = Tree(c['tree'])
        got = run(c['entry'], tree)
        want = c['expect']
        if 'refused' in want:
            require(got['outcome'] == 'refused' and got['key'] == want['refused'] and got['path'] == want['path'], 'case ' + c['id'] + ': ' + json.dumps(got)[:300])
        else:
            require(got['outcome'] == 'result', 'case ' + c['id'] + ': ' + json.dumps(got)[:300])
            r = got['result']
            require(r['allowJs'] == want['allowJs'] and r['checkJs'] == want['checkJs'], 'case ' + c['id'] + ' options')
            entry_node = next(n for n in r['graph']['nodes'] if n['path'] == c['entry'])
            require(entry_node['extendsResolved'] == (want['edges'] or []), 'case ' + c['id'] + ' edges ' + json.dumps(entry_node['extendsResolved']))
            admit_graph(r['graph'])
        out_cases.append(dict(id=c['id'], tree=c['tree'], entry=c['entry'], reads=tree.log, **got))
    require(len({c['id'] for c in out_cases}) == len(out_cases), 'duplicate case ids')

    doc = json.loads((arch / ARCH[4][0]).read_bytes())
    units = []
    for case in [c for c in doc['cases'] if c['id'].startswith('units-config-effective-allowjs-')]:
        require(case['id'] in UNITS, 'unmapped units case ' + case['id'])
        step = case['steps'][0]
        require(step['fn'] == 'discover_units' and len(case['steps']) == 1, 'units case shape')
        trusted = step['args']['markers']
        raw = {path: {k: v for k, v in fact.items() if k != 'allowJs'} for path, fact in trusted.items()}
        tree = Tree(UNITS[case['id']])
        first = current.discover_units(markers=copy.deepcopy(raw), explicit_workspace_roots=None, boundaries=None)
        observed = copy.deepcopy(raw)
        for u in first['units']:
            if u['languageFamily'] == 'tsjs' and u['markerPath'].rpartition('/')[2] in ('tsconfig.json', 'jsconfig.json'):
                observed[u['markerPath']]['allowJs'] = effective(u['markerPath'], tree)['allowJs']
        final = current.discover_units(markers=copy.deepcopy(observed), explicit_workspace_roots=None, boundaries=None)
        require(final == current.discover_units(markers=copy.deepcopy(trusted), explicit_workspace_roots=None, boundaries=None), 'units case differs from its trusted observation: ' + case['id'])
        for path, value in case['expect'].items():
            require(path.startswith('$u.'), 'expect path')
            node = final
            for part in path[3:].split('.'):
                node = node[int(part)] if part.isdigit() else node[part]
            require(node == value, 'units expectation ' + case['id'] + ' ' + path)
        units.append(dict(id=case['id'], markers=raw, tree=UNITS[case['id']], observed=observed, reads=tree.log, result=final))
    require(sorted(u['id'] for u in units) == sorted(UNITS), 'units coverage')

    registry = json.loads((arch / ARCH[2][0]).read_bytes())
    aliases = sorted([r['internalCode'], r['publicCode']] for r in registry['internalAliases'] if r['internalCode'] in KEYS.values())
    require([a[0] for a in aliases] == sorted(KEYS.values()) and all(a[1] == PUBLIC for a in aliases), 'alias rows differ')
    record = [r for r in registry['records'] if r['code'] == PUBLIC]
    require(len(record) == 1 and record[0]['owner'] == 'native' and not any(r['code'] in KEYS.values() for r in registry['records']), 'public record differs')
    row = model.D9_MAP[PUBLIC]
    remedy = model.PUBLIC_ROUTE_REMEDIES[PUBLIC]
    terminations = []
    for key in sorted(KEYS.values()):
        for path in ('packages/web/tsconfig.json', 'deep/' + 'd' * 1100 + '/tsconfig.json', 'café/' + 'é' * 1000 + '/jsconfig.json'):
            terminations.append(dict(key=key, path=path, subject=model.bounded_subject(key + ':' + path)))
    body = {'schemaVersion': 1,
            'standing': 'B2-c2 TypeScript configuration graph vectors, generated by tools/host/typescript_config_vectors.py: the law controls of M3-B r8 item 14a, their graphs admitted by the S10 native model copy (contract successor 167), and the units cases through the B2-c0 reference (contract successor 166). Design evidence, not qualification.',
            'reference': pins, 'aliases': aliases, 'publicRecord': record[0],
            'd9': {'class': row['class'], 'exitCode': row['exitCode'], 'code': row['code'], 'remedy': remedy},
            'cases': out_cases, 'units': units, 'terminations': terminations}
    return (json.dumps(body, separators=(',', ':'), ensure_ascii=True, sort_keys=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout holding the references')
    parser.add_argument('--packages-root', type=Path, required=True, help='checkout holding the provisioned python-packages snapshot')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raw = vectors(args.architecture.resolve(strict=True), product, args.packages_root.resolve(strict=True))
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the item 14a controls and the S10 and B2-c0 references.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'TypeScript configuration vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
