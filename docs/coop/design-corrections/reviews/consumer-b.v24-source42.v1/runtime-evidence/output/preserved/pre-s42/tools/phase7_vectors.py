"""Phase 7 observables (classification valid|invalid|explanatory; negatives carry firstRefusal/masksLater):

  vectors/multi-unit-missing-caps.json       R-MULTI-UNIT-MISSING-CAPS, R-CANDIDATE-ONLY-CLONES, R-PROMISE-VS-AVAILABILITY
  envelopes/invocation-disclosure.json       R-INVOCATION-DISCLOSURE
  envelopes/single-step.json                 R-SINGLE-STEP
  envelopes/multi-step.json                  R-MULTI-STEP-DIFFERENT-SELECTIONS
  envelopes/public-from-internal.json        R-PUBLIC-FROM-INTERNAL-REFUSAL
  envelopes/config-input.json                R-ENVELOPE-CONFIG-INPUT
  envelopes/retained-external-input.json     R-ENVELOPE-EXTERNAL-INPUT
  envelopes/host-invalid-internal.json       R-ENVELOPE-HOST-INVALID
  envelopes/producer-boundary.json           R-ENVELOPE-PRODUCER-BOUNDARY   (all four: R-FAILURE-ENVELOPES-D9)
  vectors/d9-extension-precedence.json       R-D9-EXTENSION-PRECEDENCE
  envelopes/receipt-availability.json        R-DURABLE-RECEIPT-AVAILABILITY
  vectors/authority-and-steps.json           R-SEMANTIC-VS-OPERATIONAL-AUTHORITY, R-MUTATION-VS-ANALYSIS-STEPS
  vectors/chain-zero-config.json             R-CHAIN-ZERO-CONFIG-TO-RECEIPT
Usage: python3 tools/runref.py tools/phase7_vectors.py
"""
import copy
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v1/output/preserved/pre-s42"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/tools")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import enumeration as EN  # noqa: E402
import membership as M  # noqa: E402
import native_facts as NF  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
NE = "native/native-evidence.schemas.v2.json"
COMMON3 = "workflows/schemas/evaluator3/common.schema.json"
ENV3 = "workflows/schemas/evaluator3/command-envelope.schema.json"
INVOC3 = "workflows/schemas/evaluator3/invocation-record.schema.json"
REPAIR3 = "workflows/schemas/evaluator3/repair.schema.json"
REG = KIT.doc(NE)["x-opensip-public-route-registry"]
INVENTORY = {c["name"]: c for c in KIT.doc("workflows/command-inventory.v3.json")["commands"]}
EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}
MATRIX_IDS = [c["id"] for c in EN.MATRIX["capabilities"]]
failures = []


def cell_state(cap, mode):
    """Matrix cell for (capability, mode); an absent cell carries no promise and is treated as NOT-SELECTED."""
    row = next((c for c in EN.MATRIX["cells"] if c["capability"] == cap and c["mode"] == mode), None)
    return row if row is not None else {"capability": cap, "mode": mode, "state": "NOT-SELECTED", "deficiency": None, "absentCell": True}


