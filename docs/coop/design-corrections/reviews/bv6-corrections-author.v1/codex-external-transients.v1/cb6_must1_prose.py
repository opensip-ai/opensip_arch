import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work')

# ---------------------------------------------------------------- native-evidence.md section 4.6
P = W / 'docs/v2/contracts/product-v1/native-evidence.md'
s = P.read_text(encoding='utf-8')
ANCHOR = """checks that v2 and the retained v1 oracle both yield `confidence-floor-unmet`
for `clones` at 100000 under floor 900000, and `satisfied` at 1000000.

### 4.7 Positive coverage case (`positive-static-consumer`)"""
NEW = """checks that v2 and the retained v1 oracle both yield `confidence-floor-unmet`
for `clones` at 100000 under floor 900000, and `satisfied` at 1000000.

**Where a per-requirement outcome travels, and in which vocabulary.** The result
shape is closed and total: `{satisfied: true, disclosures}` with **no**
deficiency, or `{satisfied: false, deficiency}` carrying exactly **one**
`DeficiencyV2` member chosen by the §10 precedence over every applicable cause.
There is no third shape, so a record that consumes this result has no lawful
reason to omit the value. A consumer record carrying **one requirement's own**
outcome therefore carries `DeficiencyV2` and **never** `D9Deficiency`: four of
these nine members — `derivation-policy-unmet`, `external-consumers-unknown`,
`input-closure-incomplete`, `resolution-incomplete` — have no `D9Deficiency`
member at all, and the D9-mapped value for all four is the same
`verdict-indeterminate`, so a D9-typed per-requirement field could only be
schema-invalid for four outcomes in nine, collapse those four into one, or drop
the disclosure. The current consumer is
`repair.schema.json#/$defs/EvidenceRequirement.deficiency` (workflows §6), which
names this vocabulary through the drift-checked mirror
`workflows:common#/$defs/NativeSufficiencyDeficiency` and is **required exactly
when `satisfied` is false**; the ownership, the mirror and the presence law are
published in
`native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary`.
Three things stay distinct and none replaces another: this **outcome**; the
**public D9 termination** of the Run or step that carries the requirement, which
is unchanged and still the §10 class/code columns; and the Coverage entry's own
retained **cause carrier**, which the requirement record does not copy — several
outcomes are requirement-relative and `required-relation-missing` has no entry at
all. `D9Deficiency` is not widened to carry any of this.

### 4.7 Positive coverage case (`positive-static-consumer`)"""
assert s.count(ANCHOR) == 1
P.write_text(s.replace(ANCHOR, NEW), encoding='utf-8')

# ---------------------------------------------------------- workflows-and-surfaces.md section 6
P2 = W / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
s2 = P2.read_text(encoding='utf-8')
ANCHOR2 = """`sufficiency_v2` and the §4.5 affected-target evidence, per requirement, and is
never collapsed into one flag.
"""
NEW2 = """`sufficiency_v2` and the §4.5 affected-target evidence, per requirement, and is
never collapsed into one flag.

**Which vocabulary `EvidenceRequirement.deficiency` carries, and when it is
required.** It carries the **native per-requirement sufficiency outcome** —
native §4.6's `DeficiencyV2`, named here through the drift-checked mirror
`common.schema.json#/$defs/NativeSufficiencyDeficiency` because this bundle
resolves only its own URNs. It is **required exactly when `satisfied` is false**
and **forbidden when `satisfied` is true**, which is precisely the closed result
shape `sufficiency_v2` returns; both directions are schema-enforced and admitted
again at preview before any descriptor exists. The field previously named
`D9Deficiency`, which cannot express four of the nine outcomes its only producer
emits — `derivation-policy-unmet`, `external-consumers-unknown`,
`input-closure-incomplete` and `resolution-incomplete` — leaving three conforming
readings and no document choosing between them: write the D9-mapped value, which
is `verdict-indeterminate` for **all four** and so cannot tell
`resolution-incomplete` (the outcome §4.6 step 6 mandates for a universal
negative under `unresolvedEdgePolicy=forbid` over an affected target, and the one
a destructive unused-code recipe turns on) from three unrelated causes; write the
sufficiency value and be schema-invalid; or omit the field and drop the
disclosure. Retyping this one per-requirement field is the correction.
`D9Deficiency` is **unchanged** and still carries every whole-Run and
comparison-step termination — three of its members name evaluation, baseline and
query outcomes no per-requirement evaluation can produce — and the public D9
route for a Run carrying such a requirement is still native §10's. The value is a
**disclosure, not an authorization**: `applicable` is false whenever any
requirement is unsatisfied, the exact cause is carried into that requirement's
unmet precondition so two different causes are two different remedies, the
evidence authority remains the sealed Run named by `evidenceRunId`, and any edit
to the value mints a different `repairPlanId` that no authorization names.
"""
assert s2.count(ANCHOR2) == 1
P2.write_text(s2.replace(ANCHOR2, NEW2), encoding='utf-8')
print('ok')
