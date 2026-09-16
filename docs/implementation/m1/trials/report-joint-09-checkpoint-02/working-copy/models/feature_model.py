"""Report evidence design reference model (author-02): RP-DO-03 coupling, RP-DO-05 entry points, RP-DO-09 symbol metrics, RP-DO-10 test reachability.

Design/reference only; no product authority, no runtime, browser or Run replay qualification.

Corrections over author-01 (review01 F1-F9):
- F1 recognition custody is read from the admitted analysis-spec parameter entries of a Run (no synthetic flag); the registry row is optional and
  new Plans carry a separate pre-Plan duty (admit_new_plan_recognition_parameter).
- F2 test reach matches origins in every reached universe and embeds the per-universe origin sets used.
- F3 recognizer test globs never establish a complete test population: every TS/JS origin set is partial; configured jest selection is read as data
  (successor_recognition) and disclosed. No absence-style test state exists.
- F4 Rust entry points are the crate roots of every selected bin/lib target from retained SourceUnitOwnershipV1 + RustUniverseV2ResolvedInputs,
  with exact missing coverage; a workspace no longer reports all while ignoring member targets.
- F6 the coupling panel is byte-bounded collection by collection under the report-wide remaining exploration budget, with deterministic priority.
- F8 coupling counts expose observations (fact2), program edges and universe-independent source dependencies.
- F9 importer ownership keys on the imports fact anchor paths (native section 2.1 selection law), not on the importer symbol inventory path.
"""
import copy
import hashlib

C = None
RM = None


def bind(canonical_module, report_model):
    global C, RM
    C, RM = canonical_module, report_model


class Refusal(Exception):
    def __init__(self, code, text=""):
        super().__init__(code + (": " + text if text else ""))
        self.code = code


def need(condition, code, text=""):
    if not condition:
        raise Refusal(code, text)


def canon(value):
    return C.canonical(value)


def measure(value):
    """Unbounded canonical byte measurement (report_model.canonical has no 4 MiB codec limit, so oversized candidates can be measured and refused)."""
    return len(RM.canonical(value))


def raw_sha(value):
    return hashlib.sha256(canon(value)).hexdigest()


def native_h(domain, record):
    return "sha256:" + C.identity(domain, record)


def ekey(endpoint):
    return RM.canonical(endpoint)


PUBLIC_BOUNDS = {"maxPageSize": 1000, "defaultPageSize": 100, "maxItemsPerOperation": 100000, "maxTraversalDepth": 64, "maxVisitedNodes": 1000000}
FAMILY = {"rust-cargo": "rust", "rust-cargo-prepared": "rust", "ts-tsconfig": "tsjs", "js-allowjs": "tsjs", "js-synthesized": "tsjs", "syntax-only": "none"}
RECOGNITION_DOMAIN = "native.framework-recognition.v1"
COMPILATION_UNIT_DOMAIN = "native.compilation-unit.v1"
SOURCE_UNIT_OWNERSHIP_DOMAIN = "native.source-unit-ownership.v1"
ORIGIN_PAGE_SIZE = 100
HOST_PAGE_SIZE = 1000
TRACE_MAX_DEPTH = 16
TEST_REACH_MAX_DEPTH = 16
MAX_TRACES = 8
MAX_TEST_REACHABILITY = 64
MAX_ORIGIN_SETS = 256
MAX_DRILLDOWN = 1000
PLACEHOLDER_DELTA = 999999999
COUPLING_POLICY = "imports-resolved-target-owner-coupling.2"
SYMBOL_EVIDENCE_POLICY = "symbol-evidence.2"
ENTRY_TARGET_KINDS = ["bin", "lib"]
TEST_SELECTION_KEYS = ["projects", "roots", "testMatch", "testPathIgnorePatterns", "testRegex"]
METRIC_CATALOG = [
    ("distinct-resolved-callees-within-1-hop", "graph.reach", "calls", "resolved-callee", "outgoing", 1),
    ("distinct-resolved-callers-within-1-hop", "graph.reach", "calls", "resolved-callee", "incoming", 1),
    ("resolved-call-facts-incoming", "graph.neighbors", "calls", "resolved-callee", "incoming", None),
    ("resolved-call-facts-outgoing", "graph.neighbors", "calls", "resolved-callee", "outgoing", None),
    ("resolved-reference-facts-incoming", "graph.neighbors", "references", "resolved-binding", "incoming", None),
]
METRIC_IDS = [m[0] for m in METRIC_CATALOG]
OWNER_CAUSES = ["membership-row-missing", "no-program-unit", "not-compiled-by-selected-targets", "owned-only-by-unselected-targets",
                "owner-manifest-not-package-inventoried", "ownership-enumeration-partial", "ownership-missing", "package-inventory-conflict",
                "package-inventory-incomplete", "universe-not-plan-bound"]
IMPORTER_CAUSES = sorted(OWNER_CAUSES + ["importer-anchor-missing", "importer-anchor-owners-disagree"])
TARGET_CAUSES = sorted(OWNER_CAUSES + ["external-non-package-target", "file-not-inventoried", "package-endpoint-inventory-mismatch", "symbol-attribution-conflict",
                                       "symbol-inventory-incomplete", "symbol-inventory-missing", "symbol-not-inventoried", "unknown-occupancy"])
COUPLING_BLOCKERS = ["cells-omitted", "evidence-limitations", "projection-lower-bound", "target-buckets-omitted", "unattributed-importers", "unattributed-targets"]
TRACE_BLOCKERS = ["entry-recognition-not-all", "evidence-limitations", "origin-attribution-unavailable"]
CARGO_MISSING = ["ownership-enumeration-partial", "target-crate-root-ambiguous", "target-crate-root-unresolved"]
ORIGIN_NONE_CAUSES = ["no-test-recognizer", "ownership-missing", "recognition-not-plan-bound", "recognition-unavailable", "unsupported-language-family",
                      "universe-not-plan-bound"]
ORIGIN_LIMITATIONS = ["foreign-unit-paths-not-matched", "in-target-unit-tests-not-identified", "no-selected-test-targets", "ownership-enumeration-partial",
                      "recognizer-globs-not-test-population", "recognizer-unresolved-choices", "shared-test-and-non-test-target-path", "symbol-attribution-conflict",
                      "symbol-inventory-incomplete", "test-selection-configured"]
TEST_BLOCKERS = ["evidence-limitations", "origin-sets-not-embedded", "reach-lower-bound", "reached-universe-without-test-origin-identity", "test-origin-set-partial"]


def internal_root(text):
    return "" if text == "." else text


def join_root(root, name):
    return name if root == "" else root + "/" + name


def item_projection(total, kept, cause=None, delta=None):
    out = {"total": total, "omitted": total - kept, "omissionCause": cause if total > kept else "none"}
    if out["omissionCause"] == "byte-budget":
        out["rejectedByteDelta"] = delta
    return out


def byte_prefix(rows, budget):
    kept = []
    for row in rows:
        if measure(kept + [row]) > budget:
            return kept, item_projection(len(rows), len(kept), "byte-budget", measure(kept + [row]) - measure(kept))
        kept.append(row)
    return kept, item_projection(len(rows), len(kept))


# ---------------------------------------------------------------------------
# glob-pattern-contract.v1

def glob_match(pattern, candidate):
    ps, ss = pattern.split("/"), candidate.split("/")

    def segment(p, s):
        table = [[False] * (len(s) + 1) for _ in range(len(p) + 1)]
        table[0][0] = True
        for i in range(1, len(p) + 1):
            if p[i - 1] == "*":
                table[i][0] = table[i - 1][0]
            for j in range(1, len(s) + 1):
                if p[i - 1] == "*":
                    table[i][j] = table[i - 1][j] or table[i][j - 1]
                elif p[i - 1] == "?" or p[i - 1] == s[j - 1]:
                    table[i][j] = table[i - 1][j - 1]
        return table[len(p)][len(s)]

    memo = {}

    def match(i, j):
        if (i, j) not in memo:
            if i == len(ps):
                memo[(i, j)] = j == len(ss)
            elif ps[i] == "**":
                memo[(i, j)] = any(match(i + 1, k) for k in range(j, len(ss) + 1))
            else:
                memo[(i, j)] = j < len(ss) and segment(ps[i], ss[j]) and match(i + 1, j + 1)
        return memo[(i, j)]
    return match(0, 0)


# ---------------------------------------------------------------------------
# F1: new-Plan duty and custody from admitted parameters

def admit_new_plan_recognition_parameter(parameters, requested_capabilities, parameter_row_of, language_mode_map, row_key):
    """PRE-PLAN duty for a NEW evaluator3 Plan (never called by retained Run closure): when any requested capability names a compiler language mode
    (identity languageModes map value typescript or rust), exactly one parameter must resolve to the recognition registry row. The row itself is
    optional in the payload registry, so every retained predecessor Run stays admissible and reads as not-plan-bound."""
    compiler = sorted({row["languageMode"] for row in requested_capabilities if language_mode_map.get(row["languageMode"]) in ("typescript", "rust")})
    selected = [p for p in parameters if parameter_row_of(p["schemaDigest"]) == row_key]
    if compiler:
        need(len(selected) == 1, "NEW_PLAN_RECOGNITION_PARAMETER_REQUIRED", ",".join(compiler))
    return {"compilerLanguageModes": compiler, "recognitionParameters": len(selected)}


def custody_from_parameters(parameters, document_sha256, availability, retained_payloads):
    """Recognition custody of ONE admitted Run from its own analysis-spec parameter entries."""
    entries = [p for p in parameters if p["schemaDigest"] == document_sha256]
    if not entries:
        return {"state": "not-plan-bound"}
    need(len(entries) == 1, "J-FRP-PARAMETER-SELECTION")
    digest = entries[0]["payloadDigest"]
    state = availability["state"]
    if state in ("expired", "purged", "corrupt", "unavailable") or (state == "partial" and digest in availability["missingDigests"]) or digest not in retained_payloads:
        return {"state": "unavailable", "parameterDigest": digest, "availability": "unavailable" if state == "retained" else state}
    need(raw_sha(retained_payloads[digest]) == digest, "J-FRP-PARAMETER-DIGEST")
    return {"state": "plan-bound", "parameterDigest": digest, "availability": state}


# ---------------------------------------------------------------------------
# native successor recognition (S1 FR-6..FR-8), applied to the pinned native recognizer output

def recognition_summary(recognized, explicit_paths):
    if explicit_paths:
        return {"state": "all", "source": "explicit"}
    has = any(r["effects"]["entryPoints"] for r in recognized)
    unresolved = any(r["unresolvedChoices"] for r in recognized)
    if has and not unresolved:
        return {"state": "all", "source": "recognized"}
    if has:
        return {"state": "partial", "source": "recognized"}
    return {"state": "none", "source": "none"}


def successor_recognition(native_result, unit_root, unit_files, explicit_paths):
    """FR-6 repository-relative evidence/entry paths; FR-8 a jest object in package.json that sets any test selection key is read as data and
    reported as unresolved choice `test-selection-configured` (the native recognizer emits default globs regardless)."""
    out = copy.deepcopy(native_result)
    for result in out["recognized"]:
        for evidence in result["evidence"]:
            evidence["path"] = join_root(unit_root, evidence["path"])
        result["effects"]["entryPoints"] = [join_root(unit_root, p) for p in result["effects"]["entryPoints"]]
        if result["recognizerId"] == "vitest-jest" and "package.json" in unit_files:
            try:
                package = C.parse(unit_files["package.json"].encode("utf-8"))
            except C.AdmissionError:
                package = None
            jest = package.get("jest") if isinstance(package, dict) else None
            if isinstance(jest, dict) and any(k in jest for k in TEST_SELECTION_KEYS) and "test-selection-configured" not in result["unresolvedChoices"]:
                result["unresolvedChoices"] = sorted(result["unresolvedChoices"] + ["test-selection-configured"])
    out["entryPoints"] = recognition_summary(out["recognized"], explicit_paths)
    return out


