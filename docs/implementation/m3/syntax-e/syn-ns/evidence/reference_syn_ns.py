"""Fixture oracle for SYN-NS r2: a small reference reading of the specification, over hand-written trees.

It is not a parser and runs none. A fixture gives source bytes and the visible tree tree-sitter yields for them
(leaf texts in source order; ranges are found by scanning the source). The oracle reads the closure documents'
own tables (bodies, atomicKinds, lineTerminators, commentKinds, directivePatterns, declares/containers, the role
tables) and applies:
  - the token law (L1) and the comment law (L2), for every row;
  - syntax subject chains for the body owner (declares rules marked container, and containers rules);
  - the statement-level control-flow law for JavaScript-family rows: lists and selection, identities, first, next,
    posttest entry, and edge rules 1 to 6, 11, 12, 14 and 15 (simple, block, branch, the loops, labeled, return,
    break, continue).
Not implemented here (E2c's fixtures cover them): L3 renaming, switch, try, throw, match, infinite loops, the Rust
graph, near-v1. A fixture that would need them is refused, not approximated.
"""
from __future__ import annotations

import re


class Node:
    def __init__(self, kind, named, field, children=None, text=None):
        self.kind, self.named, self.field = kind, named, field
        self.children, self.text = children or [], text
        self.start = self.end = None
        self.parent = None

    def named_children(self):
        return [c for c in self.children if c.named]

    def child_in(self, field):
        found = [c for c in self.children if c.field == field]
        return found[0] if found else None

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


def build(source: bytes, spec) -> Node:
    """spec: [kind, named, field, "leaf text"] or [kind, named, field, [child specs...]]."""
    pos = [0]

    def make(s, parent):
        kind, named, field, body = s
        node = Node(kind, named, field)
        node.parent = parent
        if isinstance(body, str):
            raw = body.encode('utf-8')
            at = source.index(raw, pos[0])
            assert source[pos[0]:at].strip(b' \t\n\r\x0b\x0c') == b'', (kind, body, source[pos[0]:at])
            node.start, node.end, node.text = at, at + len(raw), raw
            pos[0] = node.end
        else:
            node.children = [make(c, node) for c in body]
            node.start, node.end = node.children[0].start, node.children[-1].end
        return node

    root = make(spec, None)
    assert source[pos[0]:].strip(b' \t\n\r\x0b\x0c') == b'', 'unconsumed source'
    return root


def rows(doc):
    return {r['grammarId']: r for r in doc['rows']}


# ---------------------------------------------------------------- bodies and subjects
def bodies(root, nrow):
    out = []
    for node in root.walk():
        for rule in nrow['bodies']:
            if rule['kind'] != node.kind:
                continue
            body = node.child_in(rule['field']) if 'field' in rule else \
                next((c for c in node.named_children() if c.kind == rule['child']), None)
            if body is not None:
                out.append((node, body))
            break
    return out


def esc(text: bytes) -> str:
    return ''.join(chr(b) if 0x21 <= b <= 0x7E and chr(b) not in '%#/@:' else '%{:02X}'.format(b) for b in text)


def container_segment(node, nrow):
    for rule in nrow['declares']:
        if rule['kind'] != node.kind or not rule.get('container'):
            continue
        if rule.get('when') == 'has-field' and node.child_in(rule['name']['field']) is None:
            continue
        name = node.child_in(rule['name']['field'])
        return rule['declarationKind'], name.text
    for rule in nrow['containers']:
        if rule['kind'] == node.kind:
            return rule['tag'], b''
    return None


def owner_chain(owner, nrow, root):
    """The owner's full subject chain: its container chain (strict ancestors), then its own segment."""
    def chain_of(node):
        path, cur = [], node.parent
        while cur is not None:
            if container_segment(cur, nrow):
                path.append(cur)
            cur = cur.parent
        return list(reversed(path))
    segments = []
    for node in chain_of(owner) + [owner]:
        tag, name = container_segment(node, nrow)
        parent_chain = chain_of(node)
        earlier = 0
        for other in root.walk():
            if other is node:
                break
            seg = container_segment(other, nrow)
            if seg and seg == (tag, name) and chain_of(other) == parent_chain:
                earlier += 1
        segments.append('{}:{}@{}'.format(tag, esc(name), earlier))
    return segments


# ---------------------------------------------------------------- tokens (L1, L2)
WS = b'\t\x0b\x0c '
LT = '\n\r  '


