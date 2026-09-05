# Multi-Agent Collaboration Log

**Topic:** Greenfield programming-language choice for opensip-cli  
**Inputs:** `docs/internal/coop/{a,b,c}.md`  
**Agents:** Agent 1, Agent 2 (latest turn), Agent 3  
**Question scope:** *What language would we pick if rebuilding greenfield?* — not “should we rewrite the current repo tomorrow.”

---

## Current understanding of the problem

Pick the best **primary implementation language** for a greenfield opensip-cli: multi-tool static-intelligence CLI (fit/graph/sim/yagni/mcp), agent-loop consumer, multi-language analysis, evidence/gates/sessions, plugins with capability scoping, strategically important deep TypeScript checks.

Unbiased by sunk cost of the current TypeScript/Node monorepo, but **informed by** measured properties of *this product* (startup, check surface, TS coupling, isolation posture).

**Refined after three agents:** The question is well-posed, but the **highest-leverage greenfield decisions** are (1) check representation (declarative vs imperative), (2) extension unit (npm package vs WASM component vs subprocess), (3) warm vs cold process model — and only then (4) host language. The host-language answer remains **Rust**, by a **narrow** margin over Go.

---

## Key observations

### From the three briefs

| Brief | Primary pick | Architecture | Explicit non-rewrite stance |
|-------|--------------|--------------|-----------------------------|
| **a.md** | Rust core + JS sidecar | Hybrid; WASM plugins | Yes — rewrite likely a mistake; hybrid captures ~80% |
| **b.md** | **Go** host | Hybrid; process plugins; TS sidecar until TS7 API | Yes — no rewrite without targets + prototype |
| **c.md** | **Rust** primary | Hybrid; TS as guest | Implicit (clean-sheet rebuild framing) |

### Measurements (multi-agent, consistent)

| Finding | Source | Status |
|---------|--------|--------|
| Warm `opensip --version` ≈ 620–680 ms; bare Node ≈ 20 ms | A1, A3 M1 | **Confirmed** |
| Bootstrap is mostly ESM/package resolution + I/O, not app JS compute (~3–5% samples) | A3 M2 | **Accepted by A1** — reframes “Node is slow” → “resolution topology is expensive” |
| `NODE_COMPILE_CACHE` does not fix it | A3 M3 | Accepted |
| Bundling *shape* is right; working 8× claim **not proven** (crash, not a run) | A3 M4 | Accepted — do not cite 70–80 ms as product evidence |
| `--version` eagerly loads tsc + web-tree-sitter | A3 M5 | Accepted — composition-root defect, language-independent |
| `graph impact` ≈ pure fixed cost (~68% bootstrap at 750 files; flat 951→937 ms small→medium) | A3 M6 + public benchmarks | **Verified by A1** against `12-public-benchmarks.md` |
| Largest published tier = **750 files**; 10k–100k unmeasured | A3 M7 | Accepted — startup case **extrapolates** past last data point |
| Warm read path already exists (MCP `impact_files` etc.); producer path cold | A3 M8 | Accepted — architecture gap, not language gap |
| `checks-universal`: 0 TS-compiler coupling | a.md; A3 M9 | Confirmed |
| typescript-go stable API not ready (ADR-0162) | A1, A2 | Unchanged |
| MCP graph this session bound to **opensip-cloud** (wrong root), catalog missing | A3 | Acknowledged — reconnect only; no `refresh_graph` |

### Agent 1 (this turn) — corrections I accept from A2/A3

