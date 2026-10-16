"""Cross-implementation vectors for the D15 readers and membership decision (M3-B r9 items 19 to 24; unit B3-b2b1, plan r2
amendment A2).

Developer tool only. It runs B3-b0, the members-and-readers reference (contract successor 168), at its bound bytes over
its own checker's D15 cases (`b3-b-reference/evidence/check.py`, `d15_cases`) and over every discovery case of
security/discovery-cases.v1.json (none declares a member), and writes or checks
crates/security/src/workspace_member_vectors.json. No case is written here.

The decision core (`workspace_declarations.rs`) is B3-b0's `discover` without SLM's two passes, so each vector records,
by wrapping the reference's `_finish` and `_refuse` (their bytes unchanged), what the core decides and what it is
given:
  * `observation`: the synthetic tree below W, keyed W-relative (`""` is W), with the carrier and manifest bytes, the VCS
    side table and item 6b's supplied verdicts; W2 (no VCS marker at W or an ancestor, item 6a's NoRepository) and the
    invocation facts (invoking user, groups, the owner waiver, the workspace-roots array and its source);
  * `trial`: in branch A, the provisional members the reference's trial pass two was given, and that pass's status;
  * `expected`: the outcome. `members` (with `declaredBy`), `declarations` (the `workspaceDeclarations` rows) and
    `links` for a decided member set; a member-rule refusal's code, path and detail with the rows of the discovery
    without members; or `trial-refused` with the rows the trial carried;
  * `consulted` and `read`: every W-relative path the reference's reader code looked up (`_entry`) or read (`contents`),
    so the security test can assert that the core consults nothing else (B3B0REF-R2-RF-1's spy), and `forbidden`: the
    checker case's own `notRead` and `notObserved` paths, which the core must never touch (A2 r2, B3BA2-R1-RF-2).
Parser controls (A2 r2, B3BA2-R1-RF-1) follow the cases, labelled `control:`. JSON controls must equal the reference.
TOML controls exceed parse_toml's local bounds in an unrelated field of an otherwise usable carrier or provider manifest:
`tomllib` reads them (`referenceExpected`), and the product's `expected` is the existing `parse` disposition, computed
by running the reference over the same input with that file's bytes replaced by unparseable TOML (the carrier's digest
is the real bytes'). A large content is stored as `{"parts": [text | [unit, count], ...]}`.
Cases with no selected root (no W, so no carrier) and the side-table consistency control are listed by id only.
No filesystem tree, network or environment input.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/security/src/custody/workspace_member_vectors.json'
SCAN_TOOL = 'tools/security/discovery_scan_vectors.py'
REF = 'docs/implementation/m3/config-discovery-b/b3-b-reference/reference/member_reader_reference.py'
CHECK = 'docs/implementation/m3/config-discovery-b/b3-b-reference/evidence/check.py'
CASES = 'docs/coop/design-corrections/security/discovery-cases.v1.json'
READERS = ('cargo-config-patch', 'npm-workspaces-members')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rel(W, p):
    return '' if p == W else p[len(W.rstrip('/')) + 1:] if p.startswith(W.rstrip('/') + '/') else None


def under(W, table):
    return {r: v for p, v in table.items() if (r := rel(W, p)) is not None}


class Recorder:
    """Wraps the reference's `_finish` and `_refuse` for one `discover` call, recording each call's decision inputs."""

    def __init__(self, ref):
        self.ref, self.finishes, self.refusals = ref, [], []
        self.finish, self.refuse = ref._finish, ref._refuse

    def __enter__(self):
        def finish(ctx, inp, base, first, members, declared_by, rows, unresolved, links):
            result, out_links = self.finish(ctx, inp, base, first, members, declared_by, rows, unresolved, links)
            self.finishes.append(dict(members=list(members), declarations=self.ref._declaration_rows(rows, unresolved),
                                      status=result['status'], result=result, links=out_links))
            return result, out_links

        def refuse(slm, prov, code, path, detail):
            self.refusals.append(dict(code=code, path=path, detail=detail))
            return self.refuse(slm, prov, code, path, detail)
        self.ref._finish, self.ref._refuse = finish, refuse
        return self

    def __exit__(self, *exc):
        self.ref._finish, self.ref._refuse = self.finish, self.refuse


def relative_rows(W, rows):
    """The declaration rows with the carrier path W-relative (the core works below W; the composition spells it)."""
    return [dict(r, path=rel(W, r['path']) if r['path'] else None) for r in rows]


def vector(ref, ctx, cid, inp, forbidden=()):
    spy_contents = SpyContents(inp.get('contents', {}))
    ref.OBSERVED = []
    try:
        with Recorder(ref) as rec:
            result, links = ref.discover(ctx, dict(inp, contents=spy_contents))
        observed = list(ref.OBSERVED)
    finally:
        ref.OBSERVED = None
    prov = result['provenance']
    W = prov.get('selectedRoot')
    source = prov.get('unitSource')
    if W is None or source is None:
        return None
    w2 = not any(ref._markers(dict(inp, fs=ref._project_vcs(inp)), a) for a in ref._ancestors(W))
    array = inp.get('explicitJoins') or inp.get('configWorkspaceRoots') or []
    waive = bool(inp.get('trustProjectOwner', False)) and prov.get('mode') == 'explicit'
    fs = ref._project_vcs(inp)
    observation = dict(fs=under(W, fs), contents=under(W, inp.get('contents', {})), vcsMarkers=under(W, inp.get('vcsMarkers', {})),
                       memberObservations=under(W, inp.get('memberObservations', {})))
    facts = dict(root=W, uid=inp['invokingUid'], groups=sorted(inp.get('authorizedGroupIds', [])), waive=waive, w2=w2,
                 array=list(array), arraySource='explicit-joins' if inp.get('explicitJoins') else 'config-workspace-roots')
    trial = None
    if w2 and array:
        first = rec.finishes[0]
        trial = dict(provisional=first['members'], status=first['status'])
    if rec.refusals:
        require(len(rec.refusals) == 1, 'two member-rule refusals: ' + cid)
        plain = rec.finishes[-1]
        require(plain['members'] == [], 'a refusal carries members: ' + cid)
        r = rec.refusals[0]
        expected = dict(kind='refuse', code=r['code'], path=rel(W, r['path']) if r['path'] else None, detail=r['detail'],
                        declarations=relative_rows(W, plain['declarations']))
    elif trial is not None and trial['status'] != 'ACCEPT':
        require(len(rec.finishes) == 1, 'trial refusal decided twice: ' + cid)
        expected = dict(kind='trial-refused', declarations=relative_rows(W, rec.finishes[0]['declarations']))
    else:
        last = rec.finishes[-1]
        require(last['result'] is result, 'the result is not the last pass two: ' + cid)
        members = [dict(path=rel(W, m['path']), declaredBy=[dict(d, path=rel(W, d['path'])) for d in m['declaredBy']])
                   for m in result['provenance']['memberRepositories']]
        expected = dict(kind='members', members=members, declarations=relative_rows(W, last['declarations']),
                        links=[dict(l, providerMember=rel(W, l['providerMember'])) for l in links])
    consulted = sorted({r for p in observed if (r := rel(W, p)) is not None}, key=lambda s: s.encode())
    read = sorted({r for p in spy_contents.asked if (r := rel(W, p)) is not None}, key=lambda s: s.encode())
    return dict(id=cid, observation=observation, facts=facts, trial=trial, expected=expected, consulted=consulted, read=read,
                forbidden=sorted({r for p in forbidden if (r := rel(W, p)) is not None}, key=lambda s: s.encode()))


def expand(text):
    return text if isinstance(text, str) else ''.join(p if isinstance(p, str) else p[0] * p[1] for p in text['parts'])


def parser_controls(chk):
    """(id, input, compact contents, product override): the parser differential and alignment controls."""
    Tree, out = chk.Tree, []
    deep = {'parts': ['[x]\ny = ', ['[', 128], [']', 128], '\n']}
    wide = {'parts': ['[x]\ny = [', ['1,', 1100000], '1]\n']}
    for label, extra in (('recursion', deep), ('nodes', wide)):
        carrier = {'parts': ['[patch.crates-io]\na = { path = "repos/a" }\n'] + extra['parts']}
        t = Tree().repo('repos/a').crate('repos/a', 'a').file('.cargo/config.toml', expand(carrier))
        out.append(('control:toml-carrier-' + label, t.input(), {'.cargo/config.toml': carrier}, '.cargo/config.toml'))
        manifest = {'parts': ['[package]\nname = "a"\nversion = "1.0.0"\n'] + extra['parts']}
        t = Tree().repo('repos/a').file('repos/a/Cargo.toml', expand(manifest)).cargo_config([('a', '{ path = "repos/a" }')])
        out.append(('control:toml-manifest-' + label, t.input(), {'repos/a/Cargo.toml': manifest}, 'repos/a/Cargo.toml'))
    probes = [('depth-32', '[' * 31 + ']' * 31), ('depth-33', '[' * 32 + ']' * 32), ('integer-max', '18446744073709551615'),
              ('integer-over', '18446744073709551616'), ('integer-min', '-9223372036854775808'), ('integer-under', '-9223372036854775809'),
              ('negative-zero', '-0'), ('float', '1.0'), ('exponent', '1e2'), ('lone-surrogate', '"\\ud800"'), ('pair-surrogate', '"\\ud83d\\ude00"'),
              ('duplicate-key', '{"k": 1, "k": 2}'), ('nested-duplicate', '{"k": {"j": 1, "j": 1}}')]
    for label, value in probes:
        t = Tree().repo('repos/x').npm('repos/x', 'x').file('package.json', '{"private": true, "workspaces": ["repos/x"], "probe": %s}' % value)
        out.append(('control:json-carrier-' + label, t.input(), {}, None))
        t = Tree().repo('repos/x').file('repos/x/package.json', '{"name": "x", "version": "1.0.0", "probe": %s}' % value).workspaces(['repos/x'])
        out.append(('control:json-manifest-' + label, t.input(), {}, None))
    return out


def control_vector(ref, ctx, cid, inp, compact, override):
    real = vector(ref, ctx, cid, copy.deepcopy(inp))
    if override is not None:
        W = real['facts']['root']
        broken = copy.deepcopy(inp)
        broken['contents'][W + '/' + override] = '[unparseable\n'
        product = vector(ref, ctx, cid, broken)
        expected = product['expected']
        digest = hashlib.sha256(expand(inp['contents'][W + '/' + override]).encode()).hexdigest()
        for row in expected['declarations']:
            if row['path'] == override:
                row['contentSha256'] = digest
        for m in expected.get('members', []):
            for d in m['declaredBy']:
                if d.get('path') == override:
                    d['contentSha256'] = digest
        real = dict(real, referenceExpected=real['expected'], expected=expected)
    for r, text in compact.items():
        real['observation']['contents'][r] = text
    return real


class SpyContents(dict):
    """The `contents` side table, recording every path the reference asks it for (as B3-b0's checker does)."""

    def __init__(self, *a):
        super().__init__(*a)
        self.asked = []

    def get(self, key, default=None):
        self.asked.append(key)
        return super().get(key, default)


def vectors(arch, product, packages_root):
    scan = load('discovery_scan_vectors', product / SCAN_TOOL)
    scan.packages(product, packages_root)
    ref = load('member_reader_reference', arch / REF)
    chk = load('member_reader_reference_check', arch / CHECK)
    ctx = ref.Context(arch)
    pins = [dict(path=p, bytes=len((arch / p).read_bytes()), sha256=hashlib.sha256((arch / p).read_bytes()).hexdigest()) for p in (REF, CHECK, CASES)]
    cases, no_root, controls = [], [], []
    for c in json.loads((arch / CASES).read_bytes())['cases']:
        if c.get('model', 'discovery') != 'discovery':
            continue
        v = vector(ref, ctx, 'discovery:' + c['id'], copy.deepcopy(c['input']))
        (no_root.append('discovery:' + c['id']) if v is None else cases.append(v))
    for cid, inp, expect in chk.d15_cases():
        if 'raises' in expect:
            controls.append(cid)
            continue
        v = vector(ref, ctx, cid, copy.deepcopy(inp), expect.get('notRead', []) + expect.get('notObserved', []))
        (no_root.append(cid) if v is None else cases.append(v))
    for cid, inp, compact, override in parser_controls(chk):
        cases.append(control_vector(ref, ctx, cid, inp, compact, override))
    ids = [c['id'] for c in cases]
    require(len(ids) == len(set(ids)), 'duplicate case id')
    body = {'schemaVersion': 1,
            'standing': 'B3-b0 members-and-readers reference decisions for the D15 decision core (M3-B r9 items 19 to 24; unit B3-b2b1, '
                        'B3-b plan r2 amendment A2). Generated by tools/security/workspace_member_vectors.py over the reference checker\'s '
                        'own cases; design reference results over synthetic observations, not product qualification.',
            'sources': pins,
            'noSelectedRoot': no_root,
            'inputConsistencyControls': controls,
            'cases': cases}
    return (json.dumps(body, separators=(',', ':'), ensure_ascii=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True)
    parser.add_argument('--packages-root', type=Path, required=True)
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raw = vectors(args.architecture.resolve(strict=True), product, args.packages_root.resolve(strict=True))
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the B3-b0 reference at its bound bytes.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Workspace member vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