# ---------------------------------------------------------------------------
# retained closure mock

class World:
    def __init__(self, data):
        self.data = data
        self.project_id, self.run_id, self.snapshot_id = data["projectId"], data["runId"], data["snapshotId"]
        self.inventory = {row["path"]: row for row in data["snapshotInventory"]}
        self.membership = data["membership"]
        self.units = {u["unitOrdinal"]: u for u in self.membership["units"]}
        need(len(self.units) == len(self.membership["units"]), "J-WORLD-MEMBERSHIP")
        self.member_rows = {}
        for row in self.membership["rows"]:
            need(row["path"] not in self.member_rows, "J-WORLD-MEMBERSHIP")
            self.member_rows[row["path"]] = row
        self.plan = data["enumerationPlan"]
        need(self.plan["membershipDigest"] == raw_sha(self.membership), "J-WORLD-MEMBERSHIP")
        self.bindings = {}
        for cell_ordinal, cell in enumerate(self.plan["cells"]):
            for binding in cell["programBindings"]:
                if binding["universe"] is not None:
                    self.bindings.setdefault(binding["universe"], []).append(
                        {"cellOrdinal": cell_ordinal, "programOrdinal": binding["ordinal"], "languageMode": cell["languageMode"], "workspaceRoot": cell["workspaceRoot"]})
        self.inventories = data["subjectInventories"]
        self.ownership = data["sourceUnitOwnership"]
        self.rust_universes = data["rustUniverses"]
        for universe, record in self.ownership.items():
            need(self.family(universe) == "rust", "J-WORLD-OWNERSHIP")
            for unit in record["units"]:
                projection = {"schemaVersion": 1, "markerPath": unit["markerPath"], "targetKind": unit["targetKind"], "targetName": unit["targetName"]}
                need(unit["unitId"] == native_h(COMPILATION_UNIT_DOMAIN, projection) and unit["markerPath"] in self.inventory, "J-WORLD-OWNERSHIP")
            declared = {u["unitId"] for u in record["units"]}
            need(set(record["selectedUnitIds"]) <= declared and all(r["unitId"] in declared and r["path"] in self.inventory for r in record["ownership"]), "J-WORLD-OWNERSHIP")
        for universe, inputs in self.rust_universes.items():
            need(self.family(universe) == "rust" and all(p in self.inventory for p in inputs["crateRootPaths"]), "J-WORLD-RUST-INPUTS")
            own = self.ownership.get(universe)
            need((own is None and inputs["sourceUnitOwnershipId"] is None) or (own is not None and inputs["sourceUnitOwnershipId"] == native_h(SOURCE_UNIT_OWNERSHIP_DOMAIN, own)),
                 "J-WORLD-RUST-INPUTS", "sourceUnitOwnershipId")
        self.parameters = data["analysisSpecParameters"]
        self.parameter_document_sha256 = data["parameterDocumentSha256"]
        self.parameter_availability = data["parameterAvailability"]
        self.retained_payloads = data["retainedParameterPayloads"]
        self.config_entry_points = data["resolvedConfigurationEntryPoints"]
        self.availability = data["availability"]
        self.test_bounds = data.get("testBounds")
        self.facts = expand_facts(data)
        for fact in self.facts:
            need(all(a["path"] in self.inventory for a in fact["anchors"]), "J-WORLD-ANCHOR")
        self.relations = data["relations"]

    def custody(self):
        return custody_from_parameters(self.parameters, self.parameter_document_sha256, self.parameter_availability, self.retained_payloads)

    def recognition_record(self):
        custody = self.custody()
        return self.retained_payloads[custody["parameterDigest"]] if custody["state"] == "plan-bound" else None

    def family(self, universe):
        rows = self.bindings.get(universe)
        if not rows:
            return None
        families = {FAMILY[r["languageMode"]] for r in rows}
        need(len(families) == 1, "J-WORLD-BINDING-FAMILY")
        return families.pop()

    def unit_for_universe(self, universe):
        family = self.family(universe)
        if family not in ("rust", "tsjs"):
            return None
        roots = {internal_root(r["workspaceRoot"]) for r in self.bindings[universe]}
        need(len(roots) == 1, "J-WORLD-BINDING-ROOT")
        root = roots.pop()
        found = [u for u in self.units.values() if u["rootPath"] == root and u["languageFamily"] == family]
        return found[0] if len(found) == 1 else None

    def symbol_rows(self, universe):
        keys = {(r["cellOrdinal"], r["programOrdinal"]) for r in self.bindings.get(universe, [])}
        return [inv for inv in self.inventories if inv["kind"] == "symbol" and (inv["cellOrdinal"], inv["programOrdinal"]) in keys]

    def symbol_attribution(self, universe, native_id):
        if universe not in self.bindings:
            return None, "universe-not-plan-bound"
        inventories = self.symbol_rows(universe)
        if not inventories:
            return None, "symbol-inventory-missing"
        paths = {row["path"] for inv in inventories for row in inv["rows"] if row["nativeSubjectId"] == native_id}
        if len(paths) > 1:
            return None, "symbol-attribution-conflict"
        if paths:
            return paths.pop(), None
        if any(inv["state"] != "complete" for inv in inventories):
            return None, "symbol-inventory-incomplete"
        return None, "symbol-not-inventoried"

    def package_row(self, path):
        names, incomplete = set(), False
        for inv in self.inventories:
            if inv["kind"] != "package":
                continue
            incomplete |= inv["state"] != "complete"
            names |= {row["nativeSubjectId"] for row in inv["rows"] if row["path"] == path}
        if len(names) > 1:
            return None, "package-inventory-conflict"
        if names:
            return names.pop(), None
        return None, "package-inventory-incomplete" if incomplete else "owner-manifest-not-package-inventoried"

    def path_owner_keys(self, universe, path):
        family = self.family(universe)
        if family is None:
            return None, "universe-not-plan-bound"
        if family == "rust":
            record = self.ownership.get(universe)
            if record is None:
                return None, "ownership-missing"
            if record["enumeration"] != "complete":
                return None, "ownership-enumeration-partial"
            owners = [r["unitId"] for r in record["ownership"] if r["path"] == path]
            if not owners:
                return None, "not-compiled-by-selected-targets"
            units = {u["unitId"]: u for u in record["units"]}
            selected = [units[u] for u in owners if u in set(record["selectedUnitIds"])]
            if not selected:
                return None, "owned-only-by-unselected-targets"
            keys = {}
            for unit in selected:
                _, cause = self.package_row(unit["markerPath"])
                if cause:
                    return None, cause
                keys[unit["markerPath"]] = {"keyKind": "first-party-package", "path": unit["markerPath"]}
            return [keys[k] for k in sorted(keys)], None
        if family == "tsjs":
            row = self.member_rows.get(path)
            if row is None:
                return None, "membership-row-missing"
            if row["membership"] != "program-member" or row["languageFamily"] != "tsjs" or row["unitOrdinal"] is None:
                return None, "no-program-unit"
            unit = self.units[row["unitOrdinal"]]
            manifest = join_root(unit["rootPath"], "package.json")
            if manifest in self.inventory:
                _, cause = self.package_row(manifest)
                if cause:
                    return None, cause
                return [{"keyKind": "first-party-package", "path": manifest}], None
            return [{"keyKind": "workspace-unit", "path": unit["markerPath"]}], None
        return None, "no-program-unit"

    def endpoint_owner_keys(self, endpoint, occupancy):
        """-> (keys, cause, target source identity)"""
        if occupancy == "unknown":
            return None, "unknown-occupancy", None
        if occupancy == "external":
            if endpoint["kind"] == "package":
                return ([{"keyKind": "external-package", "universe": endpoint["universe"], "path": endpoint["packageManifestPath"], "name": endpoint["nativeSubjectId"]}], None,
                        "external-package:" + endpoint["nativeSubjectId"] + "@" + endpoint["packageManifestPath"])
            return None, "external-non-package-target", None
        if endpoint["kind"] == "package":
            name, cause = self.package_row(endpoint["packageManifestPath"])
            if cause:
                return None, cause, None
            if name != endpoint["nativeSubjectId"]:
                return None, "package-endpoint-inventory-mismatch", None
            return [{"keyKind": "first-party-package", "path": endpoint["packageManifestPath"]}], None, "package:" + endpoint["packageManifestPath"]
        if endpoint["kind"] == "file":
            if endpoint["nativeSubjectId"] not in self.inventory:
                return None, "file-not-inventoried", None
            keys, cause = self.path_owner_keys(endpoint["universe"], endpoint["nativeSubjectId"])
            return keys, cause, "path:" + endpoint["nativeSubjectId"]
        path, cause = self.symbol_attribution(endpoint["universe"], endpoint["nativeSubjectId"])
        if cause:
            return None, cause, None
        keys, cause = self.path_owner_keys(endpoint["universe"], path)
        return keys, cause, "path:" + path

    def unit_ref(self, unit):
        return {"unitOrdinal": unit["unitOrdinal"], "rootPath": unit["rootPath"], "markerPath": unit["markerPath"], "unitKind": unit["unitKind"],
                "languageFamily": unit["languageFamily"]}

    def owner_record(self, key):
        record = {"ownerKey": owner_key(key), "keyKind": key["keyKind"]}
        if key["keyKind"] == "workspace-unit":
            unit = [u for u in self.units.values() if u["markerPath"] == key["path"] and u["languageFamily"] == "tsjs"]
            need(len(unit) == 1, "J-WORLD-OWNER")
            record["workspaceUnit"] = self.unit_ref(unit[0])
            return record
        record["packageManifestPath"] = key["path"]
        if key["keyKind"] == "external-package":
            record.update(packageName=key["name"], universe=key["universe"])
            return record
        record["packageName"], cause = self.package_row(key["path"])
        need(cause is None, "J-WORLD-OWNER")
        targets = {}
        for own in self.ownership.values():
            for unit in own["units"]:
                if unit["markerPath"] == key["path"] and unit["unitId"] in set(own["selectedUnitIds"]):
                    targets[unit["unitId"]] = {"unitId": unit["unitId"], "markerPath": unit["markerPath"], "targetKind": unit["targetKind"], "targetName": unit["targetName"]}
        record["cargoTargets"] = [targets[k] for k in sorted(targets)]
        units = [u for u in self.units.values() if u["languageFamily"] == "tsjs" and join_root(u["rootPath"], "package.json") == key["path"]]
        record["workspaceUnit"] = self.unit_ref(units[0]) if len(units) == 1 else None
        return record


def owner_key_record(owner):
    if owner["keyKind"] == "workspace-unit":
        return {"keyKind": "workspace-unit", "path": owner["workspaceUnit"]["markerPath"]}
    if owner["keyKind"] == "external-package":
        return {"keyKind": "external-package", "universe": owner["universe"], "path": owner["packageManifestPath"], "name": owner["packageName"]}
    return {"keyKind": "first-party-package", "path": owner["packageManifestPath"]}


def owner_key(key_record):
    return "owner1:" + raw_sha(key_record)


