"""Post-reset author v2 (Claude): native case additions for P3 (admitted boundary inventory) and P22 (explicit Cargo
workspace root keeps member folding). Round-trips with indent=1, ensure_ascii=True. Expected values are hand-authored
from the contract text before execution (same author, not an independent oracle)."""
import json
from pathlib import Path

P = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native-cases.v2.json')
raw = P.read_bytes()
doc = json.loads(raw)
assert (json.dumps(doc, indent=1, ensure_ascii=True) + '\n').encode() == raw, "round-trip"

doc['feedbackMap']['PR2-P3'] = ("post-reset review v2 P3: native unit discovery consumes the security instrument's admitted boundary inventory "
                                "(nested repositories, nested projects, custody exclusions); units/memberships at or below a boundary are outside the "
                                "project; explicit roots crossing a boundary refuse; the Plan scope names the boundaries; the standalone instrument discloses source=none")
doc['feedbackMap']['PR2-P22'] = ("post-reset review v2 P22: an explicit Cargo workspace root keeps its member packages folded and their target output "
                                 "pruned; explicit roots are unit selection, never loss of Cargo workspace semantics")

FX = doc['fixtures']
H = lambda c: c * 64
FX['markersBoundaryRepo'] = {
    "package.json": {"sha256": H('b')},
    "vendor/lib/package.json": {"sha256": H('1')},
    "vendor/lib/node_modules/x/package.json": {"sha256": H('2')},
    "apps/site/package.json": {"sha256": H('3')},
    "apps/site/sub/Cargo.toml": {"sha256": H('4'), "isCargoWorkspace": False},
}
FX['boundaryInventoryRepo'] = {
    "schemaVersion": 1, "source": "security.discovery", "selectedRoot": "/home/alice/repo",
    "nestedRepositories": ["vendor/lib"], "nestedProjects": ["apps/site"], "custodyExcludedUnits": [],
    "prunedTrees": [{"path": "vendor/lib/node_modules", "reason": "dependency-tree", "markerCount": 1}],
}
FX['markersInsideNestedSite'] = {"package.json": {"sha256": H('3')}, "sub/Cargo.toml": {"sha256": H('4'), "isCargoWorkspace": False}}
FX['boundaryInventoryInsideNestedSite'] = {
    "schemaVersion": 1, "source": "security.discovery", "selectedRoot": "/home/alice/repo/apps/site",
    "nestedRepositories": [], "nestedProjects": [], "custodyExcludedUnits": [], "prunedTrees": [],
}
FX['markersCustody'] = {"package.json": {"sha256": H('b')}, "Cargo.toml": {"sha256": H('a'), "isCargoWorkspace": False},
                        "tools/package.json": {"sha256": H('5')}, "tools/inner/Cargo.toml": {"sha256": H('6'), "isCargoWorkspace": False}}
FX['boundaryInventoryCustody'] = {
    "schemaVersion": 1, "source": "security.discovery", "selectedRoot": "/home/alice/repo",
    "nestedRepositories": [], "nestedProjects": [],
    "custodyExcludedUnits": [{"path": "", "reason": "MARKER_CUSTODY:Cargo.toml:WRITABLE_BY_OTHERS"},
                             {"path": "tools", "reason": "DIRECTORY_CUSTODY:FOREIGN_OWNER"}],
    "prunedTrees": [],
}
FX['markersCargoWorkspaceTwoMembers'] = {"Cargo.toml": {"sha256": H('1'), "isCargoWorkspace": True},
                                         "crates/a/Cargo.toml": {"sha256": H('2'), "isCargoWorkspace": False},
                                         "crates/b/Cargo.toml": {"sha256": H('3'), "isCargoWorkspace": False}}

