# Steering 01 — Current-state evidence

**Purpose:** measurements of the **shipping product**, used to estimate porting
cost and to sequence migration.

**Scope rule:** nothing here may size a decision in `../architecture/`. These
figures describe an artifact shaped by constraints the greenfield design does not
have. Using them as design inputs is the specific error that caused this document
set to be restructured — see `../architecture/10-method.md`, method rule 6.

Figures are from `main @ a62509d6` unless noted.

---

## Rule corpus

| # | Measurement | What it means for migration |
|---|-------------|-----------------------------|
| M1 | **~64%** of 141 check files are pure single-file text/pattern; **~26%** single-file syntactic AST | The text tier is the cheapest to port to a declarative IR — the natural first slice |
| M2 | **Exactly 1 of 141** check files consumes flow-sensitive checker semantics (`null-safety`, type-aware default on) | Only one check needs the guest-analyzer path on day one. **This does not mean the target should treat semantics as rare** — see the re-derivation in `../architecture/04-fact-plane.md` |
| M3 | The type checker is reached only via the graph adapter and language service; `parse-fast` documents it as *"the single most expensive operation in a cold run"* | Centralising semantic state is a self-contained slice; the graph adapter already has roughly the target shape |
| M4 | Check bodies are already `analyze(content, filePath)` (128) or `analyzeAll(FileAccessor)` (32) — **91% pure** | Rule mechanics port cheaply. The wide interface is the tool contract, not the check contract |
| M8 | Check file LOC: median **186**, p90 **381** | Compression estimates of "5–20 line rules" are optimistic by ~an order of magnitude. Budget 3–8× on the text tier |
| M9 | Repair is vestigial — **2 of 141** checks emit it | The repair surface is effectively greenfield even inside the existing product |

## Structure and packaging

| # | Measurement | What it means for migration |
|---|-------------|-----------------------------|
| M5 | All **61** workspace packages are version-lockstep | No semver compatibility matrix exists, so consolidation is mechanical rather than compatibility-constrained — subject to the dependents question |
| M6 | The contracts barrel is **exactly 423 lines** of re-exports | A facade existing only to break cycles that exist *because* layers are separate packages. Collapsing the layers removes its reason to exist |

## Outcome and startup

| # | Measurement | What it means for migration |
|---|-------------|-----------------------------|
| M7 | **8** exit/outcome ADRs, **3** distinct exit mappers, **193** non-test exit-capable call sites | Exit classification has never had a single owner. Consolidating to one mapper is high-value and touches many sites — plan it as its own slice |
| M10 | Warm `--version` ≈ 620–680 ms; bootstrap dominated by module-resolution topology, not application compute; `--version` eagerly loads the compiler and grammars | A composition-root defect, fixable **without** any architectural change. Highest ROI, lowest risk — do it first regardless of target |
| M11 | Largest published benchmark tier is **750 files**; 10k–100k unmeasured | Every scale claim is extrapolated. Measure before committing to any latency SLO |

---

## The calibration asymmetry

The most important thing these numbers say collectively:

> **Rule mechanics are portable; rule calibration is not.**

M4 shows 91% of check bodies are already pure functions of their inputs, so
moving them is largely mechanical. What does **not** transfer is the accumulated
false-positive tuning, the knowledge of which edge cases actually bite, and the
fixture corpora that encode it.

That asymmetry is the entire argument for strangling rather than rewriting, and
it makes **fixture parity** — not code review — the acceptance test for any rule
migration. Classification is not calibration.

---

## Open measurements

| Question | Why it blocks a decision |
|----------|--------------------------|
| Fixture-parity cost of re-expressing rules in a declarative IR | The primary risk in any rule migration. Classification says the text tier is eligible; only parity proves calibration survives |
| p50/p95 snapshot cost at 10k+ files, warm and cold | Every latency claim, and the choice of execution topology |
| Baseline population in the wild | Whether the fingerprint-recipe migration design is testable before it is needed |
| External dependents of published sub-packages | Whether consolidation is mechanical or compatibility-constrained. Note: **download counts cannot discriminate** — a meta-package pulling all workspace packages makes counts converge. The signal is dependents |
