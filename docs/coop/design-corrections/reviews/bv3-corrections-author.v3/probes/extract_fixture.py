#!/usr/bin/env python3
"""Extract the synthetic construction helpers into integration-fixtures.py, using root's exact
declaration set and mechanism.

This mirrors root-input/codex-rechecks/adapt-integration-builder-v13.py so root's own probes can be
re-run against CORRECTED source. Root's version asserts the v1 handoff hash (its integration flow);
this one takes the target root as an argument and skips that pin, because the source is deliberately
newer. It writes only into a DISPOSABLE copy and never into the released delta -- root owns fixture
adaptation.
"""
import ast
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
dc = root / "docs/coop/design-corrections"
source = dc / "foundation/check-identity.py"
raw = source.read_text()
tree = ast.parse(raw)

# Root's exact set, from adapt-integration-builder-v13.py. Preserving this interface is a hard
# constraint on the released source: if any name stops being a module-level declaration, root's
# fixture adaptation fails its own assert.
names = {'GRAMMAR_FILES', 'syntax_inputs', 'SCOPE_DOCUMENT', 'unit', 'UID', 'replay',
         'LEVEL_SPECIFICATION', 'framed_body_preimage', 'relation_fixture', 'body_language_version',
         'ATOM', 'RUST_TARGET', 'CURRENT_CAPABILITY_MANIFEST_BYTES', 'TS_SOURCES', 'resync_coverage',
         'native_inputs', 'RUST_DEP_FILE', 'resync_witness', 'compiled_program', 'DELIVERY',
         'rust_inputs', 'WAIVERS', 'RUST_DEP_KEY', 'rekey_plan', 'RULE', 'CAPABILITY_RECIPE',
         'FILTER_FIELD_OF', 'put_blob', 'LANGUAGE_FIXTURE', 'sort_canonical_sets',
         'RELATION_DOCUMENT_BYTES', 'INHERITED_MANIFEST_BYTES', 'rekey', 'NATIVE_DOCUMENT',
         'RELATION_DOCUMENT', 'resync_stage_spec', 'RELATION_DOCUMENT_DIGEST', 'NATIVE_DOCUMENT_BYTES',
         'RUST_PROJECTED_CONFIG', 'graph_with_import', 'RELATION_REGISTRY', 'build', 'rule_for',
         'RUST_PREPARED_DIRECTIVES', 'current_capability_manifest', 'policy_for',
         'NATIVE_DOCUMENT_DIGEST', 'coverage_result', 'RUST_SOURCES', 'resync_proof_refs', 'POLICY',
         'STAGE_OUTPUT_SCHEMA', 'REFERENCES_PAYLOAD', 'TS_NODE_MODULES'}
# Helpers this correction pass added that the extracted builder now depends on.
extra = {'retained_clone_ownership', '_clone_disclosure', 'shared_workspace', 'mirror_admits'}

blocks, found = [], set()
for node in tree.body:
    declared = ({node.name} if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                else ({t.id for t in node.targets if isinstance(t, ast.Name)}
                      if isinstance(node, ast.Assign) else set()))
    if (names | extra) & declared:
        blocks.append(ast.get_source_segment(raw, node))
        found |= (names | extra) & declared

missing = names - found
if missing:
    sys.exit("root's required helper interface is broken: " + ", ".join(sorted(missing)))

header = '''"""Synthetic shared graph construction, extracted from the corrected coauthor reference fixture.
Source: foundation/check-identity.py SHA256 %s.
No expected verdict or independent-review claim is derived from this builder.
"""
import copy,hashlib,json,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent/'foundation'
spec=importlib.util.spec_from_file_location('integration_fixture_identity',H/'identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
W=M.workflow_admission()
spec=importlib.util.spec_from_file_location('integration_fixture_native',H.parent/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
NATIVE_FIXTURES=json.loads((H.parent/'native/native-cases.v2.json').read_text())['fixtures']

''' % hashlib.sha256(source.read_bytes()).hexdigest()

target = dc / "integration-fixtures.py"
new = header + "\n\n".join(blocks) + "\n"
compile(new, str(target), "exec")
target.write_text(new)
print("extracted %d declarations (root interface intact: %d/%d)" % (len(blocks), len(names & found), len(names)))
