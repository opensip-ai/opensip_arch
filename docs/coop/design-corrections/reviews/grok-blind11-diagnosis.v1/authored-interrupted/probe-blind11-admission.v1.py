"""Diagnostic probes for consumer-b.v11 export admission. Never acceptance.

Read-only on frozen24, consumer-b.v11, root parser/admission. Writes only under
this diagnosis directory. Disposable copies that add known kit schema bytes are
labeled DIAGNOSTIC, not admission, and do not remint Runs.
"""
from __future__ import annotations

import base64
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = '/tmp/opensip-architecture-review-env/bin/python'
PARSER = Path('/tmp/opensip-design-corrections/check-blind11-exported-graphs.v1.py')
FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v24')
CONSUMER = Path('/tmp/opensip-design-corrections/consumer-b.v11')
ROOT_ADMISSION = Path('/tmp/opensip-design-corrections/blind11-root-final-admission.v1')
SELFCHECK = Path('/tmp/opensip-design-corrections/blind11-root-parser-selfcheck.v1')
CLAIMS = ROOT_ADMISSION / 'claims.json'
TARGET = 'a87331bca7545468a266d74776d785a9903f93563220ac7f6267b6d749b82257'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
sha_b = lambda b: hashlib.sha256(b).hexdigest()


def load(p):
    return json.loads(Path(p).read_text())


def kit_docs():
    root = FROZEN / 'docs/coop/design-corrections'
    docs = {
        'native/native-evidence.schemas.v2.json': root / 'native/native-evidence.schemas.v2.json',
        'foundation/relation-payload-schemas.v2.json': root / 'foundation/relation-payload-schemas.v2.json',
        'foundation/identity-schemas.v3.json': root / 'foundation/identity-schemas.v3.json',
        'workflows/schemas/imported-evidence.schema.json': root / 'workflows/schemas/imported-evidence.schema.json',
    }
    return {sha(p): {'path': rel, 'bytes': p.read_bytes(), 'size': p.stat().st_size} for rel, p in docs.items()}


def store_stats(raw, known):
    store = json.loads(raw)
    blobs = store['blobs']
    cited = set()
    coverage_cites = []
    view_schema = []
    for oid, obj in store['objectTable'].items():
        desc = obj.get('descriptor') or {}
        if not isinstance(desc, dict):
            continue
        if 'payloadSchemaDigest' in desc:
            d = desc['payloadSchemaDigest']
            cited.add(d)
            if obj.get('domain') == 'coverage':
                coverage_cites.append({'id': oid, 'payloadSchemaDigest': d, 'inBlobs': d in blobs})
        for item in desc.get('schemaDigests') or []:
            cited.add(item)
            view_schema.append({'id': oid, 'digest': item, 'inBlobs': item in blobs})
    missing = sorted(cited - set(blobs))
    return {
        'blobCount': len(blobs),
        'objectCount': len(store['objectTable']),
        'runId': store.get('runId'),
        'citedPayloadOrViewSchemaDigests': sorted(cited),
        'citedMissingFromBlobs': missing,
        'targetInBlobs': TARGET in blobs,
        'targetCitedOnCoverage': any(c['payloadSchemaDigest'] == TARGET for c in coverage_cites),
        'coverageCitations': coverage_cites,
        'missingKnownKitDocs': [
            {'digest': d, 'kitPath': known[d]['path'], 'size': known[d]['size']}
            for d in missing
            if d in known
        ],
        'missingUnknown': [d for d in missing if d not in known],
    }


def run_parser(inp, claims, out):
    if out.exists():
        shutil.rmtree(out)
    r = subprocess.run(
        [PY, '-I', '-B', str(PARSER), '--input', str(inp), '--claims', str(claims), '--source', str(FROZEN), '--out', str(out)],
        capture_output=True,
        text=True,
    )
    report = load(out / 'report.json') if (out / 'report.json').is_file() else None
    return {'exitCode': r.returncode, 'report': report, 'stderr': r.stderr[-2000:]}


