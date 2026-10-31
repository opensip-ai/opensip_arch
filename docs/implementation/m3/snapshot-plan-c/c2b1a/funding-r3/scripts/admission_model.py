#!/usr/bin/env python3
"""C2b-1a funding derivation r4: the reference model of the per-schema admission terms.

r3 (REVIEW-r2 RF-1, NBO-1; REVIEW-r1 RF-1): the measured boundary is explicit. r4 (REVIEW-r3 RF-1,
NBO-1): every search iteration is ONE explicit three-way byte comparison (`compare_keys`), counted
with the bytes it reads; the retained digest is supplied to the census from outside the boundary.

  OUTSIDE the boundary (built before the census, never counted):
    - the accounted value representation `AV`: Rust's `Value` (canonical.rs:143-148), whose
      `String::len`, `Vec::len` and `BTreeMap::len` are O(1) and whose object members iterate
      in UTF-8 byte order (canonical.rs:549-550). C2b-1a holds the parsed value before pricing
      (LD-F-3); the reference builds `AV` from the Python value in the same shape;
    - the static price table: `Slot`s with their sorted declared-key lists, per-key member
      tables, `Inv` entries (RESOLVE, DISPATCH, literal statistics, ORDER_PARSE), the `ordered`
      arm table and ROW_CLONE. All are functions of the pinned documents only (F2).
    - C2b-1a's retained blob map (`Store`): digest -> actual retained length beta(d), and the
      digest itself, which the fetch is given (closure.rs:85-95): `Record` receives it as `key`.

  INSIDE the boundary (`census`, `scan`, `slot_lookup`, `Store.lookup`, `compare_keys`): every
  element is charged BEFORE its work from O(1)-available sizes (M1a C1): a node's kind and its
  string's byte length, the slot's static m and K, a member key's byte length, the store's
  population. Each loop counts its own steps where it runs: `scan` counts per scalar inside its
  loop; `slot_lookup` and `Store.lookup` are explicit binary searches whose every iteration is
  ONE three-way comparison (`compare_keys`, as `Ord::cmp` on byte slices), counted with the bytes
  it actually reads of both operands; no other relational operation on keys runs inside the
  boundary (the `observe_keys` control checks that); the per-invocation, per-member, per-item
  and per-UNIQUE loops count in their bodies. `Census.check()` holds counted <= charged. A `budget` makes `charge` raise
  `Exhausted` before the element's work (the exhaustion control, scripts/exhaustion.py).
  Every rule is a total function of per-node statistics (r2, RF-2). The depth gate is the
  encoder's: a container at container depth 32 refuses (canonical.rs:536; NBO-1).

Every premise is read at the pinned product commit through `git show`, never from a working tree.
Usage: admission_model.py PRODUCT_CHECKOUT
"""
import json, re, subprocess, sys, hashlib

PIN = '98159381648b0ddad022f1c7fffe678ce0e27208'
PRODUCT = sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip'


def src(path):
    return subprocess.run(['git', '-C', PRODUCT, 'show', f'{PIN}:{path}'],
                          capture_output=True, check=True).stdout


# ---------------------------------------------------------------- WorkCost and the split price

class C(tuple):
    """WorkCost {objects, edges, bytes}."""
    def __new__(cls, o=0, e=0, b=0):
        return tuple.__new__(cls, (o, e, b))
    def __add__(self, x):
        return C(self[0] + x[0], self[1] + x[1], self[2] + x[2])
    def __mul__(self, n):
        return C(self[0] * n, self[1] * n, self[2] * n)
    __rmul__ = __mul__


Z = C()


class P(tuple):
    """A price split as C9's `AdmissionPrice`: (allocations, passes). F8 holds measured storage
    to `.alloc`; the ledger charges `.total()`."""
    def __new__(cls, a=Z, p=Z):
        return tuple.__new__(cls, (C(*a), C(*p)))
    alloc = property(lambda s: s[0])
    passes = property(lambda s: s[1])
    def __add__(self, x):
        return P(self[0] + x[0], self[1] + x[1])
    def __mul__(self, n):
        return P(self[0] * n, self[1] * n)
    __rmul__ = __mul__
    def total(self):
        return self[0] + self[1]


PZ = P()
def A(c): return P(c, Z)                                       # allocation side
def S_(c): return P(Z, c)                                      # pass side

RECORD = 128                      # security custody/discovery_walk.rs:87, `owned` :89-95
STRING, VALUE = 24, 32            # node_modules_layout_tests.rs:1893-1896
LEAF = 16 + 11 * (STRING + VALUE)  # canonical.rs meter_prices LEAF_NODE
EDGES12 = 12 * 8                  # canonical.rs meter_prices INTERNAL_EDGES
STR_SLOT, VEC_SLOT = 16, 24
MAX_DEPTH = 32                    # canonical.rs:6; the gate is :536 (a container at depth 32 refuses)


def bitlen(n): return n.bit_length()
def log2(n): return max(n, 1).bit_length() - 1
def owned(b): return A(C(1, 0, b + RECORD))
def pss(k, b): return S_(C(0, k, b))
def tree_search(pop): return 11 * bitlen(pop)
def map_search(pop): return min(pop, tree_search(pop))
def search(m, q):
    k = map_search(m)
    return pss(k, 2 * k * (q + 1))
def digest_cost(n): return S_(C(1, 1, 32 + RECORD + n))       # C9 holds it on the pass side
def btree_height(m): return 1 + bitlen(m)
def btree_insert(members, key, entry):
    """snapshot.rs:112-130 (L2); nodes and their bytes on the allocation side, the search and
    move work on the pass side (C9's split, snapshot_admission.rs:458-470)."""
    h = btree_height(members)
    node = 16 + 11 * entry + EDGES12
    return P(C(h + 1, 0, (h + 1) * (node + RECORD)), C(0, 12 * h + 1, 22 * h * (key + 1) + 21 * h * entry))
def growth(n, size):
    if n == 0:
        return PZ
    minimum = 8 if size == 1 else 4
    ev = 2 + log2(n)
    return A(C(ev, ev, 3 * max(minimum, 2 * n) * size + ev * RECORD))
def formatted(n): return owned(2 * n) + growth(n, 1)


# meter prices (canonical.rs:139-258): held whole on the allocation side (C9 :571-576)
def p_entry(n): return A(C(0, 1, 16 * n))
def p_value(): return A(C(0, 1, 0))
def p_height(m): return 1 + bitlen(m)
def p_search(m, k):
    h = p_height(m)
    return A(C(0, 11 * h, 22 * h * (k + 1)))
