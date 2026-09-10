import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/v2/contracts/product-v1/native-evidence.md')
s = P.read_text(encoding='utf-8')

# ---------------------------------------------------------------------------- CB6-ADV-1
OLD1 = ("| `js-synthesized` | No `tsconfig.json`/`jsconfig.json` at the unit root; "
        "`package.json` present or any `.js/.mjs/.cjs/.jsx` file under the unit | "
        "`typescript-v2`, `configOrigin=synthesized`, `synthesizerVersion=1` | Host synthesizes "
        "`SynthesizedCompilerOptionsV1` (§2.2); Plan-bound with `DEFAULTED` provenance, disclosed "
        "in output. |")
NEW1 = ("| `js-synthesized` | Inside a `tsjs` unit already discovered by §1.4 U-1: no "
        "`tsconfig.json`/`jsconfig.json` at the unit root, so the `package.json` marker selects "
        "this mode. `.js/.mjs/.cjs/.jsx` files under that unit are program roots; they do not "
        "themselves make a unit | `typescript-v2`, `configOrigin=synthesized`, "
        "`synthesizerVersion=1` | Host synthesizes `SynthesizedCompilerOptionsV1` (§2.2); "
        "Plan-bound with `DEFAULTED` provenance, disclosed in output. |")
assert s.count(OLD1) == 1
s = s.replace(OLD1, NEW1)

ANCHOR1 = """**The syntax-only universe (CB3-MUST-3).** This column previously read"""
NEW1B = """**This table selects a MODE inside a unit; it does not discover units.** Every
row's Recognition cell is read **after** §1.4 U-1 has yielded a unit, and none of
them mints one. U-1 is the specific model — the closed `WorkspaceUnitV2` record,
the exactly-once `FileMembershipRowV1` law and the marker precedence
`tsconfig.json` > `jsconfig.json` > `package.json` — and a `tsjs` unit exists only
where a directory holds one of those three markers. So a directory of bare `.js`
files with no marker is **not** a unit: its files are `grammar-only` under U-4,
not program members, and no `js-synthesized` program is minted for them. An
earlier wording of the `js-synthesized` row read as an independent recognition
test ("`package.json` present **or** any `.js` file under the unit"), and an
implementer taking it alone would have minted units for bare-`.js` directories,
changing unit membership and therefore the Plan. The disjunct was never reachable
under U-1 — with no `tsconfig.json`, no `jsconfig.json` and no `package.json`
there is no unit for a `.js` file to be "under" — and the cell now says what it
always meant: within a U-1 unit whose marker is `package.json`, `.js` files are
program roots.

**The syntax-only universe (CB3-MUST-3).** This column previously read"""
assert s.count(ANCHOR1) == 1
s = s.replace(ANCHOR1, NEW1B)

# ---------------------------------------------------------------------------- CB6-ADV-2
OLD2 = """`native.confidence.v1` is the versioned, conformance-bound method
"declared-exact: every admitted checked fact is 1000000 under its universe; no
value below 1000000 is produced by a native provider". Rule authors express
"declared types only" through `derivationPolicy=declared-only` (§4.2), which
yields the typed `derivation-policy-unmet` deficiency, not a fake percentage.
`checkJs` is recorded because it changes diagnostics, not derivation.
"""
NEW2 = """`native.confidence.v1` is the versioned, conformance-bound method
"declared-exact: every admitted checked fact is 1000000 under its universe; no
value below 1000000 is produced by a native provider". Rule authors express
"declared types only" through `derivationPolicy=declared-only` (§4.2), which
yields the typed `derivation-policy-unmet` deficiency, not a fake percentage.
`checkJs` is recorded because it changes diagnostics, not derivation.

**The two clauses have different scopes, and the second is deliberately the wider
one.** The first names the method of `TypeDerivationV1`, whose
`confidenceMillionths` is a schema **constant** `1000000` and whose
`confidenceMethod` is the constant `native.confidence.v1`: that record exists only
on a `types@checked` fact. The second — *no value below 1000000 is produced by a
native provider* — is **not** narrowed to `types@checked`. It is a **provider
emission law** over this whole bundle: no native provider of any relation emits a
confidence below 1000000, because a native fact is exact under its admitted
universe and this design publishes no calibrated probability for any relation. It
is not read as types-scoped, and reading it that way would be a *weakening* — it
would permit a native `clones` or `references` provider to emit a fabricated
percentage, which is exactly what §4.8 removed.

That leaves `ViewEntryV3.confidenceMillionths`, whose domain is the full integer
range 0…1000000 and which carries **no** `confidenceMethod`. The wider domain is
deliberate and is what keeps §4.6 step 3 reachable: the floor comparison is the
sufficiency evaluation's, it runs for **every** relation, and it must still decide
correctly against an entry a conforming native provider would never have emitted —
an imported or non-native contribution, or a defective provider. The named
regression case
`sufficiency-v2-confidence-floor-precedes-one-rung-existential-shortcut` is
exactly that: a hand-built evaluator input, **not** a `ViewEntryV3` and **not**
provider emission, exercising `clones` at 100000 against a floor of 900000 so that
the removed early exit cannot come back. Its 100000 is therefore no counterexample
to the emission law and is not evidence that any native provider emits such a
value; it is a defensive fixture for the evaluator, and this contract makes no
claim that the product emits it.
"""
assert s.count(OLD2) == 1
s = s.replace(OLD2, NEW2)

# ---------------------------------------------------------------------------- CB6-ADV-3
OLD3 = """`docs/coop/artifacts/d9-exit-contract.v1.14.json` keeps its bytes; publishing the
successor D9 **artifact** remains that unit's, and this is the normative law the
product source carries meanwhile.
"""
NEW3 = """`docs/coop/artifacts/d9-exit-contract.v1.14.json` keeps its bytes; publishing the
successor D9 **artifact** remains that unit's, and this is the normative law the
product source carries meanwhile.

**That successor artifact is a live, mandatory cross-unit obligation, not a
deferred nicety, and it is recorded here so no later pass can mistake it for
one.** Two things are distinguished. *Now*: the selected composition above is
complete and self-sufficient as the law the product source carries — the schema,
the workflow mapper and the route registry agree, the extension is checked against
the inherited contract, and nothing is left for an implementer to choose. *Owed*:
the D9 unit must publish a successor artifact carrying the `host-invariant`
member, because a checker reading `d9-exit-contract.v1.14.json` **alone** would
refuse a lawful `host-invariant` operational-failed termination — the inherited
enum does not contain the cause. Until that artifact exists, the mismatch is a
**disclosed, attributed** integration obligation of that unit and a qualification
item, and it is carried forward as such rather than being closed by repinning the
inherited bytes. Editing the historical artifact to agree would destroy the very
evidence that this is an extension and would make the inheritance claim
unverifiable; the bytes stay exactly as they are.
"""
assert s.count(OLD3) == 1
s = s.replace(OLD3, NEW3)

P.write_text(s, encoding='utf-8')
print('ok')
