"""Bounded combined consistency pass. Reads before/ read-only; writes proposed/ only.

Every edit is an exact anchored splice asserted to occur once. All unrelated bytes are
preserved. No product implementation, no pins/reports/readiness, no suite runs.
"""
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = HERE / 'before'
P = HERE / 'proposed'
PRIOR = Path('/tmp/opensip-design-corrections')
DISPOSITIONS = []


def splice(buf: bytes, before: bytes, after: bytes, label: str) -> bytes:
    assert buf.count(before) == 1, '%s: anchor count %d' % (label, buf.count(before))
    out = buf.replace(before, after)
    assert out.count(after) >= 1 and out.replace(after, before) == buf, label
    DISPOSITIONS.append(label)
    return out


def emit(rel: str, data: bytes):
    p = P / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


# =============================================================== native-evidence.md
MD_REL = 'docs/v2/contracts/product-v1/native-evidence.md'
md = (B / MD_REL).read_bytes()

# --- agreed precedence paragraph (prose-final bytes, root-approved)
md = splice(md, (PRIOR / 'v19-precedence-coauthor.v1/before-paragraph.md').read_bytes(),
            (PRIOR / 'v19-prose-final-coauthor.v1/precedence-final.md').read_bytes(),
            'md: agreed precedence-final paragraph applied')

# --- item 5: 9.2 publishes the initial state and the update order
md = splice(
    md,
    b'the guard-equality law, the state updates each frame performs,\n',
    b'the guard-equality law, the **initial state** every exchange begins in\n'
    b'together with the order in which initialization, pre-match, matching and the\n'
    b'post-match updates are applied, the state updates each frame performs,\n',
    'md 9.2: initial state and ordered updates named as part of the complete artifact')

# --- item 3b: the false "names no field, count or limit" claim (S14 paragraph)
md = splice(
    md,
    b'they refuse HERE rather than through a generic schema exception that names no field, count or limit.',
    b'they refuse HERE rather than through a generic schema exception that carries no typed scope '
    b'projection \xe2\x80\x94 no public detail, no class or exit, no `field:count>limit` subject and no '
    b'per-field remedy \xe2\x80\x94 even though its own structured fields do identify the failing path and the bound.',
    'md S14: generic-schema claim restated as missing TYPED projection')

# --- item 4: the Plan-array order claim is scoped to its boundary
md = splice(
    md,
    b'When more than one Plan array overflows at once the subject is the first in the published '
    b'`$defs/plan` declaration order \xe2\x80\x94 `semanticClosures`, `nativeContextDigests`, `importIds` \xe2\x80\x94 '
    b'so one request always yields one subject and narrowing makes deterministic progress.',
    b'When more than one array of an assembled prospective Plan overflows at once the subject is the '
    b'first in the published `$defs/plan` declaration order \xe2\x80\x94 `semanticClosures`, '
    b'`nativeContextDigests`, `importIds` \xe2\x80\x94 so one request always yields one subject and narrowing '
    b'makes deterministic progress. That order governs the prospective-Plan boundary, among the fields '
    b'present there. It is not an ordering claim about the whole request: `nativeContextDigests` is also '
    b'accounted at the earlier producer boundary that computes, admission-validates and deduplicates the '
    b'native contexts, and an overflow refuses there before any prospective Plan is assembled.',
    'md S14: Plan-array order scoped to the prospective-Plan boundary (phases, no executable change)')

# --- item 3b: same claim in the adjacent pre-Plan admission-order paragraph
md = splice(
    md,
    b'because a `maxItems` breach is reported generically, restating the entire instance and naming '
    b'no field, count or limit;',
    b'because a `maxItems` breach is reported generically: the exception restates the entire instance '
    b'and carries no typed scope projection \xe2\x80\x94 no public detail, class, exit, `field:count>limit` '
    b'subject or per-field remedy \xe2\x80\x94 even though its own structured fields do identify the failing '
    b'path and the bound;',
    'md pre-Plan paragraph: same generic-schema claim corrected identically')
emit(MD_REL, md)

