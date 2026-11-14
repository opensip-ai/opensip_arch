# Erratum FA2-CENSUS-E3: the population-rule carrier, and rule v3 for export entries with several declarations (author draft r1, 2026-11-14)

Status: **PROPOSED, r1.** Lead coordinator's brief (`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). It is
**additive**: no accepted byte is edited. It builds on two bound texts at architecture main `06f966a1e`:
**E1** = `../errata-2026-11-13b/ERRATUM-FA2-CENSUS-E1.md` (sha256 `1dd70aa9…3232c1`) and **E2** =
`../errata-2026-11-13c/ERRATUM-FA2-CENSUS-E2.md` (sha256 `56723546361dd29bed388b22837f57f2fbb4ae131e61a7a957544ab0ad6f031e`),
with their receipts (`RcE1`, `RcE2`). `9.8:N` is `native-successors-fa/fa-2/section-9-8.md`. `F3` is the design note's
`exported` rule, `LC/f2min/DESIGN-NOTE-r5.md:98-107`. Product facts were read at product main `e3cd0bf5` (read-only).
Part A closes gaps G1-G7 of the carrier plan (`LC/f2min/census-rule-1b/PLAN.md` §1). Part B decides question 12
(`LC/f2min/census-rule-1/QUESTIONS.md` items 12, 12 revised). Its dispositions come from 1,298 probes, not inference (FCE3.4).

## FCE3.1 Part A: the carrier of population-rule bindings

E1 states the invariant (`E1:160`): "**Each enumerator closure has exactly one population-rule binding.** It is immutable,
it is reviewed, it is available before Plan selection, and it is retained for replay." It leaves the carrier owed: "the
binding must be carried by something the closure identity or the Plan fixes. That carrier is owed" (`E1:166-167`).
Statements A1-A10 are inserted into §9.8 after E1's binding paragraph.

