"""Phase A: discriminating TS/JS unitKind controls ONLY (no law, model or closure change), so their pre-fix results are
real receipts. usage: python -I -B apply_controls.py"""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-tsjs-unitkind-author.v1/tools')
from textedit import apply_all  # noqa: E402

C24 = 'docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py'
ENUMC = 'docs/coop/design-corrections/foundation/check-enumeration.v1.py'

M3_CONTROLS = '''
    # native-evidence section 1.4 U-4b.2: a tsjs unit's unitKind is the projection of its languageMode, and the TS/JS kinds
    # belong to tsjs units only. unitKind enters PlanId through membershipDigest, so the published projection is checked at
    # the owner (NV.TSJS_UNIT_KIND, used by discover_units) and at every enumeration admission (the law, ORDER).
    published = {"ts-tsconfig": "ts-program", "js-allowjs": "js-program", "js-synthesized": "js-program"}
    table = getattr(NV, "TSJS_UNIT_KIND", None)
    row("M3", "tsjs-unit-kind-owner-projection-is-the-published-closed-table",
        table == published and set(published) == set(ENUM.TS_MODES)
        and set(published.values()) <= set(NV.SCHEMAS["$defs"]["WorkspaceUnitV2"]["properties"]["unitKind"]["enum"]), table)
    owner_text = " ".join((KIT.parents[1] / "v2/contracts/product-v1/native-evidence.md").read_text().split())
    row("M3", "tsjs-unit-kind-law-is-stated-in-the-normative-owner", TSJS_UNIT_KIND_LAW in owner_text)
    marker_sha = "d" * 64
    for label, markers, expected_unit in (
            ("ts-tsconfig", {"tsconfig.json": {"sha256": marker_sha}},
             ("ts-tsconfig", "ts-program", "tsconfig.json", "typescript-config")),
            ("js-allowjs-from-a-tsconfig-marker", {"tsconfig.json": {"sha256": marker_sha, "allowJs": True}},
             ("js-allowjs", "js-program", "tsconfig.json", "typescript-config")),
            ("js-allowjs-from-a-jsconfig-marker", {"jsconfig.json": {"sha256": marker_sha}},
             ("js-allowjs", "js-program", "jsconfig.json", "typescript-config")),
            ("js-synthesized", {"package.json": {"sha256": marker_sha}},
             ("js-synthesized", "js-program", "package.json", "node-package"))):
        found = NV.discover_units(markers)["units"]
        got_unit = tuple(found[0][k] for k in ("languageMode", "unitKind", "markerPath", "recognizerId")) if len(found) == 1 else found
        row("M3", "discovered-tsjs-unit-" + label, got_unit == expected_unit, got_unit)
        canonical = NV.assign_membership(found, ["index.ts", "lib.js", "README.md"])
        row("M3", "law-admits-the-published-unit-kind-" + label, law(canonical) == [], law(canonical))
        reminted = copy.deepcopy(canonical)
        reminted["units"][0]["unitKind"] = "js-program" if expected_unit[1] == "ts-program" else "ts-program"
        row("M3", "law-refuses-a-reminted-unit-kind-" + label, law(reminted) == [ORDER], law(reminted))
    rust = NV.assign_membership(NV.discover_units({"Cargo.toml": {"sha256": marker_sha, "isCargoWorkspace": False}})["units"], ["src/main.rs"])
    fallback_only = NV.assign_membership([dict(NV.SYNTAX_ONLY_FALLBACK_UNIT, unitOrdinal=0)], ["a.ts"])
    tsjs_ts = NV.assign_membership(NV.discover_units({"tsconfig.json": {"sha256": marker_sha}})["units"], ["index.ts"])
    for name, membership, mutate, expected in (
            ("rust-unit-canonical-kind-is-lawful", rust, lambda m: None, []),
            ("rust-unit-carrying-js-program", rust, lambda m: m["units"][0].update(unitKind="js-program"), [ORDER]),
            ("fallback-unit-carrying-ts-program", fallback_only, lambda m: m["units"][0].update(unitKind="ts-program"), [ORDER]),
            ("tsjs-unit-with-a-non-tsjs-mode", tsjs_ts, lambda m: m["units"][0].update(languageMode="rust-cargo"), [ORDER])):
        m = copy.deepcopy(membership)
        mutate(m)
        row("M3", "law-" + name, law(m) == expected, law(m))
'''

REAL_RUN_ROW = '''            ("fallback-unit-reminted-with-a-tsjs-unit-kind", lambda m: m["units"][0].update(unitKind="js-program"), [fallback], ORDER),
'''

