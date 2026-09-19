# Independent bounded review — evidence encapsulation 128 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `evidence128-20260918-REQUEST.md`. Scope: the delta of frozen `evidence-encapsulation-checkpoint-128`
over frozen 126 — `crates/security/src/trust.rs` only — as correction of my platform123 F-1, plus the affected
producer/consumers. Not reference 127, not 124 F-2/F-3 or 126 N-1..N-3 (tracked, not claimed fixed), not caller
integration, OS, dependency, release or cumulative standing. No frozen/selected/product edit; scratch builds with
dedicated target directories; no commit, push or delegation. Test-only keys have no authority.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,105,448 bytes, SHA-256 `a10e9a1d1c359262e5782326bc34e96fd208e358cab5cc128b6bb0fa805c60eb` = request and `archive-pin.json` |
| Members | 390/390 regular, each length + SHA-256 equal to the manifest, read from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 126 extraction (330/330); `parent126/` copies equal the repository's 126 pin and manifest (`c4af9e9f…`) |
| Changed | exactly one file: `crates/security/src/trust.rs` `bb281f67…` (212,350 B) |
| Host pins | `host-isolation77/receipt.json`: 210 sources, **all equal the product pins**, including `trust.rs` |
| Before-images | `beforeimages-r1/trust.rs` = the 126 file; the second before-image differs from the frozen file only by the two `#[cfg(test)]` import splits the README describes |

## 2. What changed (complete delta read; `claude-out/trust.diff`)
`ProfileSetEvidence` + `verify_profile_set` moved into child module `admitted_profiles`; `RevocationEvidence` +
`verify_revocation` into `admitted_revocations`. Fields are private to the child; the parent gets
`envelope() -> &EnvelopeEvidence<QuorumReport>`, `core_pin()`, `version()`, `issued_at()` — by shared reference or
by copy — and nothing else. No `Clone`, `Default`, constructor or `&mut` accessor. All other hunks are mechanical
call-site changes (`.core_pin` → `.core_pin()` …) in consumers and tests.

**The verifiers themselves did not change.** `probes/moved_body_equivalence.py`: with whitespace removed, trailing
commas normalised and the one extra `super::` hop undone, both function bodies are character-identical to 126
(1,620 and 1,072 characters). So every predicate, order and error mapping I reviewed in 112–123 is carried over
unchanged; only the visibility boundary is new.

## 3. Evidence

**Owner checks, fresh scratch:** 75/75 security tests; strict workspace Clippy (`-D warnings`, all targets) clean.
The owner's nine compile-fail logs each contain exactly one error, located in the inserted client line, with the
privacy/borrow code the script expects (E0616/E0451/E0594). I agree with the owner's labelling: these are compiler
privacy checks, not behavioural kills.

**My compile-boundary probes** (`probes/compile_boundaries.py`, 17 clients + baseline; none overlaps the nine):

| Must NOT compile — and does not (11/11) | code |
|---|---|
| destructuring move `let ProfileSetEvidence { envelope, .. } = p` | E0451 |
| functional-update literal `ProfileSetEvidence { core_pin, ..q }` | E0451 |
| inherent `impl ProfileSetEvidence` **written in the parent** forging `Self { … }` | E0451 |
| inherent impl in the parent handing out `&mut self.version` | E0616 |
| `Default::default()` / `Clone::clone` | E0277 |
| accessor result bound as `&mut` | E0308 |
| a *sibling* child module reading a field / forging a literal | E0616 / E0451 |
| `platform_profile::AdmittedProfile(v)` tuple constructor from the parent (123 boundary, re-checked) | E0603 |
| raw-pointer cast write through `envelope()` | E0133 (`unsafe_code = forbid`, crate-wide) |

(First classification pass flagged three of these "unexpected" because rustc's *help note* points at the type
definition; each has exactly one error, inside my line. Both passes kept: `compile-boundaries.json`, `-r2.json`.)

| Compiles — where the type-level seal ends (6) | meaning |
|---|---|
| `mem::swap` of two evidences | harmless: both values are verifier-made |
| **root built by struct literal, never admitted, passed to the sealed verifier** | F-1 |
| **admitted root's `value` reassigned in the parent before verification** | F-1 |
| `ConditionalPlatformEvidence { profile, decision: <anything>, … }` literal | F-2 |
| `EnvelopeEvidence.payload = …` in the parent | F-2 |
| `QuorumReport.state = Met` in the parent | F-2 |

**Runtime demonstration of the first two** (`probes/rust_probe_inputs.rs.txt`, output `probe-io/input-forgery.txt`):
the fixture's schema-2 root with `roles.TR-PROFILE.threshold` lowered 2 → 1 is **refused by `admit`
(`RoleThreshold`)**. Given to the sealed verifier anyway — either as `root.value = forged` on a genuinely admitted
root, or as a plain `ValidatedRootPayload { value, canonical: vec![], digest: <genuine digest>, schema: 2 }` —
**7 of the 85 root-2 fixture envelopes flip from `SignatureThreshold` to a genuine, private-field
`ProfileSetEvidence`** (6 → 13 admitted), each reporting `quorum.root_digest` = the *genuine* root. All seven carry
one valid signature.

