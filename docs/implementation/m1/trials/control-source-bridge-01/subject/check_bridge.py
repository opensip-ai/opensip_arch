"""Reference check for the common-control source-selection bridge candidate.

Developer evidence only. It reads this closure and declared, pinned architecture
bytes, executes only the snapshotted accepted design verifier and writes only
under TMPDIR. It is not acceptance, runtime authorization or qualification.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import tempfile
import types
from pathlib import Path

UNIT = Path(__file__).resolve().parent
STAGED = "docs/implementation/m1/control-source-v1"
SCHEMA = {"path": "docs/coop/completion/control-completion.schema.v3.json",
          "sha256": "2929de62e9eb3a3dc78959eaf3d50361b8d1f895d086940724c1c743ac46a98c", "bytes": 22476}
SCHEMA_ID = "urn:opensip:design:control-schema:3"
APPLICATION = {"path": "docs/coop/completion/architecture-application.v1.json",
               "sha256": "15b3932adaf1c37f43a3b12e0af66fedbddc10cdd396c64105ac170c6d4bd7f3", "bytes": 443974}
SELECTOR = "/units/control"
SCHEMA_EVIDENCE = "/evidenceTargets/C.BODIES/sources/1"
REVIEW_VERDICT = "NO-OBJECTION-WITHIN-REPAIR-SCOPE"
REPORT_MEMBER = "control-completion.report.v5.json"
FROZEN_MEMBERS = 8
VERIFIER = {"path": "tools/verify_design.py",
            "sha256": "1dce4b8a01255228b1d29e322e089b2a0cfc2d5a2ba5e4e862c2d32d9b248948", "bytes": 28077}
LOCK = {"path": "design-lock.json",
        "sha256": "90e0533fc03d545888a0b68b985ebfa404aa462cec5adba586cebb907802a618", "bytes": 12505}
BINDING_INTEGRATION = "docs/implementation/m1/design-binding4-correction-integration.v1.json"
GENERATION_UNIT = "docs/implementation/m1/control-generation-unit.v1.json"
TRIAL_SUBJECT = "docs/implementation/m1/trials/control-generation-01/subject"
ROUTE = "docs/implementation/m1/control-source-route.v1.json"
REFUSAL = "generation source is not selected by accepted design"
SYNTHETIC_MARKER = "syntheticFixtureNotAcceptance"


class BridgeError(ValueError):
    """The bridge candidate does not match its historical evidence."""


def need(condition, message):
    if not condition:
        raise BridgeError(message)


def pin_of(path, raw):
    return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def load_verifier(unit):
    """Execute the exact accepted verifier bytes and record every file it opens."""
    raw = (unit / "snapshot" / "verify_design.py").read_bytes()
    need(pin_of(VERIFIER["path"], raw) == VERIFIER, "snapshot verifier differs from accepted binding4 correction")
    need(pin_of(LOCK["path"], (unit / "snapshot" / "design-lock.json").read_bytes()) == LOCK,
         "snapshot lock differs from accepted binding4 correction")
    module = types.ModuleType("snapshot_verify_design")
    exec(compile(raw, str(unit / "snapshot" / "verify_design.py"), "exec"), module.__dict__)
    original, reads = module.relative_file, []

    def recording(root, value):
        result = original(root, value)
        reads.append((Path(root), value))
        return result

    module.relative_file = recording
    return module, reads


class Declared:
    """Architecture reads are refused unless declared; discovery pins current bytes."""

    def __init__(self, verifier, architecture, rows, discover=False):
        self.verifier, self.architecture, self.discover = verifier, architecture, discover
        self.rows = {row["path"]: row for row in rows}

    def pin(self, path):
        need(isinstance(path, str), "architecture path must be a string")
        if self.discover:
            return pin_of(path, self.verifier.relative_file(self.architecture, path).read_bytes())
        need(path in self.rows, f"undeclared architecture read: {path}")
        return self.rows[path]

    def read(self, path):
        return self.verifier.pinned_bytes(self.architecture, self.pin(path))

    def json(self, path):
        return self.verifier.object_value(self.verifier.decode(self.read(path)), path)


def load_inputs(verifier, unit):
    inputs = verifier.object_value(verifier.decode((unit / "inputs.json").read_bytes()), "inputs")
    need(set(inputs) == {"schemaVersion", "standing", "snapshots", "architecture"} and inputs["schemaVersion"] == 1,
         "unsupported declared inputs")
    need(inputs["snapshots"] == [{**VERIFIER, "path": "snapshot/verify_design.py", "acceptedAs": VERIFIER["path"]},
                                 {**LOCK, "path": "snapshot/design-lock.json", "acceptedAs": LOCK["path"]}],
         "declared snapshots differ from accepted binding4 correction")
    rows = verifier.pin_rows(inputs["architecture"], "declared architecture inputs")
    need(all(isinstance(row, dict) and set(row) == {"path", "sha256", "bytes"} for row in rows),
         "declared architecture inputs must be exact pins")
    return rows


def check_snapshot_provenance(verifier, declared):
    integration = declared.json(BINDING_INTEGRATION)
    unit_pin = verifier.object_value(integration.get("unit"), "integration unit")
    need(declared.pin(unit_pin.get("path")) == unit_pin, "binding4 correction unit pin differs")
    unit = declared.json(unit_pin["path"])
    need(unit.get("status") == "ACCEPTED-UNIT" and unit.get("rootSubstantiveAssent") is True
         and unit.get("requiredUnitFindings") == [], "binding4 correction is not an accepted unit")
    review_pin = verifier.object_value(unit.get("actualClaudeReview"), "binding4 review")
    manifest_pin = verifier.object_value(unit.get("subjectManifest"), "binding4 subject")
    need(declared.pin(review_pin.get("path")) == review_pin and declared.pin(manifest_pin.get("path")) == manifest_pin,
         "binding4 correction review or subject pin differs")
    review = declared.json(review_pin["path"])
    need(review.get("verdict") == "ACCEPT-UNIT" and review.get("requiredFindings") == []
         and review.get("subjectManifestSha256") == manifest_pin["sha256"], "binding4 correction review does not accept its subject")
    for rows in (declared.json(manifest_pin["path"]).get("files"), integration.get("files")):
        need(isinstance(rows, list), "binding4 file rows must be a list")
        by_path = {row.get("path"): row for row in rows if isinstance(row, dict)}
        need(by_path.get(VERIFIER["path"]) == VERIFIER and by_path.get(LOCK["path"]) == LOCK,
             "snapshot is not the accepted and integrated binding4 verifier and lock")
    return {"integration": BINDING_INTEGRATION, "unit": unit_pin["path"], "review": review_pin["path"]}


def check_base_selection(verifier, declared, lock, record):
    approvals = lock["approvals"]
    documents = []
    for key in ("sourceManifest", "applicationManifest"):
        need(declared.pin(approvals[key]["path"]) == approvals[key], f"declared {key} differs from lock")
        documents.append(declared.json(approvals[key]["path"]))
    source, application = documents
    source_rows = [row for row in source["files"] if row.get("path") == APPLICATION["path"]]
    need(source_rows == [APPLICATION], "architecture application is not exactly selected by source45")
    need(all(row.get("path") != APPLICATION["path"] for row in application["files"]),
         "application46 overrides the architecture application")
    need(record.get("parents") == [APPLICATION], "successor parent must be exactly the accepted architecture application")
    selection = verifier.object_value(record.get("selection"), "selection")
    need(selection.get("baseApproval") == {"sourceManifest": approvals["sourceManifest"],
                                           "applicationManifest": approvals["applicationManifest"],
                                           "parentSelectedBy": "sourceManifest", "parentOverriddenByApplication": False},
         "successor base approval differs from live lock")
    effective = {}
    for document in documents:
        for row in document["files"]:
            effective[row["path"]] = row
    return effective


def accepted_rows(effective, lock, base):
    accepted = dict(effective)
    for binding in lock["inventorySuccessors"]:
        accepted[binding["candidate"]["path"]] = binding["candidate"]
    for binding, result in zip(lock["contractSuccessors"], base["contractSuccessors"]):
        for row in (binding["record"], *result["inputs"]):
            accepted[row["path"]] = row
    return accepted


def check_selector(verifier, declared, record):
    selection = verifier.object_value(record.get("selection"), "selection")
    need(selection.get("parentSelector") == {"parent": APPLICATION, "jsonPointer": SELECTOR},
         "parent selector differs from accepted /units/control")
    need(selection.get("parentSchemaEvidence") == {"parent": APPLICATION, "jsonPointer": SCHEMA_EVIDENCE},
         "parent schema evidence selector differs")
    raw = declared.read(APPLICATION["path"])
    control = verifier.object_value(verifier.selected_passage(raw, {"jsonPointer": SELECTOR}), "control unit")
    need(control.get("reviewStanding") == REVIEW_VERDICT, "application control review standing differs")
    evidence = verifier.object_value(record.get("evidence"), "evidence")
    refs = {}
    for key, field in (("review", "independentReview"), ("freeze", "freeze")):
        ref = control.get(key)
        need(isinstance(ref, dict) and set(ref) == {"path", "pin"}, f"application control {key} must be path and pin")
        pin = evidence.get(field)
        need(isinstance(pin, dict) and pin.get("path") == ref["path"] and pin.get("sha256") == ref["pin"],
             f"successor {field} differs from application control {key}")
        need(declared.pin(ref["path"]) == pin, f"successor {field} size or declared pin differs")
        refs[key] = pin
    source = verifier.object_value(verifier.selected_passage(raw, {"jsonPointer": SCHEMA_EVIDENCE}), "schema evidence")
    need(source.get("path") == SCHEMA["path"] and source.get("pin") == SCHEMA["sha256"],
         "application evidence does not pin the exact control schema")
    target = verifier.selected_passage(raw, {"jsonPointer": SCHEMA_EVIDENCE.rsplit("/", 2)[0]})
    need(isinstance(target, dict) and target.get("unit") == "control", "schema evidence target is not the control unit")
    status = verifier.decode(raw).get("status")
    return refs, status


def check_review_freeze(review, freeze, freeze_sha256):
    """Join review5 to the exact freeze; pure so drift can be tested directly."""
    need(review.get("artifact") == "control-completion-independent-review" and type(review.get("version")) is int
         and review["version"] == 5, "not the control independent review5")
    need(review.get("verdict") == REVIEW_VERDICT, "control review verdict differs")
    need(review.get("mustFindings") == [] and review.get("requiredFindings", []) == [], "control review findings remain")
    need(review.get("subjectUnchanged") is True, "control review subject changed")
    files = freeze.get("files")
    need(isinstance(files, dict) and len(files) == FROZEN_MEMBERS, "control freeze must contain exactly eight members")
    need(all(isinstance(name, str) and name and "/" not in name and isinstance(value, str) and len(value) == 64
             and all(c in "0123456789abcdef" for c in value) for name, value in files.items()),
         "control freeze member names or digests are malformed")
    subject = review.get("subject")
    need(isinstance(subject, dict) and subject.get("freezeSha256") == freeze_sha256, "control review names a different freeze")
    need(subject.get("files") == files and review.get("postReviewHashes") == files,
         "control review subject or post-review hashes differ from freeze")
    replay = review.get("replay")
    need(isinstance(replay, dict) and type(replay.get("passed")) is int and replay.get("passed") == replay.get("total")
         and replay["passed"] > 0 and replay.get("matchesRetainedReport") is True
         and replay.get("reportSha256") == files.get(REPORT_MEMBER), "control review replay does not join the frozen report")
    need(files.get(SCHEMA["path"].rsplit("/", 1)[1]) == SCHEMA["sha256"], "control freeze does not pin the exact schema")
    return files


def check_members(declared, record, freeze_pin, files):
    base = freeze_pin["path"].rsplit("/", 1)[0]
    rows = []
    for name, digest in files.items():
        pin = declared.pin(f"{base}/{name}")
        need(pin["sha256"] == digest, f"frozen member pin differs: {name}")
        declared.read(pin["path"])
        rows.append(pin)
    rows.sort(key=lambda row: row["path"])
    evidence = record["evidence"]
    need(evidence.get("frozenMembers") == rows, "successor frozen member pins differ from freeze")
    need(evidence.get("reviewVerdict") == REVIEW_VERDICT and evidence.get("reviewMustFindings") == [],
         "successor review verdict or findings differ")
    return rows


def check_candidate_scope(verifier, declared, record, accepted, members):
    need(record.get("candidates") == [SCHEMA], "successor must select exactly the existing control schema")
    need(record.get("passageOverrides") == [], "control source bridge must not override passages")
    need(record.get("acceptanceDoesNotQualifyProduct") is True, "successor must disclaim product qualification")
    need(SCHEMA in members, "selected schema is not a frozen reviewed member")
    document = verifier.object_value(verifier.decode(declared.read(SCHEMA["path"])), "control schema")
    need(document.get("$id") == SCHEMA_ID and record["selection"].get("schemaId") == SCHEMA_ID, "control schema ID differs")
    need(SCHEMA["path"] not in accepted, "control schema path is already selected by accepted design")
    need(all(row.get("sha256") != SCHEMA["sha256"] for row in accepted.values()),
         "control schema bytes are already selected under another path")


def check_selection_subject(verifier, unit, record_raw):
    raw = (unit / "selection-subject.json").read_bytes()
    subject = verifier.object_value(verifier.decode(raw), "selection subject")
    need(set(subject) == {"schemaVersion", "standing", "files"} and subject["schemaVersion"] == 1,
         "unsupported selection subject")
    expected = sorted([SCHEMA, pin_of(f"{STAGED}/successor.json", record_raw)], key=lambda row: row["path"])
    need(subject["files"] == expected, "selection subject must contain exactly the successor and existing schema")
    return pin_of(f"{STAGED}/selection-subject.json", raw)


def check_generation_join(verifier, declared):
    unit = declared.json(GENERATION_UNIT)
    need(unit.get("status") == "ACCEPTED-UNIT" and unit.get("rootSubstantiveAssent") is True
         and unit.get("requiredUnitFindings") == [] and unit.get("integrationApproved") is False,
         "control generation unit standing differs")
    review_pin, manifest_pin = unit.get("actualClaudeReview"), unit.get("subjectManifest")
    need(isinstance(review_pin, dict) and isinstance(manifest_pin, dict), "control generation pins missing")
    need(declared.pin(review_pin.get("path")) == review_pin and declared.pin(manifest_pin.get("path")) == manifest_pin,
         "control generation review or subject pin differs")
    review = declared.json(review_pin["path"])
    need(review.get("verdict") == "ACCEPT-UNIT" and review.get("requiredFindings") == []
         and review.get("subjectManifestSha256") == manifest_pin["sha256"], "control generation review does not accept its subject")
    rows = {row["path"]: row for row in declared.json(manifest_pin["path"])["files"]}

    def trial(path):
        need(path in rows, f"control generation subject lacks {path}")
        full = f"{TRIAL_SUBJECT}/{path}"
        need(declared.pin(full) == {**rows[path], "path": full}, f"trial copy differs from reviewed subject: {path}")
        return declared.read(full)

    files = {"schemas/source-map.json": trial("schemas/source-map.json"),
             "schemas/registry.json": trial("schemas/registry.json")}
    mapping = verifier.decode(files["schemas/source-map.json"])
    control = [row for row in mapping["sources"] if row.get("architectureSource") == SCHEMA]
    need(len(control) == 1, "reviewed source map must map the exact control schema once")
    for row in mapping["sources"]:
        files[row["implementationPath"]] = trial(row["implementationPath"])
    need(files[control[0]["implementationPath"]] == declared.read(SCHEMA["path"]), "generated control source bytes differ")
    return files, control[0]["implementationPath"]


def write_tree(root, files):
    for path, raw in files.items():
        target = root.joinpath(*path.split("/"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return root


def without_source(verifier, files, path):
    result = {key: value for key, value in files.items() if key != path}
    for name, field in (("schemas/source-map.json", "implementationPath"), ("schemas/registry.json", "sourcePath")):
        document = verifier.decode(files[name])
        document["sources"] = [row for row in document["sources"] if row.get(field) != path]
        result[name] = (json.dumps(document, indent=2) + "\n").encode()
    return result


def check_live_preflight(verifier, architecture, lock, files, control_path):
    with tempfile.TemporaryDirectory(prefix="control-bridge-") as tmp:
        try:
            verifier.verify(architecture, lock, write_tree(Path(tmp) / "reviewed", files))
        except verifier.DesignError as exc:
            need(str(exc) == REFUSAL, f"unexpected live source preflight refusal: {exc}")
        else:
            raise BridgeError("live lock unexpectedly selects the control source")
        result = verifier.verify(architecture, lock, write_tree(Path(tmp) / "without-control",
                                                                without_source(verifier, files, control_path)))
    return {"liveRefusal": REFUSAL, "sourcesVerifiedWithoutControl": result["generationSources"]["sourcesVerified"]}


def check_route(declared, lock, refs):
    """The untracked route note is informational; mismatch is reported, not normative."""
    route = declared.json(ROUTE)
    return (route.get("chain") == [APPLICATION, refs["review"], refs["freeze"], SCHEMA]
            and route.get("sourceManifestSha256") == lock["approvals"]["sourceManifest"]["sha256"]
            and route.get("applicationManifestSha256") == lock["approvals"]["applicationManifest"]["sha256"]
            and route.get("schemaId") == SCHEMA_ID and route.get("requiredFindings") == [])


def verify_bridge(architecture, unit=UNIT, discover=False):
    verifier, reads = load_verifier(unit)
    rows = load_inputs(verifier, unit)
    declared = Declared(verifier, architecture, rows, discover)
    lock = verifier.decode((unit / "snapshot" / "design-lock.json").read_bytes())
    base = verifier.verify(architecture, lock)
    record_raw = (unit / "successor.json").read_bytes()
    record = verifier.object_value(verifier.decode(record_raw), "successor")
    provenance = check_snapshot_provenance(verifier, declared)
    effective = check_base_selection(verifier, declared, lock, record)
    accepted = accepted_rows(effective, lock, base)
    refs, application_status = check_selector(verifier, declared, record)
    files = check_review_freeze(declared.json(refs["review"]["path"]), declared.json(refs["freeze"]["path"]),
                                refs["freeze"]["sha256"])
    members = check_members(declared, record, refs["freeze"], files)
    check_candidate_scope(verifier, declared, record, accepted, members)
    subject_pin = check_selection_subject(verifier, unit, record_raw)
    generation, control_path = check_generation_join(verifier, declared)
    preflight = check_live_preflight(verifier, architecture, lock, generation, control_path)
    route = check_route(declared, lock, refs)
    observed = {value for root, value in reads if root == architecture}
    if discover:
        return sorted((pin_of(path, verifier.relative_file(architecture, path).read_bytes()) for path in observed),
                      key=lambda row: row["path"])
    undeclared, unused = sorted(observed - set(declared.rows)), sorted(set(declared.rows) - observed)
    need(not undeclared and not unused, f"declared inputs differ from reads: undeclared={undeclared} unused={unused}")
    for row in rows:
        verifier.pinned_bytes(architecture, row)
    return {"passed": True, "baseLock": {"inputsVerified": base["inputsVerified"],
                                         "contractSuccessors": len(base["contractSuccessors"])},
            "snapshotProvenance": provenance, "parent": APPLICATION, "parentSelector": SELECTOR,
            "applicationHistoricalStatus": application_status, "independentReview": refs["review"],
            "freeze": refs["freeze"], "reviewVerdict": REVIEW_VERDICT, "reviewMustFindings": 0,
            "frozenMembersVerified": len(members), "candidate": SCHEMA, "candidateAlreadyAccepted": False,
            "selectionSubject": subject_pin, "sourcePreflight": preflight, "routeNoteConsistent": route,
            "declaredArchitectureReads": len(rows), "acceptance": False, "productQualification": False}


def verify_staged(architecture, binding, unit=UNIT, allow_synthetic=False):
    """Run the snapshot verifier over the live lock plus one appended contract binding."""
    verifier, reads = load_verifier(unit)
    declared = Declared(verifier, architecture, load_inputs(verifier, unit))
    need(isinstance(binding, dict) and set(binding) == {"record", "subjectManifest", "review", "assent"},
         "staged binding requires record, subjectManifest, review and assent")
    record_raw = (unit / "successor.json").read_bytes()
    need(binding["record"] == pin_of(f"{STAGED}/successor.json", record_raw), "staged record is not this successor")
    need(binding["subjectManifest"] == check_selection_subject(verifier, unit, record_raw),
         "staged subject is not this selection subject")
    for key in ("review", "assent"):
        document = verifier.decode(verifier.pinned_bytes(architecture, binding[key]))
        synthetic = (isinstance(document, dict) and SYNTHETIC_MARKER in document) or binding[key]["path"].startswith("synthetic")
        need(allow_synthetic or not synthetic, f"synthetic {key} fixture cannot stand as acceptance")
    lock = verifier.decode((unit / "snapshot" / "design-lock.json").read_bytes())
    staged = copy.deepcopy(lock)
    staged["contractSuccessors"].append(binding)
    generation, _ = check_generation_join(verifier, declared)
    with tempfile.TemporaryDirectory(prefix="control-bridge-staged-") as tmp:
        result = verifier.verify(architecture, staged, write_tree(Path(tmp) / "reviewed", generation))
    unit_result = result["contractSuccessors"][-1]
    need(unit_result["inputs"] == [SCHEMA] and unit_result["passageOverrides"] == [], "staged unit selects different inputs")
    allowed = set(declared.rows) | {pin["path"] for pin in binding.values()}
    extra = sorted({value for root, value in reads if root == architecture} - allowed)
    need(not extra, f"staged verification read undeclared architecture files: {extra}")
    return {"contractSuccessors": len(result["contractSuccessors"]), "selectedInputs": unit_result["inputs"],
            "generationSourcesVerified": result["generationSources"]["sourcesVerified"],
            "syntheticFixtures": allow_synthetic, "productQualification": False}


def require_environment():
    need(sys.flags.dont_write_bytecode, "run with python -B")
    tmp = os.environ.get("TMPDIR")
    need(bool(tmp) and Path(tmp).resolve().is_dir() and not Path(tmp).resolve().is_relative_to(UNIT),
         "set TMPDIR to an existing directory outside this closure")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", required=True, type=Path)
    parser.add_argument("--review", help="architecture-relative actual review for a staged lock check")
    parser.add_argument("--assent", help="architecture-relative actual root assent for a staged lock check")
    parser.add_argument("--discover-inputs", action="store_true", help="print observed architecture reads as pins")
    args = parser.parse_args()
    architecture = args.architecture.resolve()
    try:
        require_environment()
        if args.discover_inputs:
            print(json.dumps(verify_bridge(architecture, discover=True), indent=2))
            return
        report = verify_bridge(architecture)
        need((args.review is None) == (args.assent is None), "--review and --assent go together")
        if args.review:
            verifier, _ = load_verifier(UNIT)
            record_raw = (UNIT / "successor.json").read_bytes()
            binding = {"record": pin_of(f"{STAGED}/successor.json", record_raw),
                       "subjectManifest": check_selection_subject(verifier, UNIT, record_raw),
                       "review": pin_of(args.review, verifier.relative_file(architecture, args.review).read_bytes()),
                       "assent": pin_of(args.assent, verifier.relative_file(architecture, args.assent).read_bytes())}
            report["stagedBinding"] = binding
            report["staged"] = verify_staged(architecture, binding)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Bridge check failed: {exc}\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
