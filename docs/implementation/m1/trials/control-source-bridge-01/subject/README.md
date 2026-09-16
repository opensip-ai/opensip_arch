# Common-control source-selection bridge (proposed candidate)

This closure is authored for root freeze and independent review. It contains no
acceptance, review, root assent, integration or qualification. This README only
explains the unit and is not a normative design source. The reviewable selection
is `successor.json` plus `selection-subject.json`, and only a reviewed lock binding
could make it effective.

## Problem

The accepted control-generation unit maps
`docs/coop/completion/control-completion.schema.v3.json`
(`2929de62…`, 22476 bytes) as generation source 29. The live binding4
`--implementation` preflight refuses it with
`generation source is not selected by accepted design`.

The schema is not a row in source45 or application46, and no accepted inventory
or contract successor selects it. It is reached only indirectly:

- lock approvals → source45 row `architecture-application.v1.json` (`15b3932a…`)
- → `/units/control` (review standing `NO-OBJECTION-WITHIN-REPAIR-SCOPE`)
- → review5 `dc31dd4d…` and freeze5 `0e4a020f…`
- → the eight frozen members, which include schema3.

The same application also pins the schema directly at
`/evidenceTargets/C.BODIES/sources/1` for unit `control`.

## Why the v4 format can express this truthfully

The accepted `contract_successor` and `successor_chain` rules allow exactly this:

- **Parents must already be accepted.** The architecture application is a
  source45 row with an exact pin, and application46 does not override it.
- **Candidates are exact pins** equal to the reviewed subject minus the record. A
  candidate may be an existing architecture path, as long as no accepted path is
  reused. Schema3 is not accepted, and its bytes are not accepted under any other
  path either.
- **`passageOverrides` may be empty.** This unit changes no parent meaning.
- **The preflight's selected set** is the effective overlay plus the unit's
  inputs, so the schema becomes selected without any copy, new path or new ID.

The v4 verifier does not read the record's `selection` or `evidence` fields. Its
trust anchor is the pinned review and assent. A test shows that the verifier
alone accepts a fully rebound schema drift under a synthetic review. The
historical joins are therefore made explicit in the record for the reviewer, and
`check_bridge.py` checks them mechanically. No verifier change is proposed.

## Subject files

`subject-files.json` pins every file below. It is the explicit freeze list, and
the closure contains nothing else.

| File | Role |
| --- | --- |
| `successor.json` | Contract-successor record: 1 parent, 1 candidate, no overrides, selector and evidence pins |
| `selection-subject.json` | The v4 `subjectManifest`: exactly `successor.json` (staged path) and the existing schema |
| `check_bridge.py` | Reference check: historical joins, scope, live refusal, staged verification |
| `test_bridge.py` | Verification and drift tests over a mirror of declared inputs only |
| `inputs.json` | Declared closure: 2 snapshot pins and every architecture file read |
| `snapshot/verify_design.py` | Byte copy of the accepted and integrated binding4-correction verifier (`1dce4b8a…`) |
| `snapshot/design-lock.json` | Byte copy of the accepted live lock (`90e0533f…`) |
| `staged-lock-extension.md` | Description of the future lock change, with placeholders only |
| `README.md` | This explanation (not normative) |

The lock would bind only the two staged files at
`docs/implementation/m1/control-source-v1/`. The other files are review and
reference evidence, and root decides where they are retained.

## What `check_bridge.py` verifies

The checker does not trust itself or its inputs:

- It executes the snapshot verifier from its exact bytes.
- It records every architecture file the verifier opens. The observed set must
  equal the declared set in `inputs.json`, with no undeclared and no unused rows.
- Every declared pin is byte-verified.

1. **Snapshot provenance.** The snapshot bytes equal `tools/verify_design.py` and
   `design-lock.json` in the binding4-correction integration record. That record
   links to its accepted unit (`ACCEPTED-UNIT`, root assent, no findings). The
   unit's review is `ACCEPT-UNIT` with no required findings for the same subject,
   and that subject manifest lists both files.
2. **Live lock.** The full v4 verification passes: 46 inputs, inventory3 and
   metadata-v2.
3. **Base selection.** The architecture application is exactly one source45 row
   and is absent from application46. The record's parents and `baseApproval`
   match the lock.
4. **Selector.** `parentSelector` is exactly the application at `/units/control`,
   and its standing is the review5 verdict. The record's review and freeze pins
   equal the path and pin found at that selector. The direct `C.BODIES` evidence
   pins the exact schema for unit `control`.
