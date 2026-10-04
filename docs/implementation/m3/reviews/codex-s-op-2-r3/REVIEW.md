# S-OP-2 r3 review

**Verdict: REQUIRED-FINDINGS.** Two required findings remain: complete read-back predicates and complete publication of terminal loss into the frozen summary. SOP2-R2-02 is resolved; SOP2-R2-01 and -03 are partially resolved.

Subject: [PROPOSAL.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/s-op-2/PROPOSAL.md), r3, **103,714 bytes**, SHA-256 **75a87d78a5f9dc3eca267bfe2f75ff9e12acb42c1329ad63c8d3e3876d47661a**. This is a verdict on the successor text. Item 24 still defers recording and its separate manifest review.

The lead's stated limitation is accepted: the log cannot record the required envelope write's own outcome after the freeze; that outcome stays visible through the ordinary exit code/output path. Neither finding asks for post-freeze logging or a provisional summary.

## Evidence and execution

All **34 hashes.txt pins match**, including the byte-identical r2 subject (83,628 bytes, 91a2ea45a8b46873b36e21ddaf97de9e55b101e0c5331fe5659c84c0b9c5b46e) and the retained r1 subject. The complete 943-line r3 subject, r3 response table, relevant pinned context, revision diff and r2 review artifacts were read.

The product is at **3e64266aa8729160cd22509dcfff95a3bb09fcea**, the request's named main, and its working tree is clean. All seven product pins match and their diff from the proposal's cited 3d2d5b5 to 3e64266 is empty.

No repository edits, commits, pushes, delegation, Cargo, builds, tests or crash-matrix runs occurred. The real OpenSIP home and the 413 fixture were not accessed. All written files are under this review directory. Hash and encoding computations used scratch scripts here, with Python at nice -n 19, -I -B and a private 0700 TMPDIR. The accounting trace is static reasoning, not an executable concurrency probe.

Evidence artifacts: [pin-verification.json](./pin-verification.json), [input-verification-summary.json](./input-verification-summary.json), [product-context.json](./product-context.json), [encoding-calculations.json](./encoding-calculations.json), [proposal-r2-r3.diff](./proposal-r2-r3.diff), [accounting-trace.md](./accounting-trace.md).

## Required findings

### SOP2-R3-01 (P1): Preserve the complete admitted-kind predicates on read-back

**Location:** PROPOSAL.md:485–513; item 13c header and kind predicates; item 13a; K6/K12; C-4/C-9/C-12.

The explicit wire table still admits values excluded by the inherited types. K12 omits LogicalPath's backslash exclusion, so a decoded value such as a\\..\\b, C:\\private\\name, or an elided tail containing backslashes passes its slash-only component checks. The pinned LogicalPath and IE path law prohibit backslashes. K6's writer now requires the workspace-source census, but its read-back predicate at line 504 lists only lexical checks; a persisted {file:crates/vendor_private.rs,line:1} passes those checks even in the C-9 case explicitly outside the census, and can reach a P0 projection. Finally, requestId and several kind patterns replace the pinned true-end assertions with bare $, without an explicit whole-string-match rule. IE specifically identifies that non-equivalence as accepting a trailing newline in the relevant schema/regexp dialect. The closed reader-only boundary prevents minting authority but does not repair these admission predicates.

**Evidence:**

- PROPOSAL.md:429–436: A persisted value is checked against item 13c's predicate, and accepted reader-only values are re-encoded/projected.
- PROPOSAL.md:231: K6 adds mandatory membership in the owner-controlled workspace-source census to its constructor law.
- PROPOSAL.md:504: K6's shared wire/read predicate does not list census membership.
- PROPOSAL.md:510: Neither the K12 path nor elided-tail predicate excludes backslash.
- common-v4.schema.json:101–111: LogicalPath excludes backslash, empty, dot, dot-dot and NUL segments.
- identity-and-evidence.md:160–164: The logical path law excludes backslashes.
- PROPOSAL.md:485–513: RequestId is restated with a bare $; K9/K10/K14/K15 likewise use bare-$ expressions.
- identity-and-evidence.md:65–76: The accepted product identity law deliberately distinguishes bare $ from the true-end assertion, and requires RequestId/ExecutionId to reject trailing LF/CR/space rather than trim.
- PROPOSAL.md:821: C-9's lexically valid crates/vendor_private.rs lookalike is explicitly outside the census.

