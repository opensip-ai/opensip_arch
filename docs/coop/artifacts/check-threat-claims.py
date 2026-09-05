#!/usr/bin/env python3
"""Validate threat-model v3 and its live operability-gate join.

  T1   weak-boundary language is qualified in architecture prose
  T2   primary risks exist
  T3   findings validate against the declared closed schema
  T4   confinement non-goals remain visible
  T5   review/status is honest
  T6   every asset is affected by a finding
  T7   finding references and mitigation/resolution shape are valid
  T8   required properties trace to findings
  T9   every property maps to exact product gate IDs
  T10  publication state is derived from DEMONSTRATED operability gates
  T11  absolutes are deliberate and scoped
  T12  V10, deletion, storage exposure, temp, secret and output repairs hold
  T13  PROJECT-ID-V1 paths, physical-isolation qualification, purge and migration recovery

Usage: python3 artifacts/check-threat-claims.py [--selftest]
"""
from __future__ import annotations

import copy
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL = ROOT / "artifacts" / "threat-model.v3.json"
OPERABILITY = ROOT / "artifacts" / "operability.v2.json"
C2 = ROOT / "artifacts" / "c2-plan-stage-schema.v3.json"
RESOLVED_INPUTS = ROOT / "artifacts" / "resolved-inputs.v2.json"
TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"),
    ("null", None),
    ("list", []),
    ("empty-object", {}),
)
TOTALITY_NESTED_CASES = TOTALITY_ROOT_CASES
MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
)

CLAIM = re.compile(r"\bsandbox\w*|\bconfine\w*|\bisolat\w*", re.I)
QUALIFIER = re.compile(
    r"not a (security )?sandbox|fault containment|trusted computing base|\bTCB\b"
    r"|unless an? OS|absent (an? )?OS|is not a boundary|never described as"
    r"|honest (promise|limit)|cannot promise|does not promise|exfiltrat",
    re.I,
)
WEAK = {"NOT A BOUNDARY", "FAULT CONTAINMENT ONLY", "TCB-ACCEPTED"}


def paragraphs(text: str):
    offset = 0
    for paragraph in re.split(r"\n\s*\n", text):
        yield offset, paragraph
        offset += len(paragraph) + 2


def publication(fixture: dict) -> str:
    if fixture.get("boundaryLanguage") and not fixture.get("boundaryQualified"):
        return "blocked-weak-boundary-language"
    if fixture.get("gateState") != "DEMONSTRATED":
        return "blocked-undemonstrated-gate"
    return "publishable"


def _project_id_valid(value: object, namespace: dict) -> bool:
    pattern = namespace.get("projectId", {}).get("canonicalTextPattern", "")
    return isinstance(value, str) and bool(pattern) and re.fullmatch(pattern, value) is not None


def _object_id_valid(value: object, namespace: dict) -> bool:
    pattern = namespace.get("objectId", {}).get("wirePattern", "")
    return isinstance(value, str) and bool(pattern) and re.fullmatch(pattern, value) is not None


def _object_relative_path(project_id: str, object_id: str) -> str:
    return f"projects/{project_id}/objects/sha256/{object_id.split(':', 1)[1]}"


def _ledger_relative_path(project_id: str) -> str:
    return f"projects/{project_id}/ledger.sqlite"


def validate_storage_fixture(fixture: dict, namespace: dict) -> list[str]:
    """Return exact SN-* violations without treating path inequality as file identity."""
    violations: list[str] = []
    fixture_class = fixture.get("fixtureClass")
    if "projectId" in fixture and not _project_id_valid(fixture["projectId"], namespace):
        violations.append("SN-01")
    if "objectId" in fixture and not _object_id_valid(fixture["objectId"], namespace):
        violations.append("SN-02")
    if fixture.get("pathComponentState") == "symlink-or-reparse-point":
        violations.append("SN-03")
    if fixture.get("migrationTransfer") in {"hardlink", "reflink", "clone-file"}:
        violations.append("SN-04")

    if fixture_class == "lexical-object-path":
        required = {"id", "fixtureClass", "valid", "projectA", "projectB", "objectId",
                    "expectedPathA", "expectedPathB", "expectPathAlias", "claimBoundary"}
        if set(fixture) != required:
            violations.append("SN-05")
        elif not _project_id_valid(fixture["projectA"], namespace) or \
                not _project_id_valid(fixture["projectB"], namespace) or \
                not _object_id_valid(fixture["objectId"], namespace):
            violations.append("SN-05")
        else:
            path_a = _object_relative_path(fixture["projectA"], fixture["objectId"])
            path_b = _object_relative_path(fixture["projectB"], fixture["objectId"])
            if fixture["expectedPathA"] != path_a or fixture["expectedPathB"] != path_b or \
                    fixture["expectPathAlias"] != (path_a == path_b) or \
                    fixture["claimBoundary"] != "LEXICAL_ONLY":
                violations.append("SN-05")
    elif fixture_class == "lexical-ledger-path":
        required = {"id", "fixtureClass", "valid", "projectA", "projectB",
                    "expectedLedgerA", "expectedLedgerB", "expectPathAlias", "claimBoundary"}
        if set(fixture) != required:
            violations.append("SN-06")
        else:
            path_a = _ledger_relative_path(fixture["projectA"])
            path_b = _ledger_relative_path(fixture["projectB"])
            if fixture["expectedLedgerA"] != path_a or fixture["expectedLedgerB"] != path_b or \
                    fixture["expectPathAlias"] != (path_a == path_b) or \
                    fixture["claimBoundary"] != "LEXICAL_ONLY":
                violations.append("SN-06")
    elif fixture_class == "implementation-conformance-declaration":
        required = {"id", "fixtureClass", "valid", "scenario", "requiredObservationIds",
                    "claimState", "demonstrationEvidenceIds", "expectedQualification"}
        physical = namespace.get("physicalIsolationConformance", {})
        if set(fixture) != required or fixture.get("requiredObservationIds") != \
                physical.get("requiredObservationIds") or \
                fixture.get("claimState") != "IMPLEMENTABLE_UNEXECUTED" or \
                fixture.get("demonstrationEvidenceIds") != [] or \
                fixture.get("expectedQualification") != "BLOCKED_UNTIL_COMPLETE_RETAINED_EVIDENCE":
            violations.append("SN-07")
    elif fixture_class != "negative":
        violations.append("SN-07")
    return sorted(set(violations))


