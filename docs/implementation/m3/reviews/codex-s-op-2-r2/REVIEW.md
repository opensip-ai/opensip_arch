# S-OP-2 r2 review

**Verdict: REQUIRED-FINDINGS.** Three required findings remain: persisted-value predicates, the complete encoding/reservation proof, and final loss reporting. SOP2-R1-01, -03, -06 and -07 are resolved; -02, -04 and -05 are partially resolved.

Reviewed successor: [PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/s-op-2/PROPOSAL.md), r2, **83,628 bytes**, SHA-256 **91a2ea45a8b46873b36e21ddaf97de9e55b101e0c5331fe5659c84c0b9c5b46e**. This verdict is on the successor text. Item 24 defers the recording unit; this review supplies neither a recording-manifest verdict nor an inventory assessment.

## Evidence and boundaries

All **33 input pins** in the request's hashes.txt match, including the r1 proposal (60,424 bytes, SHA-256 e3b117f0cc2d73b06f8d0276ae01c551fc1503542bdf0e4c493ad15b0698e532). The prior REVIEW.md and review.json were read. The full r2 subject, its response table, the revision diff and the relevant pinned context and product evidence were inspected.

The product was observed at **3e64266aa8729160cd22509dcfff95a3bb09fcea**, with a clean working tree, rather than the request's named main commit 30c5db1. All seven cited product file pins still match. The diff between 3d2d5b5 and 30c5db1 over those paths is empty. Conclusions use the matching pinned bytes; they do not assert that the checkout is at either named commit.

No repository edits, commits, pushes, delegation, Cargo, product builds, tests or crash-matrix runs occurred. The real OpenSIP home and the 413 fixture were not accessed. All written artifacts and read-only-input scratch computations are under this review directory. Python calculations ran at nice -n 19, with -I -B and a private 0700 TMPDIR inside the directory. These computations are arithmetic and pin verification, not implementation tests. C-1 through C-12 were assessed as proposed controls only.

Supporting artifacts: [pin-verification.json](./pin-verification.json), [encoding-calculations.json](./encoding-calculations.json), [proposal-r1-r2.diff](./proposal-r1-r2.diff), [verify_inputs.py](./verify_inputs.py), [analyze_bounds.py](./analyze_bounds.py).

## Required findings

### SOP2-R2-01 (P1): Make persisted read-back predicates match the lawful wire kinds

**Location:** items 1, 5, 6 and 13a; PROPOSAL.md:396–419; C-4/C-12.

Item 13a does not establish the valid-kind guarantee it claims. K12 admits any bounded decoded UTF-8 string, including an absolute or escaping path, although ProjectPath is project-relative and item 6 excludes absolute/home/user names. The numeric grouping also contradicts the writer: K3's unrecognized wrapper and K7 contain a boolean truncated, and K2 Flag is a boolean, rather than the stated integer predicates. component is a role plus a u16 ordinal in item 1 but is read as a member of a registered table. These rules can export a forbidden path with P2 consent or reject valid host-written records. Required-header presence, descriptor RequiredIds/level consistency and the component wire spelling are not made explicit in the read-back steps.

**Evidence:**

- PROPOSAL.md:113–114: component is a K1 role plus a u16 ordinal; phase is a K1 code.
- PROPOSAL.md:210–215: K2 includes booleans; K3's unrecognized encoding contains bytes and a boolean truncated; K7 retains bytes and truncated.
- PROPOSAL.md:227–235: The only path encodings are an admitted project-relative ProjectPath or PathRef; absolute/home/user names are excluded.
- PROPOSAL.md:401: Read-back instead requires component to be a member of its registered table.
- PROPOSAL.md:412–413: K3 is called an exact two-integer shape, and K2/K7 are grouped under integers.
- PROPOSAL.md:419: K12 is accepted by decoded UTF-8 and size alone. A short JSON string such as /private/operator-name or ../private-name passes these stated conditions.
- PROPOSAL.md:421: The residual is supposed to cover grammar-valid forged values, not values violating the registered kind.

