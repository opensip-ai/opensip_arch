"""Fixture builder (author-02). Constructions following the cited owner laws; not product engine output.

Units, file membership and framework recognition of every world are produced by EXECUTING the pinned native model
(discover_units, assign_membership, recognize_frameworks) over the world's files, then the proposed native successor functions.
build(M, NM, parent07_fixtures) -> fixtures dict; assemble(desc, M, NM, parameter_sha) -> world data.
"""
import copy
import hashlib

H = lambda label: hashlib.sha256(label.encode()).hexdigest()
PROJECT = "prj1-" + H("evidence-project")
RUN = "run3:" + H("evidence-run")
PLAN = "plan2:" + H("evidence-plan")
SNAPSHOT = "snapshot2:" + H("evidence-snapshot")
UR, US, UW, UL = H("universe:rust"), H("universe:shared"), H("universe:web"), H("universe:legacy")
UT = H("universe:tests")
CLOSURE = "closure2:" + H("provider")
VIEWS = {"imports": H("view:imports"), "calls": H("view:calls"), "reach": H("view:reach")}
MARKERS = ("Cargo.toml", "package.json", "tsconfig.json", "jsconfig.json")
SUFFIX_LANGUAGE = [(".tsx", "typescript"), (".ts", "typescript"), (".js", "javascript"), (".rs", "rust"), (".json", "json"), (".toml", "toml")]
RUST_INPUT_TEMPLATE = {"schemaVersion": 2, "lockfileIdentity": {"path": "Cargo.lock", "contentSha256": "ab" * 32, "lockfileVersion": 4},
                       "dependencySourceSetId": "sha256:" + "44" * 32, "unifiedFeaturesId": "sha256:" + "45" * 32, "nativeContextId": "sha256:" + "46" * 32,
                       "cfgSets": [{"cfgSetId": "primary", "cfg": []}], "rustflags": {"executableSelected": False, "honored": [], "stripped": []},
                       "configProjectionSha256": "47" * 32, "preparedResolution": "none", "executionCapableResolution": False, "preparedOutputSetId": None}


def language(path):
    return next((lang for suffix, lang in SUFFIX_LANGUAGE if path.endswith(suffix)), "unspecified")


def fact_id(label):
    return "fact2:" + H("fact:" + label)


def ep(universe, kind, native_id, manifest=None):
    out = {"universe": universe, "kind": kind, "nativeSubjectId": native_id}
    if manifest is not None:
        out["packageManifestPath"] = manifest
    return out


def fact(label, relation, rung, view, source, target, anchors, occupancy="first-party"):
    return {"factId": fact_id(label), "relation": relation, "resolution": rung, "source": source, "target": target, "targetOccupancy": occupancy,
            "viewDigest": VIEWS[view], "anchors": [{"path": p} for p in anchors]}


def relations(limitations=None, views=("imports", "calls", "reach")):
    names = {"imports": "imports@resolved-target", "calls": "calls@resolved-callee", "reach": "reachability@from-resolved-calls"}
    out = {}
    for short in views:
        out[names[short]] = {"views": [VIEWS[short]], "coverageIds": ["coverage2:" + H("coverage:" + short)], "scopeIds": ["scope2:" + H("scope:" + short)],
                             "deficiencyCitations": [], "resolutionLimitations": copy.deepcopy((limitations or {}).get(short, []))}
    return out


# ---------------------------------------------------------------------------
# world assembly through the pinned native model

