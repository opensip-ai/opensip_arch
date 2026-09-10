"""CX-BV6-01 precisions (1)(2)(3) from the Codex note, and the CX-BV6-03 prose corrections."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work')

# ------------------------------------------------------------ CX01 (1)(2)(3): the published law
P = W / 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
law = d['x-opensip-relation-registry']['coveragePartitionLaw']
law['whyItIsNeeded'] = (
    "The clause was stated and nothing derived or compared it. A retained Run could carry two "
    "subject-scopes of ONE view with the same snapshot, relation, rung and both universes whose "
    "subject sets intersect, and close. What that demonstrates is that an INVALID partition was "
    "ACCEPTED: the same subject was committed twice under one interpretation, so a claim read over "
    "that view - a count, a completeness claim or a universal negative - can be ambiguous or "
    "double-counted depending on how a consumer joins the scopes. It is NOT asserted that every "
    "consumer necessarily double-counts; what is established, and what this law fixes, is that the "
    "published partition property was not decided anywhere. That is the same defect class as the "
    "frozen-reference file@enumerated omission."
)
law['scope'] = (
    "PER VIEW, over every subject-scope the view references - INCLUDING scopes that carry no "
    "Coverage entry. A scope with no Coverage bypasses the per-Coverage PRODUCER guard "
    "(admit_coverage_result_v3 is never called for it), which is exactly the case a single-Coverage "
    "producer cannot decide; it does still reach the retained-scope ladder guard "
    "(SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER) later in close_run, so saying it reaches no other "
    "check at all would be false. Distinct views of one Run may reference the SAME scope, and that "
    "is not an overlap: a view is one producer's interpretation, and the partition is a property of "
    "that interpretation."
)
law['refusalShape'] = (
    "SUBJECT_SCOPE_PARTITION_OVERLAP:<relation>@<rung>:<lowest overlapping subject by UTF-8 BYTE "
    "order>, matching the COVERAGE_INVENTORY_TOTALITY_OMITS_PATH shape. The ordering is named "
    "exactly: it is the byte order of the subject's UTF-8 encoding, the same order the "
    "x-opensip-order `utf8` vocabulary names, and it is NOT the canonical-JSON encoded order, which "
    "escapes and quotes and can differ. Only which subject is REPORTED depends on it; whether the "
    "Run refuses does not. It is an internal admission refusal: no public DomainDetailCode and no D9 "
    "class, exit or error code is added or changed."
)
P.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

# ------------------------------------------------------------ CX01 (2): the implementation
Q = W / 'docs/coop/design-corrections/foundation/identity-model.py'
s = Q.read_text(encoding='utf-8')
OLD = """            overlapping=seen.intersection(scope['subjects'])
            if overlapping:
                raise C.AdmissionError(COVERAGE_PARTITION_LAW['refusal']+':'+scope['relation']+'@'
                                       +scope['resolution']+':'+sorted(overlapping)[0])
"""
NEW = """            overlapping=seen.intersection(scope['subjects'])
            if overlapping:
                # The reported subject is the lowest by UTF-8 BYTE order, which is what the law
                # names. Python's default string comparison is by code point and would differ from
                # byte order above the BMP; canonical-JSON order would differ again because it
                # quotes and escapes. Only which subject is reported depends on this, never whether
                # the Run refuses.
                first=min(overlapping,key=lambda subject:subject.encode('utf-8'))
                raise C.AdmissionError(COVERAGE_PARTITION_LAW['refusal']+':'+scope['relation']+'@'
                                       +scope['resolution']+':'+first)
"""
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)
OLD2 = """        # Scopes with NO Coverage entry are included deliberately: they reach no other membership
        # check. The map is per VIEW, so two views of one Run may reference the same scope.
"""
NEW2 = """        # Scopes with NO Coverage entry are included deliberately: they bypass the per-Coverage
        # PRODUCER guard, which is the boundary that cannot see a second scope. They do still reach
        # the retained-scope ladder guard below, so this is not their only check. The map is per
        # VIEW, so two views of one Run may reference the same scope.
