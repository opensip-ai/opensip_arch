from pathlib import Path
import json, hashlib, shutil, subprocess, os, re
# Freeze the outside-product mixed-case public intake variant (SM-PUBLIC-INTAKE-MIXED-CASE-r1) for independent review.
B = Path('/tmp/opensip-implementation'); V = B / 'sm-public-intake-mixed-case-2026-10-11'; S = B / 'sm-public-intake-mixed-case-r1-stage'; Q = B / 'reviews/grok-sm-public-intake-mixed-case-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
assert not S.exists() and not Q.exists()
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def cp(p, r):
    out = S / r; out.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, out); assert pin(out) == pin(p)
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
st = json.loads((C / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
closed_stage = B / 'sm-public-intake-entry-r1-stage'; closed = json.loads((closed_stage / 'source.json').read_text()); closed_root = Path(closed['isolatedProducer'])
for f in closed['finalSourcePins']: assert pin(closed_root / f['path']) == dict(bytes=f['bytes'], sha256=f['sha256'])
assert pin(closed['compiledCargoImage']['path']) == {k: closed['compiledCargoImage'][k] for k in ['bytes', 'sha256']}
producer = V / 'producer'; new_module = 'src/cargo/util/context/experimental_public_cache_intake/mixed_case_entry.rs'
paths = [f['path'] for f in closed['finalSourcePins']] + [new_module]
for rel in paths:
    cp(producer / rel, 'candidate/' + rel)
    if rel != new_module:
        cp(closed_root / rel, 'parent/' + rel)
        old = (closed_root / rel).read_bytes(); new = (producer / rel).read_bytes()
        if rel.endswith('/experimental_public_cache_intake.rs'): assert new.startswith(old) and new[len(old):].decode().strip() == 'mod mixed_case_entry;'
        else: assert new == old
# Whole-tree check: only the new module and the one-line registration differ from the closed producer.
diff = subprocess.run(['/usr/bin/diff', '-rq', str(closed_root), str(producer)], capture_output=True, text=True).stdout.strip().splitlines()
assert len(diff) == 2 and any('mixed_case_entry.rs' in d for d in diff) and any(d.endswith('experimental_public_cache_intake.rs differ') for d in diff), diff
log = V / 'mixed-case-controls-r1.log'; checks = json.loads((V / 'mixed-case-checks-r1.json').read_text()); assert checks['exitCode'] == 0
text = log.read_text(); assert 'test result: ok. 7 passed; 0 failed; 2 ignored' in text
image_path = re.search(r'Running unittests src/cargo/lib.rs \(([^)]+)\)', text).group(1); image = dict(path=image_path, **pin(image_path))
cp(log, 'mixed-case-controls-r1.log'); cp(V / 'mixed-case-checks-r1.json', 'mixed-case-checks-r1.json')
roots = []
for line in text.splitlines():
    m = re.match(r'ACTUAL_[A-Z_]+=(.*)$', line)
    if m: roots += m.group(1).split()
for index, root in enumerate(roots):
    root = Path(root)
    for f in sorted(root.rglob('*')):
        if f.is_file(): cp(f, f'actual-control-outputs/{index}-{root.name}/' + f.relative_to(root).as_posix())
inputs = V / 'inputs'
for f in sorted(inputs.rglob('*')):
    if f.is_file(): cp(f, 'inputs/' + f.relative_to(inputs).as_posix())
for n in ['source.json', 'subject.json', 'integration.json', 'REPORT.md']: cp(closed_stage / n, 'closed-parent-reference/' + n)
for n in ['review.json', 'REVIEW.md']: cp(B / 'reviews/grok-sm-public-intake-entry-r1' / n, 'closed-parent-reference/' + n)
for n in ['prepare_sm_public_intake_mixed_case_inputs_r1.py', 'run_sm_public_intake_mixed_case_checks_r1.py', 'freeze_sm_public_intake_mixed_case_r1.py']: cp(B / n, 'runners/' + n)
source = dict(unit='SM-PUBLIC-INTAKE-MIXED-CASE-r1', standing='FROZEN OUTSIDE-PRODUCT MIXED-CASE PUBLIC CACHE INTAKE VARIANT AND ACTUAL CONTROLS; CLOSED LOWERCASE INTAKE UNCHANGED',
              productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), isolatedProducer=str(producer), closedParentProducer=str(closed_root),
              finalSourcePins=[dict(path=rel, **pin(producer / rel)) for rel in paths], compiledCargoImage=image, closedParentImage=closed['compiledCargoImage'],
              controlsPassed=7, newControlsPassed=3, closedRegressionControlsPassed=4, ignoredEntryTests=2, mixedCasePublicIndexes=1, mixedCasePublishedVersionRecords=27, mixedCaseWholeArchiveChecksumMatches=27,
              lowercaseEquivalenceOutputFiles=140, mixedCaseOutputFiles=28, refusalControls=3, closedIntakeRefusesMixedCase=True,
              closedIntakeBodyUnchanged=True, onlyNewModuleAndRegistrationDiffer=True, indexCachePathLowercasedViaCargoMakeDepPath=True, exactPublishedNameInIndexRowsAndArchiveNames=True,
              caseFoldedDuplicateRefused=True, lowercaseInputsByteIdenticalToClosedIntake=True, warnings=0,
              publicAcquisitionPerformed=True, corpusResolutionRun=False, typecheckExecuted=False, applicationExecuted=False, buildScriptOrProcMacroExecuted=False,
              sourceAuthentication=False, nativeAdmission=False, productChange=False, SMComplete=False, effectiveL=False, productQualification=False, entirePlanComplete=False)
write(S / 'source.json', source)
(S / 'REPORT.md').write_text("""Mixed-case public cache intake variant

The closed accepted public cache intake admits lowercase index names only, so the original Deno root and Smithy `rust-runtime` locks, which require crates.io `Inflector`, cannot be supplied offline. This outside-product variant adds one new module beside the closed intake; the closed intake body is byte-unchanged and the parent module gains only the one-line registration. The variant admits ASCII letters (either case), digits, `-` and `_`; refuses case-folded duplicates; requires every index row's name to equal the supplied name exactly; keeps the exact published name in archive file names (Cargo `tarball_name`); and writes the index cache under Cargo's lowered relative path (`make_dep_path` of the lowercased name), matching stock `RegistryIndex` summary loading.

Seven actual controls pass with no warnings: four closed intake regression controls and three new controls. Lowercase inputs produce byte-identical output to the closed intake (140 files). Actual anonymous `Inflector` inputs (27 published versions, all whole-checksum matched) are refused by the closed intake and admitted by the variant: one mixed-case index at `in/fl/inflector` whose 27 rows keep name `Inflector`, and 27 `Inflector-*.crate` archives. A lowered supplied name, a case-folded duplicate and an unsafe name each refuse before any registry output.

No corpus resolution, typecheck, application, build script or proc macro ran. Public acquisition is not source authentication. No native admission, product change, full S-M, effective L or qualification. Exact review, own assent and fresh verification are required before an architecture-only support publication. No push.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit=source['unit'], files=files)); subject = pin(S / 'subject.json'); Q.mkdir()
expected = {k: v for k, v in source.items() if type(v) in [int, bool]}; expected.update(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=subject['sha256'], supportingOnly=True)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-PUBLIC-INTAKE-MIXED-CASE-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the isolated producer, or control files. Do not run the compiler, Cargo, tests, runners, or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing, source reading and Git queries are permitted.

## Subject

- Stage: `{S}`
- `subject.json`: {subject['bytes']} bytes, SHA-256 `{subject['sha256']}`, {len(files)} members. Rehash every member, and rehash `finalSourcePins` in the isolated producer and the `compiledCargoImage` and `closedParentImage` pins in place.

## What to review

A new outside-product module, `candidate/{new_module}`, beside the closed accepted intake (`closed-parent-reference/`, your review `grok-sm-public-intake-entry-r1`).

1. **Closed body unchanged.** `candidate/` equals `parent/` except the new module and the trailing `mod mixed_case_entry;` line in `experimental_public_cache_intake.rs`.
2. **Semantics.** Compare `intake_mixed_case` line by line with the closed `intake`. The only intended differences: the name rule admits ASCII uppercase; uniqueness is case-folded; the index cache output path is `make_dep_path(lowercased name)` from `cargo_util::registry` (confirm against stock `RegistryIndex::parse`, `src/cargo/sources/registry/index/mod.rs`, which lowers the name before `make_dep_path`); the report adds `mixedCaseIndexes`/`indexCachePathsLowercased`. Index rows must still equal the supplied name exactly, archive names keep the exact published name (stock `tarball_name`), every version still needs an archive, and all validation precedes the first output.
3. **Controls.** `mixed-case-controls-r1.log`: 7 passed, 0 failed, 2 ignored entry tests, no warnings. Retained outputs under `actual-control-outputs/` show (a) lowercase equivalence: closed and variant trees byte-identical, 140 files; (b) actual `Inflector` inputs (`inputs/`, 27 versions, anonymous, whole-checksum matched): index at `.cache/in/fl/inflector`, rows named `Inflector`, 27 `Inflector-*.crate` archives, and the closed intake refuses the same inputs; (c) three refusals (lowered name, case-folded duplicate, unsafe name) with no registry output.
4. **Scope.** No corpus resolution or typecheck, no application/script/proc-macro execution; public acquisition is not source authentication; no native admission, product change, full S-M, effective L or qualification.

Product, law, lock, inventory 187 and contracts 161 are unchanged. O7, D3 and D13 are closed. Native production admission is not an extra gate on outside-product S-M experiments.

## Output

`review.json` must carry `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` (array), and exactly these expected fields with your independently checked values (report the actual value and raise a finding if any differs):

```json
{json.dumps(expected, indent=2)}
```

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.
""")
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Review mixed-case public intake variant.'); st['SMPublicIntakeMixedCaseFrozenSubject'] = subject; write(C / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=subject, members=len(files)), indent=2))