# =============================================================== identity-schemas.v2.json
IS_REL = 'docs/coop/design-corrections/foundation/identity-schemas.v2.json'
raw_is = (B / IS_REL).read_text(encoding='utf-8')
S = json.loads(raw_is)
assert json.dumps(S, indent=2, ensure_ascii=True) + '\n' == raw_is, 'identity-schemas format probe'
law = S['x-opensip-digest-domains']['scopeCapabilityLaw']

law['guardOrder'] = (
    "TWO boundaries decide this, in this order. FIRST the native Coverage PRODUCER admission, which "
    "judges ONE record and never sees the snapshot, so it applies this law only where the scope carries "
    "its own paths - a `source-path` relation with a `bodyIdentityJoin` - and only when its caller "
    "supplies the owning universe's dialect, as Run closure does. A FALSE `complete` for a path whose "
    "suffix no dialect table lists is refused THERE, before any Run-closure prerequisite runs. THEN, at "
    "Run closure, the prerequisites in their own order: the compilation-ownership axis, then the syntax "
    "grammar-capability registry, then this law as the backstop that makes the set of published "
    "universes total. Each keeps its own refusal name for the cases it is the first to decide; for the "
    "syntax universe this law is a strictly weaker necessary condition its own registry already implies, "
    "because that registry publishes that no data-document suffix appears in the syntax dialect table. "
    "An HONESTLY DISCLOSED unsupported scope is ADMITTED at both boundaries and closes its Run carrying "
    "`onUnsupportedScope`; only a false or mismatched claim refuses.")
law['refusals'] = (
    "A false `complete`, a wrong deficiency and a wrong or null cause each refuse separately and by "
    "their own name: `native.coverage-source-variant-*` at the producer boundary and "
    "`COVERAGE_SOURCE_VARIANT_*` at retained Run closure. Both name sets are retained and distinct, but "
    "they are NOT both reachable for every scope: where the producer boundary can already apply this law "
    "it refuses first, so the closure name is not reached for that case. Which name a scenario yields is "
    "decided by which boundary sees the defect first, not by a precedence among the names.")
out_is = json.dumps(S, indent=2, ensure_ascii=True) + '\n'
assert all(ord(c) < 128 for c in law['guardOrder'] + law['refusals']), 'ascii-only new text'
DISPOSITIONS.append('identity-schemas: scopeCapabilityLaw.guardOrder aligned to actual boundary order')
DISPOSITIONS.append('identity-schemas: scopeCapabilityLaw.refusals qualified for reachability')
emit(IS_REL, out_is.encode('utf-8'))

# =============================================================== native model
NM_REL = 'docs/coop/design-corrections/native/native_evidence_model.v2.py'
nm = (B / NM_REL).read_bytes()

nm = splice(nm, (PRIOR / 'v19-prose-final-coauthor.v1/scope-remedy-before.py').read_bytes(),
            (PRIOR / 'v19-prose-final-coauthor.v1/scope-remedy-after.py').read_bytes(),
            'model: agreed SCOPE_LIMIT_REMEDY.nativeContextDigests replacement applied')
nm = splice(nm, (PRIOR / 'v19-protocol-initial-coauthor.v1/initial-state-before.py').read_bytes(),
            (PRIOR / 'v19-protocol-initial-coauthor.v1/initial-state-after.py').read_bytes(),
            'model: agreed initialState splice applied (duplicate authority removed)')

# --- item 2: protocol3_run docstring
nm = splice(
    nm,
    b'    `rules` defaults to the PUBLISHED table and exists so a control can drive this same interpreter\n'
    b'    with a PERMUTED table and observe that the published ORDER is load-bearing rather than incidental.\n'
    b'    Nothing in the product supplies it; a caller passing None is the only production shape."""\n',
    b'    `rules` defaults to the PUBLISHED table and is a REFERENCE CONTROL INPUT: a control can drive this\n'
    b'    same interpreter with a PERMUTED table. The published rows are PAIRWISE DISJOINT - no two match one\n'
    b'    (phase, frame, state) - so permuting TODAY\'s rows preserves the outcome of every event, which is what\n'
    b'    that control asserts. The declared FIRST-MATCH order remains NORMATIVE, is what a conforming host\n'
    b'    implements, and is what would resolve any FUTURE row that did overlap.\n'
    b'    Nothing in the product supplies it; a caller passing None is the only production shape."""\n',
    'model: protocol3_run docstring - permuted-table control restated as outcome-preserving')

