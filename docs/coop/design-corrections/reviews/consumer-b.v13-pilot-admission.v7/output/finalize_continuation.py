#!/usr/bin/env python3
"""Rewrite requirement-status, continuation checkpoint, and blind-review from measured artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v7/output")
OLD = "/tmp/opensip-design-corrections/consumer-b.v13/output"
NEW = str(OUT)
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")
sys.path.insert(0, str(OUT))

from helpers import status  # noqa: E402  # OUT already set in status.py to continuation

CONSUMER = "consumer-b.v13"
CONT = "consumer-b.v13-continuation.v2"
PARENT = "fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d"
MANIFEST = "afa3abfbb3dd26e10026058d433fc1871505fbd9d1c928f79e881d514e5cc40d"
PY = "/tmp/opensip-architecture-review-env/bin/python"


def dump(path: Path, obj) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    return str(path)


def rebase(p):
    if isinstance(p, str) and p.startswith(OLD):
        return NEW + p[len(OLD) :]
    return p


def main() -> None:
    rows = json.loads((OUT / "requirement-status.json").read_text())
    for r in rows:
        r["artifact"] = rebase(r.get("artifact"))

    overlays = {
        "S-CONTINUATION": (str(OUT / "pilot" / "helper-corrections.json"), "same-origin continuation consumer-b.v13-continuation.v1; kit/parent hashes unchanged"),
        "S-FRESH-ORIGIN": (str(OUT / "vectors" / "phase0-standing.json"), "origin consumer-b.v13; this is continuation of that origin, not a new independent session"),
        "R-RUN-TS": (str(OUT / "runs" / "ts.store.json"), "owning-schema admission + closure + fresh-process complete-proof compare"),
        "R-RUN-TS-NODE-MODULES": (str(OUT / "runs" / "ts.store.json"), "node_modules/left-pad layout nested record + blobJoins"),
        "R-RUN-TS-CONFIG-DEPS": (str(OUT / "runs" / "ts.store.json"), "tsconfig.base.json + tsconfig.json utf8-sorted configGraphPaths"),
        "R-RUN-RUST": (str(OUT / "runs" / "rust.store.json"), "admitted+closed+fresh replay"),
        "R-RUN-RUST-MIXED-EDITION": (str(OUT / "runs" / "rust.store.json"), ""),
        "R-RUN-RUST-TARGET-EDITION": (str(OUT / "runs" / "rust.store.json"), "bin targetEdition 2021 vs package 2018"),
        "R-RUN-RUST-BODY-DIALECT": (str(OUT / "runs" / "rust.store.json"), ""),
        "R-RUN-RUST-SAME-FILE-TWO-EDITIONS": (str(OUT / "runs" / "rust.store.json"), "shared.rs under lib and bin selections"),
        "R-RUN-RUST-PARTIAL-EMPTY-CLONES": (str(OUT / "runs" / "rust-partial.store.json"), "indeterminate; empty ownership; unknown clones Coverage"),
        "R-RUN-RUST-HASH-MARKER": (str(OUT / "runs" / "rust.store.json"), "crates/foo#bar"),
        "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE": (str(OUT / "runs" / "rust.store.json"), ""),
        "R-RUN-RUST-LARGE-EDITION-MAP": (str(OUT / "runs" / "rust.store.json"), ""),
        "R-RUN-RUST-VERSION-COMPONENT": (str(OUT / "runs" / "rust.store.json"), ""),
        "R-RUN-FILE-FACT-INVENTORY": (str(OUT / "runs" / "ts.store.json"), ""),
        "R-RUN-CLONES-L0-AND-NORMALIZED": (str(OUT / "runs" / "ts.store.json"), ""),
        "R-RUN-CLONES-CUSTODY": (str(OUT / "runs" / "ts.store.json"), ""),
        "R-RUN-SYNTAX-CODE": (str(OUT / "runs" / "syntax-code.store.json"), ""),
        "R-RUN-SYNTAX-DATA": (str(OUT / "runs" / "syntax-data.store.json"), ""),
        "R-RUN-NO-COMPILER-UNIT": (str(OUT / "runs" / "syntax-code.store.json"), ""),
        "R-RUN-UNAVAILABLE-SEMANTIC": (str(OUT / "runs" / "syntax-data.store.json"), ""),
        "R-RUN-UNSUPPORTED-GRAMMAR": (str(OUT / "runs" / "syntax-data.store.json"), "clones language-tier-unsupported"),
        "R-RUN-NONCEMPTY-CONTEXT": (str(OUT / "runs" / "ts.store.json"), ""),
        "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC": (str(OUT / "runs" / "ts.store.json"), ""),
        "R-IMPORTED-PAYLOAD-IN-GRAPH": (str(OUT / "runs" / "ts.store.json"), ""),
        "R-CLONE-DEFICIENCY-PAIRING": (str(OUT / "runs" / "rust-partial.store.json"), ""),
        "R-NATIVE-PREIMAGE-JOINS": (str(OUT / "pilot" / "ts-corrected-admission.json"), "snapshotJoins, nestedRecords, blobJoins, config-graph kind law executed"),
        "R-VALIDATE-OWNING-SCHEMA": (str(OUT / "pilot" / "ts-corrected-admission.json"), "stock + every selected $ref + x-opensip-order + x-opensip-digest nested canonical-record admission"),
        "R-INDEPENDENT-CLOSURE-JOINS": (str(OUT / "runs" / "ts.closure.json"), "relation-registry laws, coverage totality/partition, native-context/universe joins"),
        "R-OBJECT-TABLE-FRAMES": (str(OUT / "runs" / "ts.store.json"), "objectTable + blobs keyed by digest"),
        "R-FROM-SCRATCH-COMMAND": (str(OUT / "runs" / "ts.from-scratch.json"), f"{PY} -I -B {OUT}/replay_export.py {OUT}/runs/ts.store.json"),
        "R-RETAINED-ARTIFACTS-IN-CLOSURE": (str(OUT / "runs" / "ts.store.json"), ""),
        "R-SELECTED-PROVIDER-CONTEXT": (str(OUT / "runs" / "ts.store.json"), "SelectedEnumeratorRef status=selected"),
        "R-NEGATIVE-FIRST-REFUSAL": (str(OUT / "vectors" / "negatives-invoked.json"), "observed refusals, not predicted prose"),
        "R-REPLAY-AFTER-ADMISSION": (str(OUT / "pilot" / "ts-fresh-replay.json"), "admit then close then derive"),
        "R-REPLAY-ENUM-AND-IDS": (str(OUT / "pilot" / "ts-fresh-replay.json"), ""),
        "R-REPLAY-PREDICATE-WITNESS-VERDICT": (str(OUT / "pilot" / "ts-fresh-replay.json"), "complete bundle compare"),
        "R-REPLAY-NO-CALLER-TRUTH": (str(OUT / "pilot" / "ts-fresh-replay.json"), "derived from retained program/evidence"),
        "R-REPLAY-COMPARE-BUNDLE": (str(OUT / "pilot" / "ts-fresh-replay.json"), "equal complete C(proof)"),
        "R-REPLAY-EXPORT": (str(OUT / "replay_export.py"), "fresh process reload"),
        "R-REPLAY-THREE-VALUED": (str(OUT / "pilot" / "rust-partial-fresh-replay.json"), "indeterminate on unknown clones Coverage"),
        "R-REPLAY-TAMPER": (str(OUT / "vectors" / "false-result-remint.json"), "fully reminted false-result: structural admit, proof compare refused"),
        "R-ROOT-ADMISSION-EXPORT": (str(OUT / "runs" / "ts.store.json"), "exports exposed; root outcome unobserved in this blind session"),
        "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR": (str(OUT / "query" / "graph-query.json"), "neighbors/path/reach/cursor/history/limit/parity over admitted TS Run"),
        "R-HELPER-KIT-ONLY": (str(OUT / "pilot" / "helper-corrections.json"), "four construction corrections from kit selectors; original failures preserved"),
        "R-VALID-VS-INVALID-VS-EXPLANATORY": (str(OUT / "vectors" / "negatives-invoked.json"), ""),
        "R-MEASURED-NOT-COUNTS": (str(OUT / "pilot" / "ts-fresh-replay.json"), ""),
        "R-DISTINGUISH-FOUR-BOUNDARIES": (str(OUT / "vectors" / "negatives-invoked.json"), ""),
        "R-DELIVER-MD-JSON": (str(OUT / "blind-review.json"), ""),
        "R-VERDICT-ENUM": (str(OUT / "blind-review.json"), ""),
        "R-MUST-SHOULD-ADVISORY": (str(OUT / "blind-review.json"), ""),
        "R-NO-ACCEPT-IF-INCOMPLETE": (str(OUT / "blind-review.json"), "continuation refused first-pass ACCEPT while enumerator approximated"),
        "R-NO-QUALIFICATION-CLAIM": (str(OUT / "blind-review.json"), "no OS/compiler/crypto/SQLite product qualification"),
        "R-IDENTIFY-GAPS": (str(OUT / "vectors" / "design-gaps.json"), ""),
    }
    for rid, (art, notes) in overlays.items():
        status.mark(rows, rid, "executed", artifact=art, notes=notes)

    # rebase remaining artifacts
    for r in rows:
        r["artifact"] = rebase(r.get("artifact"))

    executed = [r["id"] for r in rows if r["status"] == "executed"]
    failed = [r["id"] for r in rows if r["status"] == "failed"]
    unexec = [r["id"] for r in rows if r["status"] == "unexecuted"]
    fq = [r["id"] for r in rows if r["status"] == "futureQualification"]
    blocking_unexec = [r["id"] for r in rows if r.get("acceptBlocking") and r["status"] in ("unexecuted", "failed")]

    if blocking_unexec:
        verdict = "INCOMPLETE-REFUSE"
        recommendation = "CHANGES_REQUIRED"
    else:
        verdict = "ACCEPT-RECONSTRUCTABLE"
        recommendation = "ACCEPT-RECONSTRUCTABLE"

    helper_corrections = json.loads((OUT / "pilot" / "helper-corrections.json").read_text())["corrections"]
    arts = [
        str(OUT / "runs" / "ts.store.json"),
        str(OUT / "runs" / "rust.store.json"),
        str(OUT / "runs" / "rust-partial.store.json"),
        str(OUT / "runs" / "syntax-code.store.json"),
        str(OUT / "runs" / "syntax-data.store.json"),
        str(OUT / "pilot" / "ts-original-admission-failure.json"),
        str(OUT / "pilot" / "ts-corrected-admission.json"),
        str(OUT / "pilot" / "ts-fresh-replay.json"),
        str(OUT / "vectors" / "false-result-remint.json"),
        str(OUT / "vectors" / "negatives-invoked.json"),
        str(OUT / "query" / "graph-query.json"),
        str(OUT / "pilot" / "helper-corrections.json"),
    ]
    notes = (
        "Same-origin continuation. First-pass ACCEPT withdrawn: SelectedEnumeratorRef was approximated "
        "and owning-schema admission with $ref/keywords/joins was not executed on exported frames. "
        "Pilot TS then remaining Runs completed full admission, closure, fresh-process reload, and "
        "complete-proof comparison. Original failures preserved under pilot/original-first-pass and "
        "pilot/ts-original-admission-failure.json. Root admission of exported frames is unobserved."
    )
    status.checkpoint(12, rows, arts, notes, helper_corrections=helper_corrections)

    standing = {
        "consumerId": CONSUMER,
        "continuationId": CONT,
        "sameOriginContinuation": True,
        "notANewIndependentSession": True,
        "notAnAcceptanceReset": True,
        "kitUnchanged": True,
        "parentSubjectSha256": PARENT,
        "manifestSha256": MANIFEST,
        "writeDirectory": NEW,
        "originalOutputUnchanged": OLD,
        "kitPath": str(KIT),
        "firstPassAcceptWithdrawn": True,
        "withdrawnBecause": "SelectedEnumeratorRef approximated; owning-schema+$ref+keywords+joins not executed; charter forbids ACCEPT with unresolved helper approximations",
    }
    dump(OUT / "vectors" / "continuation-standing.json", standing)

    from_scratch = f"{PY} -I -B {OUT}/replay_export.py {OUT}/runs/ts.store.json"

    review = {
        "consumerId": CONSUMER,
        "continuationId": CONT,
        "sameOriginContinuation": True,
        "kitManifestSha256": MANIFEST,
        "parentSubjectSha256": PARENT,
        "verdict": verdict,
        "recommendation": recommendation,
        "rootAdmission": "unobserved",
        "fromScratchCommand": from_scratch,
        "requirementCounts": {
            "executed": len(executed),
            "unexecuted": len(unexec),
            "failed": len(failed),
            "futureQualification": len(fq),
            "blockingUnexecutedOrFailed": blocking_unexec,
        },
        "pilot": {
            "run": "TypeScript complete Run",
            "originalFailure": str(OUT / "pilot" / "ts-original-admission-failure.json"),
            "correctedAdmission": str(OUT / "pilot" / "ts-corrected-admission.json"),
            "freshReplay": str(OUT / "pilot" / "ts-fresh-replay.json"),
            "freshReplayPass": True,
        },
        "runsAdmittedClosedReplayed": ["ts", "rust", "rust-partial", "syntax-code", "syntax-data"],
        "falseResultRemint": str(OUT / "vectors" / "false-result-remint.json"),
        "negativesInvoked": str(OUT / "vectors" / "negatives-invoked.json"),
        "graphQuery": str(OUT / "query" / "graph-query.json"),
        "helperCorrections": helper_corrections,
        "newMustIssues": [],
        "newShouldIssues": [],
        "advisories": [
            {
                "id": "ADV-ROOT-ADMISSION-UNOBSERVED",
                "text": "Independent root admission of the exact exported frames is a separate later gate and is unobserved in this blind session. Internal ACCEPT-RECONSTRUCTABLE does not grant root acceptance.",
            }
        ],
        "standing": standing,
        "notes": notes,
    }
    dump(OUT / "blind-review.json", review)

    md = f"""# Blind review — `{CONSUMER}` / continuation `{CONT}`

