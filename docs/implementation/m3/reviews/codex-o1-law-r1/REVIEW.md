# M3-O1 r1 review

**Verdict: REQUIRED-FINDINGS.** One required finding concerns the unit dependency graph. The two S-OP-2 design units have separate ACCEPT-DESIGN-UNIT verdicts.

Subject: `docs/implementation/m3/operability/o1/PROPOSAL.md`, **73,886 bytes**, SHA-256 `ac3f12fae691e2a9a9fa6c2fff264e3e3a5365fe36652d1bd58951ff1369d37a`. Product basis: `b7b87b740b4332597ef9d609b1e96d7b420f8885`. Reviewed working-tree subject bytes; the final pin check confirms they did not change.

## Required finding

### M3-O1-RF-01 — O1-p needs the crate that O1-a creates (P2)

Location: [PROPOSAL.md:564](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/o1/PROPOSAL.md:564), item 23; also item 20 at line 477.

O1-p must add **operability's re-export of `dispose`**, but its dependency row names only J3a and the J4a question. O1-a owns creation of `crates/operability` in the preceding row. No file exists under that path at the pinned product base: the read-only `git ls-tree` check returns an empty list, preserved in [design-unit-checks.json](design-unit-checks.json).

Thus the stated graph permits O1-p to proceed after J3a while one of its required edits has no target. An implementer must either introduce part of O1-a's crate or infer an unstated integration prerequisite. Explicit unit dependencies are needed here because this law deliberately splits O1 into independently reviewed units.

**Fix:** add O1-a integrated as O1-p's prerequisite for the re-export and include the edge in the owed M3P update. Alternatively, assign the re-export to O1-b or O1-S, each already gated on both O1-a and O1-p, leaving O1-p platform-only. This finding leaves the lead's Q2 ruling intact: O1-p may still land before held J4a.

## Decisions and contract alignment

1. **Crate and package authority (G1; Q4).** A safe crate depending only on platform fits the package boundaries. CH14's table explicitly presents generated package proposals and grants no component authority (CH14:271–275). CH14-O can therefore be a record note; the reviewed inventory and manifest edges provide implementation authority. Security receives typed completion results and stays outside the operability dependency graph. Storage and components acquire their edges in their reviewed wiring units.

2. **Scope construction and wiring (G2; Q6).** The one-time capability set, sealed scope markers and owner-only mints preserve SOP2 items 7 and 8. A fixed-width value passed through an owner-held mint is permitted by item 8(b); it does not create an ambient public byte constructor. Test mints remain feature-gated and refused without debug assertions. C-1 and C-8's owner-wiring legs are owed to their actual wiring units. No synthetic RequestId or production record is permitted before RequestId wiring.

3. **Transport and hashing (G3; Q8).** SOP2 item 10 permits an in-house transport. The pinned lock has no tracing or log package, and the lock prohibition has a named enforcement owner. The host and identity policy scopes do not grant operability a SHA package. Identity's helper entails an identity edge; direct SHA package use needs policy work; the existing platform CommonCrypto wrapper is macOS-only. The in-house SHA-256/HMAC option is coherent with the platform-only edge and unsafe-code prohibition. The known-answer, padding-boundary and independent-reference controls are necessary implementation gates; no hashing implementation is accepted by this law review. This review did not resolve compiled feature closures from Cargo.lock alone or execute Cargo metadata. The M3P/OPP transport wording has explicit record follow-ups.

4. **Sink accounting and finalization (G5).** The production constants, development-feature refusal and typed startup failures remain consistent with SOP2. The law preserves finalization steps 1–5, including bounded per-sink cells, cutoff and freeze. Finalization occurs after outcome decision and before rendering; bootstrap paths provide backstops. Rendering and C-7's carrier legs remain owned by S-OP-6. The required envelope write's own outcome remains visible through the exit code, as accepted in SOP2. LoggingUnavailable changes no command result. The item 5 allocation leaves no SOP2 item 1–17 without an owner; it also identifies the deferred K6 writer/C-9 and carrier controls.

5. **Harness and phase vocabulary (G4; Q1, Q3).** The owed S-OP-2b text narrowly adds the harness sink: inherited descriptor 3, admission and close-on-exec, P0/P1 info projection, ordinary persistent-sink accounting, bounded drain, reader admission and driver-side digest of exact stream bytes through EOF, including a torn last line. It carries no product evidence authority. The phase table, pairing by phase/component, fixed parents, started/completed timestamps and explicit not-applicable completion give Q0 §9.4's checks a concrete subject. Missing owner wiring remains phase-missing. The optimized harness profile in **lead answer Q1 is sound**, provided it stays the same preregistered setting for all measured samples; the assertion count needs the nonblocking correction below. For Q3, Q0 §9.6 specifies concurrency 1. Above that setting, overlapping provider siblings can produce negative unattributed time; the existing typed rejection remains applicable and the law explicitly defers an aggregate parent to S-OP-6.

