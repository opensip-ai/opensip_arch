# Independent review — owner402 supplemental documentation correction

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. Bounded documentation-consistency re-review; document and model only, **no native jobs run**
as instructed.

**Top verdict: ACCEPT-DESIGN-UNIT. `requiredFindings: []`.**

My owner401 RF-1 is closed, and both of my non-required observations are answered. The delta is exactly
what is claimed — I verified it member by member against my own retained 401 extraction, and the
freeze script enforces the same claim internally.

---

## 1. Verification

### Pins and members

| Artefact | Declared | Match |
|---|---|---|
| `…/trials/initial-root-binding-proposal-402/subject.tar.xz` | 95 948 B, `92d8b3f45ba5d6910c5b39eb4564b5dfafbb2b693844c1ed764df31dd3fa301b` | ✓ |
| `…/trials/initial-root-binding-proposal-402/subject.json` | 8 137 B, `ebbef2b3945c46d457b8c321780cc1e42f467ab2ae506fe05816f625a8ca7302` | ✓ |

Both verified **before** extraction; extraction only into this review directory. **52 / 52** members
verified byte-for-byte and by sha256: 0 missing, 0 extra, 0 mismatched, 0 unsafe. The trial directory's
`archive-pin.json` names 52 members at the same digest, and its `README.md` is byte-identical to the
archive's `README.md` member (`ed58c816…`).

### Anchors

**47 anchors; 46 match live; all 16 product anchors match at `cd5af4d`.** The single live mismatch is
the declared historical `crates/platform/src/filesystem.rs`: 73 907 B / `9a02dcbb…` at `cd5af4d`,
now **81 813 B / `11ab4ced…`** live, because the source400 module declaration and export are integrated.
That is the expected movement, the anchor is declared historical, and no pin was edited.

### Context, checked rather than assumed

Product is clean at `883f963` with 46 inputs / **35 inventory** / **54 contract** successors, and the
integrated `crates/platform/src/filesystem/directory_publication.rs` is **byte-identical to the
candidate I accepted in the source400 review** (`1f10531ad3046d53863aaab2b263cff6a4487f7ea2feb05bda7a4f05cc66a916`,
27 048 B). The integration is faithful to what was reviewed.

---

## 2. The delta, verified against my own 401 copy

Every member of 402 compared against my own retained 401 extraction — not against the manifest, and not
against the author's account:

| | Result |
|---|---|
| Members | 49 → **52** |
| New | **3**: `correction402.json`, `freeze402.py`, `prior401-findings.json` |
| Removed | **0** |
| Changed | **exactly 2**, both `README.md` files |
| Inherited members byte-identical | **47** |

`owner-draft.md` is byte-identical (`35953d09…`), as are every model, schema, checker and result file.
So there is no semantic owner, node, count, schema or API change — the claim holds at the byte level.

`prior401-findings.json` is **byte-identical to my own owner401 `findings.json`**
(12 200 B, `7dc59659c26d902b15f952d82c4821f8243386df13b508d2011d2d68ddeb91e8`), so the prior report
travels into the archive unmodified.

`correction402.json` records `changedInheritedMembers: [README.md, diagnostic-draft/README.md]`,
`unchangedInheritedMembers: 47`, `freshTests: []`, and pins the predecessor manifest at 401's
7 680 B / `b00b6948…`. Every one of those matches my independent measurement.

**The freeze script enforces the same claim internally.** `freeze402.py` extracts 401's members while
verifying each against 401's declared digests, applies exactly one title replacement plus one appended
paragraph to `README.md` and two replacements plus one appended paragraph to the supplement README, and
then asserts `sorted(delta) == ['README.md', 'diagnostic-draft/README.md']`. It also refuses to run if
the target directories already exist. The externally verified claim and the internally asserted one
agree.

---

## 3. Closure of owner401 RF-1

The stale sentence is gone. Where the supplement README previously ended *"Other owner399 issues and
root EEXIST concern remain unresolved"*, it now reads:

> The containing owner401 resolves the prior owner399 findings and the root EEXIST concern in its
> protocol: clean loss requires AlreadyExists AND typed Unchanged; Indeterminate stops. **This
> diagnostic supplement itself does not test native publication/error dispatch.** The complete formal
> passage/schema/reference selection, generated bindings and native implementation remain outstanding.

My finding offered two remedies — correct the claim, or scope the sentence to what the supplement does
not cover. This does both, and the protocol summary it gives matches the owner draft's own wording,
which I re-read in place. **RF-1 is closed.**

---

## 4. Both observations answered

**O-1 — the helper does not authenticate its inputs.** A new paragraph states it directly:

