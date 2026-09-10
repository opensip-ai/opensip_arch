"""CB-ADV-1 adjacent site: ProofInputRef domain `schema` carries the SAME published word.

`x-opensip-digest-domains.schema` is `raw-artifact` with artifact text "the exact complete
registered schema document bytes". If registration is enforced nowhere, an arbitrary retained blob
stands in an evaluation input ref where a registered schema document is named. Probed against
whichever tree is passed as argv[1].
"""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE = sys.argv[1]
FOUND = HERE.parent / TREE / 'docs/coop/design-corrections/foundation'

s = importlib.util.spec_from_file_location('probe_fixtures_' + TREE.replace('-', '_'),
                                           FOUND / '_probe_fixtures.py')
F = importlib.util.module_from_spec(s)
s.loader.exec_module(F)
M, C = F.M, F.C
results = []


def outcome(name, fn):
    try:
        value = fn()
    except BaseException as exc:                     # noqa: BLE001
        row = {'probe': name, 'admitted': False,
               'fault': type(exc).__name__ + ':' + str(exc)[:200]}
    else:
        row = {'probe': name, 'admitted': True, 'runId': value}
    results.append(row)
    print(json.dumps(row))


def with_schema_ref(raw):
    run, objects, blobs = F.build()
    digest = hashlib.sha256(raw).hexdigest()
    blobs[digest] = raw
    pk = objects[run['evaluationSealId']][1]['proofBundleId']
    proof = copy.deepcopy(objects[pk][1])
    proof['evaluationInputRefs'] = sorted(
        proof['evaluationInputRefs'] + [{'domain': 'schema', 'digest': digest}], key=C.canonical)
    F.rekey(objects, pk, proof, run)
    return run, objects, blobs


outcome('P4-a-registered-schema-document-as-an-evaluation-input',
        lambda: M.close_run(*with_schema_ref(
            (FOUND / 'relation-payload-schemas.v2.json').read_bytes())))
outcome('P4-b-arbitrary-retained-blob-as-a-schema-evaluation-input',
        lambda: M.close_run(*with_schema_ref(b'{"not":"a registered schema document"}\n')))

(HERE / ('p4_schema_input_ref.%s.results.json' % TREE)).write_text(
    json.dumps({'tree': TREE, 'results': results}, indent=1) + '\n')