def p_insert(m, k):
    h = p_height(m)
    return A(C(h + 1, 12 * h + 1, (h + 1) * (LEAF + EDGES12) + 22 * h * (k + 1) + 21 * h * (STRING + VALUE)))
def p_string(n):
    if n == 0:
        return PZ
    g = 2 + log2(n)
    return A(C(g, g, max(8 * n, 32)))
def p_array(count):
    total, cap = Z, 0
    while cap < count:
        nxt = max(2 * cap, cap + 1, 4)
        total = total + C(1, 1, nxt * VALUE + cap * VALUE)
        cap = nxt
    return A(total)


# ---------------------------------------------------------------- the accounted value (outside)

def is_int(x): return isinstance(x, int) and not isinstance(x, bool)
def kind(x):
    if x is None: return 'null'
    if isinstance(x, bool): return 'boolean'
    if is_int(x): return 'integer'
    if isinstance(x, str): return 'string'
    if isinstance(x, list): return 'array'
    return 'object'


class AV:
    """The accounted value: what Rust's `Value` supplies in O(1) and the census may read before
    charging. A string's byte length `n` (`String::len`), a container's length `size`
    (`Vec::len` / `BTreeMap::len`), and an object's members in UTF-8 byte order, each with its
    key's byte length. Built OUTSIDE the measured boundary from the value C2b-1a already holds
    (LD-F-3); building it is not census work and is never counted."""
    __slots__ = ('kind', 'raw', 'n', 'size', 'members', 'items')
    def __init__(self, x):
        self.kind = kind(x); self.raw = x; self.n = 0; self.size = 0; self.members = None; self.items = None
        if self.kind == 'string':
            self.n = len(x.encode('utf-8'))
        elif self.kind == 'array':
            self.items = [AV(v) for v in x]; self.size = len(x)
        elif self.kind == 'object':
            self.members = sorted(((k.encode('utf-8'), k, AV(v)) for k, v in x.items()), key=lambda t: t[0])
            self.size = len(x)


ESC = {'"': 2, '\\': 2, '\b': 2, '\f': 2, '\n': 2, '\r': 2, '\t': 2}
def scan(s, c=None):
    """One pass over a string's scalars (canonical.rs:496-522 for the encoded length): decoded
    bytes, canonical encoded length, '/'-separated parts and the scalar count. INSIDE the
    boundary when `c` is given: the scan is one counted element, and each scalar counts its
    own bytes inside the loop, read once (decode) and classified once (escape class and
    separator): 2b bytes for a scalar of b bytes. There is no second pass (no `count('/')`)."""
    if c is not None:
        c.scan_begin()
    n = enc = parts = chars = 0
    for ch in s:
        b = len(ch.encode('utf-8'))
        if c is not None:
            c.step(0, 2 * b)
        n += b
        enc += ESC.get(ch, 6 if ord(ch) < 0x20 else b)
        if ch == '/':
            parts += 1
        chars += 1
    return n, enc + 2, parts + 1, chars


class St:
    """A value's statistics, returned by the census to its parent: N values, B walk bytes (every
    string and key byte, 16 per integer, 1 per literal), I integers, L canonical length, the
    kind, and for strings n / S / chars; `keys` is the container's length; `path` is (n, S) of an
    object's string `path` member, for `ordered`."""
    __slots__ = ('kind', 'N', 'B', 'I', 'L', 'n', 'S', 'chars', 'keys', 'path')


def literal_stats(x):
    """Statistics of a schema literal (`const`, `enum` candidate, order annotation): static,
    precomputed into the price table and pinned by F2. OUTSIDE the boundary (uncounted scan)."""
    st = St(); st.kind = kind(x); st.path = None; st.n = st.S = st.chars = 0; st.keys = 0
    if isinstance(x, str):
        st.n, enc, st.S, st.chars = scan(x)
        st.N, st.B, st.I, st.L = 1, st.n, 0, enc
    elif is_int(x):
        st.N, st.B, st.I, st.L = 1, 16, 1, len(str(x))
    elif x is None or isinstance(x, bool):
        st.N, st.B, st.I, st.L = 1, 1, 0, len(json.dumps(x))
    elif isinstance(x, list):
        kids = [literal_stats(v) for v in x]
        st.keys = len(x)
        st.N = 1 + sum(k.N for k in kids); st.B = sum(k.B for k in kids); st.I = sum(k.I for k in kids)
        st.L = 2 + sum(k.L for k in kids) + max(len(x) - 1, 0)
    else:
        st.keys = len(x)
        st.N, st.B, st.I, st.L = 1, 0, 0, 2 + max(len(x) - 1, 0)
        for k, v in x.items():
            kv = literal_stats(v); kn, kenc, _, _ = scan(k)
            st.N += kv.N; st.B += kn + kv.B; st.I += kv.I; st.L += kenc + 1 + kv.L
    return st


def WALK(st): return pss(st.N, st.B)                           # schema.rs Meter::value :29-50
def EQ(a, b): return pss(a.N + b.N, a.B + b.B)                 # derived PartialEq, both operands
def ENC(st):
    """canonical.rs encode (:477-562): the output Vec (P1 to L), one decimal temporary per
    integer, one pass visiting each value and reading/writing each output byte."""
    return growth(st.L, 1) + st.I * growth(20, 1) + pss(st.N, 2 * st.L)


FRAME_PREFIX = len(b'opensip.product.v1\0')


def HASH(domain, st):
    F = FRAME_PREFIX + len(domain) + 1 + 8 + st.L
    return pss(1, len(domain)) + ENC(st) + growth(F, 1) + pss(1, F + st.L) + digest_cost(F)


def IDENT(prefix):
    n = len(prefix) + 1 + 64
    return owned(64) + formatted(n) + pss(32, 32 + 64) + pss(1, 2 * n)


# ---------------------------------------------------------------- the registry premises

REG = src('crates/identity/src/schema_registry.rs').decode()
PINS = re.findall(r'id: "([^"]+)",\s*path: "([^"]+)",\s*bytes: (\d+)', REG)
D = len(PINS)
POPULATION = sum(1 + int(b) for _, _, b in PINS)
ALIASES = re.findall(r'\(\s*"([^"]+)",\s*"([^"]+)",?\s*\)',
                     re.search(r'DOCUMENT_ALIASES[^=]*=\s*&\[(.*?)\];', REG, re.S).group(1))
DOCS = {i: json.loads(src(p)) for i, p, _ in PINS}
IDENTITY = 'urn:opensip:product-v1:identity:v3'
NATIVE = 'urn:opensip:product-v1:native:evidence-schemas:v2'
NATIVE_DOC = 'native/native-evidence.schemas.v2.json'
assert dict(ALIASES)[NATIVE_DOC] == NATIVE