| ID | Correction | A1 disposition |
|----|------------|----------------|
| A2.1 | Rust is not unique for native startup / shared in-process graph data / process supervision | **Accept.** Native vs Node is the hard cut; Rust-vs-Go is incremental. |
| A2.2 | ADR-0054 already gives mechanical *fault* isolation; capability confinement incomplete | **Accept.** “Isolation is social” was too broad. |
| A2.3 | No Rust-vs-Go bakeoff exists | **Accept.** Performance edge is forecast, not proof. |
| A2.4 | TS sidecar breaks *literal* single-binary without packaging design | **Accept.** Claim becomes “native host + optional self-contained TS analyzer.” |
| A2.5 | Stable typescript-go favors packaging convenience for Go, not exclusive host language | **Accept.** Rust can supervise a Go analyzer over the same protocol. |
| A3.C1 | Startup tax is resolution model × open plugin host; WASM-component load avoids FS resolution walk | **Accept as stronger form of my startup argument.** |
| A3.C2 | WASM does not stop source exfil via finding messages; honest claim is capability-scoped I/O + finding-stream side channel | **Accept.** My earlier “trust→guarantee” wording overclaimed. Product risk if we ship that overclaim. |
| A3.C3 | Sum types are defect-rate/ergonomics, not determinism; schema + golden tests enforce envelope contracts | **Accept.** Demote from Rust-vs-Go load-bearing weight. Still a real Rust *preference*, not a determinism property. |
| A3.C4 | Rust-vs-Go has absorbed more debate than evidence warrants | **Mostly accept.** Host language still needs an answer (coordinator asked); confidence must stay **narrow / conditional**. |
| A3.C5 | TS host remains coherent if wedge is “best-in-class TS/JS guardrails” | **Accept as conditional alternative.** Not my default for the *full* multi-lang control-plane vision. |
| A3.P1 | Checks-as-code is the real lock-in; declarative-first makes host reversible | **Accept as co-primary design decision.** See refinements below — not a free pass that host language is irrelevant. |
| A3.P4 | Highest-ROI next actions are language-independent | **Full endorsement.** |

### Agent 1 refinement of P1 (checks as code vs data)

A3’s reframe is the most important new idea in the discussion. I strengthen it with bounds:

1. **Majority surface is declarative-eligible.** Universal text/regex/glob checks (zero tsc coupling) should not be *imperative TypeScript functions* in a greenfield design. That is accidental lock-in.
2. **Escape hatch is real product, not a footnote.** Differentiated value includes multi-step TS-AST / architecture / graph-aware analysis that Semgrep-class DSLs hit a ceiling on. Greenfield design: **declarative-first + versioned multi-language code escape hatch** (TS SDK first; others via same protocol).
3. **Therefore host language is reversible *for the majority of checks*, not for the whole product.** Graph kernel, matcher engine, session/baseline plane, and the imperative escape-hatch runtime still care about host choice — but the *moat* (curated rules) should not.
4. **This dissolves Open Q3 as stated.** Contributor velocity for most checks becomes “write a rule,” not “know Rust vs Go vs TS.” Host-language hiring still matters for the small kernel team.

### What I still hold (after demotions)

1. **Hybrid architecture** (native host + TS semantic guest + isolated extensions) — high confidence, three-agent + three-brief agreement.
2. **Do not rewrite the shipping product** on the strength of this greenfield answer — high confidence, unanimous.
3. **Rust over Go for the host**, narrow margin, reasons that *survive* demotion:
   - **Extension unit / WASM-component host story** (A3.C1) — file instantiate, not npm resolution walk; capability preopens; industry tooling (wasmtime).
   - **Analysis-kernel ceiling** (graph/index RSS and p95 at monorepo scale) — forecast, not bakeoff; still the right default for this *tool class* given Ruff/Biome/Oxc/ast-grep convergence.
   - **Small trusted core** remains realistic if P1 holds (declarative checks + process/WASM protocols + TS authoring SDK) — this addresses A2’s “wishful boundary” risk better than “port everything to Rust.”
4. **I withdraw** treating exhaustive enums as a *determinism* pillar, and **withdraw** treating WASM as full source-isolation.

---

## Areas of agreement

**Unanimous (A1 + A2 + A3 + briefs where noted):**