**Required fix:** Make K12's decoded path and elided-tail predicates inherit the admitted LogicalPath backslash exclusion, alongside the existing slash, dot-component, NUL and scalar rules; keep valid names such as ..note and ... accepted. Apply the K6 workspace census requirement to reader-only values as well as writer construction, or explicitly retain an approved release-specific census in the descriptor; reject or reduce nonmember files to external without echoing the rejected name. Use the pinned true-end patterns verbatim, or state and enforce a full-string match with exact decoded lengths for all regex grammars; do not rely on a dialect-dependent bare $. State per-kind encoded V checks at read-back. Extend C-4/C-9/C-12 with backslash path/tail poison, the census lookalike through persisted read-back, and LF/CR/space suffix cases, while retaining the S-OP-1 residual for forged values that really satisfy the complete predicates.

### SOP2-R3-02 (P1): Make terminal disposition accounting part of the freeze protocol

**Location:** PROPOSAL.md:578–605; item 16 disposition/reservation cells, counter copy and freeze; item 17; C-7.

First-transition-wins prevents two terminal dispositions, but the cell CAS and its matrix increment are separate operations in the stated rule. A writer can win pending -> sink-failed and then be paused before incrementing the sink counter. On expiry, step 3 skips that already-terminal cell, step 4 copies a zero counter, and the resumed increment is diverted to the unreported post-freeze tally. A genuinely lost pre-freeze record is absent from the authoritative summary, contradicting overcount, never undercount. Neither the in-flight reservation count nor writer-drained notification closes this race at deadline expiry. The same issue applies to other terminal loss transitions and to global counter updates that begin before the freeze but publish afterwards.

**Evidence:**

- PROPOSAL.md:579–581: The disposition becomes terminal by CAS; a later attempt sees terminal and does nothing.
- PROPOSAL.md:583: Reservation state and the atomic in-flight tally are separate tracked state.
- PROPOSAL.md:595–598: Expiry proceeds even when writers have not drained; step 3 accounts only cells still pending.
- PROPOSAL.md:599: Step 4 copies counters; all later counter updates go only to the post-freeze tally.
- PROPOSAL.md:605: The law claims overcount, never undercount for admitted units.
- PROPOSAL.md:628: This frozen summary is the only source of the loss carrier.
- PROPOSAL.md:819: C-7 pauses a producer before enqueue and a writer callback after freeze, but does not pause a loss callback between terminal CAS and counter publication.
- accounting-trace.md: Static interleaving: EIO return; successful pending->sink-failed CAS; callback pause; deadline/finalizer sees terminal and skips; frozen sink-failed=0; callback resumes and increments post-freeze tally. No executable concurrency probe or test was run.

**Required fix:** Specify one linearization/ownership rule joining terminal disposition, loss publication and freeze. The frozen summary must include every loss transition already committed before that boundary, even when its callback is paused before updating a matrix. A bounded/helpable accounting protocol or a summary derived from authoritative cells with an explicit counted-state/counter reconciliation can satisfy this; do not wait indefinitely for a paused callback or sink syscall. Include reservations and pre-queue/global dispositions in the same publication/freeze rule, preserve exactly one disposition/count, and route only genuinely post-boundary activity to the post-freeze tally. Base marker unconfirmed on completion not confirmed in observable state at the freeze, rather than requiring proof that the syscall physically has not returned. Add a C-7 pause specifically between terminal CAS and counter publication, with a nonzero loss in the frozen summary and final envelope, plus the corresponding global-update race. Preserve the accepted post-freeze envelope-write limitation.

## Prior required findings

| Finding | Resolution | Remaining |
|---|---|---|
| SOP2-R2-01 | PARTIALLY-RESOLVED | SOP2-R3-01 |
| SOP2-R2-02 | RESOLVED | — |
| SOP2-R2-03 | PARTIALLY-RESOLVED | SOP2-R3-02 |

