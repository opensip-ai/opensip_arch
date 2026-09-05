# Clean-sheet architecture derivation

**Isolation note.** This document was derived only from the requirements in the task prompt. No repository source, ADRs, existing architecture docs, language decisions, or prior designs were read. If any of that material was present in context, this derivation is contaminated and should be discarded.

**Purpose.** Every significant choice is forced, preferred, or guessed. The value is the *forcing chain*, not polish.

**Marking.**
- **FORCED** — a named requirement or workload compels this choice (or a small set of equivalents; the class is forced).
- **PREFERRED** — judgment call; alternatives remain live.
- **GUESSED** — insufficient information; stated as such.

---

## 0. Problem restatement (no decisions)

A CLI tells a team whether a codebase violates **declared rules**, and **proves** the answer. It must work **offline**, call **no language models**, serve **AI agents** (many small, rapid, overlapping queries after few-file edits), **CI** (full, one-shot, ephemeral, reproducible, correct fail), and **human reviewers** (occasional, need *why*). Results must be **checkable later**. Teams adopt with **existing violations** and must gate on **only what is new**, with that mechanism **trustworthy across tool upgrades**. Scale: hundreds to **100k+** files. Multi-language surface; **deep** analysis in **two** languages. Third-party analysis contribution is possible; depth open. Hosted product may consume results; **never required**. Non-goals: multi-tenant service, IDE-first, replacing VCS, inference inside the tool.

---

## 1. Core domain model

### D1. The product emits *claims with proof*, not bare pass/fail flags

| | |
|---|---|
| **Decision** | The primary domain object is a **Finding** (a claim that a rule is violated, or explicitly not, at a location under a given input identity), paired with **Evidence** sufficient for a third party to understand *why*. Aggregate **Result** = findings + completeness + input identity + tool/rule identity. |
| **Forcing** | **FORCED** by: (a) “prove the answer”; (b) “checkable later: why a claim was made”; (c) human reviewers need *why*. A boolean exit alone cannot satisfy (b)/(c). |
| **Rejected** | Exit-code-only product (fails checkability/human). LLM narrative “explanations” (forbidden; non-deterministic). Findings without evidence (fails prove/check). |
| **Falsified if** | Users accept “violation: true” with no path to reconstruct the reason from stored artifacts; or “proof” requires trusting a live service. |

### D2. Rules are first-class, versioned, declared inputs — not hard-coded product behaviour alone

| | |
|---|---|
| **Decision** | **Rule** is an explicit, durable object: identity, version (or content hash), severity/gate class, applicability, and evaluation definition. Analysis consumes a **rule set** with a closed, named identity. Built-in rules are still rules (same model), not a second opaque system. |
| **Forcing** | **FORCED** by “rules they have declared” and by checkability (“against what inputs”). Without rule identity/version, later reproduction cannot establish *which* constraint produced a claim. |
| **Rejected** | Implicit “linter defaults that change every release” without identity (breaks upgrade trust and baselining). Rules only as free-text for humans (not evaluable deterministically). |
| **Falsified if** | Two runs claiming the same tool version disagree because undeclared rule defaults changed; or baselines cannot pin rule set identity. |

### D3. Findings have stable **identity** separate from presentation

| | |
|---|---|
| **Decision** | Each finding has a **FindingKey** (stable identity for baselining/diffing) distinct from display location strings. Key is computed from a documented, versioned scheme over (rule id, primary subject identity, and only those locators the scheme declares stable). Location/message may change without changing key when the scheme says so. |
| **Forcing** | **FORCED** by “accept current state and gate only on what’s new” **and** “mechanism must stay trustworthy across tool upgrades.” Without stable identity, “new” is ill-defined under formatting, line drift, or message tweaks. |
| **Rejected** | Key = full message text (fragile). Key = line number only (fragile under edits). Key = whole-file hash (too coarse; one fix clears unrelated accepts). No key; re-baseline whole repo every upgrade (fails continuous trust). |
| **Falsified if** | Benign edits re-fire “new” violations that were accepted; or real new violations hide under an old key after upgrades. |

