# Independent bounded review — admitted root input seal 132 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `root132-20260918-REQUEST.md`. Scope: the delta of frozen `root-input-seal-checkpoint-132` over frozen 130 —
`crates/security/src/trust.rs` only — as (i) the **root-input part** of my evidence128 F-1 and (ii) the record129
T-1/T-2 test gaps. As the owner asks, I keep this narrowed correction distinct from cumulative closure of 128 F-1:
`EnvelopeEvidence`, `SignatureEvidence`, `QuorumReport`, `RootChainEvidence`, `RecoveryProposal` and
`ConditionalPlatformEvidence` are **not** sealed here (135/136). No clock adapter, production producer, OS, release
or cumulative standing. No frozen/selected/product edit; scratch builds, dedicated target dirs; no commit, push or
delegation. Test-only keys have no authority.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,110,556 bytes, SHA-256 `610c8d8001381e5c1efbb992250872c7edd4c286e3610473868806217700f590` = request and `archive-pin.json` |
| Members | 399/399 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 130 extraction (330/330); 329 unchanged; only `trust.rs` differs |
| Host pins | host81 receipt: 210 sources, all equal the product pins |

## 2. What changed (complete diff read, and classified mechanically)
`ValidatedRootPayload { value, canonical, digest, schema }` and its only constructor `admit` moved into private child
`admitted_roots`; fields private; accessors `value() -> &V`, `canonical() -> &[u8]`, `digest() -> [u8;32]`,
`schema() -> u8`; no `Clone`/`Default`/constructor/`&mut`. `probes/delta_equivalence.py`:
- `admit` body **character-identical** to 130 under my own normalisation (4,192 characters; the owner's 4,268 uses a
  different normaliser — both say identical);
- of 36 diff hunks, 20 are pure accessor substitutions under normalisation and the other 16, read one by one, are the
  module scaffolding, the moved function, `&root.value` → `root.value()` spellings my normaliser does not fold,
  two owned copies that are now explicit (`anchor.canonical().to_vec()`, `link.root.value().clone()` in a test), and
  the one new test. No predicate, order or error mapping changed.

## 3. Evidence

**Owner checks, fresh scratch:** 80/80 security tests; strict workspace Clippy clean. Owner's six compile-fail
clients: one error each in the inserted line. Owner's five mutants: report read (exit 101 each, source hashes given).

**My 128 forgery, re-tried.** Both routes that produced seven genuine sub-threshold `ProfileSetEvidence` values on 128
are now refused **by the compiler**: a struct-literal root handed to the sealed verifier (E0451) and
`root.value = forged` on an admitted root (E0616). So is the workaround named in the request — an inherent
`impl ValidatedRootPayload` written in the parent that forges `Self` (E0451) or lends `&mut value` (E0616) — and nine
further clients: digest write, destructuring move, functional-update literal from an admitted root, `Default`,
`Clone`, `value()` bound as `&mut`, assignment through `value()`, a sibling child module reading a field, a sibling
child module forging. **13/13 rejected, each with exactly one error inside my line.** With the root sealed, every
input of `verify_profile_set` / `verify_revocation` is now either a sealed value or raw external data the verifier
itself checks; I could not construct the 128 effect by any remaining parent-module route.

**What still compiles — the owner's stated residue, confirmed:** payload write on `EnvelopeEvidence`,
`QuorumReport.state = Met`, widening `SignatureEvidence` (`valid_before_revocation.insert`, `required = 0`),
rewriting `RootChainEvidence.accepted_version`, and (harmless) `mem::swap` of two admitted roots.

**No semantic drift — all retained corpora byte-identical on 132** (inputs copied unchanged; outputs compared with
`cmp`): signed-body R3 revocation 302 / recovery-epoch 242 / root-chain link 1,302 / possession 9; my re-signed
profile-set corpus 1,782 (incl. 98,644 consumer decisions); my 11,225-record admission corpus with challenge,
entropy-draw and apply columns. Six of six files identical to the 128/129 runs.

**Mutants** (9, all compiled, baseline green): **9/9 killed.** The three 129 variants the owner did not try —
projection swapping `evalHighWater`/`lastAccepted`, projection taking every expiry from `rootExpiresAt`, and the
record bound *weakened* to 50 MB rather than removed — are all killed by the new test (its five timestamps are
distinct and its oversize value is 5,000,001 bytes, so it discriminates both). The six root mutants (traversal bound,
closed member set, reader declaration, schema-2 digest under the schema-1 domain, stored value ≠ admitted input,
`schema()` constant) show the moved `admit` kept its kill power.

## 4. Closure

| Item | Status |
|---|---|
| evidence128 **F-1, root-input route** | **Closed** — compiler-refused, 13 clients, my original forgery included |
| evidence128 F-1, remaining types; F-2 consumer outputs | **Open**, as the owner states (135/136) |
| record129 **T-1** projection anchor unpinned | **Closed** — non-null anchor, five distinct non-null timestamps incl. a year-9999 expiry; owner's and my two variants killed |
| record129 **T-2** `admit`'s own bound unpinned | **Closed** — direct oversize → `Limit` before `Shape`; removal and weakening both killed |
| record129 F-1 (projection leaves the seal as an untyped `V`) | **Open**, acknowledged by the owner ("no claim that untyped cloned clock projection confers authority") |

## 5. Findings
- **N-1 (note, carried) — sealed roots sit inside unsealed aggregates.** `RootChainEvidence.links[*].root` holds
  sealed `ValidatedRootPayload` values, but the surrounding struct (`accepted_version`, `last_accepted_issued_at`,
  the `links` vector itself) is still a plain literal: a parent client can drop, reorder or re-version links made of
  genuine roots. This is inside the residue the owner lists; I name it so that 136 treats *composition* as well as
  fields (a vector of sealed items is not a sealed chain).
- **N-2 (note) — accessor cost.** `canonical().to_vec()` and `value().clone()` now copy at two call sites where 130
  moved or borrowed. Both are bounded by the 5 MB admission budget; no behavioural effect. Worth remembering when the
  production producer is written, so that copies of an admitted root are not mistaken for admitted roots — the
  README already says so.

No new defect found in the delta.

## 6. Unresolved limits
Privacy is a compile-time property of this source tree on this toolchain; same-child-module code is inside the
boundary by construction. macOS host only. No production caller exists, so "cannot be bypassed" is a statement
about the 17 clients I tried plus the owner's six, not a proof over all future code.

## 7. Bounded verdict
**132: reviewed, no finding against the delta. The root-input forgery I demonstrated on 128 is now refused by the
compiler along every route I could construct (13/13), `admit` is character-identical, all six retained corpora
reproduce byte-for-byte, record129 T-1 and T-2 are closed, and 9/9 of my mutants are killed. This closes the
root-input part of evidence128 F-1 only; envelope, signature, quorum, chain, recovery and platform outputs remain
open by the owner's own statement and must be sealed before production wiring.** Not approval of callers, custody,
current authority, OS, dependencies, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.diff`, `owner/`,
`probes/{delta_equivalence.py,delta-equivalence.json,compile_boundaries.py,compile-boundaries.json,compile-boundaries.log,compile-*.stderr,mutation.py,mutation.json,mutation.log}`,
`io/{r3-main,r3-possession,profile,records}/`, `hashes.txt`.
