# Independent scoped review — reader 232 r2, distribution 229 r3, prose 227 r9

Three bounded reviews of ROOT-authored frozen bytes. **Not cumulative approval, not readiness, and
not a review of my own 230 author work.** No repo/product/candidate edit, commit or push; output only
in this directory. Claims are graded as shape / conditional / native throughout.

## Verification and reproduction (all three)

- Each archive pin and EVERY `subject.json` member (path, sha256, bytes) verified from the tar before
  extraction into `inputs/`; all three re-verified at the end (`claude-out/pin-verification.json`).
  232 r2 `f1a3d582…714d` (19), 229 r3 `edde8b4f…6b4e` (88), 227 r9 `818604dd…6e44` (211).
- Runs used fresh output-local copies with only the runners' own output dirs/files removed;
  reference-201 reached through a symlink to my verified extraction; Python 3.12 reference env;
  every script hash-asserts `canonical.py` d47f25db… (and 229 the kernel). **No script edited.**
- 232: 42 checks → **byte-identical** to `reader-check-r3.json`; 8 variants → mutant sources
  identical; `results.json` equal to the frozen one EXCEPT two keys the frozen file has and the
  frozen runner does not write: per-variant `secondaryDiagnostic` and top-level `scope` (the
  "explicitly added diagnostic metadata" root named). Every assertion and hash matches.
- 229: 77 checks → **byte-identical** to `distribution-check-r6.json`; 10 source variants
  (mutants-r4) and 24 guard contracts (guard-r2) regenerate **identical**.
- 227: every `*-before-prose-reconciliation.md` is byte-equal to the r8 file I verified earlier;
  outside those four documents and the beforeimages, r9 is identical to r8. Nothing re-run.

---

# Part 1 — trust-reference-reader 232 r2 (structural; no graph, custody or authority)

## Confirmed

- **Present-field / matching-branch extraction, not a kind cross-product.** `oneOf` requires exactly
  one matching branch, `anyOf` follows all matching, `if/then/else` follows the taken branch,
  `properties` only when present, `items` per index. On my own P2-shaped capsule (accepted heads, a
  RECOVERY role with accepted standing, both restriction slots, reset, ceremony, staged payload, live
  batch, history) the reader returns exactly the 30 reference-shaped objects a brute-force instance
  scan finds — none missed, none phantom, null branches produce no edge (probe D).
- **No registered field is unreachable by the runtime walk.** The registry walks every schema key;
  the runtime follows only `properties/items/oneOf/anyOf/allOf/then/else`. I parsed all 118 registry
  paths: none passes through an unfollowed keyword (`additionalProperties`, `patternProperties`,
  `prefixItems`, `contains`, `not`, `if`, …) (probe A). 118 == `reference-fields.json`.
- **Raw signed `BlobRef` stays raw.** Collection `objects`, `expectedDefinition` null; `decode_edge`
  re-hashes and returns no edges; it cannot be parsed as a private record. The 229 anchor yields
  exactly six such edges.
- **Exact bytes and locators.** Canonical/size/shape before anything else; target re-hash + length;
  NodeRef targets validated under the FIELD's definition (the same bytes through another field
  refuse); event `store`/`sequence` and publication `previousCapsule` bound to decoded bytes.
- **Pending codecs refuse** `codec-unavailable`; clock source selects S4 / S4.5-epoch / challenge;
  observed-context selects only the restriction input. `edge_limit` can only lower 131072 and
  rejects bool, negative and float (probe G). Unknown field names hit `unmapped-reference` at import.

## Findings

### V-1 (medium, test adequacy) — 33 of the 118 registered fields are ever extracted by the corpus

Instrumenting `REGISTRY` while running the 42 checks: 33 rows touched, 85 never. 26 owner
definitions are never exercised at all, including `RoleRecordV1`, `AcceptedStanding`,
`AcceptedRootHead/MetadataHead`, `StagedPayload`, `LiveBatch`, `BeginBatchV1`, `SourceFence`,
`ClockPhase`, `OriginalContextV1`, `RootAdmissionNodeV1` (non-anchor), `MetadataAdmissionNodeV1`,
the three S4/S4.5 inputs, `RestrictionObservationInputV1`, `SignedTimeSourceV1`, and the
continuity / creation / restore / termination / standing-reset events. The only capsule in the
corpus is P0 (two edges). README's headline is "118 exact owner/schema-pointer fields"; the tests
show the mechanism on a quarter of them. My probe D suggests the capsule paths are right, but that is
my evidence, not the subject's. **Action:** one maximal positive fixture per root type with an
`exact()` pointer map (a P2 capsule, a full descriptor, BeginBatch, each time input, each event
kind, ordinary/recovery root nodes, metadata node), and assert `hits == set(REGISTRY)` so an
unexercised field fails the run.

