"""Fixture builder (author-01). Constructions following the cited owner laws; not product engine output.

build(M, subject05_fixtures) -> fixtures dict. Worlds are owner-schema-valid retained-closure mocks; panels are reference derivations;
cases are positive and adversarial inputs with the exact expected refusal code (or acceptance) at their layer.
"""
import copy
import hashlib

H = lambda label: hashlib.sha256(label.encode()).hexdigest()
PROJECT = "prj1-" + H("evidence-project")
RUN = "run3:" + H("evidence-run")
PLAN = "plan2:" + H("evidence-plan")
SNAPSHOT = "snapshot2:" + H("evidence-snapshot")
UR, US, UW, UL = H("universe:rust"), H("universe:shared"), H("universe:web"), H("universe:legacy")
CLOSURE = "closure2:" + H("provider")
VIEWS = {"imports": H("view:imports"), "calls": H("view:calls"), "reach": H("view:reach")}
SUFFIX_LANGUAGE = [(".tsx", "typescript"), (".ts", "typescript"), (".js", "javascript"), (".rs", "rust"), (".json", "json"), (".toml", "toml")]


def language(path):
    return next((lang for suffix, lang in SUFFIX_LANGUAGE if path.endswith(suffix)), "unspecified")


def body(path):
    return ("// fixture " + path + "\n").encode()


def fact_id(label):
    return "fact2:" + H("fact:" + label)


def ep(universe, kind, native_id, manifest=None):
    out = {"universe": universe, "kind": kind, "nativeSubjectId": native_id}
    if manifest is not None:
        out["packageManifestPath"] = manifest
    return out


# ---------------------------------------------------------------------------
# generic world assembly from a compact description

