"""B2-b4c1 candidate checks (the blind held-out census mode, B2-b4 plan r6 section 2.5; no held-out store is opened by
any check): the security suite (base and candidate, --no-fail-fast, equal failure sets), warning-denied all-targets
Clippy on host and security, rustfmt on base-clean and new edited files, the census-tool controls (the existing file and
the new blind file), the census itself (--check over the lead-readable stores and the vectors; it composes no receipt,
since none exists), the vector checks, the environment and FW-01 pins, the walker storage check, the configuration
tables, the operability census, verify_design, the blind-mode guard mutations (each patches the tool and must make the
blind controls fail), and the synthetic census-record controls for the Rust margin test (each temporarily replaces the
census record with a synthetic composed one: one valid variant must pass and each invalid variant must fail). One lane
hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, re, sys, copy
W = Path('/Users/sb/code/opensip-ai/opensip-b2b4c'); CACHE = '/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1'; P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
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
    T = Path(tempfile.mkdtemp(prefix='opensip-b2b4c1-check-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    E.update(CC='/usr/bin/cc', CXX='/usr/bin/c++', AR='/usr/bin/ar', CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc', SDKROOT=subprocess.check_output(['/usr/bin/xcrun', '--show-sdk-path']).decode().strip())
    git = lambda root, *a: subprocess.check_output(['/usr/bin/git', *a], cwd=root, env=E).decode().strip()
    assert git(P, 'rev-parse', 'HEAD') == git(W, 'rev-parse', 'HEAD') and git(P, 'status', '--porcelain') == ''
    assert not (W / 'crates/security/src/custody/discovery_census_held_out.json').exists()
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
    steps = [('rustfmt-edited', [R + 'rustfmt', '--edition', '2024', '--check', *FMT]),
             ('clippy', [R + 'cargo', 'clippy', '--locked', '--offline', '-p', 'opensip-host', '-p', 'opensip-security', '--all-targets', '--', '-D', 'warnings']),
             ('environment-exceptions', [PY, '-I', '-B', 'tools/tests/test_environment_exceptions.py', '-v']),
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
    for name, before, after in GUARD_MUTATIONS:
        F = W / TOOL; original = F.read_bytes(); text = original.decode()
        assert text.count(before) == 1, name
        F.write_text(text.replace(before, after))
        try:
            r = subprocess.run(BLIND_TESTS, cwd=W, env=E, capture_output=True, text=True)
        finally:
            F.write_bytes(original)
        assert F.read_bytes() == original
        log = r.stdout + r.stderr; (B / f'guard-mutation-{name}.log').write_text(log)
        failed = sorted(set(re.findall(r'^(?:FAIL|ERROR): (\S+) ', log, re.M)))
        caught = r.returncode != 0 and bool(failed)
        controls.append(dict(kind='guard-mutation', name=name, file=TOOL, failedTests=failed, caught=caught))
        print('guard-mutation', name, 'caught' if caught else 'NOT CAUGHT', flush=True)
    # Synthetic census records (margins invented here, never measured): the Rust margin test's classification of composed rows.
    F = W / CENSUS; original = F.read_bytes(); body = json.loads(original)
    held = [i for i, e in enumerate(body['entries']) if e.get('status') == 'outstanding: held-out']
    assert len(held) == 10 and body['heldOutMargin'] == 'outstanding'
    def measured(mp):
        return dict(status='blind-census', result=dict(status='measured', integrity=True, population=True, marginPermille=mp, passes2x=all(v >= 2000 for v in mp.values())))
    def variant(results, state, caps=None, failing=None, stale=False):
        b = copy.deepcopy(body)
        for i, res in zip(held, results):
            b['entries'][i] = dict(id=b['entries'][i]['id'], **res) if res else dict(id=b['entries'][i]['id'], status='outstanding: held-out (blind receipt stale)' if stale else 'outstanding: held-out')
        ids = [b['entries'][i]['id'] for i, res in zip(held, results) if res and res['result'].get('passes2x') is False]
        b['failingEntries'] = ids if failing is None else failing
        b['caps'] = caps or ('returned-to-law' if b['failingEntries'] else 'recorded-margin-holds')
        b['heldOutMargin'] = state
        return b
    lead = [i for i, e in enumerate(body['entries']) if 'status' not in e]
    def rename(b, i, new_id):
        b['entries'][i]['id'] = new_id
        return b
    def substitute(b):
        # A lead-readable row replaced by a passing composed held-out row with the same id.
        b['entries'][lead[0]] = dict(id=b['entries'][lead[0]]['id'], **measured(ok))
        return b
    def omit(b):
        del b['entries'][lead[0]]
        return b
    ok = dict(objects=2500, edges=2100, bytes=3000)
    low = dict(objects=2500, edges=1999, bytes=3000)
    err = dict(status='blind-census', result=dict(status='error', errorClass='MODEL'))
    bad_pass = measured(low); bad_pass['result']['passes2x'] = True
    leaky = dict(status='blind-census', result=dict(status='error', errorClass='MODEL', detail='x'))
    RECORDS = [
        ('valid-holds', True, variant([measured(ok)] * 10, 'holds (blind census)')),
        ('valid-fails', True, variant([measured(low)] + [measured(ok)] * 9, 'fails (blind census)')),
        ('valid-incomplete', True, variant([err] + [measured(ok)] * 9, 'incomplete (blind census)')),
        ('valid-stale', True, variant([None] * 10, 'outstanding', stale=True)),
        ('holds-with-a-failing-margin', False, variant([measured(low)] + [measured(ok)] * 9, 'holds (blind census)')),
        ('holds-with-an-error', False, variant([err] + [measured(ok)] * 9, 'holds (blind census)')),
        ('passes2x-disagrees', False, variant([bad_pass] + [measured(ok)] * 9, 'holds (blind census)')),
        ('partial-coverage', False, variant([None] + [measured(ok)] * 9, 'holds (blind census)')),
        ('failing-but-caps-hold', False, variant([measured(low)] + [measured(ok)] * 9, 'fails (blind census)', caps='recorded-margin-holds')),
        ('failing-not-listed', False, variant([measured(low)] + [measured(ok)] * 9, 'fails (blind census)', caps='returned-to-law', failing=[])),
        ('error-row-open-shape', False, variant([leaky] + [measured(ok)] * 9, 'incomplete (blind census)')),
        # r2 (Codex B2B4C1-R1-RF-1): identities, not only counts.
        ('same-count-duplicate-id', False, rename(variant([measured(ok)] * 10, 'holds (blind census)'), held[0], body['entries'][held[1]]['id'])),
        ('foreign-id', False, rename(variant([measured(ok)] * 10, 'holds (blind census)'), held[0], 'foreign-entry')),
        ('lead-row-substituted', False, substitute(variant([measured(ok)] * 10, 'holds (blind census)'))),
        ('lead-row-omitted', False, omit(variant([measured(ok)] * 10, 'holds (blind census)'))),
    ]
    try:
        for name, valid, b in RECORDS:
            F.write_bytes((json.dumps(b, indent=1, ensure_ascii=True) + '\n').encode())
            r = subprocess.run([R + 'cargo', T_MARGIN[0], '--locked', '--offline', *T_MARGIN[1:]], cwd=W, env=E, capture_output=True, text=True)
            log = r.stdout + r.stderr; (B / f'census-record-{name}.log').write_text(log)
            ran = any(int(p) + int(f) >= 1 for p, f in re.findall(r'test result: \w+\. (\d+) passed; (\d+) failed', log))
            failed = bool(re.findall(r'^test (\S+) \.\.\. FAILED$', log, re.M))
            caught = ran and (r.returncode == 0 and not failed if valid else failed)
            controls.append(dict(kind='census-record', name=name, valid=valid, exitCode=r.returncode, caught=caught))
            print('census-record', name, 'as expected' if caught else 'UNEXPECTED', flush=True)
    finally:
        F.write_bytes(original)
    assert F.read_bytes() == original
    (B / 'controls.json').write_text(json.dumps(dict(rows=controls, allCaught=all(c['caught'] for c in controls)), indent=2) + '\n')
    rows.append(dict(name='guard-and-record-controls', exitCode=0 if all(c['caught'] for c in controls) else 1, niceness=10))
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), receiptAbsent=not (W / 'crates/security/src/custody/discovery_census_held_out.json').exists(),
        productBase=git(P, 'rev-parse', 'HEAD'), rustfmtExcludedBaseDirty=[r['path'] for r in fmt_rows if r['baseClean'] is False],
        standing='UNREVIEWED B2-b4c1 CANDIDATE CHECKS'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