PAT = src('crates/identity/src/schema_patterns.rs').decode()
def rust_strings(block):
    return [m.group(2) for m in re.finditer(r'r(#+)"(.*?)"\1', block, re.S)]
_TB = re.search(r'const TABLE: &\[\(&str, Kind\)\] = &\[(.*?)\n\];', PAT, re.S).group(1)
TABLE = rust_strings(_TB)
TABLE_KINDS = re.findall(r'Kind::(\w+)', _TB)
FORMS = rust_strings(re.search(r'const FORMS: &\[&str\] = &\[(.*?)\];', PAT, re.S).group(1))
assert len(TABLE) == len(TABLE_KINDS)
OWNER_TESTS = ['opensip.product.symbol-census.1', NATIVE,
               'opensip.product.occupancy-companion.1', 'opensip.product.relation-payload.2']
assert all(o in src('crates/identity/src/schema.rs').decode() for o in OWNER_TESTS)
DOT = r'(^|/)\.\.?(/|$)'
SECURITY = r'^security.repo-execution-grants.v2:[0-9a-f]{64}(?![\s\S])'
EMPTY_FORMS = [FORMS[1], FORMS[2]]


def resolve_pointer(ref, owner):
    i, _, frag = ref.partition('#')
    i = i or owner
    v, parts = DOCS[i], []
    if frag:
        for part in frag[1:].split('/'):
            parts.append((part, len(v)))
            v = v[part.replace('~1', '/').replace('~0', '~')]
    return v, i, parts


def RESOLVE(ref, owner):
    """schema.rs resolve (:267-298). Static per reference: precomputed into the table (F2)."""
    target, doc, parts = resolve_pointer(ref, owner)
    r = len(ref)
    cost = pss(1, r) + search(D, len(doc)) + pss(2, 2 * r)
    for part, members in parts:
        cost = cost + pss(1, len(part)) + p_string(len(part)) + search(members, len(part))
    return target, doc, cost


def dispatch(owner, pattern):
    """schema.rs pattern_matches (:237-265) and the owner's selection. Static per pattern."""
    cost = pss(len(OWNER_TESTS), sum(len(owner) + len(o) for o in OWNER_TESTS))
    def legacy(cost):
        i = TABLE.index(pattern)
        return cost + pss(i + 1, sum(len(pattern) + len(t) for t in TABLE[:i + 1])), TABLE_KINDS[i]
    if owner == NATIVE:
        f = FORMS.index(pattern)
        cost = cost + pss(f + 1, sum(len(pattern) + len(t) for t in FORMS[:f + 1]))
        cost = cost + pss(2, 2 * len(pattern) + sum(len(t) for t in EMPTY_FORMS))
        if pattern in EMPTY_FORMS:
            return cost, 'NegativePathNative'
        cost = cost + pss(2, 2 * len(pattern) + len(DOT) + len(SECURITY))
        if pattern == DOT:
            return cost, 'DotNative'
        return legacy(cost)
    return legacy(cost)


HEX_PREFIX = {r'^[0-9a-f]{64}(?![\s\S])': 0, r'^closure2:[0-9a-f]{64}(?![\s\S])': len('closure2:'),
              r'^sha256:[0-9a-f]{64}(?![\s\S])': len('sha256:'), r'^prj1-[0-9a-f]{64}(?![\s\S])': len('prj1-')}


def MATCH(kind_, pattern, st):
    """The matcher passes (schema_patterns.rs :272-336, :497-505); none allocates (:2)."""
    n, S = st.n, st.S
    if kind_ == 'Segments255': return pss(2 + 2 * S, 3 * n)
    if kind_ == 'DotSegment': return pss(1 + S, n + 6 * S + 2)
    if kind_ == 'NegativePathNative': return pss(2 + S, 2 * n + 6 * S + 2)
    if kind_ == 'DotNative': return pss(1 + S, n + 6 * S)
    if kind_ == 'Hex': return pss(2, 2 * HEX_PREFIX[pattern] + 64)
    raise ValueError(f'unpriced matcher {kind_}')


ORDER_ARMS, ORDER_ARM = 11, 16


def order_kind(ann):
    if isinstance(ann, str):
        if ann in ('path', 'ruleId', 'waiverId'): return ('fields', [ann])
        if ann == 'predicate': return ('fields', ['ruleId', 'subjectId', 'predicateId'])
        return (ann, None)
    return ('fields', list(ann['by']))


def ORDER_PARSE(ann):
    """ArrayOrder::parse (descriptors.rs:191-232). Static per annotation."""
    if isinstance(ann, str):
        cost = pss(ORDER_ARMS, ORDER_ARMS * 2 * (ORDER_ARM + 1))
        k, fields = order_kind(ann)
        if k == 'fields':
            cost = cost + owned(STRING * len(fields)) + sum((owned(len(f)) for f in fields), PZ)
        return cost
    fields = ann['by']
    cost = pss(1, 0) + search(len(ann), 2) + owned(STRING * len(fields))
    for i, f in enumerate(fields):
        cost = cost + pss(1, 0) + btree_insert(i, len(f), 8) + owned(len(f))
    return cost


def tuple_key(nf):
    return owned(4 * STR_SLOT) if nf <= 4 else owned(4 * STR_SLOT) + growth(nf, STR_SLOT)


def order_item(ok, item, prev_key):
    """ArrayOrder::verify (descriptors.rs:243-314), one item, from the annotation's precomputed
    kind `ok` = order_kind(ann): total over every item shape. The key's bytes are bounded by the
    item's walk bytes plus one per field (r2: a field's bytes are among the item's string bytes;
    a missing or non-string field exits, :257-267)."""
    k, fields = ok
    if k == 'sequence':
        return PZ, None
    if k == 'utf8':
        cost, key = pss(1, 0), item.B
    elif k == 'fields':
        cost = tuple_key(len(fields))
        for f in fields:
            cost = cost + search(item.keys if item.kind == 'object' else 0, len(f)) + pss(1, 0)
        key = item.B + len(fields)
    elif k in ('canonical-set', 'canonical-order'):
        cost, key = ENC(item), item.L
    else:
        cost, key = pss(1, 16), 16
    if prev_key is not None:
        cost = cost + pss(1, prev_key + key + 2)
    return cost, key


def order_tail(ann):
    return pss(1, 0) if order_kind(ann)[0] == 'sequence' else PZ


# ---------------------------------------------------------------- the static price table (outside)

OUTSIDE = ('patternProperties', 'propertyNames', 'prefixItems', 'contains', 'allOf', 'anyOf', 'if', 'then', 'else')