def assemble(desc, M, NM, parameter_sha):
    if "dense" in desc:
        desc = dense_desc(desc["dense"], desc.get("projectId", PROJECT), desc.get("runId", RUN))
    files = desc["files"]
    paths = sorted(files)
    raw = {p: files[p].encode("utf-8") for p in paths}
    inventory = [{"path": p, "sha256": hashlib.sha256(raw[p]).hexdigest(), "bytes": len(raw[p])} for p in paths]
    markers = {}
    for p in paths:
        if p.rsplit("/", 1)[-1] in MARKERS:
            markers[p] = {"sha256": hashlib.sha256(raw[p]).hexdigest()}
            if p.endswith("Cargo.toml") and "[workspace]" in files[p]:
                markers[p]["isCargoWorkspace"] = True
    discovery = NM.discover_units(markers)
    membership = NM.assign_membership(discovery["units"], paths)
    NM.validate_native("UnitMembershipV1", membership)
    units = membership["units"]
    membership_digest = M.raw_sha(membership)
    order = lambda values: sorted(set(values), key=lambda v: M.canon(v))
    snapshot = desc.get("snapshotId", SNAPSHOT)
    cells = []
    for program in desc["programs"]:
        root_text = "." if program["root"] == "" else program["root"]
        under = [p for p in paths if program["root"] == "" or p.startswith(program["root"] + "/")]
        symbol_paths = order(row["path"] for row in program["symbols"])
        packages = order(path for path, _ in desc["packages"] if path in under)
        for capability, kinds in (("calls", ["symbol"]), ("imports", ["symbol"]), ("inventory", ["file", "package"])):
            extents = [{"kind": kind, "paths": {"symbol": symbol_paths, "file": order(under), "package": packages}[kind]} for kind in kinds]
            cells.append({"capabilityId": capability, "languageMode": program["mode"], "workspaceRoot": root_text, "required": True, "kinds": kinds,
                          "programBindings": [{"ordinal": 0, "provenance": "default-unit", "enumerator": {"status": "selected", "closureId": CLOSURE},
                                               "nativeContextDigest": H("context:" + program["mode"]), "universe": program["universe"], "programEntry": None,
                                               "extents": extents}], "_program": program})
    cells.sort(key=lambda c: (c["capabilityId"].encode(), c["languageMode"].encode(), c["workspaceRoot"].encode()))
    plan = {"schemaVersion": 1, "snapshotId": snapshot, "scopeDigest": H("scope"), "membershipDigest": membership_digest,
            "cells": [{k: v for k, v in c.items() if k != "_program"} for c in cells]}
    parameter_digest = M.raw_sha(plan)
    names = dict(desc["packages"])
    inventories = []
    for ordinal, cell in enumerate(cells):
        program = cell["_program"]
        for extent in cell["programBindings"][0]["extents"]:
            kind = extent["kind"]
            if kind == "symbol":
                items = [{"nativeSubjectId": r["id"], "kind": "symbol", "path": r["path"], "qualifiedName": r["id"].split(":", 1)[1], "subjectLanguage": language(r["path"]),
                          "exported": "exported", "signatureTokens": [], "projections": []} for r in program["symbols"]]
                items.sort(key=lambda r: r["nativeSubjectId"].encode())
            elif kind == "file":
                items = sorted(({"nativeSubjectId": p, "kind": "file", "path": p, "qualifiedName": p, "subjectLanguage": language(p), "signatureTokens": [], "projections": []}
                                for p in extent["paths"]), key=lambda r: r["nativeSubjectId"].encode())
            else:
                items = sorted(({"nativeSubjectId": names[p], "kind": "package", "path": p, "qualifiedName": names[p], "subjectLanguage": language(p), "signatureTokens": [],
                                 "projections": []} for p in extent["paths"]), key=lambda r: (r["nativeSubjectId"].encode(), r["path"].encode()))
            key = "%s|%s|%s" % (cell["capabilityId"], program["universe"], kind)
            state = desc.get("inventoryStates", {}).get(key, "complete")
            if state == "partial":
                dropped = desc.get("inventoryDrops", {}).get(key, [])
                items = [r for r in items if r["path"] not in dropped and r["nativeSubjectId"] not in dropped]
            inventories.append({"schemaVersion": 1, "planId": PLAN, "parameterDigest": parameter_digest, "cellOrdinal": ordinal, "programOrdinal": 0, "kind": kind,
                                "state": state, "deficiency": None if state == "complete" else "budget-exhausted", "nativeCause": None, "examinedPaths": extent["paths"], "rows": items})
    ownership, rust_inputs = {}, {}
    for universe, spec in desc.get("ownership", {}).items():
        declared = []
        for marker, crate, kind, name, edition in spec["units"]:
            unit = {"markerPath": marker, "crateName": crate, "targetKind": kind, "targetName": name, "targetEdition": edition}
            unit["unitId"] = M.native_h(M.COMPILATION_UNIT_DOMAIN, {"schemaVersion": 1, "markerPath": marker, "targetKind": kind, "targetName": name})
            declared.append(unit)
        by_name = {(u["markerPath"], u["targetKind"], u["targetName"]): u["unitId"] for u in declared}
        own_rows = sorted(({"path": path, "unitId": by_name[tuple(target)]} for path, targets in spec["owners"].items() for target in targets),
                          key=lambda r: (r["path"].encode(), r["unitId"].encode()))
        record = {"schemaVersion": 1, "enumeration": spec.get("enumeration", "complete"), "units": sorted(declared, key=lambda u: u["unitId"].encode()),
                  "selectedUnitIds": sorted((by_name[tuple(t)] for t in spec["selected"]), key=lambda x: x.encode()), "ownership": own_rows}
        ownership[universe] = record
        rust_inputs[universe] = dict(copy.deepcopy(RUST_INPUT_TEMPLATE), edition={u["crateName"]: 2021 for u in declared},
                                     crateRootPaths=sorted(spec["crateRoots"]), sourceUnitOwnershipId=M.native_h(M.SOURCE_UNIT_OWNERSHIP_DOMAIN, record))
    explicit = sorted(desc["recognition"]["explicit"], key=lambda p: M.canon(p))
    rows_out, native_results = [], {}
    for unit in units:
        if unit["languageFamily"] not in ("rust", "tsjs"):
            continue
        root = unit["rootPath"]
        sub = {(p if root == "" else p[len(root) + 1:]): files[p] for p in paths if root == "" or p.startswith(root + "/")}
        native = NM.recognize_frameworks(sub)
        native_results[unit["unitOrdinal"]] = native
        rec = M.successor_recognition(native, root, sub, explicit)
        rows_out.append({"unitOrdinal": unit["unitOrdinal"], "rootPath": root, "markerPath": unit["markerPath"], "recognitionId": M.native_h(M.RECOGNITION_DOMAIN, rec),
                         "recognition": rec})
    record = {"schemaVersion": 1, "snapshotId": snapshot, "membershipDigest": membership_digest, "explicitEntryPoints": explicit, "units": rows_out}
    payload = M.raw_sha(record)
    plan_bound = desc["recognition"].get("planBound", True)
    parameters = sorted([{"schemaDigest": H("doc:enumeration-plan"), "payloadDigest": parameter_digest}]
                        + ([{"schemaDigest": parameter_sha, "payloadDigest": payload}] if plan_bound else []), key=lambda p: M.canon(p))
    availability = desc["recognition"].get("availability", {"state": "retained", "parameterMissing": False})
    retained = {} if availability.get("parameterMissing") or not plan_bound else {payload: record}
    return {
        "projectId": desc.get("projectId", PROJECT), "runId": desc.get("runId", RUN), "snapshotId": snapshot,
        "snapshotInventory": inventory, "membership": membership, "enumerationPlan": plan, "subjectInventories": inventories,
        "sourceUnitOwnership": ownership, "rustUniverses": rust_inputs, "nativeRecognition": native_results, "recognitionRecord": record,
        "analysisSpecParameters": parameters, "parameterDocumentSha256": parameter_sha,
        "parameterAvailability": {"state": availability["state"], "missingDigests": [payload] if availability.get("parameterMissing") else []},
        "retainedParameterPayloads": retained, "resolvedConfigurationEntryPoints": explicit, "availability": desc.get("availability", "retained"),
        "testBounds": desc.get("testBounds"), "facts": desc["facts"], "syntheticFanIn": desc.get("fanIn", []), "relations": desc["relations"],
    }


# ---------------------------------------------------------------------------
# mixed Rust + TS/JS world

RUST_SYMBOLS = [("rs:svc::main", "src/main.rs"), ("rs:core::lib", "crates/core/src/lib.rs"), ("rs:core::parse", "crates/core/src/parse.rs"),
                ("rs:core::shared_fmt", "crates/core/src/shared.rs"), ("rs:core::both", "crates/core/src/both.rs"), ("rs:core::it_parses", "crates/core/tests/it.rs"),
                ("rs:app::main", "crates/app/src/main.rs"), ("rs:app::util", "crates/app/src/vendored/util.rs"), ("rs:app::orphan", "crates/app/src/orphan.rs"),
                ("rs:app::bench_only", "crates/app/benches/b.rs")]
WEB_SYMBOLS = [("ts:web/api", "packages/web/src/api.ts"), ("ts:web/button", "packages/web/src/button.tsx"), ("ts:web/button.test", "packages/web/src/button.test.tsx"),
               ("ts:web/next-config", "packages/web/next.config.js"), ("ts:web/page", "packages/web/app/page.tsx"), ("ts:web/shared-format", "packages/shared/src/format.ts")]


