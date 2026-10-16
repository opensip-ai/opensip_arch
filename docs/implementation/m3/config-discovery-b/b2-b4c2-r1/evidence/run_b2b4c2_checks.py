"""B2-b4c2 candidate checks (the blind run's receipt and the regenerated census record; B2-b4 plan r6 section 2.5). No check opens
a held-out store; the blind run itself is run_b2b4c2_blind.py, once. Rows: the security suite (base and candidate, equal failure sets),
the census tests (the margin test over the composed record), the census --check (ordinary mode: lead-readable stores plus the receipt),
the census-tool controls, the vector checks, the configuration tables, the operability census, verify_design, and three receipt
controls, each of which must make the ordinary --check refuse or differ: a tampered margin, the tool drifted by one comment byte (the
receipt goes stale), and the receipt removed. No Rust source changes, so rustfmt and Clippy are not rerun. One lane hold, nice 10,
private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re, sys, copy
W = Path('/Users/sb/code/opensip-ai/opensip-b2b4c2'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path(sys.argv[1]); B.mkdir(parents=True)
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'; PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
TOOL = 'tools/security/discovery_census.py'; CENSUS = 'crates/security/src/custody/discovery_census.json'
BLIND_TESTS = [PY, '-I', '-B', 'tools/tests/test_discovery_census_blind.py']
T_MARGIN = ['test', '-p', 'opensip-security', '--lib', '--', 'discovery_census_tests::the_census_margin_is_classified']
GUARD_MUTATIONS = [
    ('exception-text-kept', "    except (Exception, SystemExit):  # noqa: BLE001 (reduced to its class; r2, Codex B2B4C1-R1-RF-2: an exit too)\n        return error('INTEGRITY')",
     "    except Exception as x:  # noqa: BLE001\n        return dict(error('INTEGRITY'), errorClass=str(x))"),
    ('generic-message-dropped', "        print('Discovery census blind run failed.', file=sys.stderr)",
     "        print('Discovery census blind run failed: %s' % (sys.exc_info()[1],), file=sys.stderr)"),
    # r2 (Codex B2B4C1-R1-RF-2 and RF-3)
    ('abbreviation-allowed', "allow_abbrev=False)", "allow_abbrev=True)"),
    ('exit-not-reduced', "    except (Exception, SystemExit):  # noqa: BLE001\n        return error('MODEL')\n    if m.observed", "    except Exception:  # noqa: BLE001\n        return error('MODEL')\n    if m.observed"),
    ('boundary-narrowed', "    except BaseException:  # noqa: BLE001\n        # Every failure of a blind run", "    except Exception:  # noqa: BLE001\n        # Every failure of a blind run"),
    ('reference-unbound', ",\n                reference=[pin_row(product, p) for p in REFERENCE_PRODUCT] + [pin_row(arch, p) for p in REFERENCE_ARCH])", ")"),
    ('blind-join-unguarded', "    require(token is _BLIND, 'the held-out join is for the blind mode only')\n", ""),
    ('stale-binding-ignored', "    if receipt['bindings'] != current:", "    if False:"),
    ('coverage-unchecked', "    require(len(got) == len(set(got)) and sorted(got) == sorted(ids), 'receipt coverage differs from the held-out entries')\n", ""),
    ('passes2x-unchecked', "            require(r['passes2x'] is all(v >= 2000 for v in mp.values()), 'passes2x disagrees with the margins: ' + r['id'])\n", ""),
    ('ordinary-opens-held-out', "            entries.append(held_rows[entry['id']])",
     "            os.listdir(held_out_store_path(store, entry, _BLIND))\n            entries.append(held_rows[entry['id']])"),
]
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-b2b4c2-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    RECEIPT = W / 'crates/security/src/custody/discovery_census_held_out.json'; assert RECEIPT.is_file()
    def failures(root, pkg, tag):
        log = B / f'{tag}-{pkg}.log'
        with log.open('wb') as out:
            child = subprocess.Popen([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', pkg], cwd=root, env=E, stdout=out, stderr=subprocess.STDOUT); assert os.getpriority(os.PRIO_PROCESS, child.pid) == 10; code = child.wait()
        text = log.read_text(errors='replace'); fails = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', text, re.M)))
        results = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', text)
        return dict(exitCode=code, failed=fails, passed=sum(int(p) for _, p, _ in results), failedCount=sum(int(f) for _, _, f in results), suites=len(results))
    comparison = {}
    for pkg in ['opensip-security']:
        base = failures(P, pkg, 'base'); cand = failures(W, pkg, 'candidate')
        comparison[pkg] = dict(base=base, candidate=cand, equalFailureSets=base['failed'] == cand['failed'], candidateSuitesEqualBase=cand['suites'] == base['suites'], newPassingTests=cand['passed'] - base['passed'])
        print(pkg, 'base fail', base['failedCount'], 'cand fail', cand['failedCount'], 'passed', base['passed'], cand['passed'], flush=True)
    (B / 'test-comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
    rows = [dict(name='security-base-comparison', exitCode=0 if all(c['equalFailureSets'] and c['candidateSuitesEqualBase'] and c['newPassingTests'] >= 0 for k, c in comparison.items()) else 1, niceness=10)]
    edited = sorted(x for x in git(W, 'diff', '--name-only').splitlines() + git(W, 'ls-files', '--others', '--exclude-standard').splitlines() if x.endswith('.rs'))
    def fmt_clean(path):
        return subprocess.run([R + 'rustfmt', '--edition', '2024', '--check', str(path)], env=E, capture_output=True).returncode == 0
    fmt_rows = [dict(path=x, baseClean=None if not (P / x).exists() else fmt_clean(P / x), candidateClean=fmt_clean(W / x)) for x in edited]
    (B / 'rustfmt-classification.json').write_text(json.dumps(fmt_rows, indent=2) + '\n')
    FMT = [r['path'] for r in fmt_rows if r['baseClean'] is not False]
    steps = [('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
             ('discovery-scan-vectors', [PY, '-I', '-B', 'tools/security/discovery_scan_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-upward-vectors', [PY, '-I', '-B', 'tools/security/discovery_upward_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-walk-vectors', [PY, '-I', '-B', 'tools/security/discovery_walk_vectors.py', '--check', '--architecture', str(A), '--packages-root', str(P)]),
             ('discovery-fw01-pin', [PY, '-I', '-B', 'tools/tests/test_discovery_fw01.py', '-v']),
             ('test-census', [R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-security', '--lib', '--', 'discovery_census_tests', '--nocapture', '--test-threads=1']),
             ('discovery-walk-storage', [PY, '-I', '-B', 'tools/tests/test_discovery_walk_storage.py', '-v']),
             ('discovery-census-controls', [PY, '-I', '-B', 'tools/tests/test_discovery_census.py', '-v']),
             ('discovery-census-blind-controls', BLIND_TESTS + ['-v']),
             ('discovery-census', [PY, '-I', '-B', TOOL, '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]),
             ('configuration-tables', [PY, '-I', '-B', 'tools/tests/test_configuration_tables.py', '-v']),
             ('operability-source', [PY, '-I', '-B', 'tools/check_operability.py', 'source', '--repository', str(W)]),
             ('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)])]
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    controls = []
    CHECK = [PY, '-I', '-B', TOOL, '--check', '--architecture', str(A), '--packages-root', str(P), '--t2-cache', CACHE]
    def tampered(raw):
        r = json.loads(raw); mp = r['rows'][0]['marginPermille']; mp['objects'] += 1
        return (json.dumps(r, indent=1, ensure_ascii=True) + '\n').encode()
    for name, target, change in [('receipt-margin-tampered', RECEIPT, tampered), ('tool-drifted', W / TOOL, lambda raw: raw + b'#\n'), ('receipt-removed', RECEIPT, None)]:
        original = target.read_bytes()
        try:
            if change is None: target.unlink()
            else: target.write_bytes(change(original))
            r = subprocess.run(CHECK, cwd=W, env=E, capture_output=True, text=True)
        finally:
            target.write_bytes(original)
        assert target.read_bytes() == original
        (B / f'receipt-control-{name}.log').write_text(r.stdout + r.stderr)
        caught = r.returncode != 0 and 'Discovery census failed' in r.stderr
        controls.append(dict(kind='receipt-control', name=name, exitCode=r.returncode, caught=caught))
        print('receipt-control', name, 'caught' if caught else 'NOT CAUGHT', flush=True)
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='receipt-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), receiptPresent=RECEIPT.is_file(),
        productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B2-b4c2 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
