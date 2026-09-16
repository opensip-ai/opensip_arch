"""Report evidence design reference model (author-01): RP-DO-03 coupling, RP-DO-05 entry points, RP-DO-09 symbol metrics, RP-DO-10 test reachability.

Design/reference only; no product authority, no runtime, browser or Run replay qualification.

Layers:
- retained-closure mock (World) built from owner-schema-valid records: snapshot inventory, UnitMembershipV1, EnumerationPlanV1, SubjectInventoryV1,
  SourceUnitOwnershipV1, FrameworkRecognitionPlanV1 (proposed parameter) and projected graph facts with reconciled occupancy;
- host derivations (what the reporting projection computes from that closure through owner laws);
- browser-level document admission (shape is checked by the schema; these are the internal joins a single offline file can verify).

External code is bound, not imported: `bind(canonical, report_model)` receives the pinned foundation canonical codec and the pinned subject-05 report
model (page law, subject3 minting, the owner-ordered mock graph owner). Nothing here reads files.
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


def raw_sha(value):
    return hashlib.sha256(canon(value)).hexdigest()


def native_h(domain, record):
    """native_evidence_model.native_identity recipe: 'sha256:' + H(domain, C(record)) (foundation canonical.identity)."""
    return "sha256:" + C.identity(domain, record)


def ekey(endpoint):
    return canon(endpoint)


PUBLIC_BOUNDS = {"maxPageSize": 1000, "defaultPageSize": 100, "maxItemsPerOperation": 100000, "maxTraversalDepth": 64, "maxVisitedNodes": 1000000}
FAMILY = {"rust-cargo": "rust", "rust-cargo-prepared": "rust", "ts-tsconfig": "tsjs", "js-allowjs": "tsjs", "js-synthesized": "tsjs", "syntax-only": "none"}
RECOGNITION_DOMAIN = "native.framework-recognition.v1"
COMPILATION_UNIT_DOMAIN = "native.compilation-unit.v1"
ORIGIN_PAGE_SIZE = 100
HOST_PAGE_SIZE = 1000
TRACE_MAX_DEPTH = 16
TEST_REACH_MAX_DEPTH = 16
MAX_TRACES = 8
MAX_TEST_REACHABILITY = 64
MAX_DRILLDOWN = 1000
COUPLING_POLICY = "imports-resolved-target-owner-coupling.1"
SYMBOL_EVIDENCE_POLICY = "symbol-evidence.1"
METRIC_CATALOG = [
    # (metricId, operation, relation, rung, direction, maxDepth)
    ("distinct-resolved-callees-within-1-hop", "graph.reach", "calls", "resolved-callee", "outgoing", 1),
    ("distinct-resolved-callers-within-1-hop", "graph.reach", "calls", "resolved-callee", "incoming", 1),
    ("resolved-call-facts-incoming", "graph.neighbors", "calls", "resolved-callee", "incoming", None),
    ("resolved-call-facts-outgoing", "graph.neighbors", "calls", "resolved-callee", "outgoing", None),
    ("resolved-reference-facts-incoming", "graph.neighbors", "references", "resolved-binding", "incoming", None),
]
METRIC_IDS = [m[0] for m in METRIC_CATALOG]
IMPORTER_CAUSES = ["membership-row-missing", "no-program-unit", "not-compiled-by-selected-targets", "owned-only-by-unselected-targets",
                   "owner-manifest-not-package-inventoried", "ownership-enumeration-partial", "ownership-missing", "package-inventory-conflict",
                   "package-inventory-incomplete", "symbol-attribution-conflict", "symbol-inventory-incomplete", "symbol-inventory-missing",
                   "symbol-not-inventoried", "universe-not-plan-bound"]
TARGET_CAUSES = sorted(IMPORTER_CAUSES + ["external-non-package-target", "file-not-inventoried", "package-endpoint-inventory-mismatch", "unknown-occupancy"])
COUPLING_BLOCKERS = ["evidence-limitations", "projection-lower-bound", "unattributed-importers", "unattributed-targets"]
TRACE_UNKNOWN_CAUSES = ["origin-page-set-not-embedded", "reachability-evidence-unavailable", "recognition-not-plan-bound", "recognition-unavailable",
                        "subject-descriptor-not-retained"]
TRACE_BLOCKERS = ["entry-recognition-not-all", "evidence-limitations", "origin-attribution-unavailable"]
ORIGIN_NONE_CAUSES = ["no-test-recognizer", "ownership-missing", "recognition-not-plan-bound", "recognition-unavailable", "unsupported-language-family",
                      "universe-not-plan-bound"]
ORIGIN_LIMITATIONS = ["foreign-unit-paths-not-matched", "in-target-unit-tests-not-identified", "no-selected-test-targets", "ownership-enumeration-partial",
                      "recognizer-unresolved-choices", "shared-test-and-non-test-target-path", "symbol-attribution-conflict", "symbol-inventory-incomplete"]
TEST_UNKNOWN_CAUSES = ["calls-evidence-unavailable", "no-test-origin-identity", "subject-descriptor-not-retained"]
TEST_BLOCKERS = ["evidence-limitations", "reach-lower-bound", "test-origin-set-partial"]


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
    """Longest prefix whose canonical array bytes fit the budget; returns (kept, projection)."""
    kept = []
    for row in rows:
        if len(canon(kept + [row])) > budget:
            return kept, item_projection(len(rows), len(kept), "byte-budget", len(canon(kept + [row])) - len(canon(kept)))
        kept.append(row)
    return kept, item_projection(len(rows), len(kept))


# ---------------------------------------------------------------------------
# glob-pattern-contract.v1 (anchored, '/'-split, '**' whole segments, '*'/'?' Unicode scalars, no escapes/classes/braces)

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
# retained closure mock

class World:
    """An admitted-Run projection context. Every record is owner-schema valid (checked by the caller); joins here follow the owner laws."""

    def __init__(self, data):
        self.data = data
        self.project_id, self.run_id, self.snapshot_id = data["projectId"], data["runId"], data["snapshotId"]
        self.inventory = {row["path"]: row for row in data["snapshotInventory"]}
        self.membership = data["membership"]
        self.units = {u["unitOrdinal"]: u for u in self.membership["units"]}
        need(len(self.units) == len(self.membership["units"]), "J-WORLD-MEMBERSHIP", "duplicate unitOrdinal")
        self.member_rows = {}
        for row in self.membership["rows"]:
            need(row["path"] not in self.member_rows, "J-WORLD-MEMBERSHIP", "duplicate membership row")
            self.member_rows[row["path"]] = row
        self.plan = data["enumerationPlan"]
        need(self.plan["membershipDigest"] == raw_sha(self.membership), "J-WORLD-MEMBERSHIP", "EnumerationPlanV1.membershipDigest")
        self.bindings = {}
        for cell_ordinal, cell in enumerate(self.plan["cells"]):
            for binding in cell["programBindings"]:
                if binding["universe"] is not None:
                    self.bindings.setdefault(binding["universe"], []).append(
                        {"cellOrdinal": cell_ordinal, "programOrdinal": binding["ordinal"], "languageMode": cell["languageMode"], "workspaceRoot": cell["workspaceRoot"]})
        self.inventories = data["subjectInventories"]
        for inv in self.inventories:
            cell = self.plan["cells"][inv["cellOrdinal"]]
            need(inv["kind"] in cell["kinds"] and any(b["ordinal"] == inv["programOrdinal"] for b in cell["programBindings"]), "J-WORLD-INVENTORY")
        self.ownership = data["sourceUnitOwnership"]
        for universe, record in self.ownership.items():
            need(self.family(universe) == "rust", "J-WORLD-OWNERSHIP", "ownership on a non-Rust universe")
            for unit in record["units"]:
                projection = {"schemaVersion": 1, "markerPath": unit["markerPath"], "targetKind": unit["targetKind"], "targetName": unit["targetName"]}
                need(unit["unitId"] == native_h(COMPILATION_UNIT_DOMAIN, projection), "J-WORLD-OWNERSHIP", "unitId")
                need(unit["markerPath"] in self.inventory, "J-WORLD-OWNERSHIP", "markerPath")
            declared = {u["unitId"] for u in record["units"]}
            need(set(record["selectedUnitIds"]) <= declared and all(r["unitId"] in declared and r["path"] in self.inventory for r in record["ownership"]),
                 "J-WORLD-OWNERSHIP", "selection/ownership names an undeclared unit or uninventoried path")
        self.recognition = data["recognition"]
        self.config_entry_points = data["resolvedConfigurationEntryPoints"]
        self.availability = data["availability"]
        self.facts = expand_facts(data)
        self.relations = data["relations"]

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
        """Native-attested symbol path from the Plan-bound symbol inventories of this universe; never a parse of the SubjectIdV1 spelling."""
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
        """Owning package/workspace keys of one first-party path read by `universe`.
        Rust: SourceUnitOwnershipV1 rows whose path EQUALS the path, restricted to the selection; the package is the declaring manifest (markerPath)
        joined to a first-party package inventory row. TS/JS: the retained UnitMembershipV1 row's unit; its co-located package.json (U-1 marker directory)
        when that manifest is inventoried. No directory prefix, nearest manifest or symbol spelling is consulted."""
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
        if occupancy == "unknown":
            return None, "unknown-occupancy"
        if occupancy == "external":
            if endpoint["kind"] == "package":
                return [{"keyKind": "external-package", "universe": endpoint["universe"], "path": endpoint["packageManifestPath"], "name": endpoint["nativeSubjectId"]}], None
            return None, "external-non-package-target"
        if endpoint["kind"] == "package":
            name, cause = self.package_row(endpoint["packageManifestPath"])
            if cause:
                return None, cause
            if name != endpoint["nativeSubjectId"]:
                return None, "package-endpoint-inventory-mismatch"
            return [{"keyKind": "first-party-package", "path": endpoint["packageManifestPath"]}], None
        if endpoint["kind"] == "file":
            if endpoint["nativeSubjectId"] not in self.inventory:
                return None, "file-not-inventoried"
            return self.path_owner_keys(endpoint["universe"], endpoint["nativeSubjectId"])
        path, cause = self.symbol_attribution(endpoint["universe"], endpoint["nativeSubjectId"])
        if cause:
            return None, cause
        return self.path_owner_keys(endpoint["universe"], path)

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
            facts.append({"factId": "fact2:" + hashlib.sha256(("fan:%s:%d" % (fan["name"], i)).encode()).hexdigest(), "relation": fan["relation"],
                          "resolution": fan["resolution"], "source": source, "target": fan["target"], "targetOccupancy": "first-party", "viewDigest": fan["viewDigest"]})
    return facts


# ---------------------------------------------------------------------------
# query owner successor: whole-view internal projection (query-projection-contract.v3 section 8 steps 1-4 and 7; no endpoint admission, no public op)

def whole_view_projection(world, relation, rung, max_items=PUBLIC_BOUNDS["maxItemsPerOperation"]):
    need(world.availability == "retained", "QUERY-EVIDENCE-UNAVAILABLE", "the section 8 closure requires retained evidence")
    rel = world.relations.get(relation + "@" + rung)
    if rel is None or not rel["views"]:
        return {"rows": [], "countBasis": "exact", "factViewDigests": [], "coverageIds": [], "limitationKinds": ["native-evidence-unavailable"],
                "deficiencyCitationCount": 0}
    rows = {}
    for fact in world.facts:
        if fact["relation"] == relation and fact["resolution"] == rung and fact["viewDigest"] in rel["views"]:
            rows.setdefault(fact["factId"], fact)
    ordered = [rows[k] for k in sorted(rows, key=lambda f: f.encode())]
    kinds = {l["kind"] for l in rel["resolutionLimitations"]}
    produced = ordered[:max_items]
    if len(ordered) > max_items:
        kinds.add("unexamined-work-bound")
    return {"rows": produced, "countBasis": "lower-bound" if len(ordered) > max_items else "exact", "factViewDigests": ["view2:" + v for v in sorted(rel["views"])],
            "coverageIds": sorted(rel["coverageIds"]), "limitationKinds": sorted(kinds), "deficiencyCitationCount": len(rel["deficiencyCitations"])}


class EvidenceGraphOwner:
    """Public graph.* answers for the World: subject-05 MockGraphOwner ordering/page law plus the section 6 evidence disclosure per relation@rung."""

    def __init__(self, world, max_items=PUBLIC_BOUNDS["maxItemsPerOperation"]):
        self.world, self.max_items, self.calls = world, max_items, 0

    def execute(self, request):
        need(self.world.availability == "retained", "QUERY-EVIDENCE-UNAVAILABLE", "graph operations refuse HOST.IO_FAILURE on non-retained evidence")
        self.calls += 1
        params = request["params"]
        rel = self.world.relations.get(params["relation"] + "@" + params["minResolution"])
        evidence = {"coverageIds": [], "scopeIds": [], "deficiencyCitations": [], "resolutionLimitations": []}
        facts = []
        if rel is None or not rel["views"]:
            evidence["resolutionLimitations"] = [{"kind": "native-evidence-unavailable", "relation": params["relation"], "minResolution": params["minResolution"]}]
            views = []
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
        return RM.MockGraphOwner(facts, template, self.max_items).execute(request)

    def all_items(self, request):
        """Host walk of every page of one logical operation (continuation cursors are the owner's)."""
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
# RP-DO-03 coupling

def derive_coupling(world, drill_budget=None, key_resolver=None, test_origin_state=None):
    """key_resolver lets adversarial fixtures substitute a guessing attribution; the lawful resolver is World.path_owner_keys via symbol_attribution."""
    projection = whole_view_projection(world, "imports", "resolved-target")
    cells, importer_buckets, target_buckets, keys, drill = {}, {}, {}, {}, []
    attributed, importer_unattributed, target_unattributed = set(), set(), set()

    def importer_keys(endpoint):
        if key_resolver is not None:
            return key_resolver(world, endpoint)
        path, cause = world.symbol_attribution(endpoint["universe"], endpoint["nativeSubjectId"])
        if cause:
            return None, cause, None
        found, cause = world.path_owner_keys(endpoint["universe"], path)
        return found, cause, path

    for row in projection["rows"]:
        fact_id, importer, target = row["factId"], row["source"], row["target"]
        from_keys, cause, importer_path = importer_keys(importer)
        if cause:
            importer_buckets.setdefault(cause, set()).add(fact_id)
            importer_unattributed.add(fact_id)
            continue
        to_keys, cause = world.endpoint_owner_keys(target, row["targetOccupancy"])
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
                cell = cells.setdefault((owner_key(fk), owner_key(tk)), {"facts": set(), "edges": set(), "importers": set(), "sharedImporter": set(),
                                                                        "sharedTarget": set(), "universes": set()})
                cell["facts"].add(fact_id)
                cell["edges"].add((ekey(importer), ekey(target)))
                cell["importers"].add(ekey(importer))
                cell["universes"].add(importer["universe"])
                if len(from_keys) > 1:
                    cell["sharedImporter"].add(fact_id)
                if len(to_keys) > 1:
                    cell["sharedTarget"].add(fact_id)
                drill.append({"fromOwnerKey": owner_key(fk), "toOwnerKey": owner_key(tk), "factId": fact_id, "importer": importer, "target": target,
                              "importerPath": importer_path, "importerTestOrigin": test_origin_state(importer) if test_origin_state else "no-test-origin-identity"})
    def record(k):
        if key_resolver is not None and k["keyKind"] == "first-party-package" and world.package_row(k["path"])[1] is not None:
            return guessed_owner_record(world, k)
        return world.owner_record(k)
    owners = sorted((record(k) for k in keys.values()), key=lambda o: o["ownerKey"].encode())
    blockers = set()
    if projection["countBasis"] != "exact":
        blockers.add("projection-lower-bound")
    if projection["limitationKinds"] or projection["deficiencyCitationCount"]:
        blockers.add("evidence-limitations")
    if importer_buckets:
        blockers.add("unattributed-importers")
    if target_buckets:
        blockers.add("unattributed-targets")
    drill.sort(key=lambda r: (r["fromOwnerKey"].encode(), r["toOwnerKey"].encode(), r["factId"].encode()))
    budget_rows, drill_projection = (drill[:MAX_DRILLDOWN], item_projection(len(drill), min(len(drill), MAX_DRILLDOWN), "item-cap")) if drill_budget is None \
        else byte_prefix(drill[:MAX_DRILLDOWN], drill_budget)
    if drill_budget is not None and len(drill) > MAX_DRILLDOWN and drill_projection["omissionCause"] == "none":
        drill_projection = item_projection(len(drill), MAX_DRILLDOWN, "item-cap")
    elif drill_budget is not None and drill_projection["omissionCause"] == "byte-budget":
        drill_projection["total"] = len(drill)
        drill_projection["omitted"] = len(drill) - len(budget_rows)
    return {
        "policy": COUPLING_POLICY, "runId": world.run_id, "relation": "imports", "minResolution": "resolved-target",
        "projection": {k: projection[k] for k in ("countBasis", "factViewDigests", "coverageIds", "limitationKinds", "deficiencyCitationCount")},
        "owners": owners,
        "cells": [{"fromOwnerKey": f, "toOwnerKey": t, "facts": len(c["facts"]), "edges": len(c["edges"]), "importerSymbols": len(c["importers"]),
                   "sharedImporterFacts": len(c["sharedImporter"]), "sharedTargetFacts": len(c["sharedTarget"]), "internal": f == t,
                   "importerUniverses": sorted(c["universes"])} for (f, t), c in sorted(cells.items(), key=lambda kv: (kv[0][0].encode(), kv[0][1].encode()))],
        "importerBuckets": [{"cause": cause, "facts": len(ids)} for cause, ids in sorted(importer_buckets.items())],
        "targetBuckets": [{"fromOwnerKey": k, "cause": cause, "facts": len(ids)} for (k, cause), ids in sorted(target_buckets.items(), key=lambda kv: (kv[0][0].encode(), kv[0][1]))],
        "totals": {"distinctFacts": len(projection["rows"]), "attributedFacts": len(attributed), "importerUnattributedFacts": len(importer_unattributed),
                   "targetUnattributedFacts": len(target_unattributed)},
        "absence": {"blankCellMeans": "no-projected-fact", "absenceSupported": not blockers, "blockers": sorted(blockers)},
        "drilldown": budget_rows, "drilldownProjection": drill_projection,
        "provenance": COUPLING_PROVENANCE,
    }


def guessed_owner_record(world, key):
    """Only reached by adversarial resolvers naming a manifest that is not inventoried; the record then claims an invented package."""
    return {"ownerKey": owner_key(key), "keyKind": "first-party-package", "packageManifestPath": key["path"], "packageName": "guessed", "cargoTargets": [], "workspaceUnit": None}


COUPLING_PROVENANCE = {
    "verifiedInDocument": ["absence-supported-iff-no-blockers", "blockers-recomputed-from-buckets-and-projection", "cargo-target-unit-id-recomputed",
                           "cell-owner-keys-listed", "cell-count-inequalities", "drilldown-rows-join-cells", "owner-key-recomputed-from-owner-record",
                           "run-equals-envelope-run", "totals-partition-distinct-facts"],
    "hostAsserted": ["importer-symbol-path-from-plan-bound-symbol-inventory", "internal-whole-view-imports-projection", "owner-from-retained-membership-or-source-unit-ownership",
                     "per-cell-fact-edge-importer-counts", "target-occupancy-reconciliation"],
}


def admit_coupling(panel, run_id):
    need(panel["runId"] == run_id, "J-COUPLING-RUN")
    owners = {}
    for owner in panel["owners"]:
        need(owner["ownerKey"] == owner_key(owner_key_record(owner)), "J-COUPLING-OWNER-KEY")
        for target in owner.get("cargoTargets", []):
            projection = {"schemaVersion": 1, "markerPath": target["markerPath"], "targetKind": target["targetKind"], "targetName": target["targetName"]}
            need(target["unitId"] == native_h(COMPILATION_UNIT_DOMAIN, projection) and target["markerPath"] == owner["packageManifestPath"], "J-COUPLING-OWNER-KEY")
        owners[owner["ownerKey"]] = owner
    cell_facts = {}
    for cell in panel["cells"]:
        need(cell["fromOwnerKey"] in owners and cell["toOwnerKey"] in owners, "J-COUPLING-CELL")
        need(owners[cell["fromOwnerKey"]]["keyKind"] != "external-package", "J-COUPLING-CELL", "an external package imports nothing in this projection")
        need(cell["facts"] >= cell["edges"] >= 1 and cell["edges"] >= cell["importerSymbols"] >= 1 and cell["sharedImporterFacts"] <= cell["facts"]
             and cell["sharedTargetFacts"] <= cell["facts"] and cell["internal"] == (cell["fromOwnerKey"] == cell["toOwnerKey"]), "J-COUPLING-COUNT")
        cell_facts[(cell["fromOwnerKey"], cell["toOwnerKey"])] = cell
    for bucket in panel["targetBuckets"]:
        need(bucket["fromOwnerKey"] in owners and bucket["facts"] >= 1, "J-COUPLING-BUCKET")
    need(all(b["facts"] >= 1 for b in panel["importerBuckets"]), "J-COUPLING-BUCKET")
    totals = panel["totals"]
    need(totals["distinctFacts"] == totals["attributedFacts"] + totals["importerUnattributedFacts"] + totals["targetUnattributedFacts"], "J-COUPLING-TOTALS")
    need(totals["importerUnattributedFacts"] == sum(b["facts"] for b in panel["importerBuckets"]), "J-COUPLING-TOTALS")
    need(totals["targetUnattributedFacts"] <= sum(b["facts"] for b in panel["targetBuckets"]) and (totals["targetUnattributedFacts"] == 0) == (not panel["targetBuckets"]), "J-COUPLING-TOTALS")
    need(max([c["facts"] for c in panel["cells"]] + [0]) <= totals["attributedFacts"] <= sum(c["facts"] for c in panel["cells"]), "J-COUPLING-TOTALS")
    blockers = set()
    if panel["projection"]["countBasis"] != "exact":
        blockers.add("projection-lower-bound")
    if panel["projection"]["limitationKinds"] or panel["projection"]["deficiencyCitationCount"]:
        blockers.add("evidence-limitations")
    if panel["importerBuckets"]:
        blockers.add("unattributed-importers")
    if panel["targetBuckets"]:
        blockers.add("unattributed-targets")
    need(panel["absence"]["blockers"] == sorted(blockers) and panel["absence"]["absenceSupported"] == (not blockers), "J-COUPLING-ABSENCE")
    per_cell = {}
    for row in panel["drilldown"]:
        cell = cell_facts.get((row["fromOwnerKey"], row["toOwnerKey"]))
        need(cell is not None and row["importer"]["universe"] in cell["importerUniverses"], "J-COUPLING-DRILL")
        per_cell[(row["fromOwnerKey"], row["toOwnerKey"])] = per_cell.get((row["fromOwnerKey"], row["toOwnerKey"]), 0) + 1
    need(all(n <= cell_facts[k]["facts"] for k, n in per_cell.items()), "J-COUPLING-DRILL")
    projection = panel["drilldownProjection"]
    need(projection["total"] == sum(c["facts"] for c in panel["cells"]) and projection["total"] - projection["omitted"] == len(panel["drilldown"]), "J-COUPLING-DRILL")


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
    """complete vs lower-bound vs unknown. A value is the owner's count of projected result units; a zero supports absence only when exact with no limitation."""
    kinds = limitation_kinds(context)
    if "native-evidence-unavailable" in kinds:
        return {"countState": "unknown", "cause": "native-evidence-unavailable"}
    state = "exact" if context["countBasis"] == "exact" else "lower-bound"
    return {"countState": state, "value": context["totalItems"], "limitationKinds": kinds,
            "zeroSupportsAbsence": state == "exact" and context["totalItems"] == 0 and not has_limitations(context)}


def derive_metrics(world, owner, resolution, byte_budget):
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
    return byte_prefix(rows, byte_budget)


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
# RP-DO-05 recognition parameter, custody and entry traces

def recognition_summary(recognized, explicit_paths):
    """native section 8 FR-1..FR-3 summary rule (native_evidence_model.recognize_frameworks) with FR-2: explicit configuration wins."""
    if explicit_paths:
        return {"state": "all", "source": "explicit"}
    has = any(r["effects"]["entryPoints"] for r in recognized)
    unresolved = any(r["unresolvedChoices"] for r in recognized)
    if has and not unresolved:
        return {"state": "all", "source": "recognized"}
    if has:
        return {"state": "partial", "source": "recognized"}
    return {"state": "none", "source": "none"}


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


def recognition_custody(world):
    """Plan-bound parameter custody. Availability is the retained Run's monotonic availability record; the parameter is a required closure ref."""
    rec = world.recognition
    if not rec["planBound"]:
        return {"state": "not-plan-bound"}
    parameter = rec["parameter"]
    availability = rec["availability"]
    state = availability["state"]
    if state in ("expired", "purged", "corrupt", "unavailable") or (state == "partial" and availability["parameterMissing"]):
        return {"state": "unavailable", "parameterDigest": parameter["payloadDigest"], "availability": state}
    need(parameter["payloadDigest"] == raw_sha(rec["record"]), "J-FRP-PARAMETER-DIGEST")
    return {"state": "plan-bound", "parameterDigest": parameter["payloadDigest"], "availability": state}


def effective_entries(world, universe):
    """path -> provenance rows for the program's unit; explicit configuration replaces recognized effects (FR-2)."""
    record = world.recognition["record"]
    if record["explicitEntryPoints"]:
        return {p: [{"source": "explicit"}] for p in record["explicitEntryPoints"]}
    unit = world.unit_for_universe(universe)
    if unit is None:
        return {}
    row = [r for r in record["units"] if r["unitOrdinal"] == unit["unitOrdinal"]]
    out = {}
    for result in (row[0]["recognition"]["recognized"] if row else []):
        for path in result["effects"]["entryPoints"]:
            out.setdefault(path, []).append({"source": "recognized", "unitOrdinal": unit["unitOrdinal"], "recognizerId": result["recognizerId"],
                                             "recognizerVersion": result["recognizerVersion"], "assurance": result["assurance"],
                                             "evidence": copy.deepcopy(result["evidence"]), "unresolvedChoices": list(result["unresolvedChoices"])})
    return out


def entry_recognition_panel(world):
    custody = recognition_custody(world)
    if custody["state"] != "plan-bound":
        return custody
    record = world.recognition["record"]
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
    return dict(custody, explicitEntryPointCount=len(record["explicitEntryPoints"]), units=units)


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
    custody = recognition_custody(world)
    if custody["state"] == "not-plan-bound":
        return dict(base, state="unknown", cause="recognition-not-plan-bound")
    if custody["state"] == "unavailable":
        return dict(base, state="unknown", cause="recognition-unavailable")
    target = subject["endpoint"]
    unit = world.unit_for_universe(target["universe"])
    base["scopeUnitOrdinal"] = unit["unitOrdinal"] if unit else None
    request = origin_request(world, target)
    response = owner.execute(request)
    context = response["context"]
    origin_query = {"request": request, "response": response}
    if "native-evidence-unavailable" in limitation_kinds(context):
        return dict(base, state="unknown", cause="reachability-evidence-unavailable", originQuery=origin_query)
    candidates, unattributed, outside = [], 0, 0
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
        panel_units = {u["unitOrdinal"]: u for u in entry_recognition_panel(world)["units"]}
        if unit is None or unit["unitOrdinal"] not in panel_units or panel_units[unit["unitOrdinal"]]["entryPoints"]["state"] != "all":
            blockers.add("entry-recognition-not-all")
        return dict(base, state="no-entry-origin", originQuery=origin_query, originsExamined=len(response["items"]), originsUnattributed=unattributed,
                    originsOutsideEntrySet=outside, blockers=sorted(blockers), interpretation="no-entry-origin-among-projected-reachability-origins-not-dead-code")
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


def admit_traces(traces, projection, recognition, ctx):
    resolution = {s["subjectId"]: s for s in ctx["resolution"]}
    chosen = [s for s in ctx["resolution"] if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol"]
    need(projection == item_projection(len(chosen), min(len(chosen), MAX_TRACES), "item-cap")
         and [t["subjectId"] for t in traces] == sorted((s["subjectId"] for s in chosen[:MAX_TRACES]), key=lambda x: x.encode()), "J-TRACE-TOTALITY")
    units = {u["unitOrdinal"]: u for u in recognition.get("units", [])}
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
                 and trace["originsUnattributed"] + trace["originsOutsideEntrySet"] == trace["originsExamined"], "J-TRACE-STATE")
            blockers = set()
            if has_limitations(response["context"]):
                blockers.add("evidence-limitations")
            if trace["originsUnattributed"]:
                blockers.add("origin-attribution-unavailable")
            scope = units.get(trace["scopeUnitOrdinal"])
            if scope is None or scope["entryPoints"]["state"] != "all":
                blockers.add("entry-recognition-not-all")
            need(trace["blockers"] == sorted(blockers), "J-TRACE-BLOCKERS")
            continue
        start = trace["start"]
        rows = [i for i in response["items"] if i["factId"] == start["viaReachabilityFactId"]]
        need(len(rows) == 1 and ekey(rows[0]["source"]) == ekey(start["endpoint"]), "J-TRACE-START")
        entry = start["entry"]
        need(entry["path"] == start["attributionPath"], "J-TRACE-ENTRY")
        for prov in entry["provenance"]:
            if prov["source"] == "explicit":
                need(recognition["explicitEntryPointCount"] > 0, "J-TRACE-ENTRY")
            else:
                need(recognition["explicitEntryPointCount"] == 0, "J-TRACE-ENTRY", "explicit configuration replaces recognized entry points")
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
    """Exact test origin identity: Rust symbols whose attributed path is owned only by selected `test` targets; TS/JS symbols of the unit's own
    membership rows whose unit-root-relative path matches a retained vitest-jest testGlob. Imported TestPayloadV1 rows are never origins."""
    family = world.family(universe)
    base = {"universe": universe}
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
    custody = recognition_custody(world)
    if custody["state"] != "plan-bound":
        cause = "recognition-not-plan-bound" if custody["state"] == "not-plan-bound" else "recognition-unavailable"
        return dict(base, source="none", completeness="none", cause=cause, limitations=[], originCount=0), {}
    unit = world.unit_for_universe(universe)
    rows = [r for r in world.recognition["record"]["units"] if unit and r["unitOrdinal"] == unit["unitOrdinal"]]
    recognizers = [r for r in (rows[0]["recognition"]["recognized"] if rows else []) if r["recognizerId"] == "vitest-jest"]
    if not recognizers:
        return dict(base, source="none", completeness="none", cause="no-test-recognizer", limitations=[], originCount=0), {}
    if any(r["unresolvedChoices"] for r in recognizers):
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
        need(unit["rootPath"] == "" or path.startswith(unit["rootPath"] + "/"), "J-TR-SLICE", "membership row contradicts the unit root")
        relative = path if unit["rootPath"] == "" else path[len(unit["rootPath"]) + 1:]
        matched = [g for g in globs if glob_match(g, relative)]
        if matched:
            origins[sid] = {"attributionPath": path, "originEvidence": {"kind": "recognized-test-glob", "unitOrdinal": unit["unitOrdinal"], "recognizerId": "vitest-jest",
                                                                         "glob": matched[0], "relativePath": relative}}
    evidence = {"unitOrdinal": unit["unitOrdinal"], "rootPath": unit["rootPath"], "markerPath": unit["markerPath"], "recognitionId": rows[0]["recognitionId"],
                "recognizers": [{"recognizerId": r["recognizerId"], "testGlobs": list(r["effects"]["testGlobs"]), "unresolvedChoices": list(r["unresolvedChoices"]),
                                 "evidence": copy.deepcopy(r["evidence"])} for r in recognizers]}
    completeness = "partial" if limitations else "declared"
    return dict(base, source="recognized-test-globs", completeness=completeness, limitations=sorted(limitations), originCount=len(origins), evidence=evidence), origins


def reach_request(project_id, run_id, endpoint, size):
    return query_base(project_id, run_id, "graph.reach", {"relation": "calls", "minResolution": "resolved-callee", "direction": "incoming",
                                                          "start": copy.deepcopy(endpoint), "maxDepth": TEST_REACH_MAX_DEPTH, "includeStart": False}, size)


def witness_request(project_id, run_id, start, target):
    return query_base(project_id, run_id, "graph.path", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing",
                                                         "start": copy.deepcopy(start), "target": copy.deepcopy(target), "maxDepth": TEST_REACH_MAX_DEPTH}, 1)


