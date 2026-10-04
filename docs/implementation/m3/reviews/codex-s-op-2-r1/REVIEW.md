**Verdict: REQUIRED-FINDINGS — seven required findings.**

The successor addresses the requested registry, fifteen kinds, privacy classes, sink ceilings, memory/volume bounds and loss marker. Its core reductions and owner boundaries follow the accepted operability plan. r1 is not sound enough to accept: the proof of code-table provenance and serialized bundle safety is incomplete; the write-admission and drain claims overstate their mechanisms; the static encoded-size proof omits legal output bytes; escaping is inconsistent; and the reaped-RSS field does not preserve the joined native-unit contract.

**Reviewed bytes and method**

`docs/implementation/m3/operability/s-op-2/PROPOSAL.md`: **60424 bytes**, SHA-256 **`e3b117f0cc2d73b06f8d0276ae01c551fc1503542bdf0e4c493ad15b0698e532`**. All **29** supplied pins matched. The product HEAD was `3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f`. The live OPP file and its accepted `PLAN-r3.md` bytes were distinguished; the three prior reviews were read as context, not as authority for a new acceptance. Their pins are in [document-audit.json](document-audit.json).

No Cargo, compiler, product build, test suite, crash-matrix run or product verifier was executed. No repository files were changed; no delegation or commit occurred. The real OpenSIP home and 413 fixture were not inspected. Only read-only inspection, Git HEAD observation with optional locks disabled, and scratch digest/document scripts were used. Output is confined to this review directory. [pin-check.json](pin-check.json) records the pins; [subject-reviewed.md](subject-reviewed.md) preserves the exact reviewed text. The code counterexamples below are static reasoning, not executed tests.

**Required findings**

**SOP2-R1-01 (P1): Admit code tables by provenance; constness alone does not close K1.** [items 5/K1 and 8; C-1/C-2](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/s-op-2/PROPOSAL.md:212)

K1 accepts any CodeEnum implemented by any crate. An associated const prevents a runtime String from becoming TEXT, but it does not prove that the table contains approved release codes rather than source, environment values or other P3 text. For example, a one-variant implementation can set TEXT to &[include_str!("short_source.txt")]; a short UTF-8 source fragment satisfies the stated 64-byte bound and the shown type constraints. An ordinary registry entry using Code<ThatEnum> then has a P0 SafeField without a new kind or a new constructor. C-1 only rejects a non-const table, so it misses this provenance bypass. The claimed construction guarantee needs a table-admission boundary as well as const evaluation.

**Fix:** Require Code<E> to use a host-admitted, registered code table, with a sealed registration token or equivalent closed implementation boundary. Define approval/provenance rules for those tables and static templates; constness remains a bound on runtime substitution, not their privacy classification. Cover a const table populated from P3 input, arbitrary generic CodeEnum adapters, and unapproved table implementations in C-1/C-2. Retain the express exclusion for deliberate covert signalling; this finding does not demand general information-flow confinement.

**SOP2-R1-02 (P1): Re-admit serialized bundle fields before re-encoding them.** [item 13 support bundle; item 2 retirement](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/s-op-2/PROPOSAL.md:317)

Using the running registry to assign classes is necessary, but a registered event name does not prove that serialized field values are lawful SafeField encodings. A record named provider.process.spawned can contain arbitrary text in its P0 role field; class projection alone includes it in a default bundle. Unknown fields, mismatched field types, invalid code members, and malformed identity/path encodings have no disposition. Retired names are accepted, while item 2 only promises to reserve their names, not retain the schema needed to classify their fields. The parser is expressly outside SafeField, so the construction guarantee is lost at this boundary unless serialized values are re-admitted.

**Fix:** Specify bounded, closed record admission for bundle inputs: only known fields with valid encodings of their registered kinds may be re-encoded; unknown fields, invalid values and unavailable schemas must be omitted or cause the record to be dropped with a bounded disclosure. Retain complete descriptors for supported retired names, or drop retired records lacking one. Never pass through raw serialized values or trust their class claims. Add C-4/C-12 cases with a known event name but a poisoned P0 field, extra fields, malformed values and retired/older schemas. Leave file custody and the consent UI with S-OP-9.

