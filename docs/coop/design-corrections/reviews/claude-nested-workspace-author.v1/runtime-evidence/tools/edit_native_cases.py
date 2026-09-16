"""Insert the nested Cargo workspace fixture and case into native-cases.v2.json with a minimal textual diff.

Usage: edit_native_cases.py CASES_JSON

The file is re-serialized only if json.dumps(json.loads(raw), indent=1, ensure_ascii=X) + "\n" reproduces the original
bytes exactly for some X; otherwise it refuses. The fixture follows `markersCargoWorkspaceTwoMembers`; the case follows
`units-explicit-cargo-workspace-root-keeps-member-folding-and-member-target-pruning` (not the end of the array).
"""
import hashlib
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
raw = path.read_bytes()
doc = json.loads(raw)
style = None
for ensure_ascii in (False, True):
    if (json.dumps(doc, indent=1, ensure_ascii=ensure_ascii) + "\n").encode("utf-8") == raw:
        style = ensure_ascii
        break
if style is None:
    raise SystemExit("native-cases.v2.json does not round-trip through json.dumps(indent=1); refusing to rewrite")

FIXTURE = "markersCargoNestedWorkspace"
CASE_ID = "units-nested-cargo-workspace-folds-into-the-deepest-surviving-workspace-unit"
AFTER_FIXTURE = "markersCargoWorkspaceTwoMembers"
AFTER_CASE = "units-explicit-cargo-workspace-root-keeps-member-folding-and-member-target-pruning"
if FIXTURE in doc["fixtures"] or any(c["id"] == CASE_ID for c in doc["cases"]):
    raise SystemExit("already present")


def cargo(digit, ws):
    return {"sha256": digit * 64, "isCargoWorkspace": ws}


def unit(root, kind, marker, digit, provenance, members):
    return {"unitOrdinal": 0, "rootPath": root, "languageFamily": "rust", "languageMode": "rust-cargo", "unitKind": kind,
            "markerPath": marker, "markerSha256": digit * 64, "recognizerId": kind, "recognizerVersion": 1,
            "provenance": provenance, "memberPackageRoots": members}


def member_row(p):
    return {"path": p, "languageFamily": "rust", "unitOrdinal": 0, "membership": "program-member", "reason": "deepest-unit-in-language"}


def ignored_row(p):
    return {"path": p, "languageFamily": "rust", "unitOrdinal": None, "membership": "syntax-only", "reason": "host-ignore-convention"}


fixture = {"Cargo.toml": cargo("1", True), "nested-x/Cargo.toml": cargo("4", False), "nested/Cargo.toml": cargo("2", True),
           "nested/pkg/Cargo.toml": cargo("3", False), "nested/pkg/target/debug/build/x/Cargo.toml": cargo("5", False)}
pruned = [{"path": "nested/pkg/target", "reason": "cargo-build-output", "markerCount": 1, "markerCountBasis": "observed-inventory"}]
m = "$fixtures." + FIXTURE
files = ["nested-x/src/lib.rs", "nested/pkg/src/lib.rs", "nested/pkg/target/debug/x.rs", "nested/src/target/mod.rs",
         "nested/target/debug/y.rs", "src/main.rs"]