def assemble(desc, M):
    files = sorted(desc["files"])
    inventory = [{"path": p, "sha256": hashlib.sha256(body(p)).hexdigest(), "bytes": len(body(p))} for p in files]
    sha_of = {row["path"]: row["sha256"] for row in inventory}
    units = []
    for ordinal, unit in enumerate(desc["units"]):
        units.append({"unitOrdinal": ordinal, "rootPath": unit["root"], "languageFamily": unit["family"], "languageMode": unit["mode"], "unitKind": unit["kind"],
                      "markerPath": unit["marker"], "markerSha256": sha_of[unit["marker"]], "recognizerId": unit["kind"], "recognizerVersion": 1,
                      "provenance": "DISCOVERED", "memberPackageRoots": unit.get("members", [])})
    rows = []
    for path in files:
        member = desc["membership"].get(path)
        if member is None:
            rows.append({"path": path, "languageFamily": "none", "unitOrdinal": None, "membership": "syntax-only", "reason": "grammar-only"})
        else:
            family = units[member]["languageFamily"]
            rows.append({"path": path, "languageFamily": family, "unitOrdinal": member, "membership": "program-member", "reason": "deepest-unit-in-language"})
    membership = {"schemaVersion": 1, "units": units, "rows": rows, "unsupportedFiles": [], "outsideBoundaryFiles": [], "erasedFiles": []}
    membership_digest = M.raw_sha(membership)
    order = lambda values: sorted(set(values), key=lambda v: M.canon(v))
    cells = []
    for program in desc["programs"]:
        root_text = "." if program["root"] == "" else program["root"]
        under = [p for p in files if program["root"] == "" or p.startswith(program["root"] + "/")]
        symbol_paths = order(row["path"] for row in program["symbols"])
        packages = order(path for path, _ in desc["packages"] if path in under)
        for capability, kinds in (("calls", ["symbol"]), ("imports", ["symbol"]), ("inventory", ["file", "package"])):
            extents = []
            for kind in kinds:
                paths = {"symbol": symbol_paths, "file": order(under), "package": packages}[kind]
                extents.append({"kind": kind, "paths": paths})
            cells.append({"capabilityId": capability, "languageMode": program["mode"], "workspaceRoot": root_text, "required": True, "kinds": kinds,
                          "programBindings": [{"ordinal": 0, "provenance": "default-unit", "enumerator": {"status": "selected", "closureId": CLOSURE},
                                               "nativeContextDigest": H("context:" + program["mode"]), "universe": program["universe"], "programEntry": None,
                                               "extents": extents}],
                          "_program": program})
    cells.sort(key=lambda c: (c["capabilityId"].encode(), c["languageMode"].encode(), c["workspaceRoot"].encode()))
    plan = {"schemaVersion": 1, "snapshotId": desc.get("snapshotId", SNAPSHOT), "scopeDigest": H("scope"), "membershipDigest": membership_digest,
            "cells": [{k: v for k, v in c.items() if k != "_program"} for c in cells]}
    parameter_digest = M.raw_sha(plan)
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
                items = [{"nativeSubjectId": p, "kind": "file", "path": p, "qualifiedName": p, "subjectLanguage": language(p), "signatureTokens": [], "projections": []} for p in extent["paths"]]
                items.sort(key=lambda r: r["nativeSubjectId"].encode())
            else:
                names = dict(desc["packages"])
                items = [{"nativeSubjectId": names[p], "kind": "package", "path": p, "qualifiedName": names[p], "subjectLanguage": language(p), "signatureTokens": [], "projections": []}
                         for p in extent["paths"]]
                items.sort(key=lambda r: (r["nativeSubjectId"].encode(), r["path"].encode()))
            state = desc.get("inventoryStates", {}).get("%s|%s|%s" % (cell["capabilityId"], program["universe"], kind), "complete")
            if state == "partial":
                dropped = desc.get("inventoryDrops", {}).get("%s|%s|%s" % (cell["capabilityId"], program["universe"], kind), [])
                items = [r for r in items if r["path"] not in dropped and r["nativeSubjectId"] not in dropped]
            inventories.append({"schemaVersion": 1, "planId": PLAN, "parameterDigest": parameter_digest, "cellOrdinal": ordinal, "programOrdinal": 0, "kind": kind,
                                "state": state, "deficiency": None if state == "complete" else "budget-exhausted", "nativeCause": None,
                                "examinedPaths": extent["paths"], "rows": items})
    ownership = {}
    for universe, spec in desc.get("ownership", {}).items():
        declared = []
        for marker, crate, kind, name, edition in spec["units"]:
            unit = {"markerPath": marker, "crateName": crate, "targetKind": kind, "targetName": name, "targetEdition": edition}
            unit["unitId"] = M.native_h(M.COMPILATION_UNIT_DOMAIN, {"schemaVersion": 1, "markerPath": marker, "targetKind": kind, "targetName": name})
            declared.append(unit)
        by_name = {(u["markerPath"], u["targetKind"], u["targetName"]): u["unitId"] for u in declared}
        own_rows = sorted(({"path": path, "unitId": by_name[target]} for path, targets in spec["owners"].items() for target in targets),
                          key=lambda r: (r["path"].encode(), r["unitId"].encode()))
        ownership[universe] = {"schemaVersion": 1, "enumeration": spec.get("enumeration", "complete"), "units": sorted(declared, key=lambda u: u["unitId"].encode()),
                               "selectedUnitIds": sorted((by_name[t] for t in spec["selected"]), key=lambda x: x.encode()), "ownership": own_rows}
    recognition = desc["recognition"]
    record = None
    if recognition.get("units") is not None:
        rows_out = []
        for ordinal, results in recognition["units"]:
            recognized = []
            for rid, assurance, evidence, entries, globs, ignore, unresolved in results:
                recognized.append({"recognizerId": rid, "recognizerVersion": 1, "evidence": [{"path": p, "contentSha256": sha_of[p], "field": f} for p, f in evidence],
                                   "assurance": assurance, "effects": {"entryPoints": entries, "testGlobs": globs, "ignoreConventions": ignore}, "unresolvedChoices": unresolved})
            recognized.sort(key=lambda r: r["recognizerId"])
            rec = {"schemaVersion": 1, "recognized": recognized, "observedHints": [], "entryPoints": M.recognition_summary(recognized, recognition["explicit"])}
            rows_out.append({"unitOrdinal": ordinal, "rootPath": units[ordinal]["rootPath"], "markerPath": units[ordinal]["markerPath"],
                             "recognitionId": M.native_h(M.RECOGNITION_DOMAIN, rec), "recognition": rec})
        record = {"schemaVersion": 1, "snapshotId": plan["snapshotId"], "membershipDigest": membership_digest,
                  "explicitEntryPoints": sorted(recognition["explicit"], key=lambda p: M.canon(p)), "units": rows_out}
    parameter = {"schemaDigest": "<sha256 of owner/framework-recognition-plan.schema.v1.json bytes>", "payloadDigest": M.raw_sha(record)} if record else None
    return {
        "projectId": desc.get("projectId", PROJECT), "runId": desc.get("runId", RUN), "snapshotId": plan["snapshotId"],
        "snapshotInventory": inventory, "membership": membership, "enumerationPlan": plan, "subjectInventories": inventories, "sourceUnitOwnership": ownership,
        "recognition": {"planBound": recognition.get("planBound", True) and record is not None, "parameter": parameter, "record": record,
                        "availability": recognition.get("availability", {"state": "retained", "parameterMissing": False})},
        "resolvedConfigurationEntryPoints": recognition["explicit"], "availability": desc.get("availability", "retained"),
        "facts": desc["facts"], "syntheticFanIn": desc.get("fanIn", []), "relations": desc["relations"],
    }


def relations(limitations=None, views=("imports", "calls", "reach")):
    names = {"imports": "imports@resolved-target", "calls": "calls@resolved-callee", "reach": "reachability@from-resolved-calls"}
    out = {}
    for short in views:
        out[names[short]] = {"views": [VIEWS[short]], "coverageIds": ["coverage2:" + H("coverage:" + short)], "scopeIds": ["scope2:" + H("scope:" + short)],
                             "deficiencyCitations": [], "resolutionLimitations": copy.deepcopy((limitations or {}).get(short, []))}
    return out


def fact(label, relation, rung, view, source, target, occupancy="first-party"):
    return {"factId": fact_id(label), "relation": relation, "resolution": rung, "source": source, "target": target, "targetOccupancy": occupancy, "viewDigest": VIEWS[view]}


