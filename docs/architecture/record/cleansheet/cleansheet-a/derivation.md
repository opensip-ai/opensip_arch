# Clean-sheet derivation

**Scope.** A command-line tool whose job is: *tell a team whether their codebase violates rules
they have declared, and prove the answer.*

**Isolation statement.** This derivation was produced without reading any source in this
repository, any existing architecture or steering document, any ADR, any agent log, any
`CLAUDE.md`/`AGENTS.md`, or `programming-language.md`. The only filesystem operations performed
before writing were an existence test on two directory paths, to determine where to write.
No content from the existing design entered this document. Where this derivation agrees with
the existing design, that agreement is independent; where it disagrees, neither is privileged
by this document.

**Contamination notice — read before treating any agreement as corroboration.** Immediately
*after* this file was written, the tool harness spontaneously emitted a skill-discovery notice
naming several components of the existing implementation: package names for a terminal-UI kit
and an HTML report generator, several subsystem names, a `report` command, and the fact that
packages are published to npm. This was not sought and was not read from any file; it arrived
unbidden in the result of the write operation that created this document.

Consequences, stated precisely so a reader can discount correctly:

- **Every decision D01–D73 was derived before that notice existed.** No decision was added,
  removed, reworded, or re-marked afterwards. The only post-notice edits were mechanical:
  fixing a duplicated decision id, supplying a block for a dangling reference (D72), correcting
  three wrong cross-references, and replacing an invented marking tally with a counted one.
- **The leaked information is materially relevant to exactly one decision**, D66 (implementation
  language), because it reveals the actual implementation's language and distribution shape.
  D66 was written before the leak and has deliberately **not** been revised in light of it. If
  D66 happens to agree or disagree with the existing design, that is a clean signal; if it had
  been revised, it would have been worthless.
- Nothing was learned about the domain model, execution model, storage, baseline mechanism,
  unknowns handling, extension model, or exit-status design — the areas carrying most of this
  document's weight.

A reader may reasonably treat D66 with extra suspicion on the grounds that the author knew
something at file-close time. The correct remedy is to re-derive D66 independently, not to
adjust it here.

**Method.** Every decision below states the decision, what forces it, what was rejected, and
what would falsify it. Each is marked:

- **FORCED** — a stated requirement or workload compels it; I could not find a way to satisfy
  the requirement otherwise.
- **PREFERRED** — judgment call. Alternatives remain live. Named as such deliberately.
- **GUESSED** — insufficient information. The decision is a placeholder that should be revisited
  once the missing information exists.

The output's value is in the forcing, not the conclusions. Several decisions I would normally
have reached for by habit are marked PREFERRED after failing to find a requirement that demands
them. That is the point.

---

## Part 0 — A compressed reading of the requirements

Before deriving anything, I compress the brief into the smallest set of independent constraints,
because most of the design falls out of the interactions between them, not the constraints
individually.

| Tag | Constraint | Source |
|---|---|---|
| **R1** | Works entirely offline on a laptop; no service dependency for any result | stated |
| **R2** | No language models, ever; determinism is the product | stated |
| **R3** | Many languages, genuinely deep in two | stated |
| **R4** | A result must be checkable later: why the claim, against what inputs, reproducibly | stated |
| **R5** | Adopt with existing violations; gate only on new; **must stay trustworthy across tool upgrades** | stated |
| **R6** | Third parties may contribute analysis logic; how much to support is open | stated |
| **R7** | A hosted product may consume results but must never be required | stated |
| **R8** | Few hundred → 100k+ files | stated |
| **W-agent** | Dominant workload: many small, rapid, **overlapping** queries after editing a few files | stated |
| **W-ci** | Full analysis, one shot, **no residency**, reproducible, must fail the build **correctly** | stated |
| **W-human** | Occasional; wants to understand **why** | stated |

Four interactions do most of the work, and I want them visible up front because nearly every
downstream decision traces to one of them:

1. **W-agent × W-ci.** One wants warm residency and sub-second answers; the other forbids
   residency and demands reproducibility. If these are served by two engines, they will
   disagree, and R4 dies. This forces the purity/caching split (D01).

2. **R4 × R3.** R4 says a *claim* must be checkable. The claim "there are no violations" is a
   claim. R3 guarantees analysis depth is non-uniform across languages. Therefore a result that
   reports only findings is unfalsifiable and misleading. This forces coverage and unknowns into
   the result type (D05, D06). I regard this as the single highest-value forcing in the brief,
   and the one most tools in this category get wrong.

3. **R5's second clause.** "Only gate on new" is easy. "Stays trustworthy across tool upgrades"
   is the hard requirement, and it is a *statement about a mechanism's failure modes*, not a
   feature. It forces drift detection, fail-loud ambiguity resolution, and explicit migration
   (D36–D43).

4. **R2 × W-ci.** "Determinism is the product's credibility" plus "must fail the build correctly"
   makes wall-clock timeouts, unordered iteration, and environment sensitivity into *correctness*
   bugs rather than polish items. This forces a prohibition list and a deterministic budget
   model (D25, D26, D60).

**A note on what R2 does and does not force.** R2 forbids calling language models. It does not,
by itself, forbid heuristics, approximation, or incompleteness — a static analyser is allowed to
be imprecise. What R2 forbids is *unrepeatable* imprecision. Throughout this derivation I treat
"deterministic" as the operative requirement and "sound/complete" as separate, weaker goals that
must be *declared* rather than achieved (D05, D06).

---

## Part 1 — Information I do not have

Stated explicitly rather than papered over with invented requirements. Ordered by how much the
answer would change the design.

1. **What kinds of rules do teams actually declare?** This is the largest gap. If the corpus is
   dominated by *transitive* constraints (layering, "nothing in domain may reach infrastructure",
   allowed-dependency graphs), the evaluation engine needs recursion and fixpoint, and that
   choice cascades into storage, incrementality, and evidence. If the corpus is dominated by
   *local syntactic* constraints (naming, forbidden constructs, file placement), a far simpler
   non-recursive matcher is correct and the recursive engine is over-engineering. I assume the
   former (see D13) and flag every decision that depends on the assumption.

2. **Which two languages are "deep"?** This changes the tier-2 cost estimate by an order of
   magnitude and changes whether reusing an existing frontend is viable. I parameterise as
   L1/L2 and require that the count two is not baked into anything (D50, D67).

3. **What does "prove" mean — engineering-grade or audit-grade?** Engineering-grade =
   reproducible plus inspectable evidence. Audit-grade = chain of custody, signing, tamper
   evidence, possibly non-repudiation. I design for engineering-grade with an optional hook for
   the rest (D33), because audit-grade implies key management, which implies infrastructure,
   which strains R1.

4. **Are rules authored by adopting teams, or consumed as packs?** Affects whether the authoring
   surface must be pleasant for occasional users or merely precise for pack maintainers (D17).

5. **Acceptable cold CI wall-clock at 100k files.** Without a number, performance targets are
   my invention (D64). I state targets as *falsifiers* rather than requirements.

6. **Monorepo / multi-project structure, and generated code.** I assume multiple projects within
   one workspace (D11) because it is cheap to support and expensive to retrofit; generated and
   vendored code handling is GUESSED (D28).

7. **Whether cross-repository rules are in scope.** Assumed out (D72). This is the assumption
   most likely to be wrong and most expensive if it is, because it changes the identity of a
   "workspace" and makes offline operation much harder.

---

## Part 2 — Architectures rejected wholesale

I state these first because the rest of the design must justify itself against them. Three of
the four are cheaper than what I propose.

### D69 — Reject "linter aggregator" as the core · **FORCED**

**The rejected design.** Shell out to the existing per-language ecosystem (one linter per
language), normalise the output, add baseline and reporting on top.

**Why it is attractive.** It buys multi-language depth immediately, at a small fraction of the
build cost, and inherits ecosystems that took years to build.

**Why R2/R4/R5 kill it.**
- Determinism is not controllable. Each subprocess has its own config discovery, plugin
  resolution, environment sensitivity, and version drift. R2's promise becomes a promise about
  software I do not control.
- Evidence is whatever the subprocess prints. R4 requires establishing *why* a claim was made;
  "the other tool said so" does not.
- "Rules they have declared" collapses into "rules those tools happen to implement." Cross-file
  and cross-language rules — the ones a team most wants to declare and that no single-language
  linter can express — are unreachable.
- Baseline stability (R5) would depend on N third-party fingerprint schemes, each of which
  changes on its own upgrade cadence. R5's "trustworthy across upgrades" becomes untestable.

**What survives.** Importing other tools' output as *non-gating, explicitly unverifiable*
findings is useful and costs little (D54). The rejection is of aggregation as the **core**, not
of interoperation.

**Falsified by.** If a real rule corpus turns out to be ≥90% expressible as configuration of
existing linters, this rejection is over-engineering and the cheap design wins.

### D71 — Reject "compiler plugin per language" as the core · **FORCED**

**The rejected design.** Implement analysis as a plugin inside each language's own compiler.

**Why R1/R2 kill it.** It imports the compiler's impurity wholesale: build scripts, procedural
macros, code generation, network-fetching package managers, environment-dependent feature
resolution. A result then depends on a toolchain version the tool does not control, which
defeats R4's reproducibility and R2's determinism. It also makes tier-0/tier-1 coverage of
"many languages" (R3) architecturally impossible, since the mechanism exists only where a
plugin API exists.

**What survives.** Compiler-derived facts as an *opt-in, explicitly impure enrichment* whose
outputs are captured in the run record (D51).

**Falsified by.** If accurate results in L1/L2 prove unattainable without the real compiler's
resolution, the impure path becomes the primary path and R2's guarantee must be honestly
downgraded to "deterministic given a pinned toolchain."

### D70 — Reject "SQL over a relational store" as the rule language · **PREFERRED**

**Why it is attractive.** Zero engine to build; third parties can query results with no tooling
at all, which serves R4 and R7 unusually well.

**Why rejected as the rule surface.** Recursive queries are expressible but awkward; provenance
(which rows justified this row) is not available without hand-rolling it, and R4 needs it;
query-planner variability makes latency unpredictable, which hurts W-agent; and SQL's semantics
invite nondeterminism (unordered result sets, NULL three-valued logic) precisely where R2 needs
none.

**What survives.** A relational export of results *is* adopted (D29) — for durability and
third-party inspection, not as the evaluation substrate.

**Falsified by.** If a prototype shows recursive CTEs plus a hand-rolled provenance table meet
both latency and evidence needs, the engine build is unjustified and this should be reversed.

### D43 — Reject line-diff / blame-based gating as *the* only-new mechanism · **PREFERRED**

**The rejected design.** No stored baseline at all. Report only findings whose lines were touched
by the change under review. Upgrade-proof by construction, because there is no state to rot.

**Why it is genuinely attractive.** It satisfies R5's letter at near-zero cost, and it is
immune to the entire class of failures that D36–D42 exist to manage. My heavier design must earn
its keep against this, and I want that comparison recorded rather than assumed away.

**Why rejected as the gating mechanism.**
- Under the assumption in D13 (non-local rules exist), a change in file A produces a violation
  *reported at file B*. Line-diff gating hides exactly the violations the change introduced.
  This is not a corner case; for layering rules it is the normal case.
- It cannot express "we have consciously accepted this specific known violation," which is what
  adoption-with-existing-violations actually needs over time.
- It couples the gating decision to VCS history shape (squash, rebase, history rewrite), making
  the verdict depend on something outside the analysed content. That is a determinism hazard
  under R2, and it leans on version control in a way the non-goal discourages.

