"""Seal helper (not executed by check.py). Writes, in order and without self-hashing:
1. source-pins.json: exact bytes of every external file (and directory listing) read or executed by a traced check run;
2. successor.json: selectors, conditional overrides, supersession and closure references;
3. subject-files.json: every subject file except itself, including seal.py.
The external freeze anchor is the SHA-256 of subject-files.json, printed at the end. The traced run is the only child process and belongs to sealing,
not to the check: check.py itself refuses child processes.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
SUBJECT = ["check.py", "report_model.py", "build_owner.py", "build_fixtures.py", "seal.py", "fixtures.json", "report-projection.schema.json",
           "owner/command-envelope.v5.schema.json", "owner/command-inventory.v5.schema.json", "owner/command-inventory.v5.json",
           "owner/implementation-coverage-successor.v1.json", "owner/passage-overrides.v1.json", "owner/design-obligations.v1.json", "owner/budget-derivations.v1.json",
           "owner/builtin-step-planning.v1.json", "owner/query-fixture-correction.v1.json",
           "source-pins.json", "successor.json", "contract.md"]


def pin(path):
    raw = Path(path).read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def main():
    trace = HERE / "closure-trace.json"
    run = subprocess.run([PY, "-I", "-B", str(HERE / "check.py"), "--architecture", str(ARCH), "--trace-closure", str(trace)], capture_output=True, text=True)
    if run.returncode != 0:
        sys.stderr.write(run.stdout[-2000:] + run.stderr[-4000:])
        raise SystemExit("traced check failed")
    traced = json.loads(trace.read_text())
    trace.unlink()
    forbidden = [p for p in traced["files"] if p.endswith(".pyc") or p == str(ARCH / "docs/implementation/README.md")]
    assert not forbidden, forbidden
    files = [pin(p) for p in sorted(set(traced["files"]))]
    listings = [{"path": d, "entriesSha256": hashlib.sha256("\n".join(sorted(os.listdir(d))).encode()).hexdigest()} for d in sorted(set(traced["directories"]))]
    (HERE / "source-pins.json").write_text(json.dumps({"schemaVersion": 1, "standing": "exact external closure observed by an audit-hooked, fresh-source-loaded check run (including the in-process historical metadata checker); enforced before import and at every open/listing",
                                                        "roots": traced["roots"], "files": files, "directoryListings": listings}, indent=1) + "\n")
    successor = {
        "schemaVersion": 1,
        "standing": "AUTHOR-07 correction candidate for actual separate review and root acceptance; not approval. Carrier-unit readiness only; report design readiness is blocked by owner/design-obligations.v1.json (all 11 feature blockers open), M1 final integration is blocked by RP-OBL-C01 and RP-OBL-C02, M5 workflow delivery additionally by RP-OBL-P01 and RP-OBL-X01, and AUDIT-G10 stays open. RP-OBL-K01 is closed by the accepted coverage-prerequisite unit.",
        "coverageBase": {"acceptedUnit": "docs/implementation/m1/coverage-prerequisite-unit.v1.json", "subjectManifest": "docs/implementation/m1/trials/coverage-prerequisite-01/subject-manifest.json",
                         "subjectManifestSha256": "480350895e0943c26db10eb6fd5277709733a169510a7c6f7cfdd2a421bf7ff9",
                         "coverage": "docs/implementation/m1/trials/coverage-prerequisite-01/subject/implementation-coverage.v3.json", "workaround": "none"},
        "ownerSuccessorProposals": {
            "builtinStepPlanning": {"record": "owner/builtin-step-planning.v1.json",
                                    "selectorDelta": {"file": "owner/command-inventory.v5.schema.json", "selector": "/$defs/Command/properties/steps/description", "before": "absent", "after": "owner/builtin-step-planning.v1.json#/inventoryStepsCorrection/after"},
                                    "sources": "owner/builtin-step-planning.v1.json#/sources (pinned in source-pins.json)"},
            "queryFixtureCorrection": {"record": "owner/query-fixture-correction.v1.json",
                                       "selectors": ["docs/coop/design-corrections/workflows/query_surface_projection.v3.py lines 621-627 and 513", "docs/coop/design-corrections/workflows/query-projection-contract.v3.md lines 136 and 140"],
                                       "parentsEdited": False},
            "otherReportFeatureOwners": "unchanged; RP-DO-03/05/09/10 are being closed separately by /tmp/opensip-implementation/m1-report-evidence-design-author-01 and are not duplicated here"},
        "interruptionSuccessorDependencies": {
            "subject05": {"path": "/tmp/opensip-implementation/m1-interruption-envelope-subject-05", "manifestSha256": "34556f3f16d45879519016d95419880eb8edee63eb446a7c15f7c4ac2799530f",
                          "envelope6SchemaSha256": "fd2663c2673fdcf65affaf04d1cee9a6fa6345ac9f685f6470288e08d723f343",
                          "selectedErrorRule": "every before-settle interrupted carrier carries the complete in-step-order recorded request-rejected/operational-failed details (optional included, skipped/cancelled excluded); nonempty in errors exactly; empty: failure errors [] and run/invocation errors absent",
                          "finalRebaseDuties": ["select the accepted envelope/report parent and apply the prose spans and model line together", "rebase report cancellation Run selection (RP-OBL-C02) and the empty-list pending goldens (RP-OBL-C01)", "bind metadata/CLI/generated sources and renderer branches to the selected major"],
                          "adoptedByThisCandidate": False},
            "supersededReferences": {"path": "/tmp/opensip-implementation/m1-interruption-envelope-subject-03", "manifestSha256": "dcec8ab9ad2f638a9a7ae6332d27485011fad002faeef05fc6e7c8f7c11d4e14",
                          "standing": "root unreviewed, not selected; changes cancellation Run selection to include optional analysis/verify commits (RP-OBL-C02) and adds host joins; root will freeze a corrected04 supporting genuine earlier details",
                          "adoptedByThisCandidate": False}},
        "supersedes": ["/tmp/opensip-implementation/m1-report-projection-subject-06 (author-06 bytes, manifest 3b3153ced5c08fa0e8e858bc1ffc0c58278302fd5a63b3fafb59c97e7fc3131c, historical; its first wrong-cwd root run and review-06 stay historical)",
                       "/tmp/opensip-implementation/m1-report-projection-subject-05 (author-05 bytes, manifest a9f6c22a9b2af9487fc9683fdef76c58e391f5a6f64e2f8b09bfa75d288de2a4, historical)",
                       "/tmp/opensip-implementation/m1-report-projection-subject-04 (author-04 bytes, manifest 5e43e1a1034d5c8af308a0360cbdc3499b933d6f0062f58ca2712ed9e317b20e, historical)",
                       "/tmp/opensip-implementation/m1-report-projection-subject-03 (historical)", "/tmp/opensip-implementation/m1-report-projection-subject-02 (historical)",
                       "/tmp/opensip-implementation/m1-report-projection-subject-01 (historical)"],
        "envelopeParentDependency": {
            "envelope5": {"candidate": "owner/command-envelope.v5.schema.json", "sha256": "45de2b0a12fc2f1f41f3a4f50b22b5e177fad58b19e5cc5072ff808c737e789d", "bytes": 36852,
                          "bytesUnchangedFromSubject04": True},
            "envelope6": {"subject": "/tmp/opensip-implementation/m1-interruption-envelope-subject-01", "manifestSha256": "76897423bc4dd3bfaecbf6a6a0cddfe082c8545f1d4d178b62ff01753f8d71bf",
                          "standing": "root-authored, unselected, conditional successor whose parent is exactly the envelope5 bytes above; review m1-interruption-envelope-review-01 accept-conditional (F1 prose, F2 host ledger join, F3 post-commit query carrier) pending root correction",
                          "adoptedByThisCandidate": False,
                          "consequence": "the pre-Run interruption form stays pending integration (RP-OBL-C01); if envelope6 or another successor is accepted, this candidate must rebind its envelope $ref, inventory/coverage rows and turn the pending goldens into delivered goldens"}},
        "selectors": {
            "commandEnvelope": {"historical": "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4 (metadata-v2 accepted unit, unchanged)",
                                "proposed": "urn:opensip:product-v1:workflows:evaluator3:command-envelope:5", "candidate": "owner/command-envelope.v5.schema.json"},
            "commandInventorySchema": {"historical": "urn:opensip:product-v1:workflows:evaluator3:command-inventory:4", "proposed": "urn:opensip:product-v1:workflows:evaluator3:command-inventory:5",
                                       "candidate": "owner/command-inventory.v5.schema.json"},
            "commandInventory": {"historical": "docs/implementation/m1/metadata-v2/command-inventory.v4.json", "candidate": "owner/command-inventory.v5.json"},
            "implementationCoverage": {"historical": "docs/implementation/m1/metadata-v2/implementation-coverage.v2.json", "overlayCandidate": "owner/implementation-coverage-successor.v1.json"},
            "reportProjection": {"proposed": "urn:opensip:product-v1:workflows:evaluator3:report-projection:1", "candidate": "report-projection.schema.json"},
            "designObligations": "owner/design-obligations.v1.json",
            "budgetDerivations": "owner/budget-derivations.v1.json",
            "integration": "A new integration record, not an edit of metadata-unit.v1.json, selects these successors after acceptance (RP-OBL-E01).",
        },
        "passageOverrides": "owner/passage-overrides.v1.json (conditional; parents never edited)",
        "externalClosure": "source-pins.json",
        "acceptanceDoesNotQualifyProduct": True,
    }
    (HERE / "successor.json").write_text(json.dumps(successor, indent=1) + "\n")
    manifest = {"schemaVersion": 1, "standing": "complete author-07 subject file list (this manifest excludes only itself)",
                "files": [dict(pin(HERE / name), path=name) for name in SUBJECT]}
    raw = (json.dumps(manifest, indent=1) + "\n").encode()
    (HERE / "subject-files.json").write_bytes(raw)
    print("subject-files.json sha256", hashlib.sha256(raw).hexdigest(), "files", len(SUBJECT), "external pins", len(files), "listings", len(listings))


if __name__ == "__main__":
    main()