def _validate_recovery_vectors(protocol: dict, expected_fixture_ids: set[str],
                               prefix: str) -> list[str]:
    findings: list[str] = []
    table = protocol.get("crashRecoveryTable", [])
    mapping: dict[str, tuple[str, str]] = {}
    for row in table:
        if not isinstance(row, dict) or set(row) != {"observed", "action", "nextState"}:
            findings.append(f"T13 {prefix}: recovery table row is not exact")
            continue
        observed = row["observed"]
        if observed in mapping:
            findings.append(f"T13 {prefix}: duplicate recovery observation {observed}")
        mapping[observed] = (row["action"], row["nextState"])
    fixtures = protocol.get("crashFixtures", [])
    if {fx.get("id") for fx in fixtures} != expected_fixture_ids:
        findings.append(f"T13 {prefix}: crash fixture set is not closed/exact")
    if {fx.get("observed") for fx in fixtures} != set(mapping):
        findings.append(f"T13 {prefix}: crash fixtures do not cover every recovery-table row exactly")
    reachable = set(protocol.get("reachableDurableNonterminalStates", []))
    if reachable:
        covered_states = {observed.split("|", 1)[0] for observed in mapping}
        if covered_states != reachable:
            findings.append(f"T13 {prefix}: recovery rows cover durable states "
                            f"{sorted(covered_states)}, expected {sorted(reachable)}")
    for fx in fixtures:
        if not isinstance(fx, dict) or set(fx) != {
                "id", "observed", "expectedAction", "expectedNextState"}:
            findings.append(f"T13 {prefix} {fx.get('id')}: fixture shape is not exact")
            continue
        expected = mapping.get(fx["observed"])
        if expected != (fx["expectedAction"], fx["expectedNextState"]):
            findings.append(f"T13 {prefix} {fx['id']}: recovery action/state does not match table")
    return findings