**Required fix:** Specify a closed wire schema for the header and each kind: mandatory ts/level/event/requestId/fields, optional members, nonnegative count ranges, exact component role/ordinal encoding and ranges, descriptor-required identities and fixed level. Split integer, boolean and composite predicates: K3 is {unrecognized:{bytes:u64,truncated:bool}}, K7 is {bytes:u64,truncated:bool}, Flag is bool, and K6/K8/K10/K13 have explicit keys/array ordering/widths. Require the actual admitted project-relative path grammar for K12; reject absolute paths and escaping components before projection, even with P2 consent. State K14/K15's name predicates rather than relying on generic string validity. Keep the honest S-OP-1 authenticity residual and use a reader-only validated representation so parsing does not mint writer scopes or owner-only SafeFields. Extend C-4/C-12 with valid boolean/composite/component round trips, missing/mismatched headers, and absolute/traversing K12 poison.

### SOP2-R2-02 (P1): Cover every legal phase in the declared line and queue reservation bound

**Location:** items 1, 3, 14 and 15; PROPOSAL.md:454–478; C-1/C-2/C-7.

The 678-byte JSON and 756-byte human headers reproduce only with the assumed 32-byte phase. Item 1 makes phase a K1 code, whose registration grammar permits 64 bytes; no separate phase limit is asserted. With the proof's own compact 70-byte component assumption, the independent header maxima become 710 and 788 bytes. More directly, a lawful one-K12-field event can produce 1,066 human bytes while E::MAX_LINE reserves only 1,060. Thus the registry assertion does not prove the maximum that item 15 reserves before encoding. The counterexample concerns the per-event bound and admission accounting; it does not assert that this example exceeds the 4,096-byte line cap.

**Evidence:**

- PROPOSAL.md:114: phase is a K1 phase code.
- PROPOSAL.md:161–168: K1 accepts up to 64 bytes; ordinary reviewed units may add code-table members.
- PROPOSAL.md:458–459: The arithmetic silently uses phase 32 and component 70.
- PROPOSAL.md:463–468: MAX_LINE is 768 plus the sum of 36+V for all fields.
- PROPOSAL.md:478: The producer reserves E::MAX_LINE before encoding.
- encoding-calculations.json: 32-byte phase reproduces JSON 678/human 756; 64-byte phase produces JSON 710/human 788 under the same independent maxima. The lawful one-field example has all scope identities, 96-byte name, 160-byte template, 64-byte phase, compact role:65535 component, one 32-byte K12 key with encoded value 256, truncated=1 and no omitted: header 776, actual line 1066, declared MAX_LINE 1060.

**Required fix:** Either impose and assert a 32-byte maximum specifically on header phase tables, including future ordinary registration, or raise/recompute the header reserve using the actual K1 maximum. Freeze component and all composite wire spellings so the proof has one representation to count. Assert the complete maximum for both encodings against the reserved bytes and the line cap. Make the depth convention explicit for root, fields and composite values and align C-1's depth-3 case with it; the current K3 wrapper has more than two container levels if whole-record depth is counted. Add the legal one-field/truncated=1 case and a 64-byte phase registration to C-1/C-2/C-7, in addition to the existing independent-maxima calculation.

### SOP2-R2-03 (P1): Finalize loss before the authoritative snapshot and required envelope output

**Location:** items 16 and 17; PROPOSAL.md:490–537; C-7.

The declared sequence cannot reliably deliver the authoritative loss summary. Cutoff begins only after required output is done, so an already-emitted envelope cannot acquire the later diagnostics summary. At notification/expiry the snapshot is taken before queued/unconfirmed records are added as drain-abandoned, while item 17 makes that snapshot the only summary source. Closing producer admission does not define the fate of a reservation/encoder admitted before cutoff or prevent later producer/writer counter updates racing the snapshot. The four marker labels also do not explicitly represent a marker already admitted into a blocked write whose completion is unconfirmed at expiry; calling it skipped needs an honest definition distinct from never attempted. Timed waiting and abandoning a blocked writer are sound, but these finalization and observation rules remain incomplete.

**Evidence:**

