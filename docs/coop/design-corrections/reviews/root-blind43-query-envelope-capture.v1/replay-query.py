"""Capture strong owner outcomes for the observed blind24 vector/export formats.
No consumer imports, repair, cursor translation, response-based input selection,
or automatic conformance verdict. A complete admitted Run is a prerequisite.
"""
from pathlib import Path
import argparse, copy, hashlib, importlib.util, json


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def selected_cases(vectors, label):
    assert isinstance(vectors.get('vectors'), list), 'Missing vectors array'
    rows = vectors['vectors']
    assert all(type(r) is dict and type(r.get('vector')) is str and type(r.get('run')) is str for r in rows)
    assert len({r['vector'] for r in rows}) == len(rows), 'Duplicate vector names'
    selected = [r for r in rows if r['run'] == label]
    assert selected, 'No vectors for explicit Run label'
    for row in selected:
        assert 'request' in row, 'Missing exact request'
        assert type(row.get('hostObservations')) is dict, 'Missing exact host observations'
        assert ('response' in row) != ('failureEnvelope' in row), 'Missing or ambiguous recorded response'
    return selected


def execute_selected(M, Q, run_id, objects, blobs, rows, report):
    """No query call is made if transport/structural/full semantic admission fails."""
    try:
        domain, run = objects[run_id]
        assert domain == 'run'
        report['structuralAdmission'] = 'REFUSE'
        assert M.open_run_closure(run, objects, blobs)[0] == run_id
        report['structuralAdmission'] = 'ADMIT'
        report['semanticAdmission'] = 'REFUSE'
        assert M.close_run(run, objects, blobs) == run_id
        report['semanticAdmission'] = 'ADMIT'
    except Exception as exc:
        report.update(exceptionType=type(exc).__name__, reason=str(exc))
        return False
    for row in rows:
        item = {'vector': row['vector'], 'runLabel': row['run'],
                'request': copy.deepcopy(row['request']),
                'hostObservations': copy.deepcopy(row['hostObservations']),
                'consumerResponse': copy.deepcopy(row.get('response')),
                'consumerFailureEnvelope': copy.deepcopy(row.get('failureEnvelope'))}
        host = copy.deepcopy(row['hostObservations'])
        qm = Q.identity3()
        old_close = qm.close_run
        item['boundary'] = 'strong-query'
        try:
            if 'availabilityRecord' in host:
                # Decode only the consumer's declared byte transport; the frozen owner admits the record.
                carrier = host.pop('availabilityRecord')
                assert set(carrier) == {'rawBytesHex'}
                raw = bytes.fromhex(carrier['rawBytesHex'])
                assert raw.hex() == carrier['rawBytesHex']
                item['boundary'] = 'retained-availability-admission then strong-query'
                host['availability'] = Q.observe_retained_availability(raw, run_id)
            if row['vector'] == 'close-run-non-typed-exception-host-invariant':
                # Exact declared synthetic exception, after full positive admission; no Run qualification claim.
                def injected(*args, **kwargs):
                    raise RuntimeError('EVIDENCE_UNAVAILABLE:text that resembles an owner key')
                qm.close_run = injected
                item['boundary'] = 'strong-query with declared synthetic close_run RuntimeError'
            try:
                item['ownerResponse'] = Q.execute_graph_query(copy.deepcopy(row['request']),
                    copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs), host=host)
                item['ownerOutcome'] = 'RETURNED'
            except Q.ReferenceCallPrecondition as exc:
                if host.get('hostMode') != 'adapter':
                    raise
                item['boundary'] = 'strong-query precondition then declared host adapter'
                raise Q.host_adapter_refusal(exc, request=copy.deepcopy(row['request']), host=host)
        except Exception as exc:
            item.update(ownerOutcome='RAISED', exceptionType=type(exc).__name__, reason=str(exc))
            if isinstance(exc, Q.QueryRefusal):
                item['ownerFailureEnvelope'] = exc.envelope(host=copy.deepcopy(row['hostObservations']))
        finally:
            qm.close_run = old_close
        report['cases'].append(item)
    return True


def main():
    p = argparse.ArgumentParser()
    for name in ['source', 'manifest', 'export', 'vectors', 'transport', 'out']:
        p.add_argument('--'+name, type=Path, required=True)
    for name in ['manifest-sha256', 'transport-sha256', 'run-id', 'run-label']:
        p.add_argument('--'+name, required=True)
    a = p.parse_args()
    assert not a.out.exists(), 'Use a fresh output path'
    for root in [a.source, a.export.parent, a.vectors.parent]:
        assert not a.out.resolve().is_relative_to(root.resolve()), 'Output must be outside inputs'
    mf = a.manifest.read_bytes()
    assert sha(mf) == a.manifest_sha256
    assert sha(a.transport.read_bytes()) == a.transport_sha256
    R = load('root_query_transport24', a.transport)
    manifest = R.parse(mf)
    for row in manifest['files']:
        path = a.source / row['path']
        assert not path.is_symlink()
        raw = path.read_bytes()
        assert len(raw) == row['bytes'] and sha(raw) == row['sha256'], row['path']
    model = a.source/'docs/coop/design-corrections/foundation/identity-model.v3.py'
    query = a.source/'docs/coop/design-corrections/workflows/query_projection_model.v3.py'
    M = load('root_query_identity24', model)
    Q = load('root_query_owner24', query)
    raw, vraw = a.export.read_bytes(), a.vectors.read_bytes()
    vectors = R.parse(vraw)
    rows = selected_cases(vectors, a.run_label)
    if a.run_label in vectors.get('runs', {}):
        assert vectors['runs'][a.run_label] == a.run_id, 'Explicit Run id contradicts retained vector label'
    a.out.mkdir(parents=True)
    (a.out/'exact-export.json').write_bytes(raw)
    (a.out/'exact-vectors.json').write_bytes(vraw)
    report = {'standing': 'Exact strong-owner query capture only. No automatic response conformance, '
              'renderer parity, token portability, complete charter assent or implementation qualification. '
              'Exit zero means capture completed, not consumer acceptance.',
              'sourceManifestSha256': a.manifest_sha256, 'sourceFilesVerified': len(manifest['files']),
              'readerSha256': sha(Path(__file__).read_bytes()), 'transportSha256': a.transport_sha256,
              'ownerSha256': sha(model.read_bytes()), 'queryOwnerSha256': sha(query.read_bytes()),
              'exportSha256': sha(raw), 'vectorsSha256': sha(vraw), 'runId': a.run_id,
              'runLabel': a.run_label, 'selectedVectors': [r['vector'] for r in rows],
              'unselectedVectors': [r['vector'] for r in vectors['vectors'] if r['run'] != a.run_label],
              'transportAdmission': 'REFUSE', 'structuralAdmission': 'NOT-REACHED',
              'semanticAdmission': 'NOT-REACHED', 'cases': [], 'consumerAccepted': False}
    completed = False
    try:
        objects, blobs, notes = R.decode(raw, M)
        report.update(transportAdmission='ADMIT', transportNotes=notes)
        completed = execute_selected(M, Q, a.run_id, objects, blobs, rows, report)
    except Exception as exc:
        report.update(exceptionType=type(exc).__name__, reason=str(exc))
    report['captureCompleted'] = completed
    (a.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['captureCompleted', 'transportAdmission',
        'structuralAdmission', 'semanticAdmission', 'consumerAccepted']}))
    raise SystemExit(0 if completed else 1)


if __name__ == '__main__':
    main()