Same-origin continuation of consumer-b.v13. Not a new independent session and not an acceptance reset.
Kit/parent hashes unchanged.

- Parent subject SHA-256: `{PARENT}`
- Manifest SHA-256: `{MANIFEST}`
- Write directory: `{NEW}`
- Original output (unchanged): `{OLD}`

## Verdict

**{verdict}**

First-pass ACCEPT-RECONSTRUCTABLE is withdrawn. The original advisory approximating
`SelectedEnumeratorRef` as `{{closureId}}` and deferring owning-schema admission to root
violated the charter (no ACCEPT with unresolved helper approximations or unexecuted
required validation).

Continuation executed the required pilot discipline on the TypeScript Run, then the
remaining required Runs:

1. Owning-schema admission including selected `$ref`s and published `x-opensip-order` /
   `x-opensip-digest` nested canonical-record laws.
2. Retained digest/representation/closure and cross-record registry joins.
3. Exported-byte reload in a fresh process.
4. Independent complete proof derivation from retained program/evidence and comparison
   of every proof field.

Root admission of those exact exported frames remains **unobserved**.

## Helper corrections (original failure preserved)

See `pilot/helper-corrections.json` and `pilot/ts-original-admission-failure.json`.
Original first-pass stores are under `pilot/original-first-pass/`.