**SOP2-R2-01:** Item 13c repairs mandatory headers, boolean/composite spellings, widths, component role/ordinal shape and descriptor consistency, and item 13a establishes reader-only values. K12 still omits the inherited backslash restriction, K6 read-back omits its new census check, and exact-end grammar semantics remain inconsistent.

**SOP2-R2-02:** Phase/ComponentRole are capped at 32 for future registration; PathAnchor is capped at 16. The frozen compact spellings reproduce 646/724 headers within R=768, exact-key field costs, the 1002/1060 example and all 27 initial-event formulas. K12's 13-byte wrapper leaves 243 encoded tail bytes. Field-relative depth is explicit and C-1 uses the same convention. Admission must still reject the invalid read-back strings in SOP2-R3-01.

**SOP2-R2-03:** Cutoff/settle/gate closure/abandonment precede an immutable summary and envelope output; the deadline covers optional logging only; blocked writers are not joined; unconfirmed is added. The lead's post-freeze envelope-write limitation is stated and accepted. Separate state CAS and counter publication still leave a pre-freeze loss absent from the copied summary.

## Prior nonblocking observations

- **SOP2-R2-NB-01 — RESOLVED:** Unexpanded source is authoritative for literal members/templates, reviewed generated output bytes are hash-pinned, and protocol tables must equal the pinned enum. A generator/input pin alone cannot authorize changed output.
- **SOP2-R2-NB-02 — RESOLVED:** The ordered K8 map is now immutable event schema; additions/removals/reordering need a new name, and retired descriptors retain the old exact map. C-2 covers both addition and reorder.
- **SOP2-R2-NB-03 — RESOLVED:** K10's current maximum is corrected to 50, PathAnchor is capped at 16, K8 is nonempty, K13 uses explicit u32 widths/spelling, and field-relative depth is defined.
- **SOP2-R2-NB-04 — PARTIALLY-RESOLVED:** K6 construction and C-9 now use a build-carried owner-controlled source census, closing the prefix-only writer claim. The same restriction is absent from the item-13c reader predicate (SOP2-R3-01).
- **SOP2-R2-NB-05 — PARTIALLY-RESOLVED:** The raw bidi example is corrected and invalid K5/K6 inputs have rejection/external controls. C-5 still expects all escaped characters in K14/K15 and NUL in K12, although the new grammars forbid those values; see SOP2-R3-NB-01.
- **SOP2-R2-NB-06 — RESOLVED:** The marker is an elementwise saturating global-plus-sink vector, and the frozen summary retains global/per-sink matrices separately. The 1802-byte marker formula fits that single array.
- **SOP2-R2-NB-07 — RESOLVED:** window and wait limit are configured, since and grace are measured, and force grace starts at stage-1 cancellation. Provider/host CPU and native RSS meanings remain intact.

## Wire-schema assessment

The mandatory ts/level/event/requestId/fields set is explicit; duplicate keys at every level and unpaired surrogate escapes are rejected. Object members, writer order and reader order tolerance are stated. Integers have frozen widths and lexical rules, with Errno the only signed kind. component is role:ordinal, with a capped registered role and a decimal u16. Zero omitted/truncated is absent. Descriptor level, required identities and maximum are checked.

The seven identity shapes are consistent with the specified scope model: Request alone; Project; Project+Plan; Project+Execution; Project+Plan+Execution; published Project+Plan+Execution+Run; stored-read Project+Run. Attempt scopes need not invent an analysis Plan, and stored reads do not reuse an old execution as this request's attempt. The list gives no caller/candidate identity constructor. It is a shape check, not proof that the host wrote a persisted value.

| Kind | Frozen spelling assessment |
|---|---|
| K1 | Active/retired table member, re-encoded from the registered constant |
| K2 | u64 count/bytes/ns, boolean Flag, signed i32 Errno |
| K3 | Member string or unrecognized wrapper with u64 bytes and boolean truncated |
| K4 | Version ASCII grammar with 64-byte limit |
| K5 | Catalog membership plus stated 128-byte grammar |
| K6 | Fixed file/line object; writer census added, but read predicate needs the same requirement |
| K7 | Fixed u64 bytes/boolean truncated object |
| K8 | Nonempty array, u64 elements, exact length and immutable index map |
| K9 | Identity-kind string; preserve true-end matching |
| K10 | Fixed anchor/tag object, 16-byte anchor cap and exact 16-hex tag |
| K11 | Positive u32 process ID |
| K12 | Relative path or tagged elided tail; inherit backslash exclusion and encoded cap |
| K13 | Fixed line/optional-column u32 object |
| K14 | CanonicalIdentifier spelling and 1–128-byte limit; preserve exact whole-string grammar |
| K15 | Portable environment-name grammar; incompatible future DR-108 names need a successor |