def same_value(t, owner):
    """The invocations one `evaluate(t, v)` makes on v itself: t, its `$ref` target, its `oneOf`
    rules and its `not` rule, recursively (schema.rs :517-578)."""
    out = [(t, owner)]
    if isinstance(t, dict):
        for k in t:
            if k in OUTSIDE:
                raise ValueError(f'keyword {k} is outside this derivation')
        if '$ref' in t:
            tgt, doc, _ = resolve_pointer(t['$ref'], owner)
            out += same_value(tgt, doc)
        for rule in t.get('oneOf', []):
            out += same_value(rule, owner)
        if 'not' in t:
            out += same_value(t['not'], owner)
    return out


class Inv:
    """One evaluation-table invocation (t, owner) with its static parts precomputed OUTSIDE the
    boundary (F2): its keyword count m and query search S, the nine fixed lookups, RESOLVE of its
    `$ref`, its literal statistics (`const`, `enum`), its pattern's DISPATCH and matcher kind, its
    order annotation's ORDER_PARSE and kind, its required keys' byte lengths, its `properties`
    population and whether `additionalProperties` and `uniqueItems` are present."""
    __slots__ = ('t', 'owner', 'is_bool', 'm', 'S', 'fixed', 'literals', 'pattern', 'order', 'required',
                 'props_pop', 'unique', 'item_lookup')
    def __init__(self, t, owner):
        self.t, self.owner = t, owner
        self.is_bool = isinstance(t, bool)
        self.literals, self.pattern, self.order, self.required = [], None, None, []
        self.props_pop, self.unique = None, False
        if self.is_bool:
            self.m, self.S, self.fixed, self.item_lookup = 0, PZ, pss(1, 0), PZ
            return
        m = len(t); self.m = m; S = search(m, 20); self.S = S
        fixed = pss(1, 0) + 9 * S
        if '$ref' in t:
            fixed = fixed + RESOLVE(t['$ref'], owner)[2]
        if 'const' in t:
            self.literals.append(literal_stats(t['const']))
        if 'enum' in t:
            self.literals += [literal_stats(v) for v in t['enum']]
        if 'type' in t:
            fixed = fixed + (pss(1, 16) if isinstance(t['type'], str) else pss(len(t['type']), 16 * len(t['type'])))
        if 'oneOf' in t:
            fixed = fixed + pss(len(t['oneOf']), 0)
        self.fixed = fixed
        if 'pattern' in t:
            d, k = dispatch(owner, t['pattern'])
            self.pattern = (d, k, t['pattern'])
        if 'x-opensip-order' in t:
            ann = t['x-opensip-order']
            self.order = (order_kind(ann), WALK(literal_stats(ann)) + ORDER_PARSE(ann) + order_tail(ann))
        self.required = [len(r.encode()) for r in t.get('required', [])]
        props = t.get('properties')
        self.props_pop = len(props) if props is not None else None
        self.unique = t.get('uniqueItems') is True
        self.item_lookup = pss(1, 0) + S                         # schema.rs :613-621, per item
    def member(self, kn, declared):
        """This invocation's work for one object member of key length kn (schema.rs:674-707)."""
        if self.is_bool:
            return PZ
        cost = pss(1, 0) + self.S
        if self.props_pop is not None:
            cost = cost + search(self.props_pop, kn)
        if not declared:
            cost = cost + self.S
        return cost


class Slot:
    """The invocations evaluating a value at one schema position, with its children prebuilt:
    the sorted declared-key list (bytes), the child slot and per-invocation member table for
    each declared key and for an undeclared key ('*'), and the items slot. Built once from the
    pinned document, OUTSIDE the boundary (the price table; F2 regenerates it). The census only
    reads it: `slot_lookup` is the one counted operation on it."""
    __slots__ = ('invs', 'm', 'K', 'keys', 'key_bytes', 'children', 'tables', 'star', 'star_table',
                 'item_slot', 'orders', 'uniques', 'raw')
    def __init__(self, invs):
        self.raw = invs
        self.invs = [Inv(t, o) for t, o in invs]
        self.m = len(invs)
        objs = [(t, o) for t, o in invs if isinstance(t, dict)]
        self.keys = sorted({k for t, _ in objs for k in t.get('properties', {})}, key=str.encode)
        self.key_bytes = [k.encode('utf-8') for k in self.keys]
        self.K = len(self.keys)
        self.orders = [inv for inv in self.invs if inv.order is not None]
        self.uniques = [inv for inv in self.invs if inv.unique]
        self.children, self.tables, self.star, self.star_table, self.item_slot = [], [], None, None, None
    def build(self, depth):
        """Prebuild the children to the census's maximum depth (nothing deeper is ever visited)."""
        def child_for(k):
            invs, table = [], []
            for inv in self.invs:
                t = inv.t
                declared = False
                if isinstance(t, dict):
                    props = t.get('properties', {})
                    if k is not None and k in props:
                        invs += same_value(props[k], inv.owner); declared = True
                    elif 'additionalProperties' in t:
                        invs += same_value(t['additionalProperties'], inv.owner)
                table.append((inv, declared))
            return make_slot(invs, depth + 1), table
        for k in self.keys:
            child, table = child_for(k)
            self.children.append(child); self.tables.append(table)
        self.star, self.star_table = child_for(None)
        items = []
        for inv in self.invs:
            if isinstance(inv.t, dict) and 'items' in inv.t:
                items += same_value(inv.t['items'], inv.owner)
        self.item_slot = make_slot(items, depth + 1)


EMPTY = Slot([])
EMPTY.star, EMPTY.star_table, EMPTY.item_slot = EMPTY, [], EMPTY


def make_slot(invs, depth=0):
    if not invs or depth > MAX_DEPTH:
        return EMPTY
    s = Slot(invs)
    s.build(depth)
    return s


_ROOTS = {}


def root_slot(doc, selector):
    """The table for one entry, built once (outside the boundary)."""
    if (doc, selector) not in _ROOTS:
        t, o, _ = resolve_pointer('#' + selector, doc)
        _ROOTS[(doc, selector)] = make_slot(same_value(t, o))
    return _ROOTS[(doc, selector)]


def tau_size(doc, selector):
    """The table's size (max per-value multiplicity mu, invocations, slots) over every slot
    reachable from the entry's root."""
    seen, sizes = set(), []
    def go(slot):
        if id(slot) in seen or slot is EMPTY:
            return
        seen.add(id(slot)); sizes.append(slot.m)
        for ch in slot.children:
            go(ch)
        go(slot.star); go(slot.item_slot)
    go(root_slot(doc, selector))
    return max(sizes), sum(sizes), len(sizes)