def dump(rel, obj):
    os.makedirs(os.path.dirname(f"{OUT}/{rel}"), exist_ok=True)
    with open(f"{OUT}/{rel}", "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)


def must(name, cond, detail=None):
    if not cond:
        failures.append({"vector": name, "detail": detail})
    return bool(cond)


def admit(value, doc, sel):
    r = KIT.admit(value, doc, sel)
    return r["ok"], (None if r["ok"] else [r["typed"]] + [f"{x['path']}:{x['message'][:120]}" for x in r["stock"][:3]] + [str(x)[:200] for x in r["order"][:3]])


def req_id(n):
    return "req1_" + hashlib.sha256(f"cb24-request-{n}".encode()).hexdigest()[:32]


def exec_id(n):
    return "exec1_" + hashlib.sha256(f"cb24-execution-{n}".encode()).hexdigest()[:32]


# ------------------------------------------------------------------ capability selection (native s1.4)
def admit_release(rows):
    faults = []
    ok, errs = admit(rows, NE, "#/$defs/ReleaseCapabilityRegistryV1")
    if not ok:
        return [f"cb24.RELEASE_SCHEMA:{errs}"]
    seen = set()
    for r in rows:
        if r["capabilityId"].startswith("preview-"):
            faults.append(f"native.release-capability-preview-constant:{r['capabilityId']}")
            continue
        if r["capabilityId"] not in MATRIX_IDS:
            faults.append(f"native.release-capability-unregistered:{r['capabilityId']}")
            continue
        if r["capabilityId"] in seen:
            faults.append(f"native.release-capability-duplicate:{r['capabilityId']}")
        seen.add(r["capabilityId"])
        for m in r["languageModes"]:
            if m not in EN.LANGUAGE_MODES:
                faults.append(f"native.release-capability-mode-unregistered:{r['capabilityId']}:{m}")
            elif cell_state(r["capabilityId"], m)["state"] == "NOT-SELECTED":
                faults.append(f"native.release-capability-mode-not-selected:{r['capabilityId']}:{m}")
    return faults


def default_capability_selection(units):
    rows, faults, seen = [], [], {}
    for u in units:
        mode = u["languageMode"]
        for cap in MATRIX_IDS:
            if cell_state(cap, mode)["state"] == "NOT-SELECTED":
                continue
            row = {"capabilityId": cap, "languageMode": mode, "workspaceRoot": M.spell_root(u["rootPath"]), "required": True}
            t = (cap, mode, row["workspaceRoot"])
            if t in seen:
                faults.append(f"native.requested-capability-duplicate-ownership-tuple:{cap}:{mode}:{row['workspaceRoot']}")
                continue
            seen[t] = row
            rows.append(row)
    return sorted(rows, key=K.C), faults


def admit_requested_capabilities(rows):
    faults, seen = [], set()
    for r in rows:
        t = (r["capabilityId"], r["languageMode"], r["workspaceRoot"])
        if t in seen:
            faults.append(f"native.requested-capability-duplicate-ownership-tuple:{':'.join(t)}")
        seen.add(t)
        if r["capabilityId"] not in MATRIX_IDS:
            faults.append(f"native.requested-capability-unregistered:{r['capabilityId']}")
        elif r["languageMode"] not in EN.LANGUAGE_MODES:
            faults.append(f"native.requested-capability-mode-unregistered:{r['languageMode']}")
        elif cell_state(r["capabilityId"], r["languageMode"])["state"] == "NOT-SELECTED":
            faults.append(f"native.requested-capability-mode-not-selected:{r['capabilityId']}:{r['languageMode']}")
    return faults


def availability_step(step_id, rows, release):
    declared = {(r["capabilityId"], m) for r in release for m in r["languageModes"]}
    notices, accounts = [], []
    for row in rows:
        if not row["required"] or (row["capabilityId"], row["languageMode"]) in declared:
            continue
        cap = next(c for c in EN.MATRIX["capabilities"] if c["id"] == row["capabilityId"])
        cell = cell_state(row["capabilityId"], row["languageMode"])
        notices.append({"code": "native.capability-unavailable", "capabilityId": row["capabilityId"], "languageMode": row["languageMode"],
                        "workspaceRoot": row["workspaceRoot"],
                        "remedy": f"install a release declaring {row['capabilityId']} for {row['languageMode']} or narrow analysis.capabilities explicitly"})
        if cap["relations"]:
            answer = ((cell["deficiency"], "capability-missing") if cell["state"] == "UNSUPPORTED-TYPED" else ("provider-unavailable", "capability-missing"))
            accounts.append({"capabilityId": row["capabilityId"], "languageMode": row["languageMode"], "workspaceRoot": row["workspaceRoot"],
                             "projection": "coverage-entry", "relationRungs": [f"{r}@{g}" for r, g in cap["relations"]],
                             "matrixState": cell["state"], "coverageAnswerWhenRun": {"deficiency": answer[0], "nativeCause": answer[1]}})
        else:
            accounts.append({"capabilityId": row["capabilityId"], "languageMode": row["languageMode"], "workspaceRoot": row["workspaceRoot"],
                             "projection": "selection-account-only", "relationRungs": [], "matrixState": cell["state"], "coverageAnswerWhenRun": None})
    return {"stepId": step_id, "noticeCount": len(notices), "notices": notices}, accounts


def multi_unit():
    files = {"Cargo.toml": b"[package]\nname = \"tool\"\nversion = \"0.1.0\"\nedition = \"2021\"\n", "src/main.rs": b"fn main() {}\n",
             "package.json": b"{\"name\":\"root\",\"version\":\"1.0.0\"}\n", "index.js": b"module.exports = 1;\n",
             "packages/web/tsconfig.json": b"{\"compilerOptions\":{\"strict\":true}}\n", "packages/web/src/app.ts": b"export const a = 1;\n",
             "docs/README.md": b"# docs\n"}
    disc = M.discover_units(files)
    units = disc["units"]
    must("three-units", sorted((u["rootPath"], u["languageMode"]) for u in units) == [("", "js-synthesized"), ("", "rust-cargo"), ("packages/web", "ts-tsconfig")],
         [(u["rootPath"], u["languageMode"]) for u in units])
    release = sorted([{"capabilityId": "inventory", "languageModes": sorted(["js-synthesized", "rust-cargo", "ts-tsconfig"])},
                      {"capabilityId": "syntax", "languageModes": sorted(["js-synthesized", "rust-cargo", "ts-tsconfig"])},
                      {"capabilityId": "calls", "languageModes": ["ts-tsconfig"]},
                      {"capabilityId": "clones-fact", "languageModes": sorted(["rust-cargo", "ts-tsconfig"])}], key=K.C)
    rel_faults = admit_release(release)
    rows, sel_faults = default_capability_selection(units)
    spec = {"schemaVersion": 2, "requestedCapabilities": rows, "policyPackIds": [], "parameters": []}
    spec_ok, spec_errs = admit(spec, ID, "#/$defs/analysis-spec")
    step, accounts = availability_step(0, rows, release)
    availability = {"stepCount": 1, "totalNoticeCount": step["noticeCount"], "steps": [step]}
    av_ok, av_errs = admit(availability, COMMON3, "#/$defs/CapabilityAvailabilityV1")
    must("release-admits", not rel_faults, rel_faults)
    must("default-selection-no-faults", not sel_faults, sel_faults)
    must("analysis-spec-admits", spec_ok, spec_errs)
    must("availability-admits", av_ok, av_errs)
    cand = [a for a in accounts if a["projection"] == "selection-account-only"]
    must("candidate-only-accounts-present", {a["capabilityId"] for a in cand} >= {"clones-near", "clones-cross-tsjs"}, cand)
    not_selected = [(c, u["languageMode"]) for u in units for c in MATRIX_IDS if cell_state(c, u["languageMode"])["state"] == "NOT-SELECTED"]
    release_negatives = []
    for label, rows_bad, expect in (
            ("duplicate-capability-row", release + [{"capabilityId": "syntax", "languageModes": ["rust-cargo"]}], "native.release-capability-duplicate"),
            ("preview-constant-row", sorted(release + [{"capabilityId": "preview-typescript", "languageModes": ["ts-tsconfig"]}], key=K.C), "native.release-capability-preview-constant"),
            ("not-selected-mode", sorted(release + [{"capabilityId": "clones-cross-tsjs", "languageModes": ["rust-cargo"]}], key=K.C), "native.release-capability-mode-not-selected"),
            ("unregistered-capability", sorted(release + [{"capabilityId": "dataflow", "languageModes": ["ts-tsconfig"]}], key=K.C), "native.release-capability-unregistered")):
        fl = admit_release(rows_bad)
        ok = bool(fl) and fl[0].startswith(expect)
        must(label, ok, fl)
        release_negatives.append({"vector": label, "classification": "invalid", "firstRefusal": fl[0] if fl else None, "masksLater": fl[1:], "pass": ok,
                                  "publicRoute": route_row(fl[0].split(":")[0]) if fl else None})
    candidate_record = {"schemaVersion": 1, "planId": "plan2:" + "1" * 64, "executionPlanId": "exec-plan2:" + "2" * 64, "cellOrdinal": 0, "programOrdinal": 0,
                        "capabilityId": "clones-near", "languageMode": "ts-tsconfig", "universe": "3" * 64, "producerClosure": "closure2:" + "4" * 64,
                        "stageOrdinal": 0, "state": "complete", "deficiency": None, "nativeCause": None, "authority": "candidate-only",
                        "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False, "examinedPaths": ["packages/web/src/app.ts"],
                        "groupDigests": [], "sourceBodies": []}
    c_ok, c_errs = admit(candidate_record, "foundation/execution-inputs.schema.v1.json", "#/$defs/CandidateProducerResultV1")
    claim = dict(candidate_record, semanticEquivalenceClaimed=True)
    cl_ok, cl_errs = admit(claim, "foundation/execution-inputs.schema.v1.json", "#/$defs/CandidateProducerResultV1")
    must("candidate-record-admits", c_ok, c_errs)
    must("candidate-equivalence-claim-refused", not cl_ok, "admitted")
    proj = KIT.doc("foundation/evaluator-projection-registry.v1.json")["capabilityForRelation"]
    override = ["inventory", "syntax"]
    over_rows = [r for r in rows if r["capabilityId"] in override]
    over_step, _ = availability_step(0, over_rows, release)
    layers = []
    for cap, mode in (("calls", "js-synthesized"), ("types", "rust-cargo"), ("clones-near", "ts-tsconfig"), ("references", "ts-tsconfig"), ("clones-fact", "js-synthesized")):
        cell = cell_state(cap, mode)
        layers.append({"capabilityId": cap, "languageMode": mode, "productPromise": cell["state"], "requestedByDefault": cell["state"] != "NOT-SELECTED",
                       "installedAvailability": (cap, mode) in {(r["capabilityId"], m) for r in release for m in r["languageModes"]},
                       "explicitOverrideRequests": cap in override,
                       "semanticPrerequisite": {"clones-fact": "TS scopeCapabilityLaw source variant; Rust SourceUnitOwnershipV1 dialect prerequisite",
                                                "clones-near": "candidate-only; no relation, no Coverage (matrix relations [])",
                                                "types": "resolved rung RC-2 complete + types derivationPolicy", "calls": "resolved-callee RC-2",
                                                "references": "resolved-binding RC-2"}[cap]})
    dump("vectors/multi-unit-missing-caps.json", {
        "classification": "valid", "repository": sorted(files), "units": units, "releaseDeclaration": release, "releaseAdmissionFaults": rel_faults,
        "defaultAnalysisSpec": spec, "analysisSpecAdmitted": spec_ok, "availability": availability, "availabilityAccounts": accounts,
        "notSelectedCellsNeverRequested": not_selected, "releaseNegatives": release_negatives,
        "candidateOnly": {"record": candidate_record, "admitted": c_ok, "equivalenceClaimRefused": not cl_ok,
                          "noRelationMapsToCandidateCapabilities": not any(v in ("clones-near", "clones-cross-tsjs") for v in proj.values()),
                          "enumerationKinds": {c: EN.KIND_DERIVATION[c] for c in ("clones-near", "clones-cross-tsjs")},
                          "requiredAbsentEnvelope": "EXECUTION_INPUTS_CANDIDATE_REQUIRED (vectors/phase4-tables.json cellOutcomeVectors candidate-required-absent)"},
        "promiseAvailabilityOverridePrerequisite": layers,
        "explicitOverride": {"configuredCapabilities": override, "requestedRows": len(over_rows), "noticesAfterOverride": over_step["noticeCount"],
                             "provenance": "CONFIGURED (default rows carry DEFAULTED)"},
        "selectors": ["native-evidence.md s1.4 lines 610-642 (U-1..U-4), 786-1022 (default selection, release registry, availability)",
                      "native-evidence.schemas.v2.json#/$defs/ReleaseCapabilityRegistryV1", "workflows/schemas/evaluator3/common.schema.json#/$defs/CapabilityAvailabilityV1",
                      "native-capability-matrix.v2.json#/capabilities (relations [] for candidate-only)"]})
    return units, release, rows


# ------------------------------------------------------------------ public termination from internal refusal (native s10 route registry)
def route_row(key):
    row = REG["keys"].get(key)
    return None if row is None else {"possibleOrigins": row["possibleOrigins"], "originDependent": row.get("originDependent", False)}


def normalize_internal_key(raw):
    best = None
    for k in REG["keys"]:
        if raw == k or raw.startswith(k + ":"):
            if best is None or len(k) > len(best):
                best = k
    if best is None:
        return None, None
    return best, raw[len(best) + 1:] if len(raw) > len(best) else ""


def bounded_subject(raw):
    if len(raw) <= 1024:
        return raw
    marker = "...#sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return raw[:1024 - len(marker)] + marker


def public_termination_for(raw, origin):
    key, value = normalize_internal_key(raw)
    if key is None:
        return None, "native.public-route-key-unregistered"
    row = REG["keys"][key]
    if origin not in row["possibleOrigins"]:
        return None, "native.public-route-origin-not-possible"
    route = row["byOriginatingBoundary"][origin] if row.get("originDependent") else row["route"]
    if not route.get("class"):
        return None, "cb24.ROUTE_HAS_NO_TERMINATION"
    term = {"class": route["class"]}
    for f in ("errorCode", "faultCause"):
        if route.get(f):
            term[f] = route[f]
    subject = bounded_subject(f"{key}:{value}" if value else key)
    remedy = {"CONFIG.INVALID": "correct the configured capability request; one row per (capabilityId, languageMode, workspaceRoot) from the closed matrix vocabulary",
              "native.capability-spec-invalid": "correct the supplied analysis spec: name registered capabilities, one row per ownership tuple",
              "HOST.INVARIANT_VIOLATED": "report a host defect; the host minted an invalid internal record",
              "native.coverage-cause-unsupported": "the provider emitted an unsupported deficiency/cause pair; update or replace the provider",
              "PROVIDER.NOT_SELECTED": "request a capability/mode cell the product promises",
              "native.release-declaration-invalid": "reinstall or repair the authenticated release declaration"}
    if route.get("domainDetail"):
        term["domainDetail"] = {"code": route["domainDetail"], "remedy": remedy.get(route["domainDetail"], "see remedy"), "subject": subject}
    errors = [term["domainDetail"]] if "domainDetail" in term else [{"code": route["envelopeDetail"], "remedy": remedy.get(route["envelopeDetail"], "see remedy"), "subject": subject}]
    return {"key": key, "value": value, "origin": origin, "termination": term, "errors": errors}, None


def failure_envelope(derived, n, project_id=None):
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": req_id(n), "termination": derived["termination"],
           "exitCode": EXIT[derived["termination"]["class"]], "errors": derived["errors"]}
    if project_id:
        env["projectId"] = project_id
    return env