def expand_facts(data):
    facts = copy.deepcopy(data["facts"])
    for fan in data.get("syntheticFanIn", []):
        for i in range(fan["count"]):
            source = dict(fan["sourceTemplate"], nativeSubjectId=fan["sourceTemplate"]["nativeSubjectId"] + "%06d" % i)
            target = fan["target"] if "target" in fan else dict(fan["targetTemplate"], nativeSubjectId=fan["targetTemplate"]["nativeSubjectId"] + "%06d" % i)
            facts.append({"factId": "fact2:" + hashlib.sha256(("fan:%s:%d" % (fan["name"], i)).encode()).hexdigest(), "relation": fan["relation"],
                          "resolution": fan["resolution"], "source": source, "target": target, "targetOccupancy": fan.get("occupancy", "first-party"),
                          "viewDigest": fan["viewDigest"], "anchors": copy.deepcopy(fan["anchors"])})
    return facts


# ---------------------------------------------------------------------------
# query owner successor S3: whole-view internal projection (section 8 steps 1-4 and 7), exposing retained fact anchor paths

def whole_view_projection(world, relation, rung):
    need(world.availability == "retained", "QUERY-EVIDENCE-UNAVAILABLE")
    max_items = (world.test_bounds or {}).get("maxItemsPerOperation", PUBLIC_BOUNDS["maxItemsPerOperation"])
    need(max_items <= PUBLIC_BOUNDS["maxItemsPerOperation"], "J-TEST-BOUNDS", "test bounds may only lower the public caps")
    rel = world.relations.get(relation + "@" + rung)
    if rel is None or not rel["views"]:
        return {"rows": [], "countBasis": "exact", "factViewDigests": [], "coverageIds": [], "limitationKinds": ["native-evidence-unavailable"],
                "deficiencyCitationCount": 0, "maxItemsPerOperation": max_items}
    rows = {}
    for fact in world.facts:
        if fact["relation"] == relation and fact["resolution"] == rung and fact["viewDigest"] in rel["views"]:
            rows.setdefault(fact["factId"], fact)
    ordered = [rows[k] for k in sorted(rows, key=lambda f: f.encode())]
    kinds = {l["kind"] for l in rel["resolutionLimitations"]}
    produced = [dict(f, anchorPaths=sorted({a["path"] for a in f["anchors"]})) for f in ordered[:max_items]]
    if len(ordered) > max_items:
        kinds.add("unexamined-work-bound")
    return {"rows": produced, "countBasis": "lower-bound" if len(ordered) > max_items else "exact", "factViewDigests": ["view2:" + v for v in sorted(rel["views"])],
            "coverageIds": sorted(rel["coverageIds"]), "limitationKinds": sorted(kinds), "deficiencyCitationCount": len(rel["deficiencyCitations"]),
            "maxItemsPerOperation": max_items}


class EvidenceGraphOwner:
    def __init__(self, world):
        self.world, self.calls, self.cache = world, 0, {}

    def owner_for(self, request):
        params = request["params"]
        key = (params["relation"], params["minResolution"], request["projectId"], request["view"]["runId"])
        if key not in self.cache:
            rel = self.world.relations.get(params["relation"] + "@" + params["minResolution"])
            evidence = {"coverageIds": [], "scopeIds": [], "deficiencyCitations": [], "resolutionLimitations": []}
            facts, views = [], []
            if rel is None or not rel["views"]:
                evidence["resolutionLimitations"] = [{"kind": "native-evidence-unavailable", "relation": params["relation"], "minResolution": params["minResolution"]}]
            else:
                views = sorted(rel["views"])
                evidence = {"coverageIds": sorted(rel["coverageIds"]), "scopeIds": sorted(rel["scopeIds"]), "deficiencyCitations": copy.deepcopy(rel["deficiencyCitations"]),
                            "resolutionLimitations": copy.deepcopy(rel["resolutionLimitations"])}
                seen = set()
                for fact in self.world.facts:
                    if fact["relation"] == params["relation"] and fact["resolution"] == params["minResolution"] and fact["viewDigest"] in rel["views"] and fact["factId"] not in seen:
                        seen.add(fact["factId"])
                        facts.append({k: fact[k] for k in ("factId", "relation", "resolution", "source", "target")})
            template = {"projectId": request["projectId"], "resolvedView": {"runId": request["view"]["runId"]}, "factViewDigests": ["view2:" + v for v in views],
                        "availability": "retained", "truncated": False, "totalItems": 0, "countBasis": "exact", "traversalCoverage": "complete",
                        "visitedNodes": 1, "producedItems": 0, "advisory": False, "evidence": evidence}
            self.cache[key] = RM.MockGraphOwner(facts, template, PUBLIC_BOUNDS["maxItemsPerOperation"])
        return self.cache[key]

    def execute(self, request):
        need(self.world.availability == "retained", "QUERY-EVIDENCE-UNAVAILABLE")
        self.calls += 1
        return self.owner_for(request).execute(request)

    def all_items(self, request):
        request = copy.deepcopy(request)
        first = self.execute(request)
        items, response = list(first["items"]), first
        while "nextCursor" in response["context"]:
            request["page"] = {"size": request["page"]["size"], "cursor": response["context"]["nextCursor"]}
            response = self.execute(request)
            items += response["items"]
        return first, items


def query_base(project_id, run_id, operation, params, size):
    return {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": project_id, "view": {"runId": run_id}, "operation": operation,
            "params": params, "completeness": "best-effort", "page": {"size": size}}


def limitation_kinds(context):
    return sorted({l["kind"] for l in context["evidence"]["resolutionLimitations"]})


def has_limitations(context):
    return bool(context["evidence"]["resolutionLimitations"] or context["evidence"]["deficiencyCitations"])


# ---------------------------------------------------------------------------
# RP-DO-03 coupling: full derivation, then byte-bounded projection

def importer_owner_keys(world, row):
    """F9: every retained anchor path of the imports fact is owned under the same selected owners (native section 2.1 keys on the enclosing fact's
    anchor path). Disagreeing anchors refuse attribution instead of choosing one."""
    if not row["anchorPaths"]:
        return None, "importer-anchor-missing"
    found = None
    for path in row["anchorPaths"]:
        keys, cause = world.path_owner_keys(row["source"]["universe"], path)
        if cause:
            return None, cause
        if found is not None and keys != found:
            return None, "importer-anchor-owners-disagree"
        found = keys
    return found, None


def coupling_full(world, key_resolver=None, test_origin_state=None):
    projection = whole_view_projection(world, "imports", "resolved-target")
    cells, importer_buckets, target_buckets, keys, drill = {}, {}, {}, {}, []
    attributed, importer_unattributed, target_unattributed, symbol_outside = set(), set(), set(), set()
    for row in projection["rows"]:
        fact_id, importer, target = row["factId"], row["source"], row["target"]
        from_keys, cause = (key_resolver or importer_owner_keys)(world, row)
        if cause:
            importer_buckets.setdefault(cause, set()).add(fact_id)
            importer_unattributed.add(fact_id)
            continue
        symbol_path, _ = world.symbol_attribution(importer["universe"], importer["nativeSubjectId"])
        if symbol_path is not None and symbol_path not in row["anchorPaths"]:
            symbol_outside.add(fact_id)
        to_keys, cause, target_identity = world.endpoint_owner_keys(target, row["targetOccupancy"])
        if cause:
            for fk in from_keys:
                target_buckets.setdefault((owner_key(fk), cause), set()).add(fact_id)
                keys[owner_key(fk)] = fk
            target_unattributed.add(fact_id)
            continue
        attributed.add(fact_id)
        for fk in from_keys:
            for tk in to_keys:
                keys[owner_key(fk)], keys[owner_key(tk)] = fk, tk
                cell = cells.setdefault((owner_key(fk), owner_key(tk)), {"facts": set(), "edges": set(), "deps": set(), "importers": set(), "sharedImporter": set(),
                                                                        "sharedTarget": set(), "universes": set()})
                cell["facts"].add(fact_id)
                cell["edges"].add((ekey(importer), ekey(target)))
                cell["deps"].add((tuple(row["anchorPaths"]), target_identity))
                cell["importers"].add(ekey(importer))
                cell["universes"].add(importer["universe"])
                if len(from_keys) > 1:
                    cell["sharedImporter"].add(fact_id)
                if len(to_keys) > 1:
                    cell["sharedTarget"].add(fact_id)
                drill.append({"fromOwnerKey": owner_key(fk), "toOwnerKey": owner_key(tk), "factId": fact_id, "importer": importer, "target": target,
                              "importerAnchorPaths": row["anchorPaths"],
                              "importerTestOrigin": test_origin_state(importer) if test_origin_state else "no-test-origin-identity"})

    def record(k):
        if key_resolver is not None and k["keyKind"] == "first-party-package" and world.package_row(k["path"])[1] is not None:
            return {"ownerKey": owner_key(k), "keyKind": "first-party-package", "packageManifestPath": k["path"], "packageName": "guessed", "cargoTargets": [], "workspaceUnit": None}
        return world.owner_record(k)
    cell_rows = [{"fromOwnerKey": f, "toOwnerKey": t, "facts": len(c["facts"]), "programEdges": len(c["edges"]), "sourceDependencies": len(c["deps"]),
                  "importerSymbols": len(c["importers"]), "sharedImporterFacts": len(c["sharedImporter"]), "sharedTargetFacts": len(c["sharedTarget"]),
                  "internal": f == t, "importerUniverses": sorted(c["universes"])} for (f, t), c in cells.items()]
    cell_rows.sort(key=lambda c: (-c["facts"], c["fromOwnerKey"].encode(), c["toOwnerKey"].encode()))
    buckets = [{"fromOwnerKey": k, "cause": cause, "facts": len(ids)} for (k, cause), ids in target_buckets.items()]
    buckets.sort(key=lambda b: (-b["facts"], b["fromOwnerKey"].encode(), b["cause"]))
    drill.sort(key=lambda r: (r["fromOwnerKey"].encode(), r["toOwnerKey"].encode(), r["factId"].encode()))
    return {"projection": projection, "owners": {k: record(v) for k, v in keys.items()}, "cells": cell_rows, "targetBuckets": buckets,
            "importerBuckets": [{"cause": cause, "facts": len(ids)} for cause, ids in sorted(importer_buckets.items())], "drill": drill,
            "totals": {"distinctFacts": len(projection["rows"]), "attributedFacts": len(attributed), "importerUnattributedFacts": len(importer_unattributed),
                       "targetUnattributedFacts": len(target_unattributed), "cellCount": len(cell_rows), "cellFactSum": sum(c["facts"] for c in cell_rows),
                       "targetBucketCount": len(buckets), "ownerCount": len(keys), "importerSymbolPathOutsideAnchors": len(symbol_outside)}}


COUPLING_PROVENANCE = {
    "verifiedInDocument": ["absence-and-blank-cell-meaning-recomputed", "cargo-target-unit-id-recomputed", "cell-count-inequalities", "collection-priority-order",
                           "drilldown-rows-join-listed-cells", "owner-closure-equals-referenced-keys", "owner-key-recomputed-from-owner-record",
                           "projection-counts-join-totals", "run-equals-envelope-run", "totals-partition-distinct-facts"],
    "hostAsserted": ["importer-owner-from-fact-anchor-paths", "internal-whole-view-imports-projection", "omitted-collection-contents",
                     "per-cell-observation-edge-dependency-counts", "target-occupancy-reconciliation", "target-owner-from-retained-membership-or-source-unit-ownership"],
}