Reader-only validated types can only be re-encoded/projected. They cannot mint writer SafeFields, scopes, identities or owner tokens. That addresses the authority-boundary concern. A reader still must enforce all its predicates; the honest custody residual does not make a non-census K6 or non-logical K12 valid.

Slash-relative K12 rules reject /x, ../x, a/../b, ./x, empty components, trailing slash and NUL. The tagged wrapper distinguishes real ... names from elision. A scalar suffix boundary and encoded-byte budget preserve Unicode/escapes. Backslash is a missing inherited condition, not a request to forbid every control character in a valid logical filename. Names such as ..note and ... remain valid.

The truncated equality and omitted upper bound permit absent fields from older descriptors without inventing an omitted count. The check stage and output recomputation after field dropping/P2 projection deserve clarification (SOP2-R3-NB-02).

## Encoding recomputation

| Quantity | Bytes |
|---|---:|
| Maximal JSON header | 646 |
| Maximal human header including template | 724 |
| Header reserve | 768 |
| Component decoded / quoted maximum | 38 / 40 |
| One-field example header | 712 |
| One-field example encoded K12 value | 256 |
| One-field example human line | 1,002 |
| One-field reservation | 1,060 |
| K12 wrapper excluding tail | 13 |
| Available encoded tail bytes | 243 |
| log.loss.counted MAX_LINE | 1,802 |
| config.value.resolved MAX_LINE | 1,345 |
| provider.process.reaped MAX_LINE | 1,319 |

The script independently extracted all **27 initial event** field lists, added common provider/supervision role and universe, and applied exact key lengths. config.value.resolved's 1,345 is the conservative sum of all declared alternatives; only one alternative is emitted. This is safe over-reservation. The next computed events are provider.fault.reduced at 1,313 and provider.stage.terminal at 1,269.

For JSON the cost per field is k+4+V; the first-field comma allowance is conservative. Human cost is k+2+V. Both headers fit R, so the formula bounds both lawful forms. Phase and ComponentRole caps apply to future ordinary registration. PathAnchor's cap of 16 gives a 54-byte future value, within V=64.

| Value | Recomputed maximum bytes | Declared bound |
|---|---:|---:|
| K1 / recognized K3 | 66 | 66 |
| K2 u64 / Flag / i32 errno | 20 / 5 / 11 | 20 |
| K3 unrecognized | 65 | 66 |
| K4 | 66 | 66 |
| K5 | 130 | 130 |
| K6, 128-byte file + u32 line | 157 | 160 |
| K7 | 48 | 48 |
| K8, 40 u64 maxima | 841 | 841 |
| K9 Snapshot / Closure / hex | 76 / 75 / 66 | 80 |
| K10 current / anchor cap | 50 / 54 | 64 |
| K11 | 10 | 10 |
| K12 elided | 256 | 256 |
| K13 line+column | 39 | 40 |
| K14 / K15 | 130 | 130 |

K12's 13-byte object syntax leaves 243 encoded bytes for the tail, including all rule-E expansion inside it. At most six bytes per escaped scalar fits that budget with whole escape/scalar boundaries. The wrapper has field-relative depth 1; K3's nested unrecognized form has depth 2.

Depth is now explicitly field-relative: scalar 0, each enclosing container +1, with root and fields excluded. A full K3 record may have four containers. C-1 now names a field-value depth-3 negative. OPP did not define the origin; this successor supplies that interpretation without concealing whole-record nesting. No native depth or encoder control was run.

The reserve assertion correctly proves the fixed maxima fit R. It does not by itself make every possible cap increase fail, because it has slack; SOP2-R3-NB-03 corrects that wording without reopening the actual fixed-cap proof.