**What survives.** "Findings attributable to changed lines" is a *view* over the finding delta
and is offered as such — it is a good triage ordering for W-human and a good default emphasis
for W-agent.

**Falsified by.** If the declared rule corpus is overwhelmingly local (D13 assumption wrong),
line-diff gating is the correct design and the baseline machinery is waste.

### D72 — Reject cross-repository analysis in the first version · **GUESSED**

**Decision.** A workspace is a single analysis root. Rules cannot span repositories.

**Forcing.** **GUESSED** — the brief neither asks for nor excludes it, and I have no information
about whether teams declare rules that cross repository boundaries.

**Why it matters that this is a guess.** Cross-repository rules would change the identity of a
workspace, make the input snapshot (D02) span multiple version-control roots, and make offline
operation (R1) substantially harder — you would need the other repositories present locally.
It is the assumption in this derivation most expensive to be wrong about.

**Rejected.** Designing for it speculatively. Rejected: it would inflate the domain model with
no evidence of need, which is the failure mode this exercise is meant to avoid.

**Falsified by.** Any stated rule that references a symbol or module in another repository.

---

## Part 3 — Foundations

These six decisions constrain everything after them.

### D01 — Analysis is a pure function of declared inputs; residency is *only* a cache · **FORCED**

**Decision.** Every computation is a pure function of (code identity of the computation,
digests of its declared inputs, configuration digest). A persistent local cache memoises nodes
of this graph. Deleting the entire cache changes nothing except latency. A `--no-cache` mode
recomputes and asserts output-digest equality with the cached path.

**Forced by.** W-agent (needs warm residency and sub-second overlapping queries) × W-ci (forbids
residency, demands reproducibility) × R4. I could find no way to serve both without either two
engines that disagree, or one pure engine with an inert cache. Two engines is disqualified
because the interactive answer would then be unverifiable, which is exactly the credibility R2
is protecting.

**Rejected.**
- Separate "fast path" heuristics for interactive use. Rejected: creates a second truth. If the
  fast answer can differ from the authoritative one, agents are being lied to at the highest
  query volume in the system.
- Cache as an optimisation with best-effort correctness ("usually right, re-run if suspicious").
  Rejected: shifts the burden of knowing when to be suspicious onto the caller, and the dominant
  caller is an automated agent with no basis for that judgment.

**Falsified by.** A measured `--no-cache` parity test that cannot be made to pass without
sacrificing interactive latency — i.e. if purity provably cannot hit the latency target, one of
purity or latency must be renegotiated explicitly rather than silently.

**Payoff to note.** Purity makes cancellation free (D23): work from a cancelled query is still
valid and still cache-worthy. This matters because W-agent's queries are described as
*overlapping*, so cancellation is the common case, not the exception.

### D02 — Every result pins an input snapshot; mid-run mutation is an error, not a race · **FORCED**

**Decision.** A query begins by pinning a snapshot: an ordered map of (path → content digest)
over the selected file set. The answer is *about that snapshot* and says so. If a file is read
whose content no longer matches its pinned digest, the run fails with `inputs-mutated` rather
than producing a result describing a state that never existed.

**Forced by.** R4 ("against what inputs"). A resident process (implied by W-agent) is reading a
working tree that a human or agent is editing concurrently; without pinning, results describe
a superposition of states. That is unreproducible by construction.

**Rejected.**
- Ignore it; the window is small. Rejected: for W-agent the window is not small — the agent is
  editing continuously and querying continuously. This is the expected condition.
- Copy/stage inputs to a private location per query. Rejected at 100k files: the copy cost
  dominates the analysis. Digest-verification achieves the same guarantee at read cost.

**Falsified by.** If `inputs-mutated` fires often enough in real agent sessions to be an
obstruction rather than a safeguard, the answer is finer-grained snapshots (per project or per
dependency cone), not abandoning pinning.

### D03 — Two layers: extractors produce facts; rules are queries over facts · **FORCED**

**Decision.** Analysis is split at a hard boundary. *Extractors* turn source bytes into typed
facts. *Rules* are queries over facts and produce findings. Rules never see source bytes and
never touch the filesystem.

**Forced by.** Three requirements converge, and I want the convergence explicit because each
alone would be weaker:
- **W-agent incrementality.** Facts are per-file and cacheable by content digest, so a five-file
  edit re-extracts five files. A monolithic pass that walks trees and emits diagnostics cannot be
  cached at that granularity.
- **R4 evidence.** "Why was this flagged" has a real answer only if the thing that fired is a
  query whose satisfying tuples can be named and traced to spans. If the rule is opaque code,
  the best available answer is "the code decided," which does not meet R4.
- **R6 authority limits.** A query has no authority by construction. Arbitrary rule code has all
  of it. This boundary is what makes third-party rules loadable at all (D49).

**Rejected.**
- Imperative rules over a *recording* fact accessor (build-system style dependency tracking,
  Salsa/Adapton-shaped). This is a serious alternative: it delivers incrementality and a read
  log. Rejected because a read log tells you what the rule *looked at*, not what *made it fire* —
  which is a materially weaker answer to R4 — and because it grants the rule general
  computational authority, which reopens D49.
- Rules as tree-pattern matchers directly over syntax trees, skipping a fact layer. Rejected:
  cross-file and cross-language rules have no home, and evidence cannot cite anything but
  syntax.

**Falsified by.** If a substantial and important class of declared rules turns out to be
inexpressible as queries over any reasonable fact schema, the boundary is in the wrong place,
and the correct response is the sandboxed imperative escape hatch (D55), not abandoning the
split.

### D04 — Facts are tiered by analysis depth: 0 universal, 1 syntactic, 2 resolved · **FORCED**

**Decision.**

| Tier | Content | Coverage |
|---|---|---|
| **0** | File identity, path, size, encoding, line index, byte spans, VCS metadata, text-level facts | Every file, including unsupported languages and binaries |
| **1** | Tokens, syntax nodes, declarations, identifier occurrences, imports/includes as written, comments, annotations | Every language with a grammar |
| **2** | Resolved names, module graph with resolved edges, call graph, inheritance/implements, symbol identity across files | L1 and L2 only |

Each fact predicate declares its tier. Each rule declares the predicates it requires, and
therefore its minimum tier.

**Forced by.** R3 (many languages, deep in two) × R4. Without tiers, a rule requiring resolution
runs against a language with no resolver, finds nothing, and reports clean. That is a silent
false negative presented as a pass — the exact failure R4 exists to prevent. Tiers make
"this rule could not be evaluated here" *computable* rather than a matter of documentation.

**Rejected.**
- One uniform schema with nullable/absent columns for unsupported languages. Rejected: absence
  and "not applicable" become indistinguishable at query time, so the rule silently succeeds.
- Per-language schemas with no common core. Rejected: no cross-language rules, and tier-0
  facts (which are genuinely universal and genuinely useful) get reimplemented per language.

**Falsified by.** If tier-1 facts prove too shallow to express useful rules in non-deep languages,
the tiering is real but the *middle* tier is not carrying weight, and the honest response is to
narrow the language claim rather than pretend tier-1 rules are meaningful.

### D05 — A result is a triple: findings, coverage, unknowns. Absence is always qualified · **FORCED**

**Decision.** The result type is not `Finding[]`. It is
`(Finding[], Coverage, Unknown[], Verdict)`. Coverage records, per (file × tier) and per
(rule × scope), whether evaluation was complete, partial, or not performed, with a reason.
Human output leads with coverage and unknowns, not with counts. "Zero violations at 61% tier-2
coverage" is the honest rendering, and the tool renders it that way by default.

**Forced by.** R4 applied to negative claims, plus W-ci's "fail the build **correctly**." A build
that passes because analysis silently did not run has failed incorrectly. This is the decision I
am most confident is forced and most confident is commonly omitted.

**Rejected.**
- Coverage as a separate optional report. Rejected: optional means absent in CI, which is where
  it matters most, and it lets the verdict be computed without it.
- Warnings on stderr for skipped files. Rejected: stderr is not part of the result, is not
  stored, is not diffable, and cannot be gated on.

**Falsified by.** If coverage metrics prove so noisy that teams universally disable the gate,
the *metric* is wrong (wrong granularity, or measuring the wrong thing), but the presence of
coverage in the result type is not thereby falsified.

### D06 — An unknown is *material* iff it intersects the dependency cone of an enabled rule · **FORCED**

**Decision.** Because rules declare their fact dependencies (D03/D04), the tool computes whether
each unknown could have affected the verdict: an unresolved import is material if any enabled
rule depends on resolved-import facts; a parse failure in a language no enabled rule targets is
immaterial. CI can gate on `--fail-on-unknown=material`, which is the recommended default for
adoption.

**Forced by.** R4 × W-ci. Without materiality, unknowns are either ignorable noise (so R4's
qualification is decorative) or an unusable gate (any 100k-file repo has thousands of
immaterial unknowns). Materiality is what makes the qualification actionable rather than
performative. It is computable rather than heuristic *only because* of D03 — this is the
strongest argument for the two-layer split.

**Rejected.**
- Severity levels on unknowns assigned by the extractor author. Rejected: the extractor cannot
  know which rules the team enabled, so it cannot know what matters here.
- Gate on total unknown count with a threshold. Rejected: a threshold on a number nobody can
  interpret is a number teams will raise until it stops firing.

**Falsified by.** Rules whose dependency declarations are systematically wider than their actual
dependencies would make almost everything material. That is a rule-authoring quality problem
with a mechanical check available (compare declared dependencies against dependencies observed
during evaluation, and refuse over-broad declarations).

---

## Part 4 — Domain model

### D07 — Occurrence identity, persistent identity, and class identity are three different things · **FORCED**

**Decision.** Three distinct identities, never conflated:
- **Occurrence** — this violation at this span in this snapshot. Deliberately unstable.
- **Persistent** — "the same violation" across revisions. What baselines key on. Location-independent.
- **Class** — the rule. What policy and aggregation key on.

**Forced by.** R5. A single `file:line:rule` key — the classic linter model — makes baselines rot
on line drift: a formatting commit produces a flood of "new" violations, teams stop trusting the
gate, and R5's "trustworthy" fails within weeks of adoption.

**Rejected.**
- One `Diagnostic` type with location as identity. Rejected as above.
- Location as identity plus fuzzy matching at compare time. Rejected: fuzzy matching means the
  gate's behaviour depends on a similarity threshold nobody can audit, and R4 requires the
  matching decision itself be explainable.

**Falsified by.** Measured baseline churn. If content-derived identity churns *more* than
location-derived identity on real repositories (plausible: a repo-wide formatter change alters
normalised content everywhere while leaving line numbers largely intact), the scheme is wrong
even though the three-way split is right.

### D08 — Persistent identity = (ruleId, ruleVersion, scopeKey, unitDigest, ordinal) + schemeVersion · **PREFERRED**

**Decision.**
- `scopeKey` — the *semantic container*: for tier-2 languages, module path plus symbol path
  (`app/orders::OrderService::submit`); for tier-0/1 languages, the repo-relative file path,
  which is the best available.
- `unitDigest` — normalised digest of the smallest syntactic unit implicated (whitespace,
  comments, and formatting normalised away).
- `ordinal` — position among identical `unitDigest`s within the same scope, under a canonical
  ordering.
- `schemeVersion` — the version of this identity scheme, stored alongside every use.

**Forcing.** The *need* for a location-independent persistent key is FORCED (D07). This
particular tuple is PREFERRED — it is one of several defensible constructions.