def check_envelope(env):
    ok, errs = admit(env, ENV3, "#")
    faults = [] if ok else [f"SCHEMA:{errs}"]
    t = env["termination"]
    if EXIT[t["class"]] != env["exitCode"]:
        faults.append("cb24.ENVELOPE_EXIT_CLASS_MISMATCH")
    if env["kind"] == "failure" and "domainDetail" in t and env["errors"] != [t["domainDetail"]]:
        faults.append("cb24.ENVELOPE_ERRORS_DISAGREE_WITH_TERMINATION_DETAIL")
    t_ok, t_errs = admit(t, COMMON3, "#/$defs/StepTermination")
    if not t_ok:
        faults.append(f"TERMINATION_SCHEMA:{t_errs}")
    return faults


def failure_envelopes(project_id):
    # actual internal refusals
    config_raw = admit_requested_capabilities([{"capabilityId": "made-up-capability", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True}])
    spec_raw = admit_requested_capabilities([{"capabilityId": "calls", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True},
                                             {"capabilityId": "calls", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": False}])
    dup_units = [{"rootPath": "", "languageMode": "js-synthesized"}, {"rootPath": "", "languageMode": "js-synthesized"}]
    host_raw = default_capability_selection(dup_units)[1]
    g, store, _ = loaded("ts-pass")
    exported = json.load(open(f"{OUT}/runs/ts-pass.store.json"))
    cid, (cd, payload) = next((c, v) for c, v in sorted(g["coverages"].items()) if v[1] is not None)
    entry = copy.deepcopy(payload["entry"])
    entry.update({"coverage": "unknown", "deficiency": "provider-unavailable", "nativeCause": "body-language-owner-ambiguous"})
    # the same registry check ref/native_facts.coverage_faults runs at the producer boundary, over an admitted ts-pass entry
    producer_raw = [f"{k}:{entry['deficiency']}:{entry['nativeCause']}" for k in NF.cause_registry_faults(entry, payload["key"]["relation"])]
    must("producer-raw-refusal", producer_raw, cid)
    stale = json.load(open(f"{OUT}/runs/ts-pass~import-stale-snapshot.replay.json"))["graphAdmission"]["faults"]
    cases = [("config-input", config_raw[0], "external-configuration", "envelopes/config-input.json"),
             ("retained-external-input", spec_raw[0], "externally-supplied-spec", "envelopes/retained-external-input.json"),
             ("host-invalid-internal", host_raw[0], "host-generated-internal-layer", "envelopes/host-invalid-internal.json"),
             ("producer-boundary", producer_raw[0], "producer-boundary", "envelopes/producer-boundary.json")]
    summary = []
    for i, (label, raw, origin, path) in enumerate(cases):
        derived, refusal = public_termination_for(raw, origin)
        env = failure_envelope(derived, 100 + i) if derived else None
        faults = check_envelope(env) if env else [refusal]
        must(f"envelope-{label}", not faults, faults)
        doc = {"classification": "valid", "internalRefusal": raw, "originatingBoundary": origin, "derivation": derived, "envelope": env, "envelopeFaults": faults,
               "exitTable": EXIT, "selectors": ["native-evidence.schemas.v2.json#/x-opensip-public-route-registry", "workflows-and-surfaces.md s8 lines 1126-1131, s9 lines 1135-1170",
                                               "admission-and-qualification s1 (actor/layer split, via originatingBoundaryLaw)"]}
        dump(path, doc)
        summary.append({"case": label, "internalRefusal": raw, "origin": origin, "class": derived and derived["termination"]["class"],
                        "errorCode": derived and derived["termination"].get("errorCode"), "envelopeDetail": derived and derived["errors"][0]["code"], "faults": faults})
    # the stale selected import refusal has a public code already (golden import-stale-selected)
    golden = next(x for x in KIT.doc("workflows/command-inventory.v3.json")["goldens"] if x["id"] == "import-stale-selected")
    stale_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": req_id(110),
                 "termination": {"class": golden["class"], "errorCode": golden["errorCode"],
                                 "domainDetail": {"code": golden["domainDetail"], "remedy": golden["remedy"], "subject": bounded_subject(stale[0])}},
                 "exitCode": golden["exitCode"]}
    stale_env["errors"] = [stale_env["termination"]["domainDetail"]]
    sf = check_envelope(stale_env)
    must("stale-import-envelope", not sf, sf)
    controls = []
    for label, raw, origin, expect in (("origin-not-possible", producer_raw[0], "external-configuration", "native.public-route-origin-not-possible"),
                                       ("unregistered-internal-key", "native.not-a-registered-key:x", "external-configuration", "native.public-route-key-unregistered"),
                                       ("origin-dependent-differs-by-actor", config_raw[0], "host-generated-internal-layer", None)):
        derived, refusal = public_termination_for(raw, origin)
        ok = (refusal == expect) if expect else (derived is not None and derived["termination"]["class"] == "operational-failed")
        must(f"route-control-{label}", ok, (derived, refusal))
        controls.append({"vector": label, "classification": "invalid" if expect else "valid", "firstRefusal": refusal, "derived": derived, "pass": ok})
    long_mode = "x" * 4096
    long_raw = admit_requested_capabilities([{"capabilityId": "calls", "languageMode": long_mode, "workspaceRoot": ".", "required": True}])[0]
    derived, _ = public_termination_for(long_raw, "external-configuration")
    lenv = failure_envelope(derived, 120)
    lf = check_envelope(lenv)
    subj = derived["termination"]["domainDetail"]["subject"]
    must("subject-bound-elision", not lf and len(subj) == 1024 and subj.startswith("native.requested-capability-mode-unregistered:"), (lf, len(subj)))
    controls.append({"vector": "subject-bound-elision-4096-scalar-mode", "classification": "valid", "subjectLength": len(subj), "envelopeFaults": lf,
                     "subjectTail": subj[-80:], "pass": not lf and len(subj) == 1024})
    dump("envelopes/public-from-internal.json", {"cases": summary, "staleImportGolden": golden, "staleImportEnvelope": stale_env, "staleImportFaults": sf, "routeControls": controls,
                                                "internalRefusalSources": {"config/spec": "tools/phase7_vectors.py admit_requested_capabilities (same law as ref/closure.py analysis-spec check)",
                                                                           "host": "default_capability_selection duplicate guard",
                                                                           "producer": "ref/native_facts.py coverage_faults on re-admitted runs/ts-pass universe",
                                                                           "stale import": "runs/ts-pass~import-stale-snapshot.replay.json first graph fault"}})
    return g, store, exported


# ------------------------------------------------------------------ D9 extension precedence
def d9_precedence():
    inherited = KIT.doc("coop/artifacts/d9-exit-contract.v1.14.json")
    c3 = KIT.doc(COMMON3)["$defs"]
    inh_causes = set(inherited["codeMaps"]["faultCauseToErrorCode"])
    sel_causes = set(c3["D9FaultCause"]["enum"]) - {"none"}
    measured = {
        "classToExitCodeUnchanged": inherited["classToExitCode"] == EXIT,
        "errorCodesUnchanged": sorted(inherited["codeVocabulary"]["errorCodes"]) == sorted(c3["D9ErrorCode"]["enum"]),
        "reasonCodesUnchanged": sorted(inherited["codeVocabulary"]["reasonCodes"]) == sorted(c3["D9ReasonCode"]["enum"]),
        "everyInheritedCausePreserved": inh_causes <= sel_causes,
        "extensionIsExactlyHostInvariant": sel_causes - inh_causes == {"host-invariant"},
        "successorCodeHadNoInheritedCausePreimage": "SYSTEM.OUTCOME.ILLEGAL_STATE" not in inherited["codeMaps"]["faultCauseToErrorCode"].values(),
        "causePrecedenceUnchanged": inherited["causeModel"]["precedence"] == ["faultCause", "rejectionCause", "deficiency"]}
    term = {"class": "operational-failed", "errorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE", "faultCause": "host-invariant",
            "domainDetail": {"code": "HOST.INVARIANT_VIOLATED", "remedy": "report a host defect"}}
    sel_ok, sel_errs = admit(term, COMMON3, "#/$defs/StepTermination")
    inherited_check = [] if term["faultCause"] in inh_causes else ["D9-INHERITED:faultCause-outside-declared-cause-domain:host-invariant"]
    measured["selectedCompositionAdmitsHostInvariant"] = sel_ok
    measured["inheritedArtifactAloneRefusesHostInvariant"] = bool(inherited_check)
    for k, v in measured.items():
        must(f"d9-{k}", v, k)
    dump("vectors/d9-extension-precedence.json", {"classification": "valid", "measured": measured, "hostInvariantTermination": term,
                                                 "selectedAdmission": sel_ok, "selectedErrors": sel_errs, "inheritedOnlyCheck": inherited_check,
                                                 "aggregateOrderWorkflows": ["operational-failed", "request-rejected", "policy-failed", "indeterminate", "success"],
                                                 "note": "The inherited artifact keeps its bytes; the selected composition adds exactly faultCause host-invariant -> SYSTEM.OUTCOME.ILLEGAL_STATE. "
                                                         "A checker validating against the inherited artifact alone refuses a lawful selected termination (the registry's live successorArtifactObligation).",
                                                 "selectors": ["coop/artifacts/d9-exit-contract.v1.14.json#/codeMaps", "native-evidence.schemas.v2.json#/x-opensip-public-route-registry/hostInvariantSuccessor",
                                                               "workflows/schemas/evaluator3/common.schema.json#/$defs/D9FaultCause"]})


# ------------------------------------------------------------------ invocation envelopes
def analysis_result(g, proof_verdict, exec_defs):
    return {"kind": "analysis", "authority": "authoritative", "runId": g["runId"], "planId": g["plan_id"], "verdict": proof_verdict,
            "requiredCoverage": "satisfied" if not exec_defs else "unsatisfied", "durability": "committed", "deficiency": "none" if not exec_defs else "verdict-indeterminate",
            "secondaryDeficiencies": []}


def loaded(name):
    exported = json.load(open(f"{OUT}/runs/{name}.store.json"))
    store = Store.load(exported)
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    must(f"{name}-admits", not C.faults, C.faults[:2])
    g["runId"] = exported["runId"]
    return g, store, g["proof"]


def invocation_envelopes(release):
    g, store, proof = loaded("ts-pass")
    n = 200

    def step_spec(i, kind, params, depends=(), gate="completed", retry="none"):
        return {"stepId": i, "kind": kind, "requirement": "required", "dependsOn": list(depends), "dependencyGate": gate, "retryPolicy": retry, "params": params}
    analysis_params = {"kind": "analysis", "profile": "default", "role": "primary", "verdictGate": "self", "durability": "authoritative", "snapshotSource": "live-worktree"}
    render_params = {"kind": "render", "format": "json", "destination": "stdout", "sourceSteps": [0], "required": True}
    ar = analysis_result(g, proof["verdict"], proof["executionDeficiencies"])
    run_term = {"class": "success", "runId": g["runId"]}
    record = {"schemaFamily": "opensip.product.invocation", "schemaMajor": 3, "requestId": req_id(n), "projectId": g["snapshot"]["projectId"],
              "workflow": {"kind": "builtin", "name": "default"}, "mode": {"interactive": False, "ci": True, "ephemeral": False},
              "orderedSteps": [step_spec(0, "analysis", analysis_params, retry="idempotent-retry"), step_spec(1, "render", render_params, [0], "terminal", "idempotent-retry")],
              "stepResults": [{"stepId": 0, "outcome": "completed",
                               "attempts": [{"executionId": exec_id(n), "outcome": "completed",
                                             "derivation": {"planId": g["plan_id"], "executionPlanId": g["exec_plan_id"], "stageCount": 1, "stagesCompleted": 1}}],
                               "result": ar, "termination": run_term},
                              {"stepId": 1, "outcome": "completed", "attempts": [{"executionId": exec_id(n + 1), "outcome": "completed"}],
                               "result": {"kind": "render", "format": "json", "rendererVersion": 3, "bytes": 4096, "truncation": False, "written": True},
                               "termination": {"class": "success"}}],
              "termination": run_term, "terminationEmitted": True,
              "retentionDisclosure": {"policy": "durable-unbounded", "provenance": "DEFAULTED", "firstUse": True, "storageRoot": ".opensip/store"}}
    rows = store.get_record(g["plan"]["analysisSpecDigest"])["requestedCapabilities"]
    step, _ = availability_step(0, rows, release)
    availability = {"stepCount": 1, "totalNoticeCount": step["noticeCount"], "steps": [step]}
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "invocation", "requestId": record["requestId"], "projectId": record["projectId"],
           "termination": run_term, "exitCode": 0, "invocation": record, "availability": availability, "retentionDisclosure": record["retentionDisclosure"]}
    f = check_envelope(env)
    rec_ok, rec_errs = admit(record, INVOC3, "#")
    must("invocation-disclosure-envelope", not f and rec_ok, (f, rec_errs))
    run_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "run", "requestId": record["requestId"], "projectId": record["projectId"],
               "termination": run_term, "exitCode": 0, "run": ar, "availability": availability, "retentionDisclosure": record["retentionDisclosure"]}
    rf = check_envelope(run_env)
    must("run-envelope", not rf, rf)
    bounds = {"orderedSteps.maxItems": KIT.doc(INVOC3)["properties"]["orderedSteps"]["maxItems"], "attempts.maxItems": KIT.doc(INVOC3)["$defs"]["StepResult"]["properties"]["attempts"]["maxItems"],
              "availability.steps.maxItems": KIT.doc(COMMON3)["$defs"]["CapabilityAvailabilityV1"]["properties"]["steps"]["maxItems"],
              "notices.maxItems": KIT.doc(COMMON3)["$defs"]["CapabilityAvailabilityStepV1"]["properties"]["notices"]["maxItems"]}
    dump("envelopes/invocation-disclosure.json", {"classification": "valid", "envelope": env, "envelopeFaults": f, "invocationRecordAdmitted": rec_ok,
                                                 "runEnvelope": run_env, "runEnvelopeFaults": rf,
                                                 "ownershipFields": {"requestId": record["requestId"], "projectId": record["projectId"], "workflow": record["workflow"],
                                                                     "availabilityTuple": ["capabilityId", "languageMode", "workspaceRoot"]},
                                                 "boundedCardinality": bounds, "ordering": "orderedSteps/stepResults/attempts/notices are x-opensip-order sequence (step order, selection order)",
                                                 "applicableOutputFormats": INVENTORY["default"]["formats"], "parityFields": INVENTORY["default"]["parityFields"],
                                                 "selectors": ["workflows-and-surfaces.md s1, s8 lines 1088-1131", "workflows/command-inventory.v3.json#/commands[name=default]"]})
    # single-step: help (one render step)
    single = {"schemaFamily": "opensip.product.invocation", "schemaMajor": 3, "requestId": req_id(n + 10), "workflow": {"kind": "builtin", "name": "help"},
              "mode": {"interactive": True, "ci": False, "ephemeral": False},
              "orderedSteps": [step_spec(0, "render", {"kind": "render", "format": "human", "destination": "stdout", "sourceSteps": [], "required": True}, retry="idempotent-retry")],
              "stepResults": [{"stepId": 0, "outcome": "completed", "attempts": [{"executionId": exec_id(n + 10), "outcome": "completed"}],
                               "result": {"kind": "render", "format": "human", "rendererVersion": 1, "bytes": 2048, "truncation": False, "written": True},
                               "termination": {"class": "success"}}],
              "termination": {"class": "success"}, "terminationEmitted": True}
    senv = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "invocation", "requestId": single["requestId"], "termination": {"class": "success"},
            "exitCode": 0, "invocation": single}
    sf = check_envelope(senv)
    must("single-step-envelope", not sf and INVENTORY["help"]["steps"] == ["render"], sf)
    dump("envelopes/single-step.json", {"classification": "valid", "command": "help", "inventorySteps": INVENTORY["help"]["steps"], "formats": INVENTORY["help"]["formats"],
                                       "envelope": senv, "envelopeFaults": sf})
    # multi-step with different selections: two same-project Rust Runs with different analysis selections
    ga, sa, pa = loaded("rust-mixed")
    gb, sb, pb = loaded("rust-mixed-clones-required")
    must("multi-step-same-project", ga["snapshot"]["projectId"] == gb["snapshot"]["projectId"], None)
    rows_a = sa.get_record(ga["plan"]["analysisSpecDigest"])["requestedCapabilities"]
    rows_b = sb.get_record(gb["plan"]["analysisSpecDigest"])["requestedCapabilities"]
    release_rust = sorted([{"capabilityId": "calls", "languageModes": ["rust-cargo"]}, {"capabilityId": "inventory", "languageModes": ["rust-cargo"]},
                           {"capabilityId": "syntax", "languageModes": ["rust-cargo"]}], key=K.C)
    step_a, _ = availability_step(0, rows_a, release_rust)
    step_b, _ = availability_step(1, rows_b, release_rust)
    avail = {"stepCount": 2, "totalNoticeCount": step_a["noticeCount"] + step_b["noticeCount"], "steps": [step_a, step_b]}
    ra, rb = analysis_result(ga, pa["verdict"], pa["executionDeficiencies"]), analysis_result(gb, pb["verdict"], pb["executionDeficiencies"])
    multi = {"schemaFamily": "opensip.product.invocation", "schemaMajor": 3, "requestId": req_id(n + 20), "projectId": ga["snapshot"]["projectId"],
             "workflow": {"kind": "profile", "contributionId": "cb24.workflows", "activationId": "cb24.two-selection-analysis", "profileVersion": "1.0.0"},
             "mode": {"interactive": False, "ci": True, "ephemeral": False},
             "orderedSteps": [step_spec(0, "analysis", analysis_params, retry="idempotent-retry"), step_spec(1, "analysis", analysis_params, retry="idempotent-retry"),
                              step_spec(2, "render", dict(render_params, sourceSteps=[0, 1]), [0, 1], "terminal", "idempotent-retry")],
             "stepResults": [{"stepId": i, "outcome": "completed",
                              "attempts": [{"executionId": exec_id(n + 20 + i), "outcome": "completed",
                                            "derivation": {"planId": gx["plan_id"], "executionPlanId": gx["exec_plan_id"], "stageCount": 1, "stagesCompleted": 1}}],
                              "result": rx, "termination": {"class": "success", "runId": gx["runId"]}} for i, (gx, rx) in enumerate(((ga, ra), (gb, rb)))] +
                            [{"stepId": 2, "outcome": "completed", "attempts": [{"executionId": exec_id(n + 23), "outcome": "completed"}],
                              "result": {"kind": "render", "format": "json", "rendererVersion": 3, "bytes": 8192, "truncation": False, "written": True},
                              "termination": {"class": "success"}}],
             "termination": {"class": "success", "runId": ga["runId"]}, "terminationEmitted": True}
    menv = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "invocation", "requestId": multi["requestId"], "projectId": multi["projectId"],
            "termination": multi["termination"], "exitCode": 0, "invocation": multi, "availability": avail}
    mf = check_envelope(menv)
    differ = {(r["capabilityId"], r["required"]) for r in rows_a} != {(r["capabilityId"], r["required"]) for r in rows_b} and step_a["noticeCount"] != step_b["noticeCount"]
    must("multi-step-envelope", not mf and differ, (mf, step_a["noticeCount"], step_b["noticeCount"]))
    dump("envelopes/multi-step.json", {"classification": "valid", "envelope": menv, "envelopeFaults": mf,
                                      "selections": {"step0": {"run": "rust-mixed", "requestedCapabilities": rows_a}, "step1": {"run": "rust-mixed-clones-required", "requestedCapabilities": rows_b}},
                                      "releaseDeclaration": release_rust, "differentSelectionsMeasured": differ,
                                      "aggregateRule": "workflows s1 lines 230-237: over required steps operational-failed > request-rejected > policy-failed > indeterminate > success; "
                                                                       "ties retain the first termination carrying domain detail in step order, or the first termination when none carries detail"})
    return g, store