### D4. Input identity is content-addressed (and optionally revision-labelled)

| | |
|---|---|
| **Decision** | Every Result records **InputIdentity**: cryptographic hashes of the concrete bytes/trees analysed (files/units in scope), plus optional VCS revision labels as *annotations*, not substitutes for content hashes. |
| **Forcing** | **FORCED** by “against what inputs” and “reproduce it,” offline. Branch names or “HEAD” alone do not identify bytes. |
| **Rejected** | Timestamp-only provenance. “Whatever was on disk” without hashes. Network-fetched canonical source as required input (violates offline). |
| **Falsified if** | Two different trees produce identical stored input identity, or a past result cannot be matched to recoverable inputs. |

### D5. Completeness is part of the domain, not an afterthought log line

| | |
|---|---|
| **Decision** | Result includes a first-class **Completeness** object: what was in scope, what was fully determined, what was skipped/failed/unsupported, and **Undetermined** regions/rules with reasons. Policy may treat undetermined as gate-fail or warn, but the data model always records it. |
| **Forcing** | **FORCED** by “report what it could *not* determine,” CI “must fail the build correctly,” and multi-language reality (not everything deep). Silent success on partial analysis is a false negative. |
| **Rejected** | Best-effort empty findings = pass. Only stderr warnings (not machine-checkable). Collapsing undetermined into “no violation.” |
| **Falsified if** | A parse failure on a changed file yields exit 0 and empty findings with no undetermined record. |

### D6. No model of “truth from inference”; only deduction from declared analysis

| | |
|---|---|
| **Decision** | Domain forbids probabilistic or generative judgment. Analysis is a **deterministic function** of (InputIdentity contents, RuleSet identity, Tool identity, AnalysisConfig). |
| **Forcing** | **FORCED** by “Calls no language models, ever,” “Determinism is the product’s credibility,” offline, reproducible CI. |
| **Rejected** | Optional “AI explain” inside the tool. Heuristic ML classifiers as core gate. Non-deterministic parallel races that change findings set. |
| **Falsified if** | Same inputs/rules/tool/config produce different FindingKeys or completeness across runs. |

---

## 2. How analysis is executed and scheduled

### D7. Two execution modes from one engine: scoped (interactive) and full (CI)

| | |
|---|---|
| **Decision** | One analysis engine; two primary **invocation shapes**: **Full** (entire configured project) and **Scoped** (explicit paths / changed-set / dependency closure of those paths). Agents default toward scoped; CI defaults toward full. Same finding model and completeness rules in both. |
| **Forcing** | **FORCED** as a *class* by the dual workload: agents “edit a few files… did I break anything?” (many rapid queries) **and** CI “full analysis, one shot,” at scale up to 100k+ files. Requiring full reanalysis of 100k files for every agent turn is incompatible with the dominant interactive pattern unless analysis is unrealistically free. |
| **Rejected** | Agent-only daemon with no full mode (fails CI). CI-only full scans with no scope (fails agent latency at scale). Separate unrelated products for agent vs CI (split credibility of “the” result). |
| **Falsified if** | Scoped mode cannot soundly relate to full mode (e.g. scoped green systematically contradicts full red on same edits), or agents cannot get answers without full-repo cost linear in repo size every time. |

### D8. Soundness boundary of scoped analysis is explicit

| | |
|---|---|
| **Decision** | Scoped runs declare a **SoundnessClaim**: e.g. “findings only for rules/files in scope; cross-file rules either expanded to required closure or marked undetermined.” The tool does **not** claim global absence of violations from a narrow scope. |
| **Forcing** | **FORCED** by prove/checkability + agent partial queries. Partial query must not be misread as full certification. |
| **Rejected** | Silent “no violations” from path-limited runs without soundness disclaimer. Always expanding to whole program for every rule (may kill agent latency; not forced if completeness records undetermined). |
| **Falsified if** | Users treat scoped exit 0 as CI-equivalent full pass and the tool documentation/model encourages that. |