**Why each component.** Symbol-path scoping survives file renames and code movement within a
file, which are the two most common benign changes. Normalised digests survive reformatting.
The ordinal exists because content-only fingerprints collapse *n* identical violations in one
scope into one identity — so removing one of three looks like no change, and adding a fourth
looks like nothing new. That is a real, silent gating failure in tools that use bare
content fingerprints, and the ordinal is the cheapest fix.

**Rejected.**
- Content fingerprint alone. Rejected: the collapse problem above.
- Fingerprint over a window of surrounding lines. Rejected: sensitive to unrelated nearby edits,
  which reintroduces drift.
- Identity assigned by a database or service. Rejected: violates R1, and makes identity depend
  on the order in which the tool historically ran rather than on the inputs — unreproducible.

**Honest limitation, stated rather than hidden.** No identity scheme survives all refactors. A
function extracted into two, or renamed, will re-key. The architecture therefore does not
pretend: `schemeVersion` is recorded, and re-keying is an explicit, auditable migration (D41),
not a silent event. Designing as if a perfect scheme existed is the actual failure mode here.

**Falsified by.** Measured re-key rate on real refactor-heavy histories. If ordinary refactoring
re-keys a large fraction of baselined findings, the scheme is not carrying its weight and
line-diff gating (D43) becomes comparatively more attractive.

### D09 — Severity is not part of identity; rule parameters are · **FORCED**

**Decision.** Policy-assigned severity, enablement, and gating status are excluded from
persistent identity. Rule *parameters* (`maxDepth = 5`, an allowed-list) are included in the
rule's effective identity for baseline purposes, but recorded as named parameters rather than
folded opaquely into the rule id.

**Forced by.** R5. Including severity means promoting a rule from warn to error re-keys every
baselined finding for that rule — a pure policy edit silently invalidates suppression state.
Excluding parameters means changing `maxDepth` from 5 to 3 lets old baseline entries suppress
findings the old configuration could never have produced: a **silent widening of suppression**,
which is R5's worst failure mode (invisible loss of gating).

**Rejected.** Treating the whole resolved policy as part of identity. Rejected: too coarse — any
policy edit invalidates everything, so teams avoid editing policy.

**Falsified by.** A parameter that provably cannot affect the finding set (a message template,
say) would be miscategorised by this rule; the fix is declaring per-parameter
finding-affecting-ness, not abandoning the split.

### D10 — Evidence is a minimal, deterministically-selected proof; negation evidence is an exhausted-domain summary · **PREFERRED** (deterministic selection: **FORCED**)

