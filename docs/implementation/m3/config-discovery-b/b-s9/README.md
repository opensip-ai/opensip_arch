# B-S9 — contract successor S9: the `CONFIG.INVALID` remedy

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route or public code. It needs `ACCEPT-DESIGN-UNIT` from an independent reviewer and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-B r2** (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`, GROK2, `92e65825…`) requires a remedy-text successor, **S9**, "through X12-0's route, that covers configuration documents generally" (MB item 4, MB:155; successor table MB:780). M3-B's units table puts S9 in B-S1 (MB:841). **By the lead's decision of 2026-10-04, S9 is its own design unit, B-S9**, so that B-S1's SX-1 and D15 content binds without waiting on S9's binding form. B1-a's dependency "B-S1 (S9 text)" (MB:843) becomes "B-S9".

**Product.** Main at `e093e90` (F8b's binding, 77 contract successors), read only. The record is built and checked against it.

## Short names

MB is M3-B r2. X12-0 is the accepted remedy successor `docs/implementation/m2/config-remedy-x12-0/` (bound since product `b880e83`). CT is `docs/implementation/m2/capability-totality-reference-selection-v1/`, whose `reference/native_evidence_model.py` is the current selected native reference. NM2 is the frozen `docs/coop/design-corrections/native/native_evidence_model.v2.py`.

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `successor.json` | the contract successor record: three parents, no passage override, seven candidates |
| `reference/native_evidence_model.py` | the successor copy of CT's selected reference |
| `reference/native_evidence_model.v2.py` | the successor copy of NM2 |
| `evidence/copies-report.json` | generated: per copy, the parent, the bound entries applied, the effective parent's digest, the changed lines and the result |
| `evidence/build_b_s9.py`, `check_b_s9.py`, `verify_scratch.py` | build, read-only content checks, and the real verify_design with a synthetic review and assent and the feasibility probes |
| `../b-s9-subject.json` | the subject manifest (generated) |
| `../b-s9-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## The change

`PUBLIC_ROUTE_REMEDIES` in the native reference model is keyed by public code. One string must stay true for every key that reaches its code: NE's `remedyKeyingConstraint`, and the model's own comment at lines 1150-1156. B1 adds every external configuration refusal to `CONFIG.INVALID`'s population (MB item 4). So the string widens again. It is line 1158 of both native-model files, the line X12-0 overrode.

Before (X12-0's meaning):

> the configured capability or policy selection is invalid: for capabilities, name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot); for policy, name exactly one bundled policy pack id, written exactly as name:version, and supply no policy document of your own or from a third party

After (706 ASCII characters, within `BoundedText`'s 1,024):

> the configuration or selection is invalid: make each configuration file, flag and request well-formed for its schema and layer, with no unknown key, a supported schemaVersion, canonical project-relative paths that exist, and a nonempty workspaceRoots when one is given; name only a registered profile and registered or admitted ids, and state each component once with no conflicting pin and hold; for capabilities, name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot); for policy, name exactly one bundled policy pack id, written exactly as name:version, and supply no policy document of your own or from a third party

How it stays true for each key that reaches the code:

| Key or row | The next step the string gives |
|---|---|
| `native.requested-capability-unregistered`, `-mode-unregistered` | name a registered capability id from the native capability matrix (unchanged words) |
| `native.requested-capability-duplicate-ownership-tuple` | at most one row per (capabilityId, languageMode, workspaceRoot) (unchanged words) |
| X12 rows 1 (unregistered pack, `count:<n>`), 2 (supplied pack), 3a (malformed supplied document) | the policy clause, unchanged words |
| Config2 lexical admission: duplicate keys, Unicode, depth, size, inexact integers, end anchors (AQ:10-41; MB item 4 step 1) | make each configuration file well-formed |
| unknown key; unsupported `schemaVersion`; unmapped schema-one field (AQ:30-31, AQ:175-178; MB items 4 and 11) | no unknown key, a supported schemaVersion |
| per-layer allowlist, for example a global key outside `analysis.budget` (MB item 2) | well-formed for its schema **and layer** |
| logical-path grammar, an absent selected path, `entryPoints` with `.` (AQ:112-121) | canonical project-relative paths that exist |
| explicit `workspaceRoots: []` (AQ:115-117) | a nonempty workspaceRoots when one is given |
| `CONFIG_PROFILE_MISSING`, `CONFIG_PROFILE_UNREGISTERED`; waiver IDs, none registered at M3; evidence IDs (AQ:126-127, AQ:334-335) | name only a registered profile and registered or admitted ids |
| component duplicates and pin/hold conflicts (AQ:124-126) | state each component once with no conflicting pin and hold |
| a configured capability on a `NOT-SELECTED` cell (NE:3571) | name a registered capability id … (as today) |

The two predicates `foundation/check-identity.py` applies at :7212-7217 are kept byte for byte: `registered capability id from the native capability matrix` and `(capabilityId, languageMode, workspaceRoot)`.

Keys whose public detail is not `CONFIG.INVALID` are outside the string, even where the D9 code is `CONFIG.INVALID` (SL S12.1 rule 3). These include `PROJECT.EXPLICIT_PATH_INVALID`, `PROJECT.ROOT_CUSTODY_REFUSED`, `CONFIG.CUSTODY_REFUSED` and `native.explicit-root-without-marker`.

The product carries the string as `crates/host/src/configuration.rs:24` (`REMEDY_CONFIG_INVALID`). `doctor_ingress.rs:216` reuses it, and `configuration_tests.rs:338-343` pins its length and SHA-256. B1-a changes all three, citing B-S9.

## The form: complete successor copies

The candidates are complete copies of both native-model files at new paths, under `b-s9/reference/`. This is the form CT itself used to select its copy of this same file. Unit 468a used it for its common4 schema, and the I1-L draft uses it for JSON schemas (LD-L1 and LD-L2).

**Each copy is its parent's effective text.** The parent's raw bytes have every passage override and supersession the product lock binds to that path applied, in lock order. Line 1158 is then replaced by the S9 line, and nothing else changes. At `e093e90` the only bound entry on either file is X12-0's line-1158 override, so each copy differs from its effective parent, and from its raw parent, in line 1158 alone. The two copies differ from each other exactly as their parents do (12 diff lines: CT's one-function correction), so CT's correction is carried. `copies-report.json` records all of this, and `check_b_s9.py` recomputes it independently.