### D9. Analysis decomposes into deterministic **units of work** with pure outputs

| | |
|---|---|
| **Decision** | Pipeline stages: (1) discover inputs, (2) extract **Facts** per unit (AST/symbols/types/graph slices — language-specific), (3) evaluate rules against facts, (4) emit findings + completeness. Fact extraction and rule evaluation are pure given their inputs. Scheduling assigns units to workers. |
| **Forcing** | **PREFERRED** structure (pipeline), but **FORCED** properties: purity/determinism, parallelisable units for 100k+ CI. The exact stage names are not forced. |
| **Rejected** | Single-threaded monolithic walk as the only implementation (fails scale unless miraculously fast — not guaranteed). Shared mutable global analysis state that races. |
| **Falsified if** | Parallel full analysis is nondeterministic; or 100k-file CI cannot complete in reasonable CI budgets *and* no incremental fact reuse exists. (Exact time budgets not specified — scale requirement still pressures decomposition.) |

### D10. Scheduling: parallel full scans; interactive runs may cancel/supersede

| | |
|---|---|
| **Decision** | Full mode: data-parallel over units, deterministic merge (sorted by FindingKey or equivalent). Interactive: support **cancel** or **supersede** when a newer overlapping query arrives (overlapping agent queries). No fairness/multi-tenant scheduler. |
| **Forcing** | Parallelism **PREFERRED** for CI scale (not uniquely forced without latency SLOs). Cancel/supersede **PREFERRED** for “many… overlapping queries” (could queue strictly; wasteful but correct). Multi-tenant scheduling **rejected** by non-goal. |
| **Rejected** | Distributed cluster scheduler as required (offline laptop). Priority pricing queues. |
| **Falsified if** | Overlapping agent queries deadlock or corrupt the only result store; or parallel merge order changes findings set. |

### D11. Optional local fact cache; never required for correctness

| | |
|---|---|
| **Decision** | A **content-addressed fact cache** (keyed by file/unit hash + extractor version + config) may accelerate repeated agent queries. Correctness must hold with cache disabled (CI cold start). Cache is local, not a service. |
| **Forcing** | Cache itself **PREFERRED** (agents benefit). “Not required for correctness” **FORCED** by CI “no residency” + offline reproducibility. |
| **Rejected** | Mandatory long-lived daemon for any correct result. Remote cache service as dependency. |
| **Falsified if** | CI without cache disagrees with warm-cache agent results on same inputs/tool/rules. |

---

## 3. Result storage and checkability

### D12. Results are **portable artifacts**, not only live process state

| | |
|---|---|
| **Decision** | Primary output is a **Result Artifact** on the filesystem (and stdout summary): structured document(s) containing tool identity, rule set identity, input identity, completeness, findings (keys + evidence), and config hash. Hosted products **import** these; they are not the source of truth for offline use. |
| **Forcing** | **FORCED** by offline, checkable later, hosted “may consume… never required,” CI ephemeral (no residency). |
| **Rejected** | Results only in a cloud dashboard. Results only in a local daemon memory. Database server as requirement. |
| **Falsified if** | Checking a past claim requires the original process still running or a network account. |

### D13. Evidence is mechanical, not rhetorical

| | |
|---|---|
| **Decision** | Evidence includes: rule id/version, primary location, secondary related locations if any, **fact references** (which extracted facts fired the rule), and enough path/byte anchors to re-open the input. Optional rendered message for humans; message is not the sole evidence. |
| **Forcing** | **FORCED** by prove + human *why* + no LLMs. |
| **Rejected** | Free-text only. Screenshots. “Model said so.” |
| **Falsified if** | A reviewer cannot re-derive the claim from evidence + inputs + rules without guessing. |

### D14. Reproduce path: pin tool + rules + inputs + config