def inject_docs(src_store, dest_store, docs_by_digest, which):
    store = json.loads(src_store.read_text())
    added = []
    for digest in which:
        if digest in store['blobs']:
            continue
        rec = docs_by_digest[digest]
        raw = rec['bytes']
        assert sha_b(raw) == digest
        store['blobs'][digest] = base64.b64encode(raw).decode('ascii')
        added.append({'digest': digest, 'kitPath': rec['path'], 'size': rec['size']})
    store['blobCount'] = len(store['blobs'])
    dest_store.parent.mkdir(parents=True, exist_ok=True)
    dest_store.write_text(json.dumps(store, indent=2) + '\n')
    return added


def main():
    known = kit_docs()
    assert known[TARGET]['path'] == 'native/native-evidence.schemas.v2.json'
    claims = load(CLAIMS)
    rows = []
    exact_dir = HERE / 'exact-exports'
    for claim in claims:
        src = CONSUMER / 'output' / claim['path']
        dest = exact_dir / claim['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
        raw = dest.read_bytes()
        st = store_stats(raw, known)
        st.update(
            {
                'name': claim['name'],
                'path': claim['path'],
                'exportSha256': sha_b(raw),
                'claimedRunId': claim['runId'],
                'runIdFieldMatchesClaim': st.get('runId') in (None, claim['runId']) or st.get('runId') == claim['runId'],
            }
        )
        rows.append(st)

    original = run_parser(exact_dir, CLAIMS, HERE / 'parser-original-result')
    original_reasons = [
        {
            'name': c['name'],
            'ownerAdmission': c.get('ownerAdmission'),
            'semanticAdmission': c.get('semanticAdmission'),
            'reason': c.get('reason'),
            'exceptionType': c.get('exceptionType'),
            'passed': c.get('passed'),
        }
        for c in (original['report'] or {}).get('checks', [])
    ]

    # DIAGNOSTIC: add only the first-failure native coverage schema bytes
    diag1 = HERE / 'diagnostic-add-coverage-schema'
    if diag1.exists():
        shutil.rmtree(diag1)
    (diag1 / 'exports').mkdir(parents=True)
    added1 = {}
    for claim in claims:
        src = exact_dir / claim['path']
        dest = diag1 / 'exports' / Path(claim['path']).name
        added1[claim['name']] = inject_docs(src, dest, known, [TARGET])
    claims_rel = [{'name': c['name'], 'path': 'exports/' + Path(c['path']).name, 'runId': c['runId']} for c in claims]
    claims1 = diag1 / 'claims.json'
    claims1.write_text(json.dumps(claims_rel, indent=2) + '\n')
    after1 = run_parser(diag1, claims1, HERE / 'parser-diagnostic-coverage-schema-result')
    after1_reasons = [
        {
            'name': c['name'],
            'ownerAdmission': c.get('ownerAdmission'),
            'semanticAdmission': c.get('semanticAdmission'),
            'reason': c.get('reason'),
            'exceptionType': c.get('exceptionType'),
            'passed': c.get('passed'),
        }
        for c in (after1['report'] or {}).get('checks', [])
    ]

    # DIAGNOSTIC: add every cited missing kit schema document (still not a remint)
    missing_union = sorted({d for row in rows for d in row['citedMissingFromBlobs'] if d in known})
    diag2 = HERE / 'diagnostic-add-all-cited-kit-schemas'
    if diag2.exists():
        shutil.rmtree(diag2)
    (diag2 / 'exports').mkdir(parents=True)
    added2 = {}
    for claim in claims:
        src = exact_dir / claim['path']
        dest = diag2 / 'exports' / Path(claim['path']).name
        st = store_stats(src.read_bytes(), known)
        added2[claim['name']] = inject_docs(src, dest, known, [d for d in st['citedMissingFromBlobs'] if d in known])
    claims2 = diag2 / 'claims.json'
    claims2.write_text(json.dumps(claims_rel, indent=2) + '\n')
    after2 = run_parser(diag2, claims2, HERE / 'parser-diagnostic-all-cited-schemas-result')
    after2_reasons = [
        {
            'name': c['name'],
            'ownerAdmission': c.get('ownerAdmission'),
            'semanticAdmission': c.get('semanticAdmission'),
            'reason': c.get('reason'),
            'exceptionType': c.get('exceptionType'),
            'passed': c.get('passed'),
        }
        for c in (after2['report'] or {}).get('checks', [])
    ]

    selfcheck = load(SELFCHECK / 'assessment.json')
    pos = load(SELFCHECK / 'input' / 'positive.json')
    helper_eval = (CONSUMER / 'output' / 'helpers' / 'evaluator.py').read_text()
    helper_close = (CONSUMER / 'output' / 'helpers' / 'closure.py').read_text()
    recompute = (CONSUMER / 'output' / 'recompute.py').read_text()
    graph_cov = (CONSUMER / 'output' / 'helpers' / 'graph.py').read_text()

    report = {
        'standing': (
            'Diagnostic measurement of exact consumer-b.v11 exports through frozen identity-model.v3 '
            'open_run_closure/close_run. Schema-byte injections are DIAGNOSTIC copies only: not admission, '
            'not remint, not acceptance. Original refusals are preserved separately.'
        ),
        'actualApplicationPerformed': False,
        'acceptanceConferred': False,
        'frozenManifestSha256': 'a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb',
        'parserSha256': sha(PARSER),
        'identityModelSha256': sha(FROZEN / 'docs/coop/design-corrections/foundation/identity-model.v3.py'),
        'nativeEvidenceSchemaSha256': TARGET,
        'nativeEvidenceSchemaPath': 'native/native-evidence.schemas.v2.json',
        'kitDocs': {k: {'path': v['path'], 'size': v['size']} for k, v in known.items()},
        'exactExports': rows,
        'originalParser': {'exitCode': original['exitCode'], 'checks': original_reasons, 'passed': (original['report'] or {}).get('passed')},
        'selfcheck': {
            'passed': selfcheck.get('passed'),
            'positiveTargetInBlobs': TARGET in pos['blobs'],
            'cases': selfcheck.get('results'),
        },
        'diagnosticAddCoverageSchemaOnly': {
            'label': 'DIAGNOSTIC_NEVER_ACCEPTANCE',
            'added': added1,
            'exitCode': after1['exitCode'],
            'checks': after1_reasons,
            'passed': (after1['report'] or {}).get('passed'),
        },
        'diagnosticAddAllCitedKitSchemas': {
            'label': 'DIAGNOSTIC_NEVER_ACCEPTANCE',
            'missingUnionInjected': missing_union,
            'added': added2,
            'exitCode': after2['exitCode'],
            'checks': after2_reasons,
            'passed': (after2['report'] or {}).get('passed'),
        },
        'helperObservations': {
            'graphPutsNativeSchemaDigestOnCoverage': 'NATIVE_SCHEMA_SHA' in graph_cov and 'payloadSchemaDigest' in graph_cov,
            'storeExportDoesNotAutoRetainKitSchemaFiles': 'put_blob' in (CONSUMER / 'output' / 'helpers' / 'store.py').read_text()
            and 'NATIVE_SCHEMA' not in (CONSUMER / 'output' / 'helpers' / 'store.py').read_text(),
            'evaluatorNativeMatchFileAndClonesOnly': (
                'elif rel == "clones"' in helper_eval and 'rel == "file"' in helper_eval and 'unresolved-edge' not in helper_eval
            ),
            'evaluatorFileRungExactOnly': 'rel == "file"' in helper_eval and 'resolution' in helper_eval,
            'helperCloseRunNotIdentityModel': 'open_run_closure' not in helper_close and 'EvidenceUnavailable' not in helper_close,
            'recomputeComparesSavedReplayVerdicts': "replay['claimedVerdict']" in recompute and "replay['recomputedVerdict']" in recompute,
        },
    }
    (HERE / 'probes.json').write_text(json.dumps(report, indent=2) + '\n')
    print(
        json.dumps(
            {
                'originalPassed': report['originalParser']['passed'],
                'originalReasons': [c['reason'] for c in original_reasons],
                'diag1Passed': report['diagnosticAddCoverageSchemaOnly']['passed'],
                'diag1Reasons': [c.get('reason') for c in after1_reasons],
                'diag2Passed': report['diagnosticAddAllCitedKitSchemas']['passed'],
                'diag2Reasons': [c.get('reason') for c in after2_reasons],
                'missingUnion': missing_union,
            },
            indent=2,
        )
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
