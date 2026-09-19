# Independent bounded review — carrier/reader corrections 119 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. **Two separate verdicts**, as asked: (A) the 119 delta — signed106 R-1, R-2, the
new anchor-reader defect, 114 N-1, 117 N-1; (B) the inherited, unchanged Linux platform branch and
profile helpers in the same `trust.rs`, plus bounded R-3 probes. Code reading and probes only: no Linux
execution, no OS, target, dependency, current-authority or cumulative approval. No frozen/selected/
product edit; scratch builds with bytecode writing disabled and dedicated target directories; no commit,
push or delegation.

## 1. Subject verification (before extraction)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,135,268 bytes, SHA-256 `ac65c3f4931018364bf633df237630ee75bee5373fdec00ce88c08dd608e41ed` = request and `archive-pin.json` |
| Members | 422/422 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified clean after the work |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 117 extraction; 325 unchanged, 0 added/removed |
| Fixture provenance | 32 entries, 0 hash mismatches |
| Changed | `trust.rs` (+239/−26), `revocation.rs` (+2, comment), `profile-signature-cases.ndjson`, `recovery-cases.ndjson` (117 bytes are an exact prefix; +1 line), `root-chain-cases.ndjson` (2 lines changed, +1) |

---

## A. The 119 delta

### A.1 What changed (read in full)
`EnvelopeReader { root_schemas: [bool; 2], kinds: [bool; 8] }` is a required first argument of
`verify_envelope`; an all-false mask is `ReaderDeclaration`, an unsupported expected kind is
`UnsupportedKind`, and the **verifying** root and the **presented** root (for `kind = Root`) are each
checked with `UnsupportedRootSchema`, all before any signature work. Every current call site passes
`CURRENT_ENVELOPE_READER`; the chain passes `context.readers`. `verify_root_chain` now first rebinds the
already-validated anchor to the chain reader (`AnchorUnsupported`, projected as
`ROOT.SCHEMA_UNSUPPORTED`). `verify_profile_set` is carrier-first, then raw-quorum shortfall, then
shape, core pin, role, revocation filtering.

### A.2 The new anchor finding — confirmed against the composed 116 reference
I asked the reference itself rather than the legacy projected fixture (`probes/anchor_ref.py`):
`Verifier.admit_signed_root_chain` with an **empty** presented chain, for each reader set and each
anchor schema — and the projected `admit_root_chain` alone. Both refuse an unsupported anchor with
`ROOT.SCHEMA_UNSUPPORTED` (stage `root-document` in the composed form) **in both directions**
(schema-1 anchor under a schema-2 reader, and schema-2 under schema-1), and accept the other four
cells. My Rust probe over the same matrix gives exactly that: four `ACCEPT`, four `AnchorUnsupported`
(the all-false reader included; the reference refuses to construct such a Verifier at all).

**This is a genuine admission defect, and one of the corrected fixture lines is an acceptance change,
not a diagnostic one**: `schema2:readers(2,)` — a rotation from a schema-1 anchor to a schema-2 root
under a schema-2-only reader — expected **ACCEPT, acceptedVersion 2** in 117 and expects REFUSE now.
The 116 reference refuses it, so the old expectation was wrong against the reference it claimed;
the correction is in the safe direction. The owner's summary line "no acceptance changes" is true of
the profile fixture only; say so for the chain fixture.

### A.3 R-1 profile precedence — rederived independently
All **228** frozen expectations recomputed by me from `Verifier.admit_signed_profile_set` (116) with my
own class mapping: **0 mismatches** (146 no-active-role and 9 carrier mismatches → `Envelope`; 37 raw
shortfall or no valid signature → `SignatureThreshold`; 24 `CorePin`; 6 post-revocation shortfall; 6
admitted). Then **684 variants of mine** (every case with a wrong pin, with a null pin, and with every
listed signer revoked *plus* a wrong pin): Rust equals the reference class on **684 / 684**. In
particular raw shortfall + wrong pin is `SignatureThreshold` (carrier wins), and met quorum + all
signers revoked + wrong pin is `CorePin` (pin precedes revocation filtering) — in both.

### A.4 Other fixture changes
Recovery: the new case has a **1-second** window at the top of the i64 range and is `PENDING_SHAPE` in
both the fixture and the 116 reference — this is exactly the case I asked for in 114 N-1.

### A.5 Mutation (dedicated target directory, baseline green)
13 mutants: **11 killed, 2 survived, 0 counted compile failures** (one mutant was ill-typed on the
first attempt, recorded as such, and re-run type-correct: killed).
Killed: anchor rebinding removed; anchor bound to the build reader; kind, verifying-root and
presented-root capability checks each removed; empty declaration tolerated; schema-2 slot and
RecoveryEpoch/ProfileSet slot mix-ups; raw-shortfall check removed; revoked signers never filtered;
`AnchorUnsupported` projected as another public refusal.
Survived:
- *links verified under the build reader* — **equivalent in effect**: each link's payload is already
  admitted with `admit(&payload, context.readers)` before `verify_envelope`, and the verifying root is
  the anchor or a previously admitted link. The propagation is defence in depth, not a second gate.
- *core pin compared before shape* — class only (`CorePin` instead of `Shape`); it needs a genuinely
  signed, quorum-met, malformed profile, which no fixture has.

### A.6 Findings — delta
- **D-1 (note)** — record the chain fixture's ACCEPT→REFUSE line as an acceptance change (A.2).
- **D-2 (low, tests)** — one signed malformed-shape profile case would pin Shape-before-CorePin.
- **D-3 (note)** — `EnvelopeReader` is `Copy` with public-in-module fields, and every production call
  passes the all-true constant, so today it restricts nothing; its value is that a restricted reader is
  now *expressible and tested* (stage-1 mask). Host reader selection is, as stated, a separate step.