| | |
|---|---|
| **Decision** | Reproduction recipe embedded in artifact: tool version (and build identity if relevant), rule set content hash, config hash, input hashes, and command invocation shape. Same pins ⇒ same findings and completeness (byte-stable structured output in a defined canonicalisation). |
| **Forcing** | **FORCED** by reproduce + determinism + CI credibility. |
| **Rejected** | “Works on my machine” without pins. Floating “latest” tool in the artifact. |
| **Falsified if** | Following the recipe yields different FindingKeys or completeness. |

### D15. Artifact format: structured machine-readable primary; human views derived

| | |
|---|---|
| **Decision** | Canonical result is structured (e.g. JSON/JSONL or similar — exact codec **PREFERRED**). Human-oriented text/SARIF-like views are projections. Agents and CI parse the canonical form. |
| **Forcing** | Dual consumers (agents + CI + humans) **FORCE** machine-readable + human-readable *capability*; codec choice **PREFERRED**. SARIF specifically **PREFERRED**/optional compatibility, not forced by requirements. |
| **Rejected** | Human text as only output. Proprietary binary only with no dump tool. |
| **Falsified if** | Agents cannot reliably parse outcomes; or humans cannot get *why* without a separate product. |

---

## 4. “Only new violations” across tool upgrades

### D16. Baseline is an explicit set of accepted FindingKeys (plus pins)

| | |
|---|---|
| **Decision** | **Baseline** = accepted FindingKeys, each recorded with the rule id and the **key-scheme version** that produced it, and preferably the tool/rule-set pins at accept time. Gate mode: fail on findings whose keys are not in baseline (subject to severity filters). Adding to baseline is an explicit user action. |
| **Forcing** | **FORCED** by adopt-with-existing-violations + gate only on new. |
| **Rejected** | “Max N violations” thresholds (not trustworthy; allows churn). Silence all rules globally. Re-baseline automatically on every tool upgrade (hides new detections). |
| **Falsified if** | Teams cannot merge a brownfield repo without fixing all history, or “new” ignores real regressions. |

### D17. FindingKey scheme is versioned; upgrades must not silently remap

| | |
|---|---|
| **Decision** | Key scheme has a **scheme version**. Tool upgrades that change key computation bump scheme version and provide a **documented migration**: either (a) recompute keys for baseline entries from stored evidence/locations when possible, or (b) require explicit re-accept with audit, or (c) dual-key recognition window. Silent key mutation without migration is forbidden. |
| **Forcing** | **FORCED** by “trustworthy across tool upgrades.” |
| **Rejected** | Unversioned keys. Auto-accept all newly detected keys on upgrade. |
| **Falsified if** | After upgrade, previously accepted issues reappear as new without code change and without an explicit migration path; or real new issues are auto-swallowed. |

### D18. Baseline trust is local/VCS-mediated, not service-mediated

| | |
|---|---|
| **Decision** | Baseline lives as a **reviewable artifact** (file(s) in repo or signed artifact path teams choose). The tool verifies baseline integrity (hash/signature optional **PREFERRED**) but does not require a server to trust it. |
| **Forcing** | Offline **FORCES** no server. Co-location in VCS **PREFERRED** (fits “teams,” reviewability) but not forced — could be CI-secret file. |
| **Rejected** | Cloud-only baseline store as required path. |
| **Falsified if** | Gating on “only new” requires network to the vendor. |

### D19. Tool-upgrade-caused new detections are a distinct event class

| | |
|---|---|
| **Decision** | When rule pack or analyzer precision changes, newly emitted keys that match old code should be classifiable as **detection-delta** (same InputIdentity as last accept, different tool/rules pins) vs **code-delta**. Reporting distinguishes them so humans/CI policy can treat them differently (e.g. warn vs fail). Default CI policy is **PREFERRED**; distinction is **FORCED** for trustworthiness. |
| **Forcing** | Trust across upgrades **FORCES** the distinction. Exact default fail/warn **PREFERRED**. |
| **Rejected** | Treating all new keys identically with no way to see “tool got smarter.” |
| **Falsified if** | Operators cannot tell “we regressed” from “analyzer improved” after a bump. |

