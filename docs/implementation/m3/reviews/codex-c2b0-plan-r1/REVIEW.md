# C2B0-PLAN-r1 review

**Verdict: REQUIRED-FINDINGS.** Four required findings and two nonblocking observations. Q1–Q5 rulings are below.

## Subject verification

Verified the 578-byte manifest, SHA-256 `e06858bb1c3f11495516f26a5e4fdc8ec552e672b98b3573bb307fdab40eb43c`, and both members: PLAN-r1.md, 17,274 bytes / `e936a273c2ea15f0033045b7035392ac7d0ee6e60bef018b280208c2bffa0ccc`; C2B-GATING-r1.md, 5,508 bytes / `18e18bec084b0f0fad32404c7fa024e0f50752d337786c0c10302e55c3529b9b`. The gating memo is context, not a separate plan acceptance.

Declared bases are product `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a` and architecture `2d169666ee5c28eedea5e43083b7968b6ba80e9f`. Live HEADs have advanced to product `b7538549b727e13013f36d3b7c2e2917e767f3f2` and architecture `bd77891d106cd40a0e9e33962aee7e9e4ada7505`. Git checks confirmed the inspected identity JSON code, capture session, evaluator universe checks and native schema match the declared product base, and the inspected M3-C law/native contract match the declared architecture base. The review does not silently rebase the subject.

## Required findings

### C2B0PLAN-R1-RF-1 (P1): Define traversal that actually discovers pnpm sibling dependencies

Location: `docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r1.md:68`.

LD-C2B0-1 seeds the unit root's ancestor node_modules directories, and LD-C2B0-3 adds each package's own child node_modules. Neither rule reaches the siblings claimed by LD-C2B0-4. After node_modules/foo resolves to node_modules/.pnpm/foo@1/node_modules/foo, the target's own nested directory is .../foo/node_modules; foo's dependency bar is instead a sibling at node_modules/.pnpm/foo@1/node_modules/bar. That directory is not below foo, and .pnpm was deliberately excluded from the initial listing. Enumerating the target as a row does not itself enumerate the target's parent. A layout following the explicit traversal can therefore omit an ordinary pnpm dependency while the stated positive control expects it.

Required change: Specify the dependency-search directories queued for each resolved package target, including the enclosing virtual-store node_modules directory and relevant in-project ancestor search directories, with deterministic exclusions and no wholesale .pnpm-store scan. Preserve distinct installPath/realPath rows. Add a pnpm fixture with a sibling dependency reachable only through that virtual-store parent, plus scoped siblings and workspace-target ancestor lookup, and assert the exact visited-directory set as well as output rows.

### C2B0PLAN-R1-RF-2 (P1): Define visited and row-merging rules for the package-link graph

Location: `docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r1.md:65`.

Every link adds its target as a row and those target rows are enumerated in turn, but the plan gives no visited/queued identity or merge rule. Two aliases can point to the same real directory, a target can already have been encountered through another search directory, and valid package dependencies can form cycles through distinct symlinks to real directories. The one-link-level refusal does not stop such package-graph cycles. Treating a repeated installPath as impossible and refusing Order at line 89 would reject legitimate shared targets; simply re-enumerating them can loop or consume the ledger repeatedly. The 100,000-row bound only bounds distinct output rows, not revisits.

Required change: Specify charged worklist/visited state keyed by normalized project-relative directory/search-directory identity and a map keyed by installPath. Reuse equivalent rows and manifest captures, refuse inconsistent observations, and enumerate each required real directory/search location once while preserving alias rows. Distinguish a forbidden filesystem symlink chain from an allowed dependency cycle. Add shared-target aliases, repeated target discovery, a diamond dependency graph and an A-to-B-to-A package cycle; require deterministic complete rows and finite bounded work without an Order or Budget refusal caused solely by revisiting the graph.

### C2B0PLAN-R1-RF-3 (P2): Separate non-dependency exclusions from read-set eligibility

Location: `docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r1.md:79`.