cases = [
    {
        "id": "units-nested-repository-and-nested-project-are-excluded-under-the-admitted-boundary-inventory",
        "feedback": ["R1", "PR2-P3"], "kind": "positive",
        "steps": [
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersBoundaryRepo", "boundaries": "$fixtures.boundaryInventoryRepo"}, "bind": "u"},
            {"fn": "assign_membership", "args": {"units": "$u.units", "files": ["index.js", "vendor/lib/src/x.js", "apps/site/sub/src/lib.rs", "apps/site/index.js"],
                                                 "boundaries": "$fixtures.boundaryInventoryRepo"}, "bind": "m"},
            {"fn": "unit_scope_descriptor", "args": {"units": "$u.units", "ignore_paths": [], "explicit_path_prefixes": None,
                                                     "pruned_trees": "$u.prunedTrees", "boundaries": "$fixtures.boundaryInventoryRepo"}, "bind": "s"},
        ],
        "expect": {
            "$u.refused": None,
            "$u.units": [{"unitOrdinal": 0, "rootPath": "", "languageFamily": "tsjs", "languageMode": "js-synthesized", "unitKind": "js-program", "markerPath": "package.json", "markerSha256": H('b'), "recognizerId": "node-package", "recognizerVersion": 1, "provenance": "DISCOVERED", "memberPackageRoots": []}],
            "$u.prunedTrees": [{"path": "vendor/lib/node_modules", "reason": "dependency-tree", "markerCount": 1}],
            "$u.boundaries.source": "security.discovery",
            "$u.boundaries.nestedRepositories": ["vendor/lib"], "$u.boundaries.nestedProjects": ["apps/site"],
            "$u.boundaries.excludedUnits": [
                {"path": "apps/site", "marker": "package.json", "reason": "nested-project", "anchor": "apps/site"},
                {"path": "apps/site/sub", "marker": "Cargo.toml", "reason": "nested-project", "anchor": "apps/site"},
                {"path": "vendor/lib", "marker": "package.json", "reason": "nested-repository", "anchor": "vendor/lib"}],
            "$m.rows.0.path": "apps/site/index.js", "$m.rows.0.membership": "outside-project-boundary", "$m.rows.0.reason": "nested-project", "$m.rows.0.unitOrdinal": None,
            "$m.rows.1.path": "apps/site/sub/src/lib.rs", "$m.rows.1.membership": "outside-project-boundary", "$m.rows.1.reason": "nested-project",
            "$m.rows.2.path": "index.js", "$m.rows.2.membership": "program-member", "$m.rows.2.unitOrdinal": 0,
            "$m.rows.3.path": "vendor/lib/src/x.js", "$m.rows.3.membership": "outside-project-boundary", "$m.rows.3.reason": "nested-repository",
            "$m.outsideBoundaryFiles": ["apps/site/index.js", "apps/site/sub/src/lib.rs", "vendor/lib/src/x.js"],
            "$m.erasedFiles": [],
            "$s.scopeDescriptor.workspaceRoots": ["."],
            "$s.scopeDescriptor.excludedPathPrefixes": [".git", "apps/site", "node_modules", "vendor/lib", "vendor/lib/node_modules"],
            "$s.boundaries.source": "security.discovery",
            "$s.boundaries.excludedPathPrefixesFromBoundaries": ["apps/site", "vendor/lib"],
        },
        "note": "The P3 counterexample: over the same marker inventory the security instrument admits one unit (the root) and records vendor/lib as a nested repository and apps/site as a nested project; with the admitted inventory the native instrument yields the same one unit, excludes the three marker directories at or below the boundaries, keeps their files outside every unit, and the Plan scope descriptor names both anchors. The full unit array is asserted, so no second unit exists."
    },
    {
        "id": "units-explicit-root-crossing-into-a-nested-project-or-repository-refuses-typed",
        "feedback": ["R6", "PR2-P3"], "kind": "negative",
        "steps": [
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersBoundaryRepo", "explicit_workspace_roots": ["apps/site"], "boundaries": "$fixtures.boundaryInventoryRepo"}, "bind": "p"},
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersBoundaryRepo", "explicit_workspace_roots": ["apps/site/sub"], "boundaries": "$fixtures.boundaryInventoryRepo"}, "bind": "d"},
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersBoundaryRepo", "explicit_workspace_roots": ["vendor/lib/"], "boundaries": "$fixtures.boundaryInventoryRepo"}, "bind": "r"},
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersBoundaryRepo", "explicit_workspace_roots": ["."], "boundaries": "$fixtures.boundaryInventoryRepo"}, "bind": "ok"},
        ],
        "expect": {
            "$p.units": [], "$p.refused.detail": "native.explicit-root-crosses-boundary", "$p.refused.roots": ["apps/site"], "$p.refused.anchor": "apps/site",
            "$p.refused.reason": "nested-project", "$p.refused.d9.code": "CONFIG.INVALID", "$p.refused.d9.exitCode": 2,
            "$d.refused.detail": "native.explicit-root-crosses-boundary", "$d.refused.roots": ["apps/site/sub"], "$d.refused.anchor": "apps/site", "$d.refused.reason": "nested-project",
            "$r.refused.detail": "native.explicit-root-crosses-boundary", "$r.refused.roots": ["vendor/lib"], "$r.refused.anchor": "vendor/lib", "$r.refused.reason": "nested-repository",
            "$ok.refused": None, "$ok.units.0.rootPath": "", "$ok.units.0.provenance": "EXPLICIT",
        },
        "note": "Security refuses the same joins as PROJECT.EXPLICIT_PATH_INVALID / JOIN_CROSSES_NESTED_PROJECT | JOIN_CROSSES_NESTED_REPOSITORY (S3); the native layer refuses typed even when a host forwarded the root without running security's join check. The trailing slash is dropped by the shared normalization before the boundary test."
    },
    {
        "id": "units-launch-inside-a-deliberate-nested-config-selects-it-as-the-whole-project",
        "feedback": ["R1", "PR2-P3"], "kind": "positive",
        "steps": [
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersInsideNestedSite", "boundaries": "$fixtures.boundaryInventoryInsideNestedSite"}, "bind": "u"},
            {"fn": "assign_membership", "args": {"units": "$u.units", "files": ["index.js", "sub/src/lib.rs"], "boundaries": "$fixtures.boundaryInventoryInsideNestedSite"}, "bind": "m"},
        ],
        "expect": {
            "$u.refused": None, "$u.units.0.rootPath": "", "$u.units.0.languageFamily": "tsjs",
            "$u.units.1.rootPath": "sub", "$u.units.1.languageFamily": "rust", "$u.units.1.unitKind": "cargo-package",
            "$u.boundaries.source": "security.discovery", "$u.boundaries.nestedProjects": [], "$u.boundaries.excludedUnits": [],
            "$m.rows.0.path": "index.js", "$m.rows.0.unitOrdinal": 0, "$m.rows.1.path": "sub/src/lib.rs", "$m.rows.1.unitOrdinal": 1,
            "$m.outsideBoundaryFiles": [],
        },
        "note": "Launched inside apps/site, security selects the nested config as the project (mode config, S3 ADV-3) and its inventory names no nested boundary; the same directories that were outside the enclosing project are this project's units. Scope depends on which project a launch is inside, never on which directory of one project."
    },
    {
        "id": "units-standalone-instrument-without-boundary-inventory-discloses-source-none",
        "feedback": ["PR2-P3"], "kind": "negative",
        "steps": [
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersBoundaryRepo"}, "bind": "u"},
            {"fn": "unit_scope_descriptor", "args": {"units": "$u.units", "ignore_paths": []}, "bind": "s"},
        ],
        "expect": {
            "$u.refused": None,
            "$u.units.0.rootPath": "", "$u.units.1.rootPath": "apps/site", "$u.units.2.rootPath": "apps/site/sub", "$u.units.3.rootPath": "vendor/lib",
            "$u.boundaries.source": "none", "$u.boundaries.nestedRepositories": [], "$u.boundaries.nestedProjects": [], "$u.boundaries.excludedUnits": [],
            "$s.boundaries.source": "none", "$s.boundaries.excludedPathPrefixesFromBoundaries": [],
        },
        "note": "Retained standalone behaviour of the pure instrument: without an admitted inventory it cannot know that vendor/lib is another repository or that apps/site is another project, and it says so (source none, disclosure). An operational host composition must pass the security instrument's inventory; this output is not proof of boundary completeness."
    },
    {
        "id": "units-boundary-inventory-whose-pruned-trees-disagree-with-the-marker-inventory-refuses",
        "feedback": ["PR2-P3"], "kind": "negative",
        "steps": [
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersBoundaryRepo",
                                              "boundaries": {"$merge": "$fixtures.boundaryInventoryRepo", "$with": {"prunedTrees": []}}}, "bind": "u"},
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersBoundaryRepo",
                                              "boundaries": {"$merge": "$fixtures.boundaryInventoryRepo", "$with": {"source": "caller-ignores"}}}, "bind": "bad", "expectError": "exact const type/value mismatch"},
        ],
        "expect": {
            "$u.units": [], "$u.refused.detail": "native.boundary-inventory-mismatch", "$u.refused.d9.code": "REQUEST.PRECONDITION_FAILED", "$u.refused.d9.exitCode": 2,
            "$u.refused.expectedPrunedTrees": [{"path": "vendor/lib/node_modules", "reason": "dependency-tree", "markerCount": 1}],
            "$u.refused.inventoryPrunedTrees": [],
        },
        "note": "An inventory that was not produced over this marker inventory (its pruned trees differ) is refused, and an inventory whose source is not the security instrument is schema-invalid: caller-supplied ignores are never accepted as the admitted boundary set."
    },
    {
        "id": "units-custody-excluded-directory-and-marker-from-the-admitted-inventory-are-outside-the-project",
        "feedback": ["R1", "PR2-P3"], "kind": "negative",
        "steps": [
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersCustody", "boundaries": "$fixtures.boundaryInventoryCustody"}, "bind": "u"},
            {"fn": "assign_membership", "args": {"units": "$u.units", "files": ["index.js", "src/main.rs", "tools/x.js", "tools/inner/src/lib.rs"], "boundaries": "$fixtures.boundaryInventoryCustody"}, "bind": "m"},
            {"fn": "unit_scope_descriptor", "args": {"units": "$u.units", "ignore_paths": [], "explicit_path_prefixes": None, "pruned_trees": "$u.prunedTrees", "boundaries": "$fixtures.boundaryInventoryCustody"}, "bind": "s"},
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersCustody", "explicit_workspace_roots": ["tools"], "boundaries": "$fixtures.boundaryInventoryCustody"}, "bind": "e"},
        ],
        "expect": {
            "$u.refused": None, "$u.units": [{"unitOrdinal": 0, "rootPath": "", "languageFamily": "tsjs", "languageMode": "js-synthesized", "unitKind": "js-program", "markerPath": "package.json", "markerSha256": H('b'), "recognizerId": "node-package", "recognizerVersion": 1, "provenance": "DISCOVERED", "memberPackageRoots": []}],
            "$u.boundaries.excludedUnits": [
                {"path": "", "marker": "Cargo.toml", "reason": "custody-excluded", "anchor": ""},
                {"path": "tools", "marker": "package.json", "reason": "custody-excluded", "anchor": "tools"},
                {"path": "tools/inner", "marker": "Cargo.toml", "reason": "custody-excluded", "anchor": "tools"}],
            "$m.rows.0.path": "index.js", "$m.rows.0.membership": "program-member",
            "$m.rows.1.path": "src/main.rs", "$m.rows.1.membership": "syntax-only", "$m.rows.1.reason": "no-program-unit-for-language",
            "$m.rows.2.path": "tools/inner/src/lib.rs", "$m.rows.2.membership": "outside-project-boundary", "$m.rows.2.reason": "custody-excluded",
            "$m.rows.3.path": "tools/x.js", "$m.rows.3.membership": "outside-project-boundary", "$m.rows.3.reason": "custody-excluded",
            "$s.scopeDescriptor.excludedPathPrefixes": [".git", "node_modules", "tools"],
            "$e.refused.detail": "native.explicit-root-crosses-boundary", "$e.refused.reason": "custody-excluded", "$e.refused.anchor": "tools",
        },
        "note": "A root Cargo.toml the security instrument excluded for marker custody makes no rust unit (its .rs files are honest syntax-only, not erased), a directory excluded for directory custody is outside the project with everything below it, only the directory exclusion becomes a scope prefix, and an explicit root into it refuses. Security's excludedUnits rows are copied verbatim into the inventory; the native layer never re-decides custody."
    },
    {
        "id": "units-explicit-cargo-workspace-root-keeps-member-folding-and-member-target-pruning",
        "feedback": ["R1", "R6", "PR2-P22"], "kind": "positive",
        "steps": [
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersCargoWorkspaceTwoMembers"}, "bind": "auto"},
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersCargoWorkspaceTwoMembers", "explicit_workspace_roots": ["."]}, "bind": "expl"},
            {"fn": "assign_membership", "args": {"units": "$auto.units", "files": ["crates/a/src/lib.rs", "crates/a/target/debug/x.rs", "crates/a/src/target/mod.rs", "target/debug/y.rs"]}, "bind": "ma"},
            {"fn": "assign_membership", "args": {"units": "$expl.units", "files": ["crates/a/src/lib.rs", "crates/a/target/debug/x.rs", "crates/a/src/target/mod.rs", "target/debug/y.rs"]}, "bind": "me"},
            {"fn": "discover_units", "args": {"markers": "$fixtures.markersCargoWorkspaceTwoMembers", "explicit_workspace_roots": ["crates/a"]}, "bind": "member"},
            {"fn": "assign_membership", "args": {"units": "$member.units", "files": ["crates/a/src/lib.rs", "crates/a/target/debug/x.rs", "crates/b/src/lib.rs", "target/debug/y.rs"]}, "bind": "mm"},
            {"fn": "unit_scope_descriptor", "args": {"units": "$expl.units", "ignore_paths": []}, "bind": "s"},
        ],
        "expect": {
            "$auto.units.0.unitKind": "cargo-workspace", "$auto.units.0.memberPackageRoots": ["crates/a", "crates/b"],
            "$expl.refused": None, "$expl.units.0.unitKind": "cargo-workspace", "$expl.units.0.provenance": "EXPLICIT",
            "$expl.units": [{"unitOrdinal": 0, "rootPath": "", "languageFamily": "rust", "languageMode": "rust-cargo", "unitKind": "cargo-workspace", "markerPath": "Cargo.toml", "markerSha256": H('1'), "recognizerId": "cargo-workspace", "recognizerVersion": 1, "provenance": "EXPLICIT", "memberPackageRoots": ["crates/a", "crates/b"]}],
            "$ma.rows": "$me.rows",
            "$me.rows.0.path": "crates/a/src/lib.rs", "$me.rows.0.reason": "deepest-unit-in-language",
            "$me.rows.1.path": "crates/a/src/target/mod.rs", "$me.rows.1.reason": "deepest-unit-in-language",
            "$me.rows.2.path": "crates/a/target/debug/x.rs", "$me.rows.2.reason": "host-ignore-convention",
            "$me.rows.3.path": "target/debug/y.rs", "$me.rows.3.reason": "host-ignore-convention",
            "$member.refused": None, "$member.units.0.rootPath": "crates/a", "$member.units.0.unitKind": "cargo-package", "$member.units.0.memberPackageRoots": [],
            "$member.units": [{"unitOrdinal": 0, "rootPath": "crates/a", "languageFamily": "rust", "languageMode": "rust-cargo", "unitKind": "cargo-package", "markerPath": "crates/a/Cargo.toml", "markerSha256": H('2'), "recognizerId": "cargo-package", "recognizerVersion": 1, "provenance": "EXPLICIT", "memberPackageRoots": []}],
            "$mm.rows.0.path": "crates/a/src/lib.rs", "$mm.rows.0.reason": "deepest-unit-in-language",
            "$mm.rows.1.path": "crates/a/target/debug/x.rs", "$mm.rows.1.reason": "host-ignore-convention",
            "$mm.rows.2.path": "crates/b/src/lib.rs", "$mm.rows.2.reason": "no-program-unit-for-language",
            "$mm.rows.3.path": "target/debug/y.rs", "$mm.rows.3.reason": "no-program-unit-for-language",
            "$s.scopeDescriptor.excludedPathPrefixes": [".git", "crates/a/target", "crates/b/target", "node_modules", "target"],
        },
        "note": "P22: naming the Cargo workspace root explicitly yields exactly the automatic result (members folded, member target output pruned, `crates/a/src/target` stays source). Naming a member package alone selects that package: files of the unselected member and the unselected root are honest no-program-unit rows, not silently claimed and not over-ignored."
    },
]
new_ids = {c['id'] for c in cases}
doc['cases'] = [c for c in doc['cases'] if c['id'] not in new_ids]
doc['cases'].extend(cases)
ids = [c['id'] for c in doc['cases']]
assert len(ids) == len(set(ids))
P.write_bytes((json.dumps(doc, indent=1, ensure_ascii=True) + '\n').encode())
print('cases now', len(doc['cases']))
