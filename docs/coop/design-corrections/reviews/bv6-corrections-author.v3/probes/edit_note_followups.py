"""Codex v3 public-note follow-ups: ordering rationale, leftover comments, dangling pointer,
granularity matching, coarsening disclosure, and the over-broad carrier/only-fields claims."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/work')

# ---------------------------------------------------------- 1. identity-model ordering rationale
P = W / 'docs/coop/design-corrections/foundation/identity-model.py'
s = P.read_text(encoding='utf-8')
OLD = """                # The reported subject is the lowest by UTF-8 BYTE order, which is what the law
                # names. Python's default string comparison is by code point and would differ from
                # byte order above the BMP; canonical-JSON order would differ again because it
                # quotes and escapes. Only which subject is reported depends on this, never whether
                # the Run refuses.
"""
NEW = """                # The reported subject is the lowest by UTF-8 BYTE order, which is what the law
                # names, and the ordering is made EXPLICIT rather than inherited from a default.
                # For admitted Unicode scalar strings code-point order and UTF-8 byte order agree,
                # so this is not a correction of Python's default; what it excludes is a UTF-16
                # code-unit comparison, which CAN differ, and canonical-JSON order, which differs
                # again because it quotes and escapes. Only which subject is reported depends on
                # this, never whether the Run refuses.
"""
assert s.count(OLD) == 1
P.write_text(s.replace(OLD, NEW), encoding='utf-8')

# ---------------------------------------------------------- 2. check-identity leftover comments
Q = W / 'docs/coop/design-corrections/foundation/check-identity.py'
c = Q.read_text(encoding='utf-8')
OLD2 = """# CX-BV6-01. The DISJOINTNESS half is now DECIDED here, not merely stated. The frozen reference
# admitted a complete Run carrying two subject-scopes of ONE view with the same snapshot, relation,
# rung and both universes whose subject sets intersected, so one subject was claimed twice under one
# interpretation and every count, completeness claim and universal negative over that view
# double-counted it. `admit_coverage_result_v3` admits ONE scope and cannot see a second, so this is
# decidable only where the whole view is held: retained Run closure. The key is the PUBLISHED
# coveragePartitionLaw.partitionKey, which is the same tuple coverageTotalityLaw matches facts on.
"""
NEW2 = """# CX-BV6-01. The DISJOINTNESS half is now DECIDED here, not merely stated. The frozen reference
# admitted a complete Run carrying two subject-scopes of ONE view with the same snapshot, relation,
# rung and both universes whose subject sets intersected. What that establishes is that an INVALID
# partition was ACCEPTED: one subject was committed twice under one interpretation, so a count,
# completeness claim or universal negative read over that view CAN be ambiguous or double-counted
# depending on how a consumer joins the scopes - not that every consumer necessarily does.
# `admit_coverage_result_v3` admits ONE scope and cannot see a second, so this is decidable only
# where the whole view is held: retained Run closure. The key is the PUBLISHED
# coveragePartitionLaw.partitionKey, which is the same tuple coverageTotalityLaw matches facts on.
"""
assert c.count(OLD2) == 1
c = c.replace(OLD2, NEW2)
OLD3 = """# A scope with NO Coverage entry reaches no other membership check, so it is exactly the case a
# single-Coverage producer could never see. It is partitioned too.
"""
NEW3 = """# A scope with NO Coverage entry BYPASSES the per-Coverage producer guard - the boundary that
# could never see a second scope - although it does still reach the retained-scope ladder guard
# later in close_run. It is partitioned too.
"""
assert c.count(OLD3) == 1
c = c.replace(OLD3, NEW3)

# ---------------------------------------------------------- 3. replace the builtin/substring control
OLD4 = """# The reported subject is the lowest by UTF-8 BYTE order, which is what the law names. This is the
# discriminating case: 'A\\u0301' (combining) sorts BEFORE '\\u00c1' by both code point and byte
# order, while a supplementary-plane subject would order differently under a UTF-16-style
# comparison. Only which subject is REPORTED depends on this, never whether the Run refuses.
check('the-reported-overlapping-subject-is-lowest-by-utf8-byte-order',
      min({'\\U0001f600','\\uff21'},key=lambda x:x.encode('utf-8'))=='\\uff21'
      and 'BYTE order' in M.COVERAGE_PARTITION_LAW['refusalShape'])