def coupling_panel(world, full, kc, kt, kd, deltas):
    listed_cells = full["cells"][:kc]
    listed_buckets = full["targetBuckets"][:kt]
    listed_pairs = {(c["fromOwnerKey"], c["toOwnerKey"]) for c in listed_cells}
    eligible = [r for r in full["drill"] if (r["fromOwnerKey"], r["toOwnerKey"]) in listed_pairs][:MAX_DRILLDOWN]
    referenced = {c["fromOwnerKey"] for c in listed_cells} | {c["toOwnerKey"] for c in listed_cells} | {b["fromOwnerKey"] for b in listed_buckets}
    owners = sorted((full["owners"][k] for k in referenced), key=lambda o: o["ownerKey"].encode())
    drill_cap_total = len([r for r in full["drill"] if (r["fromOwnerKey"], r["toOwnerKey"]) in listed_pairs])
    blockers = set()
    proj = full["projection"]
    if proj["countBasis"] != "exact":
        blockers.add("projection-lower-bound")
    if proj["limitationKinds"] or proj["deficiencyCitationCount"]:
        blockers.add("evidence-limitations")
    if full["importerBuckets"]:
        blockers.add("unattributed-importers")
    if full["targetBuckets"]:
        blockers.add("unattributed-targets")
    if kc < len(full["cells"]):
        blockers.add("cells-omitted")
    if kt < len(full["targetBuckets"]):
        blockers.add("target-buckets-omitted")
    drill_cause = "item-cap" if kd == MAX_DRILLDOWN else "byte-budget"
    return {
        "policy": COUPLING_POLICY, "runId": world.run_id, "relation": "imports", "minResolution": "resolved-target",
        "projection": {k: proj[k] for k in ("countBasis", "factViewDigests", "coverageIds", "limitationKinds", "deficiencyCitationCount")},
        "countUnits": {"facts": "distinct-fact2-observations", "programEdges": "distinct-importer-target-endpoint-pairs-per-universe",
                       "sourceDependencies": "distinct-importer-anchor-paths-and-universe-independent-target-identity"},
        "owners": owners, "ownerClosure": {"total": full["totals"]["ownerCount"], "listed": len(owners), "rule": "owners-referenced-by-listed-cells-and-target-buckets"},
        "cells": listed_cells, "cellsProjection": item_projection(len(full["cells"]), kc, "byte-budget", deltas.get("cells")),
        "importerBuckets": full["importerBuckets"],
        "targetBuckets": listed_buckets, "targetBucketsProjection": item_projection(len(full["targetBuckets"]), kt, "byte-budget", deltas.get("targetBuckets")),
        "totals": full["totals"],
        "absence": {"blankCellMeans": "no-projected-fact" if kc == len(full["cells"]) else "not-determined-cells-omitted", "absenceSupported": not blockers,
                    "blockers": sorted(blockers)},
        "drilldown": eligible[:kd], "drilldownProjection": item_projection(drill_cap_total, kd, drill_cause, deltas.get("drilldown")),
        "provenance": COUPLING_PROVENANCE,
    }


def fit_coupling(world, full, budget):
    """Largest deterministic prefixes (cells, then target buckets, then drilldown) whose panel fits `budget` canonical bytes. Returns None when the
    skeleton itself does not fit (the panel is then omitted/exploration-budget-exceeded)."""
    placeholder = {"cells": PLACEHOLDER_DELTA, "targetBuckets": PLACEHOLDER_DELTA, "drilldown": PLACEHOLDER_DELTA}
    ncells, nbuckets = len(full["cells"]), len(full["targetBuckets"])
    if measure(coupling_panel(world, full, 0, 0, 0, placeholder)) > budget:
        return None

    def largest(limit, build):
        lo, hi = 0, limit
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if measure(build(mid)) <= budget:
                lo = mid
            else:
                hi = mid - 1
        delta = measure(build(lo + 1)) - measure(build(lo)) if lo < limit else None
        return lo, delta
    deltas = {}
    kc, deltas["cells"] = largest(ncells, lambda k: coupling_panel(world, full, k, 0, 0, placeholder))
    kt, deltas["targetBuckets"] = largest(nbuckets, lambda k: coupling_panel(world, full, kc, k, 0, placeholder))
    listed_pairs = {(c["fromOwnerKey"], c["toOwnerKey"]) for c in full["cells"][:kc]}
    ndrill = min(MAX_DRILLDOWN, len([r for r in full["drill"] if (r["fromOwnerKey"], r["toOwnerKey"]) in listed_pairs]))
    kd, deltas["drilldown"] = largest(ndrill, lambda k: coupling_panel(world, full, kc, kt, k, placeholder))
    panel = coupling_panel(world, full, kc, kt, kd, deltas)
    need(measure(panel) <= budget, "J-COUPLING-BUDGET-INTERNAL")
    return panel


def derive_coupling(world, budget=4194304, key_resolver=None, test_origin_state=None):
    return fit_coupling(world, coupling_full(world, key_resolver, test_origin_state), budget)


def admit_coupling(panel, run_id, budget):
    need(panel["runId"] == run_id, "J-COUPLING-RUN")
    need(measure(panel) <= budget, "J-COUPLING-BUDGET")
    owners = {}
    for owner in panel["owners"]:
        need(owner["ownerKey"] == owner_key(owner_key_record(owner)), "J-COUPLING-OWNER-KEY")
        for target in owner.get("cargoTargets", []):
            projection = {"schemaVersion": 1, "markerPath": target["markerPath"], "targetKind": target["targetKind"], "targetName": target["targetName"]}
            need(target["unitId"] == native_h(COMPILATION_UNIT_DOMAIN, projection) and target["markerPath"] == owner["packageManifestPath"], "J-COUPLING-OWNER-KEY")
        owners[owner["ownerKey"]] = owner
    cells = panel["cells"]
    need([(-c["facts"], c["fromOwnerKey"].encode(), c["toOwnerKey"].encode()) for c in cells]
         == sorted((-c["facts"], c["fromOwnerKey"].encode(), c["toOwnerKey"].encode()) for c in cells), "J-COUPLING-ORDER")
    need(len({(c["fromOwnerKey"], c["toOwnerKey"]) for c in cells}) == len(cells), "J-COUPLING-ORDER")
    buckets = panel["targetBuckets"]
    need([(-b["facts"], b["fromOwnerKey"].encode(), b["cause"]) for b in buckets] == sorted((-b["facts"], b["fromOwnerKey"].encode(), b["cause"]) for b in buckets), "J-COUPLING-ORDER")
    cell_map = {}
    for cell in cells:
        need(cell["fromOwnerKey"] in owners and cell["toOwnerKey"] in owners, "J-COUPLING-CELL")
        need(owners[cell["fromOwnerKey"]]["keyKind"] != "external-package", "J-COUPLING-CELL")
        need(cell["facts"] >= cell["programEdges"] >= 1 and cell["programEdges"] >= cell["importerSymbols"] >= 1 and cell["facts"] >= cell["sourceDependencies"] >= 1
             and cell["sharedImporterFacts"] <= cell["facts"] and cell["sharedTargetFacts"] <= cell["facts"] and len(cell["importerUniverses"]) <= cell["programEdges"]
             and cell["internal"] == (cell["fromOwnerKey"] == cell["toOwnerKey"]), "J-COUPLING-COUNT")
        cell_map[(cell["fromOwnerKey"], cell["toOwnerKey"])] = cell
    for bucket in buckets:
        need(bucket["fromOwnerKey"] in owners and bucket["facts"] >= 1, "J-COUPLING-BUCKET")
    need(all(b["facts"] >= 1 for b in panel["importerBuckets"]), "J-COUPLING-BUCKET")
    referenced = {c["fromOwnerKey"] for c in cells} | {c["toOwnerKey"] for c in cells} | {b["fromOwnerKey"] for b in buckets}
    need(set(owners) == referenced and panel["ownerClosure"]["listed"] == len(owners) <= panel["ownerClosure"]["total"], "J-COUPLING-OWNER-CLOSURE")
    totals = panel["totals"]
    need(totals["distinctFacts"] == totals["attributedFacts"] + totals["importerUnattributedFacts"] + totals["targetUnattributedFacts"], "J-COUPLING-TOTALS")
    need(totals["importerUnattributedFacts"] == sum(b["facts"] for b in panel["importerBuckets"]), "J-COUPLING-TOTALS")
    need(totals["importerSymbolPathOutsideAnchors"] <= totals["distinctFacts"], "J-COUPLING-TOTALS")
    cp, bp, dp = panel["cellsProjection"], panel["targetBucketsProjection"], panel["drilldownProjection"]
    need(cp["total"] == totals["cellCount"] and cp["total"] - cp["omitted"] == len(cells), "J-COUPLING-PROJECTION")
    need(bp["total"] == totals["targetBucketCount"] and bp["total"] - bp["omitted"] == len(buckets), "J-COUPLING-PROJECTION")
    need((totals["targetUnattributedFacts"] == 0) == (totals["targetBucketCount"] == 0), "J-COUPLING-TOTALS")
    if cp["omitted"] == 0:
        need(totals["cellFactSum"] == sum(c["facts"] for c in cells) and max([c["facts"] for c in cells] + [0]) <= totals["attributedFacts"] <= totals["cellFactSum"], "J-COUPLING-TOTALS")
    else:
        need(sum(c["facts"] for c in cells) < totals["cellFactSum"] and all(c["facts"] >= 1 for c in cells), "J-COUPLING-PROJECTION")
    if bp["omitted"] == 0:
        need(totals["targetUnattributedFacts"] <= sum(b["facts"] for b in buckets), "J-COUPLING-TOTALS")
    blockers = set()
    if panel["projection"]["countBasis"] != "exact":
        blockers.add("projection-lower-bound")
    if panel["projection"]["limitationKinds"] or panel["projection"]["deficiencyCitationCount"]:
        blockers.add("evidence-limitations")
    if panel["importerBuckets"]:
        blockers.add("unattributed-importers")
    if totals["targetBucketCount"]:
        blockers.add("unattributed-targets")
    if cp["omitted"]:
        blockers.add("cells-omitted")
    if bp["omitted"]:
        blockers.add("target-buckets-omitted")
    need(panel["absence"]["blockers"] == sorted(blockers) and panel["absence"]["absenceSupported"] == (not blockers)
         and panel["absence"]["blankCellMeans"] == ("no-projected-fact" if cp["omitted"] == 0 else "not-determined-cells-omitted"), "J-COUPLING-ABSENCE")
    per_cell = {}
    for row in panel["drilldown"]:
        cell = cell_map.get((row["fromOwnerKey"], row["toOwnerKey"]))
        need(cell is not None and row["importer"]["universe"] in cell["importerUniverses"], "J-COUPLING-DRILL")
        per_cell[(row["fromOwnerKey"], row["toOwnerKey"])] = per_cell.get((row["fromOwnerKey"], row["toOwnerKey"]), 0) + 1
    need(all(n <= cell_map[k]["facts"] for k, n in per_cell.items()), "J-COUPLING-DRILL")
    keys = [(r["fromOwnerKey"].encode(), r["toOwnerKey"].encode(), r["factId"].encode()) for r in panel["drilldown"]]
    need(keys == sorted(keys) and len(set(keys)) == len(keys), "J-COUPLING-DRILL")
    need(dp["total"] == sum(c["facts"] for c in cells) and dp["total"] - dp["omitted"] == len(panel["drilldown"]), "J-COUPLING-DRILL")


# ---------------------------------------------------------------------------
# RP-DO-09 symbol metrics