**SOP2-R1-03 (P1): Align the gate guarantee with its admission linearization point.** [item 17 sink gate; C-7](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/s-op-2/PROPOSAL.md:388)

The atomic load can linearize admission, but it cannot also ensure that only syscalls already issued before closure run afterward. A writer can read open, be descheduled, observe gate closure on another thread, then issue write. Item 17 only permits completion of an already-issued write and C-7 requires no new write to be issued. Those stronger claims are not implemented by the stated load-before-write mechanism. The same race applies to the direct marker path.

**Fix:** State one achievable boundary consistently. If the load is admission, expressly account for writes admitted before closure but issued or completed afterward; prohibit admissions after closure and make that residual subject to S-OP-7/X3D assent. If the intended rule is no syscall issued after closure, define a coordinated issuance mechanism that proves it. Extend C-7 with a pause between the successful gate read and syscall, and apply the rule to markers and every write/retry. Do not choose S-OP-7 suppression policy in this unit.

**SOP2-R1-04 (P1): Bound the caller drain wait independently of blocking sink I/O.** [items 16-17 drain and marker; C-7](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/s-op-2/PROPOSAL.md:361)

The writer is told to drain until a deadline and then directly write the marker using a 20 ms reserve. A blocking write to a full FIFO or stalled filesystem does not return merely because that deadline expires; the marker write can block too. No bounded caller wait, nonblocking admitted path, or abandonment of a blocked writer is specified. Thus the proposed stalled-sink control cannot establish the promised normal/cancellation drain deadline. Also, C-7 says exactly one marker per sink even though item 17 correctly forbids a marker when the gate is closed.

**Fix:** Define the deadline on the command/termination path waiting for optional logging, independently of a sink syscall. Choose a mechanism under which a blocked writer cannot hold command completion past that budget, and state any in-flight I/O limitation honestly. The reserved marker is a bounded best-effort attempt, skipped when stopped or when it cannot be attempted within the allowed wait; a time reserve is not a syscall-time bound. Define the final producer/counter cutoff and disposition of unwritten records. Make C-7 observe caller completion under a permanently blocked write and distinguish an attempted/successful marker from a suppressed or failed one. Keep descriptor/custody choices with S-OP-1.

**SOP2-R1-05 (P1): Include the entire encoding in the static size proof.** [items 5, 8 and 14 encoded bounds](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/s-op-2/PROPOSAL.md:207)

The reference MAX_ENCODED formula reserves the header and sums per-kind bounds, without bounding field-key text or including its delimiters. Item 14 repeats the sum as the record assertion. An otherwise ordinary one-field registry entry with a very long Rust field identifier can therefore satisfy the displayed count/value formula while its JSON key alone exceeds 4 KiB. The declared per-kind bounds also need an actual wire representation: K8 claims 24 bytes per variant but a named entry such as "drain-abandoned.error":18446744073709551615, needs 45 bytes. K3 allows a 64-byte code while a JSON string adds quotes; its unrecognized reduction wrapper also needs its own bound. A static assertion proves nothing if these constants omit legal output bytes.

**Fix:** Define per-form bounds on the full encoding: field names and syntax, escaping/elision, wrapper objects, separators, maximum numeric widths, static template and all lawful headers. Have registry! compute or statically prove that total; alternatively give field keys a proved reserve and bound their lengths. Specify K8 as a compact fixed-index representation if 24 bytes/variant is retained, or count named-key bytes. Correct K3 bounds for all variants. Add long-key, maximally escaped string, saturated counter and full-header boundary controls; do not rely only on one oversized payload example.

**SOP2-R1-06 (P2): Use one complete control-escaping rule for both encodings.** [items 1 and 13; C-5](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/s-op-2/PROPOSAL.md:309)

