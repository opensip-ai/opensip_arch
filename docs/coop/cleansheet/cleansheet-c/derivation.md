# Clean-sheet architecture derivation

## Boundary and force test

This derivation uses only the requirements in the commissioning prompt. No repository source, prior architecture material, ADR, public documentation, implementation description, or sibling directory was inspected.

The labels mean:

- **FORCED**: at least one stated requirement or workload rules out architectures that do not preserve the decision's invariant. The particular implementation can still vary.
- **PREFERRED**: the requirements create pressure, but at least one materially different design could satisfy them.
- **GUESSED**: the prompt does not contain enough product, team, or threat-model information to choose responsibly; the decision is a testable placeholder.

Requirement shorthand used below:

- **R-offline** — all results are available offline on a laptop; no service is required.
- **R-deterministic** — the tool never calls a language model; determinism is part of its credibility; inference is a non-goal.
- **R-languages** — many languages are supported, with genuinely deep analysis in two.
- **R-checkable** — a later reviewer can establish why a claim was made, against which inputs, and reproduce it.
- **R-adoption** — existing violations can be accepted and only new ones gated, trustworthily across upgrades.
- **R-extension** — third parties may want to contribute analysis logic; the degree of support is open.
- **R-hosted-optional** — a hosted product may consume results but is never needed to produce them.
- **R-scale** — repositories range from hundreds to more than 100,000 files.
- **W-agent** — many small, rapid, overlapping “did I break anything?” queries dominate interactive use.
- **W-CI** — CI performs a reproducible, one-shot, non-resident full analysis and must fail the build correctly.
- **W-human** — a reviewer occasionally needs to understand why a finding exists.

The derivation distinguishes three promises that are easy to conflate:

1. **Integrity**: these bytes and records have not changed.
2. **Replayability**: the same declared inputs and implementation produce the same canonical assessment.
3. **Soundness**: the analyzer's reasoning correctly represents the program.

The requirements force the first two. They require evidence for the third, but do not make formal verification of every analyzer feasible. The result format must not market a replay transcript as a mathematical proof.

## I. What an answer is

### D01 — The product answer is an assessment, not a Boolean — **FORCED**

1. **Decision.** A run yields a canonical `Assessment` binding a source snapshot, policy snapshot, analyzer cohort, execution constraints, findings, coverage, uncertainties, and a derived gate verdict. “Clean” is only one projection of that object.
2. **What forces it.** R-checkable needs provenance and reasons; W-CI needs a reliable gate; W-human needs explanation; partial language support means a bare `true` cannot distinguish “no violation” from “not analyzed.”
3. **Rejected.** A Boolean plus console messages loses the inputs and omitted work. An unstructured log is not a stable machine contract and cannot be compared or replayed reliably.
4. **Falsified by.** A demonstration that a Boolean/log pair can preserve exact inputs, structured uncertainty, stable machine consumption, later explanation, and upgrade comparison without recreating an assessment model elsewhere.

The canonical high-level relation is:

```text
Assessment = evaluate(Snapshot, Policy, AnalyzerCohort, DeclaredLimits)
Verdict    = gate(Assessment.findings, Assessment.coverage, Policy)
```

Cache state, worker count, scheduling order, wall-clock time, and daemon presence are deliberately absent from the semantic inputs.

### D02 — Analysis consumes an immutable logical snapshot — **FORCED**

1. **Decision.** Before analysis, the core captures an ordered manifest of repository-relative resources. Every resource records exact byte digest and semantic metadata (kind, symlink treatment, executable bit where relevant, and path rules). Configuration files, dependency metadata, generated-source declarations, and an allowlisted set of environment inputs are resources too. Analysis reads only this virtual snapshot.
2. **What forces it.** W-agent permits edits during overlapping queries; R-checkable requires the exact inputs; W-CI requires reproducibility. Reading the live tree throughout a run could combine states that cannot later be named or replayed.
3. **Rejected.** Repeated direct filesystem reads permit mid-run drift. “The current Git commit” omits working-tree changes, ignored-but-relevant files, configuration, and shallow/absent history. Timestamps are neither content identity nor stable across copies.
4. **Falsified by.** A filesystem or version-control interface that provides a complete, immutable, reproducible view of all relevant tracked and untracked inputs for the entire run, making the logical capture redundant.

Snapshot capture hashes bytes as it reads them and detects files changing during capture. It retries a bounded number of times, then records those resources as unstable; it does not silently analyze whichever read happened last. Paths use a canonical repository-relative representation while preserving original bytes/display spelling. Case or Unicode-normalization collisions are errors because allowing host-specific winner selection would break replay.

