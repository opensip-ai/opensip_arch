# Independent review: metadata Unicode bridge64 and signature carrier66 — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Bounded review of two unaccepted subjects. No whole-product, downstream-implementation, release or formal
selection approval is given or implied. Reference60 remains **CHANGES REQUIRED** (my r1 review); everything
below that touches reference60 is conditional on its successor, not on reference60 being accepted.

## Verdicts (one per subject, bounded)

| Subject | Verdict |
|---|---|
| **Unicode64** (`metadata_unicode15.rs`, adapter integration, contract clarification) | **Reviewed with specified nonblocking follow-ups.** No blocking finding in the bridge, its table, its integration or the version/domain boundary. One medium follow-up (U-M1) is a contract-vs-reference inconsistency that 64's own new sentence creates and must be closed before the clarification is selected. |
| **Envelope66** (`signature-envelope.schema.json`, `envelope_reference.py`, contract) | **Changes required** — narrow: E-B1 (lost exception boundary, reproduced) and E-M1 (contract reader-support rule has no reference counterpart). Routing, authority separation, RECOVERY token, root1/root2 dispatch, string endings, namespace/quorum and hashing had no defect under adversarial probing with real signatures. |

Conditional dependency, stated once: 66 hard-pins reference60's model hash `f71aceff…`. The reference60
successor will change that file (M2 composition, at minimum), so **66's pin, its 1,803 recorded cases and
my probe results must be re-established against the successor**; nothing here transfers automatically.

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `…/trials/metadata-unicode-draft-checkpoint-64/subject.tar.xz` (3,844,380 B) | `6af021020d6a2d8e17a45979c1894a94074d352f8e4f16e767f57ae29ff55657` | matches pin + `verification.json` |
| 64 manifest `subject.json` (358 members) | `b7fb83e49b8ebc21854174cdcc9fb4738b67aad3f275695c74eafa87400dc2c9` | byte-identical to review copy |
| `…/trials/envelope-reference-66/subject.tar.xz` (150,792 B) | `a47489603a71a12d14922a5d993bfbf1d6a01c23075137a37a584272e7844545` | matches pin + `verification.json` |
| 66 manifest `subject.json` (18 members) | `cf28bf9d3138ce56a4272d5271a5526a306717a4864d7a0cf502182c411465bc` | byte-identical to review copy |
| `candidate/envelope_reference.py` | `36f2ef24537bebcc9688ec346a12160c67a5410c0d868dc65c28a466033ac601` | matches manifest and `recheck-r2.json` |
| `candidate/signature-envelope.schema.json` | `48b7f4b5e7d3ae622f199aa2b5f07cb9f235ead67919cb5d428c547a5e67c8d1` | matches manifest |
| 66 contract / 64 contract / 60 contract | `bee68365…` / `18ae3e14…` / `99df85e0…` | chain 60→64→66 confirmed by diff |
| retained v8 `security-schemas.v8/envelope.schema.json` (live repo) | `82baf6967b8315546a93d955a2523805161f37bd22cb6728198442491e3cc3c1` | equals 66 `parent-inputs.json` |
| 66 `parents/root-admission-reference-60/subject.json` | `e3a5b45c…7e5d68` | equals the manifest I verified in the reference60 review |
| 66 `parents/metadata-unicode-draft-checkpoint-64/subject.json` | `b7fb83e4…dc2c9` | equals 64 manifest above |
| `unicode-normalization-0.1.24.crate` used by my harness | `5033c97c4262335cded6d6fc3e5c18ab755e1a3dc96376350f3d8e9f009ad956` | equals `product/Cargo.lock` checksum; `tinyvec 1.13.3` equals lock |

`claude-out/verify_pins.py`: every member of both manifests re-hashed from the tar and byte-compared to the
extracted directory — 358/358 and 18/18, no extra tar members, no extra extracted files, no non-regular
members. Re-run after all probes: still 0 bad for both, and the reference60 subject also still 0 bad. No
`__pycache__` written into any subject. `git status`: `ACTIVE-WORK.md` modified and an untracked
`docs/implementation/m2/reviews/claude-reference60-20260918-r1/` — neither is mine.

---

# Part 1 — Unicode64

## What the design is, and why it is sound

`normalize` / `is_nfc` split the input at every code point that is **unassigned in Unicode 15.0.0**, pass
those through untouched, and run the pinned Unicode-16 engine on the spans between them. That is correct
iff three things hold; I checked each independently rather than relying on the reported counts:

1. **The boundary table is exactly UCD15's unassigned set.** Parsed the 707 ranges out of the `.rs` source:
   825,345 scalars, sorted, disjoint, non-adjacent, no surrogates; set-equal to
   `{cp : category == Cn}` under Python 3.12 / UCD 15.0.0 (`tableMinusCn15 = 0`, `cn15MinusTable = 0`).
2. **Every U15-assigned code point behaves identically in UCD16.** Dumped category / ccc / decomposition /
   NFC / NFD for all 1,112,064 scalars under both interpreters (`ucd15.tsv`, `ucd16.tsv`). For U15-assigned
   scalars: **ccc 0 differences, NFC 0, NFD 0.** The only deltas are immaterial to normalization:
   `U+1171E` general category, and Hangul syllables where Python 3.14 merely *reports* the algorithmic
   decomposition string (NFC/NFD outputs identical).
3. **No U16-new composite can be produced from a span of U15-assigned characters** — the one way a
   "same data for old characters" argument can still fail. UCD16 adds 5,812 code points, 12 with non-zero
   ccc and 20 with canonical decompositions; for all 20 the full decomposition contains at least one
   U15-unassigned code point (`newCompositesBuiltOnlyFromU15Assigned = []`). The closest case is
   `U+105C9 = U+105D2 + U+0307` (second constituent is old); the first is a boundary, so `U+0307` stays
   separate, exactly as UCD15 requires.

Unassigned-in-15 code points are ccc-0 starters with no mappings, so a boundary blocks reordering and
composition across it on both sides — splitting there loses nothing. This is UAX #15 §11.3 applied
correctly.

## Independent differential (the subject's exact bytes, not a re-implementation)

`claude-out/unicode/rustprobe` `#[path]`-includes the subject's `metadata_unicode15.rs` read-only, built
offline with Rust 1.95 against the lock-pinned crate (`debug-assertions` on).

| Check | Result |
|---|---|
| All 1,112,064 scalars, `normalize` vs UCD15 NFC | byte-identical |
| 818,919 adversarial strings, `normalize` **and** `is_nfc` vs Python 3.12 | **0 differences** |
| Non-vacuity: same strings through raw UCD16 NFC | 55,032 differ from the UCD15 reference (so a missing/incorrect bridge would have been caught); 248,447 strings are changed by normalization |

Generators (`gen_cases.py`, seed 64): every U16-new mark / composite / constituent and 150 sampled new code
points × {one U15 mark per combining class, two-part Indic vowels, Hangul L/V/T/LV/LVT, singletons,
composition exclusions, CJK compatibility, musical symbols, deprecated tone marks, Tibetan}, both orders,
with interleaved marks; all ordered pairs of the 12 new marks under a starter; decomposed/reversed forms of
all 20 new composites; still-unassigned, noncharacters, PUA, `U+0000`, `U+10FFFF`; 400,000 random strings of
length 2–12 over that pool; the empty string.

## Boundaries and integration

- Only two call sites use the bridge, both in `security/src/trust.rs`' private `metadata` module:
  `Encoder::string` (`is_nfc`, l.449) and object key-collision (`normalize`, l.510). The module is
  `pub(crate)`, declared `mod` (not `pub mod`) in `lib.rs`.
- **Product identity is untouched:** `identity/src/relations.rs` and `capability_codec.rs` still call
  `unicode_normalization::is_nfc` directly (UCD16). Against the parent62 manifest, 288 product files are
  byte-identical; exactly `lib.rs` and `trust.rs` changed and the module + two fixtures are new — matching
  the README. `Cargo.lock` unchanged.
- Version guard: `const _: () = assert!(matches!(UNICODE_VERSION, (16, 0, 0)))` plus `=0.1.24` plus the lock
  checksum. An engine bump fails to compile rather than silently re-deriving behaviour. Good.

## Findings

### U-M1 (medium) — the contract's new "interpreter upgrade cannot silently change it" is false for the Python references
`security_lifecycle_model_v1.py` l.448 and `security_unit_lib_v8.py` l.68 / l.100 / l.639 / l.652 call
`unicodedata.normalize` with no `unidata_version` check. Reproduced
(`claude-out/unicode/ref60_interpreter_drift.py`): the same retained v8 `canonical_bytes({'x':'A̖ࢗ'})`
**succeeds under Python 3.12 and raises `NON_NFC_STRING` under Python 3.14** — a silent profile change by
interpreter choice, which is exactly what bridge64 exists to prevent on the Rust side. Both interpreters are
installed side by side in this workspace, and the reference60 security checker does not assert which one
runs it. Envelope66's `Verifier.__init__` does assert `15.0.0`; the root model and the 470-case checker do
not. Required before selecting the clarification: the reference owner that *is* the normative behaviour must
refuse to load under any other UCD (one guard in the model; v8 stays historical and is reached only through
it), or the contract sentence must be narrowed to the product implementation.

