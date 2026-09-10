# Codex independent observations, before reconciling Claude reports

Status: audit working findings, not adopted contract repairs. Review subject is the immutable post-D371 docs snapshot. Existing prior scope/contract acceptance does not establish runtime qualification.

## C-01 — accepted configuration reference admits non-integer values

HIGH, newly_discovered_defect. Frozen host-foundation-model.v1.py strict() permits finite floats; validate() uses standard Draft202012Validator integer semantics. config schemaVersion 1.0 and 1e0, and budget limits 1.0, 1e0, 1.0000000000000001, 9007199254740991.1 all produce ACCEPT in configuration(); fractional literals are rounded by json.loads before validation. Control integer literal 1 accepts with an int; invalid literals propagate Python float budget values. Evidence: codex-config-numeric-probes.json. Original host-foundation checker still passes 210/210 (182 scenarios), so its corpus does not detect this.

Contradiction: IMPLEMENTATION-FREEZE.md law18 lines1499–1508 explicitly requires exact scalar type and says float is not integer at every admission depth. Host-foundation-completion.v2 §3 binds integer schemaVersion/budget and existing uint64 provider projection. A consumer can copy accepted reference behavior and either admit unsupported input or fail later at another boundary; rounded values break exact provenance. Required correction: exact typed numeric admission before schema/scalar comparisons and retain lexical float/exponent/rounding negatives with ordinary integer control, including nested fields and generated adapters. A JSON Schema schema alone does not enforce this law. Owners DR103/123/125, config and host admission; no product exploit is claimed because product is not implemented.

## C-02 — G13 reference validator lacks independent subject and behavior-oracle bindings

HIGH candidate integration_gap, pending challenge. check_g13_result_design_v4.py valid() only equates candidate report hostDigest/providerClosureDigest with candidate runner fields (lines35–37), while HARDWARE trusted observation keys omit both executable digests. Changing all candidate subject hashes consistently to other hashes leaves trusted inventory unchanged and returns true. Setting every fixture expectedCount and actualCount to zero while expectationMatched=true also returns true. Positive control true. SchemaMajor1.0 also passes (same type hazard as C01).

Evidence codex-g13-probes.json. Required result truth: analysis-quality-completion.v2 §§3–4 exact expected sets, signed closure and subject/corpus digests; performance successor's independent observation boundary. Caveat: reference validator is not an entire release promotion system, and actual measurement/custody remains qualification work. The finding is NOT that a shipped product or signed CI system was exploited. Need clarify trusted report producer vs untrusted artifact; exact subject and per-fixture oracle must come from independent gate context or a retained authenticated producer binding, not duplicated self-assertion. Owners DR118/121/G13, full-product qualification integration. Old validator's 58/58 self-tests do not prove this join.

## C-03 — command/workflow state transition is not defined by a derivation DAG

HIGH integration_gap/known_open_contract. Chapter13 §9 preserves typed invocation steps but explicitly defines no Invocation/Run identity; coop surfaces §multi-stage says one invocation creates a parent Run; C2 graph is analysis stages rather than a composition of stored query, policy/baseline adoption, review, mutation and new verification run. Need distinguish immutable source-bound analysis Run, operational Invocation and per-step outcomes. Source-changing repair produces another snapshot and verification attempt; parent summary cannot be sealed before known required child effects/outcomes. Cancellation, required/optional steps, aggregate exit, idempotent retry and artifact linkage need exact contracts. User fit/audit behavior must not lead to a second per-tool authority. Owners DR117/131/133/125 and D9/evidence. Existing D371 correctly leaves OPEN; not a newly broken accepted full-product contract.

## C-04 — durable evidence identity, privacy, retention and project namespaces need an integrated successor

BLOCKER known_open_contract/integration_gap. D371 admits durable authoritative product; C1 ten preview-disposed rows don't close it. Native resolved-input ProjectId marker under source versus D369 private host projectKey/namespace root are different authority/custody systems. V1 evidence readable chapter says no-policy means ephemeral/reject while adopted CD-RT5 explicitly says no-policy durable/unbounded; accepted full-product successor must preserve the binding owner choice rather than accidentally implement stale readable text. Role of long-lived source/runtime evidence, proof loss, independent limits, archive cost and actual storage writer must join evidence identities, D9, threat model and lifecycle without separate authoritative stores. Recent candidate identity recipes exist; their presence or detailed vectors do not establish applied closure. Owners DR002–009/109/113/124. Do not describe all identities as absent; exact recipe standing and required inputs are the issue.

## C-05 — platform support and concurrency promises need explicit product validation

MEDIUM review concern, not proven contract defect. Actual preview admission is APFS/ext4 plus stable birth-time and release-measured Ubuntu kernel flavor/series; generic Linux labels don't imply containers, overlay/virtiofs, enterprise distros or normal developer home layouts. Foundation explicitly discloses refusals. D371's four target families need readable exact support cells. Security §5.4's exclusive project operation lease and per-operation lifecycle lease must be reconciled for concurrent analyses/agent invocations; concurrency1 performance tests cannot establish the intended agent-loop experience. Need validate trace before claiming deadlock/serialization; this is currently an untested cross-contract concern. Owners DR118/119/126, DR107/125 and G13/G18.

## Strengths independently confirmed

- Single host authority, pure evaluator, facts/findings/verdict/output separation and exact D9 post-commit output failure distinction.
- Predicate-relative evidence sufficiency; no absence claim from partial graph; test/runtime observations don't prove safe deletion.
- No ambient runtime substitution, private state, broker grant checks and confinement-honesty boundaries.
- Current lifecycle SQL protects with one-writer callbacks, FK references and dedicated OS lease locks; local reference checker passed 200/200. Callbacks remain trusted host observations, not OS proof.
- Baseline detector pivot and explicit indeterminate on incompatibility; advisory model review cannot change policy.
- Existing docs clearly distinguish design, implementation and qualification in many normative units. Navigation must present effective choices without requiring historical archaeology.