def mixed_desc():
    rs = lambda n: ep(UR, "symbol", n)
    web = lambda n: ep(UW, "symbol", n)
    path_of = dict(RUST_SYMBOLS + WEB_SYMBOLS + [("ts:legacy/old", "packages/web-legacy/src/old.ts")])
    files = {"Cargo.toml": "[workspace]\nmembers = [\"crates/app\", \"crates/core\"]\n\n[package]\nname = \"svc\"\n", "src/main.rs": "fn main() {}\n",
             "crates/core/Cargo.toml": "[package]\nname = \"core\"\n", "crates/core/src/lib.rs": "pub mod parse;\n", "crates/core/src/parse.rs": "pub fn parse() {}\n",
             "crates/core/src/shared.rs": "pub fn shared_fmt() {}\n", "crates/core/src/both.rs": "pub fn both() {}\n", "crates/core/tests/it.rs": "#[test] fn it_parses() {}\n",
             "crates/app/Cargo.toml": "[package]\nname = \"app\"\n", "crates/app/src/main.rs": "fn main() {}\n", "crates/app/src/vendored/util.rs": "pub fn util() {}\n",
             "crates/app/src/orphan.rs": "fn orphan() {}\n", "crates/app/benches/b.rs": "fn bench_only() {}\n",
             "packages/shared/package.json": "{\"name\":\"@fx/shared\",\"private\":true}", "packages/shared/src/format.ts": "export const format = 1;\n",
             "packages/web/package.json": "{\"name\":\"@fx/web\",\"private\":true,\"jest\":{}}", "packages/web/tsconfig.json": "{}",
             "packages/web/next.config.js": "module.exports = {};\n", "packages/web/app/page.tsx": "export default function Page() {}\n",
             "packages/web/src/button.tsx": "export function Button() {}\n", "packages/web/src/button.test.tsx": "test('button', () => {});\n",
             "packages/web/src/api.ts": "export function api() {}\n", "packages/web-legacy/tsconfig.json": "{}", "packages/web-legacy/src/old.ts": "export function old() {}\n",
             "packages/web-legacy/src/old.test.ts": "test('old', () => {});\n"}
    programs = [
        {"root": "", "mode": "rust-cargo", "universe": UR, "symbols": [{"id": i, "path": p} for i, p in RUST_SYMBOLS]},
        {"root": "packages/shared", "mode": "js-synthesized", "universe": US, "symbols": [{"id": "ts:shared/format", "path": "packages/shared/src/format.ts"}]},
        {"root": "packages/web", "mode": "ts-tsconfig", "universe": UW, "symbols": [{"id": i, "path": p} for i, p in WEB_SYMBOLS]},
        {"root": "packages/web-legacy", "mode": "ts-tsconfig", "universe": UL, "symbols": [
            {"id": "ts:legacy/old", "path": "packages/web-legacy/src/old.ts"}, {"id": "ts:legacy/old.test", "path": "packages/web-legacy/src/old.test.ts"}]},
    ]
    packages = [("Cargo.toml", "svc"), ("crates/core/Cargo.toml", "core"), ("crates/app/Cargo.toml", "app"), ("packages/shared/package.json", "@fx/shared"),
                ("packages/web/package.json", "@fx/web")]
    ownership = {UR: {"units": [("Cargo.toml", "svc", "bin", "svc", None), ("crates/core/Cargo.toml", "core", "lib", "core", None),
                                ("crates/core/Cargo.toml", "core", "test", "it", None), ("crates/app/Cargo.toml", "app", "bin", "app", None),
                                ("crates/app/Cargo.toml", "app", "bench", "b", None)],
                      "selected": [("Cargo.toml", "bin", "svc"), ("crates/core/Cargo.toml", "lib", "core"), ("crates/core/Cargo.toml", "test", "it"),
                                   ("crates/app/Cargo.toml", "bin", "app")],
                      "owners": {"src/main.rs": [("Cargo.toml", "bin", "svc")], "crates/core/src/lib.rs": [("crates/core/Cargo.toml", "lib", "core")],
                                 "crates/core/src/parse.rs": [("crates/core/Cargo.toml", "lib", "core")],
                                 "crates/core/src/shared.rs": [("crates/core/Cargo.toml", "lib", "core"), ("crates/app/Cargo.toml", "bin", "app")],
                                 "crates/core/src/both.rs": [("crates/core/Cargo.toml", "lib", "core"), ("crates/core/Cargo.toml", "test", "it")],
                                 "crates/core/tests/it.rs": [("crates/core/Cargo.toml", "test", "it")], "crates/app/src/main.rs": [("crates/app/Cargo.toml", "bin", "app")],
                                 "crates/app/src/vendored/util.rs": [("crates/core/Cargo.toml", "lib", "core")],
                                 "crates/app/benches/b.rs": [("crates/app/Cargo.toml", "bench", "b")]},
                      "crateRoots": ["src/main.rs", "crates/core/src/lib.rs", "crates/core/tests/it.rs", "crates/app/src/main.rs", "crates/app/benches/b.rs"]}}
    I = lambda label, source, target, anchors=None, occ="first-party": fact(label, "imports", "resolved-target", "imports", source, target,
                                                                           anchors or [path_of[source["nativeSubjectId"]]], occ)
    imports = [
        I("i01", rs("rs:app::main"), ep(UR, "package", "core", "crates/core/Cargo.toml")),
        I("i02", rs("rs:app::main"), rs("rs:core::parse")),
        I("i03-provenance-duplicate-of-i02", rs("rs:app::main"), rs("rs:core::parse")),
        I("i04", rs("rs:core::shared_fmt"), rs("rs:core::parse")),
        I("i05", rs("rs:app::util"), rs("rs:core::lib")),
        I("i06", rs("rs:svc::main"), ep(UR, "package", "app", "crates/app/Cargo.toml")),
        I("i07", rs("rs:app::orphan"), rs("rs:core::parse")),
        I("i08", rs("rs:app::bench_only"), rs("rs:core::parse")),
        I("i09", rs("rs:ghost"), rs("rs:core::parse"), ["crates/app/src/orphan.rs"]),
        I("i10", web("ts:web/api"), ep(US, "package", "@fx/shared", "packages/shared/package.json")),
        I("i11", web("ts:web/api"), ep(US, "file", "packages/shared/src/format.ts")),
        I("i12", web("ts:web/button"), ep(UW, "package", "lodash", "node_modules/lodash/package.json"), None, "external"),
        I("i13", web("ts:web/button"), ep(UW, "symbol", "ts:external/x"), None, "external"),
        I("i14", web("ts:web/page"), ep(UW, "symbol", "ts:web/unknown"), None, "unknown"),
        I("i15", ep(UL, "symbol", "ts:legacy/old"), web("ts:web/button")),
        I("i16", web("ts:web/shared-format"), web("ts:web/button")),
        I("i17", web("ts:web/button.test"), web("ts:web/button")),
        I("i18-anchor-not-symbol-path", web("ts:web/api"), web("ts:web/button"), ["packages/web-legacy/src/old.ts"]),
        I("i19-anchor-owners-disagree", rs("rs:core::both"), rs("rs:core::parse"), ["crates/core/src/both.rs", "crates/app/src/main.rs"]),
    ]
    C_ = lambda label, source, target, view="calls", rel="calls", rung="resolved-callee": fact(label, rel, rung, view, source, target, [path_of[source["nativeSubjectId"]]])
    calls = [C_("c01", rs("rs:svc::main"), rs("rs:core::parse")), C_("c02", rs("rs:core::it_parses"), rs("rs:core::both")), C_("c03", rs("rs:core::both"), rs("rs:core::parse")),
             C_("c04", rs("rs:app::main"), rs("rs:core::shared_fmt")), C_("c05", rs("rs:core::shared_fmt"), rs("rs:core::parse")),
             C_("c06", web("ts:web/page"), web("ts:web/button")), C_("c07", web("ts:web/button"), web("ts:web/api")),
             C_("c08", web("ts:web/button.test"), web("ts:web/button")), C_("c09", web("ts:web/api"), web("ts:web/shared-format"))]
    R_ = lambda label, source, target: C_(label, source, target, "reach", "reachability", "from-resolved-calls")
    reach = [R_("r01", rs("rs:svc::main"), rs("rs:core::parse")), R_("r02", rs("rs:app::main"), rs("rs:core::parse")),
             R_("r03", rs("rs:app::main"), rs("rs:core::shared_fmt")), R_("r04", web("ts:web/page"), web("ts:web/button")), R_("r05", web("ts:web/page"), web("ts:web/api"))]
    limitations = {"imports": [{"kind": "unresolved-edge-present", "relation": "imports", "minResolution": "resolved-target", "unresolvedEdgeCount": 2}]}
    return {"files": files, "programs": programs, "packages": packages, "ownership": ownership, "recognition": {"explicit": []},
            "facts": imports + calls + reach, "relations": relations(limitations)}