- PROPOSAL.md:490–500: Cutoff is after the command result is decided and its required output is done.
- PROPOSAL.md:497–499: The final snapshot is taken first; queued/unconfirmed records are then added as drain-abandoned.
- PROPOSAL.md:516–520: drain-abandoned has a global post-cutoff owner and per-sink queued/unconfirmed owners.
- PROPOSAL.md:520: The item-16 final snapshot is the only loss-summary source.
- PROPOSAL.md:527–535: The marker may start with an open gate and time remaining, then block inside its own admitted write; its closed outcome set does not explicitly define that unconfirmed case.
- PROPOSAL.md:537: A command producing an envelope must receive the diagnostics summary whenever any loss counter is nonzero.
- PROPOSAL.md:707: C-7 requires the blocked-write summary to count drain-abandoned and output/exit to complete within the stated budgets.

**Required fix:** Define a bounded finalization point for admission and dispositions, including pre-cutoff reservations/encoders, queued and unconfirmed units, late producer calls and writer callbacks. Close gates and account abandonment before freezing the final summary, or explicitly augment and freeze a copied snapshot after those additions. Preserve exactly one disposition per missed sink and prevent a late completion from double counting or silently rewriting the frozen summary; retain the stated conservative overcount residual. Deliver that frozen summary to S-OP-6 before the command envelope is rendered/emitted. State that 200/100 ms bounds optional logging wait/finalization; ordinary required-output I/O and kernel teardown retain their stated limitations. Define an observable unconfirmed/abandoned marker state, or precisely define skipped-at-expiry to include an already-attempted marker with unknown completion without claiming no bytes were written. Add C-7 cases for a stalled data write, a stalled marker write, a producer paused between reservation and enqueue, and late callbacks around finalization; require the final emitted envelope to contain the finalized loss.

## Prior required-finding resolution

| Finding | Resolution | Remaining finding |
|---|---|---|
| SOP2-R1-01 | RESOLVED | — |
| SOP2-R1-02 | PARTIALLY-RESOLVED | SOP2-R2-01 |
| SOP2-R1-03 | RESOLVED | — |
| SOP2-R1-04 | PARTIALLY-RESOLVED | SOP2-R2-03 |
| SOP2-R1-05 | PARTIALLY-RESOLVED | SOP2-R2-02 |
| SOP2-R1-06 | RESOLVED | — |
| SOP2-R1-07 | RESOLVED | — |

**SOP2-R1-01:** Sealing plus registry-private registration tokens replace the any-crate CodeEnum path. Listed release-source/schema provenance and literal/grammar checks cover K1, K3 and templates within the explicit reviewed-release-source threat boundary. Macro expansion is not itself provenance; C-2 must interpret registry-literal as literals written in the reviewed registry source and generated-contract as pinned literal output bytes.

**SOP2-R1-02:** Bounded parse, complete retired descriptors, closed classes, typed re-encoding and bounded drop-reason disclosure repair name-only projection. The header and per-kind predicates still differ from the lawful kinds and admit forbidden ProjectPath values.

**SOP2-R1-03:** Every syscall has its own acquire load; a successful load is admission. Descheduling after that load is expressly covered by one already-admitted unit of at most 64 KiB per sink writer. Item 17, C-7 and forbidden substitutes agree. R8 lawfully leaves residual acceptability and any coordinated issuance mechanism to S-OP-7 with X3D assent.

**SOP2-R1-04:** A command-owned timed wait, non-joined blocked writer, stderr-lock separation and explicit kernel teardown limitation fix the core writer-blocking problem. Output ordering, snapshot finalization, concurrent dispositions and unconfirmed marker outcomes still need a precise bounded rule.

**SOP2-R1-05:** Keys and wrapper syntax are now counted, and K3/K6/K7/K8 and the initial-event arithmetic mostly reproduce. The phase maximum used by the header proof is not the lawful K1 maximum, allowing a legal line to exceed E::MAX_LINE. Exact shapes, numeric widths and the depth anchor also need to be stated explicitly.