ORDERED_ANN = {'allowedScopes': 'sequence', 'sourceInventory': 'path', 'tree': 'path', 'blobs': 'path',
               'requires': 'numeric', 'owner-source-set': {'by': ['ownerKey']}, 'stages': 'ordinal',
               'predicateProofs': 'predicate', 'ruleResults': 'ruleId'}


def _ordered_arm(name):
    """`ordered`'s array arm (descriptors.rs:667-707): its static part, per member name."""
    cost = pss(ORDER_ARMS, ORDER_ARMS * 2 * (ORDER_ARM + 1))
    ann = ORDERED_ANN.get(name, 'canonical-set')
    if name == 'owner-source-set':
        cost = cost + owned(LEAF) + owned(2) + owned(VALUE) + owned(len('ownerKey'))
    else:
        cost = cost + owned(len(ann))
    return cost + ORDER_PARSE(ann) + order_tail(ann), order_kind(ann)


ORDERED_ARMS = {n: _ordered_arm(n) for n in ORDERED_ANN}
ORDERED_DEFAULT = _ordered_arm('*')


# ---------------------------------------------------------------- the fused census (inside)

class Exhausted(Exception):
    """Raised by `Census.charge` when the element's charge would exceed the budget, BEFORE the
    element's work (so no scan, lookup or visit of that element begins)."""


class PriceUnavailable(Exception):
    """The fail-closed gates: a container at depth 32 (NBO-1), a retained length that is not the
    value's own encoding (F11), a keyword outside the derivation."""


class Census:
    """The census's own work, counted where it runs, and its element-by-element charge (M1a C1).
    Each charge is made before the element's work, from sizes available in O(1) at that moment:
    a node's kind and its string's byte length, its slot's invocation count m and declared-key
    count K, a member key's byte length, the store's population."""
    def __init__(self, unique_steps=1, budget=None, trace=False, mutation=None):
        self.counted = Z
        self.charged = Z
        self.invocations = 0
        self.nodes = 0            # visits begun
        self.strings = 0          # string value nodes charged
        self.keys_seen = 0        # member keys charged
        self.scans_started = 0    # scans begun (strings and keys)
        self.comparisons = 0      # three-way key comparisons executed (slot and store searches)
        self.store_comparisons = 0
        self.extra = unique_steps  # mutation hook for the self-test: steps per UNIQUE item
        self.budget = budget      # C: the census refuses before an element whose charge exceeds it
        self.trace = [] if trace else None
        self.mutation = mutation  # 'scan-first' | 'linear-lookup' | None (self-tests)
        self.stack = []           # the open elements: [label, charge, counted so far]
        self.elements = 0
        self.violations = []      # elements whose counted work exceeded their charge
    def charge(self, c, label=None):
        """Open an element: debit its charge before any of its work. Every step counted until
        the element closes (children's elements excluded) is attributed to it."""
        if self.trace is not None:
            self.trace.append((label, self.charged, self.scans_started, self.nodes))
        if self.budget is not None and (self.charged[1] + c[1] > self.budget[1]
                                        or self.charged[2] + c[2] > self.budget[2]):
            raise Exhausted(label, self.charged, self.scans_started, self.nodes)
        self.charged = self.charged + c
        self.stack.append([label, c, Z])
        self.elements += 1
    def close(self):
        """Close the innermost open element and hold its counted work to its charge."""
        label, c, used = self.stack.pop()
        if used[1] > c[1] or used[2] > c[2]:
            self.violations.append((label, tuple(used), tuple(c)))
    def step(self, k=1, b=0):
        self.counted = self.counted + C(0, k, b)
        if self.stack:
            self.stack[-1][2] = self.stack[-1][2] + C(0, k, b)
    def scan_begin(self):
        self.scans_started += 1
        self.step(1)
    def check(self):
        """Counted <= charged, per element and in total."""
        assert not self.stack, self.stack
        assert not self.violations, self.violations[0]
        assert self.counted[1] <= self.charged[1] and self.counted[2] <= self.charged[2], (self.counted, self.charged)


def node_charge(m, kind_, n):
    """Before a node: its dispatch (1), its m invocations' own costs, its statistics'
    finalization (1); for a string, its one scan (1 element, 2 bytes per byte: decode and
    classify). n is the string's byte length from the representation (O(1))."""
    return C(0, 2 + m + (1 if kind_ == 'string' else 0), 2 * n)


def key_charge(m, K, k):
    """Before an object member: the key's scan (1 element, 2 bytes per byte), its slot lookup (a
    binary search over the K sorted declared keys: at most bitlen(K) comparisons, each examining
    both operands up to the shorter length plus one; charged L = bitlen(K) + 1 comparisons of
    2(k + 1) bytes), per invocation its member cost, its parse/ordered/clone contributions (3)
    and the child's accumulation (1). k is the key's byte length (O(1))."""
    L = bitlen(K) + 1
    return C(0, 1 + L + m + 3 + 1, 2 * k + 2 * L * (k + 1))


def item_charge(m):
    """Before an array item: per invocation at most three item terms (the loop's `items` lookup,
    a UNIQUE term, an ORDER term), its ordered contribution and the child's accumulation."""
    return C(0, 3 * m + 2, 0)


def beta_charge(blobs):
    """Before a retained-length lookup (RF-3's beta rule): one element and search(|blobs|, 32)."""
    k = map_search(blobs)
    return C(0, 1 + k, 2 * k * (32 + 1))


def compare_keys(a, b, c, store=False):
    """ONE three-way comparison of two byte strings, as `Ord::cmp` on `[u8]` (what a Rust
    `binary_search_by(|k| k.as_bytes().cmp(key))` iteration executes): both operands are read up
    to the first differing byte, or to the shorter length plus the length tie-break. Counted as
    one comparison with the bytes it read of both operands (<= 2(min(|a|, |b|) + 1)). It never
    calls a relational operator on the byte strings (`observe_keys` checks that). Returns -1, 0
    or 1."""
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    examined = i + 1 if i < n else n + 1
    c.step(1, 2 * examined)
    c.comparisons += 1
    if store:
        c.store_comparisons += 1
    if i < n:
        return -1 if a[i] < b[i] else 1
    return (len(a) > len(b)) - (len(a) < len(b))