> **A1. The enumerator closure.** It is "the worker's provider closure, which is also the `producerClosure` of every stage the worker serves", named by the binding's `enumerator.closureId` (`9.8:27-28`). The census request carries "that enumerator's `closure2` text" (`9.8:35`). For the TypeScript provider it is the closure `P` of which E1 says "P's `closure2` covers the dist and the note's token and relation lists" (`E1:164-165`).
>
> **A2. Form.** A binding is the member of the enumerator closure's file tree at the path `opensip-interface/symbol-census/population-rule.json`. Its bytes are exactly `{"populationRule":"<rule id>","schemaVersion":1}`: UTF-8, no whitespace, no final newline (the RFC 8785 form of that object). It names exactly one rule id. Being a tree member, it is part of the closure's identity. It is not a capability token, wire member, schema, deficiency or cause (`9.8:107-108`; `E1:154`). A note does not carry a binding (`E1:163-168`).
>
> **A3. Bindable rules.** This closed table is the only source of bindable rules:
>
> | Rule id | Binds only closures whose role subprotocol is | sha256 of the A2 bytes |
> |---|---|---|
> | `native.symbol-census-population.default.v1` | `rust-semantic` | `6f2726992d65dfcf33700abcad964a9b1aad82178976ee2a2b508e66b7a84671` |
> | `native.symbol-census-population.typescript.v3` | `typescript-semantic` | `c10552a44dc8086d300fc647f8607eda22f7327f00560302d42469ca8b8f85c7` |
>
> Any other member bytes name an **unknown** rule. This includes the withdrawn `…typescript.v1` (E2 FCE2.3) and `…typescript.v2` (FCE3.3). A rule named for one provider never binds another provider's closure. The default rule is not bound to a TypeScript closure, because that provider's census does not hold the default population (`E1:44-48`). Only an erratum that states a rule in this section adds a row.
>
> **A4. Writer, and conflicting bindings.** Only the packager that builds the enumerator closure writes the member. It copies the bytes from one static source file whose sha256 the packager pins, and it refuses to build on any other bytes. A closure has **conflicting bindings** when its digest-bound token note names a `native.symbol-census-population.` id other than the member's. The packager refuses to build it. The host never parses the note. A tree holds one member per path, so no other conflict exists.
>
> **A5. When the carrier exists.** It exists for every enumerator closure from the adoption of this erratum. The interim readings of `E1:54` ("…or that has no binding while the carrier of bindings does not yet exist, is under the default rule") and `E1:160` ("Until the carrier of these bindings exists, a closure with no binding is under the default rule") then end. From then on, a census request whose enumerator closure has no valid binding is refused, under A6.
>
> **A6. Checks, by whom and when.**
> - **Plan time, by the host, before any worker is spawned or asked for a census.** For every enumerator closure from which §9.8 makes a census owed (`9.8:24-29`), the host reads the member from that closure's admitted tree. The member must be present, its sha256 must be a row of A3, and that row must bind the closure's role subprotocol.
>   - Each failure is the outcome §9.8 already gives a Plan that disagrees with its census rule: "a host invariant refused before spawn" (`9.8:29-31`). The failures are: no member (missing binding), a digest not in A3 (unknown or withdrawn rule), and a row for another subprotocol (a rule that does not fit the provider).
>   - A Plan that owes no census does not read the member.
> - **At replay, by the evaluator.** The evaluator makes the same three checks against the closure tree that the committed Run's Plan retained, using the retained bytes and never the replaying release's packaging. A failure is a host-invariant fault: the Plan is a host-generated internal layer (`foundation/evaluator-fault-contract.v3.md:11`, "Invalid host-generated internal layer"). A binding that passes gives the rule under which the retained census is read (`E1:160`: evidence "keeps that binding's rule when it is read later").
> - No key or code is registered. Refusal keys stay internal; "no public code, D9 code, deficiency or cause is added" (`9.8:107-108`).
>
> **A7. Retention.** A committed Run whose Plan owed a census retains, with each enumerator closure descriptor its Plan fixes, the tree row (path and sha256) of that closure's binding member. Under A3 the digest determines the rule. At replay, a retained `symbol` inventory whose enumerator closure has no binding member is refused under A6.
>
> **A8. Review.** A binding changes its closure's identity, so it is reviewed as part of that closure. The two independent reviewers who accept the packaging unit that produces the closure review the static source file's bytes and the packager's checks. No closure with a binding serves a census before that unit is accepted. The first binding of a rule also needs that rule's own erratum reviews (`E2:335`). For v3 these are this erratum's two reviews.
>
> **A9. Order of statement and use.** The packaging of a binding and its checks may follow the adoption of the erratum that states its rule. A census under a rule is honoured as `complete` only after the FA-2 contract successor that states that rule in §9.8 is a `contractSuccessors` entry in the product's `design-lock.json`.
>
> **A10. The end of the complete-census prohibition.** A TypeScript provider's census is honoured as `complete` exactly when all of these hold:
> 1. its enumerator closure carries one binding naming `…typescript.v3`, which passes A6 at Plan time and at replay;
> 2. that closure is the output of an accepted packaging of code accepted as conforming to v3. That code is CENSUS-RULE-1a with the fixes and golden owed by FCE3.5, and the carrier units owed by FCE3.6;
> 3. A9's successor stating E1, E2 and this erratum is bound;
> 4. the census meets §9.8 as amended (state `complete`, `examinedPaths` equal to the extent).
>
> Until then the provider sends no `complete` census, and none is honoured (`E1:160`; `RcE2:15`).

**G4, reconciled.** E1 says: "Only a rule stated in this section can be bound" (`E1:54`). It also says its rule text is
"Inserted into §9.8 … They are the rule's only statement" (`E1:66-67`), and "Adopting the law can come before
CENSUS-RULE-1. Using the narrowed `complete` claim cannot" (`E1:213-214`). E2 says "The successor carries E1 and E2, so v2 is
stated in §9.8" (`E2:22-23`). RcE2 records that successor as "still owed and not generated" (`RcE2:14`). The two texts
reconcile once *binding* (writing the member) is separated from *use* (honouring `complete`). A9 never lets use rest on
less than the bound successor, so no text needs to change.