# ------------------------------------------------------------------ receipts and availability
def receipts(g, store, exported):
    run_id = g["runId"]
    objects = sorted({row["id"] for row in exported["objectTable"]}, key=K.C)
    inv = {"schemaVersion": 2, "runId": run_id, "objects": objects, "blobDigests": sorted(exported["blobs"], key=K.C)}
    inv_digest = K.raw_digest(inv)
    receipt = {"schemaVersion": 2, "runId": run_id, "executionId": exec_id(300), "namespaceId": "cb24.default", "commitSequence": 1, "inventoryDigest": inv_digest,
               "sealedAssurance": "replayable", "signerKeyId": "cb24-synthetic-signer"}
    gen0 = {"schemaVersion": 2, "runId": run_id, "generation": 0, "state": "retained", "missingRefs": [], "reason": "committed and retained"}
    proof_hex = g["seal"]["proofBundleId"].split(":", 1)[1]
    gen1 = {"schemaVersion": 2, "runId": run_id, "generation": 1, "state": "purged", "missingRefs": [{"domain": "proof-bundle", "digest": proof_hex}],
            "reason": "proof bytes purged under exclusive lease; sealed manifest remains queryable"}
    results = {}
    for label, rec, sel in (("commit-inventory", inv, "#/$defs/commit-inventory"), ("commit-receipt", receipt, "#/$defs/commit-receipt"),
                            ("availability-gen0", gen0, "#/$defs/availability"), ("availability-gen1", gen1, "#/$defs/availability")):
        ok, errs = admit(rec, ID, sel)
        must(f"receipt-{label}", ok, errs)
        results[label] = {"admitted": ok, "errors": errs}
    must("availability-generation-increments", gen1["generation"] == gen0["generation"] + 1 and gen1["runId"] == gen0["runId"], None)
    scope = {"schemaVersion": 1, "requestId": req_id(301), "stepId": 0, "projectId": g["snapshot"]["projectId"], "operation": "purge"}
    base = {"schemaFamily": "opensip.product.mutation-receipt", "schemaMajor": 1, "requestId": scope["requestId"], "stepId": 0, "executionId": exec_id(301),
            "operation": "purge", "idempotencyKey": K.H("workflow.mutation-intent", scope), "effectOutcome": "COMPLETED", "commitClass": "IRREVERSIBLE", "replayed": False}
    mreceipt = dict(base, receiptId="receipt2:" + K.H("workflow.mutation-receipt", base))
    replay_base = dict(base, executionId=exec_id(302), replayed=True)
    mreplay = dict(replay_base, receiptId="receipt2:" + K.H("workflow.mutation-receipt", replay_base))
    for label, rec in (("mutation-receipt", mreceipt), ("replay-delivery-receipt", mreplay)):
        ok, errs = admit(rec, REPAIR3, "#/$defs/MutationReceiptV1")
        must(label, ok, errs)
        results[label] = {"admitted": ok, "errors": errs}
    must("replay-receipt-separately-identified", mreplay["receiptId"] != mreceipt["receiptId"] and mreplay["idempotencyKey"] == mreceipt["idempotencyKey"], None)
    purge_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "mutation", "requestId": scope["requestId"], "projectId": scope["projectId"],
                 "termination": {"class": "success", "runId": run_id}, "exitCode": 0,
                 "mutation": {"operation": "purge", "receiptId": mreceipt["receiptId"], "effectOutcome": "COMPLETED", "commitClass": "IRREVERSIBLE", "replayed": False}}
    pf = check_envelope(purge_env)
    must("purge-mutation-envelope", not pf, pf)
    dump("envelopes/receipt-availability.json", {"classification": "valid", "runId": run_id, "commitInventory": {"objects": len(objects), "blobs": len(inv["blobDigests"]), "digest": inv_digest},
                                                "commitReceipt": receipt, "availability": [gen0, gen1], "mutationReceipt": mreceipt, "replayDeliveryReceipt": mreplay,
                                                "purgeEnvelope": purge_env, "purgeEnvelopeFaults": pf, "admission": results,
                                                "notPerformed": ["authenticated receipt signing", "physical fsync/durability", "ledger pin discovery"],
                                                "selectors": ["identity-and-evidence.md s6 'Reference lifecycle joins'", "identity-schemas.v3.json#/$defs/commit-receipt, #/$defs/availability",
                                                              "workflows-and-surfaces.md s1 lines 203-211 (receipt2 recipe)"]})