> The helper loads baseline/schema files by path. It does not authenticate those inputs itself; its PASS
> describes the composition against the observed bytes, not arbitrary future replacements. Exact outer
> source anchors and the eventual formal selected source maps must bind those bytes.

That is exactly the limitation I recorded, in the terms I recorded it, plus the right forward
obligation.

**O-2 — mutable draft versus frozen snapshot.** Root's qualification is correct and is a genuine
sharpening rather than a restatement. The supplement's title changes from "Mutable diagnostic
reconciliation draft" to "**Diagnostic reconciliation reference draft — frozen evidence snapshot**",
and both READMEs now distinguish the two things that were conflated: the *originating working draft* is
unselected and mutable, while *these packaged bytes* are immutable once frozen. The main README states
the consequence explicitly — "unselected draft status does not mean its frozen bytes may be edited" —
which forecloses the wrong reading of my observation.

---

## 5. Standing coherence

The request flagged the one thing that could look like a defect and is not: the inherited
`owner-draft.md` still carries the `proposal401` heading. That is correct practice — its bytes are
401's, so relabelling it would falsify a frozen body to fix a caption. The main README says so in
terms:

> The inherited owner-draft.md intentionally retains proposal401 heading: its normative body, all
> models, schemas, checkers and evidence are byte-identical to401.

I verified that statement (`35953d09…` on both sides) rather than accepting it, and I raise no finding
from it. The same applies to `checks-401.json`, `source-anchor-verification-401.json` and the inherited
stdout/stderr files: their names carry their own provenance, and the supplement README's phrase "the
frozen401 checks remain historical evidence" is accurate.

The package also claims no test rerun, consistent with `correction402.json`'s `freshTests: []`. As a
spot check — **not** offered as fresh 402 evidence — I re-ran the inherited checks on the unchanged
bytes: 39 surface checks PASS and 22 diagnostic composition checks PASS (319 codes, 117 unchanged
top-level statements), both regenerating their frozen outputs byte-identically. The inherited evidence
is intact and still reproducible.

---

## 6. What remains open — unchanged by this unit

Nothing in this correction narrows the outstanding work, and the package says so. The five composition
gaps remain; the publication model still does not model native errno or post-check classification; the
two new `INSTALLATION.*` codes remain unemittable against the selected 317-code enum until a schema
successor lands; and the complete formal passage/schema/reference/generation unit, generated bindings
and native implementation are all still required before any owner or schema activation.

I record without reviewing it that root reports a contract-generation closure pinning an older
`tools/verify_design.py` (28 690 B) against the current 33 654 B / `2764cf7b…`, with the entrypoint
refusing on input digest, and a missing generator binary being rebuilt. That is outside the frozen
candidate, I did not verify it, and no action on it was requested. `M/initial-root-binding-reconciliation`
is likewise root's working area, not part of this unit and not reviewed.

---

## 7. Limits

- **Level:** archive and anchor verification, member-by-member delta against my own retained 401
  extraction, freeze-script reading, and a reproducibility spot check of inherited evidence.
- **No native jobs**, as instructed. No portable or native test is claimed as fresh 402 evidence.
- **Not qualified:** native eligibility, current authority, P0 construction, shared budgets, profile or
  custody qualification, crash and power-loss behaviour, Linux, release.
- **Not re-reviewed on their merits:** the owner body and every model, schema, checker and result —
  they are byte-identical to 401 and carry that review's assessment, which stands unchanged.
- **Not a formal passage successor.** Selection still requires a separate complete formal
  passage/schema/reference/generation unit with its own review and root assent.
- **Unselected references remain unselected:** this owner, S9.3, `store-instance-lineage.v1.json`,
  `host-foundation-completion.v2.md`, 215.

---

## 8. Context HEADs — as of 2026-09-21T16:40:35-07:00

| Repository | HEAD | Subject |
|---|---|---|
| architecture | `35bb623b76bb6ec259946c25092f20fa71aa9328` | "Clarify publication receipts and freeze initialization reconciliation corrections" |
| product | `883f9634da5ffc422f07c8ac699a98ffdf7d4338` | "Add retained private directory staging and exclusive publication" (clean) |

HEAD claims are as of that sample only; the byte pins above are the authority.

---

## 9. Attestation

Read-only against live, frozen, history, product and locks. No byte edited, no pin edited, no select
script run, no native job, no commits, no pushes. All writing went into this review directory;
extraction went only there.

This grants no root assent, no formal selection, no passage reconciliation, no native eligibility or
writer permission, no current authority, no P0, shared-budget or profile qualification, no S9.3 or 215
adoption, no whole-M2 approval and no release qualification. Every earlier report — owner397 and its
fact addendum, owner399, owner401 and the source400/formal34 review — is untouched and keeps its own
standing.

Reviewer: Claude Opus 5 (1M context).