The plan uses C1c-0's read_set_path to apply exclusions to packages and link targets, while also promising a first-party workspace target such as packages/x. In the declared C1c r2 interface, read_set_path returns Forbidden for an authorized path outside every node_modules tree. It cannot simultaneously serve as an unconditional workspace-target exclusion predicate and admit packages/x. The specified C1c pruned-tree opener also targets regular-file capture; an explicit directory-reach/exclusion interface is needed for layout traversal. Merely skipping the predicate for workspace targets would lose the promised VCS/Cargo/extent checks.

Required change: Define the C1c-0 interfaces the layout needs: safe no-follow directory reach and a non-dependency exclusion check that can classify first-party targets separately from dependency-tree read-set eligibility. First-party workspace targets must retain the ordinary opener/custody and Walk-origin reuse rules, while all targets preserve boundaries, ignorePaths, VCS, Cargo-output and exact custody-anchor exclusions. Reconcile this with the separately reviewed C1c interface before integration. Add an allowed packages/x target and forbidden workspace targets under Cargo output, VCS/custody anchors, ignorePaths and admitted boundaries, with no-open/no-read assertions for excluded targets.

### C2B0PLAN-R1-RF-4 (P2): Own a freshness interval when no unfrozen batch can accept C2b-0

Location: `docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r1.md:85`.

LD-C2B0-7 assigns the snapshot recipe change to C2b-0 but only says it joins whichever batch is open. It does not limit joining to before the final-input freeze or schedule an interval if no batch is open. The dependency chain permits C1c-0 to have refreshed separately before C2b-0 integrates, so the companion receipt then becomes stale anew. An existing batch may also already be frozen. Neither an earlier refresh nor adding edits after a pre-run review covers this later recipe. The plan's dependency on C1c r2 is explicitly subject to revision; the missing interval cases cannot be left implicit in that reference.

Required change: State that C2b-0 may join an existing reviewed interval only before its final-input freeze. Otherwise it opens and owns a new interval with a fresh accepted baseline, exact receipt-specific deltas, pre-run review, frozen-input mechanical blind refresh and post-run review before dependent reliance. Track cumulative changes if an interval is already stale; an empty additional discovery delta does not make a previously stale discovery receipt current. Preserve passing output checks separately from freshness and update the C1c cross-reference to the agreed interval rules.

## Nonblocking observations

**C2B0PLAN-R1-NBO-1: Describe the selected JSON profile rather than generic strict JSON** (`docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r1.md:74`).

identity::canonical::parse is narrower than ordinary strict JSON: it rejects floating-point numbers, negative zero, out-of-range integers, duplicate keys and depth beyond 32, including in unrelated manifest fields. For example, a manifest with valid string name/version and an unrelated numeric value 1.5 is valid JSON but refuses this reader. MAX_BYTES is only one of its constraints.

Explicitly name this supported manifest profile and its typed refusal, and add representative profile-boundary cases. If ordinary JSON manifests with such unrelated values must be supported, select a bounded projection/parser that handles them while preserving exact captured bytes. Do not label all such refusals malformed JSON.

**C2B0PLAN-R1-NBO-2: Distinguish the row-count check from complete record admission** (`docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r1.md:111`).

The statement that 100,000 rows admit cannot be a whole-record control through the existing identity canonical encoder: it has a 4 MiB limit, and 100,000 rows with the mandatory 64-character digest and five named fields necessarily exceed it. The schema row maximum is an upper bound, not a promise that this whole layout fits every other envelope.

Test the count predicate at 100,000/100,001 in isolation and separately test feasible full layouts at canonical byte/depth and ledger boundaries. Specify the typed canonical-encoding refusal and include record construction, sorting, admission, retention and encoding buffers in the complete layout model.

## Question rulings

**Q1.** Accept no row for a recognized directory without a regular package.json as an explicit conservative supported subset. No manifest bytes may be invented. A provider read there remains outside the committed read set; this does not claim complete Node support for manifest-free index.js packages. Keep special files and symlinks from becoming manifest reads.

