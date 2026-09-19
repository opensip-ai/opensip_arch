# Independent bounded review — aggregate evidence boundaries 136 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `aggregate136-20260918-REQUEST.md`. Scope: the delta of frozen `aggregate-seal-checkpoint-136` over frozen
135 — `crates/security/src/trust.rs` only — sealing `RootLinkEvidence`/`RootChainEvidence`,
`RecoveryProposal`/`RecoveryChallengeProposal` and `ConditionalPlatformEvidence` with their producers: the aggregate
portions of my evidence128 F-1/F-2 and root132 N-1. **Privacy, not admission**: nothing here authenticates where an
observation came from, grants write or current authority, or establishes custody. record129 F-1 (typed clock adapter)
is separate. No frozen/selected/product edit; scratch builds, dedicated target dirs; no commit, push or delegation.
Test-only keys have no authority.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,113,792 bytes, SHA-256 `ba673497557db03384edcc4e21a044b60d8d7635f02a18155e5d5eb6be4e3752` = request and `archive-pin.json` |
| Members | 397/397 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 135 extraction (330/330); 329 unchanged; only `trust.rs`; no fixture change |
| Host pins | host84 receipt: 210 sources, all equal the product pins |

## 2. What changed (complete diff read)
Three private owner modules — `verified_root_chains`, `admitted_recovery_proposals`, `admitted_platform_decisions` —
hold the five structs and `verify_root_chain`, `propose_recovery`, `issue_recovery_challenge`, the injectable
`issue_challenge_with_draw` (now a **private** `fn`), `evaluate_platform`. Getters by shared reference or copy;
`links() -> &[RootLinkEvidence]`; consuming `into_profile`. Tests reach the draw seam only through a `cfg(test)`
wrapper. `probes/delta_equivalence.py`: all five producer bodies equal 135 under my normaliser **except inserted
`super::` module hops** (2, 3, 0, 2, 1 insertions; listed in the JSON). No predicate, order or error mapping changed.

## 3. Evidence

**Owner checks, fresh scratch:** 80/80 security tests; strict workspace Clippy clean. Owner's twelve compile-fail
clients read; privacy checks, as labelled.

