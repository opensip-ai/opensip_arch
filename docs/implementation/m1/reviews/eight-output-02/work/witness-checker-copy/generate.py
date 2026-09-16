"""Constructive positive-witness generator over the pinned original OpenSIP schemas.

Phase 1 seeds: true rows of the TS-runtime harvest corpus (provenance retained, file not copied).
Phase 2 generation: bounded depth-first constructive search from the original schemas only.
  - $ref/allOf are conjoined; anyOf/oneOf/if-then-else are branch points (bounded DFS);
    discriminator-shaped `if` nodes are decided statically from forced required consts.
  - leaves are built per type (const/enum, regex-directed strings, bounded integers,
    objects with error-guided repair over child candidates, arrays honouring
    minItems/contains/uniqueItems/x-opensip-order).
  - every leaf candidate is filtered by ExactValidator for every conjoined schema.
Only statically sound contradictions (type/const/enum/bound/closed-object/false-schema
conflicts, and required children proved empty) count toward a proof of
unsatisfiability; any heuristic cut-off taints the search and forbids a proof claim.
"""
import copy
import json
import re
import sys
import time
import re._constants as C
import re._parser as P
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I isolated mode omits the script directory
from witness_common import HARVEST, OUT, SOURCE_MAP, SOURCES, CHECK_METADATA, check, load, pin, targets

K_TARGET = 2            # witnesses sought per target
K_CHILD = 4             # candidates sought per child subproblem
MAX_SOLVE_DEPTH = 28    # nested container subproblems (exact codec limit is 32)
STEP_BUDGET = 400000    # solve calls + validator calls per target
TIME_BUDGET = 120.0     # seconds per target
REPAIR_ROUNDS = 64      # object repair assignments tried per leaf
ARRAY_EXTRA_LEN = 3     # lengths tried above the minimum length
VARIANTS = 6            # regex/fill character variants
LENGTH_TARGETS = (1, 0, 2, 3, 4, 8, 16, 32, 64, 128)
SEEDS_PER_REF = 2
PREF = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-_.:/ '
DEFAULT_TYPES = ('object', 'string', 'integer', 'boolean', 'null', 'array')
MIN_INT, MAX_INT = -(2**63), 2**64 - 1
INF = float('inf')

OBJECT_KW = {'properties', 'required', 'additionalProperties', 'minProperties', 'maxProperties', 'propertyNames', 'patternProperties'}
ARRAY_KW = {'items', 'contains', 'minItems', 'maxItems', 'uniqueItems'}
STRING_KW = {'pattern', 'minLength', 'maxLength'}
INTEGER_KW = {'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum'}


class Budget(Exception):
    pass


class RegexUnsupported(Exception):
    pass


def esc(segment):
    return str(segment).replace('~', '~0').replace('/', '~1').replace('%', '%25')


def child(uri, *segments):
    return uri + ''.join('/' + esc(s) for s in segments)


def jtype(value):
    if value is None:
        return 'null'
    return {bool: 'boolean', int: 'integer', str: 'string', list: 'array', dict: 'object'}[type(value)]


def norm_types(t):
    return {'integer' if x == 'number' else x for x in ([t] if isinstance(t, str) else t)}


# ---------------------------------------------------------------- regex-directed strings
CATEGORY = {C.CATEGORY_DIGIT: r'\d', C.CATEGORY_NOT_DIGIT: r'\D', C.CATEGORY_SPACE: r'\s',
            C.CATEGORY_NOT_SPACE: r'\S', C.CATEGORY_WORD: r'\w', C.CATEGORY_NOT_WORD: r'\W'}


