"""Review02 mutation driver over throwaway copies of subject-02; never subject bytes."""
import json, os, re, shutil, signal, subprocess, sys

R = '/tmp/opensip-implementation/m1-report-assets-review-02'
B = '/opt/homebrew/Cellar/rust/1.95.0/bin'
PRISTINE = R + '/work/copy'
MODE = sys.argv[1]  # final (subject-02 permanent tests) | probes (plus review02 delta probes)
WORK = R + '/work/mutant-' + MODE
LIB, PLAT = 'src/lib.rs', 'platform/src/lib.rs'

# The twelve review01 survivors, with identical edits to review01 mutate.py.
PRIOR = {
    'M01-no-scheme-check': [(LIB, "        && !scheme\n", "")],
    'M02-no-pin-path-validation': [(LIB, "    if !canonical_path(&pin.root)\n        || !canonical_path(&pin.manifest_path)\n        || !under(&pin.manifest_path, &pin.root)\n    {", "    if false {")],
    'M03-admit-zero-manifest-pin': [(LIB, "pin.manifest_bytes == 0 || ", "")],
    'M05-schema-list-dupes-only': [(LIB, "previous.is_some_and(|p| p >= current)", "previous.is_some_and(|p| p == current)")],
    'M06-accept-uppercase-hex': [
        (LIB, "(b'a'..=b'f').contains(x))", "(b'a'..=b'f').contains(&x.to_ascii_lowercase()))"),
        (LIB, "{ v - b'a' + 10 }", "{ v.to_ascii_lowercase() - b'a' + 10 }"),
    ],
    'M07-no-4096-char-bound': [(LIB, "        && path.chars().count() <= 4096\n", "")],
    'M14-no-lying-reader-guard': [(LIB, "        if count > cap {\n            return Err(AssetError::Io);\n        }\n", "")],
    'M18-admit-empty-schemas': [(LIB, "    if schemas.is_empty() {", "    if false {")],
    'M19-schema-version-le-1': [(LIB, 'length(&doc["schemaVersion"])? != 1', 'length(&doc["schemaVersion"])? > 1')],
    'M21-completeness-no-path-check': [(LIB, "    if regular_paths\n        .iter()\n        .any(|p| !canonical_path(p) || !under(p, &verified.root))\n    {", "    if false {")],
    'M28-compat-last-schema-only': [(LIB, "compatible |= current == *projection;", "compatible = current == *projection;")],
    'P08-no-O_CLOEXEC': [(PLAT, "                | libc::O_CLOEXEC\n", "")],
}
SIG = [(LIB, ") -> Result<Vec<Member>, AssetError> {", ") -> Result<(Vec<Member>, [u8; 32]), AssetError> {"),
       (LIB, "    let members = manifest(&raw, pin, projection)?;", "    let (members, listed) = manifest(&raw, pin, projection)?;"),
       (LIB, "        projection_sha256: *projection,", "        projection_sha256: listed,")]
NEW = {
    'N01-projection-zero': [(LIB, "        projection_sha256: *projection,", "        projection_sha256: [0; 32],")],
    'N02-projection-is-manifest-digest': [(LIB, "        projection_sha256: *projection,", "        projection_sha256: pin.manifest_sha256,")],
    'N03-projection-first-listed': SIG + [(LIB, "    Ok(members)\n}", "    Ok((members, digest(&schemas[0])?))\n}")],
    'N04-projection-last-listed': SIG + [(LIB, "    Ok(members)\n}", "    Ok((members, digest(schemas.last().ok_or(AssetError::Shape)?)?))\n}")],
}
MUTANTS = {**PRIOR, **NEW}
env = {'PATH': B + ':/usr/bin:/bin', 'HOME': os.environ['HOME'], 'TMPDIR': R + '/tmp',
       'CARGO_TARGET_DIR': R + '/target/mutants-' + MODE, 'RUSTC': B + '/rustc', 'RUSTDOC': B + '/rustdoc'}


def prepare(edits):
    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    # Fresh mtimes: restoring a file with its old mtime would let cargo reuse a stale mutant build.
    shutil.copytree(PRISTINE, WORK, symlinks=True, copy_function=shutil.copy)
    if MODE == 'probes':
        shutil.copy(R + '/probe-src/delta_probes.rs', WORK + '/tests/delta_probes.rs')
    if MODE == 'original':
        # Subject-02 minus the adopted regressions: the review01-era suite plus the new field.
        edits = [(LIB, "\n#[cfg(test)]\nmod asset_tests;\n", "\n")] + list(edits)
        os.remove(WORK + '/src/asset_tests.rs')
        os.remove(WORK + '/platform/tests/file_flags.rs')
    for path, old, new in edits:
        text = open(os.path.join(WORK, path)).read()
        assert text.count(old) == 1, (path, old, text.count(old))
        open(os.path.join(WORK, path), 'w').write(text.replace(old, new))


def cargo(extra):
    cmd = [B + '/cargo', 'test', '--locked', '--offline', '--no-fail-fast'] + extra
    p = subprocess.Popen(cmd, cwd=WORK, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=120)
        return ('build-error' if 'could not compile' in out else 'pass' if p.returncode == 0 else 'fail'), out
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        return 'timeout', p.communicate()[0]


results = {}
for name in ['CONTROL'] + list(MUTANTS):
    prepare(MUTANTS.get(name, []))
    root, out_root = cargo([])
    plat, out_plat = cargo(['--manifest-path', 'platform/Cargo.toml'])
    out = out_root + out_plat
    failed = sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED', out, re.M)))
    counts = [tuple(map(int, m)) for m in re.findall(r'test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored', out)]
    outcomes = {root, plat}
    if 'build-error' in outcomes:
        verdict = 'build-error'
    elif outcomes == {'pass'}:
        verdict = 'survived'
    else:
        verdict = 'killed'
    if name == 'CONTROL':
        verdict = 'control-pass' if outcomes == {'pass'} else 'CONTROL-FAILED'
    results[name] = {'verdict': verdict, 'root': root, 'platform': plat, 'failedTests': failed,
                     'resultLines(passed,failed,ignored)': counts}
    print(f'{name:36s} {verdict:13s} root={root} platform={plat} {failed}', flush=True)
    if verdict in ('CONTROL-FAILED', 'build-error'):
        print(out[-3000:])
        if name == 'CONTROL':
            break
shutil.rmtree(WORK, ignore_errors=True)
json.dump(results, open(f'{R}/mutation-{MODE}.json', 'w'), indent=2)