def _check(model: dict, operability: dict | None, c2: dict | None = None,
           resolved_inputs: dict | None = None) -> list[str]:
    findings: list[str] = []

    # T5.
    if model.get("status") == "SEALED":
        findings.append("T5: checker cannot self-seal the threat model")
    if "INDEPENDENTLY REVIEWED" not in model.get("reviewStatus", ""):
        findings.append("T5: final-round independent review is not recorded")
    if not model.get("primaryRisks"):
        findings.append("T2: no primary risks declared")

    schema = model.get("modelSchema", {})
    finding_schema = schema.get("Finding", {})
    property_schema = schema.get("RequiredProperty", {})
    severity_values = set(finding_schema.get("severity", {}).get("values", []))
    required_finding = set(finding_schema.get("required", []))
    required_property = set(property_schema.get("required", []))
    if severity_values != {"critical", "high", "medium", "low"}:
        findings.append("T3: Finding severity vocabulary is not closed/exact")
    if required_property != {"id", "property", "verifies", "gateIds", "expectedSubject"}:
        findings.append("T9: RequiredProperty schema does not bind exact gate IDs and subject")

    asset_ids = {a["id"] for a in model.get("assets", [])}
    finding_ids: set[str] = set()
    affected: set[str] = set()
    for item in model.get("findings", []):
        fid = item.get("id", "<missing>")
        if fid in finding_ids:
            findings.append(f"T3 {fid}: duplicate finding id")
        finding_ids.add(fid)
        missing = required_finding - set(item)
        if missing:
            findings.append(f"T3 {fid}: missing required fields {sorted(missing)}")
        if item.get("severity") not in severity_values:
            findings.append(f"T3 {fid}: severity '{item.get('severity')}' is outside schema")
        # The schema called itself closed but only ever checked for MISSING keys,
        # so undeclared ones accumulated silently (V9.severityChangeFromV1, and a
        # tier-level isDefault leaked onto V10). Five other contracts consume this
        # shape; a key they cannot see is drift.
        if finding_schema.get("closedKeys"):
            declared = (set(finding_schema.get("required", []))
                        | set(finding_schema.get("oneOf", []))
                        | set(finding_schema.get("optional", [])))
            undeclared = set(item) - declared
            if undeclared:
                findings.append(f"T3 {fid}: undeclared keys {sorted(undeclared)} "
                                f"outside the closed Finding schema")
        has_mitigation = bool(item.get("requiredMitigations"))
        has_resolution = bool(item.get("requiredResolution"))
        if has_mitigation == has_resolution:
            findings.append(f"T3 {fid}: requires exactly one of mitigation or resolution")
        if has_resolution:
            if not item.get("kind") or not item.get("whyNoMitigation"):
                findings.append(f"T3 {fid}: unresolved contradiction lacks kind/rationale")
        refs = item.get("affects", [])
        if not refs:
            findings.append(f"T7 {fid}: no affected assets")
        for ref in refs:
            if ref not in asset_ids:
                findings.append(f"T7 {fid}: unknown asset {ref}")
        affected.update(refs)
        if not item.get("cause"):
            findings.append(f"T7 {fid}: no cause")
    for asset in model.get("assets", []):
        if asset["id"] not in affected:
            findings.append(f"T6 {asset['id']}: asset is uncovered")

    # T8/T9 and live operability join.
    properties = model.get("requiredProperties", [])
    property_ids = {p.get("id") for p in properties}
    if len(property_ids) != len(properties):
        findings.append("T8: duplicate required property id")
    op_gates = {g["id"]: g for g in operability.get("validationGates", [])} \
        if operability else {}
    op_props = {p["id"]: p for p in operability.get("requiredPropertyRegistry", {})
                .get("properties", [])} if operability else {}
    if operability is None:
        findings.append("T9: operability.v2.json unavailable")
    for prop in properties:
        pid = prop.get("id", "<missing>")
        missing = required_property - set(prop)
        if missing:
            findings.append(f"T9 {pid}: missing required fields {sorted(missing)}")
        if prop.get("expectedSubject") != "product":
            findings.append(f"T9 {pid}: expectedSubject is not product")
        if "gate" in prop:
            findings.append(f"T9 {pid}: legacy category gate remains")
        if not prop.get("verifies"):
            findings.append(f"T8 {pid}: property verifies nothing")
        for ref in prop.get("verifies", []):
            if ref not in finding_ids and not ref.startswith("U"):
                findings.append(f"T8 {pid}: unknown finding {ref}")
        gate_ids = prop.get("gateIds", [])
        if not gate_ids:
            findings.append(f"T9 {pid}: no exact gate IDs")
        for gate_id in gate_ids:
            gate = op_gates.get(gate_id)
            if gate is None:
                findings.append(f"T9 {pid}: unknown operability gate {gate_id}")
            elif gate.get("class") != "implementation-conformance" or \
                    gate.get("subject") != "product":
                findings.append(f"T9 {pid}: gate {gate_id} has wrong subject/class")
        registry = op_props.get(f"TM.{pid}")
        if registry is None or registry.get("gateIds") != gate_ids:
            findings.append(f"T9 {pid}: threat/operability mapping drift")

        text = prop.get("property", "")
        absolute = re.search(r"\b(zero|never|always|nothing|no )\b", text, re.I)
        if absolute and not (prop.get("limits") or prop.get("exception")):
            if not prop.get("absolute"):
                findings.append(f"T11 {pid}: undeclared absolute '{absolute.group(0).strip()}'")
            elif not prop.get("absoluteRationale"):
                findings.append(f"T11 {pid}: absolute lacks rationale")

    # T10 — actual state is computed, not prose.
    demonstrated = {gid for gid, gate in op_gates.items()
                    if gate.get("status") == "DEMONSTRATED"
                    and gate.get("releaseEvidenceIds")}
    blocked_properties = sorted(
        p["id"] for p in properties
        if not p.get("gateIds") or not all(g in demonstrated for g in p["gateIds"])
    )
    current = model.get("shipGate", {}).get("currentState", {})
    if not current.get("derived") or sorted(current.get("demonstratedGateIds", [])) != \
            sorted(demonstrated) or sorted(current.get("blockedPropertyIds", [])) != \
            blocked_properties:
        findings.append("T10: shipGate.currentState is not derived from live gate evidence")
    want_publication = "BLOCKED" if blocked_properties else "PUBLISHABLE"
    if current.get("publicationState") != want_publication:
        findings.append("T10: publicationState contradicts the mapped gates")
    if "DEMONSTRATED" not in json.dumps(model.get("shipGate", {})):
        findings.append("T10: publication gate does not require DEMONSTRATED product evidence")
    decisions = set(schema.get("PublicationDecision", {}).get("values", []))
    for fixture in model.get("shipGateFixtures", []):
        got = publication(fixture)
        if fixture.get("expect") not in decisions:
            findings.append(f"T10 {fixture['id']}: unknown decision {fixture.get('expect')}")
        elif fixture["valid"] and got != fixture.get("expect"):
            findings.append(f"T10 {fixture['id']}: derived {got}, expected {fixture.get('expect')}")
        elif not fixture["valid"] and got == fixture.get("expect"):
            findings.append(f"T10 {fixture['id']}: expected rejection")
    for needed in {"publishable", "blocked-undemonstrated-gate",
                   "blocked-weak-boundary-language"}:
        if not any(x["valid"] and x["expect"] == needed
                   for x in model.get("shipGateFixtures", [])):
            findings.append(f"T10: no positive fixture for {needed}")

    # T12 — focused adjudicated defects.
    #
    # R2-TM-02 was a greenwash: V10 marked solved by assertion. The original
    # guard hard-pinned V10 to UNRESOLVED, which stopped the greenwash but also
    # made a GENUINE resolution unrepresentable. The guard is now evidence-gated
    # instead: V10 may leave UNRESOLVED only against a binding disposition that
    # discharges every requiredResolution item and names what it did not solve.
    # A bare status flip still fails — by a stricter check than before.
    v10 = next((x for x in model.get("findings", []) if x.get("id") == "V10"), {})
    v10_text = " ".join(str(v10.get(k, "")) for k in ("title", "detail", "kind", "status"))
    residual_text = " ".join(model.get("residualRisks", []))
    v10_status = v10.get("status")

    if v10_status == "UNRESOLVED":
        if v10.get("kind") != "UNRESOLVED-CONTRADICTION":
            findings.append("T12 V10: conflict is not consistently unresolved")
        if "proposedResolution" in v10 or re.search(r"resolved by|resolution is now known|both hold", v10_text, re.I):
            findings.append("T12 V10: rejected/candidate resolution is promoted as solved")
        if "V10 remains unresolved" not in residual_text:
            findings.append("T12 V10: unresolved status absent from residual risks")

    elif v10_status == "RESOLVED":
        res = v10.get("resolution") or {}
        if v10.get("kind") != "RESOLVED-BY-DISPOSITION":
            findings.append("T12 V10: RESOLVED without kind RESOLVED-BY-DISPOSITION")
        art = res.get("dispositionArtifact")
        if not art:
            findings.append("T12 V10: RESOLVED with no binding disposition artifact")
        else:
            path = ROOT / "artifacts" / pathlib.Path(art).name
            if not path.exists():
                findings.append(f"T12 V10: disposition artifact {art} does not resolve")
            else:
                disp = json.loads(path.read_text())
                if disp.get("claimId") != "ARCH.RETENTION-TIERS":
                    findings.append("T12 V10: disposition does not bind ARCH.RETENTION-TIERS")
                if not disp.get("invariants"):
                    findings.append("T12 V10: disposition declares no invariants")
                if not (disp.get("counterexampleFixtures") or {}).get("fixtures"):
                    findings.append("T12 V10: disposition has no executable counterexamples")
                if not disp.get("retainedResiduals"):
                    findings.append("T12 V10: disposition names no retained residual")
        required = v10.get("requiredResolution", [])
        discharges = res.get("discharges") or []
        if len(discharges) != len(required):
            findings.append(f"T12 V10: {len(discharges)} discharges for "
                            f"{len(required)} requiredResolution items")
        for i, d in enumerate(discharges):
            if not isinstance(d, dict) or not d.get("by") or not d.get("status"):
                findings.append(f"T12 V10: discharge {i} lacks a cited source or status")
        if "V10 resolved by disposition" not in residual_text:
            findings.append("T12 V10: resolution not recorded in residual risks")
        if not res.get("retainedResiduals"):
            findings.append("T12 V10: resolution claims no retained residual — "
                            "measurement cannot vanish with the contradiction")

    else:
        findings.append(f"T12 V10: status {v10_status!r} is neither UNRESOLVED nor RESOLVED")

    deletion = model.get("deletionProtocol", {})
    for phrase, key in (("Cross-project physical deduplication is forbidden", "ownership"),
                        ("startup resumes", "protocol"),
                        ("Verify no live", "protocol"),
                        ("does not promise forensic erasure", "meaningOfDelete")):
        value = deletion.get(key, "")
        value = " ".join(value) if isinstance(value, list) else value
        if phrase not in value:
            findings.append(f"T12 deletion: missing '{phrase}'")
    if len(deletion.get("fixturesRequired", [])) < 6:
        findings.append("T12 deletion: shared/crash verification fixtures incomplete")

    # T13 — canonical paths, real-file qualification, and crash-safe
    # namespace lifecycle are separate proof obligations.
    namespace = model.get("storageNamespace", {})
    if namespace.get("schemaVersion") != 1:
        findings.append("T13: storage namespace schemaVersion is not 1")
    expected_project_pattern = r"^prj1-[0-9a-f]{64}$"
    expected_object_pattern = r"^sha256:[0-9a-f]{64}$"
    project_spec = namespace.get("projectId", {})
    if project_spec.get("canonicalTextPattern") != expected_project_pattern:
        findings.append("T13 SN-01: ProjectId encoding is not exact/path-safe")
    owner = project_spec.get("logicalIdentityOwner", "")
    if "PROJECT-ID-V1" not in owner or \
            "resolved-inputs.v2.json#projectIdContract" not in owner:
        findings.append("T13 SN-01: storage does not name the exact PROJECT-ID-V1 identity owner")
    if "projectIdContract" not in project_spec.get("admissionJoin", "") or \
            "planIntent.wireTypes.projectId" not in project_spec.get("admissionJoin", ""):
        findings.append("T13 SN-01: ProjectId admission join is partial")
    if namespace.get("objectId", {}).get("wirePattern") != expected_object_pattern:
        findings.append("T13 SN-02: object digest encoding is not exact/path-safe")
    if c2 is None:
        findings.append("T13: C-2 unavailable; pre-admission ProjectId encoding join unverified")
    elif c2.get("planIntent", {}).get("wireTypes", {}).get("projectId", {}).get(
            "pattern") != expected_project_pattern:
        findings.append("T13: C-2 PlanIntent ProjectId encoding differs from storage namespace")
    if resolved_inputs is None:
        findings.append("T13: resolved-inputs unavailable; PROJECT-ID-V1 ownership unverified")
    else:
        project_contract = resolved_inputs.get("projectIdContract", {})
        if project_contract.get("id") != "PROJECT-ID-V1" or \
                project_contract.get("representation", {}).get("regex") != expected_project_pattern:
            findings.append("T13: live resolved-inputs PROJECT-ID-V1 differs from storage consumer")

    expected_layout = {
        "rootMarker": "<admittedStorageRoot>/storage-root.v1.json",
        "projectNamespace": "<admittedStorageRoot>/projects/<ProjectId>",
        "ledger": "<admittedStorageRoot>/projects/<ProjectId>/ledger.sqlite",
        "ledgerWal": "<admittedStorageRoot>/projects/<ProjectId>/ledger.sqlite-wal",
        "ledgerShm": "<admittedStorageRoot>/projects/<ProjectId>/ledger.sqlite-shm",
        "casObject": "<admittedStorageRoot>/projects/<ProjectId>/objects/sha256/<digestHex>",
        "cache": "<admittedStorageRoot>/projects/<ProjectId>/cache",
        "privateEphemeral": "<admittedStorageRoot>/projects/<ProjectId>/ephemeral",
        "rootControl": "<admittedStorageRoot>/control",
        "purgeJournal": "<admittedStorageRoot>/control/purge/<ProjectId>/<purgeId>.v1.json",
        "purgeQuarantine": "<admittedStorageRoot>/quarantine/purge/<ProjectId>/<purgeId>/namespace",
        "migrationStaging": "<targetStorageRoot>/quarantine/migrate/<ProjectId>/<migrationId>/namespace",
        "migrationRetirement": "<sourceStorageRoot>/quarantine/migrate-retired/<ProjectId>/<migrationId>/namespace",
    }
    layout = namespace.get("layout", {})
    for key, expected in expected_layout.items():
        if layout.get(key) != expected:
            findings.append(f"T13: layout.{key} must be {expected!r}")
    layout_rule = layout.get("rule", "")
    for term in ("There is no root-level ledger.sqlite", "control/ never stores source",
                 "quarantine"):
        if term not in layout_rule:
            findings.append(f"T13: layout rule omits {term!r}")
    root = namespace.get("admittedStorageRoot", {})
    root_marker = root.get("rootMarker", {})
    if root_marker.get("exactFields") != ["schemaVersion", "rootId"] or \
            root_marker.get("rootIdPattern") != r"^root1-[0-9a-f]{32}$":
        findings.append("T13: storage-root identity/shape is not exact")
    if not all(term in root.get("rootContents", "")
               for term in ("projects/", "control/", "quarantine/", "metadata only")):
        findings.append("T13: admitted-root contents/custody are not exact")

    purpose = namespace.get("purpose", "")
    object_spec = namespace.get("objectId", {})
    if "lexically project-exclusive" not in purpose or \
            "IMPLEMENTABLE_UNEXECUTED" not in purpose:
        findings.append("T13: lexical and physical assurance boundaries are conflated")
    if "lexical guarantee only" not in object_spec.get("lexicalNamespaceRule", "") or \
            not all(term in object_spec.get("physicalImplementationRule", "")
                    for term in ("independent regular files", "hardlinks", "reflinks",
                                 "clone-file", "shared lower CAS", "not demonstrated")):
        findings.append("T13: lexical path and normative physical rules are incomplete")
    tenancy = namespace.get("ledgerTenancy", {}).get("rule", "")
    if "Exactly one SQLite ledger per projectNamespace" not in tenancy or \
            "No SQLite database or table spans ProjectIds" not in tenancy:
        findings.append("T13: ledger tenancy is not per ProjectId")

    physical = namespace.get("physicalIsolationConformance", {})
    required_observations = {
        "PI-REGULAR-FILE", "PI-DISTINCT-FILE-IDENTITY", "PI-LINK-COUNT-ONE",
        "PI-NO-LINK-OR-CLONE-PRIMITIVE", "PI-SUPPORTED-FILESYSTEM-MATRIX",
    }
    if physical.get("state") != "SPECIFIED" or \
            physical.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            physical.get("gateIds") != ["G14"] or \
            physical.get("demonstrationEvidenceIds") != []:
        findings.append("T13: unbuilt physical isolation must remain SPECIFIED/IMPLEMENTABLE_UNEXECUTED with no evidence")
    if set(physical.get("requiredObservationIds", [])) != required_observations or \
            {item.get("id") for item in physical.get("observations", [])} != required_observations:
        findings.append("T13: physical isolation observations are incomplete")
    evidence_blob = json.dumps(physical.get("observations", []))
    for term in ("regular files", "(st_dev,st_ino)", "link count exactly one",
                 "syscall/API tracing", "platform/filesystem/operation"):
        if term not in evidence_blob:
            findings.append(f"T13: physical isolation evidence recipe omits {term}")
    qualification_fields = {
        "evidenceId", "productBuildId", "platform", "filesystem", "mountFeatures",
        "operation", "projectA", "projectB", "objectId", "fileKindA", "fileKindB",
        "fileIdentityA", "fileIdentityB", "linkCountA", "linkCountB",
        "transferTrace", "result",
    }
    if set(physical.get("qualificationRecordRequired", [])) != qualification_fields or \
            set(physical.get("requiredOperations", [])) != {
                "publish-new", "reuse-existing", "purge-quarantine",
                "migration-stage", "crash-recovery"}:
        findings.append("T13: supported-filesystem qualification record/operation matrix is not exact")
    if "Fixture declarations" not in physical.get("paperSealRule", ""):
        findings.append("T13: checker fixtures could be mistaken for physical product evidence")

    fixture_ids = {fx.get("id") for fx in namespace.get("fixtures", [])}
    required_namespace_fixtures = {
        "equal-digest-different-projects-have-distinct-paths",
        "equal-digest-same-project-deduplicates-path",
        "different-project-ledgers-have-distinct-paths",
        "physical-non-alias-qualification-declaration",
        "reject-project-traversal", "reject-uppercase-project-id",
        "reject-object-traversal", "reject-symlink-project-component",
        "reject-cross-project-hardlink-migration",
    }
    if fixture_ids != required_namespace_fixtures:
        findings.append("T13: namespace fixture set is not closed/exact")
    for fixture in namespace.get("fixtures", []):
        violations = validate_storage_fixture(fixture, namespace)
        if fixture.get("valid") and violations:
            findings.append(f"T13 {fixture.get('id')}: expected valid, got {violations}")
        elif not fixture.get("valid"):
            expected = fixture.get("violates")
            if not violations:
                findings.append(f"T13 {fixture.get('id')}: expected rejection by {expected}")
            elif expected not in violations:
                findings.append(f"T13 {fixture.get('id')}: expected {expected}, got {violations}")

    lifecycle = namespace.get("inventoryPurgeMigration", {})
    inventory = lifecycle.get("inventory", {})
    if not all(term in json.dumps(inventory)
               for term in ("control/purge", "quarantine", "migration journals",
                            "never reported as authoritative")):
        findings.append("T13: inventory cannot enumerate/reconcile incomplete purge and migration state")

    purge = lifecycle.get("purge", {})
    if not isinstance(purge, dict):
        findings.append("T13 purge: protocol is not an object")
        purge = {}
    if purge.get("purgeIdPattern") != r"^purge1-[0-9a-f]{32}$" or \
            purge.get("journalPath") != expected_layout["purgeJournal"] or \
            purge.get("quarantinePath") != expected_layout["purgeQuarantine"]:
        findings.append("T13 purge: identifiers/journal/quarantine paths are not exact")
    if set(purge.get("journalExactFields", [])) != {
            "schemaVersion", "purgeId", "projectId", "state", "transitionCounter",
            "namespaceInventoryCommitment", "quarantineRelativePath"} or \
            set(purge.get("movingMarkerExactFields", [])) != {
                "schemaVersion", "purgeId", "projectId", "namespaceInventoryCommitment"}:
        findings.append("T13 purge: journal/moving-marker shapes are not exact")
    if purge.get("states") != [
            "PREPARED", "QUARANTINED", "DELETE_IN_PROGRESS",
            "VERIFIED_ABSENT", "COMPLETE"]:
        findings.append("T13 purge: state machine is not closed/exact")
    if set(purge.get("reachableDurableNonterminalStates", [])) != {
            "PREPARED", "QUARANTINED", "DELETE_IN_PROGRESS", "VERIFIED_ABSENT"}:
        findings.append("T13 purge: reachable durable nonterminal state set is not exact")
    purge_ops = " ".join(purge.get("operationOrdering", []))
    for term in ("PREPARED root-control journal", "atomically rename",
                 "Persist DELETE_IN_PROGRESS", "deletion commit point",
                 "leaves no project namespace"):
        if term not in purge_ops:
            findings.append(f"T13 purge: operation ordering omits {term}")
    findings.extend(_validate_recovery_vectors(
        purge,
        {"purge-crash-before-rename", "purge-crash-after-rename-before-journal",
         "purge-crash-after-quarantined-before-delete-state",
         "purge-crash-mid-delete", "purge-crash-after-delete-before-verify",
         "purge-crash-after-verify-before-cleanup"},
        "purge"))

    migration = lifecycle.get("migration", {})
    if not isinstance(migration, dict):
        findings.append("T13 migration: protocol is not an object")
        migration = {}
    if migration.get("migrationIdPattern") != r"^migrate1-[0-9a-f]{32}$" or \
            migration.get("authorityRecordPath") != \
            "<userStateRoot>/opensip/storage-authority-v1/<ProjectId>.json" or \
            migration.get("journalPath") != \
            "<userStateRoot>/opensip/storage-operations/migrate/<migrationId>.v1.json":
        findings.append("T13 migration: identifiers/authority/journal paths are not exact")
    if set(migration.get("authorityRecordExactFields", [])) != {
            "schemaVersion", "projectId", "generation", "activeRootId",
            "activeRootCanonicalPath", "pendingMigrationId"} or \
            "Compare-and-swap" not in migration.get("authorityRecordRule", "") or \
            "migration is refused" not in migration.get("authorityRecordRule", ""):
        findings.append("T13 migration: single authority selection/atomicity is not exact")
    if migration.get("states") != [
            "PREPARED", "COPYING", "TARGET_VERIFIED", "TARGET_INSTALLED",
            "AUTHORITY_SWITCHED", "SOURCE_QUARANTINED", "SOURCE_RETIRED",
            "COMPLETE", "ROLLED_BACK"]:
        findings.append("T13 migration: state machine is not closed/exact")
    migration_ops = " ".join(migration.get("operationOrdering", []))
    for term in ("independently copy regular files", "still non-authoritative",
                 "Compare-and-swap", "Only after the authority switch is durable",
                 "Before AUTHORITY_SWITCHED", "After the switch"):
        if term not in migration_ops:
            findings.append(f"T13 migration: operation ordering omits {term}")
    rollback = migration.get("rollback", {})
    if set(rollback.get("allowedStates", [])) != {
            "PREPARED", "COPYING", "TARGET_VERIFIED", "TARGET_INSTALLED"} or \
            set(rollback.get("forbiddenStates", [])) != {
                "AUTHORITY_SWITCHED", "SOURCE_QUARANTINED",
                "SOURCE_RETIRED", "COMPLETE"} or \
            "CONFLICT" not in rollback.get("staleGenerationResult", ""):
        findings.append("T13 migration: rollback/authority-conflict boundary is not exact")
    findings.extend(_validate_recovery_vectors(
        migration,
        {"migration-crash-prepared", "migration-crash-copying",
         "migration-crash-target-verified", "migration-crash-target-installed",
         "migration-crash-after-authority-cas",
         "migration-crash-before-source-quarantine",
         "migration-crash-after-source-rename",
         "migration-crash-mid-source-delete",
         "migration-crash-after-source-delete",
         "migration-crash-before-journal-cleanup"},
        "migration"))

    assurance = namespace.get("assurance", {})
    if assurance.get("state") != "SPECIFIED" or \
            assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            assurance.get("demonstrationEvidenceIds") != []:
        findings.append("T13: namespace/recovery contract overclaims product evidence")
    r15 = next((x for x in properties if x.get("id") == "R15"), {})
    if not all(term in r15.get("property", "")
               for term in ("lexically distinct", "regular-file identity",
                            "supported filesystem")):
        findings.append("T13 R15: required property conflates path design with physical evidence")

    detector = model.get("storageExposureDetectors", {})
    if set(detector.get("classes", [])) != {
            "cloud-sync-or-ci-upload", "backup-managed", "permission-exposed"}:
        findings.append("T12 storage: sync, backup and permissions are not separated")
    if set(detector.get("closedResults", [])) != {"DETECTED", "NOT-DETECTED", "UNKNOWN"}:
        findings.append("T12 storage: detector result set is not closed")
    v2 = next((x for x in model.get("findings", []) if x.get("id") == "V2"), {})
    if re.search(r"\b(commonly|routinely)\b", json.dumps(v2), re.I):
        findings.append("T12 V2: unmeasured prevalence language remains")

    r11 = next((x for x in properties if x.get("id") == "R11"), {})
    if "resolved-configuration secret channel" not in r11.get("property", ""):
        findings.append("T12 R11: secret absolute is not scoped to the config channel")
    r6 = next((x for x in properties if x.get("id") == "R6"), {})
    if "cleanup guaranteed" in r6.get("property", "").lower():
        findings.append("T12 R6: impossible all-exit cleanup promise remains")
    if not any(x.get("id") == "V19" for x in model.get("findings", [])) or \
            not any(x.get("id") == "R16" for x in properties):
        findings.append("T12 output: active projection injection is absent")
    safety = model.get("projectionSafety", {})
    required_classes = {"terminal-control", "html-script", "unicode", "uri", "volume"}
    if {x.get("payloadClass") for x in safety.get("projectionSafetyFixtures", [])} != \
            required_classes:
        findings.append("T12 output: hostile projection fixture classes are incomplete")

    # T1/T4 — prose claims, still outside JSON self-consistency.
    weak_present = any(x.get("strength") in WEAK for x in model.get("trustBoundaries", []))
    if weak_present:
        for path in sorted((ROOT / "architecture").glob("*.md")):
            text = path.read_text()
            for _, paragraph in paragraphs(text):
                if paragraph.lstrip().startswith("|") or "|---" in paragraph:
                    continue
                if re.search(r"wherever confinement is claimed|confinement honesty", paragraph, re.I):
                    continue
                match = CLAIM.search(paragraph)
                if match and not QUALIFIER.search(paragraph):
                    near = paragraph[max(0, match.start() - 80):match.end() + 80]
                    if re.search(r"\b(is|are|provides?|guarantees?|ensures?)\b", near):
                        findings.append(f"T1 {path.name}: unqualified confinement claim")
    corpus = "\n".join(path.read_text() for path in (ROOT / "architecture").glob("*.md"))
    for item in model.get("nonGoals", []):
        if item.get("id") == "N2" and "exfiltration" not in corpus:
            findings.append("T4 N2: exfiltration limit absent from architecture")
        if item.get("id") == "N3" and "not a security sandbox" not in corpus:
            findings.append("T4 N3: process-boundary limit absent from architecture")
    return findings


