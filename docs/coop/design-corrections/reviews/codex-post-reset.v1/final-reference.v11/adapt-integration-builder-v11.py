"""Adapt the shared synthetic builder from the final coauthor fixture.
Run only after final actual coauthor source capture. The copied data is not an oracle. Reconcile helper list against the final handoff before use.
"""
from pathlib import Path
import ast, hashlib
root=Path.cwd();dc=root/'docs/coop/design-corrections';assert (dc/'reviews/digest-corrections-author.v9/custody.json').is_file(), 'Retain completed actual coauthor source first';source=dc/'foundation/check-identity.py';raw=source.read_text();tree=ast.parse(raw)
# Reconciled with released v8 handoff: header supplies loader/module globals; retain historical exported constants used by callers and add unit, UID, replay plus body helpers. The authored closure count label is not used as an oracle.
import json
handoff=json.loads((dc/'reviews/digest-corrections-author.v9/handoff.json').read_text())
owned={row['path']:row['sha256'] for row in handoff['ownedFilesChanged']}
assert hashlib.sha256(source.read_bytes()).hexdigest()==owned[str(source.relative_to(root))], 'Author source changed before fixture extraction'
names={'unit', 'UID', 'replay', 'LEVEL_SPECIFICATION', 'framed_body_preimage', 'relation_fixture', 'body_language_version', 'ATOM', 'RUST_TARGET', 'CURRENT_CAPABILITY_MANIFEST_BYTES', 'TS_SOURCES', 'resync_coverage', 'native_inputs', 'RUST_DEP_FILE', 'resync_witness', 'compiled_program', 'DELIVERY', 'rust_inputs', 'WAIVERS', 'RUST_DEP_KEY', 'rekey_plan', 'RULE', 'CAPABILITY_RECIPE', 'FILTER_FIELD_OF', 'put_blob', 'LANGUAGE_FIXTURE', 'sort_canonical_sets', 'RELATION_DOCUMENT_BYTES', 'INHERITED_MANIFEST_BYTES', 'rekey', 'NATIVE_DOCUMENT', 'RELATION_DOCUMENT', 'resync_stage_spec', 'RELATION_DOCUMENT_DIGEST', 'NATIVE_DOCUMENT_BYTES', 'RUST_PROJECTED_CONFIG', 'graph_with_import', 'RELATION_REGISTRY', 'build', 'rule_for', 'RUST_PREPARED_DIRECTIVES', 'current_capability_manifest', 'policy_for', 'NATIVE_DOCUMENT_DIGEST', 'coverage_result', 'RUST_SOURCES', 'resync_proof_refs', 'POLICY', 'STAGE_OUTPUT_SCHEMA', 'REFERENCES_PAYLOAD', 'TS_NODE_MODULES'}
blocks=[];found=set()
for node in tree.body:
    declared={node.name} if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) else ({t.id for t in node.targets if isinstance(t,ast.Name)} if isinstance(node,ast.Assign) else set())
    if names&declared:blocks.append(ast.get_source_segment(raw,node));found|=names&declared
assert found==names,('Author fixture interface changed; inspect before adapting',names-found)
target=dc/'integration-fixtures.py'
header='''"""Synthetic shared graph construction, copied from the corrected coauthor reference fixture.
Source: foundation/check-identity.py SHA256 SOURCE_HASH.
Copied declarations: DECLARATIONS.
No expected verdict or independent-review claim is derived from this builder.
Shared import/source mutations retain their own explicit preimage propagation.
"""
import copy,hashlib,json,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent/'foundation'
spec=importlib.util.spec_from_file_location('integration_fixture_identity',H/'identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
W=M.workflow_admission()
spec=importlib.util.spec_from_file_location('integration_fixture_native',H.parent/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
NATIVE_FIXTURES=json.loads((H.parent/'native/native-cases.v2.json').read_text())['fixtures']

'''.replace('SOURCE_HASH',hashlib.sha256(source.read_bytes()).hexdigest()).replace('DECLARATIONS',', '.join(sorted(names)))
new=header+'\n\n'.join(blocks)+'\n';compile(new,str(target),'exec');target.write_text(new)
print('Adapted shared synthetic builder; explicit fixture-source hash retained.')