**Selection.** This is stated in the record's `standing` and here:
- the current selected native reference becomes `docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py`;
- the successor text of NM2, the file law X12 names, is `docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py`;
- CT's copy, NM2 and X12-0's meaning on them become historical, as NM2 became when CT was selected ("historical native_evidence_model.v2.py remains untouched").

**How verify_design treats this (feasibility, proved by `verify_scratch.py`):**
- **Selection is not a verify_design concept.** It keeps one flat set of accepted paths, and it keys overrides by `(parent path, selector)`. It selects an effective copy only for product generation and admission sources (`schemas/source-map.json` and `schemas/admission-source-map.json`), and neither native-model file is one. So a copy at a new path is an ordinary candidate. Listing a parent that carries bound overrides is allowed: `contract_successor` requires only that each parent is accepted and is not overwritten (`tools/verify_design.py:221-229`).
- **B-S9 binds.** Appended to the `e093e90` lock it passes, design-only at `--rev e093e90` and on the checkout, where 40 generation sources are verified. The lock grows from 77 to 78, and the selected inventory and inheritance are unchanged.
- **The rejected forms refuse,** both checked as probes:
  - a second override of line 1158 gives "conflicting contract passage overrides" (`verify_design.py:381-383`);
  - VD1 supersessions of X12-0's entries give "passage supersession must select an inventory row description" (`verify_design.py:342-345`).
- **Later successors after B-S9:**
  - an override of the copy's line 1158 binds, because the copy is a fresh key;
  - an override of an old file's line 1158 refuses, as it does today;
  - an override of an old file's *other* line binds. verify_design cannot tell that the file is no longer selected, so a later unit that edits a superseded copy is caught only by review. That is this form's residual hazard, and it is the same as CT's.

## Lead decisions

Each decision is made under the owner's standing direction to decide on the lead's recommendation. Each names the alternatives it rejects.