---

## 5. Reporting what could not be determined

### D20. Undetermined is a first-class outcome surface

| | |
|---|---|
| **Decision** | Emit **Undetermined** records: subject (file/unit/rule), reason category (parse error, unsupported language, missing dependency metadata, timeout, scope exclusion, extractor failure), and whether the gate treats it as failure. Map to exit status separately from “violations found.” |
| **Forcing** | **FORCED** by explicit requirement to report what could not be determined + CI correct fail. |
| **Rejected** | stderr-only. Folding into violations. Ignoring. |
| **Falsified if** | Incomplete runs look identical to complete clean runs in machine-readable output. |

### D21. Fail-closed default for undetermined in CI full mode

| | |
|---|---|
| **Decision** | Default **full CI** policy: undetermined on in-scope code ⇒ non-zero exit (fail closed). Interactive scoped mode may default softer but must still surface undetermined. Overrides allowed and recorded in Result. |
| **Forcing** | **PREFERRED** default (fail closed matches “fail the build correctly” spirit); not uniquely forced — some orgs prefer warn. Recording overrides **FORCED** by checkability. |
| **Rejected** | Always zero exit if no violations, ignoring incompleteness. |
| **Falsified if** | Broken parser ⇒ green CI by default with no trace in the artifact. |

---

## 6. Process and deployment shape

### D22. Primary deliverable is a local CLI process

| | |
|---|---|
| **Decision** | Ship a **command-line tool** users run on laptops and CI images. All analysis completes in that trust boundary with local inputs. |
| **Forcing** | **FORCED** by “command-line tool,” offline laptop, CI one-shot. |
| **Rejected** | Mandatory always-on cloud analyzer. IDE-first as sole surface (non-goal). |
| **Falsified if** | Core analysis requires a vendor service call. |

### D23. Ephemeral processes are sufficient; long-lived helper optional

| | |
|---|---|
| **Decision** | Correct operation: invoke CLI, analyse, write artifacts, exit. Optional **local** helper (daemon/server on localhost) for cache warmth and query latency is an optimisation, disabled/absent in CI. |
| **Forcing** | Ephemeral sufficiency **FORCED** by CI no residency. Optional helper **PREFERRED** for agent dominance. |
| **Rejected** | Architecture that cannot function without a resident process. Multi-tenant hosted analyzer as core. |
| **Falsified if** | Documented CI path needs a standing daemon. |

### D24. Hosted product is a pure consumer of Result Artifacts

| | |
|---|---|
| **Decision** | Any hosted offering ingests exported results (and maybe baselines) for UI/history; it must not be on the critical path of gate decisions unless the team chooses to mirror. |
| **Forcing** | **FORCED** by “may consume… never required.” |
| **Rejected** | License checks that phone home for each analysis. Upload-required gating. |
| **Falsified if** | Offline mode cannot produce a trustworthy gate decision. |

### D25. Distribution: single (or few) native binaries preferred over language-runtime sprawl

| | |
|---|---|
| **Decision** | Prefer shipping a **self-contained binary** (or small set per OS/arch) so CI images and agents get one install unit. Language-specific runtimes for *analyzed* code are the user’s project, not the tool’s host requirement — except where deep analyzers embed/bundle their own engine. |
| **Forcing** | **PREFERRED** packaging. Offline CI reproducibility pressures “pin one tool artifact,” but multiple packages could work. |
| **Rejected** | “pip install three compilers and hope” as the only ship form without pinning. |
| **Falsified if** | Install drift routinely changes analysis outcomes without tool version change. |

---

## 7. Extension model and authority limits

### D26. Extension depth is layered; authority shrinks with distance from core