The human path rule calls two ranges "bidirectional controls" but omits U+061C and U+200E-U+200F. The file/bundle JSON rule lists C0/C1, DEL and U+2028/U+2029 but does not require bidi escaping at all, while C-5 requires bidi controls escaped in both encodings. Conversely, the human rule does not name U+2028/U+2029. This leaves the terminal-safety claim and the positive control inconsistent, and valid admitted path names can contain the omitted characters.

**Fix:** Define a common escaping policy covering the complete Unicode Bidi_Control set and the named control/line-separator characters, apply it in both forms to every relevant string-bearing kind, and reconcile items 1/13 with C-5. Add explicit cases for U+061C, U+200E, U+200F, U+2028 and U+2029 and account for expansion in the static byte bounds.

**SOP2-R1-07 (P2): Keep reaped maximum RSS in the promised native unit.** [item 23 provider.process.reaped](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/s-op-2/PROPOSAL.md:502)

The registry specifies max_rss as K2 Bytes alongside rss_unit, but M3-L requires the raw wait4 ru_maxrss value in its platform-native unit, labelled. A native unit is not necessarily bytes. Either treating that raw quantity as Bytes or normalizing it while retaining the native label misstates the measurement. The field schema must choose an unambiguous representation before this row is frozen.

**Fix:** Use a Count for max_rss_native with a closed native-unit code, preserving the sampled value. A separate normalized max_rss_bytes may be added with checked conversion, without relabelling the raw value. State the interpretation of each duration/resource field explicitly and add a C-12/control fixture for both byte and non-byte RSS units.

