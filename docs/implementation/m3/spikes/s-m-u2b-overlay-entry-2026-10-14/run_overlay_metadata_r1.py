from pathlib import Path
import os, json, hashlib, subprocess, tempfile, time
# U-2b overlay metadata runs: the variant test over (control A) rs-medium-serde with no links, (control B) the overlay's
# rs-medium-serde entry with the accepted overlay links, (target) the overlay's rs-medium-serde-json entry with the accepted
# links. Each observation root has a private home whose registry is a copy-on-write clone of template r117 (U-2a). Controls
# must resolve the same package ids and resolve graph as the accepted harness did in u2b-metadata.
V = Path(__file__).resolve().parent; os.setpriority(os.PRIO_PROCESS, 0, 10)
U = Path('/tmp/opensip-implementation/sm-dependency-source-sets-2026-10-14'); C = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-owned-corpus-xw576l4w')
WORK = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/overlay-metadata-roots'); assert not WORK.exists(); WORK.mkdir(parents=True)
def pin(p): raw = Path(p).read_bytes(); return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
build = json.loads((V / 'build.json').read_text()); assert pin(build['executable'])['sha256'] == build['sha256']
plans = {r['ordinal']: r for r in json.loads(Path('/tmp/opensip-implementation/sm-experimental-dependency-preparation-2026-10-10/corpus-attempt-inputs-r1.json').read_text())['plans']}
RUNS = [('control-A-rs-medium-serde', C / 'rs-medium-serde', [], U / 'u2b-metadata/rs-medium-serde.metadata.json'),
        ('control-B-overlay-rs-medium-serde', C / 'mr-rs-medium-serde-json/rs-medium-serde', plans[7]['overlayLinks'], U / 'u2b-metadata/mr-rs-medium-serde-json__rs-medium-serde.metadata.json'),
        ('target-overlay-rs-medium-serde-json', C / 'mr-rs-medium-serde-json/rs-medium-serde-json', plans[8]['overlayLinks'], None)]
for _, _, links, _ in RUNS:
    for l in links: assert pin(Path(l['path']) / 'Cargo.toml')['sha256'] == l['manifestPin']['sha256']
D = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T'); lane = D / 'opensip-lanes.lock'; owned = False; results = []
while True:
    try: lane.mkdir(); owned = True; break
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    for label, project, links, accepted in RUNS:
        root = WORK / label; root.mkdir(mode=0o700); (root / 'home').mkdir(mode=0o700)
        subprocess.run(['/bin/cp', '-cR', str(U / 'registry-intake-template-r117'), str(root / 'home/registry')], check=True)
        before = {str(p.relative_to(project)): pin(p) for p in project.rglob('*') if p.is_file()}
        out = root / 'metadata.json'; packet = root / 'packet.json'; packet.write_text(json.dumps(dict(observationRoot=str(root), project=str(project), output=str(out), overlayLinks=links)) + '\n')
        T = Path(tempfile.mkdtemp(prefix='opensip-u2b-overlay-run-', dir=D)); T.chmod(0o700)
        env = {k: v for k, v in os.environ.items() if k not in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE')}; env.update(TMPDIR=str(T), OPENSIP_EXPERIMENT_OVERLAY_METADATA_PACKET=str(packet), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
        with (root / 'stdout.log').open('wb') as o, (root / 'stderr.log').open('wb') as e:
            code = subprocess.run([build['executable'], 'util::context::experimental_command_data::collect_explicit_experimental_overlay_metadata', '--exact', '--ignored', '--nocapture'], cwd=V / 'producer', env=env, stdout=o, stderr=e).returncode
        after = {str(p.relative_to(project)): pin(p) for p in project.rglob('*') if p.is_file()}; assert before == after
        row = dict(label=label, project=str(project), overlayLinks=links, exitCode=code, metadata=pin(out) if out.exists() else None, root=str(root))
        if code == 0:
            m = json.loads(out.read_text()); row.update(packages=len(m['packages']), registryPackages=sum(1 for p in m['packages'] if p['source']))
            if accepted:
                a = json.loads(accepted.read_text()); norm = lambda d: (sorted(p['id'] for p in d['packages']), sorted((n['id'], sorted(x['pkg'] for x in n['deps']), n['features']) for n in d['resolve']['nodes']))
                row['controlEqualsAcceptedHarness'] = norm(a) == norm(m)
        results.append(row); print(label, code, row.get('packages'), row.get('registryPackages'), row.get('controlEqualsAcceptedHarness'), flush=True)
        (V / 'overlay-metadata-runs-r1.json').write_text(json.dumps(dict(standing='U-2b OVERLAY METADATA VARIANT RUNS', image=build, runs=results), indent=1) + '\n')
finally:
    if owned: lane.rmdir()