# ---------------------------------------------------------------------------
# mixed Rust + TS/JS world

def mixed_desc():
    rs = lambda n: ep(UR, "symbol", n)
    web = lambda n: ep(UW, "symbol", n)
    files = ["Cargo.toml", "src/main.rs", "crates/core/Cargo.toml", "crates/core/src/lib.rs", "crates/core/src/parse.rs", "crates/core/src/shared.rs",
             "crates/core/src/both.rs", "crates/core/tests/it.rs", "crates/app/Cargo.toml", "crates/app/src/main.rs", "crates/app/src/vendored/util.rs",
             "crates/app/src/orphan.rs", "crates/app/benches/b.rs",
             "packages/shared/package.json", "packages/shared/src/format.ts",
             "packages/web/package.json", "packages/web/tsconfig.json", "packages/web/next.config.js", "packages/web/app/page.tsx", "packages/web/src/button.tsx",
             "packages/web/src/button.test.tsx", "packages/web/src/api.ts",
             "packages/web-legacy/tsconfig.json", "packages/web-legacy/src/old.ts", "packages/web-legacy/src/old.test.ts"]
    units = [{"root": "", "family": "rust", "mode": "rust-cargo", "kind": "cargo-workspace", "marker": "Cargo.toml", "members": ["crates/app", "crates/core"]},
             {"root": "packages/shared", "family": "tsjs", "mode": "js-synthesized", "kind": "js-program", "marker": "packages/shared/package.json"},
             {"root": "packages/web", "family": "tsjs", "mode": "ts-tsconfig", "kind": "ts-program", "marker": "packages/web/tsconfig.json"},
             {"root": "packages/web-legacy", "family": "tsjs", "mode": "ts-tsconfig", "kind": "ts-program", "marker": "packages/web-legacy/tsconfig.json"}]
    membership = {p: 0 for p in files if p.endswith(".rs")}
    membership.update({p: 1 for p in files if p.startswith("packages/shared/src/")})
    membership.update({p: 2 for p in files if p.startswith("packages/web/") and p.endswith((".ts", ".tsx", ".js"))})
    membership.update({p: 3 for p in files if p.startswith("packages/web-legacy/") and p.endswith(".ts")})
    rust_symbols = [("rs:svc::main", "src/main.rs"), ("rs:core::lib", "crates/core/src/lib.rs"), ("rs:core::parse", "crates/core/src/parse.rs"),
                    ("rs:core::shared_fmt", "crates/core/src/shared.rs"), ("rs:core::both", "crates/core/src/both.rs"), ("rs:core::it_parses", "crates/core/tests/it.rs"),
                    ("rs:app::main", "crates/app/src/main.rs"), ("rs:app::util", "crates/app/src/vendored/util.rs"), ("rs:app::orphan", "crates/app/src/orphan.rs"),
                    ("rs:app::bench_only", "crates/app/benches/b.rs")]
    programs = [
        {"root": "", "mode": "rust-cargo", "universe": UR, "symbols": [{"id": i, "path": p} for i, p in rust_symbols]},
        {"root": "packages/shared", "mode": "js-synthesized", "universe": US, "symbols": [{"id": "ts:shared/format", "path": "packages/shared/src/format.ts"}]},
        {"root": "packages/web", "mode": "ts-tsconfig", "universe": UW, "symbols": [
            {"id": "ts:web/api", "path": "packages/web/src/api.ts"}, {"id": "ts:web/button", "path": "packages/web/src/button.tsx"},
            {"id": "ts:web/button.test", "path": "packages/web/src/button.test.tsx"}, {"id": "ts:web/next-config", "path": "packages/web/next.config.js"},
            {"id": "ts:web/page", "path": "packages/web/app/page.tsx"}, {"id": "ts:web/shared-format", "path": "packages/shared/src/format.ts"}]},
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
                                 "crates/app/benches/b.rs": [("crates/app/Cargo.toml", "bench", "b")]}}}
    imports = [
        fact("i01", "imports", "resolved-target", "imports", rs("rs:app::main"), ep(UR, "package", "core", "crates/core/Cargo.toml")),
        fact("i02", "imports", "resolved-target", "imports", rs("rs:app::main"), rs("rs:core::parse")),
        fact("i03-provenance-duplicate-of-i02", "imports", "resolved-target", "imports", rs("rs:app::main"), rs("rs:core::parse")),
        fact("i04", "imports", "resolved-target", "imports", rs("rs:core::shared_fmt"), rs("rs:core::parse")),
        fact("i05", "imports", "resolved-target", "imports", rs("rs:app::util"), rs("rs:core::lib")),
        fact("i06", "imports", "resolved-target", "imports", rs("rs:svc::main"), ep(UR, "package", "app", "crates/app/Cargo.toml")),
        fact("i07", "imports", "resolved-target", "imports", rs("rs:app::orphan"), rs("rs:core::parse")),
        fact("i08", "imports", "resolved-target", "imports", rs("rs:app::bench_only"), rs("rs:core::parse")),
        fact("i09", "imports", "resolved-target", "imports", rs("rs:ghost"), rs("rs:core::parse")),
        fact("i10", "imports", "resolved-target", "imports", web("ts:web/api"), ep(US, "package", "@fx/shared", "packages/shared/package.json")),
        fact("i11", "imports", "resolved-target", "imports", web("ts:web/api"), ep(US, "file", "packages/shared/src/format.ts")),
        fact("i12", "imports", "resolved-target", "imports", web("ts:web/button"), ep(UW, "package", "lodash", "node_modules/lodash/package.json"), "external"),
        fact("i13", "imports", "resolved-target", "imports", web("ts:web/button"), ep(UW, "symbol", "ts:external/x"), "external"),
        fact("i14", "imports", "resolved-target", "imports", web("ts:web/page"), ep(UW, "symbol", "ts:web/unknown"), "unknown"),
        fact("i15", "imports", "resolved-target", "imports", ep(UL, "symbol", "ts:legacy/old"), web("ts:web/button")),
        fact("i16", "imports", "resolved-target", "imports", web("ts:web/shared-format"), web("ts:web/button")),
        fact("i17", "imports", "resolved-target", "imports", web("ts:web/button.test"), web("ts:web/button")),
    ]
    calls = [
        fact("c01", "calls", "resolved-callee", "calls", rs("rs:svc::main"), rs("rs:core::parse")),
        fact("c02", "calls", "resolved-callee", "calls", rs("rs:core::it_parses"), rs("rs:core::both")),
        fact("c03", "calls", "resolved-callee", "calls", rs("rs:core::both"), rs("rs:core::parse")),
        fact("c04", "calls", "resolved-callee", "calls", rs("rs:app::main"), rs("rs:core::shared_fmt")),
        fact("c05", "calls", "resolved-callee", "calls", rs("rs:core::shared_fmt"), rs("rs:core::parse")),
        fact("c06", "calls", "resolved-callee", "calls", web("ts:web/page"), web("ts:web/button")),
        fact("c07", "calls", "resolved-callee", "calls", web("ts:web/button"), web("ts:web/api")),
        fact("c08", "calls", "resolved-callee", "calls", web("ts:web/button.test"), web("ts:web/button")),
        fact("c09", "calls", "resolved-callee", "calls", web("ts:web/api"), web("ts:web/shared-format")),
    ]
    reach = [
        fact("r01", "reachability", "from-resolved-calls", "reach", rs("rs:svc::main"), rs("rs:core::parse")),
        fact("r02", "reachability", "from-resolved-calls", "reach", rs("rs:app::main"), rs("rs:core::parse")),
        fact("r03", "reachability", "from-resolved-calls", "reach", rs("rs:app::main"), rs("rs:core::shared_fmt")),
        fact("r04", "reachability", "from-resolved-calls", "reach", web("ts:web/page"), web("ts:web/button")),
        fact("r05", "reachability", "from-resolved-calls", "reach", web("ts:web/page"), web("ts:web/api")),
    ]
    recognition = {"explicit": [], "units": [
        (0, [("cargo-package", "declared", [("Cargo.toml", "package/lib/bin")], ["src/main.rs"], [], ["target/"], []),
             ("cargo-workspace", "declared", [("Cargo.toml", "workspace.members")], [], [], ["target/"], [])]),
        (1, [("node-package", "declared", [("packages/shared/package.json", "type/private/exports/main")], [], [], ["node_modules/"], [])]),
        (2, [("nextjs", "inferred", [("packages/web/next.config.js", "presence")], ["packages/web/app/page.tsx"], [], [".next/"], ["config-requires-evaluation"]),
             ("node-package", "declared", [("packages/web/package.json", "type/private/exports/main")], [], [], ["node_modules/"], []),
             ("typescript-config", "declared", [("packages/web/tsconfig.json", "compilerOptions/extends/references")], [], [], [], []),
             ("vitest-jest", "declared", [("packages/web/package.json", "jest|vitest")], [], ["**/*.test.*", "**/*.spec.*", "**/__tests__/**"], [], [])]),
        (3, [("typescript-config", "declared", [("packages/web-legacy/tsconfig.json", "compilerOptions/extends/references")], [], [], [], [])]),
    ]}
    limitations = {"imports": [{"kind": "unresolved-edge-present", "relation": "imports", "minResolution": "resolved-target", "unresolvedEdgeCount": 2}]}
    return {"files": files, "units": units, "membership": membership, "programs": programs, "packages": packages, "ownership": ownership,
            "recognition": recognition, "facts": imports + calls + reach, "relations": relations(limitations)}