**Retained signed-body R3 inputs on 128.** Inputs copied byte-identical from my R3 review (its `hashes.txt`
re-checked: all OK). One harness-only adaptation, shown as a diff in the log: `.map(|e| e.version)` →
`.map(|e| e.version())`. Result: **all four outputs byte-identical to the 124 run** — revocation 302, recovery-epoch
242, root-chain link 1,302, possession 9; 0 panics, so the 0 admission disagreements carry over.

**New: re-signed near-valid *profile-set* bodies** (the moved verifier my R3 corpus did not cover).
`probes/gen_profile_corpus.py` reuses the R3 machinery unchanged: one deletion/replacement anywhere in a valid
body, canonically re-encoded, genuinely re-signed (control row reproduces the fixture signatures byte-for-byte),
and the core pin set to the digest *of the mutated body* so that `CorePin` cannot mask the payload path.
1,782 bodies → reference (125 tree) 91 ACCEPT / 1,691 refuse; Rust 91 ADMIT / 1,691 `Shape`;
**0 admission disagreements, 0 panics**. Every admitted evidence was then fed, through
`AdmittedProfile::from_verified`, to `platform_decision` with all 1,084 owner observations: 98,644 decisions,
**0 consumer panics** — the 119 I-1 path, now closed end-to-end on signed input.

**Behavioural mutants** (21 run, all compiled, baseline green; only `trust.rs`, no source pins to rebind; a 22nd
listed in the script was never implemented and is not counted): 15 killed —
including every accessor mutant (`core_pin()` returning another digest, `version()`/`issued_at()` swapped,
version read from `rootVersion`). 6 survived, all in code 128 did **not** change; re-run against my two independent
signed corpora their outputs are byte-identical too (`probes/survivors.json`): the TR-PROFILE role check and the
four disjuncts of the final binding re-check (guarantees `verify_envelope` already gives — defence in depth, not
reachable with a correct envelope layer), and the revocation metadata bound. I report them as *no observable
difference*, not as kills and not as defects of 128.

## 4. Closure of platform123 F-1
**Closed as specified.** After verification, no code outside the two child modules can construct, destructure,
clone, default or mutate either evidence type; the platform consumer can only borrow the payload of a sealed
value. The remedy I proposed in 123 is implemented exactly, and with no semantic drift.

## 5. Findings

- **F-1 (low–medium; the same defect class, one step upstream) — the seal starts at the verifier's output, but its
  inputs are still open.** `ValidatedRootPayload` (and `EnvelopeEvidence`, `QuorumReport`, `RootChainEvidence`,
  `RecoveryProposal` …) remain ordinary structs in the 4,200-line `root_payload` module. A sealed
  `ProfileSetEvidence` therefore proves "verified against *the root value it was handed*", not "against an
  admitted root": seven sub-threshold envelopes become genuine evidence under a root `admit` refuses (§3), and the
  evidence names the genuine root digest, so nothing downstream can tell. Nothing in the tree does this, and there
  is no production producer yet — this is the 123 F-1 property moved from the output to the input, which my 123
  remedy did not cover either. To finish it the same way: `ValidatedRootPayload` into a child module with `admit`
  as sole constructor and read-only accessors (it already documents "no public constructor"; make the compiler
  say so), then the envelope/quorum layer. Do this **before** wiring the first production producer, because that
  caller will live in the parent module.
- **F-2 (low) — the consumer-side outputs are forgeable literals.** `ConditionalPlatformEvidence` pairs a sealed
  profile with a `PlatformDecision` that any parent code can write. Lower risk (it grants nothing today), same fix
  when it acquires a consumer.
- **N-1 (note) — no production path reaches either verifier.** The `#[cfg(test)]` aliases mean release builds
  contain the sealed verifiers but no caller (dead code under the crate's `allow(dead_code)`). That is the honest
  state ("integration pending"); the first integration must import them un-gated, and is the moment F-1 starts to
  matter.
- **N-2 (note, shared with the reference) — lax but agreed profile shapes.** Among the 91 admitted near-valid
  bodies are `platforms: {}`, empty `measuredProfiles`, and one-character flavor/filesystem strings. Reference and
  Rust agree on all of them and every observation is then refused, so this is population policy for the profile
  owner, not a divergence.

## 6. Unresolved limits
Same-crate, same-child-module code is inside the boundary by construction. Privacy is a compile-time property of
this source; it says nothing about memory safety of dependencies, serialization (none exists), or callers that do
not yet exist. No Linux build, no release profile, no OS or dependency qualification was examined.

## 7. Bounded verdict
**128: reviewed, no blocking finding. platform123 F-1 is closed exactly as specified, with verifier semantics
byte-equivalent to 126, my retained R3 corpus reproducing byte-for-byte, and a new 1,782-body signed profile corpus
at 0 disagreements / 0 panics through the consumer. F-1 (unsealed verifier inputs) is the next step of the same
work and should precede production wiring; F-2 and the notes are minor.** Not approval of callers, custody,
current authority, OS, dependencies, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `host-pins.json`, `trust.diff`, `owner/*`,
`probes/{moved_body_equivalence.py,moved-body-equivalence.json,compile_boundaries.py,compile-boundaries*.json,compile-*.stderr,rust_probe_inputs.rs.txt,rust_probe_r3_adapted.rs.txt,rust_probe_profile.rs.txt,gen_profile_corpus.py,mutation.{py,json,log},survivors.{py,json,log}}`,
`probe-io/`, `r3/{main,possession,profile}/`, `hashes.txt`.
