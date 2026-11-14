# Erratum FA2-CENSUS-E3: the population-rule carrier, and rule v3 for export entries with several declarations (author draft r4, 2026-11-14)

Status: **PROPOSED, r4** (r3 `88701f114` plus `review-codex-e3/VERDICT-r3.md` E3-R3-CX-1 and `review-opus-e3/VERDICT-r3.md` R3-1 and advisories; the round history is in `LC/decisions/LD-DEC-11-census-population/ERRATUM-E3-HANDOFF.md`). Lead coordinator's brief (`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). It is
**additive**: no accepted byte is edited. It builds on two bound texts at architecture main `06f966a1e`:
**E1** = `../errata-2026-11-13b/ERRATUM-FA2-CENSUS-E1.md` (sha256 `1dd70aa9…3232c1`) and **E2** =
`../errata-2026-11-13c/ERRATUM-FA2-CENSUS-E2.md` (sha256 `56723546361dd29bed388b22837f57f2fbb4ae131e61a7a957544ab0ad6f031e`),
with their receipts (`RcE1`, `RcE2`). `9.8:N` is `native-successors-fa/fa-2/section-9-8.md`. `F3` is the design note's
`exported` rule, `LC/f2min/DESIGN-NOTE-r5.md:98-107`. Product facts were read at product main `e3cd0bf5` (read-only).
Part A closes gaps G1-G7 of the carrier plan (`LC/f2min/census-rule-1b/PLAN.md` §1). Part B decides question 12
(`LC/f2min/census-rule-1/QUESTIONS.md` items 12, 12 revised). Its dispositions come from 1,327 probes, not inference (FCE3.4).

## FCE3.1 Part A: the carrier of population-rule bindings

E1 states the invariant (`E1:160`): "**Each enumerator closure has exactly one population-rule binding.** It is immutable,
it is reviewed, it is available before Plan selection, and it is retained for replay." It leaves the carrier owed: "the
binding must be carried by something the closure identity or the Plan fixes. That carrier is owed" (`E1:166-167`).
Statements A1-A10 are inserted into §9.8 after E1's binding paragraph.