def mixed_resolution(M):
    subjects = [ep(UR, "symbol", "rs:core::parse"), ep(UR, "symbol", "rs:core::shared_fmt"), ep(UW, "symbol", "ts:web/api"), ep(UW, "symbol", "ts:web/button.test"),
                ep(US, "package", "@fx/shared", "packages/shared/package.json"), ep(UR, "symbol", "rs:core::both"), ep(UL, "symbol", "ts:legacy/old")]
    out = [{"subjectId": M.RM.subject_id(e), "state": "resolved", "endpoint": e} for e in subjects]
    out.insert(5, {"subjectId": "subject3:" + H("descriptor-not-retained"), "state": "descriptor-not-retained"})
    return out


def clean_coupling_desc():
    desc = mixed_desc()
    bad = {fact_id(x) for x in ("i07", "i08", "i09", "i12", "i13", "i14")}
    desc["facts"] = [f for f in desc["facts"] if f["factId"] not in bad]
    desc["relations"] = relations()
    return desc


# ---------------------------------------------------------------------------
# integration world aligned to subject-05 audit-full

def integration_desc(base):
    envelope = base["envelope"]
    resolution = base["panels"]["graph"]["data"]["subjectResolution"]
    universe = next(r["endpoint"]["universe"] for r in resolution if r["state"] == "resolved")
    S = lambda n: ep(universe, "symbol", n)
    files = ["package.json", "tsconfig.json", "src/index.ts", "src/helper.ts", "src/helper.test.ts", "src/legacy.js", "packages/util/package.json", "packages/util/src/u.ts"]
    units = [{"root": "", "family": "tsjs", "mode": "ts-tsconfig", "kind": "ts-program", "marker": "tsconfig.json"},
             {"root": "packages/util", "family": "tsjs", "mode": "js-synthesized", "kind": "js-program", "marker": "packages/util/package.json"}]
    membership = {"src/index.ts": 0, "src/helper.ts": 0, "src/helper.test.ts": 0, "src/legacy.js": 0, "packages/util/src/u.ts": 1}
    programs = [{"root": "", "mode": "ts-tsconfig", "universe": universe, "symbols": [
        {"id": "ts:src/index.ts#main", "path": "src/index.ts"}, {"id": "ts:src/helper.ts#helper", "path": "src/helper.ts"},
        {"id": "ts:src/helper.test.ts#t", "path": "src/helper.test.ts"}]}]
    packages = [("package.json", "fixture-app"), ("packages/util/package.json", "npm:@fixture/util")]
    facts = [
        fact("a-c1", "calls", "resolved-callee", "calls", S("ts:src/index.ts#main"), S("ts:src/helper.ts#helper")),
        fact("a-c2", "calls", "resolved-callee", "calls", S("ts:src/helper.test.ts#t"), S("ts:src/helper.ts#helper")),
        fact("a-r1", "reachability", "from-resolved-calls", "reach", S("ts:src/index.ts#main"), S("ts:src/helper.ts#helper")),
        fact("a-i1", "imports", "resolved-target", "imports", S("ts:src/index.ts#main"), ep(universe, "package", "npm:@fixture/util", "packages/util/package.json")),
        fact("a-i2", "imports", "resolved-target", "imports", S("ts:src/index.ts#main"), ep(universe, "file", "src/legacy.js")),
    ]
    recognition = {"explicit": ["src/index.ts"], "units": [
        (0, [("typescript-config", "declared", [("tsconfig.json", "compilerOptions/extends/references")], [], [], [], []),
             ("vitest-jest", "declared", [("package.json", "jest|vitest")], [], ["**/*.test.*"], [], [])]),
        (1, [("node-package", "declared", [("packages/util/package.json", "type/private/exports/main")], [], [], ["node_modules/"], [])]),
    ]}
    return {"files": files, "units": units, "membership": membership, "programs": programs, "packages": packages, "recognition": recognition, "facts": facts,
            "relations": relations(), "projectId": envelope["projectId"], "runId": envelope["run"]["runId"]}, resolution