def mixed_resolution(M):
    subjects = [ep(UR, "symbol", "rs:core::parse"), ep(UR, "symbol", "rs:core::shared_fmt"), ep(UW, "symbol", "ts:web/api"), ep(UW, "symbol", "ts:web/button.test"),
                ep(US, "package", "@fx/shared", "packages/shared/package.json"), ep(UR, "symbol", "rs:core::both"), ep(UL, "symbol", "ts:legacy/old")]
    out = [{"subjectId": M.RM.subject_id(e), "state": "resolved", "endpoint": e} for e in subjects]
    out.insert(5, {"subjectId": "subject3:" + H("descriptor-not-retained"), "state": "descriptor-not-retained"})
    return out


def clean_coupling_desc():
    desc = mixed_desc()
    bad = {fact_id(x) for x in ("i07", "i08", "i09", "i12", "i13", "i14", "i19-anchor-owners-disagree")}
    desc["facts"] = [f for f in desc["facts"] if f["factId"] not in bad]
    desc["relations"] = relations()
    return desc


# ---------------------------------------------------------------------------
# integration world aligned to parent07 audit-full

def integration_desc(base):
    envelope = base["envelope"]
    resolution = base["panels"]["graph"]["data"]["subjectResolution"]
    universe = next(r["endpoint"]["universe"] for r in resolution if r["state"] == "resolved")
    S = lambda n: ep(universe, "symbol", n)
    files = {"package.json": "{\"name\":\"fixture-app\",\"private\":true,\"jest\":{}}", "tsconfig.json": "{}", "src/index.ts": "export function main() {}\n",
             "src/helper.ts": "export function helper() {}\n", "src/helper.test.ts": "test('helper', () => {});\n", "src/legacy.js": "module.exports = {};\n",
             "packages/util/package.json": "{\"name\":\"npm:@fixture/util\",\"private\":true}", "packages/util/src/u.ts": "export const u = 1;\n"}
    programs = [{"root": "", "mode": "ts-tsconfig", "universe": universe, "symbols": [
        {"id": "ts:src/index.ts#main", "path": "src/index.ts"}, {"id": "ts:src/helper.ts#helper", "path": "src/helper.ts"},
        {"id": "ts:src/helper.test.ts#t", "path": "src/helper.test.ts"}]}]
    packages = [("package.json", "fixture-app"), ("packages/util/package.json", "npm:@fixture/util")]
    facts = [
        fact("a-c1", "calls", "resolved-callee", "calls", S("ts:src/index.ts#main"), S("ts:src/helper.ts#helper"), ["src/index.ts"]),
        fact("a-c2", "calls", "resolved-callee", "calls", S("ts:src/helper.test.ts#t"), S("ts:src/helper.ts#helper"), ["src/helper.test.ts"]),
        fact("a-r1", "reachability", "from-resolved-calls", "reach", S("ts:src/index.ts#main"), S("ts:src/helper.ts#helper"), ["src/index.ts"]),
        fact("a-i1", "imports", "resolved-target", "imports", S("ts:src/index.ts#main"), ep(universe, "package", "npm:@fixture/util", "packages/util/package.json"), ["src/index.ts"]),
        fact("a-i2", "imports", "resolved-target", "imports", S("ts:src/index.ts#main"), ep(universe, "file", "src/legacy.js"), ["src/index.ts"]),
    ]
    return {"files": files, "programs": programs, "packages": packages, "recognition": {"explicit": ["src/index.ts"]}, "facts": facts,
            "relations": relations(), "projectId": envelope["projectId"], "runId": envelope["run"]["runId"]}, resolution