**Decision.** Each finding carries the derivation that produced it: the derived tuple, the rule
instance that fired, and the body tuples, recursively, down to base facts that each carry a
source span. Exactly one proof is stored — the canonically-least proof under a total order —
because the number of proofs can be exponential. For negated conditions ("no `@authorized`
annotation on any handler"), the justification is an absence, so evidence records the *domain
that was searched and found empty*, summarised: "34 declarations matched `handler`; 0 carried
`@authorized`."

**Forcing.** That evidence must exist is FORCED by R4 and W-human. Proof-trees as the form are
PREFERRED (they fall out naturally if D13 is adopted; a different evaluator would need a
different evidence construction). That proof *selection* is deterministic is FORCED — otherwise
two reproductions agree on findings but disagree on explanations, and R4's "establish why"
degrades to "establish that."

**Rejected.**
- Store all proofs. Rejected: exponential.
- Store no proof; re-derive on demand when a human asks. Rejected: re-derivation requires the
  original inputs and the original tool version, so the *archived* record fails R4 as soon as
  either is gone. A stored proof is checkable years later; a promise to re-derive is not.
- Natural-language explanation generated at report time. Rejected: template rendering over the
  proof is fine; anything that would need a model is excluded by R2.

**Falsified by.** If minimal proofs are routinely uninformative to human reviewers — the least
proof being a degenerate path that does not illustrate the real problem — then "minimal" is the
wrong selection criterion and something like "shortest proof through the most specific rule"
should replace it. This is worth testing early with real reviewers; it is a usability claim
masquerading as an architectural one.

### D11 — Project / compilation unit is an explicit first-class boundary · **PREFERRED**

**Decision.** A workspace contains one or more projects. A project is a resolution boundary:
tier-2 extraction is scoped to it and cached at its granularity, and cross-project references
go through a persisted symbol index.

**Forcing.** PREFERRED. Nothing stated requires multi-project support. I adopt it because R8's
upper end (100k+ files) is characteristic of monorepos, because tier-2 resolution has no meaning
without a unit boundary, and because retrofitting a unit boundary into an established fact
schema is very expensive. Cost of being wrong is asymmetric.

**Rejected.** Workspace = single implicit project. Rejected on the asymmetry argument above.

**Falsified by.** If real usage is overwhelmingly single-project, this is harmless extra
structure — falsified in the sense of being unjustified, not in the sense of being wrong.

### Full entity list

For comparability, the complete model:

```
Workspace     analysis root; file selection; language mapping; project declarations
Project       resolution/compilation boundary
SourceFile    (repo-relative path, contentDigest, language, encoding); identity is contentDigest
Language      id, dialect/version, extractor bindings
Extractor     id, version, tier, predicates produced, purity, required capabilities
FactPredicate name, arity, column types, tier, stability class
Fact          a tuple + provenance (source span, or derivation for derived facts)
Span          (contentDigest, byte range) with line/col derived, never stored as truth
Rule          id, semver, params schema, required predicates, body, rationale, remediation,
              conformance corpus, behaviourDigest
Ruleset       resolved rules + versions + digests (composition of packs, lockfiled)
Policy        enablement, severity, gating, parameter bindings, scope filters, baseline ref,
              unknown-gating thresholds
Configuration Workspace + Ruleset + Policy, canonicalised → ConfigDigest
Finding       rule + bound params + primary span + message + Evidence + Severity + FindingIdentity
FindingIdentity  D08 tuple + schemeVersion
Evidence      minimal proof tree; exhausted-domain summaries for negations
Coverage      per (file × tier) and per (rule × scope): complete | partial | not-performed + reason
Unknown       kind, scope, cause, materiality
Suppression   inline or policy-level; rule-scoped; reasoned; usage-tracked
Baseline      attested FindingIdentity set + ConfigDigest + ruleset versions + schemeVersion
              + adoption revision + adoption metadata
FindingDelta  appeared | disappeared | persisted | re-keyed | ambiguous
RunRecord     inputs, config, versions, environment attestation, findings, evidence, coverage,
              unknowns, verdict, recordDigest (semantic fields only)
Verdict       gating decision + reason + exit class
```

Two details in that list are load-bearing and easy to miss:

- **`Span` is (contentDigest, byte range)**, with line/column *derived*. Line numbers are a
  presentation concern and a determinism hazard (line ending conventions, BOM, Unicode
  normalisation). Storing byte offsets against a content digest makes a span verifiable forever.
- **`recordDigest` covers semantic fields only.** Timings, hostname, wall-clock, and core count
  live in a non-semantic envelope outside the digest. Otherwise two identical runs produce
  different digests and record comparison — the whole point — becomes impossible. **FORCED** by
  R4.

---

## Part 5 — The rule surface

### D12 — Rules are declarative queries; imperative rule code is not the primary surface · **FORCED** (that a zero-authority surface exists) / **PREFERRED** (declarative form)

Derived in D03. Recorded separately here because it is the decision third-party contributors
will feel most (R6).

### D13 — The evaluator supports recursion with fixpoint and stratified negation (Datalog-shaped) · **PREFERRED**

**Decision.** Rule bodies are conjunctive queries with recursion, stratified negation,
aggregation, and no general computation. Evaluation is set-at-a-time (semi-naive) to a fixpoint.

**Forcing.** **PREFERRED**, resting on the assumption in Part 1 item 1 — that declared rules
include transitive/reachability constraints. If that assumption holds, recursion is forced
(a layering rule *is* transitive closure and cannot be expressed without it). Since I cannot
verify the assumption, I mark the decision PREFERRED and the assumption explicit. This is
exactly the kind of place where I would normally have written FORCED by habit.

**Why this shape, given recursion is needed.** Datalog gives termination guarantees for free
(no unbounded computation, so a hostile or careless third-party rule cannot hang the tool —
which serves D49), gives set-at-a-time evaluation that suits the fact-base model, and gives
provenance essentially for free (D10). The alternatives each lose one of those.

**Rejected.**
- Expression languages (CEL-shaped). Rejected: no recursion, so reachability rules are
  inexpressible.
- Full logic programming with negation-as-failure and unrestricted terms. Rejected: loses
  termination guarantees and stratified semantics, which are the two properties making untrusted
  rules safe.
- Graph query languages. Live alternative, honestly — good ergonomics for reachability, and
  path-returning semantics map neatly onto evidence. Rejected mainly on provenance for negation
  and on the cost of a second data model alongside relations.

**Build vs embed.** Semi-naive evaluation with stratification is a few thousand lines and gives
control over determinism, budgets (D25), and provenance (D10) — all three of which are
requirements here and none of which off-the-shelf engines expose well. Embedding is cheaper
initially; I would prototype against an embedded engine to validate expressiveness, then own the
evaluator once determinism and provenance requirements bite. **PREFERRED**, and I note this is
the single largest build-cost item in the design.

**Falsified by.** A rule corpus that is ≥90% non-recursive. Then a non-recursive matcher is
correct, much faster, and much cheaper — and D70's SQL rejection weakens too.

### D14 — Every rule ships a semantic version, a behaviour digest, and an executable conformance corpus; a rule failing its corpus is refused, not degraded · **FORCED** (drift detection) / **PREFERRED** (this triad)

**Decision.** Three mechanisms, layered:
1. **Semantic version** — author's declaration that the finding set may have changed.
2. **Behaviour digest** — computed from the rule body, its parameter schema, and its declared
   predicate dependencies. Detects change the author forgot to declare.
3. **Conformance corpus** — positive and negative examples shipped with the rule, re-run at load
   time. Detects change in *meaning* without needing any historical revision.

A rule whose corpus fails is **refused** — not warned about, not run in degraded mode. A rule
whose behaviour digest moved without a version bump is refused as authoritative for baseline
matching (D39).

**Forcing.** R5's "trustworthy across tool upgrades" **forces** that *some* mechanism detect
semantic drift; digests alone are insufficient (they detect change but not whether it matters),
and version numbers alone are insufficient (they rest on discipline, which decays). So at least
one of {replay against history, conformance corpus} is forced. The specific triad is PREFERRED.

**Rejected.**
- Trust semver. Rejected: an obligation enforced only by convention is not a mechanism, and R5
  asks for trustworthiness, not intention.
- Detect drift only by replaying at the baseline revision (D39). Rejected as the sole mechanism:
  requires the revision to be available, which shallow CI clones break — so it fails exactly
  where CI needs it.

**Falsified by.** If corpus maintenance burden causes rule authors to write trivially-passing
corpora, the mechanism is theatre. Countermeasure worth building: mutation-style coverage — a
rule whose body can be perturbed without any corpus example changing verdict has an inadequate
corpus, and that is mechanically checkable.

### D15 — Policy and rule definitions are separate artifacts; both live in-repo and are digest-pinned · **FORCED**

**Decision.** `Policy` (which rules, what severity, what gating, what parameters, what scope) is
separate from rule *definitions*. Both are version-controlled files in the repository. Both
contribute to `ConfigDigest`.

**Forced by.** R4 (reproducing a result requires the rules that produced it, so they must be
pinned and retrievable) plus R5 (a policy edit must be reviewable as a diff, since it changes
what is gated). Separation is forced by usage asymmetry: policy churns, rule logic does not, and
most teams import rule packs rather than authoring them.

**Rejected.** Configuration in a hosted service or user-level config outside the repo. Rejected:
violates R1 and makes results depend on invisible per-machine state, which is a determinism
failure that would be very hard to diagnose.

**Falsified by.** Nothing I can identify; this feels genuinely forced.

### D16 — Rule packs resolve to content digests, are lockfiled, and can be vendored · **FORCED**

**Decision.** Third-party rule packs are named, resolved to content digests, recorded in a
lockfile, and cached locally. Offline reproduction requires either the local pack cache or
vendored packs; the tool can vendor on request.

**Forced by.** R1 × R4 × R6. If reproduction requires re-fetching a pack, reproduction requires
network, which contradicts R1. If a pack is referenced by mutable name only, the same
configuration means different things at different times, which contradicts R4.

**Rejected.** Version-range dependencies resolved at run time. Rejected: makes the analysis
result depend on when it ran.

**Falsified by.** Nothing identified.

### D17 — Policy in TOML; rules in a dedicated DSL · **PREFERRED**

**Decision.** Policy is a strict, order-independent, comment-supporting configuration format —
TOML. Rule bodies use a purpose-built declarative syntax.

**Forcing.** **PREFERRED**, and genuinely near-arbitrary. The one substantive argument: YAML's
implicit typing (the Norway problem, sexagesimal-looking strings, version numbers parsing as
floats) is a determinism hazard in a tool whose product is determinism. That argument is real
but small. JSON lacks comments, which matters for policy files that record *why* a rule is off.

**Rejected.** YAML (above); JSON (comments); embedding rules in a general-purpose language
(reopens D03/D49).

**Falsified by.** Team preference; this is a decision to hold loosely and change cheaply. If it
ever becomes expensive to change, that is itself a design smell.

### D18 — Inline suppressions are supported, but a suppressed finding is recorded, never hidden · **PREFERRED**

**Decision.** Support `// allow rule-id: reason` at the point of violation, with hard
constraints: must name a specific rule (never blanket), must carry a reason, usage is tracked so
unused suppressions are reported as rot, and — critically — a suppressed finding still appears
in the result and the run record with status `suppressed`. Suppression removes *gating*, never
*visibility*.

**Forcing.** That suppressions exist at all is **PREFERRED** — nothing in the brief requires
them, and I am adopting a familiar pattern because bulk baselines and point exceptions solve
genuinely different problems (temporal debt versus a permanent justified exception). Given they
exist, "recorded not hidden" is **FORCED** by R4: a mechanism that deletes claims from the
record makes the record unable to answer why something was *not* reported.

**Rejected.**
- Blanket file-level or line-level suppression with no rule named. Rejected: it silently absorbs
  future rules, which is the same silent-widening failure as D09.
- Suppressions that remove the finding entirely. Rejected: destroys the audit trail and hides
  suppression pressure, which is exactly the signal a reviewer (W-human) and a consuming
  dashboard (R7) most want.

**Falsified by.** If suppression comments prove to be the dominant adoption mechanism and
baselines go unused, the baseline machinery is over-built — worth measuring after adoption.

---

## Part 6 — Execution and scheduling

### D19 — Cache keys are (computation identity, input digests, config digest) · **FORCED**

Direct consequence of D01. Recorded separately because the *composition* of the key is where
purity is usually broken: forgetting to include the extractor version, the rule body digest, or
a parameter binding produces a cache that silently serves stale answers — a determinism failure
that is invisible until someone reproduces a run and gets a different result.

**Falsified by.** The `--no-cache` parity test in CI. This test is not optional; it is the only
thing standing between D01 and wishful thinking.

### D20 — Six pure phases, each independently cached · **PREFERRED**

```
0  Resolve configuration            → ConfigDigest      (fails closed on unknown fields)
1  Enumerate + select files         → FileSet + digests  (deterministic order)
2  Extract tier-0/1 facts per file  (parallel; key: extractorDigest × contentDigest)
3  Build project graph; tier-2 per project
                                     (key: extractorDigest × unitDigest × depSymbolIndexDigest)
4  Evaluate rules to fixpoint       → derived facts + findings + proofs
5  Identity, baseline diff, suppressions, coverage, unknowns, materiality
6  Verdict + emit (record + report)
```

**Forcing.** PREFERRED. The phase *boundaries* are chosen for cache granularity, not for
conceptual tidiness — phase 2 is per-file because that is the unit W-agent invalidates; phase 3
is per-project because resolution has no smaller sound unit; phase 4 is whole-fact-base because
recursive rules are global.

**Rejected.** A single fused pass. Rejected: nothing is cacheable, so W-agent is unservable at
100k files.

**Falsified by.** If phase 3's key (which includes a digest over dependency symbol indexes)
causes cascading invalidation — one edit in a widely-depended-upon project invalidating
everything downstream — the boundary needs finer granularity (per-symbol rather than
per-project index digests). This is the most likely place for the phase structure to fail.

### D21 — Incrementalise extraction first. Re-evaluate rules from scratch over the warm fact base until measurement forces otherwise · **PREFERRED**

**Decision.** Phases 2 and 3 are incremental from day one (per-file, per-project, content-keyed).
Phase 4 initially re-runs completely over the in-memory fact base on every query. Incremental
view maintenance (semi-naive for additions, delete-and-rederive for retractions) is added only
if measurement shows phase 4 misses latency targets.

**Forcing.** PREFERRED — and deliberately so. The habitual move is to build incremental view
maintenance up front because the workload is described as incremental. But the expensive part of
this pipeline is parsing and resolution, not relational evaluation; a warm fact base evaluated
by a set-at-a-time engine may well answer in milliseconds at these scales. DRed is also the
single hardest correctness surface in the whole design, and getting it subtly wrong produces
*wrong answers*, which is worse than slow ones in a tool whose product is credibility.

**Rejected.**
- Full incremental view maintenance from the start. Rejected on risk-versus-evidence: high
  correctness risk, unmeasured benefit.
- Demand-driven top-down evaluation (magic sets) as the interactive path. Rejected as the
  *initial* choice, not on principle: it is better cold and worse warm, and W-agent is a warm
  workload. It remains the right answer if the resident fact base cannot fit in memory.

**Falsified by — with a number.** If warm phase-4 evaluation of a realistic ruleset at 100k
files exceeds ~300 ms p50 or ~1 s p95, incremental view maintenance becomes **FORCED** and this
decision inverts. That threshold is my invention (Part 1 item 5) and should be replaced with a
real one.

### D22 — The agent-facing answer is a *finding delta*, not a list of findings in changed files · **FORCED**

**Decision.** A query is `(changedSet, ruleSelection?, scope?)`. The answer is the delta of the
finding set — appeared / disappeared / persisted / re-keyed / ambiguous — computed against a
reference state, plus the coverage and unknowns for the snapshot.

**Forced by.** W-agent ("did I break anything?") under the D13 assumption. An edit to file A can
create a violation reported in file B; returning "findings in A" answers a different question
than the one asked, and answers it wrongly. The literal question is about *change in the finding
set*, so the answer must be a set difference.

**Rejected.** Return findings whose span lies in the changed set. Rejected as above — this is
D43's failure mode relocated into the interactive path, where it would do the most damage
because it is the highest-volume query.

**Consequence worth naming.** Baseline gating and "did I break anything" are then the *same
mechanism* with different reference states: baseline gating diffs against a recorded attested
state, and the interactive query diffs against the session's last-known state. Unifying them
(D42) is forced by having both requirements, and it means the highest-volume code path and the
CI-critical code path exercise the same logic — which is exactly the sharing you want for
credibility.

### D23 — Queries are cancellable and latest-wins-coalesced per workspace; cancelled work keeps its cache · **FORCED** (cancellation) / **PREFERRED** (coalescing policy)

**Decision.** In-flight queries are cancellable at safe points. A newer query for the same
workspace supersedes an older one with the same selection. Cache entries produced by cancelled
work are retained.

**Forced by.** W-agent explicitly says queries are *overlapping*. Without cancellation, an agent
editing quickly queues work whose answers are already worthless, and latency degrades under
exactly the load pattern that matters most.

**Rejected.** Queue and answer all queries. Rejected: unbounded queue growth under the dominant
workload.

**Payoff.** Retaining cancelled work's cache entries is sound only because of D01's purity — a
partial result is still a *correct* partial result. This is a concrete dividend of purity beyond
reproducibility.

**Falsified by.** If coalescing drops answers an agent actually needed (it asked about a
different scope), the coalescing key is too coarse; refine it rather than remove it.

### D24 — Two trust tiers: `provisional` (validity-hint-based) and `attested` (content-hash-based) · **PREFERRED**

**Decision.** Interactive queries may validate cache entries using cheap unsound hints
(mtime + size + inode) and are labelled `provisional`, carrying an explicit unknown: "N files
validated by hint, not content." Any run that produces a durable record or a CI verdict
re-validates by content hashing and is labelled `attested`. The label is part of the result,
not a flag.

**Forcing.** **PREFERRED**, resting on an unverified assumption: that content-hashing 100k files
per query is too slow for W-agent's latency budget while stat-ing them is not. If that
assumption is wrong, the tier distinction is unnecessary complexity and should be deleted.

**Why the label is mandatory.** mtime-based validation is unsound (clock skew, same-second
edits, restored files). An unsound-but-fast path is defensible; an unsound path that *presents
itself as authoritative* is not, because the dominant consumer is an automated agent with no way
to know the difference. Naming the tradeoff in the result is what makes it acceptable under R2.

**Rejected.**
- Content-hash always. Rejected on the latency assumption above — but this is the fallback if
  the assumption fails, and it is strictly simpler.
- Hint-based always. Rejected: makes CI verdicts and durable records unsound, which is
  disqualifying.

**Falsified by.** Measurement. If full content hashing of a 100k-file tree fits inside the
interactive budget (plausible with parallel I/O and a fast hash), delete this decision.

### D25 — Budgets are deterministic (steps, derived tuples, depth), never wall-clock. Wall-clock abort makes a run non-conforming · **FORCED**

**Decision.** All limits that can affect results are counted in deterministic units. A
wall-clock limit may exist as a safety valve, but tripping it produces status `aborted` and a
run that is explicitly *not* a verdict — it never yields a partial pass.

**Forced by.** R2 and W-ci. A wall-clock timeout makes the result depend on machine speed and
load, so the same inputs produce different verdicts on different machines. That is not
"determinism as the product." A run truncated by time that still reports a verdict is the
worst case: a green build caused by a busy CI agent.

**Rejected.**
- Per-rule wall-clock timeouts with a warning. Rejected: this is the industry-standard behaviour
  and it is exactly the silent-false-negative pattern R4 forbids.
- No limits at all. Rejected: a pathological rule or input can hang the tool, and D49 needs
  budgets to make untrusted rules safe.

**Falsified by.** Nothing I can see. This one feels genuinely forced, and it is the decision
most likely to be quietly violated during implementation under schedule pressure.

### D26 — Parallelism must not affect output; enforced by a parity test on every build · **FORCED**

**Decision.** Relations are sets, canonically sorted before hashing or emission. Any truncation
("first N", "stop after M") applies after canonical ordering, never in arrival order. Diagnostic
and error aggregation is sorted. CI runs the suite at parallelism 1 and parallelism N and asserts
identical output digests.

**Forced by.** R2 × R8. Parallel extraction is mandatory at 100k files; nondeterministic output
under parallelism silently destroys R2. The parity test is what converts the invariant from an
intention into a property.

**Rejected.** Rely on code review to catch order dependence. Rejected: order dependence is
invisible in review and intermittent in testing — precisely the class of bug that needs a
mechanical check.

**Falsified by.** Nothing; the test either passes or the invariant is broken.

---

## Part 7 — Storage and checkability

### D27 — The durable artifact is a self-contained, versioned run record whose digest covers semantic fields only · **FORCED**

**Decision.** A run emits a run record containing: input set as (path → digest); resolved
configuration including rule ids, versions, behaviour digests, parameter bindings; tool and
extractor versions; fact schema and identity scheme versions; environment attestation; findings
with identities and evidence; coverage; unknowns; verdict. Plus a `recordDigest` over the
semantic fields, with timings and machine metadata in a non-semantic envelope outside it.

**Forced by.** R4's three clauses map one-to-one: *why* → evidence; *against what inputs* →
input digests; *reproduce* → versions and configuration. Excluding non-semantic fields from the
digest is forced by wanting to compare two runs at all.

**Rejected.**
- Store the report and re-derive details on demand. Rejected: the record must remain checkable
  after the tool has moved on and the inputs are gone.
- Store the analysis database. Rejected: the record must be readable by parties that do not have
  our code (R7), and an internal database is neither versioned as a contract nor stable.

**Falsified by.** If records prove too large at 100k files to retain per CI run, evidence detail
becomes tiered (full for gating findings, references-only for baselined ones) — which changes
the record's shape but not this decision.

### D28 — Record input *digests*, not input contents; optionally archive inputs not covered by version control · **PREFERRED**

**Decision.** By default the record identifies inputs by digest and relies on version control to
hold the bytes. Inputs not in version control — generated code, vendored trees, untracked files
— can be archived into the record on request.

**Forcing.** PREFERRED, and the weakest link in R4's reproduction chain: a record whose inputs
have been garbage-collected from history is no longer reproducible. The counterweight is size,
and the non-goal "not replacing version control."

**Rejected.**
- Always archive contents. Rejected on size, and it duplicates version control's job.
- Never archive. Rejected: generated inputs are common and would make records covering them
  unreproducible with no available remedy.

**Falsified by.** If most analysed inputs turn out not to be tracked (heavy code generation),
the default should invert.

### D29 — In-memory columnar relations for evaluation; content-addressed blobs plus a relational index for durability · **PREFERRED**

**Decision.** Evaluation operates on interned, columnar, in-memory relations. Durability is a
content-addressed blob store for facts and proofs, plus an embedded relational database (SQLite)
as the index and the third-party query surface.

**Forcing.** PREFERRED. The split is motivated by two genuinely different access patterns
(millisecond fixpoint evaluation versus durable, portable, ad-hoc query) and by the incidental
but real benefit that a third party can inspect results with no tooling of ours — which serves
R4 and R7 well.

**Rejected.**
- Single relational store used for evaluation too. Rejected: per-query round-trips and planner
  variability defeat W-agent latency; also D70.
- Bespoke binary format only. Rejected: worse for third-party checkability, which is a stated
  requirement rather than a nicety.

**Falsified by.** If the index turns out to be pure overhead — nobody queries it, and exports
serve every need — drop it and keep blobs plus an export.

### D30 — Reproduction is a first-class command with a graded verdict · **FORCED**

**Decision.** `reproduce <record>` returns one of:

| Verdict | Meaning |
|---|---|
| `identical` | Byte-identical semantic record digest |
| `equivalent` | Findings and identities identical; evidence or ordering differ |
| `divergent` | Findings differ — with a diff |
| `not-reproducible` | Tool/extractor/pack version mismatch; refuses to guess |
| `inputs-unavailable` | Named inputs cannot be obtained at their recorded digests |

**Forced by.** R4 ("reproduce it"). A reproduction facility that silently produces a different
answer and calls it success is worse than none, because it manufactures false confidence. The
graded verdict is what makes `not-reproducible` a *reportable outcome* rather than a hidden
divergence.

**Rejected.** Reproduction as "run it again and eyeball the diff." Rejected: no defined notion of
success, so the requirement is unmet in practice even though it appears met.

**Falsified by.** If `identical` is essentially never achievable in practice, then `equivalent`
is the real contract and the record's digest scope is drawn wrongly.

### D31 — Environmental inputs are enumerated and pinned; anything unpinnable is recorded and warned · **FORCED**

**Decision.** Explicitly enumerated and neutralised: locale and collation, time zone, clock,
random sources, hash seeds, path separators, filesystem case sensitivity, Unicode normalisation
form, filesystem iteration order, environment variables, CPU feature-dependent arithmetic,
thread count. Analysis reads none of them. Those that cannot be fully neutralised — notably
filesystem case sensitivity — are recorded in the environment attestation.

**Forced by.** R2 and R4. This is unglamorous and it is where "deterministic" tools actually
fail. Two concrete instances worth naming because they bite in practice:
- **Case sensitivity.** Two files differing only in case coexist on Linux and collide on macOS.
  The tool must *detect* the collision and report it as an error or unknown, never silently
  analyse one file and attribute it to both paths.
- **Unicode normalisation.** macOS filesystems may return NFD path forms where Linux returns
  NFC. Paths participate in identity (D08 `scopeKey`), so unnormalised paths make baselines
  platform-dependent.

**Rejected.** Assume the environment is uniform. Rejected: adopting teams run macOS laptops and
Linux CI, so cross-platform divergence is the normal condition, not an edge case.

**Falsified by.** Nothing; each item is independently verifiable by test.

### D32 — The wire format is the contract; the local store is an implementation detail · **FORCED**

**Decision.** The run record schema and the result document schema are published, versioned, and
compatibility-governed. The cache and index formats are private and may change freely (a cache
version bump simply discards the cache).

**Forced by.** R7. A hosted product consuming results must depend on a stable contract, and that
contract must not be the internal store, or the store can never change and the service becomes
coupled to internals. Naming which artifacts are contracts and which are not is the whole
decision.

**Rejected.** Let the service read the local database. Rejected: couples the service to
internals and quietly makes the service's needs govern local storage evolution.

**Falsified by.** Nothing identified.

### D33 — Always a content digest; cryptographic signing optional and pluggable · **FORCED** (never required) / **PREFERRED** (design)

**Decision.** Every record carries its own content digest. Signing is an optional hook (external
signer, no key management in the tool). Verification of *reproducibility* never requires a
signature.

**Forcing.** That signing is not required is **FORCED** by R1 (keys imply infrastructure) and R7
(no service required). The digest-plus-optional-signer shape is **PREFERRED**, and this is where
Part 1 item 3 bites: if "prove" means audit-grade, this decision is under-built.

**Rejected.** Built-in key management. Rejected: strains R1 and expands scope into a domain the
brief does not ask for.

**Falsified by.** A stated requirement for tamper evidence against a motivated insider. Then
signing and an append-only anchored log become mandatory.

### D34 — SARIF is an export, not the native format · **PREFERRED**

**Decision.** Native result document first; SARIF conversion as an export.

**Why not native.** SARIF cannot faithfully carry coverage, unknowns with materiality, proof
trees, or baseline attestation, and its `partialFingerprints` are too weak for D08. Making it
native would force the domain model to shrink to what SARIF can say — which would silently
delete D05 and D06, the two most valuable decisions in this derivation.

**Why export anyway.** CI ecosystems consume it, and interoperation is cheap.

**Falsified by.** If ecosystem integration proves to be the dominant adoption path, SARIF
fidelity becomes a first-class constraint on the model — worth knowing early, since it pulls
against D05.

### D35 — Result output is streamable · **PREFERRED**

**Decision.** The result document is emitted in a form that can be produced and consumed
incrementally (record-per-line for findings, with header and trailer sections).

**Forcing.** PREFERRED, resting on an assumption about output volume at 100k files. If a
whole-document form fits comfortably in memory for realistic repositories, this is unnecessary.

**Falsified by.** Measured output size on a large repository with a substantial pre-existing
violation set — which is precisely the adoption condition R5 describes.

---

## Part 8 — "Only new violations", and surviving tool upgrades

This is R5, and it is the requirement with the most failure modes. I enumerate the failure modes
first, because each decision below exists to close one.

| # | Failure mode | Visible? | Consequence |
|---|---|---|---|
| F1 | Baseline rots on line drift → flood of false "new" | Loud | Team stops trusting the gate |
| F2 | Upgrade changes rule semantics → baselined findings resurface as new | Loud | Upgrade blocked; team pins old version forever |
| F3 | Upgrade changes rule semantics → **new** findings silently match old baseline entries | **Silent** | Gate quietly stops gating |
| F4 | New rule added by upgrade → all its findings are "new" → CI breaks on pre-existing debt | Loud | Upgrade blocked |
| F5 | Baselined code deleted, entry retained → later reintroduction silently suppressed | **Silent** | Gate quietly stops gating |
| F6 | Baseline re-keyed silently during a scheme change | **Silent** | Nobody can audit what is suppressed |

F3, F5 and F6 are the dangerous ones because they are invisible: the tool keeps reporting green
while its gating power erodes. Every silent failure here must be converted into a loud one.
That is the organising principle of this part.

### D36 — A baseline is an attested finding-identity set, not a list of locations · **FORCED**

**Decision.** A baseline records: the set of `FindingIdentity` values; the `ConfigDigest`; the
rule ids with versions and behaviour digests it was taken against; the identity scheme version;
the adoption revision; and per-entry adoption metadata (when, by what, optional reason).

**Forced by.** R5. Every field is load-bearing: without ruleset versions you cannot detect F2/F3;
without the scheme version you cannot detect F6; without the revision you cannot replay (D39);
without config digest you cannot detect a parameter change (D09).

**Rejected.** A list of `file:line:rule` entries. Rejected: F1 immediately, F3 and F5 eventually.

**Falsified by.** Nothing identified.

### D37 — Ambiguity resolves to *report*, never to *suppress* · **FORCED**

**Decision.** A baseline entry suppresses a finding only when it provably corresponds to it.
Anything else — ambiguous match, multiple candidate matches, scheme mismatch, digest drift —
results in the finding being reported.

**Forced by.** R5's "trustworthy." Closing F3. The asymmetry is deliberate and non-negotiable: a
false "new violation" is a visible annoyance that a human resolves in minutes; a false
suppression is an invisible loss of the tool's entire purpose. When a gate is uncertain, it must
fail closed.

**Rejected.** Fuzzy matching with a similarity threshold. Rejected: makes the gate's power depend
on a tunable that will be tuned in the direction of quiet, and the matching decision becomes
unexplainable, violating R4.

**Falsified by.** If fail-closed produces so much noise at adoption that teams cannot get to
green, the *identity scheme* (D08) is too brittle. The resolution is a better scheme, not a
looser gate.

### D38 — Rules absent from the baseline's ruleset are `pending-adoption`: reported, gate-neutral by default, and always enumerated · **PREFERRED**

**Decision.** A rule not present in the baseline's recorded ruleset is in a third state, distinct
from "found nothing then." Its findings are reported; by default they do not fail the build; and
the run output **must** contain a section enumerating pending-adoption rules, with a distinct
exit class so CI can see it. `--strict-new-rules` makes them gate immediately.

**Forcing.** PREFERRED. Closing F4 requires *some* third state — that much is forced — but the
default policy is a judgment call, and it is a genuine tension: gate-neutral-by-default means a
newly added rule does not protect you until adopted, which is a widening. It is acceptable only
because it is *loud*: enumerated in output, distinguished in exit status. A silent version of
this would be unacceptable.

**Rejected.**
- Treat new rules as gating immediately. Rejected: breaks CI on every upgrade for pre-existing
  debt, so teams stop upgrading, and R5's "across tool upgrades" fails by never upgrading.
- Auto-baseline new rules on first sight. Rejected: silently accepts unexamined violations,
  which is F3 by another route and defeats the point of adding the rule.

**Falsified by.** Observed behaviour at adoption. If teams routinely ignore the pending section
and rules sit unadopted indefinitely, gate-neutral-by-default is the wrong default and this
should invert to strict with an explicit grace mechanism.

### D39 — Behaviour-digest drift triggers re-attestation by replay at the baseline revision; if the revision is unavailable, entries become `needs-review` · **PREFERRED**

**Decision.** When a rule's behaviour digest changes without an adopted version bump:
1. If the baseline revision is obtainable, re-evaluate the rule *at that revision* with the new
   implementation. If the resulting finding set matches what the baseline recorded, the entries
   are automatically re-keyed and re-attested — the change was behaviour-preserving for this
   codebase.
2. If it does not match, the difference is surfaced for explicit adoption. Nothing is
   auto-suppressed.
3. If the revision cannot be obtained (shallow clone, rewritten history), the affected entries
   become `needs-review`: reported, not suppressed.

**Forcing.** PREFERRED as a mechanism; the *requirement* that drift not silently re-map baseline
entries is FORCED (F3). Replay is the strongest available answer because it tests the change
against *this* codebase rather than against the rule author's intent — but it depends on history
availability, which is why D14's conformance corpus exists as the independent check.

**Rejected.**
- Invalidate all baseline entries on any digest change. Rejected: too aggressive — any internal
  refactor of the tool would invalidate every baseline, which makes upgrades painful enough that
  teams stop upgrading.
- Trust the version bump. Rejected: F3.

**Falsified by.** If replay is too slow to be practical at 100k files, the conformance corpus
must carry the whole burden, and D14's mutation-coverage check becomes essential rather than
nice-to-have.

### D40 — Stale entries are reported and prunable; never silently retained · **FORCED**

**Decision.** A baseline entry whose scope no longer exists is `stale`. Stale entries are
reported, do not suppress anything, and can be pruned by an explicit command. Baselines are
expected to shrink.

**Forced by.** R5, closing F5. A retained entry over deleted code is a landmine: reintroducing
that code later is silently suppressed. Also, unpruned baselines only ever grow, and a
monotonically growing suppression set is not a debt-reduction mechanism.

**Rejected.** Retain entries indefinitely for safety. Rejected: accumulates invisible
suppression authority, which is the opposite of safety.

**Falsified by.** If churn makes entries flip between stale and live (a file moving in and out of
scope), staleness needs hysteresis or scope-aware matching. The reporting requirement stands
regardless.

### D41 — Baseline migration is explicit, auditable, and never implicit · **FORCED**

**Decision.** An identity-scheme change or a format-version change requires an explicit migration
command that produces a reviewable diff: entries re-keyed, entries dropped, entries needing
review. The tool refuses to read a baseline of an unknown version rather than interpreting it
optimistically.

**Forced by.** R5, closing F6. If re-keying happens implicitly, no one can ever answer "what is
currently suppressed and why," which fails R4 as applied to the gate itself.

**Rejected.** Best-effort implicit migration. Rejected: F6, and it makes the gate's state
unauditable — the exact opposite of the requirement.

**Falsified by.** Nothing identified.

### D42 — Baseline gating and finding-set diffing are one mechanism · **PREFERRED**

**Decision.** One `diff(currentFindingSet, referenceFindingSet) → FindingDelta` operation.
Baseline gating passes the attested baseline as the reference; the interactive "did I break
anything" query passes the session's last-known state; PR gating passes the merge-base run.

**Forcing.** PREFERRED as a factoring, though strongly indicated: given D22 and D36 both need set
difference over identities, two implementations would be a place for them to disagree.

**Payoff.** The CI-critical path and the highest-volume interactive path exercise the same
comparison logic, so interactive use continuously tests the code CI depends on.

**Rejected.** Separate implementations tuned per use. Rejected: divergence risk in the most
credibility-sensitive logic in the system.

**Falsified by.** If the interactive path needs a materially different comparison (e.g.
approximate matching for speed), the unification breaks — and that would need to be an explicit,
labelled difference, not a quiet one.

---

## Part 9 — Reporting what could not be determined

### D44 — Unknowns are typed, scoped, caused, and materiality-tagged · **FORCED**

**Decision.** A closed set of unknown kinds, each carrying scope, cause, and materiality (D06):

| Kind | Cause |
|---|---|
| `unsupported-language` | No extractor for this file type |
| `parse-failure` | Syntax error, or unsupported dialect/version |
| `resolution-failure` | Import unresolvable, dynamic dispatch, reflection, code generation not run, missing dependency metadata |
| `tier-unavailable` | Rule requires tier-2; language provides tier-1 only |
| `budget-exhausted` | Deterministic budget hit (D25) |
| `baseline-ambiguous` | D37 |
| `baseline-needs-review` | D39 |
| `baseline-stale` | D40 |
| `extension-faulted` | Extension errored or was declined (D51) |
| `hint-validated` | Provisional trust tier (D24) |
| `inputs-mutated` | D02 |
| `case-collision` / `path-normalisation` | D31 |

**Forced by.** R4 × R3 × W-ci. Typed rather than free-text because CI must gate on them and a
consuming product must aggregate them; free-text unknowns are unreportable and ungatable.

**Rejected.** Free-form warnings. Rejected: ungatable, unaggregatable, ignored.

**Falsified by.** A cause that does not fit any kind indicates the taxonomy is incomplete —
expected, and the reason the set is versioned along with the result schema.

### D45 — Heuristics must be declared and identified, never silent · **FORCED**

**Decision.** Where an extractor must guess (an import that could resolve to several targets, a
dynamically constructed path), it must either emit a `resolution-failure` unknown or apply a
*named, versioned heuristic* recorded on the resulting facts. Findings whose evidence includes
heuristic facts are marked as such.

**Forced by.** R2 and R4. Silent guessing is indistinguishable from knowledge in the output, so
a reviewer cannot assess a claim's strength — which is precisely what R4 asks them to be able to
do. Note this is a *determinism-preserving* allowance for imprecision: a heuristic may be wrong,
but it must be repeatably wrong and visibly wrong.

**Rejected.** Best-effort resolution with no marking. Rejected: produces confident-looking
findings resting on guesses, which damages credibility more than an honest unknown.

**Falsified by.** If nearly every fact ends up heuristic, the marking loses signal and the tier
model (D04) is drawn in the wrong place.

---

## Part 10 — Process and deployment shape

### D46 — One binary; three drivers: one-shot, resident daemon, stdio adapter · **PREFERRED**

**Decision.** A single self-contained executable with three entry modes:
- **one-shot** — full analysis, cold store, exit. Serves W-ci.
- **resident daemon** — long-lived, holds the warm fact base and graph, serves clients over a
  local socket. Serves W-agent.
- **stdio adapter** — a thin client speaking a line-oriented request/response protocol on stdin
  and stdout, for agents that spawn a child process. Connects to the daemon if present, or runs
  embedded if not.

**Forcing.** That residency must exist is **FORCED** (W-agent at 100k files cannot pay cold-start
per query). This particular three-driver shape is **PREFERRED**: a stdio-only design is simpler
but cannot share a warm fact base between two agents working the same repository, which I judge
likely enough to design for.

**Rejected.**
- Spawn the CLI per query. Rejected: cold start at 100k files is fatal to W-agent.
- Daemon only. Rejected: W-ci explicitly forbids residency, and a daemon-only design would make
  CI depend on lifecycle management it should not have.

**Falsified by.** If multi-agent concurrent use does not occur, the daemon is unnecessary
complexity and the stdio adapter alone suffices.

### D47 — The daemon is never required and never authoritative · **FORCED**

**Decision.** Any query answerable through the daemon is answerable identically without it
(`--no-daemon`). The daemon's identity includes the tool version and `ConfigDigest`; a client
whose expectations do not match refuses the daemon and falls back rather than trusting it. The
daemon holds no state that cannot be recomputed.

**Forced by.** R1 (no service dependency for any result — a local daemon is still a service) and
R4 (a result must not depend on which process happened to answer). This is D01's
"cache cannot change results" applied to residency, and it is what keeps the interactive path
verifiable.

**Rejected.** Daemon-owned authoritative state. Rejected: creates a second truth and a
correctness dependency on process lifetime.

**Falsified by.** Nothing identified.

### D48 — Local socket only; no TCP; no network anywhere in the analysis path · **FORCED**

**Decision.** Unix domain socket or named pipe, with filesystem permissions as the access
control. No TCP listener. The analysis path performs no network I/O at all; pack fetching is a
separate, explicit, non-analysis operation.

**Forced by.** R1 plus the non-goal of multi-tenant behaviour. Also: no network in analysis makes
determinism testable by sandboxing rather than by inspection.

**Rejected.** Loopback TCP for convenience. Rejected: adds an authentication problem the
non-goals say is out of scope, and invites exposure.

**Falsified by.** Nothing identified.

### D49 — No filesystem watcher in the first version · **PREFERRED**

**Decision.** No inotify/FSEvents watcher. Validity is established per query, using the
caller-supplied changed set when provided, and validity hints otherwise (D24).

**Forcing.** PREFERRED. Watchers reduce latency but introduce a large class of platform-specific
bugs and event-loss failure modes, each of which manifests as a *stale wrong answer* — the worst
possible failure for this tool.

**Rejected.** Watcher from the start. Rejected on risk versus unmeasured benefit; note that
W-agent's callers *know* what they changed and can say so, which removes most of the motivation.

**Falsified by.** If per-query revalidation cannot meet the interactive budget even with hints
and caller-supplied change sets, a watcher becomes forced — and must then be paired with a
periodic full reconciliation to bound event-loss damage.

### D50 — Version control is a narrow, optional, read-only adapter · **FORCED**

**Decision.** A small interface providing: current revision, revision content retrieval, merge
base, and changed-files-between-revisions. Git first, others possible. The tool never writes to
version control. Features needing revisions (D39 replay, merge-base diffing) report `unavailable`
when it is absent; everything else works without it.

**Forced by.** The non-goal ("not replacing version control") plus R1 plus R5 (baselines
reference revisions). Also: baselines are ordinary files the team commits, so version control
provides history and review for free rather than being reimplemented.

**Rejected.**
- Require a git repository. Rejected: R1 says offline on a laptop, not "in a repository", and
  analysing an unpacked archive is a legitimate use.
- Deep integration (hooks, notes, refs for storing baselines). Rejected: crosses the non-goal
  and couples results to history shape (see D43).

**Falsified by.** Nothing identified.

**One coupling worth flagging.** File selection commonly wants to honour ignore files. That
couples the analysed set to version-control configuration. It is acceptable only because the
*resolved* file set with digests is recorded in the run record (D27), making selection auditable
after the fact. Without that record, ignore-file-driven selection would be a silent
determinism hole.

---

## Part 11 — Extension model and authority limits

R6 explicitly leaves the extent open, so this part is where I most need to distinguish forcing
from preference. The forced part is the *shape*: authority must be stratified, because the
requirements assign different trust to different capabilities. What sits at each level is partly
judgment.

### D51 — Authority ladder, with the zero-authority rung as the primary surface · **FORCED**

| Rung | Surface | Authority | Trust needed |
|---|---|---|---|
| 0 | **Rules** — declarative queries over facts | None: no I/O, no computation beyond the query language, deterministic budget, guaranteed termination | None. Loadable from untrusted sources |
| 1 | **Declarative extractors** — grammar plus tree-pattern-to-fact mappings | Reads the file being analysed; pure | Low. Loadable with review |
| 2 | **Impure extractors** — shell out to a real toolchain | Process execution, environment, possibly network | High. Explicit opt-in per workspace |
| 3 | **Reporters** — render results | Write to stdout / a named file | Medium; sandboxed to output |

**Forced by.** R2 × R4 × R6. If the only extension surface required arbitrary code, then either
third-party logic is disallowed (contradicting R6) or determinism becomes unenforceable
(contradicting R2). The zero-authority rung is what makes third-party contribution compatible
with the determinism guarantee, so it must exist and must be the default.

**Rejected.** A single plugin surface with uniform trust. Rejected: forces trust to the level of
the most demanding extension, so a grammar contribution would carry the same authority as a
compiler integration.

**Falsified by.** If rung 0 proves insufficient for most useful third-party logic, the ladder is
correct but rung 0 is drawn too narrowly — and D55's sandboxed imperative rung becomes necessary
rather than optional.

**Note on how this interacts with D13.** Guaranteed termination at rung 0 is not an incidental
property; it is what allows loading an unreviewed rule at all. This is a substantive argument for
the Datalog-shaped evaluator that is independent of expressiveness.

### D52 — Tier-2 extractors are first-party, in-tree, and versioned with the tool · **PREFERRED**

**Decision.** Deep semantic extraction for L1 and L2 ships with the tool, versioned with it, not
loadable as third-party extensions. The number two is a current fact, not an architectural
constant: adding a third deep language must not require structural change.

**Forcing.** PREFERRED, though strongly indicated. R3 makes deep analysis a core competency, and
tier-2 correctness is where a subtle error produces confidently wrong findings — which is a
credibility failure under R2. Delegating that to third parties while promising determinism seems
unwise. But it is a judgment about trust and maintenance capacity, not a requirement.

**Rejected.** Tier-2 as a plugin surface. Rejected on the credibility argument, and because
tier-2 extractors need the deepest access to internal fact schemas, which would freeze those
schemas as public contracts prematurely.

**Falsified by.** A high-quality external tier-2 contribution for a third language would make
this a bottleneck rather than a safeguard.

### D53 — Impure extractors are opt-in, mark the run `externally-dependent`, and have their outputs captured verbatim · **FORCED**

**Decision.** Extractors that must invoke an external toolchain (a package manager to obtain
dependency metadata, a compiler to obtain resolved types) are permitted, but:
- Enabled only by explicit workspace configuration.
- Their inputs and outputs are recorded verbatim in the run record.
- The run is marked `externally-dependent`, and reproduction uses the recorded outputs — so the
  run remains *reproducible* even though it was not *self-contained*.
- Their version and invocation are part of `ConfigDigest`.

**Forced by.** R2 × R4 versus reality. Real dependency resolution often genuinely requires the
ecosystem's own tooling. The choice is between forbidding it (losing accuracy), allowing it
silently (losing determinism), or allowing it with capture. Capture is the only option that
keeps R4 intact: the impurity is not prevented, it is *recorded*, which converts an
unreproducible run into a reproducible one.

**Rejected.**
- Forbid entirely. Rejected: would cripple tier-2 for ecosystems where resolution is
  build-system-dependent.
- Allow without capture. Rejected: silently breaks reproducibility, and the breakage is invisible
  in the output.

**Falsified by.** If captured outputs are too large or too machine-specific to be useful for
reproduction, capture is theatre and the honest move is to forbid impure extraction and accept
reduced accuracy.

### D54 — Extension content digests participate in `ConfigDigest` · **FORCED**

**Decision.** Every loaded extension — rule pack, grammar, mapping, reporter — contributes its
content digest to `ConfigDigest`.

**Forced by.** R4 (reproduction needs to know exactly what ran) and R5 (a third-party rule
change must invalidate caches and trigger the D39 re-attestation path rather than silently
altering what is gated). Without this, a pack update changes the gate with no trace.

**Rejected.** Digest only first-party components. Rejected: makes third-party rule churn
invisible, which is F3 arriving from outside.

**Falsified by.** Nothing identified.

### D55 — No native plugin ABI. A fuel-metered WebAssembly rung is held in reserve · **PREFERRED**

**Decision.** No dynamic-library plugin interface. If imperative extension logic proves
necessary, the mechanism is WebAssembly with: no host imports beyond a fact-query interface, no
clock, no randomness, no threads, no floating-point nondeterminism, and *fuel metering* as the
deterministic budget.

**Forcing.** Rejecting native plugins is close to FORCED (unbounded authority defeats D51;
reproduction would depend on binary artifacts, defeating R4; ABI versioning across tool upgrades
defeats R5). Choosing WebAssembly as the reserve mechanism is PREFERRED — its notable fit is that
fuel metering is *exactly* the deterministic budget D25 requires, which no native mechanism
provides.

**Rejected.**
- Native plugins. Rejected as above.
- An embedded general-purpose scripting runtime. Rejected: most such runtimes offer no
  deterministic budget and expose ambient authority by default.

**Falsified by.** If rung 0 suffices indefinitely, this stays unbuilt — the intended outcome.

### D56 — Third-party tool output may be imported, marked unverifiable, non-gating by default · **PREFERRED**

**Decision.** Findings imported from other analysers (via SARIF) are accepted into the result and
record, tagged `externally-produced` with `evidence: unverifiable`, and do not gate by default.
They can be baselined, but their identity is explicitly weaker and labelled as such.

**Forcing.** PREFERRED — nothing requires it. It is a cheap accommodation of the ecosystem that
does not compromise the core, and it makes the D69 rejection a scoping decision rather than a
refusal to interoperate.

**Rejected.** Treat imported findings as equal to native ones. Rejected: their evidence cannot
satisfy R4 and their identity cannot satisfy R5, so equal treatment would silently dilute both
guarantees.

**Falsified by.** If imported findings become the majority of what teams gate on, the tool has
become D69 with extra steps, and the whole architecture needs re-justification.

---

## Part 12 — Failures and exit status

### D57 — Distinguishable exit classes · **FORCED**

| Code | Class | Meaning |
|---|---|---|
| 0 | success | Gating rules satisfied; coverage acceptable; no material unknowns |
| 1 | policy-failure | Gating violations found (the only code meaning "your code violates a rule") |
| 2 | usage/config | Invalid arguments, invalid or unresolvable configuration |
| 3 | undetermined | Material unknowns exceeded the configured tolerance (D06) |
| 4 | baseline-integrity | Ambiguous, unmigrated, drifted, or unreadable baseline (D37/D39/D41) |
| 5 | aborted | Deterministic budget exceeded, wall-clock safety valve, or interruption (D25) |
| 70 | internal-error | Defect in the tool |

**Forced by.** W-ci: "must fail the build **correctly**." The requirement is not "exit nonzero";
it is that a CI configuration can respond *differently* to different conditions. Collapsing
these into 0/1 makes "the analyser is broken" indistinguishable from "your code is bad", which
guarantees the wrong response.

**Rejected.**
- Binary 0/1. Rejected as above.
- Rich status only in the output document. Rejected: CI systems branch on exit codes; requiring
  a JSON parse to determine build outcome is fragile and often not available in the failure path.

**Falsified by.** If CI systems in practice cannot branch on codes beyond zero/nonzero, the
distinctions must additionally be surfaced in a way those systems consume — which changes the
surface, not the requirement to distinguish.

### D58 — Fail closed: never exit 0 when a gating decision could not be made · **FORCED**

**Decision.** Any condition preventing a sound gating decision yields a nonzero class (3, 4, or
5), never 0. There is no "partial pass."

**Forced by.** W-ci correctness plus R4. A green build produced by analysis that did not run is
the single worst output this tool can produce, because it actively removes the protection the
team believes it has.

**Rejected.** Warn and pass on incomplete analysis. Rejected: this is the common industry
behaviour and it is precisely the failure R4/R5 exist to prevent.

**Falsified by.** Nothing identified.

### D59 — Internal errors never use the policy-failure code · **FORCED**

**Decision.** Defects exit 70, never 1.

**Forced by.** W-ci correctness, for a human-behaviour reason that is nonetheless real: teams
interpret 1 as "my code is bad." A crash reported as 1 gets worked around — suppressed, or the
rule disabled — rather than reported. Miscoding tool defects as policy failures actively degrades
the rule corpus over time.

**Rejected.** Any nonzero code for any failure. Rejected as above.

**Falsified by.** Nothing identified.

### D60 — stdout is data; stderr is diagnostics; refuse-don't-guess on unknown artifact versions · **FORCED**

**Decision.** Machine-readable results go to stdout (or a named file); human diagnostics and
progress go to stderr. The tool refuses to read an artifact whose format version it does not
understand — with the single exception of caches, which are discardable and so are silently
discarded on version mismatch.

**Forced by.** W-ci (pipeable, parseable output) and R4 (an artifact interpreted optimistically
produces a result whose meaning is unknown). The cache exception is safe precisely because of
D01: a discarded cache cannot change an answer.

**Rejected.** Interleaved output; best-effort forward compatibility. Rejected: the first breaks
piping, the second produces results of unknown meaning.

**Falsified by.** Nothing identified.

---

## Part 13 — The determinism boundary: what the tool refuses to do

### D61 — An explicit prohibition list, enforced mechanically · **FORCED**

Within the analysis path (phases 1–5), the following are prohibited, and the prohibition is
enforced by tests and by sandboxing rather than by convention:

- No clock, no timers, no wall-clock-dependent behaviour affecting results (D25).
- No randomness; no randomly-seeded hash iteration in any output path. Ordered or sorted
  containers only where iteration order can reach output.
- No environment variable reads. CLI plumbing may read them; it records what it read.
- No locale, no locale-dependent collation or case folding. Case operations are explicitly
  Unicode-versioned.
- No network (D48).
- No floating-point values in facts at all. Cheap to guarantee; eliminates a whole class of
  cross-platform divergence.
- Paths canonicalised: repo-relative, forward-slash, NFC-normalised. Case collisions detected
  and reported (D31).
- Byte offsets are truth; line and column are derived for presentation (Part 4, entity notes).
- Unordered filesystem iteration is sorted before use.

**Forced by.** R2, directly. Each item is a way "deterministic" tools actually turn out not to
be. Making the list explicit and testable is what distinguishes a determinism claim from a
determinism aspiration.

**Rejected.** Treat determinism as an emergent property of careful coding. Rejected: it is
neither emergent nor observable in review; every item here needs a test.

**Falsified by.** Each item is independently testable; a failing test falsifies that item, not
the list.

---

## Part 14 — Scale

### D62 — Intern aggressively; the fact store holds no source text · **PREFERRED**

**Decision.** Paths, identifiers, and symbol names are interned to integer ids. Relations are
columnar over those ids. The fact store holds no source text — only spans referencing content
digests. Source is re-read on demand for rendering.

**Forcing.** PREFERRED, resting on a memory estimate rather than a stated requirement: at 100k
files, tier-1 facts plausibly number in the tens of millions, and storing strings inline would
dominate memory.

**Rejected.** Store text alongside facts for convenient rendering. Rejected on the memory
estimate; rendering is rare (W-human is explicitly "occasional") and re-reading is cheap.

**Falsified by.** Measured memory at 100k files. If facts are far fewer than estimated, interning
is unjustified complexity.

### D63 — Tier-2 cached per project, with a persisted cross-project symbol index · **PREFERRED**

**Decision.** Tier-2 extraction is cached at project granularity, keyed by the project's unit
digest and a digest over the symbol indexes of its dependencies. Cross-project references
resolve through the persisted index.

**Forcing.** PREFERRED. It follows from D11 and D20 rather than from a stated requirement.

**Rejected.** Whole-workspace tier-2 as one cache unit. Rejected: any edit invalidates everything,
so W-agent gets no benefit from caching the most expensive phase.

**Falsified by.** The cascade risk in D20: if dependency-index digests change on nearly every
edit, this granularity provides no benefit and per-symbol invalidation is required.

### D64 — Cache garbage collection is an explicit command; eviction cannot change results · **FORCED**

**Decision.** The cache is bounded and pruned by an explicit command with a size or age policy.
Eviction is always safe.

**Forced by.** R1 (a laptop has finite disk) and D01 (eviction safety is a property of purity,
not a feature). Worth stating because content-addressed caches grow without bound across
branches and worktrees.

**Falsified by.** Nothing identified.

### D65 — Performance targets stated as architectural falsifiers, not as requirements · **PREFERRED / partly GUESSED**

**Decision.** Targets, flagged as invented (Part 1 item 5):

| Scenario | Target | If missed |
|---|---|---|
| Cold full run, 100k files, tier-0/1, 8 cores | ≤ 3 min | Reconsider eager tier-1; move to on-demand extraction |
| Warm incremental, 5 changed files, full ruleset | ≤ 1 s end to end | D21 inverts: incremental view maintenance becomes forced |
| Warm phase-4 evaluation alone, 100k files | ≤ 300 ms p50 / 1 s p95 | Same as above |
| Resident memory, 100k files, tier-1 | ≤ 4 GB | Memory-mapped or on-disk fact store becomes forced |
| Cold full run, 1k files | ≤ 5 s | Fixed overhead is too high for the small-repo case |

**Forcing.** GUESSED as to the numbers; PREFERRED as to the practice of writing them down. Their
purpose is to make architectural decisions falsifiable rather than arguable.

---

## Part 15 — Implementation language

### D66 — Core implemented in Rust · **PREFERRED**

**Decision.** Rust for the core: file selection, extraction orchestration, fact store, evaluator,
identity, baseline, records, CLI, daemon.

**Forcing.** **PREFERRED**, not FORCED. No stated requirement names a language. The supporting
arguments, in descending strength:

1. **Single self-contained binary** across macOS, Linux, and Windows with no runtime to install
   (R1). Achievable in Go and Zig too; harder in managed or interpreted languages.
2. **No garbage-collection pauses in a resident low-latency process** (W-agent). This favours
   Rust over Go, though Go's GC is likely adequate; the fact base is a large long-lived object
   graph, which is where GC costs show up most.
3. **Determinism control** — explicit control over container iteration order and hashing. Rust's
   default hash map is randomly seeded per process and Go's map iteration is deliberately
   randomised, so *both* need the same discipline (D61); this is not a differentiator, and I
   want to record that I checked rather than assume it favoured Rust.
4. **Ecosystem alignment** with the parsing and sandboxing choices below (D67, D55).

**Rejected.**
- **Go.** Genuinely live. Better build simplicity and a lower contribution barrier — which would
  matter a great deal for R6 if the primary extension surface were Go code. It is not (D51), and
  that is what mostly dissolves this argument. Cost: GC in the resident path.
- **C++.** No advantage here and a worse safety and build story.
- **A managed or interpreted language.** Fails the single-binary and 100k-file performance
  arguments together.

**Falsified by.** If the core proves to be I/O-and-orchestration-bound rather than
compute-bound, Rust's advantage largely evaporates and Go's contribution and build advantages
dominate. Worth checking against an early profile rather than assumed.

### D67 — Tier-0/1 parsing via a generic incremental parser framework (tree-sitter shaped) · **PREFERRED**

**Decision.** Grammar-driven parsing with a framework offering: many existing grammars, error
recovery, and *incremental* reparsing.

**Forcing.** PREFERRED, but with an unusually strong fit worth spelling out:
- **Many grammars** serves R3's breadth directly, and turns "support a new language" into
  supplying data rather than writing code — which is what makes rung 1 of D51 viable.
- **Error recovery** is required, not optional: tier-1 facts must be extractable from files that
  do not fully parse, because agents query mid-edit and CI encounters unsupported dialects. A
  parser that fails wholesale on a syntax error converts a partial answer into an unknown.
- **Incremental reparsing** maps directly onto W-agent: an agent edits a region, and only that
  region is reparsed.

**Rejected.**
- Hand-written parsers per language. Rejected: does not scale to R3's breadth.
- Regex/line-based extraction. Rejected: cannot support tier-1 structural facts, and would make
  most rules unexpressible.

**Falsified by.** If grammar quality across the long tail is too poor to yield reliable tier-1
facts, breadth is illusory and the honest response is to narrow the language claim.

### D68 — Tier-2 by purpose-scoped reimplementation, with compiler-backed enrichment as an explicitly impure option · **PREFERRED**

**Decision.** Implement, in the tool, only the resolution that declared rules actually need:
module and import resolution, symbol binding, call graph, inheritance and implementation
relations. **Not** full type inference. Where a language's real semantics are unreachable without
its own toolchain, offer that as an impure extractor (D53) whose outputs are captured.

**Forcing.** PREFERRED, and this is the highest-cost, highest-risk decision in the design.

**The tension, stated plainly.** Deep analysis has two honest options. *Embed the language's own
compiler*: accurate, but imports its impurity and version skew, and pulls against R2/R4.
*Reimplement resolution*: pure and deterministic, but expensive to build and permanently behind
the language. Scoping the reimplementation to what rules need is what makes the second option
finite. Attempting faithful type inference for a language with a structural, inference-heavy type
system is not a finite project, and pretending otherwise is the most likely way this design
fails to ship.

**Rejected.**
- Full semantic fidelity in-tool. Rejected as effectively unbounded.
- Compiler-backed only. Rejected: R2's guarantee would then be contingent on toolchain pinning,
  and would have to be advertised as such.

**Falsified by.** If the declared rule corpus needs type-level reasoning (a rule about
assignability, or about generic instantiation), scoped resolution is insufficient and the impure
path becomes primary — at which point the determinism claim must be honestly restated as
"deterministic given a pinned toolchain," which is a weaker product.

### D73 — The host language is decoupled from the deep languages · **PREFERRED**

**Decision.** Implementing the tool in one of L1/L2 is not treated as an advantage worth
optimising for.

**Forcing.** PREFERRED, recorded because it is a tempting trap: writing the tool in a deep
language lets you call that language's real compiler in-process. That convenience buys accuracy
for one language and pays for it in every other requirement — performance at 100k files,
single-binary distribution, resident-process latency, and determinism. Since tier-2 needs a
purity boundary anyway (D53), it may as well be a process or embedding boundary, which frees the
host choice entirely.

**Falsified by.** If in-process access to a real compiler proves to be the only viable route to
useful tier-2 for both deep languages, host choice becomes entangled and D66 must be revisited.

### Languages, in total

| Component | Language | Why |
|---|---|---|
| Core, CLI, daemon, evaluator, store | Rust | D66 |
| Grammars | Grammar DSL of the parser framework | D67 |
| Rules | Purpose-built declarative rule language | D12/D13 |
| Policy | TOML | D17 |
| Extractor mappings (tier 0/1) | Declarative pattern-to-fact mappings | D51 rung 1 |
| Tier-2 extractors | Rust, in-tree | D52 |
| Reserved imperative extension rung | WebAssembly | D55 |

---

## Part 16 — Falsification program

The derivation is only worth as much as its testability. These are the experiments that would
most efficiently falsify it, ordered by how much they would change.

1. **Collect a real rule corpus.** Classify each rule as local-syntactic, cross-file-syntactic,
   or resolution-dependent; and as recursive or non-recursive. This single artifact adjudicates
   D13, D43, D70, and the D22 justification — the deepest assumptions in the design.
2. **Baseline churn study.** Replay 6–12 months of real history through candidate identity
   schemes (location, content-only, D08 tuple) and measure false-new and false-suppressed rates
   per commit. Adjudicates D07, D08, D37, and the D43 comparison.
3. **`--no-cache` parity, and parallelism parity, in CI from the first commit.** Adjudicates D01,
   D19, D26. If these are not in place before the cache exists, purity will already be broken by
   the time anyone checks.
4. **Interactive latency measurement at 100k files** with a warm fact base and a five-file change.
   Adjudicates D21 (the phase-4 threshold), D24 (whether trust tiers are needed at all), and D49
   (whether a watcher is forced).
5. **Cross-platform determinism run**: identical inputs on macOS and Linux, compare record
   digests. Adjudicates D31 and D61 as a whole, and will almost certainly fail the first time on
   path normalisation or case sensitivity.
6. **Upgrade drill.** Take a baseline, change a rule's implementation in a behaviour-preserving
   way and in a behaviour-changing way, and check that D39 classifies both correctly with and
   without the baseline revision available. Adjudicates the core of R5.
7. **Tier-2 scoping probe.** Take the ten most-wanted resolution-dependent rules for L1 and L2
   and determine the minimum resolution needed. Adjudicates D68, the largest cost item.

---

## Part 17 — Decision index

Decision ids run D01–D73 with no gaps and no duplicates.

| Marking | Count |
|---|---|
| **FORCED** | 42 |
| **PREFERRED** | 29 |
| **GUESSED** | 2 |
| **Total** | 73 |

The ratio is worth reading sceptically rather than approvingly. 42 FORCED out of 73 is a high
proportion, and there are two ways that happens: the requirements really are unusually
constraining, or I have been too willing to call something forced. My own audit says mostly the
former — the brief contains three requirements (R2 determinism, R4 checkability, R5 upgrade
trust) that are each *properties of failure modes* rather than features, and requirements of that
shape do force a lot of structure. But the reader of this document should apply pressure to every
FORCED marking rather than to the PREFERRED ones, because a mismarked FORCED is the error that
would do real damage here.

Where the forcing is thinnest, and where I would look first for error:

- **D13 (recursion / Datalog-shaped evaluator).** Rests entirely on an unverified assumption
  about the rule corpus, and cascades into D10, D51, and the largest build cost in the design.
  Experiment 1 should precede any implementation work here.
- **D68 (tier-2 scope).** Largest cost, and the place where an honest determinism claim is most
  likely to have to be weakened.
- **D24 (two trust tiers) and D49 (no watcher).** Both rest on unmeasured latency assumptions.
  Both are deletable if measurement disagrees, which is the correct property for a guess to have.
- **D38 (new rules gate-neutral by default).** A deliberate, loud widening. Defensible, but it is
  a widening, and it is the decision most likely to be judged wrong in hindsight.
- **D66 (Rust).** Marked PREFERRED after failing to find a requirement that forces it. Go remains
  live. I note this specifically because language choice is where habit most often masquerades as
  necessity.

Two decisions I would defend hardest, because they are forced and commonly omitted:

- **D05/D06** — coverage and materiality in the result type. "Zero violations" is not a result;
  "zero violations at this coverage, with these material unknowns" is.
- **D37** — ambiguity resolves to report, never suppress. The asymmetry between a visible false
  alarm and an invisible loss of gating is the whole reason R5 says "trustworthy" rather than
  "correct."