def check(model: object, operability: dict | None, c2: dict | None = None,
          resolved_inputs: dict | None = None) -> list[str]:
    """Total threat-model boundary for malformed parsed JSON shapes."""
    if not isinstance(model, dict) or not model:
        return ["TM-TOTALITY-ROOT: model root must be a non-empty object"]
    schema = model.get("modelSchema")
    if not isinstance(schema, dict) or \
            not isinstance(schema.get("Finding"), dict) or \
            not isinstance(schema.get("RequiredProperty"), dict):
        return ["TM-TOTALITY-SHAPE: modelSchema Finding/RequiredProperty must be objects"]
    try:
        return _check(model, operability, c2, resolved_inputs)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"TM-TOTALITY-EXCEPTION: malformed model shape "
                f"({type(exc).__name__})"]


def _invalid_severity(model):
    model["findings"][5]["severity"] = "medium-high"


def _category_gate(model):
    prop = model["requiredProperties"][0]
    prop["gate"] = "primary"
    prop.pop("gateIds")


def _false_publication_state(model):
    model["shipGate"]["currentState"] = {"derived": True, "demonstratedGateIds": ["G3"],
                                                "blockedPropertyIds": [],
                                                "publicationState": "PUBLISHABLE"}


def _solve_v10(model):
    """R2-TM-02 verbatim: resolved by assertion, with no disposition behind it.

    The base now carries a genuine RESOLVED-BY-DISPOSITION state, so this
    mutation strips the disposition to reproduce the original greenwash.
    """
    v10 = next(x for x in model["findings"] if x["id"] == "V10")
    v10["status"] = "RESOLVED"
    v10["kind"] = "UNRESOLVED-CONTRADICTION"
    v10["title"] = "Conflict resolved by proving structure"
    v10.pop("resolution", None)