def cross_universe_test_desc(base):
    """review01 C1: the test file lives in its own tsjs unit/universe and calls helper across universes."""
    desc, resolution = integration_desc(base)
    universe = desc["programs"][0]["universe"]
    desc["files"].pop("src/helper.test.ts")
    desc["files"].update({"tests/package.json": "{\"name\":\"fixture-tests\",\"private\":true,\"jest\":{}}", "tests/tsconfig.json": "{}",
                          "tests/helper.test.ts": "test('helper', () => {});\n"})
    desc["programs"][0]["symbols"] = [s for s in desc["programs"][0]["symbols"] if s["path"] != "src/helper.test.ts"]
    desc["programs"].append({"root": "tests", "mode": "ts-tsconfig", "universe": UT, "symbols": [{"id": "ts:tests/helper.test.ts#t", "path": "tests/helper.test.ts"}]})
    desc["packages"].append(("tests/package.json", "fixture-tests"))
    desc["facts"] = [f for f in desc["facts"] if f["factId"] != fact_id("a-c2")]
    desc["facts"].append(fact("x-c2-cross-universe", "calls", "resolved-callee", "calls", ep(UT, "symbol", "ts:tests/helper.test.ts#t"),
                              ep(universe, "symbol", "ts:src/helper.ts#helper"), ["tests/helper.test.ts"]))
    return desc, resolution


def jest_configured_desc(base):
    """review01 C2: package.json jest.testMatch selects *.it.ts files, which the recognizer's default globs do not match."""
    desc, resolution = integration_desc(base)
    universe = desc["programs"][0]["universe"]
    desc["files"]["package.json"] = "{\"name\":\"fixture-app\",\"private\":true,\"jest\":{\"testMatch\":[\"**/*.it.ts\"]}}"
    desc["files"].pop("src/helper.test.ts")
    desc["files"]["src/helper.it.ts"] = "test('helper', () => {});\n"
    for symbol in desc["programs"][0]["symbols"]:
        if symbol["path"] == "src/helper.test.ts":
            symbol.update(id="ts:src/helper.it.ts#t", path="src/helper.it.ts")
    desc["facts"] = [f for f in desc["facts"] if f["factId"] != fact_id("a-c2")]
    desc["facts"].append(fact("j-c2-it", "calls", "resolved-callee", "calls", ep(universe, "symbol", "ts:src/helper.it.ts#t"), ep(universe, "symbol", "ts:src/helper.ts#helper"),
                              ["src/helper.it.ts"]))
    return desc, resolution


def dense_desc(n, project, run):
    """review01 C7: n js packages, every package imports every other package's index symbol."""
    files, programs, packages, facts = {}, [], [], []
    for i in range(n):
        root = "packages/p%03d" % i
        files[root + "/package.json"] = "{\"name\":\"@dense/p%03d\",\"private\":true}" % i
        files[root + "/src/index.ts"] = "export const p%03d = 1;\n" % i
        programs.append({"root": root, "mode": "js-synthesized", "universe": H("dense-u%d" % i), "symbols": [{"id": "ts:p%03d/index" % i, "path": root + "/src/index.ts"}]})
        packages.append((root + "/package.json", "@dense/p%03d" % i))
    for i in range(n):
        for j in range(n):
            if i != j:
                facts.append(fact("dense-%d-%d" % (i, j), "imports", "resolved-target", "imports", ep(H("dense-u%d" % i), "symbol", "ts:p%03d/index" % i),
                                  ep(H("dense-u%d" % j), "symbol", "ts:p%03d/index" % j), ["packages/p%03d/src/index.ts" % i]))
    return {"files": files, "programs": programs, "packages": packages, "recognition": {"explicit": []}, "facts": facts, "relations": relations(views=("imports",)),
            "projectId": project, "runId": run}


# ---------------------------------------------------------------------------
# variants over mixed / integration

def variants(M):
    def core_package_partial(desc):
        desc["inventoryStates"] = {"inventory|%s|package" % UR: "partial"}
        desc["inventoryDrops"] = {"inventory|%s|package" % UR: ["crates/core/Cargo.toml"]}
        return desc

    def not_plan_bound(desc):
        desc["recognition"]["planBound"] = False
        return desc

    def purged(desc):
        desc["recognition"]["availability"] = {"state": "purged", "parameterMissing": True}
        return desc

    def partial_missing(desc):
        desc["recognition"]["availability"] = {"state": "partial", "parameterMissing": True}
        return desc

    def partial_present(desc):
        desc["recognition"]["availability"] = {"state": "partial", "parameterMissing": False}
        return desc

    def no_reachability(desc):
        desc["relations"] = relations({"imports": desc["relations"]["imports@resolved-target"]["resolutionLimitations"]}, views=("imports", "calls"))
        return desc

    def many_origins(desc):
        for i in range(101):
            desc["facts"].append(fact("many-%03d" % i, "reachability", "from-resolved-calls", "reach", ep(UR, "symbol", "rs:app::bench_only"),
                                      ep(UR, "symbol", "rs:core::both"), ["crates/app/benches/b.rs"]))
        return desc

    def fan_in(desc):
        desc["fanIn"] = [{"name": "lib", "count": 100001, "relation": "calls", "resolution": "resolved-callee", "viewDigest": VIEWS["calls"],
                          "sourceTemplate": ep(UR, "symbol", "rs:gen::f"), "target": ep(UR, "symbol", "rs:core::lib"), "anchors": [{"path": "crates/core/src/lib.rs"}]}]
        return desc

    def run_purged(desc):
        desc["availability"] = "purged"
        return desc

    def member_root_unresolved(desc):
        desc["ownership"][UR]["crateRoots"] = [p for p in desc["ownership"][UR]["crateRoots"] if p != "crates/app/src/main.rs"]
        return desc

    def whole_view_test_bound(desc):
        desc["testBounds"] = {"maxItemsPerOperation": 10}
        return desc

    def zero_under_limitation(desc):
        desc["relations"]["calls@resolved-callee"]["resolutionLimitations"] = [{"kind": "unresolved-edge-present", "relation": "calls", "minResolution": "resolved-callee",
                                                                               "unresolvedEdgeCount": 1}]
        return desc

    def cross_program_duplicate(desc):
        desc["facts"].append(fact("i20-same-source-other-program", "imports", "resolved-target", "imports", ep(US, "symbol", "ts:shared/format"),
                                  ep(UW, "symbol", "ts:web/button"), ["packages/shared/src/format.ts"]))
        return desc

    def reached_universe_without_identity(desc):
        desc["facts"].append(fact("c10-legacy-calls-rust", "calls", "resolved-callee", "calls", ep(UL, "symbol", "ts:legacy/old"), ep(UR, "symbol", "rs:core::shared_fmt"),
                                  ["packages/web-legacy/src/old.ts"]))
        return desc

    return {"mixed-reached-universe-without-identity": reached_universe_without_identity, "mixed-core-package-partial": core_package_partial, "mixed-not-plan-bound": not_plan_bound, "mixed-recognition-purged": purged,
            "mixed-recognition-partial-missing": partial_missing, "mixed-recognition-partial-present": partial_present,
            "mixed-no-reachability-view": no_reachability, "mixed-many-origins": many_origins, "mixed-fan-in-100001": fan_in, "mixed-run-evidence-purged": run_purged,
            "mixed-cargo-member-root-unresolved": member_root_unresolved, "mixed-whole-view-test-bound": whole_view_test_bound,
            "mixed-zero-under-limitation": zero_under_limitation, "mixed-cross-program-duplicate": cross_program_duplicate}