def metric_spec(metric_id):
    spec = [m for m in METRIC_CATALOG if m[0] == metric_id]
    need(len(spec) == 1, "J-METRIC-CATALOG")
    return spec[0]


def metric_request(project_id, run_id, metric_id, endpoint):
    _, operation, relation, rung, direction, depth = metric_spec(metric_id)
    if operation == "graph.neighbors":
        params = {"relation": relation, "minResolution": rung, "direction": direction, "endpoint": copy.deepcopy(endpoint)}
    else:
        params = {"relation": relation, "minResolution": rung, "direction": direction, "start": copy.deepcopy(endpoint), "maxDepth": depth, "includeStart": False}
    return query_base(project_id, run_id, operation, params, 1)


def metric_reading(context):
    kinds = limitation_kinds(context)
    if "native-evidence-unavailable" in kinds:
        return {"countState": "unknown", "cause": "native-evidence-unavailable"}
    state = "exact" if context["countBasis"] == "exact" else "lower-bound"
    return {"countState": state, "value": context["totalItems"], "limitationKinds": kinds,
            "zeroSupportsAbsence": state == "exact" and context["totalItems"] == 0 and not has_limitations(context)}


def metric_rows(world, owner, resolution):
    rows = []
    for subject in resolution:
        if subject["state"] == "descriptor-not-retained":
            rows += [{"subjectId": subject["subjectId"], "metricId": m, "countState": "unknown", "cause": "subject-descriptor-not-retained"} for m in METRIC_IDS]
            continue
        if subject["endpoint"]["kind"] != "symbol":
            continue
        for metric_id in METRIC_IDS:
            request = metric_request(world.project_id, world.run_id, metric_id, subject["endpoint"])
            response = owner.execute(request)
            row = {"subjectId": subject["subjectId"], "metricId": metric_id, "interpretation": "static-projected-count", "request": request, "response": response}
            row.update(metric_reading(response["context"]))
            rows.append(row)
    rows.sort(key=lambda r: (r["subjectId"].encode(), r["metricId"].encode()))
    return rows


def derive_metrics(world, owner, resolution, byte_budget):
    return byte_prefix(metric_rows(world, owner, resolution), byte_budget)


def page_ok(response, request, bounds):
    return RM.page_law(response["context"], len(response["items"]), request["page"]["size"], bounds) is None


def rows_match(request, response):
    params = request["params"]
    for item in response["items"]:
        if request["operation"] == "graph.neighbors":
            anchor = ekey(params["endpoint"])
            incident = (params["direction"] in ("outgoing", "both") and ekey(item["source"]) == anchor) or (params["direction"] in ("incoming", "both") and ekey(item["target"]) == anchor)
            if not (incident and item["relation"] == params["relation"] and item["resolution"] == params["minResolution"]):
                return False
        elif request["operation"] == "graph.reach":
            if not 1 <= item["depth"] <= params["maxDepth"]:
                return False
        else:
            if not (ekey(item["start"]) == ekey(params["start"]) and ekey(item["target"]) == ekey(params["target"]) and item["hopCount"] == len(item["edges"])
                    and len(item["nodes"]) == len(item["edges"]) + 1 and item["hopCount"] <= params["maxDepth"]
                    and all(ekey(e["source"]) == ekey(item["nodes"][i]) and ekey(e["target"]) == ekey(item["nodes"][i + 1]) for i, e in enumerate(item["edges"]))):
                return False
    return True


def exchange_ok(exchange_request, response, project_id, run_id, bounds, code_prefix):
    context = response["context"]
    need(context["projectId"] == project_id and context["resolvedView"] == {"runId": run_id} and response["operation"] == exchange_request["operation"], code_prefix + "-RUN")
    need(page_ok(response, exchange_request, bounds), code_prefix + "-PAGE")
    need(rows_match(exchange_request, response), code_prefix + "-ROWS")


def admit_symbol_metrics(metrics, projection, ctx):
    resolution = {s["subjectId"]: s for s in ctx["resolution"]}
    expected = sum(len(METRIC_IDS) for s in ctx["resolution"] if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol")
    need(projection["total"] == expected and projection["total"] - projection["omitted"] == len(metrics), "J-METRIC-TOTALITY")
    for row in metrics:
        subject = resolution.get(row["subjectId"])
        need(subject is not None, "J-METRIC-SUBJECT")
        if row["countState"] == "unknown" and row["cause"] == "subject-descriptor-not-retained":
            need(subject["state"] == "descriptor-not-retained", "J-METRIC-SUBJECT")
            continue
        need(subject["state"] == "resolved" and subject["endpoint"]["kind"] == "symbol", "J-METRIC-SUBJECT")
        need(row["request"] == metric_request(ctx["projectId"], ctx["runId"], row["metricId"], subject["endpoint"]), "J-METRIC-REQUEST")
        exchange_ok(row["request"], row["response"], ctx["projectId"], ctx["runId"], ctx["bounds"], "J-METRIC")
        reading = metric_reading(row["response"]["context"])
        need(row["countState"] == reading["countState"], "J-METRIC-STATE")
        if reading["countState"] == "unknown":
            need(row["cause"] == reading["cause"], "J-METRIC-STATE")
            continue
        need(row["value"] == reading["value"] and row["limitationKinds"] == reading["limitationKinds"], "J-METRIC-VALUE")
        need(row["zeroSupportsAbsence"] == reading["zeroSupportsAbsence"], "J-METRIC-ABSENCE")


# ---------------------------------------------------------------------------
# RP-DO-05 recognition parameter, Cargo target entries and traces

def admit_recognition_plan(world, plan):
    need(plan["snapshotId"] == world.snapshot_id, "J-FRP-SNAPSHOT")
    need(plan["membershipDigest"] == raw_sha(world.membership) == world.plan["membershipDigest"], "J-FRP-MEMBERSHIP")
    need(plan["explicitEntryPoints"] == sorted(set(world.config_entry_points), key=lambda p: canon(p)), "J-FRP-EXPLICIT")
    need(all(p in world.inventory for p in plan["explicitEntryPoints"]), "J-FRP-ENTRY")
    ordinals = [row["unitOrdinal"] for row in plan["units"]]
    need(ordinals == sorted(set(ordinals)), "J-FRP-ORDER")
    need(set(ordinals) == {u["unitOrdinal"] for u in world.units.values() if u["languageFamily"] in ("rust", "tsjs")}, "J-FRP-UNIT-TOTALITY")
    for row in plan["units"]:
        unit = world.units[row["unitOrdinal"]]
        need(unit["rootPath"] == row["rootPath"] and unit["markerPath"] == row["markerPath"], "J-FRP-UNIT")
        need(row["recognitionId"] == native_h(RECOGNITION_DOMAIN, row["recognition"]), "J-FRP-ID")
        entries = 0
        for result in row["recognition"]["recognized"]:
            for evidence in result["evidence"]:
                need(evidence["path"] in world.inventory and world.inventory[evidence["path"]]["sha256"] == evidence["contentSha256"], "J-FRP-EVIDENCE")
            need(all(p in world.inventory for p in result["effects"]["entryPoints"]), "J-FRP-ENTRY")
            entries += len(result["effects"]["entryPoints"])
        need(entries <= 65536, "J-FRP-BOUNDS")
        need(row["recognition"]["entryPoints"] == recognition_summary(row["recognition"]["recognized"], plan["explicitEntryPoints"]), "J-FRP-SUMMARY")


def cargo_target_entries(world, universe):
    """F4: every SELECTED bin/lib compilation target of a Rust universe, with its crate root = the unique retained crateRootPaths member that the
    target owns (SourceUnitOwnershipV1 row path == root). Unresolved or ambiguous roots and partial enumeration are exact missing coverage."""
    inputs, own = world.rust_universes.get(universe), world.ownership.get(universe)
    base = {"universe": universe}
    if inputs is None or own is None:
        return dict(base, state="unknown", sourceUnitOwnershipId=None, targets=[], missingCoverage=["ownership-enumeration-partial"])
    roots = set(inputs["crateRootPaths"])
    selected = set(own["selectedUnitIds"])
    missing, targets = set(), []
    if own["enumeration"] != "complete":
        missing.add("ownership-enumeration-partial")
    for unit in own["units"]:
        if unit["unitId"] not in selected or unit["targetKind"] not in ENTRY_TARGET_KINDS:
            continue
        owned = sorted({r["path"] for r in own["ownership"] if r["unitId"] == unit["unitId"] and r["path"] in roots})
        if len(owned) != 1:
            missing.add("target-crate-root-unresolved" if not owned else "target-crate-root-ambiguous")
        targets.append({"unitId": unit["unitId"], "markerPath": unit["markerPath"], "targetKind": unit["targetKind"], "targetName": unit["targetName"],
                        "crateRootPath": owned[0] if len(owned) == 1 else None})
    state = "none" if not targets else ("partial" if missing else "all")
    return dict(base, state=state, sourceUnitOwnershipId=inputs["sourceUnitOwnershipId"], targets=targets, missingCoverage=sorted(missing))


def effective_entries(world, universe):
    record = world.recognition_record()
    if record["explicitEntryPoints"]:
        return {p: [{"source": "explicit"}] for p in record["explicitEntryPoints"]}
    out = {}
    if world.family(universe) == "rust":
        for target in cargo_target_entries(world, universe)["targets"]:
            if target["crateRootPath"] is not None:
                out.setdefault(target["crateRootPath"], []).append({"source": "cargo-target", "unitId": target["unitId"], "targetKind": target["targetKind"],
                                                                    "targetName": target["targetName"], "markerPath": target["markerPath"]})
    unit = world.unit_for_universe(universe)
    row = [r for r in record["units"] if unit is not None and r["unitOrdinal"] == unit["unitOrdinal"]]
    for result in (row[0]["recognition"]["recognized"] if row else []):
        for path in result["effects"]["entryPoints"]:
            out.setdefault(path, []).append({"source": "recognized", "unitOrdinal": unit["unitOrdinal"], "recognizerId": result["recognizerId"],
                                             "recognizerVersion": result["recognizerVersion"], "assurance": result["assurance"],
                                             "evidence": copy.deepcopy(result["evidence"]), "unresolvedChoices": list(result["unresolvedChoices"])})
    return out


def scope_state(world, universe):
    record = world.recognition_record()
    if record["explicitEntryPoints"]:
        return "all"
    if world.family(universe) == "rust":
        return cargo_target_entries(world, universe)["state"]
    unit = world.unit_for_universe(universe)
    row = [r for r in record["units"] if unit is not None and r["unitOrdinal"] == unit["unitOrdinal"]]
    return row[0]["recognition"]["entryPoints"]["state"] if row else "none"


def entry_recognition_panel(world):
    custody = world.custody()
    if custody["state"] != "plan-bound":
        return custody
    record = world.recognition_record()
    units = []
    for row in record["units"]:
        recognized = row["recognition"]["recognized"]
        distinct = {p for r in recognized for p in r["effects"]["entryPoints"]}
        units.append({"unitOrdinal": row["unitOrdinal"], "rootPath": row["rootPath"], "markerPath": row["markerPath"], "recognitionId": row["recognitionId"],
                      "entryPoints": row["recognition"]["entryPoints"],
                      "effectiveSource": "explicit" if record["explicitEntryPoints"] else ("recognized" if distinct else "none"),
                      "effectiveEntryPointCount": len(record["explicitEntryPoints"]) if record["explicitEntryPoints"] else len(distinct),
                      "recognizers": [{"recognizerId": r["recognizerId"], "recognizerVersion": r["recognizerVersion"], "assurance": r["assurance"],
                                       "evidence": copy.deepcopy(r["evidence"]), "unresolvedChoices": list(r["unresolvedChoices"]),
                                       "entryPointCount": len(r["effects"]["entryPoints"]), "testGlobs": list(r["effects"]["testGlobs"])} for r in recognized]})
    cargo = [cargo_target_entries(world, u) for u in sorted(world.rust_universes)]
    return dict(custody, explicitEntryPointCount=len(record["explicitEntryPoints"]), units=units, cargoTargetEntries=cargo)


def origin_request(world, endpoint):
    return query_base(world.project_id, world.run_id, "graph.neighbors",
                      {"relation": "reachability", "minResolution": "from-resolved-calls", "direction": "incoming", "endpoint": copy.deepcopy(endpoint)}, ORIGIN_PAGE_SIZE)


def trace_path_request(project_id, run_id, start, target):
    return query_base(project_id, run_id, "graph.path", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing",
                                                         "start": copy.deepcopy(start), "target": copy.deepcopy(target), "maxDepth": TRACE_MAX_DEPTH}, 1)