def char_pred(op, av):
    if op is C.LITERAL:
        return lambda c: ord(c) == av
    if op is C.NOT_LITERAL:
        return lambda c: ord(c) != av
    if op is C.ANY:
        return lambda c: c != '\n'
    if op is C.CATEGORY:
        rx = re.compile(CATEGORY[av])
        return lambda c: rx.fullmatch(c) is not None
    if op is C.IN:
        neg = False
        tests = []
        for iop, iav in av:
            if iop is C.NEGATE:
                neg = True
            elif iop is C.LITERAL:
                tests.append(lambda c, v=iav: ord(c) == v)
            elif iop is C.RANGE:
                tests.append(lambda c, v=iav: v[0] <= ord(c) <= v[1])
            elif iop is C.CATEGORY:
                rx = re.compile(CATEGORY[iav])
                tests.append(lambda c, r=rx: r.fullmatch(c) is not None)
            else:
                raise RegexUnsupported(str(iop))
        return lambda c: any(t(c) for t in tests) != neg
    raise RegexUnsupported(str(op))


def pick(pred, variant):
    order = PREF[variant % len(PREF):] + PREF[:variant % len(PREF)]
    for c in order:
        if pred(c):
            return c
    for code in range(0x20, 0x3000):
        c = chr(code)
        if pred(c):
            return c
    return None


def regex_string(pattern, variant, target):
    parsed = P.parse(pattern)

    def gen(items):
        out = []
        for op, av in items:
            if op in (C.LITERAL, C.NOT_LITERAL, C.ANY, C.IN, C.CATEGORY):
                c = pick(char_pred(op, av), variant)
                if c is None:
                    raise RegexUnsupported('empty character class')
                out.append(c)
            elif op in (C.MAX_REPEAT, C.MIN_REPEAT, C.POSSESSIVE_REPEAT):
                lo, hi, sub = av
                hi = 1 << 20 if hi is C.MAXREPEAT else hi
                out.extend(gen(sub) for _ in range(min(hi, max(lo, target))))
            elif op is C.SUBPATTERN:
                out.append(gen(av[-1]))
            elif op is C.BRANCH:
                alts = av[1]
                out.append(gen(alts[variant % len(alts)]))
            elif op in (C.AT, C.ASSERT, C.ASSERT_NOT):
                continue  # assertions are enforced by the validator filter
            else:
                raise RegexUnsupported(str(op))
        return ''.join(out)

    return gen(parsed)