def tokens(source, body, lrow, level):
    atomic = set(lrow['atomicKinds'])
    leaves = []

    def visit(n):
        if n.kind in atomic or not n.children:
            if n.end > n.start:
                leaves.append(n)
            return
        for c in n.children:
            visit(c)
    visit(body)
    out, at = [], body.start
    for n in leaves + [None]:
        gap = source[at:(n.start if n else body.end)]
        if gap:
            if all(b in WS for b in gap):
                pass
            elif all(b in WS + b'\n\r' for b in gap):
                if lrow['lineTerminators'] == 'significant':
                    out.append(('opensip:line-break', b'\n', None))
            else:
                out.append(('opensip:gap', gap, None))
        if n is None:
            break
        out.append((('n:' if n.named else 'a:') + n.kind, n.text if n.text is not None else source[n.start:n.end], n))
        at = n.end
    if level == 'L1-lexical':
        return [(k, v) for k, v, _ in out]
    kept = []
    for k, v, n in out:
        if n is not None and n.kind in lrow['commentKinds']:
            text = v.decode('utf-8')
            directive = any(re.match(p, text) for p in lrow.get('directivePatterns', []))
            if lrow['lineTerminators'] == 'insignificant':
                directive = directive or any(c.kind in lrow.get('docMarkerKinds', []) for c in n.children)
            if directive:
                kept.append((k, v))
            elif lrow['lineTerminators'] == 'significant' and any(c in text for c in LT):
                kept.append(('opensip:line-break', b'\n'))
            continue
        kept.append((k, v))
    merged = []
    for tok in kept:
        if tok[0] == 'opensip:line-break' and merged and merged[-1][0] == 'opensip:line-break':
            continue
        merged.append(tok)
    return merged