**SOP2-R1-06:** Rule E applies to every string in both forms, escapes the complete current 12-code-point Bidi_Control set plus C0/C1/DEL/line separators, quotes and backslashes, and truncates on encoded bytes at complete boundaries. A future property-set change requires a successor. The raw-bidi documentation example is a nonblocking editorial correction.

**SOP2-R1-07:** Raw max_rss_native is labelled kib on Linux and bytes on macOS; optional max_rss_bytes is a checked conversion absent on overflow. This preserves M3L:405 and Q0:889, does not make provider-asserted resources progress, and leaves the conflicting SM-10 label with the M3-L owner.

## Prior nonblocking observations

- **SOP2-R1-NB-01 — RESOLVED:** Item 4 adds closed provider-asserted numeric provenance to P0, requires asserted labelling and excludes progress/admitted fact; item 22 and C-12 agree.
- **SOP2-R1-NB-02 — RESOLVED:** Item 11 gives P2 values explicit byte spans and classifies wholly contained credential-shaped name matches as p2-name-match rather than a defect. C-4/C-6 cover password=CANARY names.
- **SOP2-R1-NB-03 — RESOLVED:** Items 9/23 use storage-owned constructors and PublishedCommit plus the matching Run-bearing scope for published, and an attempt scope without Run for undetermined/refused. The pinned product CommitResult and private PublishedCommit support this split; C-1/C-8 cover it.
- **SOP2-R1-NB-04 — RESOLVED:** Items 12/13/13a and scope exclusions preserve per-member P2 consent; the consent UI and custody remain S-OP-9.
- **SOP2-R1-NB-05 — RESOLVED:** Item 24 preserves the actual DRC punctuation, scopes the SDK insertion to host operational records and leaves DR-114 report tiers intact. The later recording unit has its own subject manifest and review.
- **SOP2-R1-NB-06 — PARTIALLY-RESOLVED:** Global and per-sink counter ownership, total-observed CaptureSummary reduction, loss-only diagnostics and conservative in-flight overcount are now stated. The final snapshot/cutoff/output order remains incomplete (SOP2-R2-03); marker matrix aggregation merits an explicit equation.

## Code-table bypass probes

The new private token and sealed trait close the previous unregistered/generic implementation path. Classification now depends on the reviewed registry or pinned literal artifact, rather than constness alone. The explicit exclusion for secrets committed into OpenSIP's reviewed release source/schema is an honest threat boundary.

| Probe requested | Assessment |
|---|---|
| macro-generated literal | Literal token matching alone is insufficient. The normative source-written registry-literal requirement or pinned generated-output provenance is the authority; a macro-transcribed literal does not bypass that requirement. C-2 should enforce it before expansion. |
| generated-contract with unpinned generator input | The reviewed literal output module itself must be pinned by bytes. Unpinned input cannot change that admitted output under its existing pin. If regeneration changes bytes, it is a newly reviewed registration. A generator/version-only pin would not satisfy the stated pinned-output rule; make this distinction explicit. |
| protocol-enum diverging from schema | C-2's exact comparison against the pinned closed schema rejects divergence; length and constness alone would not suffice. |
| template | Registry-literal, printable ASCII, <=160 bytes, no placeholders and review constrain templates under the release-source assumption. Apply source-origin checks to templates as well as table members. |

Rust macro matching/transcription can yield literal tokens through another macro. This supports the distinction between a token-shape check and the proposal's source-provenance requirement; it is not an executed Rust probe. [Rust Reference: macros by example](https://doc.rust-lang.org/reference/macros-by-example.html).

## Re-admission and custody

Items 2 and 13a now retain complete retired descriptors, bound the input line, reject duplicate/unknown header members, check registered field keys, drop invalid values, re-encode and then project by static classes. The disclosure uses four record-drop reasons and two field-drop reasons, without rejected-byte echo. The reason vocabulary is closed and the containing manifest member remains subject to S-OP-9's member bounds.

The residual allowing grammar-valid values from someone able to write the log directory is honest and belongs to S-OP-1. It supplies no authenticity, signed log or recovery authority. It does not excuse a predicate accepting an absolute ProjectPath, and the current integer/component predicates do not yet prove valid encoding. Required finding SOP2-R2-01 addresses those defects. Reader-validated values must remain distinct from authority-bearing writer scope or owner-only constructors.