case = {
    "id": CASE_ID,
    "feedback": ["R1", "R6", "PR2-P22"],
    "kind": "positive",
    "steps": [
        {"fn": "discover_units", "args": {"markers": m}, "bind": "auto"},
        {"fn": "discover_units", "args": {"markers": m, "explicit_workspace_roots": ["."]}, "bind": "expl"},
        {"fn": "discover_units", "args": {"markers": m, "explicit_workspace_roots": [".", "nested"]}, "bind": "both"},
        {"fn": "discover_units", "args": {"markers": m, "explicit_workspace_roots": ["nested"]}, "bind": "inner"},
        {"fn": "discover_units", "args": {"markers": m, "explicit_workspace_roots": ["nested/pkg"]}, "bind": "leaf"},
        {"fn": "discover_units", "args": {"markers": m, "boundaries": {
            "schemaVersion": 2, "source": "security.discovery", "selectedRoot": "/home/alice/repo", "nestedRepositories": [],
            "nestedProjects": ["nested-x"], "custodyExcludedUnits": [], "prunedTrees": pruned}}, "bind": "bnd"},
        {"fn": "assign_membership", "args": {"units": "$auto.units", "files": files}, "bind": "ma"},
        {"fn": "unit_scope_descriptor", "args": {"units": "$auto.units", "ignore_paths": []}, "bind": "s"},
    ],
    "expect": {
        "$auto.refused": None,
        "$auto.units": [unit("", "cargo-workspace", "Cargo.toml", "1", "DISCOVERED", ["nested", "nested-x", "nested/pkg"])],
        "$auto.prunedTrees": pruned,
        "$expl.refused": None,
        "$expl.units": [unit("", "cargo-workspace", "Cargo.toml", "1", "EXPLICIT", ["nested", "nested-x", "nested/pkg"])],
        "$both.units": "$expl.units",
        "$inner.units": [unit("nested", "cargo-workspace", "nested/Cargo.toml", "2", "EXPLICIT", ["nested/pkg"])],
        "$leaf.units": [unit("nested/pkg", "cargo-package", "nested/pkg/Cargo.toml", "3", "EXPLICIT", [])],
        "$bnd.refused": None,
        "$bnd.units.0.memberPackageRoots": ["nested", "nested/pkg"],
        "$bnd.boundaries.excludedUnits": [{"path": "nested-x", "marker": "Cargo.toml", "reason": "nested-project", "anchor": "nested-x"}],
        "$ma.rows": [member_row("nested-x/src/lib.rs"), member_row("nested/pkg/src/lib.rs"), ignored_row("nested/pkg/target/debug/x.rs"),
                     member_row("nested/src/target/mod.rs"), ignored_row("nested/target/debug/y.rs"), member_row("src/main.rs")],
        "$s.scopeDescriptor.excludedPathPrefixes": [".git", "nested-x/target", "nested/pkg/target", "nested/target", "node_modules", "target"],
    },
    "note": ("U-4b.2: the fold target is the deepest enclosing SURVIVING cargo-workspace unit. `nested` declares a workspace but "
             "lies below the root workspace unit, so it is a folded member and `nested/pkg` folds into the root unit too "
             "(looking `nested` up as a unit raised StopIteration). Member roots are strict UTF-8 order (`nested-x` before "
             "`nested/pkg`); every folded root keeps its `target` pruned while `nested/src/target` stays source. P22: `.` "
             "and `.`+`nested` equal the automatic unit, `nested` alone is its own workspace unit with `nested/pkg`, "
             "`nested/pkg` alone is a cargo-package unit. U-8: a nested project at `nested-x` is excluded and never folded. "
             "Trusted marker observations only; no Cargo layout validity is asserted."),
}

fixtures = {}
for k, v in doc["fixtures"].items():
    fixtures[k] = v
    if k == AFTER_FIXTURE:
        fixtures[FIXTURE] = fixture
if FIXTURE not in fixtures:
    raise SystemExit("anchor fixture missing")
doc["fixtures"] = fixtures
index = next(i for i, c in enumerate(doc["cases"]) if c["id"] == AFTER_CASE)
doc["cases"].insert(index + 1, case)
out = (json.dumps(doc, indent=1, ensure_ascii=style) + "\n").encode("utf-8")
path.write_bytes(out)
print(json.dumps({"ensureAscii": style, "beforeSha256": hashlib.sha256(raw).hexdigest(), "beforeBytes": len(raw),
                  "afterSha256": hashlib.sha256(out).hexdigest(), "afterBytes": len(out), "caseIndex": index + 1,
                  "cases": len(doc["cases"])}, indent=1))