**Considered and rejected.** §9.1 step 1's outcome ("never spawned: affected Coverage keys are `unknown /
provider-unavailable` (cause `capability-missing`)", native-evidence `:2848-2851`) was considered for A6. Using it would
stretch a registered cause past its owner's meaning ("a row lacking … any token the Plan needs"). E1 says "is refused", and
§9.8's only Plan-time refusal is the host invariant.

**What exists today** (product main `e3cd0bf5`, read-only). `tools/typescript_closure.py` and `providers/typescript/closure`
contain no "population" text (`git grep -n -i population e3cd0bf5 -- tools/typescript_closure.py providers/typescript/closure`
gives no output, exit 1). The host's Plan has no production constructor: "only the test seam below builds one, so no
production caller can construct a Plan" (`crates/host/src/plan.rs:636-637`). Rust orchestration is `Gated`
(`plan.rs:725-726`).

## FCE3.2 Part B: rule v3, statement 4 (question 12)

**The question.** Both code reviewers found it undecided. The cross-vendor reviewer wrote: "Statement 1(b) supplies no aggregation rule for
several values/declarations of one entry … That clarification should also cover several alias targets"
(`census-rule-1/review-codex/VERDICT-r7.md:9`). The Claude reviewer wrote: "v2 does not decide it, and F3 is design-note text, not bound law"
(`review-opus/VERDICT-r9.md:32`). Inserted into §9.8 as part of rule v3 (FCE3.3):

> 4. **Export entries with several declarations, and the `exported` value they give.** An export entry is one name of a module file's export table: `default`, `export=`, or a name `K`. Its declarations are every declaration in that file that the compiler binds to that name, in any spelling and in whichever of the compiler's symbols holds it. Declarations this rule excludes (C23, such as the shorthand members of `module.exports = { F }`; C24, such as `exports.x = void 0`) are not among them. Each declaration is classified by itself, by statement 1. The number and order of the declarations do not matter. The compiler's merged symbol for the entry, and the declaration the compiler resolves it by, decide nothing.
>    - (a) **Rows.** The entry is a row (`(export).K`, `(export=)`, `default`, or the row of its declared top-level name) exactly when at least one of its declarations is not an alias.
>    - (b) **Targets.** The target of an alias declaration is the symbol that its local name (statement 1(a)) or its entity name (1(b); for a chain, its rightmost name) resolves to, as v1 resolves symbols. When that symbol is itself an alias under statement 1, the target is that alias's target, taken again until a symbol is not an alias. Every alias declaration has its own target, whatever the entry's other declarations are.
>    - (c) **`exported`, for a row at a module file's top level.** The row is `exported` in any of three cases: it is an entry row under (a); one of its meanings is the target of an alias declaration of an entry of that file; or it is a "bound subject with an export symbol" (F3, `DESIGN-NOTE-r5.md:100`). Otherwise the row is `unknown` when either holds: the file's `export=` or `default` entry has a declaration that is not an alias, or an alias declaration of an entry of that file has a target that resolves to no symbol. Otherwise it is `not-exported`. Rows elsewhere (members, global and ambient homes, file rows, `#private`) are outside this statement.
>
> **F3 and this rule.** In F3 (`DESIGN-NOTE-r5.md:98-107`), "alias" is the alias of statement 1. Under v3, F3's "an alias in the export table resolves to them" and "a non-alias `export =`/`default` value" (`:101`) mean statement 4(b) and 4(c).

**Status of F3.** F3 stays a design note. This erratum binds only the two sentences above ("F3 and this rule") and
statement 4. It claims no other `exported` value as law.

**The lead's proposal, tested.** The proposal was to decide per declaration, by syntax: every alias declaration exposes its
own target, a non-alias declaration exposes the entry, and the merged symbol decides nothing. Statement 4 is that proposal,
with five additions the probes required:
1. Excluded declarations (C23, C24) do not count. Without this rule the tsc-output case `exports.foo = void 0; … exports.foo = foo` (G01) and CX-12 would gain rows or `unknown` values that the golden and both reviewers accepted.
2. Targets are followed through statement-1 aliases. Without this, the wrapped chain `import Q = N; export = (Q)` (CH2, CH4) would differ from the bare form (CH1, CH3). That would contradict statement 0 ("a wrapper never changes a classification").
3. An unresolved target makes the file's otherwise not-exported rows `unknown`. This is what the code does with one declaration (U01, U02, U06, U07), and is now stated for every declaration (U03, U04).
4. Statement 4(a) states the entry row for every file kind. In ES modules and in TypeScript `export =`, the code's row depends on declaration order (FCE3.4).
5. Statement 4 decides only top-level rows and quotes F3:100 instead of restating F3.

No row that both reviewers accepted moves (FCE3.4, controls).

## FCE3.3 Part C: rule `native.symbol-census-population.typescript.v3`; v2 withdrawn before any use

Inserted into §9.8:

> **The TypeScript population rule `native.symbol-census-population.typescript.v3` (erratum FA2-CENSUS-E3).** It is the rule `native.symbol-census-population.typescript.v2` of erratum FA2-CENSUS-E2 (sha256 `56723546361dd29bed388b22837f57f2fbb4ae131e61a7a957544ab0ad6f031e`): every sentence of v1 that v2 incorporates, and v2's statements 0-3, unchanged. It adds statement 4 and its two sentences on F3 (FCE3.2), and the carrier statements A1-A10 apply to it.

