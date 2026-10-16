# B3-B2B2A r1 review

Verdict: **REQUIRED-FINDINGS**.

Subject manifest: 9,841 bytes, SHA-256 `366efb40dbd2071a87c096d111e41635ee4aae20c6fd746647bade929a0f0c21`. All 41 members match their byte counts and hashes. Every product-map parent, candidate and archived pin matches. Authority and product-lock pins match. Product main is clean at `46c0ebb3e88e4cfaa8d5a1021b3fdcccee2e63a8`; the detached candidate is at that base. Architecture HEAD matches `cd0f3e52d554bbbdd093eb7d5bbcb8ad94163bfe`.

## Required finding

**B3B2B2A-R1-RF-1 (P2): The identity allocator wraps, contradicting the accepted never-reused invariant.**

Location: `crates/security/src/custody/project_chain.rs:488`, and LD-B3B2B2A-1.

The single construction site uses `NEXT_CHAIN.fetch_add(1, Ordering::Relaxed)`. Atomic integer addition wraps, so identities eventually repeat. A retained old chain and its observation can then share an identity with a newly constructed chain; the retained proof constructor compares only that identity and NoRepository. The absolute “another chain gets none” claim no longer follows at that boundary.

Reaching this boundary operationally is extraordinarily remote. Nevertheless, A3 explicitly requires a private, never-reused identity, and its acceptance calls for an allocator that cannot wrap/reset into reuse. LD-1 substitutes an infeasibility assumption for that accepted invariant. The current constant-identity mutation proves rejection of immediate reuse, but does not test exhaustion.

Required: stop identity issuance before reuse with a checked/non-wrapping allocator. A new public chain-refusal code is not necessary: an internal fail-stop at the unreachable boundary can preserve every ordinary 6a decision and charge while preventing an invalid proof from being minted. Add a deterministic near-maximum allocator control using a local/test counter; do not require 2^64 walks or reset the live global counter. Refresh changed closure/product pins and evidence. This finding is established by source inspection; no exhaustion probe or test was run here.

## Binding and recheck

Apart from exhaustion, the binding is correctly implemented. ChainIdentity has a private field, one issuance site and a process-wide atomic; ProjectChain remains non-Clone. observe_tracking records inputs.chain.identity(). NoRepository::retained explicitly checks both the tracking verdict and that identity. Its returned proof borrows the supplied chain. Neither matching labels nor observation PartialEq can substitute for this identity check.

The operation accessor pairs only the subject's own admission chain/tracking or RegisteredProject chain/tracking. The new controls cover different retained walks of the same directory, a replacement repository at the same spelling, a repository's inability to yield a proof, and both eligible/fresh-registration handoff paths. These address B3B1-R2-RF-1 within the allocator's non-exhausted domain. The original borrowed RootObservation route remains valid.

**LD-2 is sound.** The manual PartialEq compares exactly the pre-existing tracking verdict and evidence fields. recheck_tracking's native pass and comparison therefore retain their previous semantics. Inspected call sites use the admission's retained chain, the registered/current retained chain, or the same installation-read inputs; none re-walks a chain merely for a recheck. The identity is deliberately a separate proof-binding relation, and retained checks it independently of evidence equality. Adding the field changes internal representation, while ordinary 6a operations, charges, evidence order and refusals remain unchanged.

LD-3's formatting treatment avoids unrelated base formatting changes and does not alter the reviewed behavior.

## Session

The session extraction preserves the old source-check order: environment, global sources, system sources, then one W-device sample if they pass. An ordinary shared-source refusal is cached as a member verdict and skips that sample, as the former batch return did. Session observe calls the unchanged member_layout and preserves gitlinks, member-refusal translation, host-I/O propagation and budget propagation. observe_members begins a session once and collects one verdict per input member, including the former empty-input source/device behavior.

The non-latching discipline remains intact: environment/config/index decisions and ordinary capture refusals stay outside charged scopes; genuine host I/O and exhaustion fail the pass. The per-candidate session allows the accepted core to stop branch A without observing later members. Native integration must continue to begin the session at the appropriate 6b stage, after trial/placement/cap priority is decided.

The new session-versus-batch charge comparison is useful wrapper coverage, but both routes now share the same implementation. Unchanged pre-refactor charging is additionally supported by the inspected extraction and the retained B3-b1 controls, rather than by an independent old-code oracle in that comparison.

## Closure and evidence

An independent structural comparison reproduces the equality projection exactly: both census files change only closure/2's byte count and SHA-256. Every candidate closure row matches its source. Census rows, predictions, model constants and held-out standing are unchanged; the margin remains outstanding. No new paths are added, so the stated lack of an additive file-inventory successor is consistent with this diff.

Archived base/candidate security logs have equal sets of 14 failing test names. Aggregate passes rise from 1,146 to 1,150 across two suites, supporting four new passing tests. This is not an entirely passing security suite. The focused logs report 37 git_tracking passes and 53 discovery/handoff passes. Archived warning-denied Clippy, formatting, vector checks, FW-01, walk-storage and census controls, census --check, environment, operability and design verification report success. They were inspected, not rerun.

All five mutation logs compile and fail behavioral tests. They meaningfully cover ignored identity, ignored tracking verdict, immediate identity reuse, altered evidence equality and ignored pass refusal. The equality mutation exercises the intentionally equal observations of distinct chains; it does not claim that such a pair is a production recheck. The allocator-boundary case in the required finding remains absent.

The only executable check run by this reviewer was the expressly permitted operability source check in the candidate worktree: passed, 114 rows, no findings. No Cargo, rustc, tests, builds, lane, census tool or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry/store/overlay was read. No panes or delegation were used. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory. No non-blocking observations are added.
