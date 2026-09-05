"""Checks authored quality matrix and opaque-object preservation design cases.
Does not execute an OpenSIP product or qualify a platform.
"""
import hashlib
import json
from pathlib import Path
import tempfile
import argparse

BASE = Path(__file__).resolve().parent
SHA = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    matrix = json.loads((BASE / 'language-quality-matrix.completed.v1.json').read_text())
    corpus = json.loads((BASE / 'quality-corpus-manifest.v1.json').read_text())
    wanted = {c + '@' + p for c in matrix['capabilityRegistry'] + ['host.integration'] for p in matrix['platforms']}
    got = [r['id'] for r in matrix['rows']]
    assert len(got) == len(set(got)) == matrix['requiredCells'] == 24
    assert set(got) == wanted
    for name, expected in matrix['sourcePins'].items():
        assert SHA(BASE / name) == expected, name
    for row in matrix['rows']:
        assert row['corpusManifestSha256'] == SHA(BASE / 'quality-corpus-manifest.v1.json')
        assert set(row['projects']) <= set(corpus['projects']) and row['projects']
        assert row['baselinePath'] == 'approved-language-native-corpus'
        assert row['performanceBaseline'] is None and row['performanceBaselineRunner'] is None
        assert row['platformQualified'] is False and row['knownLimitations']
        assert row['precision'] == row['recall'] == row['negativePassFraction'] == 1
    for entry in corpus['files']:
        assert SHA(BASE.parents[2] / entry['path']) == entry['sha256']
    native = json.loads((BASE / 'native-corpus-report.v1.json').read_text())
    assert native['count'] == native['passed'] == 16
    assert {(r['mode'], r['project']) for r in native['results']} == {
        (m, p) for m in ['native', 'prototype-program-service'] for p in corpus['projects']}
    cases = json.loads((BASE / 'sarif-preservation-cases.v1.json').read_text())
    observations = []
    for case in cases['cases']:
        with tempfile.TemporaryDirectory(prefix='opensip-output-design-') as tmp:
            root = Path(tmp)
            prior = root / case['preexistingPath'] if case['preexistingPath'] else None
            if prior:
                payload = (BASE / case['sourceFile']).read_bytes()
                assert SHA(BASE / case['sourceFile']) == case['sourceSha256']
                prior.parent.mkdir(parents=True)
                prior.write_bytes(payload)
                before = SHA(prior)
            candidate = root / 'candidate-result'
            # Serialize before publish. A real JSON type error interrupts the adapter.
            serialized = False
            try:
                output = json.dumps({'unsupported': object()}).encode()
                serialized = True
                staging = root / 'output-staging'
                staging.write_bytes(output)
                staging.rename(candidate)
            except TypeError:
                pass
            actual = {'preserved': SHA(prior) == before if prior else None,
                      'candidateCommitted': candidate.exists(), 'serializedOutputSucceeded': serialized}
            assert actual == case['expected'], (case['id'], actual)
            observations.append({'id': case['id'], 'actual': actual, 'passed': True})
    report = {'kind': 'quality-and-preservation-design-check', 'productQualification': False,
              'matrixCells': len(got), 'nativeComparisons': native['passed'], 'preservationCases': observations,
              'pins': {p.name: SHA(p) for p in [Path(__file__), BASE / 'language-quality-matrix.completed.v1.json',
                      BASE / 'sarif-preservation-cases.v1.json', BASE / 'sarif-preserved-object.v1.bin']},
              'limitations': ['Matrix coverage is authored, not measured on four platforms.',
                  'Opaque object is never decoded and is not asserted to be a valid sealed Run.',
                  'Serialization failure exercises a reference adapter only.']}
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, default=BASE / 'quality-design-report.v1.json')
    args = parser.parse_args()
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matrixCells': len(got), 'nativeComparisons': native['passed'], 'preservationCases': len(observations), 'passed': True}))

if __name__ == '__main__':
    run()
