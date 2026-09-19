# Independent bounded review — typed platform boundary 123 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. Scope: the delta of frozen `platform-boundary-checkpoint-123` over frozen 121 —
`trust.rs` and two existing corpora — as closure of my carrier119 I-1, I-2 and D-2, plus the bounded R-3
regression. Capture 121 F-1/F-2 are out of scope (124). No cumulative, OS or release qualification, no unit
selection. No frozen/selected/product edit; scratch builds with dedicated target directories; no commit,
push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,182,208 bytes, SHA-256 `1b2ce4bc582625b0f8972bc28b69ffd89e67776a35bfc1523534fa9acd30d7c0` = request and `archive-pin.json` |
| Members | 420/420 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified clean afterwards |
| Product pins | 330/330 equal; none unpinned |
| Parent | this subject names its parent pins `parent-product-inputs.json` (there is no `parent-inputs.json`); they equal **my own** verified 121 extraction; 327 unchanged |
| Fixture provenance | 32 entries, 0 hash mismatches |
| Changed | `trust.rs` (+177/−6), `platform-admission-cases.ndjson`, `profile-signature-cases.ndjson` |

Production delta, complete: a child module `platform_profile` with `AdmittedProfile<'a>(&'a V)` (private
field), `from_verified(&ProfileSetEvidence)`, `value()`, and a `#[cfg(test)]` `unsigned_fixture` that checks
the metadata limit and `profile_shape`; `platform_decision` takes `AdmittedProfile`; `kernel_release_parts`
returns `None` above 256 bytes before splitting; the single production call site wraps the verified evidence.

## 2. Evidence

Scratch build: security **72 passed / 0 failed**.

**Typed invariant, tested as compile outcomes** (never counted as kills):

| Attempt from production code | Result |
|---|---|
| pass the raw `&V` as before | does not compile |
| construct `AdmittedProfile(&v)` outside its module | does not compile |
| call the test-only constructor | compiles under `cargo test`, **does not compile in a non-test build** (`E0599`) |
| replace `profile.envelope.payload` *before* `from_verified`, inside the same parent module | **compiles** — see F-1 |

**Mutation** (baseline green, all compiled): Linux bound removed / 257 / strict `>= 256` — killed; Shape
checked after CorePin — **killed** (this was my surviving 119 mutant; the nine genuinely signed malformed
profiles do it); test constructor without the shape gate — killed. Survivors: bound counted in scalars
(**equivalent**: any string over 256 bytes with at most 256 scalars is non-ASCII and fails the grammar
anyway) and test constructor without the metadata limit (test-only; the oversize fixture also fails shape).

**R-3, more boundaries, near-valid method** (`probes/gen_nearvalid_r3.py`: one deletion or one replacement
from a 13-value pool anywhere in a *valid* input, `catch_unwind` around every call):

| Boundary | Cases | Panics | Still accepted |
|---|---|---|---|
| `admit` (both root schemas) | 2,282 | **0** | 59 admitted |
| `propose_recovery` (record and observation are unsigned caller inputs) | 280 | **0** | 58 proposed |
| `verify_profile_set` (envelope mutations, valid stored body) | 238 | **0** | 0 |

The owner's 1,606-case profile/observation regression covers the boundary that did panic in 119.

## 3. Closure

| 119 finding | Status |
|---|---|
| **I-1** `platform_decision` safe only by convention | **Closed for callers outside the module; narrowed, not eliminated, inside it** (F-1). The 98 panics and 704 unshaped admits are no longer reachable through any constructor. |
| **I-2** unbounded kernel-release reflection | **Closed.** Byte bound before splitting, identical to reviewed 122; all 31 of my 122 probes are in the corpus (my report said 32; 31 is right — corrected in a 122 addendum). Derived maximum refusal 303 characters, inside `BoundedText`. |
| **D-2** Shape-before-CorePin unpinned | **Closed** — mutant killed by genuinely signed malformed profiles. |
| **R-3** | **Still open, as the owner says.** Bounded evidence only; see F-2 for where I would look next. |

## 4. Findings

- **F-1 (low–medium) — the invariant is module-level, not type-level.** `AdmittedProfile` can only be
  built from a `ProfileSetEvidence`, but `ProfileSetEvidence { envelope, core_pin }` and
  `EnvelopeEvidence.payload` are ordinary fields visible throughout `root_payload`. I checked that
  same-module production code can assign `profile.envelope.payload = …` between verification and
  `from_verified`, and it compiles. Nothing does this today, and `verify_profile_set` is the only place
  that constructs the struct — so this is the same "by convention" property, one level up and much
  smaller. To finish it: move `ProfileSetEvidence` (fields private, read-only accessors) into the child
  module with `verify_profile_set` as its only constructor. The same applies to `RevocationEvidence` →
  `observe_revocation`, whose `unwrap()`s rely on `revocation_shape`: in my monotone113 probe I rewrote
  that evidence's payload from a test in the same module without any obstacle.
- **F-2 (R-3, concrete next gaps).** Zero panics in 2,800 further near-valid cases is encouraging and
  bounded. What remains unprobed because it needs re-signing: near-valid **stored bodies** for
  revocation, recovery-epoch and root-chain links (a mutated body invalidates its signatures, so the
  carrier refuses before the payload code runs). The owner's public test-only quorum seeds, already used
  for the nine signed malformed profiles, make this feasible: sign near-valid bodies for each kind and run
  them through `verify_revocation`, `propose_recovery` and `verify_root_chain`. Those are the paths with
  `unwrap()` after a shape gate (`verify_revocation` l.≈4690, recovery `issuedAt`, chain root text), i.e.
  the same pattern that produced the 119 panics.
- **F-3 (note, shared with the reference) — recovery does not type-check four record members.** Of the
  58 near-valid recovery inputs that are still proposed, 56 replace `record.rootExpiresAt`,
  `revocationIssuedAt`, `catalogExpiresAt` or `anchor` with arbitrary values (null, `true`, `-1`, `{}`, …)
  or delete them. The 122 reference applies exactly the same 58 (280/280 agreement,
  `probes/nv-recovery-vs-reference.json`), so this is not a Rust divergence. Those members are outside
  `RECOVERY_BOUND_FIELDS` and the writes do not touch the three expiry members, so a malformed value
  survives recovery and is next read by the clock kernel. Decide in the reference whether recovery should
  refuse a record whose clock members are malformed.

## 5. Bounded verdict
**123: reviewed, no blocking finding. carrier119 I-2 and D-2 are closed; I-1 is closed against every
external and constructor route and reduced to a same-module discipline (F-1); R-3 remains open with a
concrete next step (F-2).** Not approval of the signed-security group, capture, Linux execution, or any
cumulative, OS, release or selection standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.diff`,
`probes/mutation.{py,json,log}`, `gen_nearvalid_r3.py`, `nv-*.ndjson`, `nv-results.txt`,
`nv-still-proposed.txt`, `nv-recovery-vs-reference.json`, `rust_probe*.rs.txt`, `hashes.txt`.