### U-L1 (low) — evidence is differential, not a proof; say so in the contract's pointer
The 19,074-row suite is UCD15's own `NormalizationTest.txt`; it cannot exercise the U16-new code points that
are the entire risk, and the 1,112,064-scalar comparison cannot see ccc or composition (single scalars never
reorder or compose). The subject's own context cases (2,316 in probe63) and my 818,919 close most of that
gap, and items 2–3 above give the structural argument. The README already says "not a full arbitrary-string
proof"; I agree and consider the structural argument + differential sufficient for this bounded claim.

### U-L2 (low) — normative-data provenance is a comment, and only one of the needed files
The table cites `UnicodeData.txt` SHA `806e9aed…`. I did not have that file's bytes in the subject to
re-hash, so I bound the table to UCD15 via Python 3.12 instead (equivalent for this purpose). Follow-up: a
retained generator + test that regenerates the 707 ranges from the pinned file, so the table cannot drift
from its stated source by hand edit.

### U-L3 (observation) — refusal precedence inside one object
`Encoder::value` reports `NfcKeyCollision` before visiting keys for `NonNfc`. With two keys that collide,
at least one is non-NFC, so both refusals are true; the 9,264 primary-reference cases pin the current order.
Not a defect — recorded because a Rust/Python precedence difference here would be invisible to NFC-only
tests.

**Interaction with reference60 findings:** none with B1/B2/M1/M2 directly. 64's contract sits on 60's
contract bytes (`99df85e0…`), so it must be rebased onto the 60 successor's contract; the clarification
paragraph is textually independent of S9.1.

---

# Part 2 — Envelope66

## Adjudication against retained owners

Retained owners read: v8 `verify_envelope` / `_verify_envelope_checked` / `KIND_ROUTING` /
`root_keys_for_role` (`security_unit_lib_v8.py` l.36-43, l.346-417), v8 `envelope.schema.json`, v8 §2.1
domain registry, reference60 `ENVELOPE_KINDS` (model l.2969) and S4.5/S9.1 contract text.

**Schema delta vs retained v8 (complete, computed structurally):** `$id`/`title`; `kind` +2
(`trust-recovery-epoch`, `platform-profile-set`); `domain` +3 (`root.2`, `recovery-epoch.1`,
`platform-profile-set.1`); `role` +2 (`RECOVERY`, `TR-PROFILE`); and the five string patterns change `$` →
`(?![\s\S])`. Nothing else differs — bounds, `uniqueItems`, `additionalProperties: false` and required sets
are retained.

