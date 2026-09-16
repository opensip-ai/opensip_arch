"""Fetch one official, version-pinned compiler for bounded design probes; no install."""
from pathlib import Path
import base64
import hashlib
import io
import json
import tarfile
import urllib.request

out = Path(__file__).parent
url = 'https://registry.npmjs.org/typescript/5.6.3'
metadata_bytes = urllib.request.urlopen(url, timeout=30).read()
metadata = json.loads(metadata_bytes)
assert metadata['name'] == 'typescript' and metadata['version'] == '5.6.3'
archive = urllib.request.urlopen(metadata['dist']['tarball'], timeout=30).read()
algorithm, digest = metadata['dist']['integrity'].split('-', 1)
assert algorithm == 'sha512'
assert base64.b64encode(hashlib.sha512(archive).digest()).decode() == digest
(out / 'npm-metadata.json').write_bytes(metadata_bytes)
kept = []
with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
    for name in ['package/lib/typescript.js', 'package/package.json', 'package/LICENSE.txt']:
        body = tar.extractfile(name).read()
        target = out / 'compiler' / name.removeprefix('package/')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        kept.append(dict(path=str(target.relative_to(out)), bytes=len(body), sha256=hashlib.sha256(body).hexdigest()))
(out / 'compiler-custody.json').write_text(json.dumps(dict(
    standing='Official TypeScript5.6.3 bounded compiler probe input, not a selected OpenSIP product pin or product qualification. No installation or package scripts executed.',
    metadataUrl=url, tarballUrl=metadata['dist']['tarball'], integrity=metadata['dist']['integrity'], integrityVerified=True,
    archiveSha256=hashlib.sha256(archive).hexdigest(), files=kept,
), indent=2) + '\n')
print('Verified TypeScript5.6.3 package integrity; retained compiler, package metadata and MIT license only')