**LD-1. Complete successor copies of both native-model files, each its effective parent plus line 1158.**
- It binds on today's verify_design, with no tooling change and no re-pin.
- **Rejected:**
  - **A second override of line 1158.** Refused (above).
  - **VD1 supersessions.** Refused (above). They would need a verify_design successor, VD2. VD2 would change `tools/verify_design.py`, which `tools/contracts/generator-closure.json:1746` and `tools/typescript-lanes.json:804` pin. That means another generator rebuild and re-pin on F8b's scale.
  - **Unbinding X12-0.** That rewrites an accepted binding.
  - **A copy of CT's reference only.** NM2, the file law X12 names, would keep X12-0's text with no successor, and X12-0 deliberately kept the two in agreement.
  - **Raw-parent copies.** They carry no bound meaning. That is harmless today, because the one bound entry is replaced, but wrong in general (I1-L LD-L2).

**LD-2. One S9 string for every configuration refusal.**
- The capability and policy clauses keep their words.
- A leading clause covers configuration documents, flags and requests generally.
- **Rejected:**
  - **A new code.** The owner's no-new-codes rule forbids it.
  - **Per-row remedies.** The remedy is keyed by code.
  - **Dropping the capability or policy clauses.** They are still true and still needed for those keys.

**LD-3. Line 1158 only.**
- The comment at 1150-1156 records the earlier ownership-tuple widening and stays true, so it is kept, as X12-0 kept it.
- No other remedy or function changes.

**LD-4. The selection is declared in the record, and B1-a cites the copy.**
- The record's `standing` names the selected copy. Every later edit of `PUBLIC_ROUTE_REMEDIES` or of this model must override the B-S9 copies, not the historical files. Probe 3c shows that verify_design will not enforce this.
- **Rejected:** a verify_design rule that refuses overrides on superseded copies. That is a VD2-class tooling change, for a hazard that review already holds for CT's copy.

## Points for the reviewer

- **R1 (LD-1, LD-4).** Is the copy form, with its selection statement, a sound successor of X12-0's two line-1158 meanings? Is the residual hazard (probe 3c) acceptable as it is for CT?
- **R2 (the table).** Is the table complete for every key that reaches public detail `CONFIG.INVALID` after B1? Is each next step true?
- **R3 (the copies).** Is each copy exactly its effective parent with line 1158 replaced, carrying CT's correction?

## Conflicts and reconciliations with accepted laws

- **M3-B r2:**
  - Item 4's "through X12-0's route" is kept. The route is the `PUBLIC_ROUTE_REMEDIES` text successor; only its binding form is the copy form, which needs no verify_design change.
  - The units table's placement of S9 in B-S1 (MB:841, MB:843) is changed by the lead's decision. This is a unit-plan change, not a change of content.
- **X12 r4:** none. X12's rows keep `CONFIG.INVALID`, and their policy clause keeps its words.
- **X12-0:** its meaning on the two parents becomes historical through selection, not through any override or rebinding.
- **B-S1:** none. B-S1 no longer touches the native model.

No owner question is raised.

## Binding

B-S9 has no passage override, so it binds on the verify_design at main `e093e90` with no prerequisite. After `ACCEPT-DESIGN-UNIT`:
- copy the review to `docs/implementation/m3/reviews/grok2-b-s9-r1/review.json`;
- complete `b-s9-unit.json`;
- append the four pins to the product lock;
- run plain verify_design.

B1-a then embeds the string and repins its test.

**Evidence runs** (`python3.14 -I -B` at `nice -n 19`, read-only):
- `build_b_s9.py` twice: identical bytes.
- `check_b_s9.py`: pass.
- `verify_scratch.py`, both `--rev e093e90` and the checkout: it binds; the two rejected forms refuse; the later-successor probes give PASS, REFUSED and PASS, as described above.

## Not claimed

- No product code, test or build was run. Only the evidence scripts ran, read-only.
- The reference checkers (`check-identity.py` and the native checker) were not run. On this Mac, the native model refuses Python 3.14.6's Unicode data as an environment fault (X12-0 README). `check_b_s9.py` parses both copies with `ast` and checks the table without importing them.
- No law is amended. No public code, class, exit or detail is added.