def _undeclared_finding_key(model):
    """Reintroduce silent key drift on a Finding the closed schema governs."""
    next(x for x in model["findings"] if x["id"] == "V9")["isDefault"] = False


def _set_v10_resolved_shape(model, disposition_artifact="artifacts/retention-tiers.v5.json"):
    """Build the evidence-gated branch from today's UNRESOLVED base.

    These mutations must not assume that the live model already carries a
    resolution object. v5 is used only as a structurally complete historical
    fixture; the live model does not cite it and remains UNRESOLVED.
    """
    v10 = next(x for x in model["findings"] if x["id"] == "V10")
    v10["status"] = "RESOLVED"
    v10["kind"] = "RESOLVED-BY-DISPOSITION"
    v10["resolution"] = {
        "dispositionArtifact": disposition_artifact,
        "discharges": [
            {"by": f"fixture-{index}", "status": "DISCHARGED"}
            for index, _ in enumerate(v10.get("requiredResolution", []), start=1)
        ],
        "retainedResiduals": ["A1-RTV4-02 remains unmeasured"],
    }
    model["residualRisks"] = [
        "V10 resolved by disposition; A1-RTV4-02 remains unmeasured."
        if "V10 remains unresolved" in row else row
        for row in model.get("residualRisks", [])
    ]