# --- item 3a + item 4: plan_native_context_digests
nm = splice(
    nm,
    b'    The Plan field is a canonical SET, and several units of one language legitimately share one context\n'
    b'    (same compiler closure, same stdlib, same effective options), so identical admitted contexts collapse\n'
    b'    to one member. That is deduplication of an identical descriptor, never of two different ones.\n',
    b'    The Plan field is a canonical SET, and two units collapse to one member EXACTLY WHEN their entire\n'
    b'    admitted context descriptor is identical - the whole record the nativeContextId is minted over, not a\n'
    b'    chosen subset of it. Sharing a compiler closure, a standard library and effective options is\n'
    b'    NECESSARY AND NOT SUFFICIENT: the TypeScript context identity also covers `configProjection`\n'
    b'    (including `configGraphPaths`), `moduleResolutionMode`, `packageModuleType`,\n'
    b'    `nodeModulesLayoutDigest` and `lockfileIdentity`, and a difference in any of them mints a different\n'
    b'    digest. That is deduplication of an identical descriptor, never of two different ones.\n',
    'model: plan_native_context_digests docstring - full context-identity equality stated')
nm = splice(
    nm,
    b'    # place it can be reported with a field, a count and a limit instead of a generic schema exception.\n',
    b'    # place it can be reported as a TYPED scope refusal with a field, a count and a limit. This is a\n'
    b'    # PRODUCER boundary and it runs BEFORE any prospective Plan is assembled, so it can refuse\n'
    b'    # `nativeContextDigests` while the other Plan arrays do not yet exist; the declaration-order rule\n'
    b'    # documented there applies among the fields PRESENT at that boundary and says nothing about this one.\n',
    'model: plan_native_context_digests comment - producer boundary precedes Plan assembly')

# --- item 3a: admit_plan_selection_cardinality bullet
nm = splice(
    nm,
    b'    * `nativeContextDigests` carries one member per DISTINCT admitted native context, and units of one\n'
    b'      language collapse only when their compiler closure, standard library and effective options are\n'
    b'      identical - which co-located units of a real monorepo routinely are not.',
    b'    * `nativeContextDigests` carries one member per DISTINCT admitted native context, and units of one\n'
    b'      language collapse only when their ENTIRE admitted context descriptor is identical - sharing a\n'
    b'      compiler closure, a standard library and effective options is necessary and not sufficient, since\n'
    b'      `configProjection` (including `configGraphPaths`), `moduleResolutionMode`, `packageModuleType`,\n'
    b'      `nodeModulesLayoutDigest` and `lockfileIdentity` are part of that identity too - which co-located\n'
    b'      units of a real monorepo routinely are not.',
    'model: admit_plan_selection_cardinality bullet - full context-identity equality stated')

# --- item 3b: admit_plan_selection_cardinality generic-exception claim
nm = splice(
    nm,
    b'    In every one of those cases the only outcome was a generic jsonschema `maxItems` ValidationError that\n'
    b'    restates the whole instance and names no field, no count, no limit and no public route - the exact defect\n',
    b'    In every one of those cases the only outcome was a generic jsonschema `maxItems` ValidationError. Such\n'
    b'    an error does carry the failing path and the bound in its own structured fields; what it lacks is the\n'
    b'    required TYPED projection - no `PROJECT.SCOPE_LIMIT` detail, no `REQUEST.UNSATISFIABLE` class or exit,\n'
    b'    no `field:count>limit` subject and no per-field remedy - and its message restates the whole\n'
    b'    instance - the exact defect\n',
    'model: admit_plan_selection_cardinality - generic-exception claim restated as missing TYPED projection')