# ---------------------------------------------------------------------------
# adversarial resolvers (deliberately unlawful attribution, used to show the host derivation refuses them)

def prefix_guess(world, importer):
    path, cause = world.symbol_attribution(importer["universe"], importer["nativeSubjectId"])
    if cause:
        return None, cause, None
    manifests = []
    for inv in world.inventories:
        if inv["kind"] == "package":
            manifests += [row["path"] for row in inv["rows"]]
    best = max((m for m in set(manifests) if path.startswith(m.rsplit("/", 1)[0] if "/" in m else "")), key=len)
    return [{"keyKind": "first-party-package", "path": best}], None, path


def spelling_parse(world, importer):
    path, cause = world.symbol_attribution(importer["universe"], importer["nativeSubjectId"])
    if cause:
        return None, cause, None
    if importer["nativeSubjectId"].startswith("rs:"):
        crate = importer["nativeSubjectId"][3:].split("::")[0]
        manifest = {"svc": "Cargo.toml"}.get(crate, "crates/%s/Cargo.toml" % crate)
        return [{"keyKind": "first-party-package", "path": manifest}], None, path
    keys, cause = world.path_owner_keys(importer["universe"], path)
    return keys, cause, path


def ownership_as_package(world, importer):
    path, cause = world.symbol_attribution(importer["universe"], importer["nativeSubjectId"])
    if cause:
        return None, cause, None
    if world.family(importer["universe"]) != "rust":
        keys, cause = world.path_owner_keys(importer["universe"], path)
        return keys, cause, path
    record = world.ownership[importer["universe"]]
    units = {u["unitId"]: u for u in record["units"]}
    markers = sorted({units[r["unitId"]]["markerPath"] for r in record["ownership"] if r["path"] == path})
    return ([{"keyKind": "first-party-package", "path": m} for m in markers] or None), (None if markers else "not-compiled-by-selected-targets"), path