## Finalization, marker and accepted limits

The new ordering resolves the previous envelope/snapshot ordering error: result decision, cutoff, bounded settle, gate closure and abandonment, immutable summary, S-OP-6 diagnostics rendering, then required output. Pre-scope unpersisted disposition occurs at finalization. Ring overwrites stay in the crash header.

First-transition-wins prevents duplicate cell dispositions. It does not by itself make counter publication indivisible with that transition and the freeze. The static accounting trace demonstrates a loss committed before freeze whose delayed counter update is omitted. This is the remaining finalization finding; it is independent of the accepted absence of post-freeze required-output records.

The 200/100 ms claim is narrowed to optional logging finalization. A blocked writer is not joined or signalled; required output retains ordinary blocking behavior and stalled kernel writes may delay process teardown. Already-admitted units may complete after the freeze and conservative abandonment can overcount. The one-unit/64-KiB residual remains per sink writer, with S-OP-7/X3D deciding its acceptability.

| Marker outcome | Assessment |
|---|---|
| written | Complete success confirmed; short writes still need continuations under separate gate loads |
| failed | Confirmed error and errno; no retry/recursive loss |
| suppressed | Its gate load observed closed |
| skipped | Never attempted before the deadline or before a writer blocked upstream |
| unconfirmed | Correct additional state for an admitted write whose completion is not confirmed at freeze |

For unconfirmed, the observation should be completion not published/confirmed, rather than a factual claim that a descheduled writer's syscall has not physically returned. That wording belongs with the freeze protocol fix. A later marker result may update only the post-freeze observation, without revising the authoritative carrier or declaring a pre-freeze unconfirmed marker written.

The single Counts vector now means the elementwise saturating sum of global and this sink's matrices as of marker admission. The frozen summary retains each matrix separately. These are compatible; marker failure creates no loss counter, and the marker may undercount later abandonment.

The log cannot contain the required envelope write's own subsequent outcome. That is the user/lead-accepted limitation. Ordinary required-output failure still follows the existing exit path; optional logging does not redefine it. This review does not require logging after freeze or changing the primary termination/committed Run.

## Other changes and scope

Unexpanded literal provenance and reviewed-output-byte pins address macro-produced literal shape and unpinned-generator-input ambiguity. A schema-divergent protocol table fails exact comparison. Templates use the same unexpanded-source check and printable ASCII/160-byte bound. Sealed tokens/traits remain intact.

K8 maps are explicitly immutable event schema; a new name/retired complete map is required for incompatible changes. K6 adds an owner-controlled build census and C-9's valid-looking dependency negative; that condition must also reach the shared reader predicate. K14's name characters and length match the pinned CanonicalIdentifier apart from the true-end spelling. K15 is a deliberate portable grammar and leaves incompatible DR-108 handle names to a successor.

The configured/measured elapsed meanings are now per-field. Native RSS remains labelled kib/bytes, checked conversion is absent on overflow, provider assertions do not become progress, and phase/child CPU and M3-L boundaries are unchanged. The SM-10 cross-law unit note remains with M3-L.

The storage-owned published/not-published split still matches the pinned CommitOutcome enum and private PublishedCommit receipt. All provider/supervision rows require Project, Plan and Execution with host-held role/universe. P2 credential-shaped names keep p2-name-match and per-member consent.

The substantive diff tracks the r3 table. No S-OP-1 custody, S-OP-5 configuration, S-OP-6 public grammar/wording, S-OP-7 crash/residual acceptance, S-OP-9 custody/consent/member limit, S-OP-10/O4 activation, S-OP-12, O7 or O9 decision is taken. Item 24 retains the scoped SDK append and original DRC punctuation. Its future recording needs its own pinned proposal/parents/selectors and design-unit review.

## Proposed controls

No controls were executed.