The item-13a input threshold says 4,096 bytes plus newline, while item 14 bounds the full output including newline. A reader can be deliberately more permissive than the writer if re-encoding remains bounded; state that convention explicitly when fixing the wire predicates.

## Gate, termination and marker

Item 17 consistently makes the successful acquire load the admission point for each syscall, including short-write continuations and the marker. Closing is a release store. The forbidden-substitute rule disallows a syscall after its own load observed closed. C-7's paused-after-load case is therefore compatible with a unit issued after closure; it does not falsely prove strict issuance ordering.

With each writer having only one syscall in flight, the stated residual is at most one admitted unit of at most 64 KiB **per sink writer**. It is not an aggregate process bound. R8 explicitly leaves its acceptability after uncertain/latched outcomes to S-OP-7 with X3D assent. Neither the gate wording nor the control accepts that policy on the owner's behalf.

A termination-owned timed primitive and abandonment without joining a blocked writer bound the optional wait independently of sink write completion. The rule forbidding a logging sink from holding a lock needed by ordinary output/termination is correct, including no std Stderr lock held across a blocking logging write. Required output can still block in its own I/O; kernel teardown can still stall as stated. The unqualified C-7 output/exit timing claim should be narrowed to the logging contribution.

Global pre-queue loss and per-sink missed projections now have explicit owners. CaptureSummary reduction keeps the total observed byte count and bound-hit flag, rather than the retained-prefix size. Diagnostics is loss-only; it does not receive ordinary operational records. Exactly-once disposition, final accounting and the last summary snapshot still require SOP2-R2-03. A marker is best-effort and may undercount later abandonment; the final summary must be the correctly frozen source.

## Encoding recomputation

All figures include the final newline for lines, and quotes/composite punctuation for values. The calculation assumes the compact component spelling role:ordinal that yields the proposal's 70-byte maximum; the subject must actually freeze that spelling.

| Quantity | Recomputed bytes | Result |
|---|---:|---|
| JSON header, phase 32 | 678 | Reproduces item 14 |
| Human header, phase 32 | 756 | Reproduces item 14 |
| JSON header, phase 64 | 710 | Still below 768 |
| Human header, phase 64 | 788 | Exceeds header reserve |
| JSON field overhead, key 32 | 36 | Includes quotes, colon and comma |
| Human field overhead, key 32 | 34 | Space, key and equals |
| Lawful one-K12-field human line | 1,066 | Exceeds declared MAX_LINE 1,060 by 6 |
| Initial log.loss.counted formula | 1,905 | 768 + (36+66) + (36+841) + (36+66) + (36+20) |
| Initial provider.process.reaped formula | 1,562 | Ten fields, including common role/universe |

The 788-byte independent-maxima header is a header reserve calculation, not a zero-field counterexample with impossible omission counts. The concrete line uses one truncated field, truncated=1 and no omitted. It has a 776-byte header, a 32-byte key with 34-byte human overhead and a 256-byte encoded value. Its legal registration may use a new ordinary domain and 64-byte role/phase members; the law currently permits them. It stays below 4,096 but exceeds the bytes reserved before encoding.