**Q2.** Prefer typed Link refusal for a selected candidate whose resolved target escapes the project, rather than silently omitting an installed dependency. Normalize lexical components without following the installPath, reject traversal above root and intermediate/final symlink traversal under the supported layout. Repeated references to real directories are graph revisits, not symlink-chain refusals (RF-2).

**Q3.** Refuse a malformed or unsupported manifest as Manifest rather than silently omit it. The selected identity reader has the additional product-profile restrictions in NBO-1; make those explicit if retaining this parser. A valid general-JSON floating-point field is not a syntax error merely because the selected product profile rejects it. The existing 4 MiB reader bound can be reused explicitly; it does not impose config-file custody on installed trees.

**Q4.** Yes: C4a/J2 own choosing the no-layout branch or projecting the refusal; this library returns typed failure and never truncates rows. Composition must define the required item-5/H-NM no-layout path and how captures used only by a refused layout cease to be resolved-input dependencies without bypassing the leftover rule. A session/ledger must not be restarted to erase spent work, and WorkFailure::Budget must not silently become a successful partial layout.

**Q5.** The snapshot ledger is a reasonable explicit routing decision because the layout contributes to the same sealed snapshot. Accept it only with the full layout/capture/parse/graph/record term and soundness vectors before C2b-0 acceptance, at the unchanged r9 caps and required 2x gate, including accepted VCS/read-set work where applicable. Reconcile the earlier C1a/r9 assumptions that placed C2 pre-walk captures on discovery/outside r9, and avoid charging/re-reading the same capture twice. No separate unsourced resolution ledger or silent cap increase is approved; if the fixed-cap derivation fails, obtain a law revision.

## Other conclusions

The layout-only split is sound: retained layout rows and manifest digests do not themselves require a manifest-admitted toolchain or stdlib closure. This preparatory C2b-0 can satisfy the specific C1c integration edge for the layout after its own dependencies and review. The TypeScript context, default-lib table, stdlib closure join and universe binding remain C2b-1/C2a work. The gating record correctly separates those dependencies; it does not authorize substitute unsigned closures or claim C2a completion.

The ancestor search bounded by the project root, scoped-package enumeration, exclusion of dot-prefixed install entries, explicit nested-package rows and no implicit install are reasonable lead decisions, subject to the complete linked-package search in RF-1. Reading link text with readlinkat, resolving lexically and reaching a real directory from the retained root is compatible with the law's no-follow discipline. Every realPath being a retained installPath matches the reference/evaluator consumer check; that membership alone does not prove a traversal found all dependencies.

Manifest content must come from the session's exact captured bytes, including when a first-party capture is reused. The implementation needs a bounded way to parse retained custody bytes or a session-owned capture/parse handoff; it must not reopen the project file for parsing after hashing. Source capture, digest and later read-set observation checks remain one coherent identity. Sorted canonical layout admission, raw digest computation, typed refusals and composition preconditions are appropriate. Same-root/unit/extent provenance remains a composition obligation rather than something schema admission proves.

Returning None when no eligible node_modules directory exists on the unit chain is a reasonable no-layout result. The schema permits empty entries, so a physically present but empty or wholly excluded directory needs an explicitly consistent policy; absence and a deliberately committed empty layout are not interchangeable solely because the row count is zero.

Lead-authored vectors are appropriate because the reference model consumes layouts but does not derive them. The current vectors cover flat/scoped npm, nested npm, manifest identity, link refusals, exclusions, reuse, descriptor races and digest/consumer agreement. They do not yet establish pnpm sibling completeness or finite graph handling; add RF-1/RF-2 controls and mutations. Add RF-3 timing/provenance controls and qualify the boundary controls as NBO-2 describes. Successful evaluator admission is necessary but cannot detect a missing dependency directory that the host never enumerated.

The plan explicitly promises revision if the C1c interface review changes it. Preserve that gate: this review does not accept C1c r2 or its later revisions by reference, nor any code, caller, census refresh, Plan selection or qualification.

## Review boundaries

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, rustc, builds, tests, lanes, network, panes or delegation. No private fixture, installation directory, signing keys, held trees, T2 stores or cache were accessed. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