def browser_entry_name(world, origin):
    path, cause = world.symbol_attribution(origin["universe"], origin["nativeSubjectId"])
    if cause or not origin["nativeSubjectId"].endswith(("main", "page")):
        return None
    unit = world.unit_for_universe(origin["universe"])
    row = next(r for r in world.recognition["record"]["units"] if r["unitOrdinal"] == unit["unitOrdinal"])
    result = next(r for r in row["recognition"]["recognized"] if r["effects"]["entryPoints"])
    return path, [{"source": "recognized", "unitOrdinal": unit["unitOrdinal"], "recognizerId": result["recognizerId"], "recognizerVersion": 1,
                   "assurance": result["assurance"], "evidence": copy.deepcopy(result["evidence"]), "unresolvedChoices": list(result["unresolvedChoices"])}]


def test_name_guess(world, universe, by_symbol):
    unit = world.unit_for_universe(universe)
    row = next((r for r in world.recognition["record"]["units"] if unit and r["unitOrdinal"] == unit["unitOrdinal"]), None)
    origins = {}
    for sid, paths in sorted(by_symbol.items()):
        path = next(iter(paths))
        if "test" in sid and unit and path.startswith(unit["rootPath"] + "/"):
            origins[sid] = {"attributionPath": path, "originEvidence": {"kind": "recognized-test-glob", "unitOrdinal": unit["unitOrdinal"], "recognizerId": "vitest-jest",
                                                                         "glob": "**/*.test.*", "relativePath": path[len(unit["rootPath"]) + 1:]}}
    if unit is None or row is None:
        return {"universe": universe, "source": "none", "completeness": "none", "cause": "universe-not-plan-bound", "limitations": [], "originCount": 0}, {}
    evidence = {"unitOrdinal": unit["unitOrdinal"], "rootPath": unit["rootPath"], "markerPath": unit["markerPath"], "recognitionId": row["recognitionId"],
                "recognizers": [{"recognizerId": "vitest-jest", "testGlobs": ["**/*.test.*"], "unresolvedChoices": [], "evidence": [{"path": unit["markerPath"],
                                                                                                                                 "contentSha256": world.inventory[unit["markerPath"]]["sha256"], "field": "name-guess"}]}]}
    return {"universe": universe, "source": "recognized-test-globs", "completeness": "declared", "limitations": [], "originCount": len(origins), "evidence": evidence}, origins


def imported_test_id(world, universe, by_symbol):
    origin_set, origins = test_name_guess(world, universe, by_symbol)
    for sid in origins:
        origins[sid]["originEvidence"] = {"kind": "imported-test-id", "importId": "import2:" + H("test-import"), "testId": sid}
    return origin_set, origins


RESOLVERS = {"prefix-guess": prefix_guess, "symbol-spelling-parse": spelling_parse, "ownership-as-package": ownership_as_package}
START_RESOLVERS = {"browser-entry-name": browser_entry_name}
ORIGIN_RESOLVERS = {"test-name-guess": test_name_guess, "imported-test-id": imported_test_id}


# ---------------------------------------------------------------------------
# cases

def op(path, value=None, kind="set"):
    return {"op": kind, "path": path, "value": value} if kind != "remove" else {"op": "remove", "path": path}