def _v10_phantom_disposition(model):
    """Cite a disposition artifact that does not exist."""
    _set_v10_resolved_shape(model, "artifacts/retention-custody.v99.json")


def _v10_partial_discharge(model):
    """Discharge one of three requiredResolution items and call it resolved."""
    _set_v10_resolved_shape(model)
    v10 = next(x for x in model["findings"] if x["id"] == "V10")
    v10["resolution"]["discharges"] = v10["resolution"]["discharges"][:1]


def _v10_residual_vanishes(model):
    """Let the measurement residual disappear along with the contradiction."""
    _set_v10_resolved_shape(model)
    v10 = next(x for x in model["findings"] if x["id"] == "V10")
    v10["resolution"]["retainedResiduals"] = []


def _restore_prevalence(model):
    v2 = next(x for x in model["findings"] if x["id"] == "V2")
    v2["detail"] = "Home cache routinely sits in cloud sync roots."


def _global_secret_absolute(model):
    r11 = next(x for x in model["requiredProperties"] if x["id"] == "R11")
    r11["property"] = "A secret value never reaches any output."


def _drop_output_finding(model):
    model["findings"] = [x for x in model["findings"] if x["id"] != "V19"]


def _restore_cleanup_absolute(model):
    r6 = next(x for x in model["requiredProperties"] if x["id"] == "R6")
    r6["property"] = "No source-derived content in shared temp; cleanup guaranteed on every exit path"


