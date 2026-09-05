You are continuing the greenfield architecture → implementation work for the NEXT OpenSIP CLI.

## Repository

- **This repo (current workspace):** `/Users/sb/code/opensip-ai/opensip`
- **Not this repo:** `/Users/sb/code/opensip-ai/opensip-cli` is the *current shipping* TypeScript monorepo. It is a source of *learnings and failure modes*, not a migration constraint.
- Architecture work was moved here from `opensip-cli/docs/internal/coop/` → **`docs/coop/`** in this repo. A pointer remains at `opensip-cli/docs/internal/coop-MOVED.md`.

## What we are building

A **greenfield** local-first, deterministic, offline code-analysis CLI (no language-model calls in core paths). Consumer is **B — build this**: architecture must be specific enough that implementation does not invent week-one forks.

Technical direction already decided (do not re-litigate without new evidence):
- Host language / rewrite: **Rust**
- Semantic providers: **TypeScript + Rust**
- Rust substrate (P-4a): bundled pinned **`rustc_driver` sidecar** (see delivery binding)
- Factoring: **orchestration host + pure evaluation core**
- First topology: **one-shot host** (resident host optional / measurement-gated)
- **Probe / scenario-effectful modes: excluded** from first release until ARCH.PROBE-CONTRACT
- **Third-party / untrusted imperative rules: excluded** until restricted runtime exists
- C-1: fact sufficiency is predicate-relative; no global tier ordering

## Where the design lives

Primary tree: **`docs/coop/`**

| Path | Role |
|------|------|
| `docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md` | **Authoritative plan** to finish architecture and start implementation — read this first |
| `docs/coop/architecture/` | Narrative design (00–11) |
| `docs/coop/artifacts/*.json` | Binding contracts |
| `docs/coop/artifacts/check-*.py` | Retained checkers (`--selftest` = mutation suite) |
| `docs/coop/artifacts/claim-register.v1.json` | Claim status authority |
| `docs/coop/artifacts/*.adjudication-*.json` | Finding dispositions (agents A/B/C) |
| `docs/coop/agentlog4.md` | Recent adjudication log |
| `docs/coop/steering/` | Migration-only notes — **must not constrain greenfield** |

## Process status (as of handoff)

Completed:
- Multi-agent architecture exercise with binding contracts + 12 checkers
- Final-round reviews; Agent A adjudicated D9, EVIDENCE, FACT-IDENTITY, R-1
- Agent C adjudicated FACT-PLANE, C-2, RESOLVED-INPUTS, VERSIONING (+ D9 confidence-floor cross-surface)
- Agent B work on OPERABILITY/DELIVERY/TM/completeness instrument (see claim-register + completeness output)
- Plan captured: `ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md`
- Tree moved into this repo; checkers still run from `docs/coop/`

Approximate verification state (re-run; do not trust memory):
- Contract-shape completeness ~11/11
- Independently reviewed ~11/11
- Seal-ready ~7/11 (EVIDENCE / FACT-IDENTITY / R-1 / TM still residual or weaker)
- Product release qualification: NOT-RELEASE-QUALIFIED (demonstration gates are later)
- Cross-cutting opens may still include R2-FINAL-02 / R2-FINAL-03 — check live completeness

```bash
cd docs/coop
python3 artifacts/check-claims.py
python3 artifacts/check-completeness.py
# full suite when changing contracts:
for k in claims d9 fact-plane c2 evidence resolved-inputs fact-identity \
         versioning operability delivery threat-claims r1; do
  python3 artifacts/check-$k.py && python3 artifacts/check-$k.py --selftest
done

What we are NOT doing yet

• Implementing product code in this repo until architecture freeze (Phase 4 of the plan)
• Creating product ADRs in opensip-cli docs/decisions/ for this greenfield work
• Solving ARCH.PROBE-CONTRACT before the first vertical slice
• Porting opensip-cli package layout 1:1 into Rust crates

Recommended next steps (from the plan)

We are in finish-and-freeze, not redesign:

0. Phase 0 — Product confirms v1 slice in/out (draft is in the plan)
1. Phase 1A (highest) — Close retention / V10 / evaluation-proof custody (main remaining architecture fork)
2. Phase 1B — Seal residuals: EVIDENCE, FACT-IDENTITY, R-1 (pure core + one-shot), TM shape
3. Phase 1C — Clear cross-cutting open findings
4. Phase 1D — Keep PROBE, residency, support-window evidence, R-2 measurement parked/excluded
5. Phase 2 — Product dispositions (P-1/P-2 depth, layer-4 CI, pivot cost)
6. Phase 3 — Implementer package: freeze draft, crate map, contract→module map
7. Phase 4 — Formal architecture freeze
8. Phase 5 — Implement vertical slice in Rust: admit → PlanId → facts → pure core → seal Run → D9 exit

Working rules

• Prefer binding artifacts + checkers over prose when they conflict; update contracts when decisions change
• Checkers establish only what they inspect; do not promote green checkers to “sealed/best design”
• implementable:true ≠ DISCHARGED/DEMONSTRATED (paper seals are forbidden)
• Write architecture/process work under this repo’s docs/coop/ (or other paths the user designates)
• When unsure thorough vs minimal: choose thorough; user can dial back

First actions this session

1. Read docs/coop/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md
2. Run python3 docs/coop/artifacts/check-completeness.py (from repo root) or from docs/coop/
3. Confirm with the user whether to continue Phase 0 (slice acceptance) or Phase 1A (V10/retention)

Do not invent a new architecture process; continue from the plan and claim-register.