"""
assert s.count(OLD2) == 1
Q.write_text(s.replace(OLD2, NEW2), encoding='utf-8')

# ------------------------------------------------------------ CX01: identity section 3 prose
R = W / 'docs/v2/contracts/product-v1/identity-and-evidence.md'
t = R.read_text(encoding='utf-8')
OLD3 = """Three boundaries of that rule matter and are held by controls. It is **per view**:
two views of one Run may reference the same scope, because a view is one
producer's interpretation. It covers **every scope the view references, including
scopes with no Coverage entry** — precisely the case that reaches no other
membership check. And it is decided **here, not by the producer**: Coverage
admission sees one scope and its one entry, so it cannot decide a property that
holds between two scopes; a law nothing compares is the defect this closes.
"""
NEW3 = """Three boundaries of that rule matter and are held by controls. It is **per view**:
two views of one Run may reference the same scope, because a view is one
producer's interpretation. It covers **every scope the view references, including
scopes with no Coverage entry** — those bypass the per-Coverage *producer* guard,
though they still reach the retained-scope ladder check. And it is decided
**here, not by the producer**: Coverage admission sees one scope and its one
entry, so it cannot decide a property that holds between two scopes; a law nothing
compares is the defect this closes.
"""
assert t.count(OLD3) == 1
R.write_text(t.replace(OLD3, NEW3), encoding='utf-8')

# ------------------------------------------------------------ CX03 prose: §4 and §6 corrections
V = W / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
u = V.read_text(encoding='utf-8')
OLD4 = """(§6). It is separate from native §4.6 because these relations mint no `fact2` and
carry no Coverage, and its five outcomes each name a condition stated above:
evidence-kind availability, unmapped-only staleness, subject observability, and
observation window/population. Two limits carry over unchanged and are enforced
rather than assumed. A **satisfied** imported requirement is positive, bounded
evidence and is **never** a universal negative — `observable-unhit` is not unused
and one window is not universal non-use — so no imported requirement, satisfied or
not, can make an unsafe `delete`/`replace` applicable: that gate stays the evidence
Run's own native `ClosedWorldV2` (§6). And **required versus optional** stays where
`evidenceUse` puts it: an optional absence remains the `IMPORT.ABSENT_FOR_PREDICATE`
disclosure and is not a gating deficiency.
"""
NEW4 = """(§6). It is separate from native §4.6 because these relations mint no `fact2` and
carry no Coverage, and **each kind is projected through its own payload**: a
runtime requirement reads `observability`, `observationWindow` and
`observedPopulation`; a history requirement reads `revisionRange` and
`collectionScope`, which are the only fields `HistoryPayloadV1` has. Neither kind
may report the other's outcomes.

Four limits carry over unchanged and are enforced rather than assumed.
**Satisfied does not mean positive**: `observed-hit` is positive execution
evidence and `observable-unhit` is *bounded negative* evidence, both can satisfy,
and the disclosure records which did. **No imported observation establishes a
universal negative** — one window is not universal non-use — and imported evidence
can never *by itself* establish the native closed world or authorize an unsafe
`delete`/`replace`: that gate stays the evidence Run's own `ClosedWorldV2` (§6).
It may still be an **additional required condition** alongside an
already-established native basis, so it is wrong to say it never affects
applicability; an unsatisfied imported requirement makes an otherwise-eligible
plan inapplicable. **Whole-versus-partial** is the requirement's existing
`completeness`: `complete` needs every plan target supported, `partial-acceptable`
at least one. And **required versus optional** stays where `evidenceUse` puts it —
an optional absence remains the `IMPORT.ABSENT_FOR_PREDICATE` disclosure, is
satisfied *by absence* rather than by evidence, and an unsupplied declaration is
read as **required**, never silently as optional.
"""
assert u.count(OLD4) == 1
u = u.replace(OLD4, NEW4)
OLD6 = """  as `common.schema.json#/$defs/ImportedRequirementDeficiency`; every member names
  an already-published import condition — evidence-kind availability,
  unmapped-only staleness, subject observability, and observation
  window/population.
"""
NEW6 = """  as `common.schema.json#/$defs/ImportedRequirementDeficiency`; every member names
  an already-published import condition and is bound to the payload field that
  grounds it, and each kind reports only the outcomes **its own** payload can
  ground (§4). The requirement record gains no field: plan `targets` supply the
  per-target scope, its existing `completeness` decides whole-versus-partial, and
  `evidenceUse` supplies required-versus-optional.
"""
assert u.count(OLD6) == 1
V.write_text(u.replace(OLD6, NEW6), encoding='utf-8')
print('ok')
