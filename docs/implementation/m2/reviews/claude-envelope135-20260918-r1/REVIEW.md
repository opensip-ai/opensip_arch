# Independent bounded review — envelope / quorum seal 135 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `envelope135-20260918-REQUEST.md`. Scope: the delta of frozen `envelope-seal-checkpoint-135` over frozen 134 —
`crates/security/src/trust.rs` only — i.e. the **envelope/quorum layer** of my evidence128 F-1: `SignatureEvidence`,
`QuorumReport`, `EnvelopeEvidence` and their producers in the sealed child `verified_envelopes`. The aggregates
(`RootChainEvidence`, recovery proposals, `ConditionalPlatformEvidence`) are 136, not this subject. No current
revocation, custody, OS or production-authority claim. No frozen/selected/product edit; scratch builds, dedicated
target dirs; no commit, push or delegation. Test-only keys have no authority.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,118,036 bytes, SHA-256 `d21360440b4f8d0bc199f1ce45371a3ee01ddb83a622a7e1655076118f33434b` = request and `archive-pin.json` |
| Members | 406/406 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 134 extraction (330/330); 329 unchanged; only `trust.rs` differs; no fixture changed |
| Host pins | host83 receipt: 210 sources, all equal the product pins |

## 2. What changed (complete diff read)
Three structs and `verify_quorum`, `verify_envelope`, `filter_revoked`, `filter_envelope_revoked` (+ a `cfg(test)` raw
state helper) move into `verified_envelopes`; fields private; views by shared reference or copy
(`valid() -> &BTreeSet`, `payload() -> &V`, `state() -> &QuorumState`, digests by value) and one consuming
`into_quorum(self)`. No `Clone`, `Default`, constructor or `&mut`. Consumers change mechanically to the views.
`probes/delta_equivalence.py` (my normaliser): `filter_revoked` and `filter_envelope_revoked` are character-identical
to 134; `verify_quorum` and `verify_envelope` differ **only** by inserted `super::` hops (1 and 6 insertions, listed
in `delta-equivalence.json`). No predicate, order or error mapping changed.

## 3. Evidence

**Owner checks, fresh scratch:** 80/80 security tests; strict workspace Clippy clean. Owner's ten compile-fail
clients: one error each; labelled by the owner as privacy checks, not runtime kills — agreed.

**Escape routes I tried** (`compile_boundaries.py` + `_r2.py`, 23 clients). **19 must-fail, all rejected**, each by a
privacy/borrow/move error inside my line: the three writes that still compiled on 128/132 (envelope payload, quorum
`state = Met`, widening `SignatureEvidence` — E0616); report, envelope and signature-evidence literals (E0451),
including an envelope **with a caller-chosen quorum type** `EnvelopeEvidence<u8>`; parent-written inherent impls that
forge a report, lend `&mut valid`, or **re-wrap an envelope around another quorum** via a generic `impl<Q>` (E0616);
destructuring; `insert` through `valid()`; assignment through `payload()`; `state()` bound as `&mut`; `Clone`;
`Default`; reuse of an envelope after `into_quorum` (E0382 — the consumption is real); a sibling child module reading
a field; and the `cfg(test)` raw-state helper from non-test code (absent in release, E0425).
(Three r1 clients failed only on *name resolution*, because `SignatureEvidence`/`filter_revoked` are not imported
into the parent outside tests; I re-ran them with full paths so that the rejection is the privacy error — r1 outputs
kept under `probes/r1/`.)

**What compiles, and why it is not a privacy hole:** `mem::swap` of two verifier-made reports; and
`filter_revoked(evidence, &BTreeSet::new())` — see N-1. The three 136 aggregates are still writable, as the owner says.

**No semantic drift — all eight retained corpora byte-identical on 135, with no harness adaptation at all:**
signed-body R3 revocation 302 / recovery-epoch 242 / root-chain link 1,302 / possession 9; re-signed profile-set
1,782 (+ 98,644 consumer decisions); record admission 11,225 (admission, challenge, entropy draws, apply); the 134
clock corpus 40,000; my 11 genuinely signed edge recovery epochs. Root chain, recovery, profile and revocation — the
affected callers the request names — are all covered by these.

**Behavioural mutants** (7 valid + 1 harness error of mine, not counted — the threshold line occurs twice): **7/7
killed** — `preimage_digest()`/`stored_digest()` swapped, `QuorumReport::root_digest()` returning the message,
`required()` returning 0, state computed before revoked keys are removed, revoked keys retained, payload nulled
while filtering. The views return the right members and the moved producers kept their kill power.

**Owned buffers.** `stored()` returns `&[u8]` borrowed from the evidence; `filter_envelope_revoked` and `into_quorum`
move rather than copy; nothing hands out a reference that outlives its owner (the borrow checker rejects my
use-after-`into_quorum` client). I found no new clone of `stored` on a hot path in the diff.

## 4. Closure

| Item | Status |
|---|---|
| evidence128 **F-1, envelope/quorum layer** | **Closed** — 19/19 clients rejected, including the generic re-wrap and caller-chosen-`Q` routes |
| evidence128 F-1 root input | closed in 132, retained upstream (my 132 clients still fail: root types unchanged in this diff) |
| evidence128 F-1/F-2 aggregates; root132 N-1 composition | **Open** → 136 |
| record129 F-1 untyped clock projection | open, separate |

## 5. Findings
- **N-1 (note; semantic, not privacy) — the type does not say *which* revocation set was applied.**
  `QuorumReport` means "filtered", not "filtered with the current revocation population": a parent-module caller can
  obtain a `Met` report, or a whole `EnvelopeEvidence<QuorumReport>`, by filtering with an empty set, and it is
  indistinguishable by type from a correctly filtered one. This is the documented TCB input ("revocation population
  … remain TCB inputs") and predates 135; I record it because sealing makes every *other* route impossible, so this
  becomes the one remaining way to a too-generous quorum, and the future production producer is where it must be
  bound (e.g. the verifier taking a sealed revocation observation rather than a raw set). Out of scope here by the
  owner's own statement.
- **N-2 (note)** `SignatureEvidence` and `filter_revoked` are reachable from the parent only by full path in
  non-test builds, which is good hygiene; `verify_quorum` is `cfg(test)`-imported. When the production producer is
  written these gates will be lifted — that is the moment to re-run the client suite.

No defect found in the delta.

## 6. Unresolved limits
Compile-time property of this tree and toolchain; same-child-module code is inside the boundary. No production caller
exists. macOS host only. "Cannot be bypassed" means the 23 + 10 clients tried, not a proof over future code.

## 7. Bounded verdict
**135: reviewed, no finding against the delta. The envelope/quorum layer of evidence128 F-1 is closed: every
construction, mutation, accessor, parent-inherent-impl, generic re-wrap and consumed-value route I could build is
refused by the compiler (19/19), producer bodies are identical up to module hops, all eight retained signed and
record corpora reproduce byte-for-byte without any harness change, and 7/7 behavioural mutants are killed. The
aggregates remain open for 136; N-1 (which revocation set) is a semantic obligation for the future producer, not a
privacy defect.** Not approval of callers, revocation currency, custody, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.diff`, `owner/`,
`probes/{delta_equivalence.py,delta-equivalence.json,compile_boundaries.py,compile_boundaries_r2.py,compile-boundaries*.json,compile-boundaries*.log,compile-*.stderr,r1/,mutation.py,mutation.json,mutation.log}`,
`io/{r3-main,r3-possession,profile,records,clock}/`, `hashes.txt`.
