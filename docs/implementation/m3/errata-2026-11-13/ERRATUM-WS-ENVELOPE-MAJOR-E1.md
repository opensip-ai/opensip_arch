# Erratum WS-ENVELOPE-MAJOR-E1: the current command envelope is major 7, not 3 (author draft, 2026-11-13)

Status: **PROPOSED.** It implements register row R-35 (`LC/coordinator/REFACTOR-RISK-REGISTER-2026-11-12.md:76`, `:99`,
`:147`; `LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`): "an erratum mapping WS's major 3 to the
selected major 7". It is **additive**: one sentence, mapping the prose to the bound selection. No product behaviour changes.

Subject: the product contract `docs/v2/contracts/product-v1/workflows-and-surfaces.md` (WS), 133,335 bytes, sha256
`1ee203e3ce626d88a53d0247881cd3ffb0d52b421821ac798b9f0b57346ff6ed`.

**Whose words.** WS's standing line (WS:3-4): "Authored and corrected by actual Claude, Codex and actual Grok under D-367
delegated design authority". The prose is not the owner's own words, so it is corrected by an erratum, not a note.

**Which record form applies.** WS is a design-lock input (product `design-lock.json`, `inputs`, `:263`, same sha256).
So the correction is a **contract successor** with one passage override, in the NE-4-4-DETAIL-UNITS-r1 form
(`../errata-2026-11-11/ne-4-4-detail-r1/`). This file is its text; the record is owed (WSE1.5).

## WSE1.1 The three claims, verified

| Claim (R-35) | Verdict | Where |
|---|---|---|
| WS says the envelope's major is 3. | **Holds.** | WS:33-34: "Its closed schemas live under `workflows/schemas/evaluator3/`: envelope, invocation, command inventory and graph query major3"; WS:1108: "`json` v3 (the `CommandEnvelope` major 3 is the parity reference)". Also WS:63 and WS:69 (succession-table rows: "**Succeeded** by envelope major 3 (§8)" and "**Succeeded for product envelope major3** by `common.schema.json#/$defs/StepTermination`"). |
| The selection uses 7. | **Holds, with one precision.** | `docs/implementation/m1/source-selection-v2/current-dispatch.json:22`: `"schemaId": "urn:opensip:product-v1:workflows:evaluator3:command-envelope:7"`, source `…/schemas/sources/command-envelope.v7.schema.json`. Precision: the v2 unit itself was never installed ("It is not accepted yet", `source-selection-v2/README.md:3-4`). The bound record is **source selection v3**, which reuses v2's members at their frozen paths (`source-selection-v3/README.md:3`): its `successor.json:120` names `current-dispatch.json` and `:560` names `command-envelope.v7.schema.json`. The product lock binds v3 as a `contractSuccessors` entry (`design-lock.json:6014`, review `m1/reviews/grok-source-selection-v3-01/review.json`). |
| The product emits 7. | **Holds.** | Product main `1bd328f3`, `crates/host/src/outcomes.rs:208`: `"schemaFamily":"opensip.product.envelope","schemaMajor":7,`. |

So this is stale contract prose, not a product/contract conflict (the register's own downgrade, `:99`). The selection
already says how to read it: "README.md, current-dispatch.json, semantic-owner-joins.json and scoped-owner-succession.json
define current versus historical interpretation. Parent contracts remain unchanged outside explicit scoped succession."
(`source-selection-v3/successor.json:786`). Its `scoped-owner-succession.json` says the same of the envelope
(`currentVersionResolution`, `source-selection-v2/scoped-owner-succession.json:7`): "Old envelope5/6 and invocation3/4 labels
in preserved predecessor clauses denote their historical correction scope, not alternative current encoders." This erratum puts that mapping in WS, where a reader of WS will see it.

## WSE1.2 The amendment

An insertion after WS:43 ("baseline is never interpreted as an empty population in a new baseline."), which ends
the paragraph (WS:31-43) that names the majors, as a new paragraph:

> **Current envelope major (erratum WS-ENVELOPE-MAJOR-E1).** The current `CommandEnvelope` is major 7 (`urn:opensip:product-v1:workflows:evaluator3:command-envelope:7`), as the bound source selection v3 selects it through `docs/implementation/m1/source-selection-v2/current-dispatch.json`. Where this contract names the envelope major 3 as current (the list above and §8's renderer parity reference), read major 7; major 3 is historical.

## WSE1.3 What this does not change

- WS:63 and WS:69 are left as written. They record what succeeded older texts (the major-1 union; D9's termination
  union), and at that time the successor was major 3. The inserted sentence does not reach them.
- The `json` renderer's own version ("`json` v3", WS:1108) is not the envelope major and is not touched.
- No schema, generator root, digest, fixture or product code. The selection's bytes are unchanged.
- Same kind, not drafted (R-35 names only the envelope): WS:34 also says invocation, command inventory and graph query
  are "major3", while the selection has invocation 5 (`current-dispatch.json:14`), command inventory 6 (`:102`) and
  graph query 4 (`:30`); WS:1148-1149 says graph query "major 3". The selection's reference copy
  `source-selection-v2/reference/effective-workflows-and-surfaces.md` (lines 34, 63, 69 and 1112) repeats WS's "major 3"
  wording. Candidates for the same successor if the lead wants one record.

## WSE1.4 Review

**One independent review** (OD-PACE-1 rule 2), as NE-4-4-DETAIL-UNITS-r1 (a contract successor with no behaviour change)
was routed. OD-PACE-1 settles it: "where OD-REVIEW-1 or an older plan asks for more reviewers than rule 4 above, rule 4
governs" (`OD-PACE-1.md:67-68`), and rule 4 (`:30-31`) does not name contract text.

## WSE1.5 Binding owed (not generated)

A contract successor record (one passage override of WS line 43: `before` "baseline is never interpreted as an empty
population in a new baseline.", `after` the same text, a blank line and the paragraph above), its subject manifest, the review, the unit assent, and one
`contractSuccessors` entry in the product's `design-lock.json`. It is mechanical once the text is settled. It is not
generated here because the text may change in review, and the model restaged its manifest after review
(`errata-2026-11-11-r1` commit `112aa8528`).