def slot_lookup(slot, kb, c):
    """The declared-key lookup: an explicit binary search over the slot's sorted static key list,
    each iteration one counted three-way comparison (`compare_keys`). At most bitlen(K)
    iterations. Returns the key's index or None (an undeclared key)."""
    keys = slot.key_bytes
    if c.mutation == 'linear-lookup':                             # self-test: an unpriced linear scan
        for j, x in enumerate(keys):
            if compare_keys(x, kb, c) == 0:
                return j
        return None
    if c.mutation == 'two-sided':                                 # self-test: r3's defect, one count for two relational operations
        lo, hi = 0, len(keys)
        while lo < hi:
            mid = (lo + hi) // 2
            x = keys[mid]
            c.step(1, 2 * (min(len(x), len(kb)) + 1)); c.comparisons += 1
            if x < kb:
                lo = mid + 1
            elif x > kb:
                hi = mid
            else:
                return mid
        return None
    lo, hi = 0, len(keys)
    while lo < hi:
        mid = (lo + hi) // 2
        r = compare_keys(keys[mid], kb, c)
        if r < 0:
            lo = mid + 1
        elif r > 0:
            hi = mid
        else:
            return mid
    return None


class ObservedBytes(bytes):
    """A byte string that counts every relational operation applied to it: the independent
    observer of the searches (the `observe_keys` control). Under `compare_keys` the count stays
    zero, because the comparison reads bytes and never calls these."""
    ops = 0
    def _hit(self, other, f):
        ObservedBytes.ops += 1
        return f(bytes(self), bytes(other))
    def __lt__(self, o): return self._hit(o, bytes.__lt__)
    def __gt__(self, o): return self._hit(o, bytes.__gt__)
    def __le__(self, o): return self._hit(o, bytes.__le__)
    def __ge__(self, o): return self._hit(o, bytes.__ge__)
    def __eq__(self, o): return self._hit(o, bytes.__eq__)
    def __ne__(self, o): return self._hit(o, bytes.__ne__)
    __hash__ = bytes.__hash__


def observe_keys(slot, kb, mutation=None):
    """Look `kb` up in `slot` with every key wrapped in `ObservedBytes`, returning (index,
    counted comparisons, counted bytes, observed relational operations, bitlen(K))."""
    class _S: pass
    s = _S(); s.key_bytes = [ObservedBytes(k) for k in slot.key_bytes]
    c = Census(mutation=mutation)
    c.charge(C(0, 10 ** 9, 10 ** 12), ('observe',))
    ObservedBytes.ops = 0
    j = slot_lookup(s, ObservedBytes(kb), c)
    c.close()
    return j, c.comparisons, c.counted[2], ObservedBytes.ops, bitlen(len(slot.key_bytes))


def inv_cost(inv, st, census):
    """One invocation's own cost on a value of statistics st (schema.rs:501-712), excluding its
    children's and same-value rules' invocations (each counted where it is evaluated) and its
    per-member/per-item terms (added per member/item). A closed form of the invocation's static
    entry and st, computed in time bounded by the entry's size; counted as one step. Total on
    every value kind."""
    census.invocations += 1
    census.step(1)
    if inv.is_bool:
        return inv.fixed
    cost = inv.fixed
    S = inv.S
    for lit in inv.literals:
        cost = cost + WALK(st) + WALK(lit) + EQ(st, lit)
    if st.kind == 'integer':
        cost = cost + 2 * S
    elif st.kind == 'string':
        cost = cost + pss(1, st.n) + 3 * S
        if inv.pattern is not None:
            d, k, pattern = inv.pattern
            cost = cost + d + MATCH(k, pattern, st)
    elif st.kind == 'array':
        cost = cost + 6 * S
        if inv.order is not None:
            cost = cost + WALK(st) + inv.order[1]
    elif st.kind == 'object':
        cost = cost + 5 * S
        for r in inv.required:
            cost = cost + pss(1, 0) + search(st.keys, r)
    return cost


def census(av, slot, c, name='', depth=0, identity=False, clone=False):
    """Post-order over the accounted value: returns (statistics, price parts). The parts are
    `eval` (every invocation's own cost), `parse` (the metered parse's per-value prices),
    `ordered` (identity `ordered`) and `clone` (`JsonValue::clone`). O(1) state per frame;
    nothing is allocated. Every element is charged before its work."""
    m = slot.m
    st = St(); st.kind = av.kind; st.path = None; st.n = st.S = st.chars = 0; st.keys = 0
    if st.kind == 'string':
        if c.mutation == 'scan-first':                            # the r2 defect, for the self-test only
            st.n, enc, st.S, st.chars = scan(av.raw, c)
        c.charge(node_charge(m, 'string', av.n), ('string', c.strings))
        c.strings += 1; c.nodes += 1; c.step(1)                   # dispatch
        if c.mutation != 'scan-first':
            st.n, enc, st.S, st.chars = scan(av.raw, c)           # the one scan, after its charge
        assert st.n == av.n
    else:
        c.charge(node_charge(m, st.kind, 0), ('node', st.kind, c.nodes))
        c.nodes += 1; c.step(1)                                   # dispatch, including the depth gate
        if st.kind in ('array', 'object') and depth >= MAX_DEPTH:
            raise PriceUnavailable('container at container depth 32: the encoder refuses it (canonical.rs:536)')
    parts = {'eval': PZ, 'parse': p_value(), 'ordered': pss(1, 0) if identity else PZ, 'clone': PZ}
    if st.kind == 'string':
        st.N, st.B, st.I, st.L = 1, st.n, 0, enc
        parts['parse'] = parts['parse'] + p_string(st.n)
        if clone: parts['clone'] = owned(st.n)
    elif st.kind == 'integer':
        st.N, st.B, st.I, st.L = 1, 16, 1, len(str(av.raw))
    elif st.kind in ('null', 'boolean'):
        st.N, st.B, st.I, st.L = 1, 1, 0, len(json.dumps(av.raw))
    elif st.kind == 'array':
        n = st.keys = av.size
        st.N, st.B, st.I, st.L = 1, 0, 0, 2 + max(n - 1, 0)
        parts['parse'] = parts['parse'] + p_array(n)
        if clone and n: parts['clone'] = owned(VALUE * n)
        child_slot = slot.item_slot
        ok = None
        if identity:
            arm, ok = ORDERED_ARMS.get(name, ORDERED_DEFAULT)
            parts['ordered'] = parts['ordered'] + arm
        prev = [None] * len(slot.orders)
        prev_ordered = None
        for item_av in av.items:
            c.charge(item_charge(m), ('item', c.nodes))
            ist, ip = census(item_av, child_slot, c, '', depth + 1, identity, clone)
            for k in ip: parts[k] = parts[k] + ip[k]
            st.N += ist.N; st.B += ist.B; st.I += ist.I; st.L += ist.L
            for inv in slot.invs:                                           # schema.rs :613-621
                c.step(1)
                parts['eval'] = parts['eval'] + inv.item_lookup
            for _ in slot.uniques:                                          # :634-644
                c.step(c.extra)
                parts['eval'] = parts['eval'] + WALK(ist) + ENC(ist) + btree_insert(n, ist.L, VEC_SLOT)
            for i, inv in enumerate(slot.orders):                           # :645-658
                c.step(1)
                cost, prev[i] = order_item(inv.order[0], ist, prev[i])
                parts['eval'] = parts['eval'] + cost
            if identity:                                                    # descriptors.rs :670-679, :703-706
                c.step(1)
                if name in ('sourceInventory', 'tree', 'blobs'):
                    parts['ordered'] = parts['ordered'] + search(ist.keys if ist.kind == 'object' else 0, 4) + pss(1, 0)
                    if ist.path:
                        parts['ordered'] = parts['ordered'] + PATHCHECK(*ist.path)
                if name == 'stages':
                    parts['ordered'] = parts['ordered'] + 2 * search(ist.keys if ist.kind == 'object' else 0, 8) + pss(ist.N, 32 * ist.N)
                cost, prev_ordered = order_item(ok, ist, prev_ordered)
                parts['ordered'] = parts['ordered'] + cost * (2 if name == 'stages' else 1)
            c.close()                                                       # the item's element
    else:
        k_n = st.keys = av.size
        st.N, st.B, st.I, st.L = 1, 0, 0, 2 + max(k_n - 1, 0)
        if clone and k_n:
            parts['clone'] = owned(LEAF) if k_n <= 11 else k_n * owned(LEAF + EDGES12)
        K = slot.K
        for i, (kb, k, item_av) in enumerate(av.members):                  # in key order (BTreeMap)
            kn = len(kb)                                                    # O(1): String::len
            c.charge(key_charge(m, K, kn), ('key', c.keys_seen))
            c.keys_seen += 1
            kn2, kenc, _, _ = scan(k, c)                                    # the key's one scan
            assert kn2 == kn
            j = slot_lookup(slot, kb, c)                                    # the counted binary search
            child = slot.children[j] if j is not None else slot.star
            table = slot.tables[j] if j is not None else slot.star_table
            for inv, declared in table:
                c.step(1)
                parts['eval'] = parts['eval'] + inv.member(kn, declared)
            c.step(4)                                                       # parse, clone, ordered, accumulation
            parts['parse'] = parts['parse'] + p_string(kn) + p_search(i, kn) + p_insert(i, kn)
            if clone: parts['clone'] = parts['clone'] + owned(kn)
            ist, ip = census(item_av, child, c, k, depth + 1, identity, clone)
            for p in ip: parts[p] = parts[p] + ip[p]
            if identity:                                                    # descriptors.rs :657-665
                parts['ordered'] = parts['ordered'] + pss(2, 2 * kn + len('path') + len('logicalPath'))
                if k in ('path', 'logicalPath') and ist.kind == 'string':
                    parts['ordered'] = parts['ordered'] + PATHCHECK(ist.n, ist.S)
            if k == 'path' and ist.kind == 'string':
                st.path = (ist.n, ist.S)
            st.N += ist.N; st.B += kn + ist.B; st.I += ist.I; st.L += kenc + 1 + ist.L
            c.close()                                                       # the member's element
    c.step(1)                                                               # finalization
    for inv in slot.invs:
        parts['eval'] = parts['eval'] + inv_cost(inv, st, c)
    if clone:
        parts['clone'] = parts['clone'] + pss(1, st.B if st.kind in ('string',) else 0)
    c.close()                                                               # the node's element
    return st, parts