# ------------------------------------------------------------------ authority and step kinds
def authority_steps():
    kinds = KIT.doc(INVOC3)["$defs"]["StepKind"]["enum"]
    seals = {"analysis", "verify"}  # workflows s1: only analysis and verify steps seal or link run3
    receipts_k = set(KIT.doc(REPAIR3)["x-opensip-mutation-operation-map"]["byStepKindReceiptOperation"]) & set(kinds)
    retry_never = set(KIT.doc(INVOC3)["$defs"]["StepSpec"]["allOf"][0]["if"]["properties"]["kind"]["enum"])
    retry_ok = {"analysis", "verify", "query", "render", "doctor", "export-delivery"}  # StepSpec.retryPolicy description
    rows = []
    for k in kinds:
        rows.append({"stepKind": k, "sealsOrLinksRun3": k in seals, "requiredReceipt": k in receipts_k, "idempotentRetryLawful": k in retry_ok,
                     "retryPolicyNoneBySchema": k in retry_never})
    must("retry-description-agrees-with-schema", not (retry_ok & retry_never), sorted(retry_ok & retry_never))
    controls = []
    params = {"mutation": {"kind": "mutation", "mutationClass": "waiver-change", "idempotencyKey": "a" * 64},
              "analysis": {"kind": "analysis", "profile": "default", "role": "primary", "durability": "authoritative", "snapshotSource": "live-worktree"},
              "render": {"kind": "render", "format": "json", "destination": "stdout", "sourceSteps": [], "required": True}}
    for label, spec, want in (("mutation-with-idempotent-retry", {"stepId": 0, "kind": "mutation", "requirement": "required", "dependsOn": [], "dependencyGate": "completed",
                                                                  "retryPolicy": "idempotent-retry", "params": params["mutation"]}, False),
                              ("analysis-with-idempotent-retry", {"stepId": 0, "kind": "analysis", "requirement": "required", "dependsOn": [], "dependencyGate": "completed",
                                                                  "retryPolicy": "idempotent-retry", "params": params["analysis"]}, True),
                              ("render-terminal-gate", {"stepId": 1, "kind": "render", "requirement": "required", "dependsOn": [0], "dependencyGate": "terminal",
                                                        "retryPolicy": "none", "params": params["render"]}, True),
                              ("analysis-terminal-gate", {"stepId": 1, "kind": "analysis", "requirement": "required", "dependsOn": [0], "dependencyGate": "terminal",
                                                          "retryPolicy": "none", "params": params["analysis"]}, False),
                              ("repair-apply-as-generic-mutation", {"stepId": 0, "kind": "mutation", "requirement": "required", "dependsOn": [], "dependencyGate": "completed",
                                                                    "retryPolicy": "none", "params": dict(params["mutation"], mutationClass="repair-apply")}, False)):
        ok, errs = admit(spec, INVOC3, "#/$defs/StepSpec")
        must(f"step-{label}", ok == want, errs)
        controls.append({"vector": label, "classification": "valid" if want else "invalid", "admitted": ok, "firstRefusal": None if ok else (errs or [None])[0], "pass": ok == want})
    b = json.load(open(f"{OUT}/runs/syntax-code.build.json"))
    identities = {"semantic (content-derived, sealing)": ["snapshot2", "plan2", "exec-plan2", "scope2", "fact2", "coverage2", "view2", "subject3", "finding3", "proof3", "evidence3",
                                                         "seal3", "run3", "policy-derivation3", "finding-key2", "repairplan2", "baseline2", "comparison2"],
                  "operational (host-minted or request-scoped; no semantic authority)": ["RequestId req1_", "ExecutionId exec1_", "StepId", "ReceiptId receipt2 (H over a receipt carrying requestId/executionId)",
                                                                                          "mutation-intent idempotency key (bare H over MutationReplayScopeV1)", "security authorization refs",
                                                                                          "CommandEnvelope/InvocationRecord"],
                  "measured": {"runIdIndependentOfRequest": "envelopes/invocation-disclosure.json and envelopes/multi-step.json cite the same run3 values as runs/*.store.json under different RequestIds",
                               "syntaxCodeRunId": b["runId"]}}
    dump("vectors/authority-and-steps.json", {"stepKinds": rows, "stepSpecControls": controls, "identities": identities,
                                             "selectors": ["workflows-and-surfaces.md s1 lines 75-107, 109-125, 203-211", "workflows/schemas/evaluator3/invocation-record.schema.json#/$defs/StepSpec",
                                                           "identity-and-evidence.md s2 (tenant and operational identity)"]})


