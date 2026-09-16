"""Resumed delta review02: single-edit mutants of the candidate02 tool on throwaway copies.

Each mutant runs the permanent unit tests, the permanent adopted regressions, and the
review02 delta probes. Scratch fixtures (including the deep 16-segment tree) are removed
only with descriptor-relative operations, never by long absolute paths.
Usage: python -I -B -X pycache_prefix=<empty> mutate_delta.py
"""
import json
import os
import re
import shutil
import stat
import subprocess

R = '/tmp/opensip-implementation/m1-report-asset-assembly-review-02'
PY = '/tmp/opensip-implementation/metadata-reference-env/bin/python'
PRISTINE = R + '/copy'
WORK = R + '/w'
SCRATCH = R + '/s/m'
PYC = R + '/pycache-empty'
TOOL = 'tools/report_asset_manifest.py'
IDENTITY = '(actual.st_dev, actual.st_ino) == (entry.st_dev, entry.st_ino), "ASSET_CHANGED")\n'

PRIOR = {
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
DELTA = {
    'N01-no-typed-filesystem-wrapper': [('    except OSError as error:\n        raise AssemblyRefusal("ASSET_FILESYSTEM") from error\n',
                                         '    except AssemblyRefusal:\n        raise\n')],
    'N02-wrapper-masks-all-exceptions': [('    except OSError as error:', '    except Exception as error:')],
    'N03-wrapper-leaks-os-text': [('raise AssemblyRefusal("ASSET_FILESYSTEM") from error', 'raise AssemblyRefusal(str(error)) from error')],
    'N04-no-aggregate-precheck': [('                need(count_bytes + actual.st_size <= BUNDLE_LIMIT, "ASSET_BUNDLE_LIMIT")\n', '')],
    'N05-aggregate-precheck-ignores-member-size': [('count_bytes + actual.st_size <= BUNDLE_LIMIT', 'count_bytes <= BUNDLE_LIMIT')],
    'N06-aggregate-precheck-strict': [('count_bytes + actual.st_size <= BUNDLE_LIMIT', 'count_bytes + actual.st_size < BUNDLE_LIMIT')],
    'N07-no-windows-reserved-check': [(' and p.split(".", 1)[0] not in WINDOWS_RESERVED', '')],
    'N08-windows-reserved-whole-name-only': [('p.split(".", 1)[0] not in WINDOWS_RESERVED', 'p not in WINDOWS_RESERVED')],
    'N09-windows-reserved-last-extension-only': [('p.split(".", 1)[0] not in WINDOWS_RESERVED', 'p.rsplit(".", 1)[0] not in WINDOWS_RESERVED')],
    'N10-windows-reserved-com9-missing': [('("com" + str(i) for i in range(1, 10))', '("com" + str(i) for i in range(1, 9))')],
    'N11-windows-reserved-aux-missing': [('"con", "prn", "aux", "nul"', '"con", "prn", "nul"')],
    'N12-final-count-not-compared': [('need(count == before.st_size == after.st_size', 'need(before.st_size == after.st_size')],
}
MUTANTS = {**PRIOR, **DELTA}


def remove_tree(path):
    """Descriptor-relative recursive removal; no long absolute path is constructed or traversed."""
    parent, name = os.path.split(path)
    try:
        parent_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    except FileNotFoundError:
        return
    try:
        _remove(parent_fd, name)
    finally:
        os.close(parent_fd)


def _remove(dir_fd, name):
    try:
        info = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    if stat.S_ISDIR(info.st_mode):
        fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=dir_fd)
        try:
            for child in os.listdir(fd):
                _remove(fd, child)
        finally:
            os.close(fd)
        os.rmdir(name, dir_fd=dir_fd)
    else:
        os.unlink(name, dir_fd=dir_fd)


def prepare(edits):
    remove_tree(WORK)
    remove_tree(SCRATCH)
    os.makedirs(WORK)
    os.makedirs(SCRATCH + '/t')
    for part in ('tools', 'tests', 'inputs'):
        shutil.copytree(os.path.join(PRISTINE, part), os.path.join(WORK, part), copy_function=shutil.copy)
    path = os.path.join(WORK, TOOL)
    text = open(path).read()
    for old, new in edits:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    open(path, 'w').write(text)


def suite(name, cmd):
    env = dict(os.environ, TMPDIR=SCRATCH + '/t')
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)
    except subprocess.TimeoutExpired:
        return {'status': 'timeout', 'failed': []}
    if name == 'unit':
        failed = sorted(set(re.findall(r'^(?:FAIL|ERROR): (\w+)', p.stderr, re.M)))
    else:
        result = SCRATCH + '/' + name + '.json'
        try:
            probes = json.load(open(result))['probes']
            failed = sorted(k for k, v in probes.items() if v['result'] != 'PASS')
        except (OSError, ValueError):
            failed = ['<no results> ' + p.stderr[-300:]]
    return {'status': 'pass' if p.returncode == 0 else 'fail', 'failed': failed}


def run():
    base = [PY, '-I', '-B', '-X', 'pycache_prefix=' + PYC]
    return {
        'unit': suite('unit', base + [WORK + '/tests/test_report_asset_manifest.py']),
        'regressions': suite('regressions', base + [WORK + '/tests/review_regressions.py', WORK + '/' + TOOL,
                                                    WORK + '/inputs/report-asset-binding.v1.json', SCRATCH + '/i',
                                                    SCRATCH + '/regressions.json']),
        'delta': suite('delta', base + [R + '/probe-src/delta_probes.py', WORK + '/' + TOOL, SCRATCH + '/delta.json']),
    }


results = {}
for name in ['CONTROL'] + list(MUTANTS):
    prepare(MUTANTS.get(name, []))
    suites = run()
    permanent_killed = any(suites[s]['status'] != 'pass' for s in ('unit', 'regressions'))
    any_killed = permanent_killed or suites['delta']['status'] != 'pass'
    if name == 'CONTROL':
        verdict = 'control-pass' if not any_killed else 'CONTROL-FAILED'
    else:
        verdict = ('killed-by-permanent' if permanent_killed else
                   'killed-by-review-probe-only' if any_killed else 'survived')
    results[name] = {'verdict': verdict, **suites}
    print(f"{name:44s} {verdict:28s} unit={suites['unit']['failed']} reg={suites['regressions']['failed']} delta={suites['delta']['failed']}", flush=True)
    if name == 'CONTROL' and any_killed:
        break
remove_tree(WORK)
remove_tree(SCRATCH)
json.dump(results, open(R + '/mutation-delta.json', 'w'), indent=2)