# --- item 4: admit_plan_selection_cardinality ORDER paragraph
nm = splice(
    nm,
    b'    ORDER. `PLAN_SELECTION_FIELDS` is the published `$defs/plan` declaration order. A request that overflows\n'
    b'    two arrays at once refuses on the first of them in that fixed order, so the same request always yields the\n'
    b'    same subject and a caller narrowing one selection makes deterministic progress."""\n',
    b'    ORDER, AND THE BOUNDARY IT GOVERNS. `PLAN_SELECTION_FIELDS` is the published `$defs/plan` declaration\n'
    b'    order, and it decides the subject AT THIS BOUNDARY, among the fields actually PRESENT in the mapping\n'
    b'    passed in. On an assembled prospective Plan that is all three, so a request overflowing two of them\n'
    b'    refuses on the first in that fixed order and the same request always yields the same subject, and a\n'
    b'    caller narrowing one selection makes deterministic progress. It is NOT an ordering claim about the whole\n'
    b'    request: `plan_native_context_digests` calls this function with `nativeContextDigests` ALONE, while it is\n'
    b'    producing that field and before any prospective Plan exists, so an overflow there refuses at that earlier\n'
    b'    producer boundary whatever a later-assembled Plan would have contained. Both are the same typed refusal;\n'
    b'    only the boundary differs."""\n',
    'model: admit_plan_selection_cardinality ORDER - scoped to this boundary and its present fields')

ast.parse(nm)  # the proposed module still parses
emit(NM_REL, nm)

# =============================================================== protocol3 table
PT_REL = 'docs/coop/design-corrections/native/protocol3-transitions.v1.json'
raw_pt = (B / PT_REL).read_text(encoding='utf-8')
D = json.loads(raw_pt)
assert json.dumps(D, indent=1, ensure_ascii=True) + '\n' == raw_pt, 'protocol3 format probe'

# initialState must equal the model's literal, taken from the BEFORE model by AST
tree = ast.parse((B / NM_REL).read_text(encoding='utf-8'))
fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'protocol3_run')
lit = ast.literal_eval(next(n for n in fn.body if isinstance(n, ast.Assign)
                            and getattr(n.targets[0], 'id', None) == 'state').value)
assert len(lit) == 9 and all(isinstance(v, (str, bool, int, type(None))) for v in lit.values())

ORDER_TEXT = json.loads((PRIOR / 'v19-protocol-initial-coauthor.v1/'
                         'protocol3-transitions.proposed.json').read_text())['initializationAndUpdateOrder']
OUT = {}
for k, v in D.items():
    OUT[k] = v
    if k == 'phases':
        OUT['initialState'] = dict(lit)
        OUT['initializationAndUpdateOrder'] = ORDER_TEXT
# main's corrected matchLaw is PRESERVED verbatim; all 34 rows byte/value identical
assert OUT['matchLaw'] == D['matchLaw'] and 'PAIRWISE DISJOINT' in OUT['matchLaw']
assert json.dumps(OUT['rules'], sort_keys=True) == json.dumps(D['rules'], sort_keys=True)
assert OUT['ruleCount'] == len(OUT['rules']) == 34
for k in D:
    assert json.dumps(OUT[k], sort_keys=True) == json.dumps(D[k], sort_keys=True), k
assert set(OUT) - set(D) == {'initialState', 'initializationAndUpdateOrder'}
assert all(ord(c) < 128 for c in ''.join(ORDER_TEXT)), 'ascii-only order text'
out_pt = json.dumps(OUT, indent=1, ensure_ascii=True) + '\n'
assert json.loads(out_pt)['initialState'] == lit
DISPOSITIONS.append('protocol3 table: initialState + initializationAndUpdateOrder added; '
                    "main's corrected matchLaw preserved verbatim; all 34 rows identical")
emit(PT_REL, out_pt.encode('utf-8'))

# =============================================================== report
print('dispositions (%d):' % len(DISPOSITIONS))
for d in DISPOSITIONS:
    print('  -', d)
print()
for rel in (MD_REL, IS_REL, NM_REL, PT_REL):
    a = (B / rel).read_bytes(); b = (P / rel).read_bytes()
    print('%-62s before=%s\n%-62s after =%s  (%+d bytes)'
          % (rel, hashlib.sha256(a).hexdigest(), '', hashlib.sha256(b).hexdigest(), len(b) - len(a)))