def PATHCHECK(n, S):
    """descriptors.rs path (:621-623)."""
    return pss(1 + S, 2 * n + 12 * S)


# ---------------------------------------------------------------- the retained store (outside) and its lookup (inside)

def canon_bytes(x):
    return json.dumps(x, ensure_ascii=False, separators=(',', ':'), sort_keys=True).encode('utf-8')


def digest_key(x, prefix=b''):
    """A stand-in for the retained blob's digest: a 32-byte key of the value's encoding. OUTSIDE
    the boundary: the fixture builds it when it builds the store, and `Record` receives it as
    `key`, as the pinned fetch receives an already supplied digest (closure.rs:85-95). It is never
    computed inside a census."""
    return hashlib.sha256(prefix + canon_bytes(x)).digest()


class Store:
    """C2b-1a's retained blob map, modelled as a sorted list of (digest, actual length beta).
    Built OUTSIDE the boundary (C2b-1a builds its RetainedInputs itself). `lookup` is the funded
    census element that obtains beta(d) (RF-3's beta rule, companion §0.3)."""
    def __init__(self, entries):
        self.entries = sorted(entries)
    def lookup(self, key, c):
        c.charge(beta_charge(len(self.entries)), ('beta',))
        c.step(1)
        lo, hi, found = 0, len(self.entries), None
        while lo < hi:
            mid = (lo + hi) // 2
            r = compare_keys(self.entries[mid][0], key, c, store=True)   # one three-way comparison
            if r < 0:
                lo = mid + 1
            elif r > 0:
                hi = mid
            else:
                found = self.entries[mid][1]
                break
        c.close()
        return found


# ---------------------------------------------------------------- terms over a census

class Record:
    """One priced record: its accounted value (outside), its census, run once and charged
    element by element, and, when a store is given, the funded lookup of its retained length."""
    def __init__(self, x, doc, selector, identity=False, clone=False, store=None, key=None,
                 budget=None, trace=False, mutation=None, unique_steps=1):
        self.av = AV(x)                                           # outside the boundary
        self.census = Census(unique_steps, budget, trace, mutation)
        self.census.charge(C(0, 8, 0), ('record',)); self.census.step(8)   # the record's term assembly
        self.st, self.parts = census(self.av, root_slot(doc, selector), self.census, '', 0, identity, clone)
        self.census.close()                                       # the record's element
        self.beta = None
        if store is not None:
            assert key is not None, 'the retained digest is supplied from outside the boundary'
            self.beta = store.lookup(key, self.census)            # the charged, counted lookup
        self.census.check()
        self.doc, self.selector = doc, selector
    def walk(self):
        return pss(self.st.N, self.st.B)


def MEMBERSHIP(entry_len):
    k = tree_search(POPULATION)
    return pss(k, k * 2 * (entry_len + 1))


def LOOKUP(doc_id, selector):
    entry = len(doc_id) + 1 + len(selector)
    return (pss(1, 2 * (len(doc_id) + 1)) + pss(D, D * 2 * (len(doc_id) + 1))
            + formatted(entry) + pss(1, entry) + MEMBERSHIP(entry)
            + owned(len(selector)) + pss(1, len(selector)))


def ALIAS(document):
    return pss(len(ALIASES), sum(len(document) + len(a) for a, _ in ALIASES))


def PARSE(r):
    return p_entry(r.st.L) + r.parts['parse']