5. **Review5 and freeze5.**
   - The review is the control independent review, version 5, with verdict
     `NO-OBJECTION-WITHIN-REPAIR-SCOPE`, `mustFindings: []` and no required
     findings. Its subject is unchanged.
   - The review's subject freeze digest equals freeze5. Its subject files and
     post-review hashes equal the freeze's eight files.
   - The replay passed everything and matches the frozen report digest.
6. **Eight members.** Each member's pin is byte-verified, and the record's
   `frozenMembers` equal them exactly.
7. **Scope.**
   - The candidates are exactly the schema, which is a frozen member with `$id`
     `urn:opensip:design:control-schema:3`.
   - There are no passage overrides, and the record disclaims product
     qualification.
   - The schema path is not already accepted, and its bytes are not accepted
     under another path.
   - The selection subject is exactly the record and the schema.
8. **Generation join.**
   - `control-generation-unit.v1.json` is `ACCEPTED-UNIT` with
     `integrationApproved: false`. Its review is `ACCEPT-UNIT` with no required
     findings for subject `c4d3c10d…`.
   - The trial source map, registry and all 29 mapped sources match that subject.
     The control row maps the exact schema bytes.
9. **Live preflight.** With the live lock, the reviewed trial sources are refused
   with the exact message above. The same tree with only the control row removed
   verifies 28 sources.
10. **Route note.** `control-source-route.v1.json` is untracked, so the checker
    reports whether it is consistent but does not rely on it.
11. **Staged run** (`--review` and `--assent`). The checker runs the snapshot
    verifier over the live lock plus the appended binding and the source
    preflight. It requires the selected inputs to be exactly the schema, refuses
    synthetic fixtures and allows only declared reads.

The tests cover all of the above. They also show refusals for the following
kinds of drift:

- schema bytes, including a fully rebound drift;
- the selector and schema-evidence pointer;
- application bytes, including a rebound application;
- the parent;
- the review, freeze and member pins;
- review and freeze documents (verdict, findings, subject, post-review hashes,
  replay, member count, schema digest);
- scope (extra candidate, overrides, disclaimer, subject membership);
- an already accepted path or duplicated bytes, via the verifier's own reuse rule;
- the trial generation copy;
- the snapshot, and undeclared, unused or re-pinned inputs.

They also cover the v4 rejections of wrong verdict, findings, subject, assent
status and successor size.

## Synthetic fixtures

`test_bridge.py` creates review and assent JSON only under `TMPDIR`, in a path
beginning `synthetic-not-acceptance/`, carrying the key
`syntheticFixtureNotAcceptance`. These fixtures exercise the verifier and are
not reviews, assent or acceptance. They are never written to this closure or the
architecture checkout. Real-mode `verify_staged` refuses both the marker and the
path prefix. That refusal guards against accidental use; it does not
authenticate a review.

## Rerun (only this closure plus the architecture checkout)

Uses the Python standard library only: no network, subprocesses or jsonschema.
It was authored with Python 3.14.6. The checker and tests refuse to run without
`-B`, or when `TMPDIR` is missing or inside the closure.

```
cd <this closure>
export TMPDIR=<existing directory outside the closure>
python3 -B check_bridge.py --architecture <opensip_arch>
OPENSIP_ARCHITECTURE=<opensip_arch> python3 -B test_bridge.py -v
python3 -B check_bridge.py --architecture <opensip_arch> --discover-inputs   # compare with inputs.json "architecture"
```

## Limits (not claimed)

- **Acceptance.** Nothing is selected until an actual review, root assent and lock
  binding exist. See `staged-lock-extension.md`.
- **Historical status.** The application's own `status` string is
  `WORKING-INTEGRATION-NOT-FROZEN-OR-ADOPTED`. Its authority here comes only from
  its exact selection by source45 under the lock's application46 approvals. That
  is the same basis the live verifier and the route note use.
- **Scope of selection.** Only schema3 bytes are selected, for generation-source
  provenance. Framing, state, sequence, correlation, authorization, effects and
  durable outcomes remain with the unwritten
  `crates/components/src/control_protocol.rs`. Review5's pending security/journal
  and host-qualification joins remain open.
- **Open obligations.** CA2 to CA5 and the other control-generation integration
  obligations stay open.
- **Pins.** The architecture checkout is dirty, and several evidence files,
  including the route note, are untracked. Pins are verified by hash, not by
  commit history.
- **Read recording.** Read recording relies on the snapshot verifier opening
  architecture files through `relative_file`, which is true for every such read
  in these bytes. The checker reads closure files directly.
- No product, M1 or release qualification.