def derive_trace(world, owner, subject, start_resolver=None):
    base = {"subjectId": subject["subjectId"]}
    if subject["state"] == "descriptor-not-retained":
        return dict(base, state="unknown", cause="subject-descriptor-not-retained")
    custody = world.custody()
    if custody["state"] == "not-plan-bound":
        return dict(base, state="unknown", cause="recognition-not-plan-bound")
    if custody["state"] == "unavailable":
        return dict(base, state="unknown", cause="recognition-unavailable")
    target = subject["endpoint"]
    unit = world.unit_for_universe(target["universe"])
    base["scopeUniverse"] = target["universe"]
    base["scopeUnitOrdinal"] = unit["unitOrdinal"] if unit else None
    request = origin_request(world, target)
    response = owner.execute(request)
    context = response["context"]
    origin_query = {"request": request, "response": response}
    if "native-evidence-unavailable" in limitation_kinds(context):
        return dict(base, state="unknown", cause="reachability-evidence-unavailable", originQuery=origin_query)
    candidates, unattributed, outside, scopes_not_all = [], 0, 0, False
    for item in response["items"]:
        origin = item["source"]
        if start_resolver is not None:
            found = start_resolver(world, origin)
        else:
            path, cause = world.symbol_attribution(origin["universe"], origin["nativeSubjectId"])
            if cause:
                unattributed += 1
                continue
            entries = effective_entries(world, origin["universe"])
            found = (path, entries[path]) if path in entries else None
        if found is None:
            outside += 1
            scopes_not_all |= scope_state(world, origin["universe"]) != "all"
            continue
        candidates.append((item, found))
    if not candidates:
        if "nextCursor" in context:
            return dict(base, state="unknown", cause="origin-page-set-not-embedded", originQuery=origin_query)
        blockers = set()
        if has_limitations(context):
            blockers.add("evidence-limitations")
        if unattributed:
            blockers.add("origin-attribution-unavailable")
        if scope_state(world, target["universe"]) != "all" or scopes_not_all:
            blockers.add("entry-recognition-not-all")
        origin_universes = sorted({i["source"]["universe"] for i in response["items"]})
        return dict(base, state="no-entry-origin", originQuery=origin_query, originsExamined=len(response["items"]), originsUnattributed=unattributed,
                    originsOutsideEntrySet=outside, originUniverses=origin_universes, blockers=sorted(blockers),
                    interpretation="no-entry-origin-among-projected-reachability-origins-not-dead-code")
    item, (path, provenance) = candidates[0]
    start = {"endpoint": item["source"], "viaReachabilityFactId": item["factId"], "attributionPath": path, "entry": {"path": path, "provenance": provenance}}
    path_request = trace_path_request(world.project_id, world.run_id, item["source"], target)
    path_response = owner.execute(path_request)
    state = "path-found" if path_response["items"] else "path-not-within-bound"
    return dict(base, state=state, originQuery=origin_query, start=start, path={"request": path_request, "response": path_response})


