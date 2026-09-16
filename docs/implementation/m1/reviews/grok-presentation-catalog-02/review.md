# Independent Grok review: presentation-catalog02 original unit

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-presentation-catalog-subject-02`
**Manifest SHA-256:** `3d5d377df4d5b57a5245e9746dfb2db0659dc82688141a54296f2d2a45c9272f`
**Members:** 22
**Verdict:** **ACCEPT WITHIN STATED REFERENCE SCOPE**

This is not product catalogue delivery, signature verification, Run admission, report integration, browser qualification, or milestone/source promotion. Catalogue03 was withdrawn; this 22-file freeze is the intended target. Joint10 later combined acceptance does **not** waive this unit.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not executed against and not written.

| Check | Result |
| --- | --- |
| Manifest | `3d5d377d…272f` matches declared and adjacent copy |
| Files | 22 listed = 22 walk |
| Pins | **12/12** |
| After | frozen hash unchanged |

No modes/symlinks listed.

## Documented checker and controls

Private `check.py`: **16/16** groups, 12 pins, exit 0. `mutants.py`: **9/9** behavioral controls killed; **CAT-M3** canonical-size deletion **survives** as classified (not claimed as a kill).

## CAT-F1–F7 (review01 → this freeze)

| Id | This freeze |
| --- | --- |
| **F1/F2/F3** | Closed source states: `retained` / `not-retained` / `corrupt`. Both trees omit the reserved path → `no-catalogue-declared` (not a retention failure). Unassociated bytes refuse. Missing selected descriptor in a retained listing → `descriptor-not-declared`. |
| **F4** | Singular authenticated **release association** (see below). |
| **F5** | Control/bidi characters refused in name/description/parameter text. |
| **F6** | Recipe `targetBounds` is `finding-fingerprints` with RepairPreviewParams limits; extra parameter keys refuse. RecipeKey omits `closureId`. |
| **F7** | Receipt copies `tree`, `platform`, `protocolMajor`; same-platform check. |

Independently reproduced (**24/24**), not only author tests.

## Singular authenticated association: who admits, how retained

**Law.** After existing signed closure, release, and Run admission, the host supplies: exact retained `ReleaseCapabilityRegistryV1` digest, **one** designated presentation `catalogClosureId`, that id ∈ Run `Plan.semanticClosures`, and same platform. Capability description keys must be declared by that release and listed in that closure. A second closure cannot reuse the first authority (`RELEASE-CLOSURE`). Rules/recipes may live in other closures **without** capability declarations.

**Who admits it.** Not this reference. `capability_authority` / `admit_catalog` join **synthetic host custody dictionaries**. Matching caller declarations to a caller-copied digest is **not** authentication (independent probe documents that the join succeeds whenever the caller supplies a consistent pair). Product must construct private admitted handles.

**How it is retained.** With the Run’s native release context. `select_descriptions` requires a retained receipt for `source_state=retained`; `not-retained`/`corrupt` → `unavailable` (`catalog-not-retained` / `catalog-corrupt`); historical Runs without the association disclose unavailability and do not rewrite identities. Injecting a new closure into an already retained Plan is a host Plan-minting duty, not performed here.

**Sufficiency.** Sufficient as a **proposed association law** over disclosed synthetic preconditions. **Not** sufficient as product admission, signature proof, or retained Run lookup.

## CAT-M3 redundant canonical-size guard

Independent: pretty-printed raw SHA-256 is the tree binding; canonical bytes ≤ pretty raw; 4 MiB+1 refused as `BYTE_LIMIT_OR_TYPE` before canonical size. Under this exact-JSON codec, extra whitespace cannot enlarge canonical form past the raw cap. Surviving deletion of `reference.canonical(data)` is **not** a reachable size bypass. Classification accepted.

## Joint10

Joint10 `composed-sources/presentation-catalog.schema.json` is 7058 bytes but sha256 `df6a1133…5211`, **not** this freeze’s `8ba7c6b4…5097`. No byte-identical mapping of this schema into joint10. Joint10 combined acceptance does not rewrite or waive this 22-file unit. Catalogue03 remains withdrawn.

## Must-fix / should-fix

None in the stated reference scope.

## Remaining duties

Product signatures; actual release/Run admission and retained lookup; report carrier binding (receipt + descriptors, four feature placeholders); core completeness gate; renderer HTML/CSP; browser. RP-DO-04 redaction remains a separate owner.