def _drop_deletion_protocol(model):
    del model["deletionProtocol"]


def _wrong_gate_mapping(model):
    next(x for x in model["requiredProperties"] if x["id"] == "R1")["gateIds"] = ["G12"]


def _drop_projection_fixture(model):
    model["projectionSafety"]["projectionSafetyFixtures"] = [
        x for x in model["projectionSafety"]["projectionSafetyFixtures"]
        if x["payloadClass"] != "terminal-control"
    ]


def _shared_cross_project_cas(model):
    model["storageNamespace"]["layout"]["casObject"] = \
        "<admittedStorageRoot>/objects/sha256/<digestHex>"


def _shared_cross_project_ledger(model):
    model["storageNamespace"]["layout"]["ledger"] = \
        "<admittedStorageRoot>/ledger.sqlite"


def _path_normalise_project_id(model):
    model["storageNamespace"]["projectId"]["canonicalTextPattern"] = \
        "^prj1-[0-9A-Fa-f./-]+$"


def _alias_equal_cross_project_digest(model):
    fixture = next(x for x in model["storageNamespace"]["fixtures"]
                   if x["id"] == "equal-digest-different-projects-have-distinct-paths")
    fixture["expectPathAlias"] = True


def _allow_hardlink_migration(model):
    fixture = next(x for x in model["storageNamespace"]["fixtures"]
                   if x["id"] == "reject-cross-project-hardlink-migration")
    fixture["valid"] = True


def _paper_demonstrate_storage(model):
    model["storageNamespace"]["assurance"] = {
        "state": "DEMONSTRATED",
        "evidenceGrade": "DEMONSTRATED",
    }


def _purge_scans_global_cas(model):
    model["storageNamespace"]["inventoryPurgeMigration"]["purge"] = \
        "Scan a global CAS and delete matching digests."


def _drop_physical_file_identity_observation(model):
    physical = model["storageNamespace"]["physicalIsolationConformance"]
    physical["requiredObservationIds"].remove("PI-DISTINCT-FILE-IDENTITY")
    physical["observations"] = [x for x in physical["observations"]
                                if x["id"] != "PI-DISTINCT-FILE-IDENTITY"]


def _fake_physical_demonstration(model):
    physical = model["storageNamespace"]["physicalIsolationConformance"]
    physical["state"] = "DEMONSTRATED"
    physical["evidenceGrade"] = "DEMONSTRATED"
    physical["demonstrationEvidenceIds"] = ["fixture-not-product-evidence"]


def _ambiguous_purge_recovery(model):
    fixture = model["storageNamespace"]["inventoryPurgeMigration"]["purge"]["crashFixtures"][1]
    fixture["expectedAction"] = "recreate-empty-project"


def _drop_quarantined_durable_recovery(model):
    purge = model["storageNamespace"]["inventoryPurgeMigration"]["purge"]
    purge["crashRecoveryTable"] = [
        row for row in purge["crashRecoveryTable"]
        if not row["observed"].startswith("QUARANTINED|")]
    purge["crashFixtures"] = [
        fx for fx in purge["crashFixtures"]
        if fx["id"] != "purge-crash-after-quarantined-before-delete-state"]


def _authority_record_inside_source_root(model):
    migration = model["storageNamespace"]["inventoryPurgeMigration"]["migration"]
    migration["authorityRecordPath"] = \
        "<sourceStorageRoot>/control/storage-authority/<ProjectId>.json"


def _permit_rollback_after_authority_switch(model):
    rollback = model["storageNamespace"]["inventoryPurgeMigration"]["migration"]["rollback"]
    rollback["forbiddenStates"].remove("AUTHORITY_SWITCHED")
    rollback["allowedStates"].append("AUTHORITY_SWITCHED")