1. **Architecture:** Native systems host + TypeScript analysis guest (compiler-backed exact semantics) + out-of-process and/or WASM plugins.
2. **Not candidates as primary:** Python, JVM, Zig, pure C/C++, OCaml/Haskell.
3. **Greenfield ≠ rewrite authorization** without latency/memory/distribution targets and an evidence-parity vertical prototype.
4. **TypeScript remains required** in the design as guest/SDK — tree-sitter/oxc are not substitutes for exact `tsc` semantics today.
5. **Go is a close, legitimate second** — not a wrong answer; team composition or bakeoff falsifiers can flip it.
6. **Literal single-binary** must not be promised until TS analyzer packaging is designed.
7. **Sandbox claims must be precise:** capability-scoped ambient I/O (no network / no unexpected FS / no secret env) ≠ “source cannot leak via findings.”
8. **Highest near-term ROI is language-independent** (A3 P4): fix eager composition root; warm producer path; threat model; measure 10k+ files; prototype declarative checks.
9. **MCP graph evidence is currently unusable** for this session (wrong project root); reconnect before citing graph.

**New agreement after A1 turn 2:**

10. **Checks-as-data is a first-class greenfield commitment** (declarative-first + code escape hatch). Host language ranks below this for long-term reversibility.
11. **Startup argument is mechanism-correct (resolution topology) but scale-extrapolated** — strong for small/agent fixed-cost commands; unproven as monorepo analysis rationale above 750 files.
12. **Warm long-lived process** already solves the worst fixed-cost commands on the read path; extending it is higher ROI than a language change for agent loops.

---

## Open questions

| # | Question | Status |
|---|----------|--------|
| 1 | Latency dominance at **10k–100k** files | **Still open** — only data through 750 files |
| 2 | typescript-go stable API timeline | Gated by ADR-0162; option value only |
| 3 | Host engineers vs check authors | **Reframed by P1** — mostly dissolves under declarative-first |
| 4 | WASM vs process isolation | Dual-support; threat model (Q11) first |
| 5 | Team/org composition | **Unstated** — can override Rust→Go |
| 6 | TS analyzer delivery shape | Required packaging design |
| 7 | Scale bakeoff targets (RSS, p95, index build) | Required before locking Rust-over-Go on perf |
| 8 | Fraction of checks declarative-eligible | **Unmeasured; dominates reversibility story** |
| 9 | What blocks warm **producer** path? | Unanswered (cache invalidation vs session identity vs unbuilt) |
| 10 | Greenfield extension unit | Sets startup floor more than host language |
| 11 | Plugin threat model written down? | Missing — required before sandbox marketing |

---

## Risks and concerns

| Risk | Severity | Mitigation |
|------|----------|------------|
| Full rewrite consumes 12–18 mo; moat is checks/evidence not language | **High** | Greenfield pick ≠ roadmap; staged language-independent wins first |
| Overclaim WASM as full isolation | **High (product trust)** | Threat model; honest “finding-stream side channel” |
| Promise single binary while TS guest exists | **Medium** | Explicit dual install modes |
| Choose Go primarily for typescript-go vapor | **Medium** | ADR-0162 gate; protocol keeps guest swappable |
| Choose Rust and then port every check into Rust | **High (velocity death)** | P1 + small kernel + TS SDK |
| Debate host language while composition root loads tsc on `--version` | **Medium (opportunity cost)** | P4 action #1 |
| Extrapolate 620 ms argument past 750-file evidence | **Medium (decision quality)** | One 10k+ measurement |
| Declarative DSL hits Semgrep ceiling; all real checks fall into escape hatch | **Medium** | Prototype 20 checks; measure Q8 early |

---

## Proposed solutions

### Consensus recommendation (A1 + A2 + A3)

| Layer | Choice |
|-------|--------|
| **Host / core language** | **Rust** (narrow win over Go) |
| **Semantic guest** | **TypeScript** (compiler-backed `Program`/`TypeChecker` until a stable native API exists) |
| **Default check representation** | **Declarative rules where expressible**, executed by a native matcher; retain a code escape hatch and measure the eligible fraction (Q8) |
| **Check escape hatch** | Versioned process/WASM protocol; **TypeScript SDK first** |
| **Untrusted extensions** | OS-process fault isolation baseline; WASM where capability confinement is promised |
| **Distribution** | Native host artifact + optional self-contained TS analyzer — not “one magic binary” until designed |
| **Shipping product today** | **No rewrite.** Execute language-independent P4 sequence. |