def derive_traces(world, owner, resolution, start_resolver=None):
    chosen = [s for s in resolution if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol"]
    traces = sorted((derive_trace(world, owner, s, start_resolver) for s in chosen[:MAX_TRACES]), key=lambda t: t["subjectId"].encode())
    return traces, item_projection(len(chosen), min(len(chosen), MAX_TRACES), "item-cap")


def admit_entry_recognition(panel):
    if panel["state"] != "plan-bound":
        return
    ordinals = [u["unitOrdinal"] for u in panel["units"]]
    need(ordinals == sorted(set(ordinals)), "J-ENTRY-ORDER")
    for unit in panel["units"]:
        pseudo = [{"effects": {"entryPoints": ["x"] * r["entryPointCount"]}, "unresolvedChoices": r["unresolvedChoices"]} for r in unit["recognizers"]]
        need(unit["entryPoints"] == recognition_summary(pseudo, ["x"] * panel["explicitEntryPointCount"]), "J-ENTRY-SUMMARY")
        need(unit["effectiveSource"] == ("explicit" if panel["explicitEntryPointCount"] else ("recognized" if any(r["entryPointCount"] for r in unit["recognizers"]) else "none")), "J-ENTRY-SUMMARY")
        if panel["explicitEntryPointCount"]:
            need(unit["effectiveEntryPointCount"] == panel["explicitEntryPointCount"], "J-ENTRY-SUMMARY")
        else:
            counts = [r["entryPointCount"] for r in unit["recognizers"]]
            need(max(counts + [0]) <= unit["effectiveEntryPointCount"] <= sum(counts), "J-ENTRY-SUMMARY")
    universes = [c["universe"] for c in panel["cargoTargetEntries"]]
    need(universes == sorted(set(universes)), "J-ENTRY-ORDER")
    for cargo in panel["cargoTargetEntries"]:
        missing = set()
        for target in cargo["targets"]:
            projection = {"schemaVersion": 1, "markerPath": target["markerPath"], "targetKind": target["targetKind"], "targetName": target["targetName"]}
            need(target["unitId"] == native_h(COMPILATION_UNIT_DOMAIN, projection) and target["targetKind"] in ENTRY_TARGET_KINDS, "J-ENTRY-CARGO")
            if target["crateRootPath"] is None:
                need(bool({"target-crate-root-unresolved", "target-crate-root-ambiguous"} & set(cargo["missingCoverage"])), "J-ENTRY-CARGO")
        if cargo["state"] == "unknown":
            need(not cargo["targets"], "J-ENTRY-CARGO")
            continue
        unresolved = any(t["crateRootPath"] is None for t in cargo["targets"])
        need(unresolved == bool({"target-crate-root-unresolved", "target-crate-root-ambiguous"} & set(cargo["missingCoverage"])), "J-ENTRY-CARGO")
        expected = "none" if not cargo["targets"] else ("partial" if cargo["missingCoverage"] else "all")
        need(cargo["state"] == expected, "J-ENTRY-CARGO")


def panel_scope_state(recognition, universe, unit_ordinal):
    if recognition["explicitEntryPointCount"]:
        return "all"
    cargo = {c["universe"]: c for c in recognition["cargoTargetEntries"]}
    if universe in cargo:
        return cargo[universe]["state"]
    units = {u["unitOrdinal"]: u for u in recognition["units"]}
    return units[unit_ordinal]["entryPoints"]["state"] if unit_ordinal in units else "none"


def admit_traces(traces, projection, recognition, ctx):
    resolution = {s["subjectId"]: s for s in ctx["resolution"]}
    chosen = [s for s in ctx["resolution"] if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol"]
    need(projection == item_projection(len(chosen), min(len(chosen), MAX_TRACES), "item-cap")
         and [t["subjectId"] for t in traces] == sorted((s["subjectId"] for s in chosen[:MAX_TRACES]), key=lambda x: x.encode()), "J-TRACE-TOTALITY")
    units = {u["unitOrdinal"]: u for u in recognition.get("units", [])}
    cargo = {c["universe"]: c for c in recognition.get("cargoTargetEntries", [])}
    for trace in traces:
        subject = resolution[trace["subjectId"]]
        if trace["state"] == "unknown" and trace["cause"] == "subject-descriptor-not-retained":
            need(subject["state"] == "descriptor-not-retained", "J-TRACE-SUBJECT")
            continue
        need(subject["state"] == "resolved" and subject["endpoint"]["kind"] == "symbol", "J-TRACE-SUBJECT")
        expected_cause = {"not-plan-bound": "recognition-not-plan-bound", "unavailable": "recognition-unavailable"}.get(recognition["state"])
        if expected_cause:
            need(trace["state"] == "unknown" and trace["cause"] == expected_cause, "J-TRACE-AVAILABILITY")
            continue
        need(not (trace["state"] == "unknown" and trace["cause"] in ("recognition-not-plan-bound", "recognition-unavailable")), "J-TRACE-AVAILABILITY")
        need(trace["scopeUniverse"] == subject["endpoint"]["universe"], "J-TRACE-SUBJECT")
        request = trace["originQuery"]["request"]
        need(request == query_base(ctx["projectId"], ctx["runId"], "graph.neighbors", {"relation": "reachability", "minResolution": "from-resolved-calls",
                                                                                     "direction": "incoming", "endpoint": subject["endpoint"]}, ORIGIN_PAGE_SIZE), "J-TRACE-REQUEST")
        response = trace["originQuery"]["response"]
        exchange_ok(request, response, ctx["projectId"], ctx["runId"], ctx["bounds"], "J-TRACE")
        kinds = limitation_kinds(response["context"])
        if trace["state"] == "unknown":
            if trace["cause"] == "reachability-evidence-unavailable":
                need("native-evidence-unavailable" in kinds, "J-TRACE-STATE")
            else:
                need("nextCursor" in response["context"], "J-TRACE-STATE")
            continue
        need("native-evidence-unavailable" not in kinds, "J-TRACE-STATE")
        if trace["state"] == "no-entry-origin":
            need("nextCursor" not in response["context"] and trace["originsExamined"] == len(response["items"])
                 and trace["originsUnattributed"] + trace["originsOutsideEntrySet"] == trace["originsExamined"]
                 and trace["originUniverses"] == sorted({i["source"]["universe"] for i in response["items"]}), "J-TRACE-STATE")
            blockers = set()
            if has_limitations(response["context"]):
                blockers.add("evidence-limitations")
            if trace["originsUnattributed"]:
                blockers.add("origin-attribution-unavailable")
            if panel_scope_state(recognition, subject["endpoint"]["universe"], trace["scopeUnitOrdinal"]) != "all":
                blockers.add("entry-recognition-not-all")
            if trace["originsOutsideEntrySet"] and not recognition["explicitEntryPointCount"]:
                for universe in trace["originUniverses"]:
                    if universe != subject["endpoint"]["universe"] and universe not in cargo:
                        blockers.add("entry-recognition-not-all")
                    elif universe in cargo and cargo[universe]["state"] != "all":
                        blockers.add("entry-recognition-not-all")
            need(set(trace["blockers"]) >= blockers and set(trace["blockers"]) <= set(TRACE_BLOCKERS), "J-TRACE-BLOCKERS")
            continue
        start = trace["start"]
        rows = [i for i in response["items"] if i["factId"] == start["viaReachabilityFactId"]]
        need(len(rows) == 1 and ekey(rows[0]["source"]) == ekey(start["endpoint"]), "J-TRACE-START")
        entry = start["entry"]
        need(entry["path"] == start["attributionPath"], "J-TRACE-ENTRY")
        for prov in entry["provenance"]:
            if prov["source"] == "explicit":
                need(recognition["explicitEntryPointCount"] > 0, "J-TRACE-ENTRY")
                continue
            need(recognition["explicitEntryPointCount"] == 0, "J-TRACE-ENTRY", "explicit configuration replaces other entry points")
            if prov["source"] == "cargo-target":
                rows_ = cargo.get(start["endpoint"]["universe"], {}).get("targets", [])
                need(any(t["unitId"] == prov["unitId"] and t["crateRootPath"] == entry["path"] and t["targetKind"] == prov["targetKind"] for t in rows_), "J-TRACE-ENTRY")
            else:
                unit = units.get(prov["unitOrdinal"])
                need(unit is not None and any(r["recognizerId"] == prov["recognizerId"] and r["entryPointCount"] > 0 and r["evidence"] == prov["evidence"]
                                              and r["assurance"] == prov["assurance"] and r["unresolvedChoices"] == prov["unresolvedChoices"] for r in unit["recognizers"]),
                     "J-TRACE-ENTRY")
        path_request = trace["path"]["request"]
        need(path_request == trace_path_request(ctx["projectId"], ctx["runId"], start["endpoint"], subject["endpoint"]), "J-TRACE-REQUEST")
        exchange_ok(path_request, trace["path"]["response"], ctx["projectId"], ctx["runId"], ctx["bounds"], "J-TRACE")
        need((trace["state"] == "path-found") == bool(trace["path"]["response"]["items"]), "J-TRACE-PATH")


# ---------------------------------------------------------------------------
# RP-DO-10 test origins and static test reachability

def derive_test_origins(world, universe, name_resolver=None):
    family = world.family(universe)
    base = {"universe": universe, "interpretation": "native-static-origin-identity-not-imported-execution"}
    if family is None:
        return dict(base, source="none", completeness="none", cause="universe-not-plan-bound", limitations=[], originCount=0), {}
    limitations, origins = set(), {}
    inventories = world.symbol_rows(universe)
    if any(inv["state"] != "complete" for inv in inventories) or not inventories:
        limitations.add("symbol-inventory-incomplete")
    by_symbol = {}
    for inv in inventories:
        for row in inv["rows"]:
            by_symbol.setdefault(row["nativeSubjectId"], set()).add(row["path"])
    if name_resolver is not None:
        return name_resolver(world, universe, by_symbol)
    if family == "rust":
        record = world.ownership.get(universe)
        if record is None:
            return dict(base, source="none", completeness="none", cause="ownership-missing", limitations=[], originCount=0), {}
        limitations.add("in-target-unit-tests-not-identified")
        if record["enumeration"] != "complete":
            limitations.add("ownership-enumeration-partial")
        units = {u["unitId"]: u for u in record["units"]}
        selected = set(record["selectedUnitIds"])
        tests = sorted(u for u in selected if units[u]["targetKind"] == "test")
        if not tests:
            limitations.add("no-selected-test-targets")
        owners = {}
        for row in record["ownership"]:
            if row["unitId"] in selected:
                owners.setdefault(row["path"], set()).add(row["unitId"])
        for sid, paths in sorted(by_symbol.items()):
            if len(paths) != 1:
                limitations.add("symbol-attribution-conflict")
                continue
            path = next(iter(paths))
            owning = owners.get(path, set())
            if owning and all(units[u]["targetKind"] == "test" for u in owning):
                origins[sid] = {"attributionPath": path, "originEvidence": {"kind": "rust-test-target", "unitIds": sorted(owning)}}
            elif any(units[u]["targetKind"] == "test" for u in owning):
                limitations.add("shared-test-and-non-test-target-path")
        evidence = {"testTargets": [{"unitId": u, "markerPath": units[u]["markerPath"], "targetKind": "test", "targetName": units[u]["targetName"]} for u in tests]}
        return dict(base, source="rust-test-targets", completeness="partial", limitations=sorted(limitations), originCount=len(origins), evidence=evidence), origins
    if family != "tsjs":
        return dict(base, source="none", completeness="none", cause="unsupported-language-family", limitations=[], originCount=0), {}
    custody = world.custody()
    if custody["state"] != "plan-bound":
        cause = "recognition-not-plan-bound" if custody["state"] == "not-plan-bound" else "recognition-unavailable"
        return dict(base, source="none", completeness="none", cause=cause, limitations=[], originCount=0), {}
    unit = world.unit_for_universe(universe)
    rows = [r for r in world.recognition_record()["units"] if unit and r["unitOrdinal"] == unit["unitOrdinal"]]
    recognizers = [r for r in (rows[0]["recognition"]["recognized"] if rows else []) if r["recognizerId"] == "vitest-jest"]
    if not recognizers:
        return dict(base, source="none", completeness="none", cause="no-test-recognizer", limitations=[], originCount=0), {}
    limitations.add("recognizer-globs-not-test-population")
    choices = {c for r in recognizers for c in r["unresolvedChoices"]}
    if "test-selection-configured" in choices:
        limitations.add("test-selection-configured")
    if choices - {"test-selection-configured"}:
        limitations.add("recognizer-unresolved-choices")
    globs = sorted({g for r in recognizers for g in r["effects"]["testGlobs"]})
    for sid, paths in sorted(by_symbol.items()):
        if len(paths) != 1:
            limitations.add("symbol-attribution-conflict")
            continue
        path = next(iter(paths))
        member = world.member_rows.get(path)
        if member is None or member["unitOrdinal"] != unit["unitOrdinal"]:
            limitations.add("foreign-unit-paths-not-matched")
            continue
        need(unit["rootPath"] == "" or path.startswith(unit["rootPath"] + "/"), "J-TR-SLICE")
        relative = path if unit["rootPath"] == "" else path[len(unit["rootPath"]) + 1:]
        matched = [g for g in globs if glob_match(g, relative)]
        if matched:
            origins[sid] = {"attributionPath": path, "originEvidence": {"kind": "recognized-test-glob", "unitOrdinal": unit["unitOrdinal"], "recognizerId": "vitest-jest",
                                                                         "glob": matched[0], "relativePath": relative}}
    evidence = {"unitOrdinal": unit["unitOrdinal"], "rootPath": unit["rootPath"], "markerPath": unit["markerPath"], "recognitionId": rows[0]["recognitionId"],
                "recognizers": [{"recognizerId": r["recognizerId"], "testGlobs": list(r["effects"]["testGlobs"]), "unresolvedChoices": list(r["unresolvedChoices"]),
                                 "evidence": copy.deepcopy(r["evidence"])} for r in recognizers]}
    return dict(base, source="recognized-test-globs", completeness="partial", limitations=sorted(limitations), originCount=len(origins), evidence=evidence), origins


def reach_request(project_id, run_id, endpoint, size):
    return query_base(project_id, run_id, "graph.reach", {"relation": "calls", "minResolution": "resolved-callee", "direction": "incoming",
                                                          "start": copy.deepcopy(endpoint), "maxDepth": TEST_REACH_MAX_DEPTH, "includeStart": False}, size)


def witness_request(project_id, run_id, start, target):
    return query_base(project_id, run_id, "graph.path", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing",
                                                         "start": copy.deepcopy(start), "target": copy.deepcopy(target), "maxDepth": TEST_REACH_MAX_DEPTH}, 1)


def test_blockers(context, sets, universes, embedded):
    """No origin set is ever complete, so test-origin-set-partial is always present: no absence-style test state exists."""
    blockers = {"test-origin-set-partial"}
    if context["countBasis"] != "exact":
        blockers.add("reach-lower-bound")
    if has_limitations(context):
        blockers.add("evidence-limitations")
    for universe in universes:
        if universe not in embedded:
            blockers.add("origin-sets-not-embedded")
        elif sets[universe]["completeness"] == "none":
            blockers.add("reached-universe-without-test-origin-identity")
    return sorted(blockers)


def derive_test_reachability(world, owner, resolution, name_resolver=None):
    sets, origin_maps, pending = {}, {}, []

    def origin_set(universe):
        if universe not in sets:
            sets[universe], origin_maps[universe] = derive_test_origins(world, universe, name_resolver)
        return sets[universe]
    chosen = [s for s in resolution if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol"][:MAX_TEST_REACHABILITY]
    for subject in chosen:
        if subject["state"] == "descriptor-not-retained":
            pending.append((subject, None, None))
            continue
        target = subject["endpoint"]
        origin_set(target["universe"])
        if target["nativeSubjectId"] in origin_maps[target["universe"]]:
            pending.append((subject, "origin", None))
            continue
        request = reach_request(world.project_id, world.run_id, target, HOST_PAGE_SIZE)
        first, items = owner.all_items(request)
        if "native-evidence-unavailable" in limitation_kinds(first["context"]):
            pending.append((subject, "calls-unavailable", None))
            continue
        reached = sorted({i["endpoint"]["universe"] for i in items if i["endpoint"]["kind"] == "symbol"})
        for universe in reached:
            origin_set(universe)
        pending.append((subject, "reach", (request, first, items, reached)))
    embedded = set(sorted(sets)[:MAX_ORIGIN_SETS])
    rows = []
    for subject, kind, reach in pending:
        base = {"subjectId": subject["subjectId"]}
        if kind is None:
            rows.append(dict(base, state="unknown", cause="subject-descriptor-not-retained"))
            continue
        target = subject["endpoint"]
        if kind == "origin":
            need(target["universe"] in embedded, "J-TR-ORIGIN-SETS-CAP")
            rows.append(dict(base, state="is-test-origin", **copy.deepcopy(origin_maps[target["universe"]][target["nativeSubjectId"]])))
            continue
        if kind == "calls-unavailable":
            rows.append(dict(base, state="unknown", cause="calls-evidence-unavailable"))
            continue
        request, first, items, reached = reach
        context = first["context"]
        reach_ctx = {"request": request, "responseContext": context}
        considered = sorted(set(reached) | {target["universe"]})
        if all(sets[u]["completeness"] == "none" for u in considered):
            rows.append(dict(base, state="unknown", cause="no-test-origin-identity", reach=reach_ctx, reachedUniverses=reached))
            continue
        hits = sorted((i for i in items if i["endpoint"]["kind"] == "symbol" and i["endpoint"]["universe"] in embedded
                       and i["endpoint"]["nativeSubjectId"] in origin_maps[i["endpoint"]["universe"]]),
                      key=lambda i: (i["depth"], RM.endpoint_tuple(i["endpoint"])))
        if hits:
            start = hits[0]["endpoint"]
            wreq = witness_request(world.project_id, world.run_id, start, target)
            rows.append(dict(base, state="static-path-from-test-origin", reach=reach_ctx,
                             origin=dict(endpoint=start, **copy.deepcopy(origin_maps[start["universe"]][start["nativeSubjectId"]])),
                             witness={"request": wreq, "response": owner.execute(wreq)}, interpretation="static-calls-path-not-executed-coverage"))
            continue
        rows.append(dict(base, state="not-found-incomplete", reach=reach_ctx, reachedUniverses=reached, blockers=test_blockers(context, sets, reached, embedded),
                         interpretation="no-static-path-from-identified-test-origins-not-untested"))
    rows.sort(key=lambda r: r["subjectId"].encode())
    total = len([s for s in resolution if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol"])
    used = [sets[k] for k in sorted(sets)]
    return rows, item_projection(total, len(chosen), "item-cap"), used[:MAX_ORIGIN_SETS], item_projection(len(used), min(len(used), MAX_ORIGIN_SETS), "item-cap")


def admit_origin_evidence(origin, origin_set):
    evidence = origin["originEvidence"]
    if evidence["kind"] == "rust-test-target":
        need(origin_set["source"] == "rust-test-targets" and set(evidence["unitIds"]) <= {t["unitId"] for t in origin_set["evidence"]["testTargets"]}, "J-TR-ORIGIN")
        return
    need(origin_set["source"] == "recognized-test-globs" and evidence["unitOrdinal"] == origin_set["evidence"]["unitOrdinal"], "J-TR-ORIGIN")
    need(any(evidence["glob"] in r["testGlobs"] for r in origin_set["evidence"]["recognizers"]) and glob_match(evidence["glob"], evidence["relativePath"]), "J-TR-ORIGIN")
    need(origin["attributionPath"] == join_root(origin_set["evidence"]["rootPath"], evidence["relativePath"]), "J-TR-ORIGIN")


def admit_test_reachability(rows, projection, origin_sets, sets_projection, recognition, ctx):
    resolution = {s["subjectId"]: s for s in ctx["resolution"]}
    chosen = [s for s in ctx["resolution"] if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol"]
    need(projection == item_projection(len(chosen), min(len(chosen), MAX_TEST_REACHABILITY), "item-cap")
         and [r["subjectId"] for r in rows] == sorted((s["subjectId"] for s in chosen[:MAX_TEST_REACHABILITY]), key=lambda x: x.encode()), "J-TR-TOTALITY")
    need(sets_projection["total"] - sets_projection["omitted"] == len(origin_sets), "J-TR-ORIGIN-SET")
    units = {u["unitOrdinal"]: u for u in recognition.get("units", [])}
    sets = {}
    for origin_set in origin_sets:
        need(origin_set["completeness"] != "complete", "J-TR-ORIGIN-SET")
        if origin_set["source"] == "rust-test-targets":
            need("in-target-unit-tests-not-identified" in origin_set["limitations"], "J-TR-ORIGIN-SET")
        if origin_set["source"] == "recognized-test-globs":
            need("recognizer-globs-not-test-population" in origin_set["limitations"], "J-TR-ORIGIN-SET")
            evidence, unit = origin_set["evidence"], units.get(origin_set["evidence"]["unitOrdinal"])
            retained = [{"recognizerId": r["recognizerId"], "testGlobs": r["testGlobs"], "unresolvedChoices": r["unresolvedChoices"], "evidence": r["evidence"]}
                        for r in (unit["recognizers"] if unit else []) if r["recognizerId"] == "vitest-jest"]
            need(unit is not None and recognition["state"] == "plan-bound" and unit["rootPath"] == evidence["rootPath"] and unit["markerPath"] == evidence["markerPath"]
                 and unit["recognitionId"] == evidence["recognitionId"] and evidence["recognizers"] == retained, "J-TR-ORIGIN-SET")
            choices = {c for r in retained for c in r["unresolvedChoices"]}
            need(("test-selection-configured" in origin_set["limitations"]) == ("test-selection-configured" in choices)
                 and ("recognizer-unresolved-choices" in origin_set["limitations"]) == bool(choices - {"test-selection-configured"}), "J-TR-ORIGIN-SET")
        sets[origin_set["universe"]] = origin_set
    for row in rows:
        subject = resolution[row["subjectId"]]
        if row["state"] == "unknown" and row["cause"] == "subject-descriptor-not-retained":
            need(subject["state"] == "descriptor-not-retained", "J-TR-SUBJECT")
            continue
        need(subject["state"] == "resolved" and subject["endpoint"]["kind"] == "symbol", "J-TR-SUBJECT")
        target = subject["endpoint"]
        if row["state"] == "is-test-origin":
            need(target["universe"] in sets, "J-TR-ORIGIN-SET")
            admit_origin_evidence(row, sets[target["universe"]])
            continue
        if row["state"] == "unknown" and row["cause"] == "calls-evidence-unavailable":
            continue
        reach = row["reach"]
        need(reach["request"] == reach_request(ctx["projectId"], ctx["runId"], target, HOST_PAGE_SIZE), "J-TR-REQUEST")
        context = reach["responseContext"]
        need(context["projectId"] == ctx["projectId"] and context["resolvedView"] == {"runId": ctx["runId"]}, "J-TR-RUN")
        need("native-evidence-unavailable" not in limitation_kinds(context), "J-TR-STATE")
        if row["state"] == "unknown":
            considered = sorted(set(row["reachedUniverses"]) | {target["universe"]})
            need(all(u in sets and sets[u]["completeness"] == "none" for u in considered), "J-TR-STATE")
            continue
        if row["state"] == "static-path-from-test-origin":
            origin_universe = row["origin"]["endpoint"]["universe"]
            need(origin_universe in sets, "J-TR-ORIGIN-SET")
            admit_origin_evidence(row["origin"], sets[origin_universe])
            wreq = row["witness"]["request"]
            need(wreq == witness_request(ctx["projectId"], ctx["runId"], row["origin"]["endpoint"], target), "J-TR-WITNESS")
            exchange_ok(wreq, row["witness"]["response"], ctx["projectId"], ctx["runId"], ctx["bounds"], "J-TR")
            need(len(row["witness"]["response"]["items"]) == 1, "J-TR-WITNESS")
            continue
        need(row["reachedUniverses"] == sorted(set(row["reachedUniverses"])), "J-TR-STATE")
        need(row["blockers"] == test_blockers(context, sets, row["reachedUniverses"], set(sets)), "J-TR-BLOCKERS")


def test_origin_state_fn(world):
    cache = {}

    def state(endpoint):
        if endpoint["universe"] not in cache:
            cache[endpoint["universe"]] = derive_test_origins(world, endpoint["universe"])
        origin_set, origins = cache[endpoint["universe"]]
        if origin_set["completeness"] == "none":
            return "no-test-origin-identity"
        return "test-origin" if endpoint["kind"] == "symbol" and endpoint["nativeSubjectId"] in origins else "not-identified-as-test-origin"
    return state


# ---------------------------------------------------------------------------
# panels and report-wide placement

SYMBOL_EVIDENCE_PROVENANCE = {
    "verifiedInDocument": ["cargo-target-entry-state-recomputed", "entry-summary-recomputed-from-recognizers", "explicit-entry-points-replace-other-entries",
                           "metric-reading-recomputed-from-owner-context", "metric-request-recomputed-from-catalog-and-subject", "origin-sets-bound-to-embedded-recognition",
                           "owner-page-law", "rows-match-request", "run-equals-envelope-run", "test-blockers-recomputed-from-embedded-sets",
                           "test-origin-glob-matched-on-unit-relative-path", "trace-path-request-start-is-embedded-origin-row", "trace-state-and-blockers-recomputed",
                           "unit-id-subset-of-test-targets", "witness-path-request-from-origin-to-subject"],
    "hostAsserted": ["origin-symbol-path-from-plan-bound-symbol-inventory", "reached-universes-of-unembedded-reach-rows", "recognition-id-over-unembedded-entry-paths",
                     "recognition-parameter-availability", "test-origin-membership-of-unembedded-rows"],
}


def symbol_evidence_panel(world, parts, metrics, metrics_projection):
    return {"policy": SYMBOL_EVIDENCE_POLICY, "runId": world.run_id, "metricCatalog": METRIC_IDS, "metrics": metrics, "metricsProjection": metrics_projection,
            "entryRecognition": parts["recognition"], "traces": parts["traces"], "tracesProjection": parts["tracesProjection"], "testOrigins": parts["sets"],
            "testOriginsProjection": parts["setsProjection"], "testReachability": parts["reach"], "testReachabilityProjection": parts["reachProjection"],
            "provenance": SYMBOL_EVIDENCE_PROVENANCE}


def derive_symbol_evidence(world, resolution, budget, start_resolver=None, name_resolver=None, owner=None):
    owner = owner or EvidenceGraphOwner(world)
    rows = metric_rows(world, owner, resolution)
    traces, traces_projection = derive_traces(world, owner, resolution, start_resolver)
    reach, reach_projection, sets, sets_projection = derive_test_reachability(world, owner, resolution, name_resolver)
    parts = {"recognition": entry_recognition_panel(world), "traces": traces, "tracesProjection": traces_projection, "sets": sets, "setsProjection": sets_projection,
             "reach": reach, "reachProjection": reach_projection}
    skeleton = symbol_evidence_panel(world, parts, [], item_projection(len(rows), 0, "byte-budget", PLACEHOLDER_DELTA))
    if measure(skeleton) > budget:
        return None
    kept, projection = byte_prefix(rows, budget - measure(skeleton) + measure([]))
    panel = symbol_evidence_panel(world, parts, kept, projection)
    while measure(panel) > budget:
        kept = kept[:-1]
        projection = item_projection(len(rows), len(kept), "byte-budget", measure(rows[:len(kept) + 1]) - measure(kept))
        panel = symbol_evidence_panel(world, parts, kept, projection)
    return panel


def admit_panel_prerequisites(panels):
    evidence = panels.get("symbolEvidence")
    if evidence is not None and panels.get("graph", {}).get("state") != "present":
        need(evidence == {"state": "unavailable", "reason": "prerequisite-panel-not-present"}, "J-SE-PREREQUISITE")


def admit_symbol_evidence(panel, ctx):
    need(panel["runId"] == ctx["runId"], "J-SE-RUN")
    need(ctx["resolution"] == ctx["graphResolution"], "J-SE-SUBJECTS")
    need(measure(panel) <= ctx["budget"], "J-SE-BUDGET")
    admit_symbol_metrics(panel["metrics"], panel["metricsProjection"], ctx)
    admit_entry_recognition(panel["entryRecognition"])
    admit_traces(panel["traces"], panel["tracesProjection"], panel["entryRecognition"], ctx)
    admit_test_reachability(panel["testReachability"], panel["testReachabilityProjection"], panel["testOrigins"], panel["testOriginsProjection"], panel["entryRecognition"], ctx)


OMITTED = {"state": "omitted", "reason": "exploration-budget-exceeded"}
SUCCESSOR_PANELS = ["symbolEvidence", "coupling"]


def place_successor_panels(existing, cap, build):
    """Report-wide placement after every parent panel (priority comparison, catalog, evidence, graph, history, symbolEvidence, coupling): each successor
    panel gets exactly the canonical bytes left by the whole panels object, and an omitted panel forces every later one omitted (J-BUDGET-ORDER)."""
    panels = copy.deepcopy(existing)
    for name in SUCCESSOR_PANELS:
        panels[name] = dict(OMITTED)
    budgets, stopped = {}, False
    for name in SUCCESSOR_PANELS:
        if stopped:
            continue
        remaining = cap - measure(panels) + measure(panels[name]) - measure({"state": "present", "data": None}) + measure(None)
        budgets[name] = remaining
        data = build[name](remaining) if remaining > 0 else None
        if data is None:
            stopped = True
            continue
        panels[name] = {"state": "present", "data": data}
        need(measure(panels) <= cap, "J-BUDGET-PLACEMENT-INTERNAL")
    return panels, budgets


def admit_successor_placement(panels, cap):
    need(measure(panels) <= cap, "J-BUDGET-TOTAL")
    seen_omitted = False
    for name in SUCCESSOR_PANELS:
        value = panels.get(name)
        if value is None:
            continue
        if value.get("state") == "present":
            need(not seen_omitted, "J-BUDGET-ORDER")
        elif value.get("reason") == "exploration-budget-exceeded":
            seen_omitted = True
