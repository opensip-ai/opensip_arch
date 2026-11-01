# VD3-LAW r1: the opt-in package-successor profile of tools/verify_design.py

Law unit of PKG-ROWS-1 (PLAN-r3 section 2; Addendum-1), following VD2's F8c. It selects, by value:

- reference/tools/verify_design.py: VD3's verifier, the law reference (reference/verify_design.vd3.diff is
  `git diff 462a7a7e -- tools/verify_design.py`; applying it to the parent copy gives the candidate);
- product/tools/contracts/generator-closure.json and product/tools/typescript-lanes.json: the two registries re-pinned
  onto that verifier (each changes only its tools/verify_design.py row), which their consumers require to be selected
  (tools/generate_contracts.py, tools/check_typescript.py).

The profile. An inventory successor whose record carries "profile": "opensip.inventory-package-successor.v1" changes
raw packages, and its standing, only. Its record carries packageAdditions (complete rows) and dependencyAdditions ({from, to} onto
inherited rows), at least one entry in total, and "inheritedPackageRowsPreservedExceptDeclaredEdges": true. The
candidate's packages must equal the parent's rows with the declared edges appended in order, followed by the declared
rows in order. New rows have exactly id, path, kind, purpose, dependencies and standing; ids match [a-z][a-z0-9-]*;
paths are canonical repository-relative valid UTF-8, with no NUL or other ASCII control character; ids and paths are unique; kinds come from the parent's vocabulary; purposes
are nonempty valid UTF-8; standing is "proposed"; dependencies are unique, known and not the row itself, and Rust rows depend only on Rust rows. Edges
start at inherited rows, name known non-self targets, are unique and new. Files, pendingDecisions and schemaVersion
stay equal; the top-level standing may change (it describes the successor); no other top-level key changes. All equality is type-preserving canonical JSON. The independent
review restates profile, packageAdditions and dependencyAdditions, and the root assent names the profile. A record
without "profile" follows the unchanged additive-files rule, under which any package change refuses. The lock format is
unchanged. The profile names no particular package, so later package successors need no verifier change.

No product qualification, runtime admission or package admission beyond the inventory's rows is conferred.