### V-2 (low–medium) — "field-specific target" holds for NodeRef, not for EventRef

Every `EventRef` field has `expectedDefinition: TrustEventV1`, the nine-kind union. `decode_edge`
therefore accepts ANY event where a specific one is meant: a CREATION event decodes successfully as
the target of a role event's `clock.by`, which must be a clock-write (probe E). The same holds for
`staged.by` (a recovery PRESENT), `ceremony.begin`, `revokedBy`/`quorumLostBy`, `reset.by`
(standing-reset), `beginEvents`, `LiveBatch.members.by`, `sourceFence.by`. README says "field-specific
target shape refuse substituted records" without that limit. Kind/role/event joins are semantic and
may be owed elsewhere, but the variant is knowable from the schema field exactly as it is for
`ClockWriteEventV1.evaluation`. **Action:** map EventRef fields to their variant definition where
the owner fixes one (`clock.by` → `ClockWriteEventV1`, `reset.by` → `StandingResetEventV1`, …), or
narrow the README sentence to NodeRef.

### V-3 (low, hardening) — edges are plain dicts

`decode_edge` trusts `edge['expectedDefinition']`. A hand-made edge with `expectedDefinition: None`
and `referenceType: "NodeRef"` skips all shape checking (probe F). README states edges "must come
from this extractor", so this is a declared internal contract, not a hole in the claim; an opaque
frozen edge type (or re-deriving the row from `(owner, schemaPointer)` inside `decode_edge`) would
make the contract structural instead of conventional.

### V-4 (note) — hash-only locators are not edges

`previous`, `previousCapsule`, `NativeBefore.sha256`, `intentDigest`, `sourceFence.sourceBefore`,
`RootBinding.rootDigest`, `ClosureId` carry digests without a length and are not terminals (probe B
lists the inline sha256-bearing shapes: `NativeBefore`, `FileRef`, `TreeEntry`,
`ArtifactCaptureObservationV1` — the last deliberately non-dereferenceable). Correct for a
reference reader; worth one README sentence so nobody takes "all references" to include predecessor
links, which are 222's proof joins.

Scope honesty is good: single record, no graph budget, no custody, no eager old-T traversal, internal
expected type. The packaging-error disclosure is accurate (the r2 archive is complete).

---

# Part 2 — core-distribution 229 r3 (fixes to my r2 R-1…R-3 only)

| r2 item | r3 state | evidence |
|---|---|---|
| **R-1** chain-gap / backdated untested; bound and budget guards surviving | **closed** | cases for gap, wrong predecessor and backdated exist; my all-reasons survey now kills every reason except four `ERROR-not-a-kill` (each has a positive label hit) and `symlink-resolution-bound`, which survives label-deletion ONLY because the unconditional loop-exhaustion `raise` carries the same label — exactly what `R3-VALIDATION-NOTE.md` says, and the r4 `symlink-bound` SOURCE variant covers it. Budgets: exact-fit admits, one object or one byte short refuses, raising either limit / bool / zero refuses `work-profile` (W1–W7) |
| **R-2** implied vs declared directories | **closed** | `kinds.get(parent) == 'dir'`: removing `bin`, removing an intermediate row whose own parent is declared, a symlink as parent, and a symlink inside an undeclared directory all refuse `tree-parent-type`; a symlink to a declared directory and an empty declared directory admit (T1–T6). The fixture now declares its three dir rows |
| **R-3** meaning of "complete" | **closed** | OWNER states the manifest DEFINES the chain and that later-root envelope/quorum authentication is upstream |

Remaining, low: `conditional_embedded_head` still hard-codes its own 268435456 byte check while
`verify_anchor_bindings` takes lowerable limits — harmless, but the two budgets are separate and
the selector's is untestable at fixture scale. The first failed r3 fixture and the survey
correction are preserved and described accurately; `distribution-check-r5.json` is an empty failed
output, as the note says. R-4 (the 215 restriction-projection delta) stays queued by root's statement.

---

# Part 3 — 227 r9 prose reconciliation (no schema/model change; nothing re-run)

I checked each of the nine former numbered overrides against the new single text:

| former override | retained in r9 |
|---|---|
| 1 accepted events omit `refusalReason`; refused require a vocabulary member | yes — "required non-null iff `refused` … forbidden when `accepted` (two closed shapes)" |
| 2 three clock sources; challenge is not a time evaluation; RECOVERY-EPOCH reconstructible; re-run kernels | yes — three bullets plus "Re-run the bound source kernel; output shape … never establishes these effects" |
| 3 private `host-trust-admission`; no public command / exemption / report-only publisher | yes — and role derivation is now named as owed producer work |
| 4 inputs may be built during the invocation; upstream only; stable operation node; continuity binds the intent; late BEFORE images on events | yes — and the contradicting author sentence ("only objects that existed before the operation began", "must not name … a logical-before hash") is gone rather than left beside its override |
| 5 clock-write vs observed-context vs the single not-required reason; no S4 substitute | yes; the safe-ABORT old-T exception is stated separately and narrowly |
| 6 private termination sets target state AND clears ceremony; TRUSTED entry clears both slots | yes, in both the role-event and termination sections |
| 7 `COMMITTED` batch termination after the COMMIT events, same publication, no tenth event | yes; the author's open question is resolved, not deleted silently |
| 8 `staged.by` = first canonical successful recovery-PRESENT; re-observation preserves it | yes (section C unchanged) |
| 9 226 r3 already covers null entries / ABORT annotations / source heads | yes (section D) |

The schema agrees with the prose: `OperationInputV1` has 14 variants, the last
`host-trust-admission`, and continuity's kind is `transition-intent-input`. No stale "13 values",
`continuity-input`, "226 r2" or "222 r4" remains. I found **no narrowing and no new authority**: the
`s4` bullet's "P0 requires the initial L write" is the existing S4 fresh-install rule (F := tEval,
L := A), not a new one.

Two small items:
- **P-1** EVENT-JOINS cites "[O 224 / 226 r3 / **222 r7**]" while CODECS builds on "222r6", and the
  latest FROZEN 222 trial is r6. Cite the frozen revision, or say r7 is a working draft.
- **P-2** README's "one current account" is accurate for the three reconciled documents;
  TIME-INPUT-JOINS and PROOF-NODE-JOINS were not part of this reconciliation and I did not re-read them.

---

## Limitations

232 probes call the owner's unmodified functions on my own synthetic values; the P2 capsule is
shape-valid, not a reachable state. Registry coverage was measured by wrapping `REGISTRY` lookups,
which counts a field as exercised whenever it is extracted, whether or not its value is asserted.
229: only R-1…R-3 were reviewed; my survey disables a reason label, so guards sharing a label are
disabled together. 227: prose only, against the frozen before-copies; no 215/222 review implied. No
harness failure occurred in this task; two of my re-used 229 probes (S3, S5) refuse `tree-order`
because they add a directory row the r3 fixture now already declares — a stale probe, not a defect,
left in the output and superseded by the targeted probes.

## Pins

232 `reference_reader.py` 9ff48d10489967a9261cdf223e6ee25323ae852c3e414e00301b2b036cf3f599 ·
`check_reader.py` cd1122366436482b1a4c4b2fdfabe4551f1ebabc753e46743ee9b87e15b0c092 · schema
d9ac024357c1645727449bb38f940dbf886244e1d3959998a3e28b64d6857968
229 `distribution_model.py` eb6fc68c98355fc17ac0de1a6a8bdd69010979dda95ef27f1b97de1fad7da1f6 ·
`check_distribution.py` 6680597c92bc7708bde9ec5027922e70dbcb7ccde2e21b3ed165ac57de46d653 ·
`OWNER.md` f0860bf6e5adb39ca9f724dbc437691c4ae75862050c8fb37eec00d3f9be0f92
227 `EVENT-JOINS.md` 69000c34d63da11e661f35ec84d70c1e4b81fc3f413a7c0d7cca0244cc7fa806 ·
`CODECS.md` 772a297543fc430ae85218e4ba33e6a4555a6f0bb162dea9de586a130e384264 ·
`PENDING-JOINS.md` a4e6262d7119670c2e5532326082e6ec003c9a3b4a2308f87403abed0458acaa ·
`README.md` 3e0e5ca235d2d321efeaaddcbf09feb997ccc8da01044902f802eab9e0f123b9
Reference: `canonical.py` d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442 · kernel
df45c9c5444790b5f89b458efbee5cb068781d5fc1e82483c2678d2f10712299
