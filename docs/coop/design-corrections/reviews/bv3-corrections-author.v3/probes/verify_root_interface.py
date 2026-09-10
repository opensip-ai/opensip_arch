#!/usr/bin/env python3
"""Verify root's FIXED helper-extraction interface still works against corrected source.

Root's adapt-integration-builder-v13.py extracts exactly 54 module-level declarations by name from
foundation/check-identity.py and asserts the set is complete. If a correction makes one of those
declarations depend on a NEW module-level name, the extraction compiles but fails at import, and
root's rechecks break. This probe reproduces root's extraction using ONLY root's name set, then
imports the result and exercises it, so that coupling is caught here rather than by root.
"""
import ast
import importlib.util
import json
import sys
from pathlib import Path

work = Path(sys.argv[1])
dc = work / "docs/coop/design-corrections"
source = dc / "foundation/check-identity.py"
names = set(json.load(open(Path(__file__).parent / "required-helper-names.json")))

raw = source.read_text()
tree = ast.parse(raw)
blocks, found = [], set()
for node in tree.body:
    declared = ({node.name} if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                else ({t.id for t in node.targets if isinstance(t, ast.Name)}
                      if isinstance(node, ast.Assign) else set()))
    if names & declared:
        blocks.append(ast.get_source_segment(raw, node))
        found |= names & declared
if found != names:
    sys.exit("root interface INCOMPLETE, missing: " + ", ".join(sorted(names - found)))

header = """import copy,hashlib,json,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent/'foundation'
spec=importlib.util.spec_from_file_location('integration_fixture_identity',H/'identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
W=M.workflow_admission()
spec=importlib.util.spec_from_file_location('integration_fixture_native',H.parent/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
NATIVE_FIXTURES=json.loads((H.parent/'native/native-cases.v2.json').read_text())['fixtures']

"""
target = dc / "integration-fixtures.py"
target.write_text(header + "\n\n".join(blocks) + "\n")

spec = importlib.util.spec_from_file_location("root_iface_fixture", target)
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)

results = {"namesExtracted": len(found), "namesRequired": len(names), "importedCleanly": True}
# Exercise the entry points root's own probes call.
run, objects, blobs = fixture.build(universe_language="syntax", relation="file", source_path="README.md")
results["inventoryControlRunId"] = fixture.M.close_run(run, objects, blobs)
run, objects, blobs = fixture.build()
results["baseControlRunId"] = fixture.M.close_run(run, objects, blobs)
results["graphWithImportRunId"] = fixture.M.close_run(*fixture.graph_with_import())
print(json.dumps(results, indent=2))