# ---------------------------------------------------------------- search context
class Search:
    def __init__(self, reference, registry, documents):
        self.reference = reference
        self.registry = registry
        self.docs = documents
        self.validators = {}
        self.memo = {}
        self.expand_memo = {}
        self.active = set()
        self.steps = 0
        self.taints = 0
        self.events = []
        self.deadline = INF

    # -- budget/taint bookkeeping
    def tick(self):
        self.steps += 1
        if self.steps > STEP_BUDGET or time.monotonic() > self.deadline:
            raise Budget()

    def taint(self, kind, pos, depth, detail=None):
        self.taints += 1
        if len(self.events) < 4000:
            self.events.append({'depth': depth, 'kind': kind, 'selector': list(pos), 'detail': detail})

    # -- schema access
    def node(self, uri):
        doc, _, frag = uri.partition('#')
        n = self.docs[doc]
        if frag:
            if not frag.startswith('/'):
                raise KeyError('unsupported fragment ' + uri)
            for seg in unquote(frag[1:]).split('/'):
                n = n[int(seg)] if isinstance(n, list) else n[seg.replace('~1', '/').replace('~0', '~')]
        return n

    def resolve(self, uri, ref):
        doc = uri.partition('#')[0]
        target = doc + ref if ref.startswith('#') else (ref if '#' in ref else ref + '#')
        if target.partition('#')[0] not in self.docs:
            raise KeyError('unregistered $ref ' + ref)
        return target

    def validator(self, uri):
        v = self.validators.get(uri)
        if v is None:
            v = self.validators[uri] = self.reference.ExactValidator({'$ref': uri}, registry=self.registry)
        return v

    def valid(self, uri, value):
        self.tick()
        return self.validator(uri).is_valid(value)

    def error_detail(self, uri, value):
        try:
            import jsonschema.exceptions as E
            err = E.best_match(self.validator(uri).iter_errors(value))
        except Exception as exc:
            return {'error': type(exc).__name__, 'message': str(exc)[:400]}
        if err is None:
            return None
        return {'schema': uri, 'message': err.message[:400], 'instancePath': err.json_path,
                'schemaPath': [str(s) for s in err.absolute_schema_path], 'validator': err.validator}

    # -- conjunction expansion
    def expand(self, pos, decided):
        key = (pos, decided)
        hit = self.expand_memo.get(key)
        if hit is not None:
            return hit
        atoms, disj, seen, stack = [], [], set(), list(pos)
        result = None
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            n = self.node(u)
            if n is True:
                continue
            if n is False:
                result = (None, ('false-schema', u))
                break
            atoms.append((u, n))
            if '$ref' in n:
                stack.append(self.resolve(u, n['$ref']))
            stack.extend(child(u, 'allOf', i) for i in range(len(n.get('allOf', ()))))
            for kw in ('oneOf', 'anyOf'):
                if kw in n and (u, kw) not in decided:
                    disj.append(((u, kw), [(child(u, kw, i),) for i in range(len(n[kw]))]))
            if 'if' in n and (u, 'if') not in decided:
                then = (child(u, 'if'),) + ((child(u, 'then'),) if 'then' in n else ())
                other = (child(u, 'else'),) if 'else' in n else ()
                disj.append(((u, 'if'), [then, other]))
        if result is None:
            result = (atoms, disj)
        self.expand_memo[key] = result
        return result

    def prop_uris(self, atoms, key):
        uris = []
        for u, n in atoms:
            matched = False
            if key in n.get('properties', {}):
                uris.append(child(u, 'properties', key))
                matched = True
            for p in n.get('patternProperties', {}):
                if re.search(p, key):
                    uris.append(child(u, 'patternProperties', p))
                    matched = True
            if not matched and 'additionalProperties' in n:
                uris.append(child(u, 'additionalProperties'))
        return tuple(sorted(set(uris)))

    def facts(self, atoms):
        types = None
        for _, n in atoms:
            if 'type' in n:
                t = norm_types(n['type'])
                types = t if types is None else types & t
        required = set()
        for _, n in atoms:
            required.update(n.get('required', ()))
        return types, required

    def forced(self, atoms, required):
        out = {}
        for key in required:
            got = self.expand(self.prop_uris(atoms, key), frozenset())
            if got[0] is None:
                continue
            for _, sn in got[0]:
                if 'const' in sn:
                    out.setdefault(key, []).append(sn['const'])
                elif isinstance(sn.get('enum'), list) and len(sn['enum']) == 1:
                    out.setdefault(key, []).append(sn['enum'][0])
        return out

    def contradiction(self, atoms):
        """Statically sound contradiction reason for a positive conjunction, or None."""
        eq = self.reference.equal_typed
        types, required = self.facts(atoms)
        if types is not None and not types:
            return 'type-intersection-empty'
        consts = [n['const'] for _, n in atoms if 'const' in n]
        enums = [n['enum'] for _, n in atoms if 'enum' in n]
        if consts:
            if any(not eq(consts[0], c) for c in consts[1:]):
                return 'const-conflict'
            if types is not None and jtype(consts[0]) not in types:
                return 'const-type-conflict'
            if any(not any(eq(consts[0], x) for x in e) for e in enums):
                return 'const-not-in-enum'
        if enums:
            common = [x for x in enums[0] if all(any(eq(x, y) for y in e) for e in enums[1:])]
            if types is not None:
                common = [x for x in common if jtype(x) in types]
            if not common:
                return 'enum-intersection-empty'

        def bound(kw, agg, default, shift=0):
            vals = [n[kw] + shift for _, n in atoms if kw in n and type(n[kw]) is int]
            return agg(vals) if vals else default
        only = lambda t: types is not None and types <= {t}
        lo = max(bound('minimum', max, -INF), bound('exclusiveMinimum', max, -INF, 1))
        hi = min(bound('maximum', min, INF), bound('exclusiveMaximum', min, INF, -1))
        if only('integer') and (lo > hi or lo > MAX_INT or hi < MIN_INT):
            return 'integer-bounds-empty'
        if only('string') and bound('minLength', max, 0) > bound('maxLength', min, INF):
            return 'length-bounds-empty'
        if only('array') and max(bound('minItems', max, 0), 1 if any('contains' in n for _, n in atoms) else 0) > bound('maxItems', min, INF):
            return 'items-bounds-empty'
        if only('object'):
            if max(bound('minProperties', max, 0), len(required)) > bound('maxProperties', min, INF):
                return 'properties-bounds-empty'
            for key in required:
                for u, n in atoms:
                    if n.get('additionalProperties') is False and key not in n.get('properties', {}) \
                            and not any(re.search(p, key) for p in n.get('patternProperties', {})):
                        return 'required-key-closed:' + key
                if self.expand(self.prop_uris(atoms, key), frozenset())[0] is None:
                    return 'required-key-false-schema:' + key
            for key, vals in self.forced(atoms, required).items():
                if any(not eq(vals[0], v) for v in vals[1:]):
                    return 'required-key-const-conflict:' + key
        return None

    def eval_if(self, if_uri, atoms):
        """True/False when the if-node outcome is forced for every instance of atoms, else None."""
        n = self.node(if_uri)
        types, required = self.facts(atoms)
        if n is True:
            return True
        if not isinstance(n, dict) or types is None or types != {'object'}:
            return None
        if set(n) - {'properties', 'required', 'description', 'title', '$comment', 'type'}:
            return None
        eq = self.reference.equal_typed
        result = True
        if 'type' in n:
            if not (types & norm_types(n['type'])):
                return False
            if not types <= norm_types(n['type']):
                result = None
        forced = self.forced(atoms, required)
        for key in n.get('required', ()):
            if key not in required:
                result = None
        for key, sub in n.get('properties', {}).items():
            if sub is True:
                continue
            if not isinstance(sub, dict) or set(sub) - {'const', 'enum', 'description'}:
                result = None
                continue
            vals = forced.get(key)
            if not vals or any(not eq(vals[0], v) for v in vals[1:]):
                result = None
                continue
            ok = ('const' not in sub or eq(sub['const'], vals[0])) and ('enum' not in sub or any(eq(x, vals[0]) for x in sub['enum']))
            if not ok:
                return False
        return result

    # -- search
    def solve(self, pos, decided=frozenset(), k=1, depth=0):
        self.tick()
        key = (pos, decided)
        hit = self.memo.get(key)
        if hit is not None:
            out, final, ktried = hit
            if len(out) >= k or final:
                return out[:k]
            if k <= ktried:
                self.taint('reused-incomplete-subsearch', pos, depth)
                return out[:k]
        if depth > MAX_SOLVE_DEPTH:
            self.taint('depth-limit', pos, depth)
            return []
        if key in self.active:
            self.taint('recursion-cycle', pos, depth)
            return []
        self.active.add(key)
        before = self.taints
        out, seen = [], set()

        def add(v):
            c = self.reference.canonical(v)
            if c not in seen:
                seen.add(c)
                out.append(v)
        try:
            atoms, disj = self.expand(pos, decided)
            reason = disj if atoms is None else self.contradiction(atoms)
            if reason:
                self.events.append({'depth': depth, 'kind': 'static-contradiction', 'selector': list(pos), 'detail': reason}) if len(self.events) < 4000 else None
            elif disj:
                ranked = []
                for did, options in disj:
                    if did[1] == 'if':
                        outcome = self.eval_if(child(did[0], 'if'), atoms)
                        if outcome is True:
                            options = [options[0]]
                        elif outcome is False:
                            options = [options[1]]
                        else:
                            ifn = self.node(child(did[0], 'if'))
                            _, required = self.facts(atoms)
                            if isinstance(ifn, dict) and set(ifn.get('required', ())) - required:
                                options = [options[1], options[0]]
                        ranked.append((len(options), 1, did, options))
                    else:
                        ranked.append((len(options), 0, did, options))
                ranked.sort(key=lambda r: (r[0], r[1]))
                _, _, did, options = ranked[0]
                for addpos in options:
                    npos = tuple(sorted(set(pos) | set(addpos)))
                    for v in self.solve(npos, decided | {did}, k - len(out), depth):
                        add(v)
                    if len(out) >= k:
                        break
            else:
                proof = {'complete': True}
                for v in self.construct(pos, atoms, k, depth, proof):
                    if all(self.valid(u, v) for u in pos):
                        add(v)
                        if len(out) >= k:
                            break
                    else:
                        bad = next(u for u in pos if not self.valid(u, v))
                        self.taint('candidate-rejected', pos, depth, {'candidate': self.reference.canonical(v).decode()[:600], 'validatorError': self.error_detail(bad, v)})
                if not out and not proof['complete']:
                    self.taint('construction-bounded', pos, depth, proof.get('why'))
        finally:
            self.active.discard(key)
        final = len(out) < k and self.taints == before
        self.memo[key] = (out, final, k)
        return out

    # -- leaf construction
    def construct(self, pos, atoms, k, depth, proof):
        eq = self.reference.equal_typed
        consts = [n['const'] for _, n in atoms if 'const' in n]
        enums = [n['enum'] for _, n in atoms if 'enum' in n]
        if consts:
            yield copy.deepcopy(consts[0])
            return
        if enums:
            for x in enums[0]:
                if all(any(eq(x, y) for y in e) for e in enums[1:]):
                    yield copy.deepcopy(x)
            return
        types, _ = self.facts(atoms)
        present = set().union(*(set(n) for _, n in atoms)) if atoms else set()
        if types is None:
            inferred = [t for t, kws in (('object', OBJECT_KW), ('array', ARRAY_KW), ('string', STRING_KW), ('integer', INTEGER_KW)) if present & kws]
            order = inferred + [t for t in DEFAULT_TYPES if t not in inferred]
        else:
            order = [t for t in DEFAULT_TYPES if t in types]
        for t in order:
            if t == 'null':
                yield None
            elif t == 'boolean':
                yield False
                yield True
            elif t == 'integer':
                yield from self.integers(atoms, proof)
            elif t == 'string':
                yield from self.strings(atoms, proof)
            elif t == 'object':
                yield from self.objects(pos, atoms, k, depth, proof)
            elif t == 'array':
                yield from self.arrays(atoms, k, depth, proof)

    def integers(self, atoms, proof):
        lo, hi = MIN_INT, MAX_INT
        for _, n in atoms:
            if type(n.get('minimum')) is int:
                lo = max(lo, n['minimum'])
            if type(n.get('exclusiveMinimum')) is int:
                lo = max(lo, n['exclusiveMinimum'] + 1)
            if type(n.get('maximum')) is int:
                hi = min(hi, n['maximum'])
            if type(n.get('exclusiveMaximum')) is int:
                hi = min(hi, n['exclusiveMaximum'] - 1)
        proof['complete'] = False
        seen = set()
        for x in (0, 1, lo, lo + 1, hi, hi - 1, 2, 3, 7, 42):
            if lo <= x <= hi and x not in seen:
                seen.add(x)
                yield x

    def strings(self, atoms, proof):
        proof['complete'] = False
        patterns = [n['pattern'] for _, n in atoms if 'pattern' in n]
        lo = max([n['minLength'] for _, n in atoms if 'minLength' in n] or [0])
        hi = min([n['maxLength'] for _, n in atoms if 'maxLength' in n] or [INF])
        compiled = [re.compile(p) for p in patterns]
        targets = [t for t in dict.fromkeys((max(lo, 1), lo) + LENGTH_TARGETS + ((hi,) if hi != INF else ()))]
        seen = set()
        for variant in range(VARIANTS):
            for target in targets:
                for generator in (patterns or [None]):
                    try:
                        if generator is None:
                            if not lo <= target <= hi:
                                continue
                            s = pick(lambda c: True, variant) * target
                        else:
                            s = regex_string(generator, variant, target)
                    except RegexUnsupported as exc:
                        proof['why'] = 'regex-unsupported: ' + str(exc)
                        continue
                    if s not in seen and lo <= len(s) <= hi and all(c.search(s) for c in compiled):
                        seen.add(s)
                        yield s

    def objects(self, pos, atoms, k, depth, proof):
        types, required = self.facts(atoms)
        keys = sorted(required)
        minp = max([n['minProperties'] for _, n in atoms if 'minProperties' in n] or [0])
        maxp = min([n['maxProperties'] for _, n in atoms if 'maxProperties' in n] or [INF])
        if len(keys) < minp:
            for _, n in atoms:
                for key in n.get('properties', {}):
                    if len(keys) < minp and key not in keys and self.contradiction(atoms + [(None, {'required': [key], 'type': 'object'})]) is None:
                        keys.append(key)
            names = tuple(sorted({child(u, 'propertyNames') for u, n in atoms if 'propertyNames' in n}))
            if len(keys) < minp:
                for name in self.solve(names, frozenset(), minp + K_CHILD, depth + 1):
                    if len(keys) < minp and type(name) is str and name not in keys and self.contradiction(atoms + [(None, {'required': [name], 'type': 'object'})]) is None:
                        keys.append(name)
            if len(keys) < minp:
                proof['complete'] = False
                proof['why'] = 'minProperties needs more property names than properties lists'
                return
        if len(keys) > maxp:
            return  # static: required count exceeds maxProperties
        candidates = {}
        for key in keys:
            uris = self.prop_uris(atoms, key)
            got = self.solve(uris, frozenset(), K_CHILD, depth + 1)
            if not got:
                hit = self.memo.get((uris, frozenset()))
                if not (hit and hit[1] and key in required and types == {'object'}):
                    proof['complete'] = False
                    proof['why'] = {'emptyRequiredChild': key, 'selector': list(uris)}
                return
            candidates[key] = got
        idx = {key: 0 for key in keys}
        tried, produced = set(), 0
        proof['complete'] = False
        for _ in range(REPAIR_ROUNDS):
            sig = tuple(idx[key] for key in keys)
            if sig in tried:
                break
            tried.add(sig)
            obj = {key: copy.deepcopy(candidates[key][idx[key]]) for key in keys}
            implicated, failing = set(), False
            for u in pos:
                self.tick()
                for err in self.validator(u).iter_errors(obj):
                    failing = True
                    self.implicated(err, implicated)
            if not failing:
                yield obj
                produced += 1
                if produced >= k:
                    return
                implicated = set(keys)
            movable = [key for key in keys if key in implicated and len(candidates[key]) > 1]
            if not movable:
                break
            for key in movable:  # odometer over implicated keys
                idx[key] += 1
                if idx[key] < len(candidates[key]):
                    break
                idx[key] = 0

    def implicated(self, err, acc):
        if len(err.absolute_path):
            acc.add(err.absolute_path[0])
        for sub in err.context or ():
            self.implicated(sub, acc)

    def arrays(self, atoms, k, depth, proof):
        items = tuple(sorted({child(u, 'items') for u, n in atoms if 'items' in n}))
        contains = tuple(sorted({child(u, 'contains') for u, n in atoms if 'contains' in n}))
        lo = max([n['minItems'] for _, n in atoms if 'minItems' in n] + [1 if contains else 0])
        hi = min([n['maxItems'] for _, n in atoms if 'maxItems' in n] or [INF])
        orders = [n['x-opensip-order'] for _, n in atoms if 'x-opensip-order' in n]
        strict = [o for o in orders if o not in ('sequence', 'canonical-order')]
        unique = any(n.get('uniqueItems') is True for _, n in atoms) or bool(strict)
        proof['complete'] = False
        length = lo
        while length <= hi and length <= lo + ARRAY_EXTRA_LEN:
            if length == 0:
                yield []
                length += 1
                continue
            pool = self.solve(items, frozenset(), length + K_CHILD, depth + 1)
            plans = [[]]
            if contains:
                # one element meeting every contains, else one distinct element per contains
                plans = [[h] for h in self.solve(tuple(sorted(set(items) | set(contains))), frozenset(), K_CHILD, depth + 1)]
                if len(contains) > 1:
                    separate = [self.solve(tuple(sorted(set(items) | {c})), frozenset(), K_CHILD, depth + 1) for c in contains]
                    if all(separate):
                        plans.append([got[0] for got in separate])
            if not pool and not any(len(plan) >= length for plan in plans):
                proof['why'] = {'emptyItems': list(items)}
                length += 1
                continue
            for plan in plans:
                arr, canon, fields = [], set(), set()
                for v in plan + list(pool):
                    if len(arr) >= length:
                        break
                    c = self.reference.canonical(v)
                    f = self.order_key(strict, v)
                    if c in canon or (unique and f is not None and f in fields):
                        continue
                    canon.add(c)
                    if f is not None:
                        fields.add(f)
                    arr.append(copy.deepcopy(v))
                if len(arr) == length:
                    yield self.arrange(orders, arr)
            length += 1

    @staticmethod
    def order_key(orders, v):
        if not orders:
            return None
        o = orders[0]
        try:
            if isinstance(o, dict):
                return tuple(v[f] for f in o['by'])
            if o in ('path', 'ruleId', 'waiverId'):
                return v[o]
            if o == 'predicate':
                return tuple(v[f] for f in ('ruleId', 'subjectId', 'predicateId'))
            if o in ('ordinal', 'candidateOrdinal'):
                return None
            return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        except (KeyError, TypeError):
            return None

    def arrange(self, orders, arr):
        for o in orders:
            if o in ('ordinal', 'candidateOrdinal'):
                for i, v in enumerate(arr):
                    if isinstance(v, dict) and o in v:
                        v[o] = i
        for o in orders:
            if o == 'sequence':
                continue
            try:
                if isinstance(o, dict):
                    arr.sort(key=lambda v: tuple(v[f].encode('utf-8') for f in o['by']))
                elif o == 'utf8':
                    arr.sort(key=lambda v: v.encode('utf-8'))
                elif o in ('canonical-set', 'canonical-order'):
                    arr.sort(key=self.reference.canonical)
                elif o in ('path', 'ruleId', 'waiverId'):
                    arr.sort(key=lambda v: v[o].encode('utf-8'))
                elif o == 'predicate':
                    arr.sort(key=lambda v: tuple(v[f].encode('utf-8') for f in ('ruleId', 'subjectId', 'predicateId')))
                elif o == 'numeric':
                    arr.sort()
            except (KeyError, TypeError, AttributeError):
                pass
            break
        return arr