### D03 — The semantic execution boundary is hermetic and deterministic — **FORCED**

1. **Decision.** An analyzer can observe only snapshot resources, canonical policy, pinned analyzer data, and declared limits. It has no network, clock, ambient random source, undeclared environment, host filesystem, subprocess, or mutable global input. Enumeration and reduction orders are specified. A result may vary only when a declared semantic input varies.
2. **What forces it.** R-offline and R-hosted-optional prohibit service dependence. R-deterministic prohibits model calls and nondeterministic inference. R-checkable and W-CI require repeatability.
3. **Rejected.** “Best effort offline” still lets DNS, registries, telemetry, or license servers affect results. Merely documenting that plugins should be deterministic cannot enforce the product promise. Seeding random behavior makes it repeatable but still leaves an unnecessary semantic input and does not fix clock, concurrency, or network dependence.
4. **Falsified by.** A stated requirement for a result that inherently depends on live external state, or evidence that the supported platforms cannot enforce the boundary and an equally credible deterministic substitute is unavailable.

Dependency/package installation is outside a check run. A run never downloads a parser, rule pack, type stub, vulnerability database, or compiler. If a declared dependency is absent from the snapshot or pinned installation, the corresponding analysis is incomplete.

### D04 — Rules and analyzer semantics are versioned inputs — **FORCED**

1. **Decision.** A `PolicySnapshot` is the canonical expansion of declared rules. Each `RuleInstance` has a stable namespace/name, semantic revision, normalized parameters, applicability, required capabilities, severity/gating action, and rollout mode. An `AnalyzerCohort` identifies the core build, every fact producer/rule implementation digest, fact-schema revisions, and bundled language frontend versions.
2. **What forces it.** Teams declare the rules, R-checkable asks “against what inputs,” and R-adoption requires upgrade behavior to be auditable. A rule name alone does not identify semantics when code or defaults change.
3. **Rejected.** Hashing only the user-written config hides expanded defaults and transitive rule packages. A single marketing version for the whole tool cannot identify independently changing analyzer semantics. Treating severity as analyzer output gives extensions authority over team policy.
4. **Falsified by.** A permanently monolithic distribution in which every semantic component and default is provably identified by one immutable build digest and policies have no transitive expansion.

### D05 — Facts, claims, evidence, coverage, and verdict are separate domain objects — **PREFERRED**

