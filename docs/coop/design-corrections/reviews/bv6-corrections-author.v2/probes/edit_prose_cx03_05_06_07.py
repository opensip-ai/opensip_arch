"""CX-BV6-03 prose, CX-BV6-05 scope of the unit prerequisite, CX-BV6-06 projection law,
CX-BV6-07 four precision corrections."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work')
NAT = W / 'docs/v2/contracts/product-v1/native-evidence.md'
WF = W / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'

s = NAT.read_text(encoding='utf-8')

# ---------------------------------------------- CX-BV6-06 + CX-BV6-03 : §4.6 projection paragraph
OLD = """**Where a per-requirement outcome travels, and in which vocabulary.** The result
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
"""
NEW = """**Where a per-requirement outcome travels, and in which vocabulary.** The full
result of `sufficiency_v2` is `{satisfied, deficiency?, disclosures, causes}`:
`causes` is returned on **both** branches — empty when satisfied — and
`disclosures` may be non-empty on the **failing** branch as well as the satisfied
one. What a consumer record carries is the **satisfaction/deficiency projection**
of that result: `satisfied`, and exactly one `DeficiencyV2` member when it is
false, chosen by the §10 precedence over every applicable cause. `causes` and
`disclosures` are **not** projected — they stay with the producer and with the
retained Coverage, and nothing here licenses dropping them. The projection is
total in the only sense a consumer needs: a failing requirement always has exactly
one reported outcome, so omitting the value is never lawful.

That projected value is a `DeficiencyV2` member and **never** `D9Deficiency`: four
of these nine — `derivation-policy-unmet`, `external-consumers-unknown`,
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

**This section owns the NATIVE relations only.** `sufficiency_v2` ranges over a
native **view**, so it is defined exactly for the thirteen native fact relations.
Repair also admits a requirement over the two **imported-evidence** relations
(`runtime-observation`, `history-change`), which mint no `fact2`, carry no
`sourceUniverse`/`targetUniverse` and have no Coverage entry — asked about one of
them, `sufficiency_v2` would only report `required-relation-missing`, which says
nothing true about an import. Those requirements have their own producer and their
own outcome vocabulary, owned by
`imported-evidence.schema.json#/x-opensip-imported-requirement-law`; the two
vocabularies are disjoint and a cross-plane value is refused at admission. This
section is not that law and does not decide those relations.