- 117 N-1 comment: accurate.

### Verdict A
**119 delta: reviewed, no blocking finding. signed106 R-1 and R-2 are closed at this boundary; the new
anchor-reader defect is real, correctly fixed, and agrees with the composed 116 reference on the full
reader × anchor matrix including empty chains; 114 N-1 and 117 N-1 are closed.**

---

## B. Inherited, unchanged code: Linux branch, `profile_shape`, `linux_profile`, `mac_profile`, helpers

### B.1 Reading (complete for these functions)
`upper_uuid`, `lower_hex_width`, `kernel_line`, `kernel_flavor`, `mac_profile`, `linux_profile`,
`profile_shape`, both arms of `platform_decision`, `mac_build_key`, `kernel_release_parts`.
The shape functions are sound as gates: each calls `closed(o, required, [])` before indexing, so their
own `o[k]` lookups cannot miss; enumerations are closed (filesystems, series `24.04`, `bootAttestation`,
lanes); digests are exact-width lower hex. An empty `platforms` object and empty `measuredProfiles` are
admitted, which only yields "not in population". `supportedMajors` keys are not constrained to two
digits; harmless because lookup is by the parsed build major.
The Linux arm: distro/series first (replaces the refusal list); then the boot facts accumulate
(`PROC_VERSION`, package ownership, archive key digest, secure boot / lockdown / UEFI signer only under
`secure-boot-lockdown`, namespace stability); `osrelease` grammar `line-abi-flavor`; first matching
measured profile selects `ExactMeasured` with ABI recorded as drift; otherwise baseline by line and
flavor. Semantically it agreed with reference107 on all my 112/114 Linux cases (1,029 + 771 + 407 + …
refusals, 0 differences) — that remains differential evidence, **not Linux execution**.

### B.2 Findings — inherited
- **I-1 (medium, R-3 made concrete) — `platform_decision` is safe only behind `profile_shape`, and
  nothing in its type says so.** It takes `profile: &V` and then uses `ps[key]`, `.unwrap()` on
  `measuredProfiles`, `supportedMajors`, `lane`, `minBuild`. Near-valid probe (`probes/nearvalid.*`,
  one deletion or one replacement anywhere in a valid profile set or observation, 1,606 cases):
  **98 panics — every one with a profile that `profile_shape` refuses; 0 panics with a shape-valid
  profile; 0 panics from any observation mutation.** The same run shows **704 cases where
  `platform_decision` ADMITS with a profile `profile_shape` refuses.** The single production caller
  passes `profile.envelope.payload` of a verified `ProfileSetEvidence`, so neither is reachable today —
  by convention. Make the parameter the verified evidence type (or a private newtype only
  `verify_profile_set` constructs); that turns both the panic surface and the unshaped-admit surface
  into compile errors instead of caller discipline.
- **I-2 (low–medium, inherited in reference and Rust) — observed kernel-release text still reaches
  refusals and drift unbounded.** 112 removed `fsType` reflection with the comment "never copy arbitrary
  observed text into a refusal"; the Linux arm still formats
  `KERNEL_LINE_OR_FLAVOR_{line}-{flavor}` and stores `line`/`abi`/`flavor` as drift. The character set is
  restricted (digits, dots, lower-case/digits) so it is not an injection vector, but length is not:
  against the 116 reference a 5 kB flavor gives a **5,055-character refusal**, and a 4 kB ABI is
  **ADMITTED with a 4,002-character drift value** (`probes/linux_reflect.py`). Rust mirrors this by
  construction (read, not executed for these four inputs). Bound the three parts (the reference first),
  or refuse over-long `osrelease` as `OSRELEASE_GRAMMAR`.
- **I-3 (note)** — Linux `ExactMeasured` binds only line + flavor + lane; ABI is drift by design. That
  is a policy statement worth keeping visible next to the macOS tier, which binds kernel UUID and dyld
  cdhash.

### B.3 Bounded malformed-input probes for R-3 (measured cases only)
20,000 random structured values × 7 boundaries = **140,000 calls under `catch_unwind`: 0 panics** —
`admit`, `verify_envelope`, `verify_root_chain` (one link), `verify_profile_set`, `verify_revocation`,
`propose_recovery`, `platform_decision` with arbitrary profile and observation. These inputs are
shallow (most fail the first shape check); the near-valid probe above is what found the 98. **This is
not evidence of panic absence**: it does not cover near-valid mutations of signed envelopes, roots,
recovery records or revocation documents (which need re-signing to get past the carrier), nor
allocation or stack limits. The owner's regression and fuzz gates remain necessary, and I-1 shows the
productive direction: mutate *valid* structures, one member at a time, behind each gate.

### Verdict B
**Inherited Linux branch and profile helpers: read in full; no semantic defect found and no disagreement
with reference107 in any case I have run; two findings to correct — I-1 (type-level binding of
`platform_decision` to a verified profile; 98 panics and 704 unshaped admits otherwise) and I-2
(unbounded kernel-release reflection, shared with the reference).** This is a code-reading and probe
verdict only. It is not Linux or OS qualification, and signed106 **R-3 stays open**: I measured bounded
cases, one of which panics behind a caller convention.

---

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.diff`, `revocation.diff`,
`probes/anchor_ref.py` + `anchor-ref.json`, `anchor-matrix.rust`, `profile_ref.py` + `profile-ref.json`,
`profile-mine.{ndjson,rust}`, `fixture-check.json`, `mutation.{py,json,log}`, `gen_malformed.py`,
`malformed.rust`, `gen_nearvalid.py`, `nearvalid.{ndjson,rust}`, `linux_reflect.py`,
`rust_probe*.rs.txt`, `hashes.txt`.