REAL_RUN_TSJS = '''
    # Real complete Runs with a discovered TS/JS unit: the published kind closes; a kind reminted BEFORE membershipDigest
    # (so the whole Plan is coherent) must refuse at Run closure rather than admit a second PlanId for the same project.
    for label, markers in (("ts-tsconfig", {"tsconfig.json": {"sha256": "d" * 64}}),
                           ("js-allowjs-from-a-tsconfig-marker", {"tsconfig.json": {"sha256": "d" * 64, "allowJs": True}}),
                           ("js-synthesized", {"package.json": {"sha256": "d" * 64}})):
        units = NV.discover_units(markers)["units"]
        graph, got = run_with(mutate_after(lambda m: None, units))
        row("M3", "real-run-closes-with-the-published-unit-kind-" + label,
            got is None and graph["membership"]["units"][0]["unitKind"] == units[0]["unitKind"], got)
        wrong = "js-program" if units[0]["unitKind"] == "ts-program" else "ts-program"
        graph, got = run_with(mutate_after(lambda m, w=wrong: m["units"][0].update(unitKind=w), units))
        row("M3", "real-run-refuses-a-reminted-unit-kind-" + label, got is not None and ORDER in got, got)
'''

LAW_CONST = '''
# native-evidence section 1.4 U-4b.2, whitespace-normalised: the published TS/JS unitKind projection.
TSJS_UNIT_KIND_LAW = ("whose `unitKind` is `ts-program` exactly when that mode is `ts-tsconfig` and `js-program` "
                      "when it is `js-allowjs` or `js-synthesized`")
'''

ENUM_CONTROLS = '''    # native section 1.4 U-4b.2: a tsjs unit's unitKind is the projection of its languageMode. Change ONLY unitKind on
    # this ts-tsconfig baseline and rebind membershipDigest, so a digest mismatch cannot mask the unit-kind decision.
    tsjs_unit_kind_cases = []
    for label, kind, expected in [("ts-tsconfig-published-ts-program", "ts-program", "ADMIT"),
                                  ("ts-tsconfig-reminted-js-program", "js-program", "REFUSE")]:
        changed_membership = copy.deepcopy(memb)
        changed_membership["units"][0]["unitKind"] = kind
        changed_plan = copy.deepcopy(ep)
        changed_plan["membershipDigest"] = M.raw_digest(changed_membership)
        result = admit(changed_plan, [
            inv("file", "complete", copy.deepcopy(files), file_ext),
            inv("package", "complete", copy.deepcopy(pkgs), pkg_ext),
        ], changed_membership, sc, universes, retained, source)
        exact_faults = [] if expected == "ADMIT" else ["ENUMERATION_MEMBERSHIP_ORDER"]
        tsjs_unit_kind_cases.append({"case": label, "expected": expected, "enumerationResult": result["result"],
                                     "refusals": result["refusals"],
                                     "passed": result["result"] == expected and result["refusals"] == exact_faults})

'''

rows = apply_all('phase A: TS/JS unitKind controls only', [
    (C24, [
        ('''SR = load("c24_semantic_replay", HERE / "check-semantic-replay.v3.py")
''', '''SR = load("c24_semantic_replay", HERE / "check-semantic-replay.v3.py")
''' + LAW_CONST),
        ('''        row("M3", "law-" + name, got == expected, got)

''', '''        row("M3", "law-" + name, got == expected, got)
''' + M3_CONTROLS + '''
'''),
        ('''            ("duplicate-row", lambda m: m["rows"].append(copy.deepcopy(m["rows"][-1])), (), ORDER)):
''', '''            ("duplicate-row", lambda m: m["rows"].append(copy.deepcopy(m["rows"][-1])), (), ORDER),
''' + REAL_RUN_ROW.rstrip('\n').rstrip(',') + '''):
'''),
        ('''        row("M3", "real-run-refuses-" + name, got is not None and token in got, got)
''', '''        row("M3", "real-run-refuses-" + name, got is not None and token in got, got)
''' + REAL_RUN_TSJS),
    ]),
    (ENUMC, [
        ('''    rec("missing-expected-inventory", admit(ep, [inv("file", "complete", files, file_ext)], memb, sc, universes, retained, source))
''', ENUM_CONTROLS + '''    rec("missing-expected-inventory", admit(ep, [inv("file", "complete", files, file_ext)], memb, sc, universes, retained, source))
'''),
        ('''                      for row in unit_root_cases if not row["passed"])
''', '''                      for row in unit_root_cases if not row["passed"])
    mismatches.extend({"case": "tsjs-unit-kind-" + row["case"], "observed": row}
                      for row in tsjs_unit_kind_cases if not row["passed"])
'''),
        ('''        "internalUnitRootControls": unit_root_cases,
''', '''        "internalUnitRootControls": unit_root_cases,
        "tsjsUnitKindControls": tsjs_unit_kind_cases,
'''),
    ]),
])
print(json.dumps(rows, indent=1))
