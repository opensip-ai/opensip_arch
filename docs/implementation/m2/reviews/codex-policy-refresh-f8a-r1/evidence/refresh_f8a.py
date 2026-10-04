"""F8a: refresh the stale localSources rows of the two dependency policies.

Run from the product worktree root. Refuses unless every replaced row still holds
its base (30c5db1) value and every added path is unpinned. After the edit, each
policy's localSources equals the observed census exactly (sorted, unique, the
current bytes and sha256). Only localSources changes; json.dumps(indent=2) + '\n'
reproduces both files byte for byte at base, so no other byte moves.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve(strict=True)

EDITS = {
    'tools/contracts/dependency-policy.json': ('crates/contracts', {
        'src/generated/evidence.rs': (1569029, '8b269f8b993966eb45ec08886c6288728a73d6ec4d7d3ad917a5d6b8cf2f3bb7'),
    }, []),
    'tools/identity/dependency-policy.json': ('crates/identity', {
        'src/lib.rs': (1739, 'f08e459fe69e4537c47b8440ee448353d27a5b55fbc648324de2943bc83be562'),
        'src/schema_registry.rs': (26808, 'bc6b914324e1175cffdcd793c8fc67f1b5d691cdd0d06ecfc46a728c4939c511'),
    }, ['src/project_registry.rs', 'src/project_registry_tests.rs', 'src/store_identity.rs',
        'src/store_lineage.rs', 'src/store_marker.rs', 'src/store_selection.rs']),
}


def pin(path):
    raw = path.read_bytes()
    return len(raw), hashlib.sha256(raw).hexdigest()


def census(crate):
    files = {'Cargo.toml'}
    for path in (crate / 'src').rglob('*'):
        assert not path.is_symlink(), path
        if path.is_file():
            files.add(path.relative_to(crate).as_posix())
    return files


report = {}
for policy_path, (crate_path, replaced, added) in EDITS.items():
    file = ROOT / policy_path
    raw = file.read_bytes()
    policy = json.loads(raw)
    assert (json.dumps(policy, indent=2) + '\n').encode() == raw, 'policy does not round-trip'
    crate = ROOT / crate_path
    rows = {row['path']: row for row in policy['localSources']}
    changes = []
    for name, (old_bytes, old_sha) in replaced.items():
        row = rows[name]
        assert row['bytes'] == old_bytes and row['sha256'] == old_sha, name
        size, digest = pin(crate / name)
        changes.append({'path': name, 'before': {'bytes': row['bytes'], 'sha256': row['sha256']},
                        'after': {'bytes': size, 'sha256': digest}})
        row['bytes'], row['sha256'] = size, digest
    for name in added:
        assert name not in rows, name
        size, digest = pin(crate / name)
        rows[name] = {'path': name, 'bytes': size, 'sha256': digest}
        changes.append({'path': name, 'before': None, 'after': {'bytes': size, 'sha256': digest}})
    policy['localSources'] = [rows[name] for name in sorted(rows)]
    observed = census(crate)
    assert set(rows) == observed, sorted(set(rows) ^ observed)
    for row in policy['localSources']:
        assert (row['bytes'], row['sha256']) == pin(crate / row['path']), row['path']
    out = (json.dumps(policy, indent=2) + '\n').encode()
    file.write_bytes(out)
    report[policy_path] = {'before': {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()},
                           'after': {'bytes': len(out), 'sha256': hashlib.sha256(out).hexdigest()},
                           'localSources': len(policy['localSources']), 'changes': changes}
print(json.dumps(report, indent=2))
