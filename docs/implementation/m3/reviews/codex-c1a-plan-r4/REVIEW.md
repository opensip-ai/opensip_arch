# ACCEPT — C1a implementation plan, round 4

Subject manifest SHA-256: `d2517dc99e696fb3ffe285e17a77c6a60d5a36fab9989d9e6b73fe5d56a8be4b`. All four members match their declared bytes and hashes. Archived r1–r3 remain unchanged. r4 is 36,209 bytes, SHA-256 `73ce52b14a84a8a51a74225ac08ea3f7171fe45d15e7b23ab7a4b17281e9cafe`. Product HEAD is clean at `808ad6476fb848f84e732ee233a47229370081f4`; architecture HEAD is `43402bbc8543b0e4f265bcb4fd482c1c113f562c`.

## Prior findings resolved

- **C1APLAN-R3-RF-1:** The cost model now separates the native 1,023-byte raw-name envelope from the law's 255-scalar segment and 4,096-scalar path limits. Valid UTF-8 envelopes are 1,020 and 16,384 bytes respectively. Classification and escaped-refusal copies are included. Multibyte and raw-name controls plus the restored-255-byte mutant address the underpricing. The actual macOS directory stream's required NUL within a 1,024-byte slice supports the native bound. See the non-blocking synthetic-control note below.
- **C1APLAN-R3-RF-2:** LD-C1A-10, its payload guard and Q4 are explicitly withdrawn. The read phase again reads every extent file to EOF, subject to charged work and the finite attempt envelope. Growth/stale size cannot yield a sealed partial capture. Replacement C1A-T6 controls retain later read-I/O, changed-read, custody and open refusals ahead of step-5 totalBytes. The unsupported observational-equivalence claim is removed; no new law clarification is required for a guard the plan no longer implements.

The full r3-to-r4 diff is confined to the recorded corrections and supporting controls. In particular, the former 8 GiB/100,000-row restriction on the cost optimization is removed: all attempts use the same edge constraint, including walks that ultimately fail semantic bounds.

## Requested decisions

**Fidelity and ownership:** The plan covers items 1, 2, 5 and 6 and allocates their named C1a controls across the four steps. C1b retains Git/member VCS, C1c retains the installed-package read set, and J retains production composition, ephemeral identity draws and public projection. No caller, C1 completion or qualification is inferred.

**Q1 / split:** The split is faithful to C1-T2. Security judges custody, opens and observes descriptors; only host `snapshot.rs` reads source content. Candidate custody takes chunks. Pre-captures have a security opener; the extent walk opens and re-observes through its enumerating retained parent and compares identity/type. Read-count, rewrite and ancestor-replacement controls support the source pin without duplicating the shared extent or custody rule.

**Q2 / ledger and census:** A separate snapshot profile is justified: global `with_limits` cannot supply the required caps, and the discovery profile has the wrong object cap and a separately fixed byte cap. Recipe and derivation precede C1a1's constructor. Charging all operation types before execution, with byte-carrying types also consuming objects or edges, permits a finite conservative optimization. Exact solver arithmetic must preserve an upper bound, including fractional vertices; the planned evidence must prove model coverage and constants before any numerical cap is accepted. A result above the proposed threshold returns to the law, rather than being silently reduced. This acceptance does not assert that the derivation will pass or that any T2 margin holds.

The whole-file census re-pin, explicitly stale receipt, unchanged discovery projection, C1a4 pre-/post-reviewed blind refresh and repeat transitions after a later cap revision follow the accepted precedent. No held-out run was performed or newly authorized in this review.

**Q3 / VCS:** The internal interim refusal is sound for the scoped library. An enclosing Git repository or any admitted D15 member waits for C1b. Only authenticated NoRepository with no members seals the interim schema-2 none observation. The I-complete read lending stays separate from writer authority; I-absent remains gated on E-1/S7b and J2c.

**Other lead decisions:** Shared extent reuse, one reused chunk buffer, caller-supplied private custody, no ambient TMPDIR selection, and the empty read set pending C1c remain appropriate. The finite attempt envelope is an allowance, not a promise that every possible short-read/Interrupted sequence completes; terminal exhaustion and ledger latching remain implementation obligations. In-memory duplicate handling is scoped to fresh, exclusively owned, immutable-per-digest invocation custody, with later consumer verification. Temporary disk capacity remains a separate J/S-OP-8 responsibility, with no preflight implementation claimed here.

**Carrier/sealing:** B1's captured project-carrier input is the correct source of the presence/digest observation. The seven-row join preserves digest, presence, type and exclusion distinctions without importing X2 source bytes. The full canonical snapshot descriptor, not merely inventory bytes, is checked at the law's sealing step 5; the envelope boundary and mixed-error controls preserve that distinction and refusal order. Canonical inventory hashing, uniqueness/order, identity admission and exclusion of operational values remain required.

The proposed sequencing, baseline comparisons, warning-denied Clippy, formatting, vectors, source pins, environment/FW-01 checks, model comparisons and mutations are adequate plan-level gates. Numerical pricing, implementation soundness and corpus results remain subject to their own unit reviews.

## C1APLAN-R4-NBO-1 — Synthetic name boundary

A native macOS stream cannot return a full 1,024-byte name through its 1,024-byte NUL-terminated slice. The planned injected 1,024-byte control is therefore outside the native input contract. When implementing it, charge and retain all injected refusal bytes, or reject at the bounded stream boundary; do not truncate the diagnostic to 1,023 bytes while calling it the complete escaped name. This does not block plan acceptance.

No required findings remain. Review used only file reads, hashing, JSON parsing and Git queries. No build, test, generator, network, delegation or prohibited private-data access occurred. Only this directory's `REVIEW.md` and `review.json` were written; neither repository was edited.