1. **Decision.** The core model has: `Fact` (typed analyzer observation), `Subject` (file/span/symbol/module/project identity), `Claim` (a rule's assertion about a subject), `EvidenceNode/Edge` (the derivation witness), `CoverageCell` (whether required work was completed), `Finding` (a violated claim selected for presentation), and `Verdict` (core policy projection). Producers emit facts and candidate claims; only the core creates the final assessment and verdict.
2. **What forces it.** No single requirement forces this exact decomposition. It is preferred because W-human needs explanations, R-extension needs authority separation, R-languages needs heterogeneous facts, and W-CI needs verdict semantics that do not depend on presentation.
3. **Rejected.** A universal AST loses language-specific type and control-flow meaning. Letting every analyzer emit final diagnostics directly makes evidence, identity, baseline comparison, and exit policy inconsistent. A single undifferentiated event log can represent the information but makes invariants harder to validate.
4. **Falsified by.** A simpler model that supports deep language-specific reasoning, trustworthy extensions, structured explanation, coverage accounting, and stable upgrade comparison with less translation or duplicated state.

Facts use a small common kernel (resource, span, symbol, dependency, relation) plus versioned language-specific namespaces. The architecture does not pretend that every language shares one semantic tree.

### D06 — Unknown is first-class and is never encoded as pass — **FORCED**

1. **Decision.** Each planned rule/subject cell ends as `satisfied`, `violated`, `not_applicable`, or `indeterminate`. Indeterminate has a reason code such as unsupported construct, missing dependency, unstable input, analyzer failure, budget exhaustion, invalid evidence, or conservative impact closure failure. Coverage aggregates cells without erasing their reasons.
2. **What forces it.** R-languages promises deep analysis in only two languages; therefore some requested facts will be unavailable. The prompt explicitly requires reporting what could not be determined. W-CI cannot “fail correctly” if an analyzer crash or unsupported construct becomes a clean result.
3. **Rejected.** Dropping failed targets creates false passes. Turning every unknown into a violation misstates what was proved and makes human explanation dishonest. Logging warnings without machine status lets CI ignore them accidentally.
4. **Falsified by.** Complete, terminating, sound analyzers for every supported language and rule, with no missing dependencies, resource limits, invalid source, or operational failures.

An assessment may therefore be `FAIL` with incomplete coverage: one proved violation is sufficient to fail, while other questions remain unknown. The report retains both facts.

### D07 — Capability claims define the analyzable universe — **FORCED**

1. **Decision.** Language frontends and analyzers publish versioned capabilities such as parse, bind, type, call graph, control flow, data flow, dependency resolution, and cross-language linkage. A rule declares what it requires. Planning materializes the target universe and either schedules a compatible producer or records why it cannot.
2. **What forces it.** R-languages explicitly combines breadth with deep support in only two languages. R-checkable requires an honest account of which statements the tool was capable of establishing.
3. **Rejected.** A binary “language supported” flag exaggerates shallow syntax support. Running a rule with missing semantic inputs risks plausible-looking but unsound findings. Silently excluding unsupported files corrupts the denominator for “clean.”
4. **Falsified by.** One uniform analysis representation that provides identical, sound semantics for all supported languages without capability variation.

### D08 — A finding carries a machine-checkable evidence witness — **FORCED**

1. **Decision.** Every finding points to a finite evidence graph containing source anchors, relevant fact values, producer provenance, rule predicates, and derivation edges. Source anchors include resource digest plus span and a surrounding structural/content anchor. `explain` renders this graph as deterministic text or HTML; prose is a view, not the authority.
2. **What forces it.** The tool's job is to “prove the answer”; R-checkable and W-human require a later reviewer to understand why a claim was made.
3. **Rejected.** A message and line number are fragile under movement and reveal no derivation. Saving debug logs exposes implementation noise but does not define which steps justify a claim. Storing only a full rerun command cannot explain a historical result if the implementation or input is missing.
4. **Falsified by.** Users establish sufficient trust from analyzer identity and source location alone, or a practical formal proof-certificate system supersedes evidence graphs for all supported analyses.

`verify` has explicit levels: integrity verification, evidence replay against stored facts/source, and full analyzer rerun. It reports which level succeeded. None is described as a proof that an analyzer algorithm is mathematically sound unless that analyzer actually supplies a separately verified proof certificate.

### D09 — Semantic reproducibility has a canonical root identity — **FORCED**

1. **Decision.** Canonical serialization and domain-separated hashes identify snapshot, policy, analyzer cohort, declared limits, assessment payload, and baseline delta. The reproducibility contract is: equal semantic input roots under the same schema yield an equal canonical assessment root and the same exit class.
2. **What forces it.** R-deterministic, R-checkable, and W-CI require a checkable notion of “same run.” Without canonical identity, later comparison relies on mutable filenames or human interpretation.
3. **Rejected.** Byte-comparing ordinary JSON is sensitive to key order and incidental metadata. Run UUIDs identify executions but not equivalence. Timestamps and hostnames harm reproducibility and disclose irrelevant information.
4. **Falsified by.** A different stable equivalence protocol that supports offline verification and collision-resistant input/result binding without a canonical root.

Wall-clock timestamps and host labels may live in a non-semantic envelope; they are excluded from the assessment root. Any platform property that changes analysis, such as path case rules or target architecture, is instead a declared semantic input.

## II. Making the answer durable

### D10 — Immutable result artifacts are separate from disposable acceleration state — **FORCED**

1. **Decision.** A completed assessment is immutable. A mutable cache may accelerate recomputation, but deleting or corrupting it cannot alter a retained result. Baseline anchors and exported replay bundles pin their reachable objects independently of cache retention.
2. **What forces it.** R-checkable requires later inspection; W-agent and R-scale motivate aggressive cache replacement; R-adoption requires accepted state to survive tool changes and garbage collection.
3. **Rejected.** Treating the latest cache database as the record makes eviction and schema upgrades rewrite history. Storing reports only in a hosted service violates R-offline and R-hosted-optional. Plain console output omits structured closure.
4. **Falsified by.** Acceleration state can be made permanently immutable, portable, schema-stable, and cheap enough that a separate artifact concept adds no value.

### D11 — Use a content-addressed object store and closeable replay bundles — **PREFERRED**

1. **Decision.** Locally, manifests, source blobs, facts, evidence, and reports live as content-addressed objects using domain-separated SHA-256 identifiers. A thin report can reference the local object store; a sealed deterministic archive materializes its complete transitive closure, including exact source/config bytes and the installable analyzer cohort or verified distribution digests. Only a sealed closure may claim independent later replayability.
2. **What forces it.** No requirement mandates CAS or SHA-256. This is preferred because R-scale benefits from deduplication, while R-checkable and R-adoption need immutable reachability and portable closure.
3. **Rejected.** A monolithic database complicates partial export and corruption isolation. Embedding every repository byte in every report scales poorly. Hashes without retained objects establish identity but cannot guarantee replay. BLAKE3 may be faster, but SHA-256 has broader independent verifier availability; the schema remains algorithm-agile.
4. **Falsified by.** Measurements show hashing/object overhead dominates at target scale, SHA-256 is too slow, or a transactional pack format provides equally portable immutable closure with lower complexity.

A verifier distinguishes `valid`, `corrupt`, and `incomplete closure`. It never treats “the digest is named but the bytes are gone” as replayable. Human-readable reports and hosted uploads are projections from the canonical artifact.

## III. Accepting the old state without lying about upgrades

### D12 — Acceptance records an immutable comparison anchor, not mutable suppressions — **PREFERRED**

1. **Decision.** `accept` captures an immutable source snapshot root, policy context, analyzer/result root used during review, accepted scope, and optional reviewer/note. It does not annotate current findings as forever ignored. Updating acceptance creates a new anchor and a reviewable delta; it never mutates the old anchor in place.
2. **What forces it.** R-adoption forces a durable notion of accepted state, but does not force source-snapshot anchoring specifically. Snapshot anchoring is preferred because it preserves what code was accepted and can be reevaluated under new semantics.
3. **Rejected.** A list of analyzer-generated fingerprints goes stale when fingerprints or rules change. Source-line suppressions move policy into code, are hard to audit in bulk, and can mask future instances. Automatically replacing the baseline after every run destroys the gate.
4. **Falsified by.** A stable finding-identity scheme survives semantic analyzer and rule upgrades with less storage and no silent suppression, or retaining accepted source snapshots is operationally unacceptable.

An anchor is policy-scoped: teams can choose “gate only new occurrences under this rule,” “enforce this newly added rule everywhere,” or “do not require this capability.” Those are policy choices, not analyzer guesses.

### D13 — Across an upgrade, analyze anchor and current snapshots with the same current semantics — **PREFERRED**

1. **Decision.** For a net-new gate under analyzer cohort `E2`, evaluate both accepted snapshot `A` and current snapshot `C` with `E2` and the current rule instance, then compare those two assessments. Preserve the historical `E1(A)` result for audit, but do not compare `E1(A)` fingerprints directly with `E2(C)`. Cache `E2(A)` so the upgrade cost is paid once per anchor/cohort.
2. **What forces it.** R-adoption requires trust across upgrades, but pinning the old tool is another viable design. Twin evaluation is preferred because a newly detected violation that already existed in `A` appears on both sides, while semantic changes caused by new code appear only in `C`.
3. **Rejected.** Comparing old and new analyzer outputs attributes implementation churn to users. Permanently pinning `E1` preserves comparison semantics but prevents fixes and new analysis from entering the gate. Auto-migrating fingerprints without replay cannot prove what they now refer to.
4. **Falsified by.** Baseline replay cost remains unacceptable after caching, old snapshots cannot legally or practically be retained, or a version-independent proof identity is demonstrated for all rule classes.

This design does not claim that twin analysis makes correspondence trivial. It removes analyzer-version asymmetry; it does not solve arbitrary code lineage.

### D14 — Delta classification is multi-valued; ambiguous lineage is indeterminate — **FORCED**

1. **Decision.** The core, not a rule extension, constructs occurrence lineage from rule identity, semantic subject identity, normalized structural anchors, dependency context, and repository change mapping. Delta states are `existing`, `introduced`, `resolved`, `changed`, and `indeterminate`. A finding is gated as “new” only when introduction is established under the selected rollout policy; inability to match is visible and subject to the completeness gate.
2. **What forces it.** R-adoption says the mechanism must remain trustworthy. Arbitrary moves, refactors, generated code, split/merged symbols, and changed analyzer anchors make a forced binary choice capable of silently forgiving or inventing new violations.
3. **Rejected.** Path-plus-line hashes break on inserted lines. Message hashes bind identity to presentation. Fuzzy matching with a threshold but no ambiguity state turns heuristic confidence into policy. Letting extensions declare “existing” gives them authority to bypass the gate.
4. **Falsified by.** A complete, version-independent identity exists for every finding through arbitrary program transformations, eliminating ambiguous correspondence.

### D15 — Baseline formats are append-only/migrated explicitly and acceptance never occurs during upgrade — **FORCED**

1. **Decision.** New tool releases must read old anchor manifests or run a deterministic migration that emits a new linked object while retaining the old root. Unsupported schema or missing anchor objects yields `indeterminate`; it never triggers automatic re-acceptance. `accept` is a separate explicit action whose artifact shows exactly what becomes tolerated.
2. **What forces it.** R-adoption explicitly requires trust across upgrades; R-checkable requires historical inputs. Silent rewriting would let an upgrade change the accepted set without review.
3. **Rejected.** In-place database migrations erase the old interpretation. “If incompatible, regenerate baseline from current” can bless new violations. Best-effort parsing risks partial, invisible loss.
4. **Falsified by.** The product explicitly abandons cross-version acceptance compatibility or an immutable universal baseline schema is proven never to require migration.

## IV. Executing enough work quickly

### D16 — Execute a dependency DAG of deterministic tasks — **PREFERRED**

1. **Decision.** Planning expands requested rule instances into tasks for discovery, parse, bind, type, dependency, summaries, rule evaluation, evidence validation, and delta comparison. Tasks declare input object roots, output schema, capability, and target set. The scheduler executes the DAG, reusing outputs and invalidating dependents by keys rather than by timestamps.
2. **What forces it.** No requirement forces a DAG. It is preferred because W-agent needs incremental reuse, R-scale needs parallelism, and deep analysis naturally shares intermediate work across rules.
3. **Rejected.** A monolithic full-repository pass wastes work on rapid small queries. One independent pass per rule repeats parsing and semantic resolution. A mutable in-memory object graph without declared dependencies makes invalidation and reproducibility difficult to audit.
4. **Falsified by.** Profiling shows full runs are already below interactive latency at 100,000 files, or a streaming architecture achieves better reuse and determinism with materially less complexity.

### D17 — Cached facts are valid only under complete semantic keys — **PREFERRED**

1. **Decision.** A task cache key covers producer digest, output schema, normalized parameters, exact input object roots, transitive dependency summaries, language configuration, platform semantic inputs, and declared limits. Cache hits are schema-validated. Reusing a cache entry is semantically equivalent to executing its task; cold and warm runs must have the same assessment root.
2. **What forces it.** Caching itself is a judgment, hence PREFERRED. Once chosen for W-agent/R-scale, R-deterministic and R-checkable force complete keys and cache transparency.
3. **Rejected.** Path/mtime keys miss content and configuration changes. Analyzer-version-only invalidation is too coarse for performance and too weak for transitive inputs. Trusting serialized extension output without validation lets old or corrupt data cross authority boundaries.
4. **Falsified by.** Maintaining complete keys costs more than recomputation, or an analyzer's true inputs cannot be declared; that analyzer must then be non-cacheable rather than weakly keyed.

### D18 — One semantic engine has a one-shot mode and an optional local resident mode — **PREFERRED**

1. **Decision.** `check` can run the engine entirely in its process. For interactive use it may connect to, or start, a user-local workspace daemon that retains indices and coordinates overlapping queries. CI explicitly uses one-shot mode and obtains identical canonical results. Failure or absence of the daemon falls back to one-shot; the daemon is never an answer dependency.
2. **What forces it.** W-CI forces a non-resident path. Nothing strictly forces a daemon; it is preferred for W-agent and R-scale. Sharing the semantic engine protects R-deterministic.
3. **Rejected.** A mandatory local or remote service violates R-offline's no-service dependency and complicates CI. One-shot-only may pay cold-start and index costs for every agent edit. Separate implementations for daemon and CI invite result drift.
4. **Falsified by.** Measured one-shot latency meets the dominant workload without residency, or local process lifecycle/security costs exceed the saved work.

### D19 — Every query owns a snapshot; identical work can be coalesced without sharing mutable results — **PREFERRED**

1. **Decision.** The daemon captures or receives a snapshot root per request. It coalesces identical task keys, prioritizes foreground queries, and reference-counts cancellation so one canceled request cannot cancel work needed by another. Results are assembled only from immutable task outputs tied to that query's root.
2. **What forces it.** No requirement dictates this scheduler. It is preferred for overlapping W-agent queries while preserving D02 and D09.
3. **Rejected.** A single mutable “latest project” graph can mix edits across requests. Serializing all checks preserves correctness but wastes overlap and increases latency. Canceling shared work on the first client cancellation introduces timing-dependent results.
4. **Falsified by.** Overlap is rare in measured use, snapshot capture dominates, or a transactional mutable index demonstrates simpler equivalent isolation.

### D20 — Scoped checks prove their scope and use conservative impact closure — **FORCED**

1. **Decision.** A small check starts from changed resources relative to a named anchor, expands through known reverse dependencies and rule-declared global effects, and records the resulting target universe. If dependency information is missing, it widens to a safe scope or marks uncovered targets indeterminate. Only a full check may claim repository-wide coverage.
2. **What forces it.** W-agent asks a small “did I break anything?” question, but R-checkable forbids presenting a partial search as a universal answer. Deep analyses can be affected by edits outside changed files.
3. **Rejected.** Checking only edited lines misses type, call, dependency, and policy effects elsewhere. Always running the full repository preserves soundness but may defeat the dominant rapid workload at R-scale. Heuristic impact selection without recorded coverage gives an uncheckable clean result.
4. **Falsified by.** All supported rules are proven file-local, or full analysis at 100,000 files consistently meets the small-query latency objective.

The interactive wording is therefore “no violations found in the analyzed impact closure” plus coverage, never an unqualified “nothing broke” when work remains unknown.

### D21 — Parallel scheduling and resource limits cannot silently change semantics — **FORCED**

1. **Decision.** Tasks may run in parallel, but input enumeration, output ordering, tie-breaking, numeric behavior where relevant, and reductions are canonical. CPU/memory/fuel/depth limits are declared semantic inputs. Exhaustion produces an indeterminate cell and recorded usage, not truncated success. CI profiles pin limits; interactive profiles may choose smaller limits and receive a different, explicitly identified assessment.
2. **What forces it.** R-scale pressures parallelism; R-deterministic and W-CI require scheduling independence. Finite laptop resources mean nontermination/exhaustion must have defined output.
3. **Rejected.** “First result wins,” wall-clock timeouts, unordered hash-map emission, and race-dependent cancellation change output with load. Unlimited analysis risks hanging CI or a laptop. Silently returning partial data at a budget boundary creates false confidence.
4. **Falsified by.** All analyses are proven to terminate within fixed negligible bounds and run serially within scale targets, eliminating resource and scheduling variance.

### D22 — Heavy analyzers run in isolated workers and failure is localized — **PREFERRED**

1. **Decision.** Parsing/type/dataflow frontends run as supervised local workers with read-only snapshot access, bounded resources, and a versioned protocol. A worker crash marks its affected capabilities/targets indeterminate; independent tasks continue and a valid partial assessment is emitted when the core remains healthy.
2. **What forces it.** Worker isolation is not compelled. It is preferred because heterogeneous language engines may crash or retain large heaps, W-agent benefits from reusable workers, and explicit unknowns allow honest partial continuation.
3. **Rejected.** Loading all frontends into the core process gives lower IPC cost but expands the crash and memory-retention domain. Starting every analyzer per file is isolated but too costly. Aborting the entire run on one parser failure discards useful findings and coverage evidence.
4. **Falsified by.** In-process frontends prove materially faster and sufficiently failure-safe, or worker IPC/serialization dominates analysis cost.

## V. Third-party logic without surrendering the promise

### D23 — The initial public extension surface is declarative and non-inferential — **PREFERRED**

1. **Decision.** Third parties may publish rule packages in a bounded declarative language over versioned fact schemas, with fixed deterministic predicates, joins, aggregations, structural matching, and evidence templates. The language has no arbitrary native/WASM functions, I/O, process launch, network, clock, randomness, or model execution. New fact producers and deep frontends enter the trusted distribution through review, conformance tests, and release pinning rather than arbitrary runtime loading.
2. **What forces it.** R-extension explicitly leaves degree of support open, so this is judgment. It is preferred because it enables many architectural/convention rules while making R-deterministic, R-offline, “no language models ever,” and authority validation technically credible.
3. **Rejected.** Native plugins cannot be hermetically constrained portably and could call a model or network. General WASM removes ambient capabilities but still permits arbitrary embedded inference and complicates termination/evidence validation. No extension surface needlessly excludes common organization-specific rules.
4. **Falsified by.** Real third-party rules require analyses not expressible in the bounded language, and a portable sandbox plus certification process can enforce no-inference, determinism, provenance, resource, and evidence constraints for executable extensions.

This is intentionally not optimized for maximum ecosystem size. If executable extensions are added later, their results need a distinct trust class until the product can enforce the same guarantees as built-ins.

### D24 — Extensions provide candidates; the core owns authority and package identity — **FORCED**

1. **Decision.** An extension can select facts and propose a claim/evidence template. It cannot read outside the snapshot, mutate facts or baselines, choose occurrence lineage, suppress uncertainty, change severity/gating policy, set exit status, forge producer provenance, or write the canonical result. Policy locks every package and transitive data dependency by digest; a run never resolves “latest.”
2. **What forces it.** R-deterministic and R-checkable require exact executable/data identity. R-adoption would be untrustworthy if extensions could declare findings old or accepted. W-CI requires exit behavior to remain under core/team policy.
3. **Rejected.** Trusting package names/semantic-version ranges allows the same config to change over time. Letting plugins emit final reports fragments schema and baseline behavior. Runtime package resolution violates offline operation.
4. **Falsified by.** Extensions are removed entirely, or a cryptographically attestable extension runtime proves equivalent core enforcement while safely delegating these authorities.

## VI. Failure and process status

### D25 — Represent truth, completeness, and process health separately; use a small stable exit mapping — **PREFERRED**

1. **Decision.** The report contains (a) logical verdict `PASS | FAIL | INDETERMINATE`, (b) independent coverage/completeness with reasons, and (c) operational diagnostics. Exit codes are: `0` complete PASS; `1` at least one policy-gating violation (coverage may also have gaps); `2` no proved gate failure but required coverage is indeterminate; `3` invocation/configuration error before a valid assessment; `4` core failure before a valid assessment; and conventional `130` for interruption. Analyzer/extension failures after planning belong in the assessment and normally lead to `2`, not `4`.
2. **What forces it.** W-CI requires reliable nonzero behavior and the prompt requires reporting what could not be determined. The exact numbers and precedence are judgment, hence PREFERRED.
3. **Rejected.** One nonzero code for everything prevents CI/humans from distinguishing code violations from tool failure. A bitmask encodes combinations but is awkward in shells and still cannot carry rich diagnostics. Returning `0` with warnings for partial analysis produces false passes. Returning only the most severe operational code can hide a proved violation; the report carries all dimensions while the exit code remains simple.
4. **Falsified by.** Target CI platforms impose a different fixed convention, or user research shows a bitmask/standardized sysexits mapping is materially less error-prone.

`not_applicable` is not incomplete: it means policy and capability planning established that the rule does not address that target. `indeterminate` means an answer was required but not established. CI's full profile requires all policy-required cells to be determinate. Interactive checks use the same truth semantics even when they request a narrower target universe.

## VII. Language and deployment choices

### D26 — Implement the trusted core in Rust — **PREFERRED**

1. **Decision.** Use Rust for snapshotting, canonical serialization, scheduling, CAS, policy evaluation, evidence validation, baseline comparison, CLI, daemon, and worker supervision. Language engines may be separate pinned workers when their authoritative ecosystem is elsewhere.
2. **What forces it.** No requirement names an implementation language. Rust is preferred for a distributable offline binary, controlled memory/CPU at R-scale, safe concurrency for W-agent, and a small trusted runtime without a required VM.
3. **Rejected.** Go is a live alternative with simpler builds but less control over memory/layout and weaker embedding options; this is not disqualifying. C++ offers control but a larger memory-safety burden. A TypeScript/Python core eases some analyzer integration but adds runtime packaging, cold-start, and large-repository memory concerns. A JVM core is viable but enlarges deployment/runtime assumptions.
4. **Falsified by.** Team expertise or ecosystem integration makes another language materially safer/faster to deliver, profiling shows runtime costs are irrelevant, or supported-platform distribution is worse with Rust.

### D27 — Make TypeScript/JavaScript and Python the two deep language families — **GUESSED**

1. **Decision.** The first deep frontends provide project-aware parsing/binding/types, module resolution, call/control-flow, and interprocedural summaries for TypeScript/JavaScript and Python. “Deep” is capability-tested, not a marketing label.
2. **What forces it.** R-languages forces two deep languages but gives no repository demographics, customer priorities, rule catalog, or required platforms. The choice is a guess based only on their likely prevalence in AI-agent-edited code, which is not evidence supplied by the prompt.
3. **Rejected.** Rust, Java/Kotlin, C/C++, C#, and Go are all plausible. Selecting the core implementation language as a deep target merely for symmetry is not a product requirement. Claiming more than two deep languages initially dilutes the explicit depth commitment without staffing data.
4. **Falsified by.** Target-customer corpus and rule-demand data rank a different pair, or compiler licensing/distribution/determinism makes either chosen frontend impractical.

Bundled/pinned official frontend components should be used where they provide the most faithful semantics, but their diagnostics are normalized into the common evidence/provenance protocol. Exact frontend selection needs a separate empirical/licensing decision.

### D28 — Breadth comes from capability-graded adapters, not fake semantic uniformity — **PREFERRED**

1. **Decision.** Additional languages can support file/layout/dependency rules, token/structural patterns, and parser-level facts through pinned adapters. Each adapter advertises and tests exact capabilities. Cross-language facts share the small kernel; language-specific semantics remain versioned extensions. A rule requiring types cannot run on a parse-only adapter.
2. **What forces it.** R-languages forces breadth and unequal depth, but not this adapter structure. It is preferred because it makes the inequality explicit and supports incremental addition without weakening D06.
3. **Rejected.** Translating every language into one universal AST discards semantics and encourages rules to overclaim. Calling text regex support “language support” without capability labels misleads users. Building deep bespoke frontends for every language conflicts with the stated two-language focus.
4. **Falsified by.** A common semantic IR demonstrates faithful deep representation across the target languages at acceptable cost, or users define “support” solely as deep compiler-level analysis.

### D29 — Ship a self-sufficient local distribution and make hosted consumption one-way — **FORCED**

1. **Decision.** The distribution contains the core and pinned built-in analyzer assets needed for declared capabilities. CI invokes the same binary in one-shot mode with network unnecessary and produces the canonical artifact plus exit code. A hosted product may ingest or render a sealed artifact, but no hosted response participates in assessment, baseline comparison, evidence, or verdict.
2. **What forces it.** R-offline, R-hosted-optional, and W-CI directly require this process/deployment boundary.
3. **Rejected.** A remote analysis API or cloud cache in the correctness path makes network/service state part of the result. A hosted-only baseline store makes offline net-new gating impossible. A separate cloud analyzer could produce different semantics from local CI.
4. **Falsified by.** The product requirements change to mandate centrally computed results or accept loss of offline/reproducible operation.

### D30 — Signatures are optional; content integrity is mandatory — **GUESSED**

1. **Decision.** Every anchor is hash-addressed and intended for version-control review. Cryptographic reviewer signatures are supported as an optional policy, not required by default.
2. **What forces it.** Nothing in the prompt defines an attacker, key infrastructure, protected branch model, or who is authorized to accept debt. Hash integrity is needed for R-checkable; signer authentication is not specified.
3. **Rejected.** Mandatory signatures impose key management without a stated threat model. No integrity binding at all permits accidental mutation to go undetected.
4. **Falsified by.** A threat model says contributors who may edit repository files must be unable to alter accepted state without designated approval, or enterprise adoption requires signed provenance by default.

## VIII. End-to-end forced chain

The architecture follows from a short sequence rather than from a preferred diagram:

```text
later-checkable claim
  -> exact immutable input and policy identities
  -> hermetic deterministic analyzer cohort
  -> structured evidence plus explicit coverage
  -> immutable assessment artifact

rapid overlapping edits
  -> per-query snapshots
  -> keyed reusable tasks
  -> optional local residency, never semantic dependency

accepted existing debt across upgrades
  -> immutable accepted snapshot
  -> same-current-semantics analysis of anchor and current
  -> explicit lineage ambiguity
  -> no automatic baseline mutation

unequal language depth + third-party interest
  -> declared capabilities
  -> unknown rather than fabricated pass
  -> constrained extension authority
```

A minimal full-check flow is:

1. Capture and seal the logical source/config snapshot.
2. Canonicalize policy and resolve only digest-pinned local packages.
3. Plan rule/capability/target cells and their task DAG.
4. Execute hermetically, reusing only completely keyed validated outputs.
5. Validate evidence and account for every planned cell.
6. If gating against accepted debt, evaluate/cache the anchor under the same current semantics and compute a multi-valued delta.
7. Derive verdict and completeness in the core.
8. Emit a canonical assessment root, human projection, replay closure as requested, and stable process exit.

## IX. Known unknowns that should not be disguised as architecture

- **Latency and resource budgets.** “Rapid” has no numeric target, and 100,000 files says nothing about dependency density or generated code. Daemon, cache granularity, and worker boundaries require benchmarks.
- **Soundness expectation.** The prompt does not say whether rules favor false negatives, false positives, or explicit unknowns. This derivation refuses silent unknowns, but individual analyses still need contracts.
- **Baseline lineage policy.** Whether editing an existing violating construct should keep it accepted, mark it changed, or make it newly gated is a product policy per rule/rollout, not derivable here.
- **Threat model.** There is no statement about malicious contributors, hostile repositories, baseline authorization, secret source retention, or artifact signing. D30 is therefore deliberately GUESSED.
- **Language pair and rule catalog.** D27 is deliberately GUESSED until corpus and demand data exist.
- **Platforms and distribution constraints.** Supported operating systems, CPU architectures, maximum artifact size, air-gap installation mechanics, and compiler licenses are unspecified.
- **Extension demand.** The declarative boundary should be tested against real third-party rule proposals before adding arbitrary executable plugins.
- **Formal proof level.** Structured evidence and replay establish provenance and repeatability, not universal analyzer correctness. If “prove” is intended to mean proof-carrying static analysis, that is a substantially stronger unstated requirement.

These unknowns are falsification inputs, not invitations to make silent defaults part of the product contract.
