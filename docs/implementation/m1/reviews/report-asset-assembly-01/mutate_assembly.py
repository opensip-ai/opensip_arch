"""Resumed independent review: single-edit mutants of the assembly tool on throwaway copies.

Usage: python -I -B -X pycache_prefix=<empty> mutate_assembly.py tests|probes
"""
import json
import os
import re
import shutil
import subprocess
import sys

R = '/tmp/opensip-implementation/m1-report-asset-assembly-review-01'
PY = '/tmp/opensip-implementation/metadata-reference-env/bin/python'
PRISTINE = R + '/work/assembly'
MODE = sys.argv[1]
# Short work path: AF_UNIX socket paths (used by subject tests and probes) are limited to 103 bytes on macOS.
WORK = R + '/w' + MODE[0]
PYC = R + '/pycache-empty'
TOOL = 'tools/report_asset_manifest.py'
IDENTITY = '(actual.st_dev, actual.st_ino) == (entry.st_dev, entry.st_ino), "ASSET_CHANGED")\n'

MUTANTS = {
    'T01-trailing-dot-admitted': [(' and p[-1] not in ". "', '')],
    'T02-no-member-size-precheck': [('    need(before.st_size <= limit, "ASSET_MEMBER_LIMIT")\n', '')],
    'T03-no-running-bundle-check': [('                need(count_bytes <= BUNDLE_LIMIT, "ASSET_BUNDLE_LIMIT")\n', '')],
    'T04-no-file-lstat-open-identity': [('need(stat.S_ISREG(actual.st_mode), "ASSET_NONREGULAR")\n                need(' + IDENTITY,
                                         'need(stat.S_ISREG(actual.st_mode), "ASSET_NONREGULAR")\n')],
    'T05-no-directory-lstat-open-identity': [('                    actual = os.fstat(child_fd)\n                    need(' + IDENTITY,
                                              '                    actual = os.fstat(child_fd)\n')],
    'T06-no-post-open-regular-check': [('                need(stat.S_ISREG(actual.st_mode), "ASSET_NONREGULAR")\n', '')],
    'T07-no-O_NOFOLLOW': [('os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK', 'os.O_CLOEXEC | os.O_NONBLOCK')],
    'T08-no-O_NONBLOCK': [('os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK', 'os.O_CLOEXEC | os.O_NOFOLLOW')],
    'T09-no-lstat-kind-check': [('            need(stat.S_ISREG(entry.st_mode) or stat.S_ISDIR(entry.st_mode), "ASSET_NONREGULAR")\n', '')],
    'T10-no-directory-change-check': [('        need((before.st_mtime_ns, before.st_ctime_ns) == (after.st_mtime_ns, after.st_ctime_ns), "ASSET_DIRECTORY_CHANGED")\n', '')],
    'T11-no-file-mtime-ctime-check': [('\n         and before.st_mtime_ns == after.st_mtime_ns\n         and before.st_ctime_ns == after.st_ctime_ns, "ASSET_CHANGED")', ', "ASSET_CHANGED")')],
    'T12-no-file-size-equality': [('need(count == before.st_size == after.st_size', 'need(True')],
    'T13-no-directory-count-limit': [('        need(visited_directories <= FILE_LIMIT, "ASSET_DIRECTORY_LIMIT")\n', '')],
    'T14-no-listing-count-limit': [('        need(len(names) <= FILE_LIMIT + 1, "ASSET_DIRECTORY_LIMIT")\n', '')],
    'T15-no-projection-count-limit': [('0 < len(projection_digests) <= PROJECTION_LIMIT', '0 < len(projection_digests)')],
    'T16-no-build-channel-check': [('    need(build_channel in ("development", "release"), "ASSET_BUILD_CHANNEL")\n', '')],
    'T17-no-root-directory-check': [('    need(stat.S_ISDIR(os.fstat(directory_fd).st_mode), "ASSET_ROOT_NOT_DIRECTORY")\n', '')],
    'T18-no-byte-order-row-sort': [('    rows.sort(key=lambda row: row["path"].encode("ascii"))\n', '')],
    'T19-empty-roles-admitted': [('0 < len(roles) <= FILE_LIMIT', 'len(roles) <= FILE_LIMIT')],
    'T20-no-role-count-limit': [('0 < len(roles) <= FILE_LIMIT', '0 < len(roles)')],
    'T21-manifest-exclusion-by-prefix': [('if release_path == manifest_path:', 'if release_path.startswith(manifest_path):')],
    'T22-manifest-directory-admitted': [('need(release_path != manifest_path, "ASSET_MANIFEST_NONREGULAR")', 'None')],
    'T23-no-undeclared-file-check': [('                need(release_path in roles, "ASSET_UNDECLARED_FILE")\n', '')],
    'T24-no-visit-depth-check': [('        need(depth <= DEPTH_LIMIT, "ASSET_DEPTH")\n', '')],
    'T25-no-path-length-limit': [('0 < len(path) <= PATH_LIMIT', '0 < len(path)')],
    'T26-no-segment-count-limit': [('    need(len(parts) <= DEPTH_LIMIT, "ASSET_DEPTH")\n', '')],
    'T27-no-manifest-size-limit': [('need(0 < len(manifest) <= MANIFEST_LIMIT, "ASSET_MANIFEST_LIMIT")', 'None')],
    'T28-no-missing-file-check': [('need([row["path"] for row in rows] == sorted(roles), "ASSET_MISSING_FILE")', 'None')],
    'T29-uppercase-digest-admitted': [('r"[0-9a-f]{64}"', 'r"[0-9a-fA-F]{64}"')],
    'T30-role-path-not-under-root': [('path.startswith(asset_root + "/") and path != manifest_path', 'path != manifest_path')],
    'T31-interrupted-read-not-retried': [('        except InterruptedError:\n            continue\n', '        except InterruptedError:\n            raise\n')],
    'T32-no-final-bundle-with-manifest': [('    need(count_bytes + len(manifest) <= BUNDLE_LIMIT, "ASSET_BUNDLE_LIMIT")\n', '')],
    'T33-nested-manifest-admitted': [('    need("/" not in relative_manifest, "ASSET_MANIFEST_LOCATION")\n', '')],
    'T34-no-manifest-root-check': [('need(manifest_path.startswith(asset_root + "/"), "ASSET_MANIFEST_ROOT")', 'None')],
    'T35-prior-manifest-not-excluded': [('                    continue\n', '                    pass\n')],
    'T36-uppercase-names-admitted': [('r"[a-z0-9][a-z0-9._-]*"', 'r"[a-zA-Z0-9][a-zA-Z0-9._-]*"')],
}


