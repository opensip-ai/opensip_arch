# B2-d implementation plan r1 review

Verdict: **REQUIRED-FINDINGS**.

The subject manifest independently matches SHA-256 `22709600ab21e0b6a6e8d8722ccad7c99dad759964955d5d21f0393000236adf` (449 bytes). Its sole member PLAN-r1.md matches 15748 bytes and `df3befe5f3e482174909b3801027aba2fa6b61e121b377a2b0bc75e3b79bbbc0`. Product main is clean at `a50ae9646c9cf6b6c3600c2c28c816f7a77ab609`; architecture is at `4415adb5051de65c8e2b0e0ce493d1a59f2941c6`.

## Required findings

**B2DPLAN-R1-RF-1 — Correct the inherited entry-point state rule for FR-1 disclosures**

PLAN-r1.md section 1, lines 55-66; section 3.

The plan preserves the reference entryPoints.state rule, which returns none whenever all effect entry lists are empty, even with config-requires-evaluation. For example, vite.config.ts without index.html, next.config.js without routes, or an outside-subset pnpm carrier produces none. NE FR-1 and law item 16 require partial for a config needing evaluation. The wrapper cannot promise exactly four changes while inheriting this conflicting state rule.

Required: Explicitly amend the reference state calculation for FR-1 disclosures, propagate it to product vectors, and add no-known-entry and mixed-recognizer cases. Keep any explicit override behavior separately specified.

**B2DPLAN-R1-RF-2 — Enforce the entry-point ceiling across the unit**

PLAN-r1.md section 3, lines 117-124.

FR-4 sets maxEntryPointsPerUnit, but the proposed overflow policy examines one recognizer and drops only that recognizer when its own list exceeds 65536. A unit with 65536 Next.js route entries and a distinct Vite index.html exceeds the unit bound although neither result exceeds its individual schema maxItems.

Required: Define the per-unit aggregate effective recognized-entry calculation and its bound, including overlap handling. Add 65536/65537 cases split across recognizers. An explicit all-or-nothing disclosure without truncation can be conservative, but it must apply at the owning unit scope and retain uncertainty.

**B2DPLAN-R1-RF-3 — Do not equate explicit empty entryPoints with absence**

PLAN-r1.md section 4, line 148; section 5, line 160.

The explicit override activates only for a nonempty resolved array. The configuration schema admits entryPoints: [], and the resolver preserves winning-leaf provenance. Law item 1 distinguishes absence (automatic) from an admitted higher-layer array replacing a lower array whole. A project/local explicit [] can clear a lower explicit list; the proposed check instead re-enables recognized defaults and permits recommendations as if configuration were absent.

Required: Determine explicit intent from presence/winning provenance, define the effective empty-set result, and preserve higher-layer empty overrides. Add absent versus explicit-empty and lower-nonempty/higher-empty controls for recognition and recommendation generation.

**B2DPLAN-R1-RF-4 — Keep the proposed YAML grammar a subset of scalar sequences**

PLAN-r1.md section 2, lines 77-86.

The stated plain-scalar exclusions reject colon-space only, so `packages:\n  - foo:\n` satisfies the proposed scalar rules although foo: is a block mapping entry, not a plain scalar. Colon followed by a tab has the same separator issue. The sequence-item production also needs explicit separation after the dash; -foo is scalar text rather than a block-sequence item.

Required: Specify YAML-valid dash separation and plain-scalar colon termination/separation rules, then reject mapping-valued items and other non-scalar constructs with the existing disclosure. Add terminal-colon, colon-tab, dash-without-separation and quoted counterparts to the grammar vectors.

**B2DPLAN-R1-RF-5 — Settle TOML parser resource differences before defining exact oracle equality**

PLAN-r1.md section 1, lines 46-51 and 68-73; section 3, line 133.

The oracle uses tomllib while the product uses parse_toml, which has a 4 MiB byte cap, a recursion limit and a 1000000-node limit. A valid Cargo document with a usable package/workspace table plus a sufficiently large unrelated array can parse in tomllib and fail NodeLimit in the product. The current plan requires every oracle vector to reproduce byte for byte but supplies no resource-difference disposition or differential controls.

Required: Declare how every parse_toml error maps to recognition disclosure and the shared Cargo-workspace fact. Align the oracle profile or label intentional product-bound divergences, following the existing B3-b parser-control precedent. Include usable tables plus unrelated deep/wide fields and exact/past-bound inputs.

**B2DPLAN-R1-RF-6 — Map unit-relative recognition paths before proposing project settings**

PLAN-r1.md sections 3-5 and Q2.