# ---------------------------------------------------------------- driver
def seeds(reference, registry, refs):
    raw = HARVEST.read_bytes()
    data = json.loads(raw)
    rows = {}
    for ref, index, ok in data['rows']:
        if ok is True and ref in refs:
            rows.setdefault(ref, []).append(index)
    cases, index_record = [], {}
    for ref in refs:
        chosen = sorted(rows.get(ref, ()), key=lambda i: (len(reference.canonical(data['values'][i])), i))[:SEEDS_PER_REF]
        kept = []
        for i in chosen:
            value = data['values'][i]
            if check(reference, registry, ref, value) is None:
                cases.append({'ref': ref, 'value': value, 'origin': {'kind': 'harvest-seed', 'valueIndex': i}})
                kept.append(i)
        if chosen:
            index_record[ref] = {'trueRowCount': len(rows[ref]), 'seededValueIndexes': kept}
    return cases, index_record, len(data['values']), len(data['rows'])


def main():
    started = time.time()
    reference, registry, documents = load()
    refs = list(targets())
    harvest_pin = pin(HARVEST)
    seed_cases, seed_index, nvalues, nrows = seeds(reference, registry, refs)
    for case in seed_cases:
        case['origin']['harvestSha256'] = harvest_pin['sha256']
    search = Search(reference, registry, documents)
    generated, uncovered, per_target = [], [], {}
    for n, ref in enumerate(refs):
        search.steps, search.events = 0, []
        search.deadline = time.monotonic() + TIME_BUDGET
        before, t0, budget = search.taints, time.monotonic(), False
        try:
            values = search.solve((ref,), frozenset(), K_TARGET, 0)
        except Budget:
            values, budget = [], True
            search.active.clear()
        kept = []
        for v in values:
            err = check(reference, registry, ref, v)
            if err is None:
                kept.append(v)
            else:
                search.events.append({'depth': 0, 'kind': 'final-check-rejected', 'selector': [ref], 'detail': err})
        for v in kept:
            generated.append({'ref': ref, 'value': v, 'origin': {'kind': 'generated', 'generator': 'generate.py'}})
        per_target[ref] = {'generated': len(kept), 'steps': search.steps, 'seconds': round(time.monotonic() - t0, 3),
                           'budgetExhausted': budget, 'tainted': search.taints != before}
        if not kept:
            per_target[ref]['events'] = sorted(search.events, key=lambda e: -e['depth'])[:12]
        print(n, ref, len(kept), search.steps, 'BUDGET' if budget else '', file=sys.stderr, flush=True)
    generator_pin = pin(OUT / 'generate.py')
    for case in generated:
        case['origin']['generatorSha256'] = generator_pin['sha256']
    covered = {c['ref'] for c in seed_cases} | {c['ref'] for c in generated}
    for ref in refs:
        if ref in covered:
            continue
        info = per_target[ref]
        proved = not info['budgetExhausted'] and not info['tainted']
        events = info.get('events', [])
        hard = next((e for e in events if e['kind'] == 'candidate-rejected'), None) or (events[0] if events else None)
        uncovered.append({'ref': ref, 'reason': {
            'classification': 'proved-unsatisfiable' if proved else ('search-budget-exhausted' if info['budgetExhausted'] else 'search-failed-not-proved'),
            'hardNode': hard, 'staticContradictions': [e for e in events if e['kind'] == 'static-contradiction'][:8] if proved else None}})
    cases = seed_cases + generated
    order = {r: i for i, r in enumerate(refs)}
    cases.sort(key=lambda c: (order[c['ref']], c['origin']['kind']))
    (OUT / 'witnesses.json').write_text(json.dumps({'schemaVersion': 1, 'cases': cases, 'uncovered': uncovered}, ensure_ascii=False, indent=1) + '\n')
    (OUT / 'seed-index.json').write_text(json.dumps({'source': harvest_pin, 'valuesInSource': nvalues, 'rowsInSource': nrows,
                                                     'selection': 'rows with result exactly true; per ref the %d smallest canonical values re-checked' % SEEDS_PER_REF,
                                                     'refs': seed_index}, indent=1) + '\n')
    (OUT / 'generation-report.json').write_text(json.dumps({
        'generator': generator_pin, 'seconds': round(time.time() - started, 1),
        'limits': {'K_TARGET': K_TARGET, 'K_CHILD': K_CHILD, 'MAX_SOLVE_DEPTH': MAX_SOLVE_DEPTH, 'STEP_BUDGET': STEP_BUDGET,
                   'TIME_BUDGET_SECONDS': TIME_BUDGET, 'REPAIR_ROUNDS': REPAIR_ROUNDS, 'ARRAY_EXTRA_LEN': ARRAY_EXTRA_LEN,
                   'VARIANTS': VARIANTS, 'LENGTH_TARGETS': LENGTH_TARGETS, 'SEEDS_PER_REF': SEEDS_PER_REF},
        'perTarget': per_target}, indent=1, default=str) + '\n')
    print('cases', len(cases), 'covered', len(covered), 'uncovered', len(uncovered), file=sys.stderr)


if __name__ == '__main__':
    main()
