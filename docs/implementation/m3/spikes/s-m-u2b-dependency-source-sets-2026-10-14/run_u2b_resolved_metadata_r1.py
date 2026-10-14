from pathlib import Path
import os, json, hashlib, subprocess, tempfile, time
# U-2b step 2: the accepted run_axum_resolved_metadata.py recipe (accepted harness image 45816163..., test
# opensip_spike_metadata_collect; offline/frozen/locked configure; no_deps=false; filter-platform aarch64-apple-darwin;
# private CARGO_HOME seeded only from the receipt; immutable-corpus check) looped over the nine U-2b receipts.
# axum is the control: its metadata must equal the accepted axum-resolved-metadata.json up to private paths.
W = Path(__file__).resolve().parent; os.setpriority(os.PRIO_PROCESS, 0, 10)
C = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-owned-corpus-xw576l4w')
def pin(p): raw = Path(p).read_bytes(); return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
IMAGE = dict(path='/tmp/opensip-implementation/native-cargo-profile-source-2026-10-09/spike-metadata-target/debug/deps/cargo-820b7793ee1bc124', bytes=73176200, sha256='4581616330816ce2d3c95694b218b86a054473ae56431d1daf3816883b256f92')
assert pin(IMAGE['path']) == IMAGE
index = json.loads((W / 'u2b-receipts.json').read_text()); OUT = W / 'u2b-metadata'; assert not OUT.exists(); OUT.mkdir()
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False; attempts = []
while True:
    try: lane.mkdir(); owned = True; break
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    for row in index['receipts']:
        rp = Path(row['receipt']['path']); assert pin(rp) == row['receipt']; receipt = json.loads(rp.read_text())
        assert pin(receipt['originalLock']['path'])['sha256'] == receipt['originalLock']['sha256']
        for r in receipt['packages']: q = pin(r['archive']); assert q['sha256'] == r['checksum'] == r['sha256'] and q['bytes'] == r['bytes']
        for r in receipt['indexFiles']: q = pin(r['path']); assert q['sha256'] == r['sha256'] and q['bytes'] == r['bytes']
        assert pin(receipt['registryConfigPath'])['sha256'] == receipt['registryConfigSha256']
        root = C / row['entry']; before = {str(p.relative_to(root)): pin(p) for p in root.rglob('*') if p.is_file()}
        T = Path(tempfile.mkdtemp(prefix='opensip-sm-u2b-resolve-', dir=D)); T.chmod(0o700); home = T / 'home'; home.mkdir(mode=0o700)
        out = OUT / f"{row['slug']}.metadata.json"; packet = T / 'packet.json'
        packet.write_text(json.dumps(dict(cwd=str(root), privateCargoHome=str(home), manifestPath=str(root / 'Cargo.toml'), output=str(out), rustc='/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot/bin/rustc',
                                          dependencyCacheReceipt=str(rp), noDeps=False, filterPlatform='aarch64-apple-darwin')) + '\n')
        E = dict(PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin', CARGO_HOME='/Users/sb/.cargo', TMPDIR=str(T), OPENSIP_SPIKE_METADATA_PACKET=str(packet))
        if 'HOME' in os.environ: E['HOME'] = os.environ['HOME']
        stdout = OUT / f"{row['slug']}.stdout"; stderr = OUT / f"{row['slug']}.stderr"; start = time.monotonic_ns()
        with stdout.open('wb') as o, stderr.open('wb') as e:
            child = subprocess.Popen([IMAGE['path'], 'util::context::sealed_spike_metadata_tests::opensip_spike_metadata_collect', '--exact', '--ignored', '--nocapture'], cwd=T, env=E, stdout=o, stderr=e)
            priority = os.getpriority(os.PRIO_PROCESS, child.pid); assert priority == 10; code = child.wait()
        after = {str(p.relative_to(root)): pin(p) for p in root.rglob('*') if p.is_file()}; assert before == after, 'corpus files changed'
        v = dict(entry=row['entry'], slug=row['slug'], exitCode=code, elapsedNanos=time.monotonic_ns() - start, privateTMPDIR=str(T), privateCargoHome=str(home), receipt=row['receipt'], observedNiceness=priority,
                 originalSourceCopiesUnchanged=True, generatedOrUpdatedLockfile=False, repositoryCodeExecuted=False, sourceAdmission=False, filterPlatform='aarch64-apple-darwin', stdout=pin(stdout), stderr=pin(stderr), metadata=pin(out) if out.exists() else None)
        if code == 0:
            assert '1 passed' in stdout.read_text(); m = json.loads(out.read_text()); assert m['resolve'] is not None
            v.update(packages=len(m['packages']), registryPackages=sum(1 for p in m['packages'] if p['source']), resolvedNodes=len(m['resolve']['nodes']), workspaceMembers=len(m['workspace_members']))
        attempts.append(v); print(row['entry'], 'exit', code, v.get('packages'), v.get('registryPackages'), flush=True)
        (W / 'u2b-metadata-attempts-r1.json').write_text(json.dumps(dict(standing='U-2b RESOLVED METADATA ATTEMPTS (ACCEPTED HARNESS; OFFLINE LOCKED FROZEN; FILTER aarch64-apple-darwin)', image=IMAGE, attempts=attempts, ownedLane=True), indent=1) + '\n')
finally:
    if owned: lane.rmdir()
    assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