Three things stay distinct and none replaces another: this **outcome**; the
**public D9 termination** of the Run or step that carries the requirement, which
is unchanged and still the §10 class/code columns; and the Coverage entry's own
retained **cause carrier**, which the requirement record does not copy — several
outcomes are requirement-relative and `required-relation-missing` has no entry at
all. `D9Deficiency`'s enum is not widened to carry any of this.
"""
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

# ---------------------------------------------- CX-BV6-05 : scope the unit prerequisite
OLD5 = """**This table selects a MODE inside a unit; it does not discover units.** Every
row's Recognition cell is read **after** §1.4 U-1 has yielded a unit, and none of
them mints one. U-1 is the specific model"""
NEW5 = """**This table selects a MODE; it does not discover units.** No Recognition cell
mints a unit. For the five rows that name a **compilation** universe —
`ts-tsconfig`, `js-allowjs`, `js-synthesized`, `rust-cargo` and
`rust-cargo-prepared` — the cell is read **after** §1.4 U-1 has yielded a unit of
that language family, because those modes describe a program and a program needs
one. **`syntax-only` carries no such prerequisite and must not be read as if it
did:** it is the compiler-free path, it has no compilation unit at all (§1.2's
third-universe paragraph and §6.3's grammar dialect branch both depend on that),
and it is exactly what serves a repository in which U-1 yields **no** TS or Rust
unit. A file reached that way is `syntax-only` membership with `unitOrdinal: null`
under U-4, not a member of an invented unit. U-1 is the specific model"""
assert s.count(OLD5) == 1
s = s.replace(OLD5, NEW5)

# ---------------------------------------------- CX-BV6-07(4) : ADV-2 examples
OLD7 = """deliberate and is what keeps §4.6 step 3 reachable: the floor comparison is the
sufficiency evaluation's, it runs for **every** relation, and it must still decide
correctly against an entry a conforming native provider would never have emitted —
an imported or non-native contribution, or a defective provider. The named
regression case"""
NEW7 = """deliberate and is what keeps §4.6 step 3 reachable: the floor comparison is the
sufficiency evaluation's, it runs for **every** relation, and it must still decide
correctly against an entry a conforming native provider would never have emitted —
a defective or non-conforming provider, and the defensive fixture below. No
*imported* route is offered as an example and none is implied: imported evidence
is a separate plane that mints no `ViewEntryV3` at all (§7, workflows §4), so it
could not supply one of these values, and inventing such a path to explain the
wider domain would be fabricating a mechanism. The named regression case"""
assert s.count(OLD7) == 1
s = s.replace(OLD7, NEW7)
NAT.write_text(s, encoding='utf-8')

# ---------------------------------------------- CX-BV6-07(1,2,3) : the config-kind law text
P = W / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
law = d['x-opensip-config-node-kind-law']
law['whyExactAndNotThePrefixConvention'] = (
    "Both readings are natural and they disagree on real files, so one had to be chosen and written "
    "down. Exact basenames are chosen because `kind` records WHICH RECOGNIZED CONFIGURATION FILE "
    "this node is, not what a project chose to name a base; because the exact table is TOTAL, "
    "decidable from the retained path alone and identical on every filesystem, whereas a prefix rule "
    "would additionally have to decide `jsconfig.build.json`, an extensionless `tsconfig` and "
    "`tsconfig.jsonc`; and because it is the rule the selected model already derives, so publishing "
    "it changes no existing value. `other` is not a defect classification: it is the honest "
    "statement that this node's basename is neither recognized name, which is exactly what an "
    "explicitly selected custom-named configuration presents. NOTE ON SCOPE: this rationale is "
    "internal to this design. No claim is made here about what any external toolchain recognizes or "
    "what meaning it assigns to a filename convention; such a claim would be unverified from these "
    "bytes and is not needed to fix the reading."
)
law['enforcedAt'] = (
    "native_evidence_model.typescript_config_graph_faults, which READS this table rather than "
    "restating it and reports `native.config-graph-kind-contradicts-path:<path>` for any node whose "
    "declared kind is not the derived one - so a relabelled entry, a relabelled base and an asserted "
    "`tsconfig` on `tsconfig.build.json` all refuse. ORDERING, precisely: "
    "typescript_universe_retained_input_faults computes the candidate C(record) digest and compares "
    "it to the universe's tsconfigGraphHash BEFORE it calls the graph faults, and both contribute to "
    "one fault list. So a candidate hash may well be computed; what never happens is ADMISSION - the "
    "universe is not admitted and no identity is accepted while any fault stands. The earlier "
    "wording `refuse before the graph digest is used` described the wrong boundary."
)
law['driftScope'] = (
    "The MODEL and this table cannot drift, because the model reads this table rather than restating "
    "it, and a control holds the derived values against it. Agreement between this table and the "
    "PROSE in native-evidence.md section 2.2 is NOT established by that control and is not claimed "
    "here: prose agreement is a review obligation, and asserting it by substring search would be a "
    "format-sensitive test rather than evidence."
)
d['x-opensip-config-node-kind-law'] = law
P.write_text(json.dumps(d, indent=1, ensure_ascii=True) + '\n', encoding='utf-8')

# the §2.2 prose sentence that repeated the same two claims
s2 = NAT.read_text(encoding='utf-8')
OLD22 = """`tsconfig.build.json` reached as a base is `other` — the widespread
`tsconfig*.json` naming convention has no specified meaning and is deliberately
**not** the rule, since `tsconfig.json` and `jsconfig.json` are the only two
basenames the language recognizes by name. `other` is an ordinary value, not a
defect:"""
NEW22 = """`tsconfig.build.json` reached as a base is `other` — the widespread
`tsconfig*.json` naming convention is deliberately **not** the rule, because the
exact table is total and decidable from the retained path alone while a prefix
rule would additionally have to decide `jsconfig.build.json`, an extensionless
`tsconfig` and `tsconfig.jsonc`. `other` is an ordinary value, not a defect:"""
assert s2.count(OLD22) == 1
s2 = s2.replace(OLD22, NEW22)
OLD23 = """declared kind is not the derived one refuses
(`native.config-graph-kind-contradicts-path`), so neither the entry nor a base can
be relabelled."""
NEW23 = """declared kind is not the derived one refuses
(`native.config-graph-kind-contradicts-path`), so neither the entry nor a base can
be relabelled. A candidate digest may already have been computed and compared when
that fault is raised — the universe is simply never **admitted**, and no identity
is accepted, while any fault stands."""
assert s2.count(OLD23) == 1
NAT.write_text(s2.replace(OLD23, NEW23), encoding='utf-8')

# ---------------------------------------------- CX-BV6-03 : workflows §6 and §4
t = WF.read_text(encoding='utf-8')
OLD6 = """**Which vocabulary `EvidenceRequirement.deficiency` carries, and when it is
required.** It carries the **native per-requirement sufficiency outcome** —
native §4.6's `DeficiencyV2`, named here through the drift-checked mirror
`common.schema.json#/$defs/NativeSufficiencyDeficiency` because this bundle
resolves only its own URNs. It is **required exactly when `satisfied` is false**
and **forbidden when `satisfied` is true**, which is precisely the closed result
shape `sufficiency_v2` returns; both directions are schema-enforced and admitted
again at preview before any descriptor exists. The field previously named"""
NEW6 = """**Which vocabulary `EvidenceRequirement.deficiency` carries, and when it is
required.** Preview admits a requirement over **either evidence plane**, so the
field carries the vocabulary of **that requirement's** plane and the plane is
decided at admission from the relation's registry membership — the same place the
two planes are already separated — never from the value.

* **Native plane** — the thirteen native fact relations. The value is native
  §4.6's `DeficiencyV2`, named here through the drift-checked mirror
  `common.schema.json#/$defs/NativeSufficiencyDeficiency` because this bundle
  resolves only its own URNs.
* **Imported plane** — `runtime-observation` and `history-change`. Those relations
  mint no `fact2` and have no Coverage entry, so `sufficiency_v2` has nothing to
  range over and is not asked. Their outcomes are owned by
  `imported-evidence.schema.json#/x-opensip-imported-requirement-law` and mirrored
  as `common.schema.json#/$defs/ImportedRequirementDeficiency`; every member names
  an already-published import condition — evidence-kind availability,
  unmapped-only staleness, subject observability, and observation
  window/population.

The two vocabularies are **disjoint**, and a cross-plane value — a native
requirement claiming `import-unmapped-only`, or an imported one claiming
`resolution-incomplete` — is refused at admission. The schema alone cannot decide
this, because `relation` is a canonical identifier rather than an enum; it admits
either vocabulary, and the plane check is the admission's. That division is stated
rather than implied.

The value carried is the **satisfaction/deficiency projection** of its producer's
result, not that result: `sufficiency_v2` also returns `causes` on both branches
and may return `disclosures` on a failing branch, and those stay with the producer
and the retained Coverage. Presence is **typed**: `deficiency` is **required
exactly when `satisfied` is false** and **forbidden when it is true**, `satisfied`
must be an actual boolean, and an explicit `null` is refused in both branches
because a present key with a null value is not an absent key. Both boundaries — the
schema and the preview admission — decide that same law and are held equal on an
enumerated shape table. The field previously named"""
assert t.count(OLD6) == 1
t = t.replace(OLD6, NEW6)

OLD4 = """One window never establishes universal non-use;
runtime coverage is never OpenSIP Coverage. History payloads are advisory priority
inputs unless a policy predicate explicitly declares `evidenceUse` for them.
"""
NEW4 = """One window never establishes universal non-use;
runtime coverage is never OpenSIP Coverage. History payloads are advisory priority
inputs unless a policy predicate explicitly declares `evidenceUse` for them.

**A repair evidence requirement over one of these two relations has its own
owning outcome law**, `imported-evidence.schema.json#/x-opensip-imported-requirement-law`
(§6). It is separate from native §4.6 because these relations mint no `fact2` and
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
assert t.count(OLD4) == 1
WF.write_text(t.replace(OLD4, NEW4), encoding='utf-8')
print('ok')