### Conditional table (authoritative for “when not Rust”)

| Condition | Choose |
|-----------|--------|
| WASM components as extension unit; kernel ceiling matters; team can staff Rust | **Rust** (default) |
| Team substantially Go-native; velocity binding; extensions are subprocesses anyway | **Go** — no agent should fight this |
| Falsifiers: Go inside RSS/p95 budgets *and* materially faster to ship; or stable typescript-go eliminates guest with large packaging win | **Go** |
| Product wedge is explicitly “best-in-class TS/JS guardrails only,” multi-lang kernel secondary | **TypeScript host** remains defensible — fix composition root + warm producers first |
| Forced single language, no hybrid | **Rust**, accept weaker exact-TS depth initially (c.md) — all agents prefer hybrid instead |

### Ranked greenfield host languages

1. **Rust** — default  
2. **Go** — close second; often correct under team/falsifier conditions  
3. **TypeScript** — third for full multi-lang vision; coherent under TS-first wedge  

### Language-independent actions (do these regardless of host) — ordered ROI

1. Fix eager composition root so `--version` / help do not load tsc + tree-sitter (M5).  
2. Warm producer path for `fit --changed` / `graph` build (M8), mirroring warm MCP reads.  
3. Write plugin threat model (Q11) before any sandbox marketing.  
4. Measure fit/graph on a real **10k+** file repo (Q1/M7).  
5. Prototype declarative format on ~20 universal checks (Q8/P1).  
6. *Then* consider native host extraction or greenfield kernel — only with targets + evidence-parity vertical slice.

### Agent positions (final)

| Agent | Host pick | Margin | Distinctive contribution |
|-------|-----------|--------|---------------------------|
| **A1** | Rust | Narrow (revised down) | Initial hybrid framing; accepts A3 demotions; endorses P1 with escape-hatch bound |
| **A2** | Rust | Narrow | Weighting table; falsifiers; single-binary honesty; ADR-0054 layer split |
| **A3** | Rust | Narrow / conditional | Measurement suite; resolution-model reframe; P1 checks-as-data; P4 ROI ordering |

---

## Outstanding disagreements

| Topic | Status after A1 turn 2 |
|-------|------------------------|
| Rust vs Go as host | **Resolved as consensus Rust, narrow, conditional** — not resolved as “Rust is clearly superior” |
| Whether Rust-vs-Go is the crux | **Agreed with A3:** secondary to check representation + extension unit + warm path |
| Checks code vs data | **Agreed:** declarative-first + escape hatch is greenfield commitment; Q8 still unmeasured |
| Sandbox strength | **Agreed:** narrow honest claim |
| Sum types as determinism | **Agreed with A3:** demoted to ergonomics |
| Startup evidence regime | **Agreed:** strong mechanism, weak monorepo scale data |
| TS-first wedge keeps TS host defensible | **Agreed as conditional** — not the default for full vision |

**No material disagreement remains on the answer.** Remaining work is measurement and product decisions (team, threat model, packaging), not further host-language debate.

---

## Consensus position

### THE ANSWER (three-agent consensus)

> **If rebuilding opensip-cli greenfield: implement the host/core in Rust; keep TypeScript as a compiler-backed semantic guest and first-class check/plugin authoring surface; make portable checks declarative by default while retaining a versioned code escape hatch; isolate untrusted extensions via processes and/or capability-scoped WASM; do not rewrite the current Node product solely because of this pick.**

### Why this is the consensus (stripped to surviving reasons)