**Why a new id.** Statement 4(c) decides `exported` values that v2 left undecided, according to both reviewers. Statement
4(a) states rows for ES-module and `export =` entries with several declarations. E1 says: "Rule ids are immutable"
(`E1:54`); "an id is never re-used for another population" (`E1:132`). One could argue that an `exported` value is not
"population", so that adding it leaves v2's meaning intact. The stricter answer is taken: deciding what an id left open
changes what that id asserts, so it takes a new id. That is E2's precedent for v1 (`E2:43-47`).

**v2 is withdrawn before any use.** It stays in E2 as bound, it is never bound to any enumerator closure, and any reference
to it moves to v3. This was checked at product main `e3cd0bf5`:
- `git grep -n "symbol-census-population" e3cd0bf5` finds five lines, all in the code unit's test and its generated copy:
  - `providers/typescript/src/test/census-corpus.test.ts:60`, `:741`, `:1051` and `:1054` (the skipped `CR-GATE`, which binds nothing);
  - `providers/typescript/src/embedded/source-census.ts:334`.
- No closure carries a binding: the carrier does not exist (the population grep in FCE3.1 gives no output).
- `git grep -c "symbol-census-population.typescript.v3"` finds nothing at product `e3cd0bf5` or at architecture `06f966a1e` (exit 1 for both). `grep -rl` finds nothing in `LC/decisions` or `LC/f2min`.

The check covers only these tracked sources. It does not prove that no untracked artifact names v2. An artifact found outside
them keeps v2's interpretation and binding (as `E2:116-122`). Non-use is not the ground for anything here.

## FCE3.4 The probes: what the code does at `e3cd0bf5`

**Method.** The provider was extracted with `git archive e3cd0bf5` and compiled (TypeScript 6.0.3, Node 24.16.0). Each case
ran through both the reference harness `runCensus` and the provider's own builder `runCensusViaBuilder`. The scripts and outputs
are in `LC/decisions/LD-DEC-11-census-population/e3-probes/`:
- `probe-q12.mjs` (sha256 `3ddfd4e4…`) and `probe-q12.out.txt` (`d8404589…`);
- `probe-q12-extra.mjs` (`122dbd41…`) and `probe-q12-extra.out.txt` (`4445e511…`).

The generated tables are `fix-owed-e3.md` (`ea2e4a9b…`) and `matches-e3.md` (`746554f7…`).

**What the probe set covers.** Each case is one entry with one, two or three declarations, in every sequence (so every
order). The declaration kinds are:
- every spelling of statement 1(b);
- bare, wrapped and require- or import-declared targets;
- non-alias values;
- the unlisted spellings `exports['K'] =` and `module['exports'] =`;
- top-level `this.K =`, `Object.defineProperty(exports, 'K', …)` and a class expression;
- export specifiers, and `export var K`.

Each case was run in CommonJS JavaScript, ES-module JavaScript and TypeScript, and TypeScript `export =`. Thirty-four
hand-written cases cover C23 and C24 interplay, repeated and dotted targets, alias chains, unresolved targets, and the
golden's accepted multi-declaration rows.

**Results.** Every case is complete, with no failure, and both runners agree on all 1,298 cases.

| Family | Cases | Match v3 | Differ | With a compiler diagnostic |
|---|---|---|---|---|
| CommonJS, entry `K` (8 kinds) | 584 | 292 | 292 | 0 |
| CommonJS, entry `export=` (6 kinds) | 258 | 108 | 150 | 0 |
| ES-module JS, `default` | 155 | 19 | 136 | 148 |
| ES-module TS, `default` | 155 | 19 | 136 | 150 |
| TypeScript `export =` | 84 | 16 | 68 | 80 |
| ES-module JS / TS, named `K` | 14 / 14 | 4 / 4 | 10 / 10 | 0 / 12 |
| Hand-written | 34 | 24 | 10 | 1 |
| **Total** | **1,298** | **486** | **812** | |

**What the differences are** (`analysis-q12.txt`).
- **All 32 one-declaration cases of the generated set match.**
- **CommonJS** is the only file kind whose language permits several declarations of one entry. All 442 differences there are `exported` values of targets. No row differs. The code exposes at most one target in every one of the 842 CommonJS cases, so with two alias declarations naming different targets, all but one are `not-exported` (or `unknown`). In some orders the code also exposes the entity value of a non-alias declaration (`exports['K'] = L`, `module['exports'] = L`). Statement 4 gives neither result.
- **ES modules and `export =`.** ECMAScript makes a duplicate exported name an early error (ECMA-262, the module early errors), and the compiler reports most of these cases ("A module cannot have multiple default exports.", "Duplicate identifier 'export='.", "Duplicate identifier 'K'."). TypeScript reports none for some JavaScript files and for `export default (L1); export { L2 as default }`.
  - The census still decides these cases ("The census does not fail as a whole because a declaration of any class … is present", `E1:74`).
  - In 116 of them the code's rows differ. The entry row can depend on order: `export default L1; export default 1` gives no `default` row, while the reverse order gives one. Two alias declarations (`export default (L1); export { L2 as default }`) can also give a `default` row with the value `not-exported`.
  - In 40 of them the entry row's own value is `not-exported`.