# ---------------------------------------------------------------------------
# adversarial resolvers

def prefix_guess(world, row):
    path = row["anchorPaths"][0]
    manifests = {r["path"] for inv in world.inventories if inv["kind"] == "package" for r in inv["rows"]}
    best = max((m for m in manifests if path.startswith(m.rsplit("/", 1)[0] if "/" in m else "")), key=len)
    return [{"keyKind": "first-party-package", "path": best}], None


def spelling_parse(world, row):
    sid = row["source"]["nativeSubjectId"]
    if sid.startswith("rs:"):
        crate = sid[3:].split("::")[0]
        return [{"keyKind": "first-party-package", "path": {"svc": "Cargo.toml"}.get(crate, "crates/%s/Cargo.toml" % crate)}], None
    return world.path_owner_keys(row["source"]["universe"], row["anchorPaths"][0])


def symbol_path_owner(world, row):
    path, cause = world.symbol_attribution(row["source"]["universe"], row["source"]["nativeSubjectId"])
    if cause:
        return None, "importer-anchor-missing"
    return world.path_owner_keys(row["source"]["universe"], path)


def ownership_as_package(world, row):
    universe, path = row["source"]["universe"], row["anchorPaths"][0]
    if world.family(universe) != "rust":
        return world.path_owner_keys(universe, path)
    record = world.ownership[universe]
    units = {u["unitId"]: u for u in record["units"]}
    markers = sorted({units[r["unitId"]]["markerPath"] for r in record["ownership"] if r["path"] == path})
    return ([{"keyKind": "first-party-package", "path": m} for m in markers] or None), (None if markers else "not-compiled-by-selected-targets")


def browser_entry_name(world, origin):
    path, cause = world.symbol_attribution(origin["universe"], origin["nativeSubjectId"])
    if cause or not origin["nativeSubjectId"].endswith(("main", "page")):
        return None
    unit = world.unit_for_universe(origin["universe"])
    row = next(r for r in world.recognition_record()["units"] if r["unitOrdinal"] == unit["unitOrdinal"])
    result = next(r for r in row["recognition"]["recognized"] if r["effects"]["entryPoints"])
    return path, [{"source": "recognized", "unitOrdinal": unit["unitOrdinal"], "recognizerId": result["recognizerId"], "recognizerVersion": 1,
                   "assurance": result["assurance"], "evidence": copy.deepcopy(result["evidence"]), "unresolvedChoices": list(result["unresolvedChoices"])}]


def test_name_guess(world, universe, by_symbol):
    unit = world.unit_for_universe(universe)
    record = world.recognition_record()
    row = next((r for r in record["units"] if unit and r["unitOrdinal"] == unit["unitOrdinal"]), None) if record else None
    base = {"universe": universe, "interpretation": "native-static-origin-identity-not-imported-execution"}
    if unit is None or row is None:
        return dict(base, source="none", completeness="none", cause="universe-not-plan-bound", limitations=[], originCount=0), {}
    origins = {}
    for sid, paths in sorted(by_symbol.items()):
        path = next(iter(paths))
        if "test" in sid and (unit["rootPath"] == "" or path.startswith(unit["rootPath"] + "/")):
            relative = path if unit["rootPath"] == "" else path[len(unit["rootPath"]) + 1:]
            origins[sid] = {"attributionPath": path, "originEvidence": {"kind": "recognized-test-glob", "unitOrdinal": unit["unitOrdinal"], "recognizerId": "vitest-jest",
                                                                         "glob": "**/*test*", "relativePath": relative}}
    evidence = {"unitOrdinal": unit["unitOrdinal"], "rootPath": unit["rootPath"], "markerPath": unit["markerPath"], "recognitionId": row["recognitionId"],
                "recognizers": [{"recognizerId": "vitest-jest", "testGlobs": ["**/*test*"], "unresolvedChoices": [],
                                 "evidence": [{"path": unit["markerPath"], "contentSha256": world.inventory[unit["markerPath"]]["sha256"], "field": "name-guess"}]}]}
    return dict(base, source="recognized-test-globs", completeness="partial", limitations=["recognizer-globs-not-test-population"], originCount=len(origins), evidence=evidence), origins


def imported_test_id(world, universe, by_symbol):
    origin_set, origins = test_name_guess(world, universe, by_symbol)
    for sid in origins:
        origins[sid]["originEvidence"] = {"kind": "imported-test-id", "importId": "import2:" + H("test-import"), "testId": sid}
    return origin_set, origins


RESOLVERS = {"prefix-guess": prefix_guess, "symbol-spelling-parse": spelling_parse, "ownership-as-package": ownership_as_package, "symbol-path-not-anchor": symbol_path_owner}
START_RESOLVERS = {"browser-entry-name": browser_entry_name}
ORIGIN_RESOLVERS = {"test-name-guess": test_name_guess, "imported-test-id": imported_test_id}


# ---------------------------------------------------------------------------
# cases

def op(path, value=None, kind="set"):
    return {"op": kind, "path": path, "value": value} if kind != "remove" else {"op": "remove", "path": path}