def prepare(edits):
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK + '/t')
    for part in ('tools', 'tests', 'inputs'):
        shutil.copytree(os.path.join(PRISTINE, part), os.path.join(WORK, part), copy_function=shutil.copy)
    path = os.path.join(WORK, TOOL)
    text = open(path).read()
    for old, new in edits:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    open(path, 'w').write(text)


def run():
    env = dict(os.environ, TMPDIR=WORK + '/t')
    base = [PY, '-I', '-B', '-X', 'pycache_prefix=' + PYC]
    if MODE == 'tests':
        cmd = base + [WORK + '/tests/test_report_asset_manifest.py']
    else:
        cmd = base + [R + '/probe-src/assembly_probes.py', WORK + '/' + TOOL,
                      WORK + '/inputs/report-asset-binding.v1.json', WORK + '/interop', WORK + '/probe-results.json']
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)
    except subprocess.TimeoutExpired:
        return 'timeout', []
    if MODE == 'tests':
        failed = sorted(set(re.findall(r'^(?:FAIL|ERROR): (\w+)', p.stderr, re.M)))
    else:
        try:
            probes = json.load(open(WORK + '/probe-results.json'))['probes']
            failed = sorted(k for k, v in probes.items() if v['result'] != 'PASS')
        except (OSError, ValueError):
            failed = ['<no results>: ' + p.stderr[-400:]]
    return ('pass' if p.returncode == 0 else 'fail'), failed


results = {}
for name in ['CONTROL'] + list(MUTANTS):
    prepare(MUTANTS.get(name, []))
    status, failed = run()
    verdict = {'pass': 'survived', 'fail': 'killed', 'timeout': 'killed-timeout'}[status]
    if name == 'CONTROL':
        verdict = 'control-pass' if status == 'pass' else 'CONTROL-FAILED'
    results[name] = {'verdict': verdict, 'failed': failed}
    print(f'{name:40s} {verdict:14s} {failed}', flush=True)
    if name == 'CONTROL' and status != 'pass':
        break
shutil.rmtree(WORK, ignore_errors=True)
json.dump(results, open(f'{R}/mutation-assembly-{MODE}.json', 'w'), indent=2)