def ADMIT(r):
    entry = f'{r.doc}#{r.selector}'
    return MEMBERSHIP(len(entry)) + PARSE(r) + r.walk() + RESOLVE(entry, '')[2] + r.parts['eval']


DOMAINS = {'closure': 'closure2', 'snapshot': 'snapshot2'}


def FROM_JSON(domain, r):
    sel = f'/$defs/{domain}'
    return (formatted(len(sel)) + pss(1, len(sel)) + LOOKUP(IDENTITY, sel) + ADMIT(r) + r.parts['ordered']
            + HASH(domain, r.st) + IDENT(DOMAINS[domain]))


ROLES = [('subject-scope', 'enumeratorClosure'), ('view', 'producerClosure'), ('fact', 'producerClosure'),
         ('finding', 'ruleClosure'), ('evaluation-seal', 'evaluatorClosure'), ('proof-bundle', 'evaluatorClosure'),
         ('import', 'producerClosure'), ('import', 'adapterClosure'), ('cache-key', 'producerClosure')]


def OBJECT_WRAPPER(key, domain, st, objects):
    """closure.rs object (:125-162) and candidate (:97-124) around from_json: the object-map search,
    r2's refusal-path `MissingObject(key.into())` string (:103-106), the re-encode, the identifier
    comparison and the role-row scan (no row names `closure` or `snapshot`)."""
    assert not any(o == domain for o, _ in ROLES)
    return (search(objects, len(key)) + owned(len(key)) + ENC(st) + pss(1, 2 * len(key))
            + pss(len(ROLES), sum(len(o) + len(domain) for o, _ in ROLES)))


def T_CLOSURE(key, r, objects):
    return OBJECT_WRAPPER(key, 'closure', r.st, objects) + FROM_JSON('closure', r)


def BLOB(beta, blobs):
    """closure.rs blob (:85-96): the map search and the hash of the ACTUAL retained buffer, of
    length beta(d) (RF-3's beta rule)."""
    return search(blobs, 32) + digest_cost(beta)


def beta_of(r, derived):
    """F11: the retained length the census looked up must be the value's own encoding length
    (the frame F or the record L), because PARSE and UNFRAME are derived over that encoding.
    Without a store the derived length is used (C2b-1a's store holds exactly that encoding)."""
    if r.beta is None:
        return derived
    if r.beta != derived:
        raise PriceUnavailable(f'retained length {r.beta} is not the value\'s own encoding length {derived} (F11)')
    return r.beta


def CANONICAL_RECORD(r):
    return PARSE(r) + ENC(r.st) + pss(1, 2 * r.st.L)


def UNFRAME(domain, r):
    return (pss(1, len(domain)) + pss(1, 2 * FRAME_PREFIX) + pss(1, 2 * (len(domain) + 1)) + pss(1, 16)
            + PARSE(r) + ENC(r.st) + pss(1, 2 * r.st.L))


IDENTITY_DOC = DOCS[IDENTITY]
SETS = IDENTITY_DOC['x-opensip-digest-domains']['domainSets']


def ROW_CLONE(set_name, domain):
    """The registry row's deep clone (closure.rs:1470-1473): static per domain (F2), computed
    OUTSIDE the boundary with its own uncounted census object."""
    c = Census()
    st, parts = census(AV(SETS[set_name][domain]), EMPTY, c, clone=True)
    return parts['clone'] + pss(st.N, st.B)


def frame_length(domain, r):
    return FRAME_PREFIX + len(domain) + 1 + 8 + r.st.L


def T_FRAME(domain, set_name, r, blobs):
    row = SETS[set_name][domain]
    sel = row['selector'][1:]
    F = beta_of(r, frame_length(domain, r))
    dd = IDENTITY_DOC['x-opensip-digest-domains']
    return (BLOB(F, blobs) + pss(1, 2 * FRAME_PREFIX) + pss(1, len(domain) + 1) + pss(2, 2 * len(domain))
            + search(D, len(IDENTITY)) + search(len(IDENTITY_DOC), len('x-opensip-digest-domains'))
            + search(len(dd), len('domainSets')) + search(len(SETS), len(set_name))
            + search(len(SETS[set_name]), len(domain)) + ROW_CLONE(set_name, domain)
            + UNFRAME(domain, r) + ENC(r.st) + 2 * search(len(row), len('selector'))
            + ALIAS(row['document']) + LOOKUP(NATIVE, sel) + ADMIT(r)
            + HASH(domain, r.st) + pss(1, 64) + owned(len(domain)))


def T_RECORD(selector, r, blobs):
    pointer = selector[1:]
    key_bytes = 32 + len(NATIVE_DOC) + len(selector)
    L = beta_of(r, r.st.L)
    return (pss(2, 0) + owned(len(NATIVE_DOC)) + owned(len(selector)) + 2 * BLOB(L, blobs)
            + btree_insert(0, 32, 32) + CANONICAL_RECORD(r) + ALIAS(NATIVE_DOC) + LOOKUP(NATIVE, pointer)
            + ADMIT(r) + btree_insert(0, key_bytes, 32 + 2 * STRING))


def W_REC(r, blobs):
    return BLOB(beta_of(r, r.st.L), blobs) + CANONICAL_RECORD(r)


def CLONE(r):
    """`JsonValue::clone` of a closure descriptor (native_context.rs:222), from its census
    (records built with clone=True)."""
    return r.parts['clone'] + pss(r.st.N, r.st.B)


def c9_shape(snap):
    rows = snap['sourceInventory']
    return dict(top=[len(snap[k].encode()) for k in ('projectId', 'resolvedConfigDigest', 'scopeDigest', 'vcsDigest')],
                rows=len(rows), paths=sum(len(r['path'].encode()) for r in rows),
                segments=sum(r['path'].count('/') + 1 for r in rows),
                encoded_rows=sum(len(json.dumps(r, ensure_ascii=False, separators=(',', ':'), sort_keys=True).encode()) for r in rows),
                length=None)


ENTRIES = [(IDENTITY, '/$defs/closure'), (IDENTITY, '/$defs/snapshot'),
           (NATIVE, '/$defs/TypeScriptNativeContextV2'), (NATIVE, '/$defs/TypeScriptUniverseV2ResolvedInputs'),
           (NATIVE, '/$defs/TypeScriptConfigGraphV1'), (NATIVE, '/$defs/ResolvedNodeModulesLayoutV1')]

if __name__ == '__main__':
    for doc, sel in ENTRIES:
        print(doc + '#' + sel, 'tau (mu, invocations, slots):', tau_size(doc, sel))
    print('D', D, 'population', POPULATION, 'aliases', len(ALIASES), 'TABLE', len(TABLE), 'FORMS', len(FORMS))
