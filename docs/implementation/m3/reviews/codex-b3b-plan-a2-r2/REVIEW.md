# B3-b plan amendment A2 r2 review

Verdict: **ACCEPT**. No required findings. One non-blocking implementation observation.

Subject: `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A2.md`, 11,194 bytes, SHA-256 `98c5cff08b8e9554fec5ff3f0a9e44dc66c849ff4e03a7e36d57f039ba1829f1`. Byte count and hash match. Architecture HEAD matches `1f3f2b1ea4d019a1f24980f05cb2d2ef2501d766`; clean product main matches `03876532b54d8327db96091fababb1fd994a83d2`.

## Prior findings

**B3BA2-R1-RF-1 resolved.** The original D15 checker cases remain an unchanged baseline, and the added, separately labelled controls explicitly exercise TOML recursion and node limits in otherwise usable carriers and provider manifests, including unrelated fields. They record reference and product outcomes separately. The product's bounded parser errors map to existing refused/parse or link-manifest-unusable/parse dispositions; the plan no longer assumes unconditional equality between tomllib and the bounded product implementation. This describes a local parser execution limit rather than changing TOML syntax or adding a refusal code.

The JSON controls require equality at and beyond the shared byte, depth and integer bounds and on duplicate keys, floats, negative zero and non-scalar escapes. The revised body qualifies the retained phrase “No case is invented”: it applies to the baseline reference cases, while differential controls are explicitly additional. The lead's tomllib probe results are supplied context, not results rerun by this reviewer. Fixtures should remain within tomllib's workable depth, as the stated 128-level example does, so the differential result is meaningful rather than an unhandled reference RecursionError.

**B3BA2-R1-RF-2 resolved.** Vectors now retain metadata/content access records and the checker cases' notObserved/notRead lists. The WorkspaceObservation test adapter records all observation methods; subset and forbidden-path checks complement final-output equality. The output-preserving forbidden-access mutation directly addresses the previous gap. This preserves the reader/core safety assertions rather than assuming B3-b2a's separate walker tests cover them. Logical marker/listing calls must be mapped consistently to reference path observations in the adapter; the plan does not require identical internal call ordering.

**B3BA2-R1-NBO-1 resolved.** A2-3 step 4 expressly assigns every native charge once, separates reader, member and descent terms, and retains the reader term at n=0. This supersedes section 4.2's older allocation of provider-manifest reads while preserving its full-ledger coverage and validation requirements. The allocation clarification below remains useful for implementation.

## Obligations and composition

The split retains every section-3 obligation left by A1. B3-b2b1 owns the pure decisions, parsers, carrier rows, placement/cap, branch decisions and links over supplied observations. B3-b2b2 owns native observation and custody, actual 6b, operation-handoff binding, scenario composition, complete V3 declaration serialization, both T2 link-map controls and the joint sweep. Item 24's refusal/disclosure rows remain applicable. The accepted supplied-member seam remains at the link stage for its stated test purpose, and is not a production admission bypass.

WorkspaceObservation describes the reference's relevant access families: metadata, bytes, markers and marker kinds, directory children and supplied 6b verdicts. The existing pure custody checks still require their complete ACL/grant, ownership and invocation context; the interface's field summary does not authorize discarding that data or collapsing host/budget failures into absence.

The branch-A trial-walk split preserves SLM-first priority. Readers and provisional placement precede the trial; a failed trial cannot be overridden by later placement, cap or 6b decisions. Final membership precedes links. Branch B's “final member set” means final after placement, cap and 6b verdicts, as the surrounding decision list and native composition require. B3-b2b2 still owns the integrated trial/refusal provenance behavior. Existing cases plus differential controls and access assertions are an appropriate planned baseline; they are not a claim of exhaustive correctness.

## Identity and gates

The process-unique, never-reused ProjectChain identity is a sound way to preserve the accepted retained-root binding after moving chain and observation into Eligible or RegisteredProject. The observation must record the private identity of the actual chain used by 6a; proof construction must require both identity equality and NoRepository, and return a proof borrowing that chain. Identity must survive moves, differ for separately retained roots even at the same spelling, and never be caller-assigned or reused after overflow/reset. Path labels, raw descriptor numbers and movable addresses cannot substitute for it. The same-chain recheck must preserve existing native operations, charges and refusal behavior apart from intentional identity comparison.

The built handoff retains the fenced tracking result alongside the admission/registered chain, so rejecting an unfenced replacement 6a observation as the proof source remains correct. That second observation would not be the one the handoff decided under the fence.

The project_chain.rs change requires A1-2's closure re-pin and equality projection in B3-b2b2. The full native observation cost still belongs in B3-b3a's pinned bound, measured-versus-model validation and under-count controls. The held-out margin remains outstanding until the exact-byte pre-run gate, single blind run and post-run review; workspace margins and failure-to-law consequences remain mandatory. This amendment authorizes no held-out access during implementation and does not claim project completion or qualification.

## Non-blocking observation

**B3BA2-R2-NBO-1:** placement and visible-repository listing now belong to the member term, but can occur when zero members are admitted: a glob-only carrier may scan visible repositories, and excluded candidates still cost placement work. Do not make that entire term proportional only to admitted n. Include these charges at n=0 and derive their dependence on declaring entries and listed population; carry an appropriate zero-admitted-member case into B3-b3a validation. The requirement to assign every charge exactly once already forbids omission, so this is an implementation clarification rather than a remaining plan blocker.

Review used read-only reading, hashing and Git queries, followed by writing the requested review outputs. No Cargo, rustc, tests, builds, lane or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry was read. No panes or delegation were used. Neither repository nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