def chain():
    arrows = [
        ("security discovery / admitted boundaries -> discover_units", "native s1.4 U-8; ref/membership.py", "runs/*.store.json unit-membership records; vectors/multi-unit-missing-caps.json#/units"),
        ("discover_units -> UnitMembershipV1 + scope-descriptor", "native s1.4 U-1..U-4a, scope descriptor", "runs/syntax-code.replay.json (membership + scope re-derived in closure)"),
        ("release declaration + units -> default analysis-spec (required=true)", "native s1.4 lines 786-842", "vectors/multi-unit-missing-caps.json#/defaultAnalysisSpec"),
        ("analysis-spec + snapshot -> EnumerationPlanV1 / EvaluatorEmissionPlanV1 parameters -> plan2", "identity s4; enumeration contract s1", "runs/*.store.json plan objects; closure parameter checks"),
        ("capability manifest CVE1 -> capabilityManifestId", "CAP-MANIFEST-ID-V1", "vectors/capability-manifests.json; plan.capabilityManifestId re-derived in closure"),
        ("plan2 -> provider protocol3 session (Hello, stages, Coverage, Complete)", "native s9; protocol3-transitions.v1.json", "traces/complete.json, traces/unavailable.json, traces/fault.json"),
        ("provider returns -> fact2/scope2/coverage2/view2 (native producer admission)", "native s4; identity s3", "runs/*.replay.json graphAdmission"),
        ("stage returns -> ExecutionInputsV1 (host capture)", "execution-inputs contract s1-s5", "runs/*.store.json execution-inputs; closure re-derivation"),
        ("inputs -> evaluator3 proof3 -> evidence3 -> seal3 -> run3", "composition s9", "runs/*.replay.json semanticReplay (complete recompute + byte compare)"),
        ("run3 -> commit receipt + availability", "identity s6 reference lifecycle joins", "envelopes/receipt-availability.json"),
        ("run3 + termination -> CommandEnvelope (json parity reference)", "workflows s8-s9", "envelopes/invocation-disclosure.json, envelopes/single-step.json, envelopes/multi-step.json")]
    dump("vectors/chain-zero-config.json", {"classification": "explanatory", "arrows": [{"arrow": a, "owner": o, "executedArtifact": x} for a, o, x in arrows],
                                           "notExecuted": ["real security discovery instrument and OS custody", "real provider processes", "durable commit/fsync", "renderer processes"]})


def main():
    units, release, rows = multi_unit()
    g, store, exported = failure_envelopes(None)
    d9_precedence()
    invocation_envelopes(release)
    receipts(g, store, exported)
    authority_steps()
    chain()
    print("failures", len(failures))
    print(json.dumps(failures, default=str)[:6000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