Rust confirms that `include_str!` embeds file contents into a compile-time string expression; const storage is not itself source classification. [Rust primary documentation](https://doc.rust-lang.org/std/macro.include_str.html). Unicode’s complete bidi-control property includes the three omitted code points named in SOP2-R1-06. [Unicode 17 property data](https://www.unicode.org/Public/17.0.0/ucd/PropList.txt).

**Scope, standing and joins**

The whole OPP:408 subject area is present. The proposal inherits the per-file/retention values while properly leaving storage capability, custody, rotation and retention implementation to S-OP-1. It does not activate public switches/configuration (S-OP-5/-6), the panic hook/descriptor/suppression policy (S-OP-7), bundle writes/consent UI (S-OP-9/O5), OTLP egress (S-OP-10/O4), the cancellation/commit stopping join (S-OP-12), confinement (O7), or restricted raw stderr capture (O9). Headroom and the per-name budget are permissible provisional S-OP-2 mechanisms. The required gate/drain fixes concern this unit’s mechanism claims; they do not decide the deferred suppression or custody policies.

SDK4’s own candidate header does not self-grant authority. APP:3860-3865 explicitly inherits its exact SHA-256 under the satisfied DR-125 row; APP:620-630 separately selects the pinned DRC §8. Those joins match the actual bytes. Citing inherited SF-2 is sound on that basis. Giving bounded structured diagnostics a host-owned typed-record construction path does not remove an SDK operation or grant protocol meaning to stderr. The R1 reading is acceptable within O1(a), subject to the findings; R2’s stricter operational error treatment is also acceptable because the doctor report retains DC4’s name-plus-scrubbed-message rule and unchanged schema.

F03’s resolved-secret exclusion is preserved, and analyzed-source confidentiality is not mistaken for that secret rule. P3 has no kind; raw stderr/fault/refusal detail, nonces, caller correlation text, environment values, error messages and panic payloads have no operational field. Future DR-108 handles remain names/presence only and grant no credential-storage activation. CH13’s ordinary resolver/provenance rule is respected: operational filters/settings cannot quietly read RUST_LOG, backtrace variables or OTEL_*; legitimate platform/resolver environment access remains on OPP’s owner exception list.

M3-L is used as a **draft dependency**, not an accepted authority. The provider table agrees with its record join: stderr/fault detail becomes length/truncation without a digest; closed fault/terminal reasons are codes; admitted host transitions supply progress; resource assertions are not progress; identities use host-held values. Reducing refusal detail and excluding nonces apply the same closed-vocabulary rule without changing CC’s wire bodies. The empty detailCode table preserves M3-L’s default treatment and gives no D9 authority. Item 24 is a future recording unit, not a current verify_design application.

**Classes and every kind**

Keep **RuleId at P2** (R5). That is the accepted OPP class, stays valid when policy becomes project-authored, and avoids changing privacy with the currently bundled-pack population. Digests remain classified by provenance: sealed identities/closures P1; fingerprints of arbitrary text/source P3. The explicit limitation on malicious code choosing codes/counts/timings is honest; these findings do not demand general covert-channel confinement.

| Kind | Assessment |
|---|---|

| K1 Code | P0 is right for approved closed codes. Any-crate table provenance is not closed by constness: SOP2-R1-01. |

| K2 Count/Bytes/Elapsed/Flag/Errno | The numerical kinds fit P0 for the named approved measurements; Errno restriction and secret-length exclusion are right. Clarify asserted-resource provenance and actual units. Numeric types do not prove absence of deliberate information-flow signalling. |

| K3 RegisteredCode | P0 exact match to a host-owned admitted table, emitting that entry rather than input bytes, is sound. Empty RustDetailCode is appropriate. The fallback and code encodings need complete bounds: SOP2-R1-05. |

| K4 Version | P0 is appropriate for release constants or admitted signed-manifest version fields; preserve that admission boundary and encoded bound. |

| K5 AdmittedId | P0 is appropriate for the specific admitted release/signed catalog entries, never a caller-shaped string. The catalog entry type must mean admitted provenance. |

| K6 CodeLocation | P0 is appropriate for the host build’s code location. Dependency/absolute paths must encode as external, with line only. Workspace-relative must mean an actual workspace path, not merely a prefix match allowing dot-segment escapes. C-9 is a useful independent release check. |

| K7 Reduced | P0 length/truncation with the text discarded and no digest follows OPP and OP-R2-NB-01. Capture metadata must distinguish total observed from the retained prefix. |

| K8 Counts | P0 closed loss counters are appropriate. Define compact/indexed or named-key encoding and its actual maximum: SOP2-R1-05. |

| K9 IdentityDigest | P1 is right for the listed typed sealed identities and signed artifact-manifest digest. Raw file-content digests remain excluded. A parser-produced digest type alone must not substitute for an admitted owning identity. |

| K10 PathRef | P1 anchored ephemeral HMAC correlation is sound for this non-authoritative role. The 256-bit process key is not persisted; a 64-bit tag is a correlator, not a collision-free identity. Rejecting an unkeyed hash of guessable paths is right. |

| K11 ProcessId | P1, sourced only from self or a host-spawned process, is right. It remains an attribute, not the universal correlator. |

| K12 ProjectPath | P2 with admitted discovery/snapshot/fact-anchor provenance is right. Names may themselves be sensitive; that is a stated exclusion rather than secret-value clearance. Escaping/static elision need SOP2-R1-05/-06. |

| K13 Position | P2 admitted line/column is right; no arbitrary source value or worker echo should be treated as an admitted span. |

| K14 RuleId | P2 is right; do not downgrade to P0 based on today’s bundled packs. |

| K15 DeclaredName | P2 declared variable/future handle name is right. A declaration does not authorize the value, and DR-108 remains deferred. Apply the common escaping rule wherever names can contain controls. |

Constructor closure also requires implementation ownership: no blanket text/byte adapters, arbitrary deserializer, generic mint bypass, publicly forgeable scope marker, or raw parsed-identity conversion. The law states the right owner/provenance requirement for P1/P2; the code unit must make that ownership real. Request allocation remains the only RequestId source, ExecutionId survives CommitUndetermined, RunId comes only from committed publish/stored read, and allocation failure yields only the fixed emergency line. The conditional storage event needs the owned outcome constructor noted below.

**Sinks, registry and recording**

All five OPP sinks are present with the correct ceilings. Static field projection is preferable to rejecting an entire mixed-class event. Internal P1 correlation headers must also be excluded from the OTLP encoding; item 13 expressly does so. The pre-scope buffer adds no persistent authority, and envelope diagnostics is the existing P0 loss-summary carrier, not a route for ordinary events. A running-registry bundle projection is the right policy source, but SOP2-R1-02 closes its serialized input boundary.

All **26** initial names satisfy the three-segment grammar and fit the bounds. Every M3-L:412-419 named need has an event: spawned/ready/stage/terminal/reaped, both cancellation edges, liveness missed, progress absent, stderr reduced and fault reduced. Host-held Plan/Execution/universe correlation and the reuse event align with the draft. Required identities beyond RequestId are phase-lawful; provider scope construction must retain ProjectId as M3-L:378 requires. Every export candidate remains P0-only **after projection**, including removal of universe/identity headers. No export is authorized at r1. The RSS field needs SOP2-R1-07; give abbreviated fields concrete K1-K15 types in the generated code-unit registry.

The SDK4 JSON pointer and DRC line-576 before passage are correct. The two overlays are sufficient parent joins if the later subject manifest pins this complete accepted proposal and the lock binds that record. Deferring recording until the first M3-O code unit is consistent with the stated workflow and does not itself accept or apply anything. Preserve the insertion wording and operational scope noted in SOP2-R1-NB-05. The later recording requires its own ACCEPT-DESIGN-UNIT and a single-string subjectManifestSha256. This r1 review has neither a subject-manifest verdict nor an inventoryCandidateAssessment.

**Controls C-1 through C-12**

| Control | Can it falsify its named claim? |
|---|---|

| C-1 | Yes for direct unsafe field types and typed scope/bound violations. Add approved-table bypasses, generic/From/mint adapters and wrong outcome/scope combinations; a missing const alone is insufficient. Match the intended diagnostic rather than any unrelated compilation failure. |

| C-2 | Yes for registry grammar/uniqueness/drift and constructor ownership. Include table admission, complete retired descriptors and the actual encoded-size formula. |

| C-3 | Yes for dependency event routing. Instrument field visitors/formatters too: absence of sink bytes alone does not show those callbacks never ran. |

| C-4 | Yes for plaintext/fingerprint leakage. Add poisoned serialized bundle records and a known credential-shaped P2 name; include unknown/retired schemas. |

| C-5 | Yes once its complete escape policy agrees with both encoders; include all omitted bidi/line-separator characters. Path-tag comparisons are probabilistic and do not confer identity authority. |

| C-6 | The synthetic guard corpus checks the guard, not construction closure. Define the expected treatment of valid P2-name matches separately from forbidden-value leakage. |

| C-7 | Yes for queue count/byte limits, headroom, nonblocking producers and exact loss accounting. Repair the gate race, blocked-syscall drain guarantee, marker exceptions and full encoding boundaries in SOP2-R1-03/-04/-05. Exercise EACCES/ENOSPC/EIO and short writes, not only FIFO saturation. |

| C-8 | Yes for runtime lawful headers/emergency allocation; add the storage outcome/Run pairing and stored-read/ephemeral cases. |

| C-9 | Yes for absolute/dependency code paths. Also reject apparent workspace prefixes with traversal or a non-workspace origin. |

| C-10 | Yes for the named hidden-environment inputs; hold declared resolver input fixed and compare effective sink/filter/bound settings as well as emitted bytes. |

| C-11 | Yes for semantic/termination invariance; compare deterministic results, not nonsemantic counters/timestamps. Include optional-sink failure/init failure, saturation, and the accepted concurrency-1/automatic comparison. |

| C-12 | Yes for the provider disposal table; include registered/unregistered detailCode, health/nonces/refusal cases, asserted resources, and native RSS units. |

These are proposed controls, not results. S-OP-11 authors them and M6 qualifies them; no test evidence is inferred from this law review.

**Nonblocking observations**

**SOP2-R1-NB-01: Keep the P0 definition consistent with provider-asserted resources.** P0 defines counts/sizes/durations as host-measured, but items 22 and 23 correctly identify resourceReport quantities as provider-asserted P0. These are different provenance claims. The closed numeric carrier can remain a nonsemantic measurement under the express covert-channel exclusion; it must not be described as a host-measured fact or used as progress.

Name the approved asserted-numeric category explicitly in P0, retain provider-asserted labels, and let C-12 verify that resource assertions never become admitted progress.

**SOP2-R1-NB-02: Distinguish valid P2-name scrubber matches from vocabulary defects.** A lawful admitted filename can contain a known credential-shaped substring, for example password=CANARY. DC4 expressly permits sensitive operator-chosen names. A final byte scrubber may match that valid P2 value even though no forbidden secret value entered a field. Calling every such match a vocabulary defect conflates provenance with pattern matching.

Specify whether the guard excludes permitted P2-name spans from credential matching or reports legitimate disclosure-tier matches separately. Include a known credential-shaped filename in C-4 and state its expected guard result; do not count expected escaping as a defect.

**SOP2-R1-NB-03: Make the outcome-dependent Run header an owned constructor join.** The normative phase rules are correct, but a fixed Event::Requires set does not by itself tie a runtime outcome Code to the optional Run header. The code unit must not expose a free struct/outcome pairing that allows CommitUndetermined to be emitted through a Run-bearing scope.

Use an outcome/receipt-aware private constructor or equivalent checked scope transition for storage.commit.classified; exercise both wrong pairings in C-1/C-8. Seal scope/marker implementations and keep generic From or mint adapters on the audited owner list.

**SOP2-R1-NB-04: Retain member-specific P2 consent in the later bundle unit.** A bundle-wide P2 ceiling is a necessary bound, not a substitute for the accepted plan requirement that P2 members need their own consent. The draft leaves the flow with S-OP-9/O5, which is the right owner boundary.

Carry OPP:356 into S-OP-9; an approval for one P2 member or class must not implicitly authorize another. r1 need not decide that UI.

**SOP2-R1-NB-05: Preserve exact recording text and its operational scope.** The SDK4 pointer and DRC line-576 target are correct, and recording with M3-O plus its own manifest/review is appropriate. The DRC after text changes meaning. to meaning;, so it is not literally insertion-only. Also, free text reaches no sink should stay explicitly scoped to operational records, since the doctor report retains its accepted disclosure tier.

Preserve the original punctuation when inserting the reduction sentence and qualify the appended SDK4 sentence as operational-record sink law. The later recording review must verify exact selectors/parents, include the accepted proposal bytes in its subject manifest and preserve the DR-114 report split.

**SOP2-R1-NB-06: Specify sink-local final loss snapshots and typed capture summaries.** The marker has a sink field, while the counter description names 40 counters plus first errors per sink; sink-local versus invocation-global totals should be explicit. A once-only marker also needs a producer/counter cutoff. Reduced::of(text, truncated) must obtain the total observed count from capture metadata if text contains only the bounded prefix.

In the code-unit design, define counter ownership, one disposition per lost sink projection, the final snapshot after producer admission closes, and a capture-owner summary carrying observed bytes/truncation. Clarify envelope routing: item 12 every sink does not make ordinary events eligible for diagnostics, whose row permits only the loss summary.

**Citation spot checks**

Confirmed the OPP identity table, privacy/digest rules, sink ceilings, bounds, crash stopping policy, member consent, enforcement, successor row and controls; M3P:89/92/160/174; APP:620-630 and 3860-3869; SDK4:78-82/99-105; F02:179-197; DRC:513-601; DC4:1005-1086; F03:45-50/56-59/65-67; CH13:59-62; CC:9-65; RPP:117/441-445; DLV:857/1133; NE:2025/2967/3160-3164; QG:403-441; SLJ:481; and the listed historical OPV10 passages. The F03 line-45 correction is right. Prior review findings OP-R1-03/-08, OP-R2-NB-01 and OP-R3-NB-02 were read directly. The scalar subjectSha256 in [review.json](review.json) is the pinned successor text hash.
