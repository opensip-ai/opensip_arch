# C1c-1 binding review, round 1

Reviewer: codex-c1c1-r1, Codex gpt-6.1-sol/high, R2-DEEP; different vendor from the Claude author.
Subject: **C1C1-DESCRIPTIONS-r1**, proposed contract successor 191, for product
`c1e9df9aa56c1f4f2a7da51dce2826e62e23b090` on
`98159381648b0ddad022f1c7fffe678ce0e27208`.

Request SHA-256: `74ed94bf0fac988196af45b1d99e685f064068655f8f49441dc823ceabe17fb4`.
Subject manifest SHA-256: `715d03ca199f1339d5b6eb8c2d54aa9fb87528b004b08ad2ebc5f50be6e7b38a`.
Successor record SHA-256: `b19f6daa93ded34b270472207c333ac70ae516c7de72dd6338914d9828981b11`.

## Required finding

**B-RF-1 — The new reader meaning must preserve native observation errors as HostIo.**

In staged successor.json:102, `/passageSupersessions/0/after` describes a malformed nonsuffix name
as counted only when observed no-follow as a regular file, link or special file, **“and otherwise
refuses Name.”** That otherwise is false for a failed native observation.

The adopted, staged ADDENDUM-unobservable-name-r2.md §1(c) expressly preserves the existing
`HostIo` refusal and native provenance when the component predicate accepts a name but native
observation fails. In the frozen product, snapshot_read_set.rs:1392-1412 implements the distinction:
present files/links/specials return true; directory and absence return false; a constructed
InvalidInput without OS errno returns false; every other error moves intact into HostIo.
Raw native EINVAL is a distinguishing case, sharing InvalidInput's kind but retaining errno 22.
Code review RF-3 corrected and controlled precisely this distinction; the new public meaning
cannot collapse it again.

Limit the Name statement to observed directory, absence and component-predicate rejection before
observation. Explicitly retain HostIo and its native provenance for native observation errors,
and preserve budget exhaustion if the refusal cannot be funded. For example, qualify the refusal
as Name for those three cases when funded, while stating that native errors remain HostIo.
No new law choice or product code correction is needed. Regenerate the record and subject pins
and obtain review of that revised subject. The current manifest cannot be accepted.

## Coordinator's inventory-scope condition: met

**inventoryScopeExcludesArchitectureLawDocuments = true.**

The repository/module-layout contract owns the implementation target filenames and explicitly
separates that organization from the existing architecture record and its pinned schema/evidence
files (docs/v2/architecture/14-repository-and-module-layout.md:55-60, 145-155). The inventory is
stored in the architecture repository but describes the target product repository; storage
location does not make it an inventory of architecture documents.

The selected v242 contains 1,461 product-path rows. Its docs rows are product documentation
(`docs/README.md`, `docs/architecture.md`, `docs/development.md`, `docs/report.md`), not the
architecture's docs/implementation law corpus. None of these four architecture law/receipt
paths is a product-inventory row. The actual 9815938-to-c1e9df9 diff modifies exactly 21 product
paths and adds, removes or renames none.

The four adopted files are present by value beside PLAN-r4, byte-identical to the coordinator's
adopted sources. Each is in lawFilesByValue, candidates and the reviewed seven-member subject.
The contract-successor verifier pins every subject member and requires candidates to cover
exactly those members other than the successor record. This supplies their binding custody
without treating them as product files. The C2a-3 description record also distinguishes its
product-file additions from the architecture addendum published by value; it is corroborating
precedent, not the sole basis for this scope conclusion.

Thus **no inventory v243 is required for this unit or these four law files**. The complete
description/law binding route is appropriate once B-RF-1 is fixed. This positive scope conclusion
does not accept the currently false description.

## Remaining meaning and structural assessment

The other two new meanings are true of c1e9df9. The seal override removes the stale negative
read-set/Git claim and describes the separate allocation-free guard, its authorization/suffix/
exclusion conditions, its position before the bounds and its funded measuring/check work.
The no-layout/no-read-set case remains unchanged. The sort override accurately adds
sort_unique's charged sort and adjacent deduplication for excluded paths.

Resolved the current meanings from the product's selected contract history rather than relying
on raw v242 text alone. The 18 UNCHANGED_TRUE paths retain true descriptions: evaluator exports
and native-plan joins; layout ownership, controls and vectors; the host capture/session,
harness and seal controls; the shared rule and discovery vectors; walk/model controls; and the
three census/model tools. Their new additive functionality does not contradict those existing
descriptions. The classification covers all 21 changed files exactly once: two overrides, one
supersession and 18 unchanged meanings.

Both override selectors name the correct v242 rows and their exact raw before text.
The reader supersession correctly selects v242 row 822 while naming the published
C2B-M5-DESCRIPTIONS-r1 passage over v241 row 818. Its before text equals that predecessor's
reviewed after text. The machine payload below lists exactly the record's supersedes object;
this acknowledgement identifies the intended target and does not accept its proposed new text.

