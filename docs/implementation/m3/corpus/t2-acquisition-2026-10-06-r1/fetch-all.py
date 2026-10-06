"""Explicit T2 acquisition outside all analysis/measurement runs."""
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time

product = pathlib.Path('/Users/sb/code/opensip-ai/opensip')
architecture = pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch')
evidence = pathlib.Path('/tmp/opensip-implementation/t2-acquisition')
cache = pathlib.Path('/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1')
cache.chmod(0o700)
sys.path.insert(0, str(product / 'tools/quality'))
from canonical import Refusal
from corpus import manifest_document
import fetch

# The owner fixes PATH without /usr/bin. Preserve the accepted command's
# complete flags/arguments and select the available system Git explicitly.
# This trusted acquisition adapter changes no repository or persisted config.
original_command = fetch.command
def absolute_git(*args):
    command = original_command(*args)
    assert command[0] == 'git'
    return ['/usr/bin/git', *command[1:]]
fetch.command = absolute_git
os.environ['PATH'] = '/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin'
os.environ['CARGO_HOME'] = '/Users/sb/.cargo'
manifest_path = architecture / 'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json'
raw = manifest_path.read_bytes()
manifest_digest = hashlib.sha256(raw).hexdigest()
assert manifest_digest == 'c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578'
manifest = manifest_document(raw)
assert len(manifest['repositories']) == 49
darwin = pathlib.Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR'], text=True).strip())
scratch = pathlib.Path(tempfile.mkdtemp(prefix='opensip-t2-fetch-', dir=darwin))
scratch.chmod(0o700)
store = cache / 'store'
report = {'standing': 'PINNED PUBLIC T2 ACQUISITION ONLY', 'manifest': {'path': str(manifest_path), 'bytes': len(raw), 'sha256': manifest_digest}, 'store': str(store), 'scratch': str(scratch), 'startedAt': datetime.datetime.now(datetime.UTC).isoformat(), 'nice': 10, 'gitExecutable': '/usr/bin/git', 'results': [], 'T1ProducerRan': False, 'repositoryCodeExecuted': False, 'heldOutInspected': False, 'providerLaunched': False, 'productQualification': False, 'HOMEChanged': False}
source_pins = []
for name in ['canonical.py', 'corpus.py', 'fetch.py', 'records.py', 'store.py']:
    source = product / 'tools/quality' / name
    data = source.read_bytes()
    source_pins.append({'path': 'tools/quality/' + name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
report['productSourcePins'] = source_pins
for entry in manifest['repositories']:
    started = time.monotonic()
    try:
        result = fetch.acquire(entry, manifest_digest, store, scratch)
        row = {'entry': entry['id'], 'status': 'VERIFIED', 'result': result}
    except (Refusal, OSError, KeyError, TypeError, ValueError) as error:
        code = str(error) if isinstance(error, Refusal) else type(error).__name__
        row = {'entry': entry['id'], 'status': 'REFUSED', 'refusal': code}
    row['elapsedSeconds'] = round(time.monotonic() - started, 3)
    report['results'].append(row)
    (evidence / 'acquisition.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'entry': row['entry'], 'status': row['status'], 'refusal': row.get('refusal')}), flush=True)
assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
report['completedAt'] = datetime.datetime.now(datetime.UTC).isoformat()
report['verifiedEntries'] = sum(row['status'] == 'VERIFIED' for row in report['results'])
report['refusedEntries'] = sum(row['status'] == 'REFUSED' for row in report['results'])
(evidence / 'acquisition.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'verified': report['verifiedEntries'], 'refused': report['refusedEntries']}), flush=True)
