"""F8b step 1: add license = Apache-2.0 to the three tooling manifests (proposal r2 rows 1-3).

Refuses unless each manifest holds its base bytes. Placement: the Cargo manifest has no
publish key, so the line follows edition = "2024", which ends [package]; each package.json
gets "license" after "private": true, with its two-space indent (L1's rule)."""
import hashlib, json, sys
from pathlib import Path
W = Path(sys.argv[1]).resolve(strict=True)
def pin(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
EDITS = [
    ('tools/contracts/Cargo.toml', '6b769285e95d2aa94a420fa63d74d6a199bbe84c9ceadef75550112fb3d88a7f',
     b'edition = "2024"\n', b'edition = "2024"\nlicense = "Apache-2.0"\n', '8c2323b688e075e6dd2f98b5c52428959846e2d8c635d97739a2f345e5d6193a'),
    ('tools/contracts/package.json', '1c71c0980aa483c08d4adf10c90706346287e86f8c940a63002e3fb1317cacc4',
     b'  "private": true,\n', b'  "private": true,\n  "license": "Apache-2.0",\n', '678aa95d9a72a96d0740db1aa6ba8be35d6e5cc5b8b75641fb861513b6b04df5'),
    ('tools/typescript-boundary/package.json', '98ae9218de30d736c7dcd28cab71c882e4ab9cf78aded2c7b6bf126864fe9806',
     b'  "private": true,\n', b'  "private": true,\n  "license": "Apache-2.0",\n', '2d15756d013eeff1473df9dadb5a65a8d5f88a38f07993264fcececeae1bbc05'),
]
report = {}
for path, before_sha, old, new, after_sha in EDITS:
    raw = (W / path).read_bytes()
    assert pin(raw)['sha256'] == before_sha and raw.count(old) == 1 and b'license' not in raw, path
    out = raw.replace(old, new)
    if path.endswith('.json'): json.loads(out)
    assert pin(out)['sha256'] == after_sha, path
    (W / path).write_bytes(out)
    report[path] = {'before': pin(raw), 'after': pin(out)}
print(json.dumps(report, indent=2))