- **Hand-written, differing:** X01, X02, X06, X07 and X08 (several targets); X10 (a dotted target listed before a bare one); CH2 and CH4 (a wrapped alias chain); U03 and U04 (an unresolved target beside a resolved one).
- **Controls that match** (accepted rows that must not move): X03 (CX-12), X04, X05, X09, X11-X15 (the golden's R7, CX-7 and CX-9 cases in both orders), G01 (the corpus's D2 tsc output), G01b, G02 (CX-10), G03-G06, CH1, CH3, CH5, U01, U02, U05, U06 and U07.

## FCE3.5 Part D: obligations, and what is not bound

**Code fix owed** (in the CENSUS-RULE-1a line, after this erratum is accepted). `exportedTargets` (`P/facts/census.ts:845-899`) must apply statement 4:
- collect an entry's declarations across the compiler's symbols for that name;
- classify each declaration by statement 1, never using `getAliasedSymbol` of the merged symbol;
- give the entry row under 4(a);
- resolve each target under 4(b) (bare and wrapped alike);
- apply 4(c)'s `unknown` rule per declaration.

The exact rows and `exported` values for each of the 812 differing cases are in `fix-owed-e3.md`. The general statement
governs, and the cases are evidence.

**Golden owed.** All 1,298 cases are owed, table-driven, with complete row maps, in both runners. Each case is written first,
and the 812 cases fail at `e3cd0bf5`. The golden's five marked cases (`census-corpus.test.ts:903`, `:921`, `:928`, `:929`,
`:960`) lose the `[UNDECIDED BY v2 …]` mark:
- the four mixed cases keep their values, which are now law;
- the two-alias case flips: `s.js#a` goes from `not-exported` to `exported`.

**References that move from v2 to v3:** `census-corpus.test.ts:60`, `:741`, `:1051` and `:1054` (`CR-GATE`); the generated
`src/embedded/source-census.ts`; and the carrier's static file and table (A3).

**Not bound by this erratum:**
- the carrier's code units: the packager and static file, the host's Plan check, the evaluator's replay check, and defence in depth at fact admission (planner units CR1b-PKG, CR1b-HOST, CR1b-H5);
- the internal keys those units use;
- the FA-2 contract successor that states E1, E2 and this erratum in §9.8, and its `design-lock.json` entry;
- the one repackaging, lane restage and inventory change;
- any F3 value other than statement 4's;
- the evaluator owner's erratum (`E1` FCE1.6).

## FCE3.6 Change log, and open points for the reviewers

**r1:** first draft. Part A closes G1 (A2, A4), G2 (A5), G3 (A6), G4 (A9), G5 (A6, A7), G6 (A8) and G7 (A3). Part B states
statement 4, and Part C defines v3 and withdraws v2. Where this draft departs from the planner's sentences:
- G2: the carrier exists from adoption, not "from the first host release that checks it", because that would tie law to a release;
- G3: the refusal is the existing host invariant, adding no `PlanOutcome` variant to the law;
- G5: replay refuses without depending on a claim that no Run exists;
- G7: the default rule binds Rust only.

**Open points:**
1. **A5 ends E1's interim default rule at adoption.** Today no production Plan exists and Rust is gated, so this is believed to cost nothing. A Rust census then needs a default binding.
2. **A6 uses the host-invariant class for a closure packaged without a binding.** The alternative is §9.1 step 1's semantic outcome, which would need the owner of cause `capability-missing`.
3. **Statement 4(c) decides values in programs the language forbids** (duplicate export names). The alternative is to leave them undecided, which both reviewers asked not to do.
4. **E2's FCE2.5 sentence "The `exported` value of each row is the one E1 gives"** has nothing in E1 to point to (E1 states no `exported` value). For statement 4's cases, v3 now gives the value.
5. **The 812 fix-owed cases** come from one general mechanism. Reviewers may prefer to rerun the scripts rather than read the table.