| | |
|---|---|
| **Decision** | Layers (outer → inner power): (1) **Config** (enable/severity/paths); (2) **Declarative rules** over exposed fact schemas; (3) **Fact extractors / analyzers** for languages; (4) **Core runtime** (scheduling, baselining, artifacts, exit status). Third parties primarily target (2), optionally (3). Core (4) stays product-controlled for determinism and gate integrity. |
| **Forcing** | That *some* contribution path exists is **PREFERRED** (requirement says third parties *may* want to; “how much is open”). Layering with core authority limits is **PREFERRED** engineering judgment for trust. Requirements **FORCE** that extensions cannot introduce LLM calls or nondeterminism into the certified path if results claim determinism. |
| **Rejected** | Arbitrary in-process scripts with full authority and no purity contract (threatens determinism/baseline). Fully closed system with zero extension (allowed by requirements but forgoes “may want to contribute”). Browser-plugin-style unrestricted API. |
| **Falsified if** | Third-party rules can change FindingKey semantics globally without scheme version; or extensions network out during “offline” analysis. |

### D27. Extensions on the gating path must be deterministic and offline

| | |
|---|---|
| **Decision** | Any extension whose output can affect findings/baseline/exit must declare pure inputs, produce deterministic outputs, and perform no required network I/O during analysis. Violations of the contract exclude the extension from “certified” mode or mark completeness undetermined. |
| **Forcing** | **FORCED** by offline + no LLMs + determinism + checkability. |
| **Rejected** | “Extensions may call APIs for context.” |
| **Falsified if** | Enabling a plugin makes CI unreproducible. |

### D28. Trust model for third-party analyzers: explicit enablement

| | |
|---|---|
| **Decision** | Third-party extractors/rules are **opt-in**, named in config (pinned by content hash), visible in Result artifact. No implicit community marketplace execution. |
| **Forcing** | **PREFERRED** (security judgment). Provenance in artifact **FORCED** by checkability (“against what inputs” includes which analyzers ran). |
| **Rejected** | Auto-download plugins on first run (offline break; supply chain). |
| **Falsified if** | A result cannot list which extension code participated. |

---

## 8. Failures and exit status

### D29. Exit status encodes orthogonal outcome classes

| | |
|---|---|
| **Decision** | Distinguish at least: **clean complete** (0); **violations (gate fail)** (non-zero, stable code); **undetermined/incomplete** (non-zero, different code); **tool error** (invocation/config/crash — non-zero, different code). Stdout/artifact always carry the detailed Result when possible. |
| **Forcing** | **FORCED** class separation by CI “fail the build correctly” + undetermined reporting + agent parsing. Exact numeric mapping **PREFERRED**. |
| **Rejected** | Single non-zero for all failure modes. Exit 0 on tool crash. |
| **Falsified if** | CI cannot fail on violations while alerting differently on infra errors, or agents mis-handle crashes as clean. |

### D30. Policy layer maps findings → gate without rewriting evidence

| | |
|---|---|
| **Decision** | **Policy** (severity thresholds, baseline subtraction, undetermined handling) consumes immutable findings and produces **GateDecision**. Policy parameters are hashed into Result. |
| **Forcing** | **FORCED** split between observation and gate by baselining (“accept current”) and checkability (same findings, different policy still explainable). |
| **Rejected** | Dropping evidence for baselined findings entirely (humans lose *why* for accepted debt). |
| **Falsified if** | Accepted findings disappear so thoroughly they cannot be audited. |

---

## 9. Language strategy

### D31. Many languages at shallow-to-medium depth; two at deep depth

| | |
|---|---|
| **Decision** | Architecture supports a **language tiering** model: *deep* (rich facts: names, types/flow/graph as applicable), *standard* (syntax/structure/imports), *surface* (text/regex/path rules only). Product commits to **two deep** languages; others ride lower tiers without pretending equality. |
| **Forcing** | **FORCED** by “many programming languages” + “genuinely deep analysis in two.” |
| **Rejected** | Equal deep investment in all languages (unbounded). Only two languages total (fails “many”). |
| **Falsified if** | Marketing claims deep support where Completeness always marks undetermined for semantic rules. |