> **A1. The enumerator closure.** It is "the worker's provider closure, which is also the `producerClosure` of every stage the worker serves", named by the binding's `enumerator.closureId` (`9.8:27-28`). The census request carries "that enumerator's `closure2` text" (`9.8:35`). For the TypeScript provider it is the closure `P` of which E1 says "P's `closure2` covers the dist and the note's token and relation lists" (`E1:164-165`).
>
> **A2. Form.** A binding is the member of the enumerator closure's file tree at the path `opensip-interface/symbol-census/population-rule.json`. Its bytes are exactly `{"populationRule":"<rule id>","schemaVersion":1}`: UTF-8, no whitespace, no final newline (the RFC 8785 form of that object). It names exactly one rule id. Being a tree member, it is part of the closure's identity. It is not a capability token, wire member, schema, deficiency or cause (`9.8:107-108`; `E1:154`). A note does not carry a binding (`E1:163-168`). A member binds its rule (`E1:54`) only once that rule is stated in this section (A9); before that it is a packaged member that binds nothing.
>
> **A3. Bindable rules (prospective).** From adoption, this closed table is the only source of rules that packaging may write and a Plan may admit. It governs packaging and Plan admission only; replay is A7's. A closure's role subprotocol is that of the universe of the Plan's available binding that names the closure as its `enumerator.closureId` (`9.8:24-28`; `typescript-semantic` or `rust-semantic`, `9.8:15`), not the closure record's `role`.
>
> | Rule id | Binds only closures whose role subprotocol is | sha256 of the A2 bytes |
> |---|---|---|
> | `native.symbol-census-population.default.v1` | `rust-semantic` | `6f2726992d65dfcf33700abcad964a9b1aad82178976ee2a2b508e66b7a84671` |
> | `native.symbol-census-population.typescript.v3` | `typescript-semantic` | `c10552a44dc8086d300fc647f8607eda22f7327f00560302d42469ca8b8f85c7` |
>
> Any other member bytes name an **unknown** rule for packaging and Plan admission. This includes the withdrawn `…typescript.v1` (E2 FCE2.3) and `…typescript.v2` (FCE3.3). Withdrawal is prospective: it never changes how a retained binding is read (A7). A rule named for one provider never binds another provider's closure. The default rule is not bound to a TypeScript closure, because that provider's census does not hold the default population (`E1:44-48`). Only an erratum that states a rule in this section adds a row.
>
> **A4. Writer, and conflicting bindings.** Only the packager that builds the enumerator closure writes the member. It copies the bytes from one static source file whose sha256 the packager pins, and it refuses to build on any other bytes. A closure has **conflicting bindings** when its digest-bound token note names a `native.symbol-census-population.` id other than the member's. "Names" means that the note's bytes contain the prefix `native.symbol-census-population.` followed by an id, anywhere, prose included, so a note that mentions a withdrawn id is refused. The packager refuses to build it. The host never parses the note. A tree holds one member per path, so no other conflict exists.
>
> **A5. When the carrier exists.** It exists for every enumerator closure from the adoption of this erratum. The interim readings of `E1:54` ("…or that has no binding while the carrier of bindings does not yet exist, is under the default rule") and `E1:160` ("Until the carrier of these bindings exists, a closure with no binding is under the default rule") then end. From then on, a census request whose enumerator closure has no valid binding is refused, under A6.
>
> **A6. Plan-time checks (prospective).** At Plan time, the host checks before any worker is spawned or asked for a census, for every enumerator closure from which §9.8 makes a census owed (`9.8:24-29`). It reads the member from that closure's admitted tree, and four conditions must hold:
>   1. the member is present;
>   2. its sha256 is a row of A3;
>   3. that row binds the closure's role subprotocol;
>   4. the FA-2 contract successor that states the row's rule in §9.8 is a `contractSuccessors` entry of the host's own design lock (A9).
>
>   Each failure takes the existing outcome of `9.8:29-31`: "A Plan that binds such a universe to another enumerator, or that disagrees with this rule, is a host invariant refused before spawn." The failures are a missing binding (1), an unknown or withdrawn rule (2), a rule that does not fit the provider (3) and a rule not yet stated (4). How the host tells which `contractSuccessors` entry states a rule is the host's carrier unit's (CR1b-HOST); the law fixes only the condition. A Plan that owes no census does not read the member. Nothing is registered: refusal keys stay internal, and "no public code, D9 code, deficiency or cause is added" (`9.8:107-108`).
>
> **A7. Retention and replay.** A committed Run whose Plan owed a census retains, with each enumerator closure descriptor its Plan fixes, the tree row (path and sha256) of that closure's binding member, when there is one. At replay, the evaluator reads the retained digest and the closure's retained identity and review evidence, never the replaying release's packaging or today's A3 table. The retained records carry no design-lock identity, so A7 claims only the historical *interpretation* of a rule (`E1:160`: evidence "keeps that binding's rule when it is read later"). It does not re-verify that the original host passed A6 check 4.
>
> **Binding class: one ordered procedure.** At replay, each retained enumerator closure has exactly one binding class. The class is the first of these steps that applies:
>    1. **Conflict.** There is an A2 member and also a record presented as another binding of the same closure → *unrecognized*. `E1:160` allows "exactly one population-rule binding" and refuses "conflicting bindings", so the stricter step comes first. This is the one place the order departs from "A2 first".
>    2. **A2 member.** There is an A2 member → its class is the rule id its bytes are the A2 form of: *v1*, *v2*, *v3* or *default*. Bytes that are the A2 form of no rule are *other id*.
>    3. **Demonstrated historical binding.** There is no A2 member, and a record presented as a binding is *demonstrated*: its retained identity and review evidence are present, and a reader for its owning law reads them as meeting `E1:160` and `E1:166-167` (one per closure; immutable; reviewed; available before Plan selection; retained for replay; fixed by the closure identity or the Plan; naming a rule stated in §9.8) → *historical*.
>    4. **Presented but not demonstrated.** There is no A2 member, and a record is presented as a binding but is not demonstrated (no reader, evidence lost or silent, or the conditions are not met) → *unrecognized*.
>    5. **Otherwise** (nothing presented; this includes lost or silent closure evidence) → *none*.
>
> **The replay table is total.** Each row is stated over the provider, the class and the census with its inventory, so the rows are disjoint by construction. Every state has exactly one row, or exactly one of these "cannot occur" reasons:
> - a complete census with a host-derived inventory cannot occur, because a complete census is projected with origin provider-return (`9.8:82-91`);
> - an over-bound census with a host-derived inventory cannot occur, because an over-bound census arrives on `Complete` and takes the scope-limit route (`9.8:60-62`, `:99-101`), while host-derived outcomes belong to the other terminals (`9.8:75-80`);
> - a provider-reported inventory with no census cannot occur, because a terminal that carries no census gives host-derived inventories only (`9.8:75-80`).
>
> | Row | Provider | Class | Complete census | Over-bound census | No census (host-derived) |
> |---|---|---|---|---|---|
> | RT-1 | `typescript-semantic` | *v3* | O1 | O2 | O3 |
> | RT-2 | `rust-semantic` | *default* | O1 | O2 | O3 |
> | RT-3 | `rust-semantic` | *none* | O1, default rule (`E1:54`'s interim reading; the same population as `default.v1`) | O2, default rule | O3 |
> | RT-4 | `typescript-semantic` | *none* | O4 | O5 | O3 |
> | RT-5 | `typescript-semantic` | *v1* or *v2*: neither ever could bind. v1 "is never bound to any enumerator closure" (`E2:103-104`). v2 bound nothing before its successor (A9; `E2:22-23`), and FCE3.3 withdraws it while that successor is still owed | O4; the member fixes only the rule's interpretation (`E2:120-121`) | O5; the same | O3 |
> | RT-6 | either | *historical* | O7 | O7 | O3 |
> | RT-7 | `typescript-semantic` | *default*, *other id* or *unrecognized* | O6 | O6 | O3 |
> | RT-7 | `rust-semantic` | *v1*, *v2*, *v3*, *other id* or *unrecognized* | O6 | O6 | O3 |
>
> The outcomes are these:
> - **O1.** The census is read under the row's rule and goes to §9.8's projection and admission unchanged (`9.8:82-96`).
> - **O2.** The census is read as a count of the row's rule's population. Its record takes the scope-limit route (`9.8:99-101`), and that route's owner decides it.
> - **O3.** The host-derived inventory (`9.8:76-79`) carries no census and no rows. It is read as its owner admits it, with no population rule, and the binding is not consulted.
> - **O4.** The complete census is not admitted, on the producer route of `foundation/evaluator-fault-contract.v3.md:12`. The ground is `E1:160` ("sends no `complete` census, under any rule, until its binding exists"), together with a binding that is absent (RT-4: none is demonstrated) or that could never bind (RT-5). The route is not a finding of whose fault it was: after adoption, A6 checks 1-2 also refused such a Plan, and replay cannot date a Plan.
> - **O5.** The over-bound census's counts are not read as a count of any rule's population. Its record takes the scope-limit route (`9.8:99-101`), which asserts no completeness.
> - **O6.** Fail closed: the census is not admitted, and its counts are not read under any rule. This erratum makes no producer or host-fault finding, because an unrecognized representation by itself proves neither the absence of a binding nor a breach. The route depends on the failure, and each is taken by its established owner:
>   - where referenced promised retained bytes are lost, `EvidenceUnavailable` (`evaluator-fault-contract.v3.md:13`);
>   - otherwise, "admission refusal under their actual external or producer boundary" (`:14`).
> - **O7.** The binding keeps its rule, and the census is read as O1 or O2 under it, by the reader of step 3.
>
> From adoption, A2 is the only representation that packaging may write (A2-A4, A6).
>
> **A8. Review.** A binding changes its closure's identity, so it is reviewed as part of that closure. The two independent reviewers who accept the packaging unit that produces the closure review the static source file's bytes and the packager's checks. No closure with a binding serves a census before that unit is accepted. The first binding of a rule also needs that rule's own erratum reviews (`E2:335`). For v3 these are this erratum's two reviews.
>
> **A9. "Stated in this section" (`E1:54`) for an adopted erratum.** Take a rule that an adopted erratum amending this section states, while the FA-2 contract successor that carries that erratum is still owed. That rule is not yet "stated in this section" (`E2:22-23`: the successor carries the errata, "so v2 is stated in §9.8"). Until that successor is a `contractSuccessors` entry of the design lock:
>   - the rule's A2 member may be written, packaged, reviewed and tested, but it binds nothing;
>   - every Plan that owes a census from its closure is refused by A6 check 4.
>
>   Once that entry exists, the rule is stated in this section, its member binds it, and a census under it may be requested.
>
> **A10. The end of the complete-census prohibition.** A TypeScript provider's census is admitted as `complete` only when all three hold:
>   1. it is the census of a Plan that passed A6's four checks with a binding naming `…typescript.v3`;
>   2. its closure is the output of a packaging unit accepted under A8, of code accepted as conforming to v3 (CENSUS-RULE-1a with FCE3.5's fixes and golden, and the carrier units);
>   3. it meets §9.8 as amended (`complete`, `examinedPaths` equal to the extent).
>
>   A6 refuses any other Plan that owes a census before spawn, so no other census is requested. At replay, A7 decides. Until then the provider sends no `complete` census (`E1:160`; `RcE2:15`).

*Commentary from here to FCE3.2 (not inserted into §9.8).*

**G4, reconciled.** E1 says: "Only a rule stated in this section can be bound" (`E1:54`). It also says its rule text is
"Inserted into §9.8 … They are the rule's only statement" (`E1:66-67`), and "Adopting the law can come before
CENSUS-RULE-1. Using the narrowed `complete` claim cannot" (`E1:213-214`). E2 says "The successor carries E1 and E2, so v2 is
stated in §9.8" (`E2:22-23`), and RcE2 records that successor as "still owed and not generated" (`RcE2:14`). A9 reads `E1:54`
with E2: an adopted erratum's rule is stated in §9.8 only through its bound successor. So a written member binds nothing
before then, and A6 check 4 enforces this at Plan time. The texts reconcile, and none needs to change.

**A6 and A7 together.** A3 and A6 decide what may be packaged and requested from adoption on. A7 decides only what
retained evidence means, and its table is total.
- A prospective withdrawal, path or table never turns a binding that was valid when it was made into a fault (RT-6, O7).
- Replay never admits a census that no binding could have made complete (RT-4, RT-5).
- An unrecognized representation fails closed without being called a breach (RT-7).

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
>    - (b) **Targets, by a finite walk.** The walk starts at the symbol that the declaration's local name (statement 1(a)) or entity name (1(b); for a chain, its rightmost name) resolves to, as v1 resolves symbols.
>      - A symbol that is not an alias under statement 1 is a target.
>      - A symbol that is an alias is followed to the symbols that its own alias declarations name, resolved the same way. A symbol with several such declarations gives the targets of all of them.
>      - Unlike an export entry (above), an intermediate alias is not collected across compiler symbols. Its declarations are those of the one compiler symbol that its name resolves to. A same-name declaration that the compiler binds to another symbol (a duplicate identifier) or in another scope (shadowing) is not followed (CY-05, CY-05r, CY-06). In a duplicate-identifier program, "resolves to" means the pinned compiler's resolution, so declaration order can change the result. That is the stated law for v3: the result is a fixed function of the source under the pinned compiler, and such programs are censused (`E1:74`).
>      - Cycles are detected per path. A step to a symbol already on the chain being walked ends that branch with no target. A symbol already completed by another branch gives its completed result again, both its targets and whether it is unresolved. Reaching a symbol twice is not a cycle (RC-01 to RC-04).
>      - A branch that ends in a cycle, or at a step that resolves to no symbol, makes the declaration **unresolved** (CY-01, CY-04, RC-05).
>      - The walk is finite: each path visits each symbol at most once, and a program has finitely many symbols.
>
>      Every alias declaration has its own targets, whatever the entry's other declarations are. A declaration can have targets and be unresolved at once.
   - (c) **`exported`, for a row at a module file's top level.** The row is `exported` in any of three cases: it is an entry row under (a); one of its meanings is the target of an alias declaration of an entry of that file; or it is a "bound subject with an export symbol" (F3, `DESIGN-NOTE-r5.md:100`). Otherwise, the row is `unknown` when either of two conditions holds:
>      - the file's `export=` or `default` entry has a declaration that is not an alias and whose value is an expression: an `export default` or `export =` expression, or an assignment to `module.exports` in any spelling. A class, function or interface declaration exported as `default` (`export default class C {}`, `export default function () {}`) is not such a value;
>      - an alias declaration of an entry of that file is unresolved under (b).
>
>      Otherwise it is `not-exported`. A row that is a target is `exported` even when another declaration is unresolved. Rows elsewhere (members, global and ambient homes, file rows, `#private`) are outside this statement.
>
> **F3 and this rule.** In F3 (`DESIGN-NOTE-r5.md:98-107`), "alias" is the alias of statement 1. Under v3, F3's "an alias in the export table resolves to them" and "a non-alias `export =`/`default` value" (`:101`) mean statement 4(b) and 4(c).

**Status of F3.** F3 stays a design note. This erratum binds only statement 4 and the two sentences above ("F3 and this
rule"). Outside statement 4, no `exported` value is law. E2's FCE2.5 sentence ("The `exported` value of each row is the one
E1 gives") is a golden instruction, now satisfied for statement 4's rows only.

*The proposal it tests, and the additions the probes required, are recorded in the handoff (not inserted).* No row that both reviewers accepted moves (FCE3.4, controls).

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
them keeps v2's interpretation and binding (as `E2:116-122`). At replay it is read as A7 says. An A2 member naming v2
has its interpretation fixed but could not bind (RT-5). A demonstrated historical binding in another representation is RT-6,
and an unrecognized representation is RT-7. Non-use is not the ground for anything
here.

## FCE3.4 The probes (evidence, not inserted)

The probes were read-only, at product `e3cd0bf5` (TypeScript 6.0.3), through both runners (`runCensus`, `runCensusViaBuilder`).
The scripts, outputs and generated tables are in `LC/decisions/LD-DEC-11-census-population/e3-probes/`:
- `probe-q12.mjs` (sha256 `3ddfd4e4…`) and its output `probe-q12.out.txt` (`d8404589…`);
- `probe-q12-extra.mjs` (`4db56268…`) and its output `probe-q12-extra.out.txt` (`8e58aee9…`);
- `fix-owed-e3.md` (`f67d5d83…`) and `matches-e3.md` (`82dafc38…`);
- `replay-table.py` (`998c8618…`) and its output `replay-table.out.txt` (`6e81ffab…`): 1,728 concrete states, every one with exactly one row or "cannot occur" reason.

There are 1,327 cases: 513 match v3 and 814 differ. Every case is complete, and the runners agree on every case. Member
values in the expected maps (`N.v`, `N1.a`, `I~a`, `C.s`) are F3's: they are golden instruction, not v3 law. The families,
the controls and the analysis are in the handoff.

## FCE3.5 Part D: obligations, and what is not bound

**Code fix owed** (in the CENSUS-RULE-1a line, after this erratum is accepted). `exportedTargets` (`P/facts/census.ts:845-899`) must apply statement 4:
- collect an entry's declarations across the compiler's symbols for that name;
- classify each declaration by statement 1, never using `getAliasedSymbol` of the merged symbol;
- give the entry row under 4(a);
- resolve each target under 4(b) (bare and wrapped alike; a finite walk; several declarations of an intermediate alias);
- apply 4(c)'s `unknown` rule per declaration, triggered only by expression values and unresolved declarations.

The exact rows and `exported` values for each of the 814 differing cases are in `fix-owed-e3.md`. The general statement
governs, and the cases are evidence.

**Golden owed.** All 1,327 cases are owed, table-driven, with complete row maps, in both runners. They include the r2
declaration-form defaults and the cycle cases. Each case is written first, and the 814 cases fail at `e3cd0bf5`. The golden's five marked cases (`census-corpus.test.ts:903`, `:921`, `:928`, `:929`,
`:960`) lose the `[UNDECIDED BY v2 …]` mark:
- the four mixed cases keep their values, which are now law;
- the two-alias case flips: `s.js#a` goes from `not-exported` to `exported`.

**Replay controls owed** (in the carrier's evaluator unit, written first):
- the totality control `replay-table.py`. It evaluates the binding-class procedure on concrete evidence states, derives the class, and requires exactly one applicable row or "cannot occur" reason for each state. Its negative controls (a dropped row; RT-3 in its r3 wording) must fail;
- one evaluator control per row and per census column. These include a Rust closure with no member and an unreadable presented record (RT-7, not RT-3), a TypeScript closure with no member and lost evidence (RT-4), a historical v2 member (RT-5), a demonstrated historical binding (RT-6), and a host-derived inventory under every row (O3).

The Plan-time controls for A6's four checks are owed too, check 4 included (a valid v3 member with no successor in the host's
lock is refused).

**References that move from v2 to v3:** `census-corpus.test.ts:60`, `:741`, `:1051` and `:1054` (`CR-GATE`); the generated
`src/embedded/source-census.ts`; and the carrier's static file and table (A3).

**Not bound by this erratum:**
- the carrier's code units: the packager and static file, the host's Plan check, the evaluator's replay check, and defence in depth at fact admission (planner units CR1b-PKG, CR1b-HOST, CR1b-H5);
- the internal keys those units use;
- the FA-2 contract successor that states E1, E2 and this erratum in §9.8, and its `design-lock.json` entry;
- the one repackaging, lane restage and inventory change;
- any F3 value other than statement 4's (outside statement 4, no `exported` value is law);
- the evaluator owner's erratum (`E1` FCE1.6).

## FCE3.6 Open points for the reviewers

1. 4(b)'s single-symbol reading makes the intermediate result depend on order in duplicate-identifier programs (CY-05 against CY-05r). It is stated as law above.
2. RT-6 names no concrete historical reader, because none is known. A reader is owed only if a historical binding is ever demonstrated.
3. O4 takes the producer route for RT-4 and RT-5 whenever the Plan was made. It is a route, not a finding of fault.
4. Step 1 of the binding-class procedure puts a conflict before the A2 member (`E1:160`). This departs from the lead's order, as stated there.