| Control | Coverage | Assessment |
|---|---|---|
| C-1 | COVERED-IN-TEXT | Unsafe constructors/impls, scopes/receipt ownership, 33-byte header members, empty K8, max line and field-relative depth are present. |
| C-2 | COVERED-IN-TEXT | Unexpanded literals, output-byte pins, exact schema enums, caps, frozen maps, maxima/docs and constructor census are covered. |
| C-3 | COVERED-IN-TEXT | Foreign visitors/formatters stay unvisited and no log logger is installed. |
| C-4 | PARTIAL | Kinds/header round trips and most poison cases are present; add full inherited predicates, census read-back and exact-end suffixes, and clarify dot-prefix positives and projection counters. |
| C-5 | CLARIFICATION-NEEDED | Rule E and wrapper boundaries are specified, but invalid K14/K15/NUL K12 must test rejection or the pure escaper, not legal kind construction. |
| C-6 | COVERED-IN-TEXT | P2 name matches, zero defects and synthetic guard checks remain distinct. |
| C-7 | PARTIAL | New timing/output order, stalled marker, reservations and late callback controls cover r2 requests; add terminal-CAS-to-counter and global-update-to-freeze pauses. |
| C-8 | COVERED-IN-TEXT | Published/attempt/stored-read/ephemeral/emergency identity examples remain. |
| C-9 | PARTIAL | Writer census/lookalike case is present; carry the census into read-back and exercise persisted poison. |
| C-10 | COVERED-IN-TEXT | Environment changes cannot alter effective filters, sink sets, bounds or content with resolver input fixed. |
| C-11 | COVERED-IN-TEXT | Semantic invariance across logging modes, failure/saturation and concurrency remains. |
| C-12 | PARTIAL | Provider dispositions and native RSS conversion/overflow are covered; persisted provider cases inherit SOP2-R3-01. |

## Nonblocking observations

### SOP2-R3-NB-01

**Location:** PROPOSAL.md:816–817; C-4/C-5 versus items 13b/13c.

C-5 asks for every escape-set character in every K12/K14/K15 value. K14 and K15 now have ASCII name grammars excluding that set, and K12 excludes NUL. Those cases cannot be constructed lawfully. C-4 also says elided tails starting with .. are poisoned, although ..note and ... are valid normal components under the actual predicate.

**Recommendation:** Split pure rule-E escaper checks from kind admission checks. Valid K12 names exercise allowed controls and escaping; NUL/backslash K12 and invalid K14/K15 inputs must be rejected. Use exactly .. or ../x for escaping-tail negatives and include ..note/... as positives, rather than a blanket starts-with-two-dots rejection.

### SOP2-R3-NB-02

**Location:** PROPOSAL.md:427–433; field drops, header consistency and projection.

truncated equality and the omitted upper bound are useful, but the text does not state whether consistency is checked over the parsed input before unknown/invalid-field drops or over the surviving reader values. A removed elided field changes the count, and later P2 projection can change it again. The output counters must describe the output fields.

**Recommendation:** Define the input check point, how an unknown elided field is treated, and recomputation of omitted/truncated after field dropping and projection. Add a two-field round trip with one elided P2 field projected out, plus an unknown/invalid elided field, to show the intended disclosure and whether the whole record or only that field is dropped.

### SOP2-R3-NB-03

**Location:** PROPOSAL.md:535–536; header reserve assertion.

The assertion that both maxima are <=768 does not make raising any cap fail: the human maximum is 724, leaving 44 bytes of slack. For example, a one-byte cap increase would remain within the reserve. The separate fixed 32-byte registration rule does prohibit such a header-table member.

**Recommendation:** Say cap changes require the applicable contract review and rechecking of the frozen grammar/maxima; increases fail the reserve assertion only when the recomputed maximum exceeds R. Keep the direct 32-byte header-table and 16-byte PathAnchor checks.

### SOP2-R3-NB-04

**Location:** PROPOSAL.md:579–581; written disposition and closed loss matrix.

Each terminal transition is said to increment exactly one counter, but written is a terminal state and is not one of the eight loss reasons. A successful projection must not create a nonzero loss entry. The text can be read as implying an additional written counter, but it is not declared.

**Recommendation:** Limit matrix increments to terminal missed-projection states, or define a separate success counter that never enters the loss carrier/marker. Keep the disposition cell for written and its first-transition rule.

This review completes the requested law review artifacts. It does not certify implementation behavior, a recording manifest or an inventory.

