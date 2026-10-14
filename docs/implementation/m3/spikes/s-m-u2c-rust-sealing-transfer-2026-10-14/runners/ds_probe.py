from pathlib import Path
import json, hashlib, sys, time, importlib.util, os
# U-2c SM-5 dependency-source part (D-2): one child per sample. Setup (inputs, reference model) precedes the timed span; the
# timed span reads and SHA-256-hashes every member of the set (O_NOFOLLOW, manifest order), checks each digest and length
# against the package manifest, then computes each package's fileManifestSha256 and the set identity with the reference
# model and checks them against the accepted values. Prints one JSON line.
sys.path.insert(0, '/Users/sb/code/opensip-ai/opensip/tools/contracts/python-packages')
model = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native_evidence_model.v2.py'); spec = importlib.util.spec_from_file_location('native_model', model); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
entry = json.loads(Path(sys.argv[1]).read_text()); desc = json.loads(Path(entry['descriptor']).read_text())
plan = [(p, json.loads(Path(p['manifest']).read_text())) for p in entry['packages']]
start = time.monotonic_ns(); files = 0; total = 0
for p, listing in plan:
    seen = {}
    for f in listing:
        fd = os.open(Path(p['root']) / f['path'], os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC); h = hashlib.sha256(); n = 0
        with os.fdopen(fd, 'rb') as fh:
            while part := fh.read(1048576): h.update(part); n += len(part)
        assert h.hexdigest() == f['contentSha256'] and n == f['byteLength']; seen[f['path']] = dict(sha256=h.hexdigest(), byteLength=n); files += 1; total += n
    assert M.file_manifest_identity(seen) == p['fileManifestSha256']
sid = M.dependency_source_set_identity(desc); assert sid == entry['dependencySourceSetId']
elapsed = time.monotonic_ns() - start
print(json.dumps(dict(entry=entry['entry'], elapsedNanos=elapsed, packages=len(plan), files=files, bytes=total, setIdentity=sid, allDigestsAndIdentitiesMatched=True)))