**Composition and escape routes** (`compile_boundaries.py`, 26 clients, none copied from the owner's).
**23 must-fail — all 23 rejected**, each by a privacy/borrow/move error inside my line:
- *chain composition with genuine sealed parts* (root132 N-1): re-version (E0616); **drop** the last link; **reorder**;
  **splice** the genuine links of another chain under this anchor (`{ links: b.links, ..a }`); rebuild from the
  read-only slice (needs `Clone` on a link — absent); reorder through `links()` (E0596); a link literal assembled from
  a *genuine* sealed root and *genuine* quorum reports (E0451); parent-written inherent impls that re-version or build
  a chain from genuine links;
- *proposals*: writes/`floor_lowered` replaced beside a genuine envelope (compiled on 135); write through `writes()`;
  proposal literal with a genuine envelope and caller-chosen writes; challenge literal with arbitrary pending
  (compiled on 129);
- *entropy seam*: the injectable draw from the parent is **private** (E0603); the `cfg(test)` wrapper does not exist
  in a release build (E0425);
- *platform*: literal with a forged decision beside a genuine profile (compiled 128–135); decision or observation
  replaced; refusals cleared through `decision()`; reuse after `into_profile` (E0382);
- sibling-module field read; `Clone`; `Default`.

**3 compile, and mark where privacy ends:** `mem::swap` of two verifier-made chains; a free-standing
`PlatformDecision` literal (it can no longer be *attached* to evidence); and the record129 F-1 residue (the six-member
clock projection is an untyped `V`) — open by the owner's own statement.

**No semantic drift — all eight retained corpora byte-identical on 136.** Harness-only adaptation, shown in
`probes/adapted/ADAPTATION.diff` (4 lines): `.floor_lowered` → `.floor_lowered()`, `.accepted_version` →
`.accepted_version()`, `&p.writes` → `p.writes()`. Signed-body R3 302 / 242 / 1,302 / 9; profile-set 1,782
(+ 98,644 decisions); records 11,225; clock 40,000; signed edge recovery 11.

**Behavioural mutants** (9, all compiled, baseline green; stage 1 owner tests, stage 2 my corpora): **6 killed**
(`accepted_version()` = 0, `links()` dropping a link, zeroed `anchor_digest()`, `writes()` returning the bound record,
negated `floor_lowered()`, `pending()` returning the exported challenge). **3 survived both stages** — T-1..T-3.

## 4. Closure

| Item | Status |
|---|---|
| evidence128 **F-1** aggregates (chain, recovery) | **Closed at the privacy layer** — with 132 (root) and 135 (envelope/quorum) every evidence type I named in 128 is now sealed |
| evidence128 **F-2** consumer outputs (`ConditionalPlatformEvidence`) | **Closed** |
| root132 **N-1** composition of sealed parts | **Closed** — drop, reorder, splice, rebuild and re-version are all refused |
| record129 **F-1** `RecoveryChallengeProposal` literal | **Closed**; the untyped clock projection part remains open |
| envelope135 N-1 (which revocation set) | unchanged, semantic, for the future producer |

## 5. Findings

- **T-3 (low–medium) — production's use of the platform entropy draw is unpinned.** Replacing
  `opensip_platform::recovery_nonce` in `issue_recovery_challenge` with a **constant nonce** passes all 80 tests and
  all my corpora: the only test of the production path checks that the exported and pending nonces are equal, are
  64 hex digits and admit as pending — all true of a constant. Sealing made the seam private, which is right; but the
  one line that chooses the *real* source is exactly what nothing checks, and here a wrong choice is replayable
  challenges rather than a missing flush. Same family as 106 N-1 / 126 N-1. Minimal pin: issue two production
  challenges for the same record and observation and assert the nonces differ (and differ from the fixture constant
  `ab…`); that is probabilistic only at 2⁻²⁵⁶.
- **T-1 (low) — `RootLinkEvidence::continuity()` is unpinned.** Returning the *possession* report instead survives:
  the chain test asserts `continuity.message == possession.message`, which holds for either report, and never
  distinguishes them by root digest or role. Assert `continuity().root_digest()` = the *previous* root and
  `possession().root_digest()` = the link's own root.
- **T-2 (low) — `ConditionalPlatformEvidence::observed()` is unpinned.** Returning the profile payload survives; the
  test only asserts `observed != Null`. Assert equality with the supplied observation.
- **N-1 (note, scope)** Sealing proves *who constructed* a value, not that its inputs were admissible observations:
  `evaluate_platform` still takes a raw `&V` observation, `propose_recovery` a raw observation and revoked set,
  `verify_root_chain` raw `evaluation_time`/`wall`/revoked/readers. The owner says so ("does not authenticate raw
  observation provenance"); I repeat it because after 132/135/136 those raw parameters are the entire remaining
  attack surface of this module, and they are what the production producers must bind.

No defect found in the sealing itself.

## 6. Unresolved limits
Compile-time property of this tree and toolchain; code inside each owner module is inside its boundary (all three
`use super::*`, so the modules can *read* each other's public-to-parent API but not each other's fields — confirmed
by the sibling client). No production caller exists; macOS host only; "cannot be bypassed" means the 26 + 12 clients
tried.

## 7. Bounded verdict
**136: reviewed, no finding against the sealing. Every aggregate route I could build — including dropping,
reordering, splicing and re-versioning chains made of genuine sealed roots, substituting proposal writes beside a
genuine envelope, attaching a forged platform decision, and reaching the entropy injection seam — is refused by the
compiler (23/23); producer bodies are identical up to module hops; all eight retained corpora reproduce byte-for-byte
with a four-line accessor adaptation. With 132 and 135 this completes the privacy layer of evidence128 F-1/F-2.
T-3 (production entropy source unpinned — a constant nonce passes) should be closed before the challenge path gains
a caller; T-1/T-2 are two getters no test distinguishes.** Privacy is not admission: not approval of observation
provenance, revocation currency, custody, write authority, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.diff`, `owner/`,
`probes/{delta_equivalence.py,delta-equivalence.json,compile_boundaries.py,compile-boundaries.json,compile-boundaries.log,compile-*.stderr,adapted/,mutation.py,mutation.json,mutation.log}`,
`io/{r3-main,r3-possession,profile,records,clock}/`, `hashes.txt`.