| Kind | Declared bound / initial K8 size | Recalculation and qualifications |
|---|---:|---|
| K1 | 66 | 64 ASCII bytes plus JSON quotes; grammar includes underscore. |
| K2 | 20 | u64 max 20 digits; signed 32-bit errno min 11; booleans at most 5. Numeric types/widths must be explicit on read-back. |
| K3 | 66 | Matched member 66; {unrecognized:{bytes:u64::MAX,truncated:false}} is 65. |
| K4 | 66 | 64 grammar-safe bytes plus quotes. |
| K5 | 130 | 128 grammar-safe bytes plus quotes; underscore is admitted. |
| K6 | 160 | Compact {file:<128-byte workspace path>,line:u32::MAX} is 157; external variant is smaller. |
| K7 | 48 | Compact {bytes:u64::MAX,truncated:false} is 48. |
| K8 | 841 | 40 u64::MAX entries: 21*n+1=841 for n>=1; empty table needs 2. |
| K9 | 80 | Quoted SnapshotId 76, ClosureId 75 and universe key 66; bound 80 covers them. |
| K10 | 64 | Longest current PathAnchor installation plus 16-hex tag is 50, safely below 64. |
| K11 | 10 | u32 pid maximum 10 decimal digits. |
| K12 | 256 | Encoded-byte elision must include quotes and prefix; control escapes cost at most 6 bytes per code point. |
| K13 | 40 | Compact u32 line/column object is 39; u64 would be 59. State the width. |
| K14 | 130 | Quoted, escaped and elided name with total encoded cap 130; name read-back grammar needs stating. |
| K15 | 130 | Same encoded cap discipline as K14; declaration/name read-back grammar needs stating. |

K3's wrapper correction and the fixed-index K8 array repair the r1 undercounts. K10 is 50 rather than the request's 49, but V=64 is safe. K13's 40-byte claim is conditional on the stated compact spelling and u32 widths; it is not proven for unspecified integer widths. Numeric widths and every composite spelling should be part of the descriptor/encoder law.

Depth also needs an explicit origin. For a full JSON record, K3's unrecognized encoding has root, fields, unrecognized wrapper and reduced object containers. For a field value alone it has two containers. Item 14 and C-1 must use the same convention and explain the OPP encoded-record join. No implementation nesting check was run.

## Rule E and RSS

