"""Shared loader for review probes. Loads frozen subject/owner source by exec of
bytes (no import machinery, no bytecode); run with the reference Python -I -B."""
import hashlib
import json
import types
from pathlib import Path

ROOT = Path('/tmp/opensip-implementation')
ARCH = Path('/Users/sb/code/opensip-ai/opensip_arch')
DC = ARCH / 'docs/coop/design-corrections'


def load(path, name):
    path = Path(path)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


def jload(path):
    return json.loads(Path(path).read_bytes())


class Recorder:
    def __init__(self, subject):
        self.subject = subject
        self.rows = []

    def record(self, pid, kind, expectation, observed, holds, note=''):
        # kind: control-valid | control-invalid | finding | derivation
        self.rows.append({'id': pid, 'kind': kind, 'expectation': expectation,
                          'observed': observed, 'expectationHolds': bool(holds), 'note': note})

    def outcome(self, fn):
        try:
            return {'returned': fn()}
        except Exception as exc:  # probes record the exact class/message
            return {'raised': type(exc).__name__, 'message': str(exc)[:300]}

    def dump(self, path):
        data = {'subject': self.subject, 'probes': self.rows,
                'controlsHold': all(r['expectationHolds'] for r in self.rows if r['kind'].startswith('control')),
                'findingsReproduced': [r['id'] for r in self.rows if r['kind'] == 'finding' and r['expectationHolds']]}
        Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str) + '\n')
        print(json.dumps({k: data[k] for k in ('subject', 'controlsHold', 'findingsReproduced')}, indent=1))
        return data