| Question | Adjudication | Evidence (`claude-out/envelope/probe-results.json`, 158 cases, 0 unexpected) |
|---|---|---|
| All eight kinds | Correct. Each verifies only with its own authority; every one of the 7 other key groups signing under it yields "no valid signature" (49 cross-authority cases); swapping the role token to ROOT / RECOVERY / TR-CORE / TR-PROFILE and signing with that group is a routing refusal; swapping the domain is a routing refusal; a correctly labelled envelope whose preimage was computed under another domain is a preimage refusal. | `valid:*`, `cross-authority:*`, `role-swap:*`, `domain-swap:*`, `preimage-other-domain:*` |
| root1/root2 domain dispatch | Correct and exact-typed. Full root1/root2 bodies verify under their own domain; labelled with the other domain → `root schema/domain mismatch`; `rootSchema` `true`, `3`, `"1"`, absent, or a non-object body → `root payload schema dispatch` (`type(...) is int`, so `True` is not 1). | `root-kind-full-root*`, `root*-labelled-domain-*`, `root-dispatch-*` |
| Explicit `RECOVERY` wire token | **Sound and necessary.** `role` is one of the six signed fields, so without a distinct token a recovery epoch would have to claim `ROOT` (wrong key set) or borrow a `roles` entry (none exists). The token selects `root['recoveryAuthority']` only; it is never looked up in `roles`, so it cannot alias a role entry. Distinct domain + kind + role in the signed message rule out cross-kind replay of a recovery signature. | `recovery-signers-1/2` shortfall, `-3/-5` verified; works identically under root1 |
| recoveryAuthority-only key selection | Correct in both directions, including mixed sets: 2 recovery + 3 root signatures = `valid=2` shortfall; 1 root + 5 recovery under `ROOT` = `valid=1` shortfall. | `recovery-2-plus-3-root-keys-shortfall`, `root-1-plus-5-recovery-keys-shortfall` |
| Quorum counting | Distinct **keyIds**, not records: same key twice (second record altered so the array stays unique) counts once; an identical duplicate record is a shape refusal. Threshold is reported, not granted (v8 semantics retained). | `same-key-twice-counts-once`, `identical-duplicate-record-refused` |
| Namespace | ROOT and RECOVERY are namespace-independent but the namespace is still signed; other roles require membership in the admitted role's list (foreign namespace → zero authorized keys); explicit publisher binding enforced when supplied. | `profile-foreign-namespace`, `publisher-namespace-*`, `root-role-any-namespace` |
| Typed-absent / missing roles | Never zero-threshold authority: TR-PROFILE under root1 (absent from `roles`) and under a root2 with typed-absent TR-PROFILE both → `ROLE-UNAVAILABLE`. Reference60's gate guarantees `standing` is present on every admitted role, so the `selection['standing']` index cannot raise — **a dependency on reference60's new standing rule**. | `profile-under-root1`, `profile-typed-absent-root2` |
| Exact string endings | All five patterned fields refuse a final LF, including a namespace that was **genuinely signed** with the LF in it; uppercase hex, bool/float `envelopeSchema`, other `alg`, unknown member, 0 or 17 signatures all refuse as `RJ-4 UNSIGNED`. | `final-LF-*`, shape cases |
| Canonical byte / domain hashing | Retained exactly: `storedSha256` over the stored bytes as given; preimage = metadata-domain digest of the strictly parsed body; signed message = `opensip.metadata.envelope.2` digest of the six-field subject. Non-canonical whitespace still verifies (v8 behaviour); BOM, duplicate key, float, NFD, invalid UTF-8 → `canonicalization refused`. A body containing `A U+0897 U+0316` verifies — i.e. the reference is operating in the Unicode-15 metadata profile that 64 defines. | `stored-*` |
| Complete root admission | The **verifying** root always passes reference60's complete `admit_root_document(…,(1,2))` inside the call (threshold-1 role, duplicate public key, `None` → `ROOT-NOT-ADMITTED`). See E-M2 for what is *not* admitted. | `root-not-admitted-*`, `root-none` |
| Refusal order | context → (new) byte bound → publisher context → root → presence → shape → route → stored digest → parse/dispatch/preimage → publisher namespace → role availability → signatures → threshold. Same as v8 except the items in E-L1. | `ORDER-*` |
| Profile wire vs model projection | The contract's statement is accurate: reference60's `admit_profile_set_envelope` consumes `{envelopeSchema, kind, body, bodyDigest}` + asserted `signers`, which is a projection, not a second signature carrier. But see the interaction with reference60 M2 below. | code inspection |

## Findings

### E-B1 (blocking, reproduced) — the v8 exception boundary was dropped
v8 wraps the whole verifier: `except Exception → ('RJ-4 ENVELOPE_MISMATCH', 'boundary exception …')`
("exceptions inside the boundary are refusals", SEC3-M1/M4). `Verifier.verify` has no such wrapper. Fuzzing
6,000 junk-typed mutations of envelope / root / context produced one uncaught class, 11 times:
**`UnicodeEncodeError` from `V._is_str` when `publisher_namespace` is a string containing a lone surrogate**
(e.g. `'\ud800'`) — a caller-supplied context value crashes the verifier instead of returning
`malformed publisher context`. `ed25519_verify` (subprocess / temp-file I/O) can also raise `OSError` that
v8 would have converted to a refusal. A verifier whose failure mode is an exception rather than a refusal is
exactly what the retained owner ruled out. Required: restore the outer boundary (any exception → the v8
refusal), and retain the surrogate case as a regression.