def test_blockers(context, origin_set):
    blockers = set()
    if context["countBasis"] != "exact":
        blockers.add("reach-lower-bound")
    if has_limitations(context):
        blockers.add("evidence-limitations")
    if origin_set["completeness"] != "declared":
        blockers.add("test-origin-set-partial")
    return sorted(blockers)


def derive_test_reachability(world, owner, resolution, name_resolver=None):
    sets, origin_maps, rows = {}, {}, []
    chosen = [s for s in resolution if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol"][:MAX_TEST_REACHABILITY]
    for subject in chosen:
        base = {"subjectId": subject["subjectId"]}
        if subject["state"] == "descriptor-not-retained":
            rows.append(dict(base, state="unknown", cause="subject-descriptor-not-retained"))
            continue
        target = subject["endpoint"]
        if target["universe"] not in sets:
            sets[target["universe"]], origin_maps[target["universe"]] = derive_test_origins(world, target["universe"], name_resolver)
        origin_set, origins = sets[target["universe"]], origin_maps[target["universe"]]
        if target["nativeSubjectId"] in origins:
            rows.append(dict(base, state="is-test-origin", **copy.deepcopy(origins[target["nativeSubjectId"]])))
            continue
        if origin_set["completeness"] == "none":
            rows.append(dict(base, state="unknown", cause="no-test-origin-identity"))
            continue
        request = reach_request(world.project_id, world.run_id, target, HOST_PAGE_SIZE)
        first, items = owner.all_items(request)
        context = first["context"]
        reach = {"request": request, "responseContext": context}
        if "native-evidence-unavailable" in limitation_kinds(context):
            rows.append(dict(base, state="unknown", cause="calls-evidence-unavailable"))
            continue
        hits = sorted((i for i in items if i["endpoint"]["universe"] == target["universe"] and i["endpoint"]["kind"] == "symbol" and i["endpoint"]["nativeSubjectId"] in origins),
                      key=lambda i: (i["depth"], RM.endpoint_tuple(i["endpoint"])))
        if hits:
            start = hits[0]["endpoint"]
            wreq = witness_request(world.project_id, world.run_id, start, target)
            rows.append(dict(base, state="static-path-from-test-origin", reach=reach,
                             origin=dict(endpoint=start, **copy.deepcopy(origins[start["nativeSubjectId"]])), witness={"request": wreq, "response": owner.execute(wreq)},
                             interpretation="static-calls-path-not-executed-coverage"))
            continue
        blockers = test_blockers(context, origin_set)
        if blockers:
            rows.append(dict(base, state="not-found-incomplete", reach=reach, blockers=blockers))
        else:
            rows.append(dict(base, state="no-static-path-within-bound", reach=reach, maxDepth=TEST_REACH_MAX_DEPTH,
                             interpretation="no-static-calls-path-from-identified-test-origins-within-bound-not-untested"))
    rows.sort(key=lambda r: r["subjectId"].encode())
    total = len([s for s in resolution if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol"])
    return rows, item_projection(total, len(chosen), "item-cap"), [sets[k] for k in sorted(sets)]


def admit_origin_evidence(origin, origin_set):
    evidence = origin["originEvidence"]
    if evidence["kind"] == "rust-test-target":
        need(origin_set["source"] == "rust-test-targets" and set(evidence["unitIds"]) <= {t["unitId"] for t in origin_set["evidence"]["testTargets"]}, "J-TR-ORIGIN")
        return
    need(origin_set["source"] == "recognized-test-globs" and evidence["unitOrdinal"] == origin_set["evidence"]["unitOrdinal"], "J-TR-ORIGIN")
    need(any(evidence["glob"] in r["testGlobs"] for r in origin_set["evidence"]["recognizers"]) and glob_match(evidence["glob"], evidence["relativePath"]), "J-TR-ORIGIN")
    need(origin["attributionPath"] == join_root(origin_set["evidence"]["rootPath"], evidence["relativePath"]), "J-TR-ORIGIN")


def admit_test_reachability(rows, projection, origin_sets, recognition, ctx):
    resolution = {s["subjectId"]: s for s in ctx["resolution"]}
    chosen = [s for s in ctx["resolution"] if s["state"] == "descriptor-not-retained" or s["endpoint"]["kind"] == "symbol"]
    need(projection == item_projection(len(chosen), min(len(chosen), MAX_TEST_REACHABILITY), "item-cap")
         and [r["subjectId"] for r in rows] == sorted((s["subjectId"] for s in chosen[:MAX_TEST_REACHABILITY]), key=lambda x: x.encode()), "J-TR-TOTALITY")
    units = {u["unitOrdinal"]: u for u in recognition.get("units", [])}
    sets = {}
    for origin_set in origin_sets:
        if origin_set["source"] == "rust-test-targets":
            need(origin_set["completeness"] == "partial" and "in-target-unit-tests-not-identified" in origin_set["limitations"], "J-TR-ORIGIN-SET")
        if origin_set["source"] == "recognized-test-globs":
            need((origin_set["completeness"] == "declared") == (not origin_set["limitations"]), "J-TR-ORIGIN-SET")
            evidence, unit = origin_set["evidence"], units.get(origin_set["evidence"]["unitOrdinal"])
            retained = [{"recognizerId": r["recognizerId"], "testGlobs": r["testGlobs"], "unresolvedChoices": r["unresolvedChoices"], "evidence": r["evidence"]}
                        for r in (unit["recognizers"] if unit else []) if r["recognizerId"] == "vitest-jest"]
            need(unit is not None and recognition["state"] == "plan-bound" and unit["rootPath"] == evidence["rootPath"] and unit["markerPath"] == evidence["markerPath"]
                 and unit["recognitionId"] == evidence["recognitionId"] and evidence["recognizers"] == retained, "J-TR-ORIGIN-SET",
                 "test globs must be the retained vitest-jest recognition of the embedded unit")
            need(("recognizer-unresolved-choices" in origin_set["limitations"]) == any(r["unresolvedChoices"] for r in retained), "J-TR-ORIGIN-SET")
        sets[origin_set["universe"]] = origin_set
    for row in rows:
        subject = resolution[row["subjectId"]]
        if row["state"] == "unknown" and row["cause"] == "subject-descriptor-not-retained":
            need(subject["state"] == "descriptor-not-retained", "J-TR-SUBJECT")
            continue
        need(subject["state"] == "resolved" and subject["endpoint"]["kind"] == "symbol", "J-TR-SUBJECT")
        target = subject["endpoint"]
        origin_set = sets.get(target["universe"])
        need(origin_set is not None, "J-TR-ORIGIN-SET")
        if row["state"] == "is-test-origin":
            admit_origin_evidence(row, origin_set)
            continue
        if row["state"] == "unknown":
            if row["cause"] == "no-test-origin-identity":
                need(origin_set["completeness"] == "none", "J-TR-STATE")
            else:
                need(origin_set["completeness"] != "none", "J-TR-STATE")
            continue
        need(origin_set["completeness"] != "none", "J-TR-STATE")
        reach = row["reach"]
        need(reach["request"] == reach_request(ctx["projectId"], ctx["runId"], target, HOST_PAGE_SIZE), "J-TR-REQUEST")
        context = reach["responseContext"]
        need(context["projectId"] == ctx["projectId"] and context["resolvedView"] == {"runId": ctx["runId"]}, "J-TR-RUN")
        need("native-evidence-unavailable" not in limitation_kinds(context), "J-TR-STATE")
        if row["state"] == "static-path-from-test-origin":
            admit_origin_evidence(row["origin"], origin_set)
            wreq = row["witness"]["request"]
            need(wreq == witness_request(ctx["projectId"], ctx["runId"], row["origin"]["endpoint"], target), "J-TR-WITNESS")
            exchange_ok(wreq, row["witness"]["response"], ctx["projectId"], ctx["runId"], ctx["bounds"], "J-TR")
            need(len(row["witness"]["response"]["items"]) == 1, "J-TR-WITNESS")
        elif row["state"] == "no-static-path-within-bound":
            need(not test_blockers(context, origin_set), "J-TR-STATE")
        else:
            need(row["blockers"] == test_blockers(context, origin_set) and row["blockers"], "J-TR-BLOCKERS")


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
# panels

SYMBOL_EVIDENCE_PROVENANCE = {
    "verifiedInDocument": ["entry-summary-recomputed-from-recognizers", "explicit-entry-points-replace-recognized", "metric-reading-recomputed-from-owner-context",
                           "metric-request-recomputed-from-catalog-and-subject", "owner-page-law", "rows-match-request", "run-equals-envelope-run",
                           "test-origin-glob-matched-on-unit-relative-path", "trace-path-request-start-is-embedded-origin-row", "trace-state-and-blockers-recomputed",
                           "unit-id-subset-of-test-targets", "witness-path-request-from-origin-to-subject"],
    "hostAsserted": ["origin-symbol-path-from-plan-bound-symbol-inventory", "recognition-id-over-unembedded-entry-paths", "recognition-parameter-availability",
                     "test-origin-membership-of-unembedded-rows", "test-reach-rows-contain-no-identified-origin"],
}


def derive_symbol_evidence(world, resolution, metric_budget, start_resolver=None, name_resolver=None, owner=None):
    owner = owner or EvidenceGraphOwner(world)
    metrics, metrics_projection = derive_metrics(world, owner, resolution, metric_budget)
    recognition = entry_recognition_panel(world)
    traces, traces_projection = derive_traces(world, owner, resolution, start_resolver)
    reach_rows, reach_projection, origin_sets = derive_test_reachability(world, owner, resolution, name_resolver)
    return {"policy": SYMBOL_EVIDENCE_POLICY, "runId": world.run_id, "metricCatalog": METRIC_IDS, "metrics": metrics, "metricsProjection": metrics_projection,
            "entryRecognition": recognition, "traces": traces, "tracesProjection": traces_projection, "testOrigins": origin_sets,
            "testReachability": reach_rows, "testReachabilityProjection": reach_projection, "provenance": SYMBOL_EVIDENCE_PROVENANCE}


def admit_panel_prerequisites(panels):
    """symbolEvidence subjects are the graph panel's subjects: without a present graph panel it must be unavailable/prerequisite-panel-not-present."""
    evidence = panels.get("symbolEvidence")
    if evidence is not None and panels.get("graph", {}).get("state") != "present":
        need(evidence == {"state": "unavailable", "reason": "prerequisite-panel-not-present"}, "J-SE-PREREQUISITE")


def admit_symbol_evidence(panel, ctx):
    need(panel["runId"] == ctx["runId"], "J-SE-RUN")
    need(ctx["resolution"] == ctx["graphResolution"], "J-SE-SUBJECTS", "subjects are exactly the graph panel subject resolution")
    admit_symbol_metrics(panel["metrics"], panel["metricsProjection"], ctx)
    admit_entry_recognition(panel["entryRecognition"])
    admit_traces(panel["traces"], panel["tracesProjection"], panel["entryRecognition"], ctx)
    admit_test_reachability(panel["testReachability"], panel["testReachabilityProjection"], panel["testOrigins"], panel["entryRecognition"], ctx)
