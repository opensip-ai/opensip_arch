"""Review02 compile-fail probes: public API cannot forge or mutate verified state."""
import json, os, shutil, subprocess

R = '/tmp/opensip-implementation/m1-report-assets-review-02'
B = '/opt/homebrew/Cellar/rust/1.95.0/bin'
WORK = R + '/work/compile-fail'
HEAD = 'use opensip_report_asset_trial::{Role, VerifiedAsset, VerifiedBundle};\n#[allow(dead_code)]\n'
CASES = {
    'cf_ok_control': (None, 'fn f(b: &VerifiedBundle) -> [u8; 32] { let _ = b.assets(); *b.projection_sha256() }'),
    'cf_construct_bundle': ('E0451', 'fn f() -> VerifiedBundle { VerifiedBundle { root: String::new(), manifest_path: String::new(), manifest_sha256: [0; 32], projection_sha256: [0; 32], assets: Vec::new() } }'),
    'cf_construct_asset': ('E0451', 'fn f() -> VerifiedAsset { VerifiedAsset { path: String::new(), role: Role::Script, bytes: Vec::new() } }'),
    'cf_read_private_projection_field': ('E0616', 'fn f(b: &VerifiedBundle) -> [u8; 32] { b.projection_sha256 }'),
    'cf_assign_projection_through_accessor': ('E0594', 'fn f(b: &mut VerifiedBundle) { *b.projection_sha256() = [0; 32]; }'),
    'cf_assign_manifest_digest_through_accessor': ('E0594', 'fn f(b: &mut VerifiedBundle) { *b.manifest_sha256() = [0; 32]; }'),
    'cf_mutate_asset_bytes': ('E0594', 'fn f(b: &mut VerifiedBundle) { b.assets()[0].bytes()[0] = 1; }'),
    'cf_clone_bundle': ('E0308', 'fn f(b: &VerifiedBundle) -> VerifiedBundle { b.clone() }'),
}
env = {'PATH': B + ':/usr/bin:/bin', 'HOME': os.environ['HOME'], 'TMPDIR': R + '/tmp',
       'CARGO_TARGET_DIR': R + '/target/compile-fail', 'RUSTC': B + '/rustc', 'RUSTDOC': B + '/rustdoc'}
if os.path.exists(WORK):
    shutil.rmtree(WORK)
shutil.copytree(R + '/work/copy', WORK, symlinks=True)
results = {}
for name, (code, body) in CASES.items():
    path = f'{WORK}/tests/{name}.rs'
    open(path, 'w').write(HEAD + body + '\n')
    p = subprocess.run([B + '/cargo', 'test', '--locked', '--offline', '--no-run', '--test', name],
                       cwd=WORK, env=env, capture_output=True, text=True)
    os.remove(path)
    codes = sorted(set(__import__('re').findall(r'error\[(E\d{4})\]', p.stderr)))
    ok = (p.returncode == 0) if code is None else (p.returncode != 0 and codes == [code])
    results[name] = {'expected': code or 'compiles', 'exit': p.returncode, 'errorCodes': codes, 'pass': ok}
    print(f'{name:45s} expected={code or "compiles":8s} got={codes or p.returncode} {"PASS" if ok else "FAIL"}')
shutil.rmtree(WORK)
json.dump(results, open(R + '/compile-fail-results.json', 'w'), indent=2)