### E-M1 (medium) — contract rule "reader support must be declared explicitly" has no reference counterpart
The 66 contract adds: "Reader support for added kinds and root2 must be declared explicitly. A reader
without the required support refuses the unsupported kind/domain without fallback." `verify()` takes no
reader set: it hard-codes `admit_root_document(root, (1, 2))` and accepts all eight kinds and `root.2`
unconditionally. The stage-1 `{1}` reader that S9.1 requires to refuse typed
(`ROOT.SCHEMA_UNSUPPORTED`, state unchanged) cannot be expressed, so that sentence is asserted, not
modelled, and none of the 1,803 cases can exercise it. Required: a `reader_schemas` / supported-kinds
parameter with the typed refusal and cases for a `{1}` reader meeting `root.2`, `platform-profile-set`
and `trust-recovery-epoch`, or remove the sentence from this proposal.

### E-M2 (medium) — a `root`-kind payload is dispatched, not admitted; the docstring/README overstate it
For `kind == 'root'` the body is checked only for `rootSchema ∈ {1,2}`. A three-signature ROOT envelope over
the stub `{"rootSchema":2}` returns **`VERIFIED`** (`OBSERVE-root-kind-stub-body-not-root-admitted`). The
contract is explicit that a verified carrier is insufficient for payload admission, so this is consistent
with the contract — but the module docstring ("All root payloads pass that candidate's complete RootV1/V2
admission") and README ("runs complete RootV1/V2 payload admission") read as though the *signed* root is
admitted. It is the *verifying* root that is. Combined with reference60 **M2** (chain and profile-set paths
that accept a root the document gate refuses), there is currently no single composed path in which a newly
presented root is (a) signature-verified, (b) document-admitted and (c) chain-verified. Required: fix the
wording now; when the reference60 successor lands its composed boundary, state which function owns
"verified **and** admitted" for a presented root and test the stub case there.

### E-M3 (medium) — recorded expectations are mostly golden snapshots of the candidate itself
In `check_envelope_reference66.py` the expected value of almost every row is the candidate's own output
(`q['expected']=r`; `add()` stores `engine.verify(...)`). Real assertions exist only for: valid envelopes,
the signer-subset masks, the three named authority/domain cases, the final-LF case, and "legacy changes are
root-kind only". The `kind=`, `role=` and `namespace=` sweeps (the bulk of the 1,803) assert nothing, so
they pin behaviour but would equally have pinned a wrong behaviour. My 158 cases carry independent
expectations and found no wrong outcome, which mitigates this for the current bytes; the retained suite
should still gain explicit expectations for those sweeps before it is relied on as a regression oracle for
a Rust implementation.

### E-L1 (low) — two new outcomes and one order change, none registered
`LOCAL-LIMIT` and `ROLE-UNAVAILABLE` do not exist in v8's outcome vocabulary and appear in **no** registry,
contract table or the reference60 model (grep: 0 hits in the 66 contract, the public-detail registry, the
v8 completion text and the model). `LOCAL-LIMIT` is also evaluated before root admission and before the
publisher-context check (`ORDER-limit-before-unadmitted-root`), whereas v8 reached the size bound only
inside `load_json_strict`, after the stored-digest step, as `canonicalization refused: METADATA_TOO_LARGE`.
Refusing oversize input early is the better order; it just has to be written down. This is the same class
of defect as reference60 **B1**: a new public token minted in one unit without its registry/enum owners.
Required before any consumer sees these strings: register them (or map them onto existing RJ-4 outcomes)
and state the order in the contract's verification paragraph.

### E-L2 (low, architecture) — three kind/route tables, and the schema has no owning location
After 66 there are three statements of kind → domain → authority: v8 `KIND_ROUTING` (6 kinds), reference60
`ENVELOPE_KINDS` (5 kinds, a different subset, prose authorities) and 66 `ROUTES` (8 kinds). Nothing checks
them against each other or against the schema enums or the contract table. The schema declares
`$id urn:opensip:product:signature-envelope:2` but lives only in the trial archive: it is in no
`source-pins`, no selected manifest, and the contract refers to it by bare filename. Required for placement:
one owning table (the schema + `ROUTES`), the model's `ENVELOPE_KINDS` either derived from it or deleted,
a drift check joining schema enums ↔ `ROUTES` ↔ contract table, and pins in every unit that reads it.
`report-asset-binding.v1.json` also enumerates trust roles and should be checked for whether `TR-PROFILE` /
`RECOVERY` belong there (I did not resolve this).

### E-L3 (observation) — crypto evidence is separate from trust/custody, as requested
All signatures in my probes are real Ed25519 signatures made and verified with OpenSSL 3.6.3 over keys I
generated under `claude-out/envelope/keys/` (**reviewer test-only private keys; no authority; safe to
delete**). I did not test weak/small-order public keys or non-canonical `S`: OpenSSL's permissiveness there
is a known, separately tracked difference from the strict Rust primitive (59/62) and is not an acceptance
rule of this proposal. Neither root admission (reference60) nor this verifier validates that `publicKey` is
a sound curve point; that remains owned by the strict-crypto review. Revoked-key filtering, trusted time,
recovery challenge/counter and current-core pin are correctly declared as owning checks elsewhere and are
not claimed here.

## Interaction with the reference60 findings (conditional use)

| Reference60 finding | Effect on 64 / 66 |
|---|---|
| B1 generated `DomainDetail` enum drift | 66 repeats the pattern (E-L1). Fix both under one rule: a new public token lands with every generated copy in the same change. |
| B2 cross-unit pins | 66's schema/reference are pinned by nobody (E-L2); 64's new Rust module and fixtures are outside the design-tree pin sets and need their own owner. |
| M1 unpinned regressions | 66's `ROLE-UNAVAILABLE` path relies on reference60's schema-2 standing rule — the exact branch M1 found unpinned. If that branch regressed, `selection['standing']` could raise `KeyError`, and with E-B1 unfixed that is a crash, not a refusal. |
| M2 uncomposed chain / profile-set | Directly relevant to the "projection" paragraph: the contract says the profile-set projection "must be constructed from verified evidence; callers cannot invent signers or a bodyDigest", but reference60's `admit_profile_set_envelope` still accepts caller-asserted `signers` and any `acceptedRoot`. 66 supplies the evidence-producing half; nothing yet **binds** the projection to a `VERIFIED` result. Treat that sentence as a requirement on the reference60 successor, not as something 66 establishes. |
| Model hash pin `f71aceff…` | Will break on the successor by design; re-pin and re-run everything. |

---

## Commands and outcomes (all output under `claude-out/`)

| Command | Interpreter / tool | Outcome |
|---|---|---|
| `verify_pins.py` (before and after probes) | py3.12 | 358/358 and 18/18 tar + extracted match; 0 extra |
| `unicode/dump_ucd.py` ×2, `stability.py` | py3.12 UCD15, py3.14 UCD16 | table ≡ UCD15 `Cn`; 0 ccc/NFC/NFD changes for U15-assigned; 0 new composites buildable from old characters |
| `cargo build --release --offline` (`unicode/rustprobe`) | Rust 1.95 | built; crate checksum equals product lock |
| `gen_cases.py` → `rustprobe` → `cmp` | py3.12 / Rust | 818,919 strings identical (normalize + is_nfc); 1,112,064 scalars identical |
| raw-UCD16 non-vacuity pass | py3.14 | 55,032 of those strings differ without the bridge |
| `ref60_interpreter_drift.py` ×2 | py3.12 / py3.14 | same reference call: OK vs `NON_NFC_STRING` (U-M1) |
| `envelope/probe_envelope.py` | py3.12 + OpenSSL 3.6.3 | 158 cases, 0 unexpected; fuzz 6,000 → 11 uncaught `UnicodeEncodeError` (E-B1) |

Not run: the one-shot preparers/checkers over retained directories; the product workspace's own
`cargo test` / Clippy (I exercised the module's exact bytes through my own harness instead of re-running
the reported 160 tests); any strict-Rust-crypto comparison.

## Unresolved assumptions

1. `unicode-normalization 0.1.24` implements UCD 16.0.0 faithfully. Bound empirically (exhaustive scalars +
   818,919 strings vs an independent UCD15 oracle, and UCD15≡UCD16 for old characters via CPython), not by
   reading the crate's tables.
2. CPython 3.12's `unicodedata` is a faithful UCD 15.0.0 — it is the *selected* reference, so this is the
   definition of correct here, but it is an assumption all the same.
3. I did not re-hash `tools/unicode/case-data/unicode-v15/UnicodeData.txt` (bytes not in the subject).
4. `trust.rs`' full diff against parent62 was not reviewed (parent bytes are not in the subject, only its
   manifest); I reviewed the two integration sites in the candidate bytes and confirmed by manifest that
   only `lib.rs`/`trust.rs` changed. The README mentions an incidental rustfmt change to `trust_time.rs`
   retained as a separate file; I did not adjudicate it.
5. The quorum62 roots used by the archived 66 checker were not independently re-admitted by me; my probes
   used freshly built roots that I confirmed pass reference60 admission.
6. Everything in Part 2 is relative to reference60 model `f71aceff…`, which is not accepted.