def document_cases():
    return [
        {"id": "coupling-owner-record-not-key", "panel": "coupling", "ops": [op("/owners/@core/packageManifestPath", "crates/core2/Cargo.toml")], "expect": "J-COUPLING-OWNER-KEY"},
        {"id": "coupling-cargo-target-unit-id-tampered", "panel": "coupling", "ops": [op("/owners/@core/cargoTargets/0/unitId", "sha256:" + H("x"))], "expect": "J-COUPLING-OWNER-KEY"},
        {"id": "coupling-facts-below-edges", "panel": "coupling", "ops": [op("/cells/@app-core/programEdges", 5)], "expect": "J-COUPLING-COUNT"},
        {"id": "coupling-source-dependencies-above-facts", "panel": "coupling", "ops": [op("/cells/@app-core/sourceDependencies", 5)], "expect": "J-COUPLING-COUNT"},
        {"id": "coupling-provenance-duplicate-collapsed", "panel": "coupling", "ops": [op("/cells/@app-core/facts", 3)], "expect": "J-COUPLING-TOTALS"},
        {"id": "coupling-cells-priority-order-broken", "panel": "coupling", "ops": [{"op": "swap", "path": "/cells", "i": 0, "j": 7}], "expect": "J-COUPLING-ORDER"},
        {"id": "coupling-importer-bucket-dropped", "panel": "coupling", "ops": [op("/importerBuckets/0", kind="remove")], "expect": "J-COUPLING-TOTALS"},
        {"id": "coupling-blank-cell-absence-claimed", "panel": "coupling", "ops": [op("/absence/absenceSupported", True)], "expect": "J-COUPLING-ABSENCE"},
        {"id": "coupling-blockers-erased", "panel": "coupling", "ops": [op("/absence/blockers", []), op("/absence/absenceSupported", True)], "expect": "J-COUPLING-ABSENCE"},
        {"id": "coupling-blank-cell-means-no-dependency", "panel": "coupling", "ops": [op("/absence/blankCellMeans", "no-dependency")], "expect": "SCHEMA"},
        {"id": "coupling-extra-owner-not-referenced", "panel": "coupling", "ops": [op("/owners", "@owners-plus-unreferenced")], "expect": "J-COUPLING-OWNER-CLOSURE"},
        {"id": "coupling-run-mismatch", "panel": "coupling", "ops": [op("/runId", "run3:" + H("other-run"))], "expect": "J-COUPLING-RUN"},
        {"id": "coupling-cells-projection-hides-omission", "panel": "coupling", "ops": [op("/cellsProjection/total", 9)], "expect": "J-COUPLING-PROJECTION"},
        {"id": "coupling-drilldown-row-moved-to-absent-cell", "panel": "coupling", "ops": [op("/drilldown/@drill-svc-app/toOwnerKey", "@web"),
                                                                                           {"op": "resort", "path": "/drilldown", "by": ["fromOwnerKey", "toOwnerKey", "factId"]}],
         "expect": "J-COUPLING-DRILL"},
        {"id": "metric-value-not-total", "panel": "symbolEvidence", "ops": [op("/metrics/@parse-in/value", 7)], "expect": "J-METRIC-VALUE"},
        {"id": "metric-state-lower-bound-on-exact", "panel": "symbolEvidence", "ops": [op("/metrics/@parse-in/countState", "lower-bound")], "expect": "J-METRIC-STATE"},
        {"id": "metric-zero-absence-with-nonzero", "panel": "symbolEvidence", "ops": [op("/metrics/@parse-in/zeroSupportsAbsence", True)], "expect": "J-METRIC-ABSENCE"},
        {"id": "metric-runtime-hotness-id", "panel": "symbolEvidence", "ops": [op("/metrics/@parse-in/metricId", "runtime-hotness")], "expect": "SCHEMA"},
        {"id": "metric-request-direction-swapped", "panel": "symbolEvidence", "ops": [op("/metrics/@parse-in/request/params/direction", "outgoing")], "expect": "J-METRIC-REQUEST"},
        {"id": "metric-response-total-not-produced", "panel": "symbolEvidence", "ops": [op("/metrics/@parse-in/response/context/totalItems", 4)], "expect": "J-METRIC-PAGE"},
        {"id": "metric-row-dropped-without-projection", "panel": "symbolEvidence", "ops": [op("/metrics/@parse-in", kind="remove")], "expect": "J-METRIC-TOTALITY"},
        {"id": "trace-start-not-embedded-origin-row", "panel": "symbolEvidence", "ops": [op("/traces/@parse/start/viaReachabilityFactId", fact_id("r04"))], "expect": "J-TRACE-START"},
        {"id": "trace-entry-path-not-attribution", "panel": "symbolEvidence", "ops": [op("/traces/@parse/start/entry/path", "src/main.rs")], "expect": "J-TRACE-ENTRY"},
        {"id": "trace-cargo-target-provenance-other-root", "panel": "symbolEvidence", "ops": [op("/traces/@parse/start/entry/provenance/0/unitId", "@svc-bin-unit")], "expect": "J-TRACE-ENTRY"},
        {"id": "trace-explicit-provenance-without-explicit", "panel": "symbolEvidence", "ops": [op("/traces/@parse/start/entry/provenance", [{"source": "explicit"}])], "expect": "J-TRACE-ENTRY"},
        {"id": "trace-dead-code-state", "panel": "symbolEvidence", "ops": [op("/traces/@both/state", "dead-code")], "expect": "SCHEMA"},
        {"id": "trace-blockers-erased", "panel": "symbolEvidence", "ops": [op("/traces/@button-test/blockers", [])], "expect": "J-TRACE-BLOCKERS"},
        {"id": "trace-after-recognition-purged", "panel": "symbolEvidence", "ops": [op("/entryRecognition", {"state": "unavailable", "parameterDigest": H("p"), "availability": "purged"})],
         "expect": "J-TRACE-AVAILABILITY"},
        {"id": "cargo-entries-all-despite-missing-coverage", "panel": "symbolEvidence", "ops": [op("/entryRecognition/cargoTargetEntries/0/missingCoverage", ["target-crate-root-unresolved"])],
         "expect": "J-ENTRY-CARGO"},
        {"id": "cargo-entries-test-target-as-entry", "panel": "symbolEvidence", "ops": [op("/entryRecognition/cargoTargetEntries/0/targets/0/targetKind", "test")], "expect": "SCHEMA"},
        {"id": "test-origin-imported-test-id", "panel": "symbolEvidence",
         "ops": [op("/testReachability/@button-test/originEvidence", {"kind": "imported-test-id", "importId": "import2:" + H("i"), "testId": "button renders"})], "expect": "SCHEMA"},
        {"id": "test-origin-glob-not-retained", "panel": "symbolEvidence", "ops": [op("/testReachability/@button-test/originEvidence/glob", "**/*")], "expect": "J-TR-ORIGIN"},
        {"id": "test-origin-rust-non-test-target", "panel": "symbolEvidence", "ops": [op("/testReachability/@both/origin/originEvidence/unitIds", "@core-lib-unit")], "expect": "J-TR-ORIGIN"},
        {"id": "test-absence-state-reintroduced", "panel": "symbolEvidence",
         "ops": [op("/testReachability/@shared/state", "no-static-path-within-bound"), op("/testReachability/@shared/blockers", kind="remove")], "expect": "SCHEMA"},
        {"id": "test-origin-set-complete", "panel": "symbolEvidence", "ops": [op("/testOrigins/@web/completeness", "complete")], "expect": "SCHEMA"},
        {"id": "test-origin-set-default-glob-limitation-dropped", "panel": "symbolEvidence",
         "ops": [op("/testOrigins/@web/limitations", ["foreign-unit-paths-not-matched"])], "expect": "J-TR-ORIGIN-SET"},
        {"id": "test-witness-start-not-origin", "panel": "symbolEvidence", "ops": [op("/testReachability/@both/origin/endpoint/nativeSubjectId", "rs:svc::main")], "expect": "J-TR-WITNESS"},
        {"id": "test-executed-coverage-interpretation", "panel": "symbolEvidence", "ops": [op("/testReachability/@both/interpretation", "executed-coverage")], "expect": "SCHEMA"},
        {"id": "test-blockers-without-partial-origin-set", "panel": "symbolEvidence", "ops": [op("/testReachability/@shared/blockers", ["evidence-limitations"])], "expect": "J-TR-BLOCKERS"},
        {"id": "test-unknown-identity-with-origin-set", "panel": "symbolEvidence",
         "ops": [op("/testReachability/@shared", "@shared-unknown-identity")], "expect": "J-TR-STATE"},
        {"id": "test-reach-depth-widened", "panel": "symbolEvidence", "ops": [op("/testReachability/@shared/reach/request/params/maxDepth", 64)], "expect": "J-TR-REQUEST"},
        {"id": "test-origin-set-globs-not-retained", "panel": "symbolEvidence", "ops": [op("/testOrigins/@web/evidence/recognizers/0/testGlobs", ["**/*"])], "expect": "J-TR-ORIGIN-SET"},
    ]