def document_cases():
    wrong = "owner1:" + H("wrong")
    return [
        # coupling (world mixed)
        {"id": "coupling-owner-record-not-key", "panel": "coupling", "base": "mixed", "ops": [op("/owners/@core/packageManifestPath", "crates/core2/Cargo.toml")], "expect": "J-COUPLING-OWNER-KEY"},
        {"id": "coupling-cargo-target-unit-id-tampered", "panel": "coupling", "base": "mixed", "ops": [op("/owners/@core/cargoTargets/0/unitId", "sha256:" + H("x"))], "expect": "J-COUPLING-OWNER-KEY"},
        {"id": "coupling-facts-below-edges", "panel": "coupling", "base": "mixed", "ops": [op("/cells/@app-core/facts", 1)], "expect": "J-COUPLING-COUNT"},
        {"id": "coupling-provenance-duplicate-collapsed", "panel": "coupling", "base": "mixed", "ops": [op("/cells/@app-core/facts", 3)], "expect": "J-COUPLING-DRILL"},
        {"id": "coupling-importer-bucket-dropped", "panel": "coupling", "base": "mixed", "ops": [op("/importerBuckets/0", kind="remove")], "expect": "J-COUPLING-TOTALS"},
        {"id": "coupling-blank-cell-absence-claimed", "panel": "coupling", "base": "mixed", "ops": [op("/absence/absenceSupported", True)], "expect": "J-COUPLING-ABSENCE"},
        {"id": "coupling-blockers-erased", "panel": "coupling", "base": "mixed", "ops": [op("/absence/blockers", []), op("/absence/absenceSupported", True)], "expect": "J-COUPLING-ABSENCE"},
        {"id": "coupling-blank-cell-means-no-dependency", "panel": "coupling", "base": "mixed", "ops": [op("/absence/blankCellMeans", "no-dependency")], "expect": "SCHEMA"},
        {"id": "coupling-external-owner-as-importer", "panel": "coupling", "base": "mixed",
         "ops": [op("/cells/@web-web/fromOwnerKey", "@lodash"), {"op": "resort", "path": "/cells", "by": ["fromOwnerKey", "toOwnerKey"]}], "expect": "J-COUPLING-CELL"},
        {"id": "coupling-run-mismatch", "panel": "coupling", "base": "mixed", "ops": [op("/runId", "run3:" + H("other-run"))], "expect": "J-COUPLING-RUN"},
        {"id": "coupling-target-bucket-no-dependency-cause", "panel": "coupling", "base": "mixed", "ops": [op("/targetBuckets/0/cause", "no-dependency")], "expect": "SCHEMA"},
        {"id": "coupling-drilldown-row-moved-to-absent-cell", "panel": "coupling", "base": "mixed",
         "ops": [op("/drilldown/@drill-svc-app/toOwnerKey", "@web"), {"op": "resort", "path": "/drilldown", "by": ["fromOwnerKey", "toOwnerKey", "factId"]}], "expect": "J-COUPLING-DRILL"},
        # metrics (world mixed)
        {"id": "metric-value-not-total", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in/value", 7)], "expect": "J-METRIC-VALUE"},
        {"id": "metric-state-lower-bound-on-exact", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in/countState", "lower-bound")], "expect": "J-METRIC-STATE"},
        {"id": "metric-zero-absence-with-nonzero", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in/zeroSupportsAbsence", True)], "expect": "J-METRIC-ABSENCE"},
        {"id": "metric-runtime-hotness-id", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in/metricId", "runtime-hotness")], "expect": "SCHEMA"},
        {"id": "metric-interpretation-hotness", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in/interpretation", "runtime-hotness")], "expect": "SCHEMA"},
        {"id": "metric-request-direction-swapped", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in/request/params/direction", "outgoing")], "expect": "J-METRIC-REQUEST"},
        {"id": "metric-request-other-endpoint", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in/request/params/endpoint/nativeSubjectId", "rs:core::lib")], "expect": "J-METRIC-REQUEST"},
        {"id": "metric-response-total-not-produced", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in/response/context/totalItems", 4)], "expect": "J-METRIC-PAGE"},
        {"id": "metric-response-other-run", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in/response/context/resolvedView/runId", "run3:" + H("other-run"))], "expect": "J-METRIC-RUN"},
        {"id": "metric-row-dropped-without-projection", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in", kind="remove")], "expect": "J-METRIC-TOTALITY"},
        {"id": "metric-unknown-without-evidence-limitation", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/metrics/@parse-in", "@unknown-row")], "expect": "J-METRIC-STATE"},
        # traces (world mixed)
        {"id": "trace-start-not-embedded-origin-row", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/traces/@parse/start/viaReachabilityFactId", fact_id("r04"))], "expect": "J-TRACE-START"},
        {"id": "trace-entry-path-not-attribution", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/traces/@parse/start/entry/path", "crates/app/src/main.rs")], "expect": "J-TRACE-ENTRY"},
        {"id": "trace-explicit-provenance-without-explicit", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/traces/@parse/start/entry/provenance", [{"source": "explicit"}])], "expect": "J-TRACE-ENTRY"},
        {"id": "trace-path-depth-widened", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/traces/@parse/path/request/params/maxDepth", 64)], "expect": "J-TRACE-REQUEST"},
        {"id": "trace-path-state-contradicts-rows", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/traces/@parse/state", "path-not-within-bound")], "expect": "J-TRACE-PATH"},
        {"id": "trace-dead-code-state", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/traces/@shared/state", "dead-code")], "expect": "SCHEMA"},
        {"id": "trace-blockers-erased", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/traces/@button-test/blockers", [])], "expect": "J-TRACE-BLOCKERS"},
        {"id": "trace-after-recognition-purged", "panel": "symbolEvidence", "base": "mixed",
         "ops": [op("/entryRecognition", {"state": "unavailable", "parameterDigest": H("p"), "availability": "purged"})], "expect": "J-TRACE-AVAILABILITY"},
        {"id": "trace-origin-query-other-relation", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/traces/@parse/originQuery/request/params/relation", "calls")], "expect": "J-TRACE-REQUEST"},
        # test reachability (world mixed)
        {"id": "test-origin-imported-test-id", "panel": "symbolEvidence", "base": "mixed",
         "ops": [op("/testReachability/@button-test/originEvidence", {"kind": "imported-test-id", "importId": "import2:" + H("i"), "testId": "button renders"})], "expect": "SCHEMA"},
        {"id": "test-origin-glob-not-retained", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/testReachability/@button-test/originEvidence/glob", "**/*")], "expect": "J-TR-ORIGIN"},
        {"id": "test-origin-relative-path-mismatch", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/testReachability/@button-test/originEvidence/relativePath", "src/button.tsx")], "expect": "J-TR-ORIGIN"},
        {"id": "test-origin-rust-non-test-target", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/testReachability/@both/origin/originEvidence/unitIds", "@core-lib-unit")], "expect": "J-TR-ORIGIN"},
        {"id": "test-no-path-claimed-with-partial-origins", "panel": "symbolEvidence", "base": "mixed",
         "ops": [op("/testReachability/@shared/state", "no-static-path-within-bound"), op("/testReachability/@shared/blockers", kind="remove"),
                 op("/testReachability/@shared/maxDepth", 16), op("/testReachability/@shared/interpretation", "no-static-calls-path-from-identified-test-origins-within-bound-not-untested")],
         "expect": "J-TR-STATE"},
        {"id": "test-witness-start-not-origin", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/testReachability/@both/origin/endpoint/nativeSubjectId", "rs:svc::main")], "expect": "J-TR-WITNESS"},
        {"id": "test-executed-coverage-interpretation", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/testReachability/@both/interpretation", "executed-coverage")], "expect": "SCHEMA"},
        {"id": "test-rust-origin-set-declared", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/testOrigins/@rust/completeness", "declared")], "expect": "SCHEMA"},
        {"id": "test-blockers-wrong", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/testReachability/@shared/blockers", ["reach-lower-bound"])], "expect": "J-TR-BLOCKERS"},
        {"id": "test-unknown-identity-with-origin-set", "panel": "symbolEvidence", "base": "mixed",
         "ops": [op("/testReachability/@shared", {"subjectId": "@shared-subject", "state": "unknown", "cause": "no-test-origin-identity"})], "expect": "J-TR-STATE"},
        {"id": "test-reach-depth-widened", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/testReachability/@shared/reach/request/params/maxDepth", 64)], "expect": "J-TR-REQUEST"},
        {"id": "test-origin-set-globs-not-retained", "panel": "symbolEvidence", "base": "mixed", "ops": [op("/testOrigins/@web/evidence/recognizers/0/testGlobs", ["**/*"])], "expect": "J-TR-ORIGIN-SET"},
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
        {"id": "coupling-target-ownership-as-package", "feature": "coupling", "resolver": "ownership-as-package", "world": "mixed-core-package-partial", "expect": "J-COUPLING-OWNER"},
        {"id": "trace-browser-entry-name-heuristic", "feature": "traces", "resolver": "browser-entry-name", "expect": "J-TRACE-ENTRY"},
        {"id": "test-origin-name-guess", "feature": "testReachability", "resolver": "test-name-guess", "expect": "J-TR-ORIGIN-SET"},
        {"id": "test-origin-imported-test-id-resolver", "feature": "testReachability", "resolver": "imported-test-id", "expect": "SCHEMA"},
    ]


def variants(M):
    """name -> compact description transform over mixed_desc (applied by build and by the checker through the same function)."""
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
            desc["facts"].append(fact("many-%03d" % i, "reachability", "from-resolved-calls", "reach", ep(UR, "symbol", "rs:app::main"), ep(UR, "symbol", "rs:core::shared_fmt")))
        return desc

    def fan_in(desc):
        desc["fanIn"] = [{"name": "lib", "count": 100001, "relation": "calls", "resolution": "resolved-callee", "viewDigest": VIEWS["calls"],
                          "sourceTemplate": ep(UR, "symbol", "rs:gen::f"), "target": ep(UR, "symbol", "rs:core::lib")}]
        return desc

    def run_purged(desc):
        desc["availability"] = "purged"
        return desc

    return {"mixed-core-package-partial": core_package_partial, "mixed-not-plan-bound": not_plan_bound, "mixed-recognition-purged": purged,
            "mixed-recognition-partial-missing": partial_missing, "mixed-recognition-partial-present": partial_present,
            "mixed-no-reachability-view": no_reachability, "mixed-many-origins": many_origins, "mixed-fan-in-100001": fan_in, "mixed-run-evidence-purged": run_purged}


def world_desc(name, base_fixture=None):
    if name == "mixed":
        return mixed_desc()
    if name == "clean":
        return clean_coupling_desc()
    return None


def build(M, subject05_fixtures):
    base = subject05_fixtures["bases"]["audit-full"]
    integration, integration_resolution = integration_desc(base)
    return {
        "schemaVersion": 1,
        "standing": "author-01 constructions following the cited owner laws; not product engine output, not runtime, browser or Run replay evidence",
        "subject05Base": {"fixture": "bases/audit-full", "runId": base["envelope"]["run"]["runId"], "projectId": base["envelope"]["projectId"]},
        "descriptions": {"mixed": mixed_desc(), "clean": clean_coupling_desc(), "integration": integration},
        "variants": sorted(variants(M)),
        "resolutions": {"mixed": mixed_resolution(M), "integration": integration_resolution},
        "documentCases": document_cases(),
        "recognitionCases": recognition_cases(),
        "hostCases": host_cases(),
    }
