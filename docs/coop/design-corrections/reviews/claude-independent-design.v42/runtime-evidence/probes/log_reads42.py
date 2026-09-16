"""Append the read-ledger rows for reads performed so far this charter (exact paths and ranges read with the Read tool; hashes
and line counts recomputed now). Same row format as ledger.py."""
import datetime, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v42'
S42 = '/tmp/opensip-design-corrections/candidate-subject.v42'
FD = 'docs/coop/design-corrections/foundation/'
ROWS = [
    ('fresh42Read', 'complete single read', FD + 'execution-inputs-contract.v1.md', '1-303'),
    ('fresh42Read', 'complete single read', FD + 'enumeration-contract.v1.md', '1-186'),
    ('fresh42Read', 'complete single read', FD + 'execution_inputs_fixture.v3.py', '1-505'),
    ('fresh42Read', 'complete single read (v9 and v10 are byte-identical bytes)', 'docs/v2/architecture/implementation-normative-inputs.v11.json', '1-160'),
    ('fresh42Read', 'promised_pointers', FD + 'execution_inputs_model.v1.py', '150-244'),
    ('fresh42Read', 'plan/execution-plan joins, resolution, receipts, attribution loop, accounts', FD + 'execution_inputs_model.v1.py', '860-1464'),
    ('fresh42Read', 'stage ordinal, receipt producer, selectedRefs exact totality', FD + 'execution_inputs_model.v1.py', '1600-1733'),
    ('fresh42Read', '_u1_entry, snapshot index, unit roots', FD + 'enumeration_model.v1.py', '425-519'),
    ('fresh42Read', 'binding enumerator/context/universe/programEntry joins', FD + 'enumeration_model.v1.py', '740-879'),
    ('fresh42Read', 'close_run, open_run_closure head', FD + 'identity-model.v3.py', '866-960'),
    ('fresh42Read', 'stage specs, evaluation view roots, per-view planId/producer/scope/partition/coverage closure', FD + 'identity-model.v3.py', '1760-1944'),
    ('fresh42Read', 'execution_input_account and enumeration admission in reconstruct', FD + 'evaluator_input_model.v3.py', '1-175'),
    ('fresh42Read', 'checker module wiring and primitives', FD + 'check-execution-inputs.v1.py', '1-108'),
    ('fresh42Read', 'full_run driver and full_run_case', FD + 'check-execution-inputs.v1.py', '696-815'),
    ('fresh42Read', 'seed scanner, seed_seal, seal_derived, builder signature', FD + 'evaluator_semantic_fixture.v3.py', '148-307'),
    ('fresh42Read', 'semantic views/scopes/facts and returned graph keys', FD + 'evaluator_semantic_fixture.v3.py', '560-809'),
    ('fresh42Read', 'fixture helpers and build_file_inputs docstring', FD + 'evaluator_graph_fixture.v3.py', '1-60'),
    ('fresh42Read', 'required-native views, unsupported cell, stage, inputs, seal_fixture', FD + 'evaluator_graph_fixture.v3.py', '280-390'),
    ('fresh42Read', 'baseline helpers and main head', FD + 'check-enumeration.v1.py', '60-349'),
    ('fresh42Read', 'Available/Unavailable program binding definitions', FD + 'enumeration-plan.schema.v1.json', '330-489'),
    ('delta41to42Read', 'complete 41->42 diff (identical to the 40->42 diff)', FD + 'check-enumeration.v1.py', 'complete'),
    ('delta41to42Read', 'complete 41->42 diff (identical to the 40->42 diff)', FD + 'enumeration-contract.v1.md', 'complete'),
    ('delta41to42Read', 'complete 41->42 diff (identical to the 40->42 diff)', FD + 'enumeration_model.v1.py', 'complete'),
    ('delta41to42Read', 'complete 41->42 diff (identical to the 40->42 diff)', FD + 'evaluator_graph_fixture.v3.py', 'complete'),
    ('delta40to42Read', 'complete 40->42 diff', FD + 'execution-inputs-contract.v1.md', 'complete'),
    ('delta40to42Read', 'complete 40->42 diff', FD + 'execution_inputs_model.v1.py', 'complete'),
    ('delta40to42Read', 'complete 40->42 diff', FD + 'execution_inputs_fixture.v3.py', 'complete'),
    ('delta40to42Read', 'complete 40->42 diff', FD + 'check-execution-inputs.v1.py', 'complete'),
    ('delta40to42Read', 'complete 40->42 diff', 'docs/v2/architecture/implementation-planning-sources.v1.json', 'complete'),
    ('delta40to42Read', 'complete 40->42 diff', 'docs/v2/architecture/implementation-coverage.v1.json', 'complete'),
    ('delta40to42Read', 'complete 40->42 diff', 'docs/coop/design-corrections/workflows/workflows-report.v1.json', 'complete'),
    ('evidenceRead', 'author proposal, complete', '/tmp/opensip-design-corrections/claude-view-attribution-assessment.v1/review.md', 'complete'),
    ('evidenceRead', 'author proposal, complete', '/tmp/opensip-design-corrections/claude-attribution-capture-assessment.v1/review.md', 'complete'),
    ('evidenceRead', 'author proposal, complete', '/tmp/opensip-design-corrections/claude-program-entry-clarification.v1/review.md', 'complete'),
    ('evidenceRead', 'author proposal, complete', '/tmp/opensip-design-corrections/claude-program-entry-enforcement.v1/review.md', 'complete'),
    ('evidenceRead', 'root integration record, complete', '/tmp/opensip-design-corrections/root-view-attribution-integration.v1/integration.json', 'complete'),
    ('evidenceRead', 'root integration record, complete', '/tmp/opensip-design-corrections/root-capture-integration.v1/integration.json', 'complete'),
    ('evidenceRead', 'root integration record, complete', '/tmp/opensip-design-corrections/root-program-entry-enforcement-integration.v1/assessment.json', 'complete'),
    ('evidenceRead', 'root integration record, complete', '/tmp/opensip-design-corrections/root-program-entry-clarification-integration.v1/integration.json', 'complete'),
    ('evidenceRead', 'root planning clarification, complete', '/tmp/opensip-design-corrections/root-planning-layer-history-clarification.v1/change.diff', 'complete'),
    ('evidenceRead', 'root planning clarification, complete', '/tmp/opensip-design-corrections/root-planning-layer-history-clarification.v1/assessment.json', 'complete'),
    ('evidenceRead', 'package binding, complete', '/tmp/opensip-design-corrections/claude-author-package-successor.v19/source-binding.v42.json', 'complete'),
    ('evidenceRead', 'root verification, complete', '/tmp/opensip-design-corrections/author-package-final42-verification.v1/verification.json', 'complete'),
    ('evidenceRead', 'rebuild report head', '/tmp/opensip-design-corrections/root-author-package-final42-rebuild.v1/rebuild-report.json', '1-120'),
]
with open(RT + '/receipts/read-ledger.jsonl', 'a', encoding='utf-8') as out:
    for kind, note, path, rng in ROWS:
        full = path if path.startswith('/') else os.path.join(S42, path)
        b = open(full, 'rb').read()
        row = {'kind': kind, 'path': path, 'range': rng, 'sha256': hashlib.sha256(b).hexdigest(),
               'lines': b.count(b'\n') + (0 if not b or b.endswith(b'\n') else 1), 'note': note, 'at': datetime.datetime.now().isoformat(timespec='seconds')}
        if kind.startswith('delta'):
            key = kind[len('delta'):-len('Read')]
            d = RT + '/receipts/delta-diffs-' + key + '/' + path.replace('/', '__') + '.diff'
            row['diff'] = d.replace(RT + '/', '')
            row['diffSha256'] = hashlib.sha256(open(d, 'rb').read()).hexdigest()
        out.write(json.dumps(row) + '\n')
print(len(ROWS), 'rows appended')