def recognition_cases():
    return [
        {"id": "frp-recognition-id-drift", "ops": [op("/units/0/recognitionId", "sha256:" + H("drift"))], "rehash": False, "expect": "J-FRP-ID"},
        {"id": "frp-evidence-digest-not-inventory", "ops": [op("/units/0/recognition/recognized/0/evidence/0/contentSha256", H("other"))], "rehash": True, "expect": "J-FRP-EVIDENCE"},
        {"id": "frp-entry-not-inventoried", "ops": [op("/units/0/recognition/recognized/0/effects/entryPoints", ["src/index.ts"])], "rehash": True, "expect": "J-FRP-ENTRY"},
        {"id": "frp-unit-relative-entry-spelling", "ops": [op("/units/2/recognition/recognized/0/effects/entryPoints", ["app/page.tsx"])], "rehash": True, "expect": "J-FRP-ENTRY"},
        {"id": "frp-summary-all-with-unresolved-choice", "ops": [op("/units/2/recognition/entryPoints", {"state": "all", "source": "recognized"})], "rehash": True, "expect": "J-FRP-SUMMARY"},
        {"id": "frp-unit-row-missing", "ops": [op("/units/3", kind="remove")], "rehash": False, "expect": "J-FRP-UNIT-TOTALITY"},
        {"id": "frp-membership-digest-mismatch", "ops": [op("/membershipDigest", H("membership"))], "rehash": False, "expect": "J-FRP-MEMBERSHIP"},
        {"id": "frp-explicit-not-configuration", "ops": [op("/explicitEntryPoints", ["src/main.rs"])], "rehash": False, "expect": "J-FRP-EXPLICIT"},
        {"id": "frp-unregistered-recognizer", "ops": [op("/units/1/recognition/recognized/0/recognizerId", "angular")], "rehash": False, "expect": "SCHEMA"},
        {"id": "frp-units-out-of-order", "ops": [op("/units", "@reversed")], "rehash": False, "expect": "J-FRP-ORDER"},
        {"id": "frp-root-path-mismatch", "ops": [op("/units/1/rootPath", "packages")], "rehash": False, "expect": "J-FRP-UNIT"},
        {"id": "frp-snapshot-mismatch", "ops": [op("/snapshotId", "snapshot2:" + H("other"))], "rehash": False, "expect": "J-FRP-SNAPSHOT"},
        {"id": "frp-parent-cycle-plan-id", "ops": [op("/planId", PLAN, kind="add")], "rehash": False, "expect": "SCHEMA"},
        {"id": "frp-dot-root-sentinel-retained", "ops": [op("/units/0/rootPath", ".")], "rehash": False, "expect": "SCHEMA"},
    ]


def host_cases():
    return [
        {"id": "coupling-prefix-guess", "feature": "coupling", "resolver": "prefix-guess", "expect": "J-COUPLING-OWNER"},
        {"id": "coupling-symbol-spelling-parse", "feature": "coupling", "resolver": "symbol-spelling-parse", "expect": "J-COUPLING-OWNER"},
        {"id": "coupling-symbol-path-instead-of-anchor", "feature": "coupling", "resolver": "symbol-path-not-anchor", "expect": "J-COUPLING-OWNER"},
        {"id": "coupling-target-ownership-as-package", "feature": "coupling", "resolver": "ownership-as-package", "world": "mixed-core-package-partial", "expect": "J-COUPLING-OWNER"},
        {"id": "trace-browser-entry-name-heuristic", "feature": "traces", "resolver": "browser-entry-name", "world": "mixed-cargo-member-root-unresolved", "expect": "J-TRACE-ENTRY"},
        {"id": "test-origin-name-guess", "feature": "testReachability", "resolver": "test-name-guess", "expect": "J-TR-ORIGIN-SET"},
        {"id": "test-origin-imported-test-id-resolver", "feature": "testReachability", "resolver": "imported-test-id", "expect": "SCHEMA"},
    ]


def build(M, NM, parent07_fixtures):
    base = parent07_fixtures["bases"]["audit-full"]
    integration, integration_resolution = integration_desc(base)
    cross, _ = cross_universe_test_desc(base)
    jest, _ = jest_configured_desc(base)
    return {
        "schemaVersion": 2,
        "standing": "author-02 constructions following the cited owner laws; units, membership and recognition executed through the pinned native model; not product engine output, not runtime, browser or Run replay evidence",
        "parent07Base": {"fixture": "bases/audit-full", "runId": base["envelope"]["run"]["runId"], "projectId": base["envelope"]["projectId"]},
        "descriptions": {"mixed": mixed_desc(), "clean": clean_coupling_desc(), "integration": integration, "cross-universe-test": cross, "jest-configured": jest,
                         "dense-120": {"dense": 120, "projectId": base["envelope"]["projectId"], "runId": base["envelope"]["run"]["runId"]}},
        "variants": sorted(variants(M)),
        "resolutions": {"mixed": mixed_resolution(M), "integration": integration_resolution},
        "documentCases": document_cases(),
        "recognitionCases": recognition_cases(),
        "hostCases": host_cases(),
    }
