# Steering 02 — Reachability and slices

**Status:** SEALED as sequencing. See `00-overview.md` for the one-way rule:
nothing here may constrain `../architecture/`.

Which parts of the target design are reachable incrementally, in what order, and
at what risk. **Most of it is reachable without a rewrite and without a language
decision.**

---

## Migration reachability

**SEALED as a migration property — not an architectural one.** Reachability says
nothing about whether a design is *correct*; it says what a transition costs. An
infeasible-but-correct target is still correct, and steering may legitimately
recommend not pursuing it — but it may never edit the target to make the
transition cheaper. Each element below is classified by whether it can be adopted
incrementally inside the shipping product.

| Element | Incremental? |
|---------|--------------|
| Unified Run identity (kill the session/execution-run split) | **Yes** |
| Always-write Run; projections over one record | **Yes** |
| Fact store behind existing tools (extract once, query many) | **Yes** |
| Semantic guest relocated to provider tier | **Yes** — the existing graph adapter is already close to this shape |
| Declarative tier for the text-pattern rules | **Yes** |
| Baselines/gates as queries over run history | **Yes**, subject to recipe versioning |
| Package consolidation toward ≤5 public contracts | **Yes**, mechanical |
| Narrow `Extractor`/`Rule`/`Projection` replacing `Tool` | **Partly** — needs the fact store first |
| Out-of-process-everything, wire-protocol plugin edge | **No — discontinuity** |
| Rust host | **No — discontinuity** |

> **The conclusion:** every high-value element is host-language-independent. The
> two items requiring discontinuity are exactly the two the language
> deliberation already declined to authorise. The design is therefore actionable
> now without touching the language question.

---

## Strangler slices

**SEALED as sequencing.** Each slice is independently shippable and reversible.
Do **not** implement the target in the order its diagram is drawn.

| # | Slice | Notes |
|---|-------|-------|
| 1 | **Canonical input/output seam** | Resolved project descriptor + resolved config + envelope adapters around current commands. Internal/experimental only until the config, project, and envelope artifacts are reviewed — do not freeze a public ABI here |
| 2 | **One Run projection** | Allocate a parent execution identity, dual-read legacy sessions, always return the resolved identity. No destructive migration yet |
| 3 | **Shared fact service** | Content and provenance keys beneath graph, impact, and a small check slice; compare old and new findings |
| 4 | **Semantic provider** | Centralise TS semantic universes; move the one checker-dependent rule to a guest-side analyzer. Parity fixtures prove the escape hatch |
| 5 | **Rule IR** | Port ~20 text-tier rules with **exact fixture parity**; keep the imperative fallback |
| 6 | **Fingerprint compatibility** | Version-negotiated recipe plus a skipped-release upgrade test **before** changing any subject identity |
| 7 | **Narrow contribution registry** | C-narrow profiles; legacy Tool bridge runs beside it; new features use only the new registry |
| 8 | **Command aliases + package consolidation** | Switch canonical grammar only after docs, CI, and telemetry migration |
| 9 | **Native host evaluation** | A vertical slice consuming the same fixtures and wire contracts; cut over only on distribution, SLO, and maintenance evidence |

Slices 1 and 2 may proceed in parallel — unified Run identity without a shared
fact plane still leaves tools inventing private inventories, and a fact store
without one Run identity still fractures replay. Neither strictly gates the
other.

## Discipline for every slice

**SEALED.** Each slice records:

- **Parity criteria** — what must produce identical output
- **Rollback** — how to revert without data loss
- **Data migration** — including dual-write windows
- **The exact legacy surface it makes removable**

> **Package and command deletion must never lead the replacement capability.**

A Rust cutover requires differential EvidenceDigest, fixture, and SLO proof —
never a schedule.

---

## The minimum vertical prototype

**SEALED.** Before treating this architecture as validated:

1. Snapshot + content-addressed facts for one language
2. Five declarative rules and two imperative rules
3. One graph query (who-calls / blast radius)
4. Always-write Run + MCP show-run + CLI projection parity
5. Gate compare as a query over two Runs
6. Latency and RSS measured on a 10k+ file corpus

### Adversarial proofs the prototype must also pass

1. A worktree mutation mid-analysis **cannot** seal a mixed snapshot
2. A newly added inbound reference invalidates a **negative-query** result; a
   changed compiler config invalidates semantic facts
3. A retained Run remains **explainable after cache GC**
4. Crash and cancel recovery yield one attempt identity and an honest terminal or
   abandoned state — **never a passing empty run**
5. Embedded and warm-engine deployments emit the **same** EvidenceDigest
6. A Probe runs in an ephemeral workspace and cannot mutate the source snapshot
7. Projection parity is semantic across CLI, MCP, SARIF, and HTML
8. **Fixture parity** for re-expressed rules — classification is not calibration
9. A **dual-fingerprint transition** produces zero false net-new across the window
10. Two concurrent CLI processes produce two valid Runs with no lost writes,
    daemon disabled
11. A RepairPlan is refused against a moved worktree, and the accepted path emits
    a linked verification Run

**Success:** evidence parity on the slice, latency budgets met, and no second run
identity.

---

## What a rewrite would risk losing

**SEALED.** Not visible in any diagram, and none of it transfers automatically:

- 152 tuned checks with real-world false-positive calibration
- Six working language adapters
- Qualification and burn-in lanes
- Accumulated knowledge of which edge cases actually bite

The mechanics are more portable than assumed — See [01-current-state-evidence](01-current-state-evidence.md): 91% of rule bodies
are already pure functions of their inputs. The
**calibration** is not. That asymmetry is the whole argument for strangling rather
than rewriting.
