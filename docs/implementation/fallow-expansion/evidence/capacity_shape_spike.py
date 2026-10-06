"""Measure synthetic request JSON sizes; never product qualification or schema admission."""
import hashlib
import json
from pathlib import Path

ARCH = Path(__file__).resolve().parents[4]
MATRIX = ARCH / 'docs/coop/design-corrections/native/native-capability-matrix.v2.json'
CANON = ARCH / 'docs/coop/design-corrections/foundation/canonical.py'


def pin(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(ARCH)), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def measure():
    matrix = json.loads(MATRIX.read_text())
    capabilities = sorted(cell['capability'] for cell in matrix['cells']
                          if cell['mode'] == 'ts-tsconfig' and cell['state'] != 'NOT-SELECTED')
    cases = []
    for count in (93, 94, 256, 1024):
        for root_length in (32, 256, 4096):
            rows = []
            for ordinal in range(count):
                prefix = f'packages/unit-{ordinal:04d}/'
                root = prefix + 'x' * (root_length - len(prefix))
                rows.extend({'capabilityId': cap, 'languageMode': 'ts-tsconfig',
                             'workspaceRoot': root, 'required': True}
                            for cap in capabilities)
            # Object is a prospective field projection, not a complete admitted analysis-spec.
            raw = json.dumps({'requestedCapabilities': rows}, ensure_ascii=False,
                             sort_keys=True, separators=(',', ':')).encode('utf-8')
            cases.append({'units': count, 'rootAsciiBytes': root_length,
                          'capabilityRows': len(rows), 'projectionJsonBytes': len(raw),
                          'exceedsInheritedRowBound1024': len(rows) > 1024,
                          'exceedsInheritedCanonicalByteBound4194304': len(raw) > 4194304})
    return {'kind': 'synthetic-request-size-observation',
            'claim': 'serialization size only; no product run, performance or admission result',
            'matrix': pin(MATRIX), 'canonicalReference': pin(CANON),
            'method': 'ASCII roots, ts-tsconfig selected matrix, canonical JSON settings; field projection only',
            'capabilities': capabilities, 'cases': cases,
            'limitations': ['No aggregate Plan, source, dependencies, frames, facts or replay cost measured',
                            'Current native/identity schema and vocabulary still govern actual admission',
                            '4 MiB is the inspected canonical reference bound, not every protocol frame bound',
                            'Additional selected capabilities increase row and byte counts']}


if __name__ == '__main__':
    print(json.dumps(measure(), indent=2))
