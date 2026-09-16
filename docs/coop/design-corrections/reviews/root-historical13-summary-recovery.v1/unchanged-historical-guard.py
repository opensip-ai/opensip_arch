historical_manifest_path = root / (dc + 'reviews/candidate-subject.v13.json')
historical_manifest = load(historical_manifest_path)
assert sha(historical_manifest_path) == C.HISTORICAL_V13_MANIFEST_SHA256
historical_path = Path(historical_manifest['snapshotRoot']) / (dc + 'validation-summary.v1.json')
historical_row = next(r for r in historical_manifest['files'] if r['path'] == dc + 'validation-summary.v1.json')
assert sha(historical_path) == historical_row['sha256']
assert load(historical_path)['native']['matrixCells'] == C.HISTORICAL_V13_MATRIX_CELLS