"""
NEW4 = """# WHICH subject the actual guard reports when TWO subjects overlap, exercised through a full Run
# rather than by demonstrating a builtin or matching prose. The two competing strings are chosen so
# that a UTF-16 code-unit comparison would pick the OTHER one: U+FF21 is below U+1F600 in UTF-8 byte
# order and in code-point order, but a UTF-16 comparison orders the surrogate pair first. Only which
# subject is reported depends on this; whether the Run refuses does not.
_COMPETING=['\\uff21','\\U0001f600']
rejects_because('the-guard-reports-the-lowest-overlapping-subject-by-utf8-byte-order',
    lambda:partition_run(lambda s,o:s.update(subjects=sorted(set(o['subjects']+_COMPETING)))),
    'SUBJECT_SCOPE_PARTITION_OVERLAP:references@resolved-binding:\\uff21')
"""
assert c.count(OLD4) == 1
Q.write_text(c.replace(OLD4, NEW4), encoding='utf-8')

# ---------------------------------------------------------- 4. dangling map pointer
R = W / 'docs/coop/design-corrections/workflows/schemas/repair.schema.json'
d = json.loads(R.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
voc = d['$defs']['MutationOperation']['x-opensip-vocabulary']
assert voc['map'].endswith('/byCommand'), voc['map']
voc['map'] = ('workflows/schemas/repair.schema.json#/x-opensip-mutation-operation-map/'
              'byCommandGenericMutationStep')
voc['receiptOperationByStepKind'] = ('workflows/schemas/repair.schema.json#/'
                                     'x-opensip-mutation-operation-map/byStepKindReceiptOperation')
voc['fieldDomain'] = ('workflows/schemas/repair.schema.json#/x-opensip-mutation-operation-map/'
                      'admissibleGenericFieldDomain')
# native-preparation boundTo rationale: this IS an operational key.
recipes = d['x-opensip-mutation-operation-map']['receiptIdempotencyKeyByStepKind']['recipes']
recipes['native-preparation']['boundTo'] = (
    "the same immutable admitted invocation/step/project inputs. This is an OPERATIONAL key and "
    "says so: it already contains the host-minted RequestId, so it is scoped to ONE admitted "
    "invocation and step. The per-ATTEMPT identity is the ExecutionId and is deliberately NOT in "
    "this preimage, because the key is chosen per admitted invocation/step rather than per attempt - "
    "not because operational identities are excluded here, which would be false of a preimage that "
    "already carries RequestId. An earlier revision gave that wrong rationale. Each attempt remains "
    "separately identified by its own ExecutionId in the invocation record.")
recipes['import']['boundTo'] = (
    "the host-minted RequestId of the admitted invocation, the StepId which is the step position, "
    "and the ProjectId - all immutable once the invocation is admitted. This is an OPERATIONAL key "
    "scoped to that invocation and step; per-attempt identity stays with the ExecutionId in the "
    "invocation record.")
d['$defs']['MutationOperation']['x-opensip-vocabulary'] = voc
R.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

# ---------------------------------------------------------- 5. HistoryPayload "only fields" claim
C = W / 'docs/coop/design-corrections/workflows/schemas/common.schema.json'
e = json.loads(C.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
desc = e['$defs']['ImportedRequirementDeficiency']['description']
desc = desc.replace(
    "a history requirement through revisionRange and collectionScope, which are the only fields "
    "HistoryPayloadV1 has.",
    "a history requirement through revisionRange and collectionScope, which are its BOUNDS fields - "
    "HistoryPayloadV1 has others, notably its subjects, but it carries no observationWindow, "
    "observedPopulation or observability at all.")
e['$defs']['ImportedRequirementDeficiency']['description'] = desc
C.write_text(json.dumps(e, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
print('ok')