All seven subject-member byte/hash pins match; candidates cover the complete subject except
the record itself; the parent inventory pin matches the selected v242. All summary review,
pricing, mutation, lane and adopted-law evidence pins match their current artifacts. The
summary retains the earlier required-finding rounds and final code acceptance, and reports the
two failed lane tests. This binding review does not establish receipt-interval closure or
convert that lane to a green run.

Independently ran c1e9df9's unmodified read-only verifier against the existing dry-run tree and
lock: **passed**, 202 inventory successors, 191 contract successors, 184 inheritance entries,
productQualification false. Dry-run lock SHA-256:
`d08e852c12b2099190c5097c4324ade9b020c1f8bcb75c93aefa30cb93b0f649`.
The dry run uses clearly marked PLACEHOLDER acceptance and assent. It proves structural
feasibility, not semantic acceptance, substantive root assent or publication. After correction,
the actual review and author assent must replace those placeholders before final binding.

Live controls select the C1c-1 plan and R2-DEEP; route preflight returned
`ROUTE-OK R2-DEEP codex gpt-6.1-sol/high`. Architecture staging base is clean at
`4f2b6a5164dffdf327cb6c1fe119148b21c2c055`; the canonical architecture main remains
45d11ae73. No product, law, control, accepted inventory, lock or Git state was edited; no refresh,
build, Cargo test or T2/store access was performed.

## Machine-review output and write limitation

Automatic approval review rejected the requested write to
`binding/stage/docs/implementation/m3/reviews/codex-c1c1-descriptions-r1/review.json` because that
path is outside this session's writable project. The staged review file remains **unwritten**.
The complete intended JSON is retained below in this authorized prose artifact. It is a
REQUIRED-FINDINGS review and must not be replaced with the dry-run ACCEPT placeholder.

```json
{
  "verdict": "REQUIRED-FINDINGS",
  "requiredFindings": [
    {
      "id": "B-RF-1",
      "path": "docs/implementation/m3/snapshot-plan-c/c1c/c1c-1-integration/descriptions-r1/successor.json",
      "selector": "/passageSupersessions/0/after",
      "title": "Preserve the native HostIo route in the new reader meaning",
      "finding": "The new snapshot_read_set.rs meaning says that a malformed nonsuffix name is counted only when observed as a file, link or special file, and otherwise refuses Name. That otherwise also covers a failed native observation, for which adopted LD-C1C-5A section 1(c) and c1e9df9's unconverted_disposition instead preserve HostIo and the original errno. Raw EINVAL is a distinguishing case explicitly fixed and controlled in code review RF-3. The proposed binding therefore publishes a false refusal classification despite the corrected code.",
      "requiredChange": "Limit the Name statement to observed directory, absence and pre-observation component-predicate rejection, and explicitly retain HostIo with native provenance for native observation errors. Preserve budget exhaustion when refusal construction is underfunded. Regenerate the successor and subject pins and obtain review of the revised subject; no product code or law change is needed."
    }
  ],
  "subjectManifestSha256": "715d03ca199f1339d5b6eb8c2d54aa9fb87528b004b08ad2ebc5f50be6e7b38a",
  "nonBlockingObservations": [
    "The inventory-scope condition is met. The repository-layout contract separates the implementation target inventory from the existing architecture record. Inventory v242 has 1461 product-path rows, including product docs, and does not inventory architecture law documents. C1c-1 modifies 21 product paths and adds, removes or renames none. The four adopted architecture law/receipt files are byte-identical to the adopted sources and are covered by lawFilesByValue, candidates and the seven-member subject manifest. They require no product inventory v243.",
    "The dry-run verifier passes with 202 inventory successors, 191 contract successors and 184 inheritance entries, using PLACEHOLDER review and assent. This proves structural feasibility only; it does not accept the incorrect description, close the receipt interval, supply substantive root assent, publish the binding or qualify the product."
  ],
  "supersededPassages": [
    {
      "record": {
        "path": "docs/implementation/m3/snapshot-plan-c/c2b/m5/descriptions-r1/successor.json",
        "bytes": 9883,
        "sha256": "7daab8230dd2d9ec585f082f51403b7daaff40bb0b6a59ac2df082fe6f0bab51"
      },
      "parent": {
        "path": "docs/implementation/m2/repository-file-inventory.v241.json",
        "bytes": 822071,
        "sha256": "77f298a1181f8250f576192e37e587ed2041e3d9c22f0392170acd45be818197"
      },
      "selector": {
        "jsonPointer": "/files/818/description"
      }
    }
  ],
  "productQualification": false,
  "inventoryScopeExcludesArchitectureLawDocuments": true
}
```

C1C1-BINDING: REQUIRED-FINDINGS