Recognition effects are unit-root-relative, while recommendations are placed in a project configuration carrier. For a unit rooted at apps/web, recognized src/main.ts must not be proposed as project discovery.entryPoints src/main.ts. That wrong path can pass the actual resolver because syntax admission does not establish unit ownership. Deferring all path joins to C4 leaves B2-d3 recommendation evidence incorrect.

Required: Specify the unit-root-to-project path mapping for proposed entryPoints and ignore conventions, preserve unit identity through aggregation, and test nested units and colliding relative names. Keep this recommendation mapping separate from the still-unaccepted FR-6 change to retained recognition paths.

## Answers to the plan's decisions

**Coverage and ownership.** The overall split covers the nine host recognizers, readers, recommendation evidence and FW-01 controls, and appropriately leaves file capture to C1/J1, Plan commitment to C4, consumption to providers, and command rendering to M4. The listed findings block the promise that FR-1–FR-5 hold exactly. A schema-valid record alone cannot detect the inherited FR-1 state conflict or the cross-recognizer FR-4 overflow.

**B2-d0 and disclosure strings.** A separately reviewed, hash-pinned wrapper bound as contract successor 171 is an appropriate way to update the accepted B-S9 reference. Parsed Cargo tables, JSONC checking and the selected YAML reader are justified by item 16. The new Cargo.toml-not-toml and tsconfig-not-jsonc strings fit the existing open unresolvedChoices field and the model's package.json-not-strict-json precedent; they require exact vectors and safe parse-error dispositions. However, the wrapper needs the additional state correction and a stated product-parser resource profile. The proposed four-change/everything-else-equal boundary is not presently sufficient.

**LD-B2D-1.** A first-party closed reader with no YAML dependency is consistent with item 16 and M3-P0. Excluding other top-level keys rather than silently skipping unsupported syntax is defensible. Narrowing quoted escape support is also a legitimate closed subset. RF-4 concerns accepting syntax that is not a scalar sequence, rather than demanding a full YAML reader. The proposed 64 KiB cap should be treated as this reader's selected bound; item 14a's TypeScript-file cap does not itself impose a generic bound on every format.

**LD-B2D-2.** The closed nine-result/one-evidence-file implementations make the 32-recognizer and 64-evidence ceilings unreachable in ordinary current inputs. Structural assertions are reasonable, but the promised limit/one-past controls should exercise the bound validator directly rather than claim a nine-result count demonstrates the 32/33 boundary. A nontruncating disclosure for entry-point overflow is a defensible conservative design; FR-3's no-refusal sentence specifically concerns unrecognized frameworks, so it is not by itself the law for every overflow. The plan must settle the aggregate bound and uncertainty explicitly, as RF-1/RF-2 request.

**Q1 / LD-B2D-3.** No law clarification is needed merely to leave the semantic resolver's discovery fold empty and bind recognition through FrameworkRecognitionPlanV1. Law item 1 explicitly states both that the M3 semantic fold is empty and that discovered entry points, test globs and ignore conventions bind through their own Plan records. This is stronger authority than the plan's cited line-204 control alone. Recognizer id/version on each effect-bearing result gives an unambiguous source for DISCOVERED provenance; its rendering and retention/consumer handoff should be covered by vectors. It is not a seventh configuration layer. The remaining problem is the explicit-array behavior in RF-3, which must be corrected rather than justified by keeping the fold empty.

**Q2.** The accepted reference's unit-relative recognition rows may remain unit-relative in B2-d. The schema's x-opensip-path-law note is explicitly proposed, and Grok's report-evidence-design-02 review states S1–S4 remain unaccepted proposals. Do not silently implement FR-6–FR-8. C4 must settle the eventual retained Plan path join before consuming those records. Separately, B2-d3 already emits project settings and must join those paths now; that is ordinary recommendation correctness, not adoption of FR-6 (RF-6).

**Q3.** An internal pure RecommendationEvidenceV1 type is appropriate at M3; item 18 does not require a new public wire schema or a command. The five evidence parts, use of the actual resolver and unchanged-with-no-proposal control are correct. Not proposing workspaceRoots avoids turning package workspace recognition into D15 membership authority. Round trips must validate the actual mapped project settings and preserve explicit choices; syntax acceptance alone cannot prove the proposed path names the intended unit file.

**Order and gates.** Reference, reader, recognition and recommendation units with separate review/inventory gates are a sensible sequence. Settle these plan semantics before freezing B2-d0: its oracle must include the revised state, bound and explicit-intent behavior that later units are required to reproduce. No product implementation or qualification is accepted by this plan review.

Non-blocking observations: none separately recorded.

Only REVIEW.md and review.json are written. Neither repository was edited, committed or pushed. No product build, test, generator, census, network, delegation, installation directory, private fixture, signing keys, T2 store or overlay was accessed. Counterexamples above are derived from the documented grammar, schemas and source; no model or product code was executed.