Rule E uses the same escaping in JSON and human strings, covers quotes/backslashes, C0, DEL, C1, U+2028/U+2029 and the complete current 12-code-point Bidi_Control set, and elides only on encoded-byte/code-point/escape boundaries. The Bidi_Control list matches [Unicode 17.0 PropList](https://www.unicode.org/Public/17.0.0/ucd/PropList.txt). The versioned closed-set successor rule is sound. Grammar-safe codes and workspace paths need no control escaping on valid input; the rule still applies to them. A raw U+202E in the documentation example needs editorial replacement.

The revised RSS event preserves raw wait4 ru_maxrss with an explicit native unit, and the normalized byte value is optional checked conversion. This matches M3L:405 and Q0:889. The child/reaped-descendant interpretation remains informational, without an aggregate-memory or budget claim. The conflicting SM-10 label at M3L:286 is identified for that owner; r2 does not silently amend M3-L.

Host-phase CPU is a RUSAGE_SELF user+system delta; reaped-provider CPU is the child's wait4 figure. Provider residentBytes/cpuNanoseconds/openHandles remain admitted-message assertions, labelled asserted and never progress. memory denotes observed physical bytes; snapshot bytes denotes sealed-file bytes. M3-L's start/transfer/analysis/teardown boundaries remain intact. The window/since/grace/limit sentence merits the per-field clarification below.

## Changed text, joins and scope

The pinned product CommitResult has Committed(PublishedCommit), Undetermined carrying execution_id and Refused(T); PublishedCommit's owner-controlled fields/getters support the proposed split. Items 9/23 require the storage owner's published event to use its receipt and matching Run-bearing scope; not_published uses an attempt scope and never a Run-bearing scope. No parsed log value may supply that authority. C-1/C-8 address the unsafe alternatives. This is a contract-level resolution, not a compiled proof.

Every provider/supervision row requires Project, Plan and Execution, plus host-owned role and universe, matching M3L:378 and its spawn-after-seal/admission boundary. The generic typography P, P, E is explicitly explained. K1 admits underscore and upper-case D9 spelling; K5 admits underscore and its stated catalog punctuation. Reduced has exactly the whole-text and capture-summary constructors, with no text or fingerprint retained.

P2 credential-shaped names use explicit spans and the p2-name-match category; only matches wholly inside a P2 field receive that expected classification. Member consent stays with S-OP-9. Changes inspected in the revision diff track the response table; no additional successor activation was found.

S-OP-1 retains storage/custody/retention/doctor/tamper decisions. S-OP-5 retains configuration. S-OP-6 retains public switch/human grammar, identity display and diagnostic wording. S-OP-7 retains crash descriptors, nonblocking hook stderr, suppression and the R8 residual decision. S-OP-9 retains custody, member limits and per-member consent. S-OP-10/O4 export, S-OP-12, O7 and O9 remain deferred.

Item 24's SDK4 family selector and operational-only append preserve DR-114 report tiers. Its DRC insertion matches the actual phrase and keeps the existing punctuation. The eventual recording must pin the then-accepted proposal, validate parents/selectors and receive its own ACCEPT-DESIGN-UNIT with a single-string subjectManifestSha256.

## C-1 through C-12 coverage

These are text coverage assessments, not executed controls.

| Control | Coverage | Assessment |
|---|---|---|
| C-1 | PARTIAL | All r1 unsafe constructors/implementations, scope and owner-token negatives, key/template/field limits are listed. Add the header-phase boundary and define the depth anchor; literal source-origin checks belong to C-2. |
| C-2 | PARTIAL | Registry/domain/retired descriptors, literal provenance, exact schema enums, bounds and docs drift are covered. The computed formula currently inherits the phase error; strengthen raw-source provenance and persisted K8 map checks. |
| C-3 | COVERED-IN-TEXT | Foreign log/tracing visitors and formatters must never run; this includes the r1 no-serialization request. |
| C-4 | PARTIAL | Canary origins/sinks/fingerprints, P2 names and poisoned known/unknown/retired/malformed records are included. Add lawful composite/boolean/component round trips and absolute/traversing K12 poison plus required-header consistency. |
| C-5 | COVERED-WITH-CLARIFICATION | The complete escape set, both forms, encoded-byte elision and non-UTF-8 fallback are present. K5/K6 invalid attempts need rejection rather than impossible escaped construction. |
| C-6 | COVERED-IN-TEXT | P2 name matches are separated from defects; normal corpus zero-defect and synthetic guard checks are distinct. |
| C-7 | PARTIAL | Floods, headroom, failures, per-syscall gate pause, stalled writer, four marker labels and numeric/header maxima are included. Add the legal one-field phase case and a final-envelope/counter-freeze protocol, paused producers/late callbacks, and blocked marker completion. |
| C-8 | COVERED-IN-TEXT | Published/not-published Run pairing, stored read, ephemeral scope and emergency allocation are listed; receipt-owner construction is reinforced by C-1. |
| C-9 | COVERED-WITH-CLARIFICATION | Non-workspace and traversal origins are excluded; include a lexically permitted dependency lookalike to prove actual source ownership. |
| C-10 | COVERED-IN-TEXT | With resolver input held fixed, environment variations may not change output, effective filters, sink sets or bounds. |
| C-11 | COVERED-IN-TEXT | Semantic invariance across levels, disabled logging, init/failure/saturation and concurrency is specified; operational counters/timestamps are excluded from equality. |
| C-12 | PARTIAL | Provider rows, asserted/progress distinction, native RSS units and conversion overflow are included. Persisted provider probes need the corrected read-back predicates from SOP2-R2-01. |

## Nonblocking observations

### SOP2-R2-NB-01

**Location:** PROPOSAL.md:148–165; provenance classes and templates; C-2.

A literal fragment matcher is not an attestation of original source: another macro can transcribe literal tokens. The normative registry-literal/source and pinned-output provenance requirements close that route under the stated reviewed-release-source assumption, but the current C-2 scan alone is weaker than those requirements.

**Recommendation:** Check the unexpanded registry source or another explicit provenance record, including templates and macro-generated literals. Resolve generation pins to the reviewed output bytes; record approved generator/input pins when they are the asserted provenance. An unpinned input cannot authorize changed output bytes under an old pin. Keep the exact closed-schema member comparison for protocol-enum tables.

[Rust Reference: macros by example](https://doc.rust-lang.org/reference/macros-by-example.html).

### SOP2-R2-NB-02

**Location:** PROPOSAL.md:131–134; event evolution; K8 at line 216 and read-back at line 413.

K8 gives persisted counts meaning through table order. The broad item-2 rule that non-additive event changes need a new name should apply to index-layout changes, but neither the K8 text nor C-2 explicitly freezes the ordered map. Member non-removal alone is insufficient: equal-length reordering silently changes labels, and member addition changes the length accepted by the current descriptor.

**Recommendation:** State that the ordered K8 map is part of the immutable event field schema. Preserve that exact map in each retired descriptor; require a new event name/layout descriptor for incompatible changes, or define an explicit compatible version rule. C-2/read-back controls should use a known older vector across member addition and attempted reordering.

### SOP2-R2-NB-03

**Location:** PROPOSAL.md:207–222; per-kind encoded maxima; item 14 depth.

K10's longest closed anchor encoding is 50 bytes, rather than the request's 49, and remains within V=64. 21*n+1 is correct for nonempty K8 tables but gives 1 for n=0 while [] needs 2. K13's V=40 holds for the compact line/column object with u32 values (39 bytes); the same shape with u64 values is 59. The proposal does not state that width or an exact composite spelling. Whole-record K3 container depth is root -> fields -> unrecognized wrapper -> reduced object; a field-relative depth convention needs to be explicit.

**Recommendation:** Correct the K10 arithmetic, require nonempty K8 or use max(2,21*n+1), freeze K13 widths/keys and define where depth counting begins. Generate the documented maxima from those exact encoders. These qualifications do not invalidate the reproduced 40-entry initial marker size; the phase defect remains required finding SOP2-R2-02.

### SOP2-R2-NB-04

**Location:** PROPOSAL.md:214; K6 CodeLocation; C-9.

The workspace-prefix/normal-component filter is necessary but does not itself attest source ownership. A dependency origin spelled crates/vendor_private.rs can satisfy that lexical filter. C-9 already requires all non-workspace origins to encode as external, so implementation must enforce that stronger claim.

**Recommendation:** Tie K6's accepted source names to an admitted build/source census or equivalent owner-controlled mapping and add a syntactically valid non-workspace lookalike to C-9. Interpret panic Location file text using compiler/source-path semantics, rather than native host Path semantics.

[Rust Location::file documentation](https://doc.rust-lang.org/std/panic/struct.Location.html#method.file).

### SOP2-R2-NB-05

**Location:** PROPOSAL.md:437; rule E example; C-5.

The second example in line 437 contains an actual U+202E character rather than the printable escape. The normative escape table is complete. C-5 also says K5/K6 attempts are escaped, while their grammars exclude those characters.

**Recommendation:** Print the ASCII characters backslash-u-202e in the example. Specify that K5/K6 invalid inputs are rejected or reduced to external as appropriate; the accepted K12/K14/K15 string cases exercise escaping. Do not require an invalid K5/K6 value to be constructible.

### SOP2-R2-NB-06

**Location:** PROPOSAL.md:527–533; marker matrix aggregation; initial log.loss.counted at line 636.

The marker is said to encode the global matrix plus S's matrix, while its event schema has one 40-entry Counts field. A single array is sufficient if plus means saturating elementwise addition, but that equation and the global-versus-per-sink interpretation are unstated.

**Recommendation:** Define the aggregation explicitly and keep sink dispositions distinct in the final summary. If two separate matrices are intended in the marker, add both fields and recompute its whole-line bound instead of certifying 1,905 bytes.

### SOP2-R2-NB-07

**Location:** PROPOSAL.md:665–673; measurement interpretations.

The RSS, CPU, resourceReport, physical-memory and sealed-file-byte interpretations are consistent with their named sources. The single sentence for window/since/grace/limit leaves configured duration versus actual elapsed duration ambiguous.

**Recommendation:** Map each elapsed field to one meaning: configured liveness/wait limit where intended, measured time since the last admitted transition for since, and an explicit configured-or-measured definition for grace. Keep all in monotonic nanoseconds and retain M3-L's start/transfer/analysis/teardown boundaries.

The review does not substitute for the lead's native lane, a later recording review or any deferred owner decision.