1. **Product class** is a multi-language analysis / evidence kernel (systems CLI), not a web app.  
2. **Extension model** should not inherit npm’s runtime resolution tax (C1) — WASM components / native host fix the *irreducible* Node coupling better than micro-optimizing ESM.  
3. **Exact TS analysis** is irreducible today without a TS guest (ADR-0162; all agents).  
4. **Go remains one good decision away** (team or bakeoff) — consensus is not “anti-Go.”  
5. **Moat preservation** demands portable checks where the prototype proves the model fits and **forbids** a purity rewrite of 152 imperative checks into Rust. Q8 remains measurement, not a foregone numerical majority.

### Confidence (Agent 1 final, aligned with group)

| Claim | Confidence |
|-------|------------|
| Hybrid architecture is correct | **High** |
| Greenfield host = Rust (narrow over Go) | **Medium** |
| Declarative-first checks is the higher-leverage design bet | **Medium–high** (Q8 unmeasured) |
| Full rewrite now is a strategic error | **High** |
| Language-independent P4 beats language change on near-term ROI | **High** |
| Startup dominates at 10k–100k files | **Low** (unmeasured) |
| WASM fully “scopes capability” including source confidentiality | **Rejected** |

### Completion criteria

| Criterion | Status |
|-----------|--------|
| Major tradeoffs explored | **Yes** |
| Significant risks identified | **Yes** |
| Alternatives considered | **Yes** (Rust / Go / TS; WASM / process; checks-as-data; warm daemon; bundling) |
| Remaining disagreements minor or well understood | **Yes** |
| Clear recommendation and rationale | **Yes** |

**Agent 1 declares completion criteria met** and joins Agents 2–3 on the consensus answer above. Further turns should only reopen if: (a) team-composition data arrives, (b) 10k+ file measurements invert the startup/kernel story, (c) Q8 shows almost no checks are declarative-eligible, or (d) stable typescript-go library API ships and packaging/latency gains are product-significant.

**Agent 2 ratifies the three-agent consensus.** The declarative-check wording above is a precision refinement, not a reopened disagreement: declarative-first is the design default, while “a majority is eligible” remains a hypothesis for the proposed 20-check prototype. No material disagreement remains, and the completion criteria are met.

---

## Turn log

### Agent 1 — 2026-07-28 (turn 1)

- Read a/b/c; measured startup; noted ADR-0162.  
- Pick: Rust host + TS sidecar. Left Rust-vs-Go open.

### Agent 2 — 2026-07-28

- Corrections: native benefits not Rust-unique; ADR-0054 fault vs capability; single-binary honesty.  
- Pick: Rust, narrow; listed Go falsifiers.

### Agent 3 — 2026-07-28

- Measurement suite M1–M9; MCP wrong-root flag; C1–C5; P1 checks-as-data; P4 ROI.  
- Pick: Rust, narrow/conditional; completion criteria met pending A1 response to P1.

### Agent 1 — 2026-07-28 (turn 2 — this turn)

- Accepted A2/A3 corrections (startup mechanism, isolation layers, sandbox honesty, sum-type demotion, single-binary, no bakeoff).  
- Refined P1 with escape-hatch bound; demoted own overclaims.  
- Verified public-benchmark numbers behind M6.  
- **Final pick unchanged in name, narrowed in confidence: Rust host + TS guest + declarative-first checks + isolated extensions; no rewrite.**  
- Declared three-agent consensus and completion criteria met.

### Agent 2 — 2026-07-28 (turn 2 — final ratification)

- Accepted Agent 3's measurement-based startup reframe, sandbox-claim correction, warm-path priority, and checks-as-data insight, together with Agent 1's bounded escape-hatch refinement.
- Tightened one unsupported phrase: declarative-by-default is consensus; a numerical majority of eligible checks is still Q8 and must be measured.
- **Ratified the final choice: Rust host/core + TypeScript semantic guest and SDK + portable declarative checks + versioned code escape hatch + process/WASM extension isolation; no rewrite authorization.**
- Declared completion criteria met with no material disagreement remaining.
