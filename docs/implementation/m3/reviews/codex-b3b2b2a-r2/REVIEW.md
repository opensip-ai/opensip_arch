# B3-B2B2A r2 review

Verdict: **ACCEPT-UNIT**. No required findings or non-blocking observations.

Subject manifest: 10,085 bytes, SHA-256 `fc94f6c74527737b4a561131cbcea7bfc154b1847f81defbba59614c3056b496`. All 42 members match their sizes and hashes. Every product-map parent, candidate and archived pin matches. Authority and product-lock pins also match.

Product main is clean at `46c0ebb3e88e4cfaa8d5a1021b3fdcccee2e63a8`; the detached candidate is at that base with the advertised eight modified paths. Architecture HEAD matches `cd0f3e52d554bbbdd093eb7d5bbcb8ad94163bfe`.

## Round-1 finding

**B3B2B2A-R1-RF-1 resolved.** draw_identity uses atomic fetch_update with checked_add. Each successful update returns the prior counter value as the identity; concurrent draws cannot issue the same prior value. At u64::MAX the update fails without advancing or issuing an identity, so exhaustion remains terminal and never wraps. Relaxed ordering suffices for unique allocation; identity does not publish chain contents through the counter.

The production counter remains private and starts at 1. The sole ProjectChain construction calls this allocator and returns the existing ProjectChainRefusal::Io on exhaustion before constructing a chain. The maximum value is reserved as an exhausted state, which is acceptable; using every possible value is not required. Ordinary construction adds no native observation or ledger charge, and no public refusal code is introduced. Revised LD-1 meets A3's invariant rather than relying on infeasibility.

The new control uses a local counter at MAX-2, obtains distinct identities, observes None twice and verifies the counter remains MAX. It never resets or advances the live global counter. The archived allocator-wraps mutation compiles and fails this control when it incorrectly issues MAX; the never-advancing mutation also fails the boundary and retained-binding controls. These are meaningful deterministic checks of the repaired condition. I inspected them and their logs without executing tests.

## Binding, recheck and handoff

The retained binding remains sound. ChainIdentity's value is private, ProjectChain is non-Clone, and the production chain construction has one issuance path. observe_tracking records the identity of inputs.chain. NoRepository::retained requires both NoRepository and explicit identity equality, then borrows that exact chain. A second retained walk or replacement at the same spelling gets a distinct identity. Observation evidence equality cannot authorize a different chain. The original borrowed RootObservation route remains available.

The operation accessor selects only the subject's own admission chain/tracking or RegisteredProject chain/tracking. Existing and added controls cover repository rejection, repeated walks, same-spelling replacement and eligible/fresh-registration handoff paths. The handoff source and its test file are byte-identical to round 1.

LD-2 remains sound: the manual PartialEq compares exactly the original tracking verdict and evidence, keeping identity as a separate binding condition. recheck_tracking and its callers preserve their native operations, charges and refusal behavior. The inspected admission, registered/current and installation-read sites re-observe their existing retained chain/inputs. git_tracking.rs is byte-identical to round 1; the r2 allocator change affects chain creation, not a recheck's observation sequence. LD-3 appropriately avoids reformatting unrelated base bytes.

## Session

The session implementation is unchanged from round 1. begin checks environment, global sources and system sources once, caches an ordinary shared-source refusal without sampling W's device, and otherwise samples that device once. observe then invokes the unchanged per-member layout and preserves gitlinks, ordinary refusal values, host-I/O propagation and budget failures. observe_members remains the compatibility wrapper over one begin and each requested observe, preserving its former order and charges, including empty input.

The existing decided config/environment/index and capture paths retain the non-latching discipline. A session can supply the accepted core's per-candidate requests without forcing later-member observations after branch A refuses. The native integration still owns when to begin the session and must preserve trial/placement/cap priority. The session-versus-wrapper test establishes the current wrapper relationship; preservation against the pre-refactor algorithm is additionally supported by the inspected extraction and retained B3-b1 controls.

## Census and evidence

An independent structural comparison reproduces the equality projection: both census files change only closure/2's bytes and SHA-256. Every candidate closure pin hashes to its source. Census rows, predictions, constants and held-out standing are unchanged; the margin remains outstanding. The unit adds no paths and therefore needs no additive file-inventory successor.

Archived suite logs have equal sets of 14 pre-existing failures. Aggregate passes increase from 1,146 to 1,151 across two suites, substantiating five new passing tests. This is an equal-failure comparison, not an entirely green security suite. Focused logs report 38 git_tracking passes and 53 discovery/handoff passes. Archived warning-denied Clippy, formatting, vector checks, FW-01, storage/census controls, census --check, environment, operability and design verification report success. They were inspected rather than rerun.

All six mutation logs show compilation followed by relevant behavioral failures: ignored identity, ignored tracking verdict, non-advancing identity allocation, wrapping allocation, identity included in evidence equality, and ignored shared-source refusal. The equality mutation exercises the deliberately equal evidence observations of distinct chains; the separate retained constructor still rejects their cross-pairing.

The only executable check run by this reviewer was the expressly permitted operability source check in the candidate worktree: passed, 114 rows, no findings. No Cargo, rustc, tests, builds, lane, census tool or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry/store/overlay was read. No panes or delegation were used. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.

Acceptance covers this session/binding unit. Native observation, composition and production use remain B3-b2b2b; T2 controls, later cost/margin gates and qualification remain outstanding.