### D32. Choice of the two deep languages

| | |
|---|---|
| **Decision** | **Deep language A: TypeScript** (including the JS surface that shares tooling). **Deep language B: Python**. Rationale: dominant targets for AI coding agents and common CI estates; both have mature parse/type ecosystems usable deterministically offline. |
| **Forcing** | **GUESSED / PREFERRED.** Requirements force *count* (two) and quality (“genuinely deep”), **not which**. No customer stack data in the prompt. Alternatives live: Java/Kotlin, Go, C#, Rust, C/C++ — any pair could be correct for a different market. |
| **Rejected as forced choices** | Picking a pair because it is “elegant.” Claiming the pair is required by the prompt. |
| **Falsified if** | Target users’ critical path languages are neither TS nor Python, and agent workload is mostly elsewhere — then swap deep investment. |

### D33. Implementation language of the tool itself

| | |
|---|---|
| **Decision** | Implement the CLI runtime in a language that ships static binaries and supports reliable parallelism (candidates: Rust, Go). Language-specific deep engines may be embedded libraries, subprocesses with pinned versions, or in-process bindings — chosen per deep language for determinism and offline packaging. |
| **Forcing** | **PREFERRED.** Requirements force offline CLI and determinism, not host language. Subprocess vs in-process for engines **PREFERRED** with constraint that pins appear in Result. |
| **Rejected** | Host language choice presented as FORCED. Unpinned subprocess tools on PATH as sole deep engine (breaks reproducibility). |
| **Falsified if** | Host language prevents offline single-artifact distribution or forces nondeterministic runtimes for core gating. |

---

## 10. Cross-cutting: concurrency, scale, multi-language facts

### D34. Shared fact schema only where it earns its keep

| | |
|---|---|
| **Decision** | Define a **small common fact vocabulary** (files, ranges, symbols, references, diagnostics) plus **language-specific fact extensions**. Rules may be common or language-specific. Avoid a grand unified IR that pretends all languages are equal. |
| **Forcing** | **PREFERRED.** Multi-language + two deep suggests some sharing, but requirements do not force a universal IR. |
| **Rejected** | One mega-IR mandatory for every rule (high cost, often shallow). Zero commonality (duplicates baselining/evidence machinery per language). |
| **Falsified if** | Common IR erases deep language fidelity, or total split duplicates FindingKey/evidence bugs per language. |

### D35. Scale strategy: stream, shard, cache facts; don’t require whole-program RAM

| | |
|---|---|
| **Decision** | Full analysis must not assume the entire 100k-file fact graph fits in luxury RAM as one ball of mud. Stream unit results; shard by package/path; merge deterministically. Whole-program graphs allowed **per deep language** when needed but bounded/optional per rule. |
| **Forcing** | **PREFERRED** tactics; **FORCED** that 100k+ is in scope so unbounded single-node memory designs are risky. No hard memory SLO given — mark tactical details PREFERRED. |
| **Rejected** | “Load all ASTs into one giant structure” as the only design. Distributed mapreduce cluster as required (offline laptop). |
| **Falsified if** | Fixed architecture OOM on large monorepos with no sharding path. |

---

## 11. What the requirements do *not* force (explicit non-decisions)

These are left open on purpose so the derivation does not invent pressure:

| Topic | Status |
|---|---|
| Exact CLI UX grammar | Not forced |
| SARIF vs custom JSON | Preferred codec only |
| Whether baseline file is committed to git | Preferred yes |
| Default severities taxonomy | Preferred |
| Whether agents talk via stdin RPC or subprocess CLI | Preferred (CLI subprocess sufficient; RPC optional helper) |
| Monetization / hosted features | Out of scope except consumer boundary |
| Precise performance SLOs | Not given |
| Which two deep languages | Guessed/preferred above |
| How rich the declarative rule language is | Open per extension depth |
| GUI / IDE | Non-goal |
| Multi-tenant SaaS core | Non-goal |

---

## 12. Minimal architecture picture (consequence of forcing, not aesthetics)

