"""Offline mechanical verification only; no source inspection or target execution."""
import datetime
import hashlib
import json
import pathlib
import stat
import sys

product = pathlib.Path('/Users/sb/code/opensip-ai/opensip')
architecture = pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch')
evidence = pathlib.Path('/tmp/opensip-implementation/t2-acquisition')
cache = pathlib.Path('/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1')
sys.path.insert(0, str(product / 'tools/quality'))
from corpus import manifest_document
from store import verify, workspace
from canonical import canonical
raw = (architecture / 'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes()
manifest_digest = hashlib.sha256(raw).hexdigest()
assert manifest_digest == 'c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578'
manifest = manifest_document(raw)
entries = {row['id']: row for row in manifest['repositories']}
assert len(entries) == 49
acquisition = json.loads((evidence / 'acquisition.json').read_text())
assert acquisition['verifiedEntries'] == 49 and acquisition['refusedEntries'] == 0
assert {r['entry'] for r in acquisition['results']} == entries.keys()
report = {'standing': 'OFFLINE T2 STORE AND DECLARED OVERLAY VERIFICATION ONLY', 'manifestSha256': manifest_digest, 'store': str(cache / 'store'), 'workspacesRoot': str(cache / 'workspaces'), 'startedAt': datetime.datetime.now(datetime.UTC).isoformat(), 'verifiedEntries': [], 'workspaces': [], 'repositoryCodeExecuted': False, 'heldOutInspected': False, 'providerLaunched': False, 'productQualification': False}
def save():
    (evidence / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
for entry in entries.values():
    key = entry['treeDigest']['value']
    result = verify(cache / 'store' / key, entry)
    receipt_path = cache / 'store' / (key + '.admission.json')
    receipt_raw = receipt_path.read_bytes()
    receipt = json.loads(receipt_raw)
    assert receipt_raw == canonical(receipt) + b'\n'
    assert stat.S_IMODE(receipt_path.stat().st_mode) == 0o444
    assert receipt['manifestSha256'] == manifest_digest
    for name in ('id', 'url', 'commit', 'gitTree', 'treeDigest', 'contentDigest', 'licence', 'family', 'heldOut'):
        assert receipt[name] == entry[name]
    report['verifiedEntries'].append({'entry': entry['id'], **result, 'receipt': {'path': str(receipt_path), 'bytes': len(receipt_raw), 'sha256': hashlib.sha256(receipt_raw).hexdigest()}})
    save()
    print(json.dumps({'verified': entry['id']}), flush=True)
for definition in manifest['workspaces']:
    result = workspace(cache / 'workspaces', cache / 'store', definition, entries)
    destination = cache / 'workspaces' / definition['id']
    files = []
    for name in ('workspace-overlay.json', '.cargo/config.toml'):
        path = destination / name
        if path.exists():
            data = path.read_bytes()
            assert stat.S_IMODE(path.stat().st_mode) == 0o444
            files.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    assert stat.S_IMODE(destination.stat().st_mode) == 0o555
    for member in definition['overlay']['members']:
        path = destination / member['mount']
        assert path.is_symlink() and path.resolve() == (cache / 'store' / member['treeDigest']).resolve()
    report['workspaces'].append({**result, 'files': files, 'memberCount': len(definition['memberIds'])})
    save()
    print(json.dumps(result), flush=True)
assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
report['completedAt'] = datetime.datetime.now(datetime.UTC).isoformat()
report['verifiedEntryCount'] = len(report['verifiedEntries'])
report['workspaceCount'] = len(report['workspaces'])
save()
print(json.dumps({'verified': report['verifiedEntryCount'], 'workspaces': report['workspaceCount']}), flush=True)