def _detach_project_id_owner(model):
    model["storageNamespace"]["projectId"]["logicalIdentityOwner"] = \
        "Storage derives ProjectId from the canonical root path."


MUTATIONS = [
    ("accept an instance outside Finding severity enum (R2-TM-01)", _invalid_severity),
    ("restore category gates instead of exact IDs (R2-TM-01/04)", _category_gate),
    ("editorially claim all properties publishable (R2-TM-04)", _false_publication_state),
    ("mark V10 solved again (R2-TM-02)", _solve_v10),
    ("reintroduce undeclared key drift on a Finding (T3 closure)", _undeclared_finding_key),
    ("resolve V10 against a phantom disposition", _v10_phantom_disposition),
    ("resolve V10 discharging 1 of 3 required items", _v10_partial_discharge),
    ("let the measurement residual vanish with V10", _v10_residual_vanishes),
    ("restore unmeasured V2 prevalence (R2-TM-03)", _restore_prevalence),
    ("widen config-secret absolute to arbitrary text (R2-TM-06)", _global_secret_absolute),
    ("delete active output injection (R2-TM-07)", _drop_output_finding),
    ("restore impossible all-exit cleanup (R2-TM-08)", _restore_cleanup_absolute),
    ("delete CAS-safe deletion protocol (R1/R2-TM-01/05)", _drop_deletion_protocol),
    ("map a threat property to a design-only gate (R2-TM-04)", _wrong_gate_mapping),
    ("drop ANSI/OSC negative control (R2-TM-07)", _drop_projection_fixture),
    ("remove ProjectId from the physical CAS path (IP-R4-06)", _shared_cross_project_cas),
    ("share one ledger across ProjectIds (IP-R4-06)", _shared_cross_project_ledger),
    ("normalise unsafe ProjectId spellings into a namespace", _path_normalise_project_id),
    ("alias equal object digests across projects", _alias_equal_cross_project_digest),
    ("permit cross-project hardlink migration", _allow_hardlink_migration),
    ("paper-demonstrate an unbuilt storage engine", _paper_demonstrate_storage),
    ("purge through a global cross-project CAS", _purge_scans_global_cas),
    ("omit stable file identity from physical qualification", _drop_physical_file_identity_observation),
    ("promote fixture declarations to physical product evidence", _fake_physical_demonstration),
    ("make rename-gap purge recovery choose a different action", _ambiguous_purge_recovery),
    ("drop durable QUARANTINED purge recovery branch", _drop_quarantined_durable_recovery),
    ("put cross-root authority selection inside the source root", _authority_record_inside_source_root),
    ("permit automatic rollback after authority switch", _permit_rollback_after_authority_switch),
    ("let storage mint ProjectId instead of consuming PROJECT-ID-V1", _detach_project_id_owner),
]


def selftest(model: dict, operability: dict | None, c2: dict | None,
             resolved_inputs: dict | None) -> int:
    pre = check(model, operability, c2, resolved_inputs)
    if pre:
        print(f"REFUSING to self-test: base model has {len(pre)} finding(s)")
        for item in pre[:8]:
            print("  -", item)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, root in TOTALITY_ROOT_CASES:
        found = check(copy.deepcopy(root), operability, c2, resolved_inputs)
        if not found:
            escaped += 1
        print(f"  {'reject' if found else 'ESCAPE':>6}  parsed-JSON root {name}")
        print(f"          {found[0] if found else 'NO FINDING — root survived'}")
    for name, value in TOTALITY_NESTED_CASES:
        candidate = copy.deepcopy(model)
        candidate["modelSchema"] = copy.deepcopy(value)
        found = check(candidate, operability, c2, resolved_inputs)
        if not found:
            escaped += 1
        print(f"  {'reject' if found else 'ESCAPE':>6}  modelSchema nested {name}")
        print(f"          {found[0] if found else 'NO FINDING — nested shape survived'}")
    for name, mutation in MUTATIONS:
        candidate = copy.deepcopy(model)
        mutation(candidate)
        found = check(candidate, operability, c2, resolved_inputs)
        if not found:
            escaped += 1
        print(f"  {'reject' if found else 'ESCAPE':>6}  {name}")
        print(f"          {found[0] if found else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        total = len(MUTATIONS) + len(TOTALITY_ROOT_CASES) + len(TOTALITY_NESTED_CASES)
        print(f"{escaped}/{total} retained cases ESCAPED")
        return 1
    print(f"all {len(MUTATIONS)} semantic mutations, {len(TOTALITY_ROOT_CASES)} root-shape "
          f"cases and {len(TOTALITY_NESTED_CASES)} nested-shape cases rejected — "
          "adjudicated defects are load-bearing")
    return 0


def main() -> int:
    if not MODEL.exists():
        print(f"missing model: {MODEL}", file=sys.stderr)
        return 2
    model = json.loads(MODEL.read_text())
    operability = json.loads(OPERABILITY.read_text()) if OPERABILITY.exists() else None
    c2 = json.loads(C2.read_text()) if C2.exists() else None
    resolved_inputs = json.loads(RESOLVED_INPUTS.read_text()) if RESOLVED_INPUTS.exists() else None
    if "--selftest" in sys.argv:
        return selftest(model, operability, c2, resolved_inputs)
    found = check(model, operability, c2, resolved_inputs)
    if found:
        print(f"{len(found)} finding(s):")
        for item in found:
            print("  -", item)
        return 1
    current = model["shipGate"]["currentState"]
    print(f"threat model v{model['version']} OK — {len(model['assets'])} user assets, "
          f"{len(model['primaryRisks'])} primary risks, {len(model['findings'])} findings, "
          f"{len(model['requiredProperties'])} required properties, T1..T13 clean")
    # derived, not asserted — a hardcoded status word is how a banner outlives
    # the fact it describes
    v10 = next((x for x in model["findings"] if x["id"] == "V10"), {})
    v10_line = f"V10 {v10.get('status', '?')}"
    if v10.get("status") == "RESOLVED":
        res = v10.get("resolution", {})
        v10_line += (f" by {pathlib.Path(res.get('dispositionArtifact', '?')).name}"
                     f", {len(res.get('retainedResiduals', []))} residual(s) retained")
    print(f"  publication: {current['publicationState']} — "
          f"{len(current['blockedPropertyIds'])} properties undemonstrated; {v10_line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