```
                    ┌─────────────────────────────┐
                    │  CLI invocation (ephemeral) │
                    │  full | scoped + policy     │
                    └─────────────┬───────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
   InputIdentity            RuleSet pin              Tool pin
   (content hashes)         (content hash)           (version)
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  ▼
                    ┌─────────────────────────────┐
                    │ Deterministic engine        │
                    │ discover → facts → rules    │
                    │ optional local fact cache   │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    ▼                            ▼
              Findings+Evidence            Completeness
                    │                            │
                    └─────────────┬──────────────┘
                                  ▼
                    ┌─────────────────────────────┐
                    │ Policy: baseline subtract,  │
                    │ severity, undetermined map  │
                    └─────────────┬───────────────┘
                                  ▼
                    Result Artifact + exit class
                         │
                         ▼ (optional, never required)
                    Hosted consumer import
```

Nothing in this picture requires a network hop for analysis.

---

## 13. Decision index (summary)

| ID | Title | Mark |
|----|--------|------|
| D1 | Claims with proof | FORCED |
| D2 | Versioned declared rules | FORCED |
| D3 | Stable FindingKey | FORCED |
| D4 | Content-addressed inputs | FORCED |
| D5 | Completeness first-class | FORCED |
| D6 | Deterministic non-ML domain | FORCED |
| D7 | Full + scoped modes | FORCED (class) |
| D8 | Explicit scoped soundness | FORCED |
| D9 | Pure units pipeline | PREFERRED structure / FORCED purity |
| D10 | Parallel + optional supersede | PREFERRED |
| D11 | Optional fact cache | PREFERRED; correctness without it FORCED |
| D12 | Portable result artifacts | FORCED |
| D13 | Mechanical evidence | FORCED |
| D14 | Reproduction pins | FORCED |
| D15 | Structured canonical output | FORCED capability; codec PREFERRED |
| D16 | Baseline of FindingKeys | FORCED |
| D17 | Versioned key scheme + migration | FORCED |
| D18 | Offline baseline artifact | FORCED offline; VCS co-location PREFERRED |
| D19 | Detection-delta vs code-delta | FORCED distinction; policy PREFERRED |
| D20 | Undetermined records | FORCED |
| D21 | CI fail-closed undetermined | PREFERRED default |
| D22 | Local CLI primary | FORCED |
| D23 | Ephemeral sufficient | FORCED; daemon optional PREFERRED |
| D24 | Hosted as consumer only | FORCED |
| D25 | Self-contained distribution | PREFERRED |
| D26 | Layered extensions | PREFERRED depth; purity FORCED |
| D27 | Extension determinism/offline | FORCED |
| D28 | Opt-in pinned extensions | PREFERRED enable; provenance FORCED |
| D29 | Orthogonal exit classes | FORCED classes; codes PREFERRED |
| D30 | Policy separate from evidence | FORCED |
| D31 | Language tiering; two deep | FORCED |
| D32 | Deep = TS + Python | GUESSED/PREFERRED |
| D33 | Host implementation language | PREFERRED |
| D34 | Small common facts + extensions | PREFERRED |
| D35 | Stream/shard at scale | PREFERRED tactics; scale pressure FORCED |

---

## 14. Falsification summary (architecture-level)

This derivation is wrong if any of the following hold:

1. Credible “prove / check later” without durable evidence and input pins.
2. Agent-dominant use works at 100k+ files only with full-repo semantics every query *and* that is still fast enough that scoping is unnecessary (would demote D7 from FORCED to PREFERRED).
3. Baselining can be trustworthy across upgrades without stable versioned finding identity.
4. Offline/determinism can be maintained while calling external inference or unpinned network tools on the gate path.
5. CI can “fail correctly” without distinguishing violations, incompleteness, and tool errors.
6. Market data shows the two deep languages must be a different pair (invalidates only D32, not the tiering model).

---

*End of clean-sheet derivation. No comparison to other designs was attempted.*