6. **Registrations and generated tables (G7, G8).** O1-a's repair registration matches J-RW's seven kinds and fourteen states. D3a owns its provider, supervision and tool additions; the added domain is an ordinary registration. M3-L emissions remain gated on L taking effect. O1-c waits for E2s and a separately reviewed generator successor, with literal tables and reviewed-module hashes. K6's retained reader vocabulary does not authorize its deferred S-OP-7 writer.

7. **Enforcement (G6).** The textual scanner, sorted exact-count ratchet and negative controls are an appropriate interim mechanism. Inline test modules remain counted until the later Clippy sweep; explicit test-only path exclusions are a deliberate scope decision. A closed, no-I/O disposition helper in platform is reachable by platform and security without forbidden edges. O1-S waits for J3a, J4a and X3c-3, uses explicit per-crate lint values and retains audited crash-path exceptions. The count discrepancy below changes neither ownership nor that sequencing.

8. **Unit boundaries (Q2, Q7).** Read-only status checks of J3a, J4a, X3c-3 and E2s reproduce the in-flight file groups in item 23; the broad exclusions cover their changed and untracked paths. J4a's platform-lib hunk is the filesystem re-export at lines 41–47, distinct from the proposed clock re-export at 96. **Lead answer Q2 is sound:** no held-J4a integration dependency is needed; the later unit rebases. The missing O1-a dependency is a separate issue. O1-a is large, but its codec, capability and accounting controls are coupled; a single ACCEPT-UNIT boundary is defensible (Q7). The three-day estimate remains an unmeasured planning estimate.

The two-unit selection decision (G9; Q5) is sound independently of the O1-p finding. P selects the APP-pinned parents; R faithfully records accepted SOP2 item 24. Their separate reviews contain the binding evidence.

## Nonblocking observations

- **M3-O1-NB-01 — request self-pin.** The supplied REQUEST pin expects 14,923 bytes / `516611d2cd1c914552bfc1299fb1256dc4703c269fe64006c6605e22220d7d82`. Observed bytes are 15,899 / `5351a04e88ff2cca0626293a2dae2e5afe9dea05830418fdef2edf0b2cbc7abb`. I followed the current request including Q1/Q2. The other 49 pins match, including every subject/member; all observed bytes were stable through final verification. Refresh the context self-pin for the next request.
- **M3-O1-NB-02 — assertion count (331, 634).** There are four actual production assertion macro sites, not nine: security/trust/floor_publication.rs:702; security/trust/trust_bootstrap.rs:956; storage/blob_store.rs:81,98. The other five broad matches are compile-refusal attributes or a test guard string. Correct the count and re-audit at O1-b launch. This is agreement with Q1 with a factual correction.
- **M3-O1-NB-03 — scanner baseline (449, 477).** The total 306 lines in 150 files matches. The stated path exclusions leave 143 lines (platform 56, security 73, storage 10, CLI 3, lifecycle 1), rather than 140/security 70. Correct the totals or enumerate the additional excluded test-support paths; compute the ratchet seed at the actual integration base.

## Verification and limits

The permitted pinned Python binding helper ran at nice 19 in this review's private detached worktree of b7b87b7, with isolated home and a private 0700 Darwin-user TMPDIR. Baseline passed at 101 contracts/5 supersessions/v138; P alone passed at 102/5; P→R passed at 103/5, with and without implementation checking. R alone refused for unselected parents. All nine probes produced their specified results, including the future VD2 supersession passing. The non-contract chains stayed unchanged.

See [local-binding-check.json](local-binding-check.json), [design-unit-checks.json](design-unit-checks.json), [pin-verification.json](pin-verification.json), [product-facts.json](product-facts.json) and [in-flight-files.json](in-flight-files.json). The literal appended-lock CLI fails closed on SCRATCH review files; the overlay is the local binding evidence, not a live integration. Builder/checker source was inspected; their reported 37-check run was not independently repeated.

No Cargo, product build, test lane or crash-matrix run; no repository source edit, commit, push, delegation, real-home access or private fixture access. The verification worktree and TMPDIR are removed; [cleanup.json](cleanup.json) records cleanup. Code-unit acceptance and product qualification remain for their own reviews.