# ---------------------------------------------------------------- control flow (JavaScript family)
class CF:
    def __init__(self, source, root, owner, body, nrow):
        self.src, self.root, self.owner, self.body = source, root, owner, body
        cf = nrow['controlFlow']
        self.lists = {r['kind']: r.get('field') for r in cf['statementLists']}
        self.non = set(cf['nonStatements'])
        self.roles = {r['kind']: r for r in cf['roles']}
        self.body_kinds = {(r['kind'], r.get('field')) for r in nrow['bodies']}
        self.prefix = owner_chain(owner, nrow, root)
        self.edges = set()
        self.ident = {}
        self.parent_flow = {}
        self.list_of = {}      # flow node -> (list nodes, owner flow node or None, list key)
        self.selected = {}     # flow node -> {selector: [list] or node}

    def List(self, node):
        field = self.lists[node.kind]
        return [c for c in node.named_children() if c.kind not in self.non and (field is None or c.field == field)]

    def role(self, n):
        return self.roles.get(n.kind)

    def select(self, s):
        """{name: ('list', [flow nodes]) or ('single', node)} for the role-selected children of flow node s."""
        r = self.role(s)
        out = {}
        if r is None:
            return out
        def pick(name, node):
            if node is None:
                return
            if (node.parent.kind, node.field) in self.body_kinds:
                return     # opacity
            if node.kind in self.lists:
                out[name] = ('list', self.List(node))
            else:
                out[name] = ('single', node)
        kind = r['role']
        if kind == 'branch':
            pick('consequence', s.child_in(r['consequence']))
            alt = s.child_in(r['alternative'])
            if alt is not None and alt.kind == r['alternativeChild']:
                alt = next(c for c in alt.named_children() if c.kind not in self.non)
            pick('alternative', alt)
        elif kind in ('pretest-loop', 'posttest-loop', 'infinite-loop', 'labeled'):
            pick('body', s.child_in(r['body']))
        elif kind == 'block':
            if s.kind in self.lists:
                out['list'] = ('list', self.List(s))
        elif kind in ('return', 'break', 'continue'):
            pass
        else:
            raise NotImplementedError('role ' + kind + ' is outside this oracle')
        return out

    def collect(self):
        order = []

        def place(nodes, owner, name):
            for i, n in enumerate(nodes):
                self.parent_flow[n] = owner
                self.list_of[n] = (nodes, i, owner, name)
                order.append(n)
                sel = self.select(n)
                self.selected[n] = sel
                for child_name, (form, val) in sel.items():
                    place(val if form == 'list' else [val], n, child_name)
        top = self.List(self.body) if self.body.kind in self.lists else []
        place(top, None, 'body')
        self.order = order
        for n in order:
            chain, cur = [], n
            while cur is not None:
                chain.append(cur)
                cur = self.parent_flow[cur]
            chain.reverse()
            segs = []
            for depth, m in enumerate(chain):
                same = [o for o in order[:order.index(m)] if o.kind == m.kind
                        and self._enclosing(o) == self._enclosing(m)]
                segs.append('stmt:{}@{}'.format(esc(m.kind.encode()), len(same)))
            self.ident[n] = segs

    def _enclosing(self, n):
        out, cur = [], self.parent_flow[n]
        while cur is not None:
            out.append(cur)
            cur = self.parent_flow[cur]
        return out

    def subject(self, n, path):
        tail = {'entry': ['entry:@0'], 'exit': ['exit:@0']}.get(n) if isinstance(n, str) else self.ident[n]
        return 'syntax:{}#{}'.format(esc(path.encode()), '/'.join(self.prefix + tail))

    # first / next / enter --------------------------------------------------------------------------------
    def first_of(self, sel_entry, cont_owner, name):
        form, val = sel_entry
        if form == 'single':
            return val
        return val[0] if val else self.continuation(cont_owner, name)

    def continuation(self, owner, name):
        """(target, edgeKind or None) reached when the list `name` of flow node `owner` completes."""
        if owner is None:
            return ('exit', None)
        r = self.role(owner)['role']
        if r in ('pretest-loop', 'posttest-loop', 'infinite-loop') and name == 'body':
            return (owner, 'loop')
        return self.next(owner)

    def next(self, s):
        nodes, i, owner, name = self.list_of[s]
        if i + 1 < len(nodes):
            return (nodes[i + 1], None)
        return self.continuation(owner, name)

    def enter(self, x):
        if isinstance(x, str):
            return x
        r = self.role(x)
        if r is not None and r['role'] == 'posttest-loop':
            sel = self.selected[x].get('body')
            if sel is not None and (sel[0] == 'single' or sel[1]):
                return self.enter(sel[1] if sel[0] == 'single' else sel[1][0])
        return x

    def target(self, t):
        """Resolve a first() result that may be a (continuation, kind) pair."""
        return t if isinstance(t, tuple) else (t, None)

    def add(self, a, b, kind, raw=False):
        b = b if raw else self.enter(b)
        self.edges.add((a, b, kind))

    def build_edges(self):
        top = self.List(self.body) if self.body.kind in self.lists else []
        if top:
            self.add('entry', top[0], 'fallthrough')
        else:
            self.add('entry', 'exit', 'fallthrough')
        for s in self.order:
            r = self.role(s)
            kind = r['role'] if r else 'simple'
            sel = self.selected[s]
            if kind == 'simple':
                tgt, k = self.next(s)
                self.add(s, tgt, k or 'fallthrough', raw=(k == 'loop'))
            elif kind == 'block':
                lst = sel.get('list', ('list', []))[1]
                if lst:
                    self.add(s, lst[0], 'fallthrough')
                else:
                    tgt, k = self.next(s)
                    self.add(s, tgt, k or 'fallthrough', raw=(k == 'loop'))
            elif kind == 'branch':
                t, k = self.target(self.first_of(sel['consequence'], s, 'consequence'))
                self.add(s, t, 'branch-true', raw=(k == 'loop'))
                if 'alternative' in sel:
                    t, k = self.target(self.first_of(sel['alternative'], s, 'alternative'))
                else:
                    t, k = self.next(s)
                self.add(s, t, 'branch-false', raw=(k == 'loop'))
            elif kind in ('pretest-loop', 'posttest-loop'):
                b = sel.get('body')
                if b is None or (b[0] == 'list' and not b[1]):
                    self.add(s, s, 'loop', raw=True)
                else:
                    self.add(s, b[1] if b[0] == 'single' else b[1][0], 'branch-true')
                tgt, k = self.next(s)
                self.add(s, tgt, 'branch-false', raw=(k == 'loop'))
            elif kind == 'labeled':
                t, k = self.target(self.first_of(sel['body'], s, 'body'))
                self.add(s, t, 'fallthrough', raw=(k == 'loop'))
            elif kind == 'return':
                self.add(s, 'exit', 'return')
            elif kind == 'continue':
                assert s.child_in(r['label']) is None, 'labels are outside this oracle'
                loop = next(m for m in self._enclosing(s)
                            if self.role(m) and self.role(m)['role'].endswith('-loop'))
                self.add(s, loop, 'loop', raw=True)
            elif kind == 'break':
                assert s.child_in(r['label']) is None, 'labels are outside this oracle'
                loop = next(m for m in self._enclosing(s)
                            if self.role(m) and self.role(m)['role'].endswith('-loop'))
                tgt, k = self.next(loop)
                self.add(s, tgt, 'fallthrough', raw=(k == 'loop'))
            else:
                raise NotImplementedError(kind)

    def graph(self, path):
        self.collect()
        self.build_edges()
        name = lambda x: self.subject(x, path)
        return {'nodes': sorted({name('entry'), name('exit')} | {name(n) for n in self.order}),
                'edges': sorted([name(a), name(b), k] for a, b, k in self.edges)}