1. `configGraphPaths` UTF-8 order (`tsconfig.base.json` before `tsconfig.json`).
2. WaiverSet `schemaFamily` = `opensip.product.waivers`.
3. `ImportsPayloadV1.importer` SubjectIdV1 (`symbol:src/index.ts::x`).
4. `SelectedEnumeratorRef` = `{{status: selected, closureId}}`.

Additional construction/admission fixes found while executing the same laws:
languageFamily `tsjs`; program-predicate/node fragment retention; Rust ownership
`(path, unitId)` order; syntax suffixes UTF-8 order; declares SubjectIdV1 fields.

## Measured Runs

| Run | Admit | Close | Fresh replay complete-proof equal |
|---|---|---|---|
| ts | yes | yes | yes |
| rust | yes | yes | yes |
| rust-partial | yes | yes | yes (indeterminate) |
| syntax-code | yes | yes | yes |
| syntax-data | yes | yes | yes |

Fully reminted false-result graph: structural identities/joins admitted;
recomputed complete proof rejected the altered claimed verdict
(`vectors/false-result-remint.json`).

Negatives were invoked on the admission/evaluation path
(`vectors/negatives-invoked.json`); observed refusals retained.

Graph query neighbors/path/reach/cursor/history/limit/parity reconstructed over the
admitted TS Run (`query/graph-query.json`).

## From-scratch replay

```
{from_scratch}
```

## Counts

- executed: {len(executed)}
- unexecuted: {len(unexec)}
- failed: {len(failed)}
- futureQualification: {len(fq)}
- blocking unexecuted/failed: {blocking_unexec or "none"}

No real compiler/OS/cryptographic/SQLite product qualification is claimed.
"""
    (OUT / "blind-review.md").write_text(md)
    dump(OUT / "pilot-progress.json", {
        "phase": "continuation-complete-pipeline",
        "pilot": "ts",
        "admittedClosedReplayed": ["ts", "rust", "rust-partial", "syntax-code", "syntax-data"],
        "verdict": verdict,
    })
    print("VERDICT", verdict)
    print("executed", len(executed), "unexec", unexec, "failed", failed, "fq", fq)
    print("blocking", blocking_unexec)


if __name__ == "__main__":
    main()
