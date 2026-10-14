from pathlib import Path
import importlib.util, json, hashlib, tomllib, os, subprocess, sys
# U-2b steps 5-7: package keys and unified features (accepted project_actual_axum_features.py), per-package file manifests
# (the accepted, unretained step-6 format reconstructed: sorted [{path, contentSha256, byteLength}], indent 2, newline) and
# the DependencySourceSetV1 descriptor (accepted prepare_actual_dependency_source_set.py), for every audited U-2b entry.
# Every identity is computed by the reference model AND the rebuilt product bridge, which must agree. axum is the control:
# package keys, all 187 file manifests and the descriptor must equal the accepted ones byte for byte (set 879ff234...).
sys.path.insert(0, '/Users/sb/code/opensip-ai/opensip/tools/contracts/python-packages')  # product-vendored jsonschema 4.25.1 (the measurement copy is no longer complete); os.setpriority(os.PRIO_PROCESS, 0, 10)
W = Path(__file__).resolve().parent; A = Path('/Users/sb/code/opensip-ai/opensip_arch'); SP = A / 'docs/implementation/m3/spikes'
model = A / 'docs/coop/design-corrections/native/native_evidence_model.v2.py'; spec = importlib.util.spec_from_file_location('native_model', model); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
bridge_build = json.loads((W / 'hash-bridge/build.json').read_text()); BR = bridge_build['executable']
def pin(p): raw = Path(p).read_bytes(); return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def bridge(domain, path):
    assert pin(BR)['sha256'] == bridge_build['sha256']
    child = subprocess.Popen([BR, domain, str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE); out, err = child.communicate(); assert child.returncode == 0, err
    return 'sha256:' + json.loads(out)['identityDigest']
def resolver_of(root):
    t = tomllib.loads((root / 'Cargo.toml').read_text())
    if 'workspace' in t and 'resolver' in t['workspace']: return int(t['workspace']['resolver']), 'workspace.resolver'
    if 'package' in t and 'resolver' in t['package']: return int(t['package']['resolver']), 'package.resolver'
    edition = str(t.get('package', {}).get('edition', '2015')); r = 3 if edition == '2024' else 2 if edition == '2021' else 1
    return r, f'Cargo default for package edition {edition}'
att = {a['slug']: a for a in json.loads((W / 'u2b-metadata-attempts-r1.json').read_text())['attempts']}
audits = json.loads((W / 'u2b-source-audits.json').read_text())['entries']; OUT = W / 'u2b-sets'; assert not OUT.exists(); OUT.mkdir(); summary = []
acc_keys = {r['packageKey']: r for r in json.loads((SP / 's-m-context-identity-2026-10-09/actual-feature-projection/package-keys.json').read_text())['packages']}
acc_desc = (SP / 's-m-dependency-fragment-2026-10-09/retained-set/descriptor.json').read_bytes()
for e in audits:
    if not e['audited']: summary.append(dict(entry=e['entry'], slug=e['slug'], built=False, reason=e['reason'])); continue
    a = att[e['slug']]; D = OUT / e['slug']; D.mkdir()
    meta = Path(a['metadata']['path']); assert pin(meta) == a['metadata']; j = json.loads(meta.read_text()); root = Path(j['workspace_root'])
    receipt = json.loads(Path(a['receipt']['path']).read_text()); lockpath = Path(receipt['originalLock']['path']); assert pin(lockpath) == receipt['originalLock']
    lockdoc = tomllib.loads(lockpath.read_text()); lock_packages = lockdoc['package']; resolver, resolver_basis = resolver_of(root)
    # Step 5
    lookup = {}; tuple_rows = []; seen = set()
    for p in j['packages']:
        t = [p['name'], p['version'], p['source'] or '']; matches = [r for r in lock_packages if [r['name'], r['version'], r.get('source', '')] == t]; assert len(matches) == 1, t
        enc = M.C.canonical(t); key = 'pkg1-' + hashlib.sha256(enc).hexdigest(); assert key not in seen and p['id'] not in lookup; seen.add(key); lookup[p['id']] = key
        tuple_rows.append(dict(metadataId=p['id'], tuple=t, canonicalTupleUtf8=enc.decode(), packageKey=key))
    rows = []
    for node in j['resolve']['nodes']:
        f = node['features']; assert f == sorted(set(f)) and all(x['pkg'] in lookup for x in node['deps']); rows.append(dict(packageKey=lookup[node['id']], features=f))
    rows.sort(key=lambda r: r['packageKey'])
    features = dict(schemaVersion=1, resolverVersion=resolver, targetTriple=a['filterPlatform'], activated=rows, computedBy=dict(producer='opensip-cargo-adapter', producerBuildId='measurement-cargo-' + json.loads((W / 'u2b-metadata-attempts-r1.json').read_text())['image']['sha256']))
    write(D / 'unified-features.json', features); write(D / 'package-keys.json', dict(standing='LOCK TUPLE / METADATA UNIQUE JOIN (U-2b); NOT SOURCE ADMISSION', packages=sorted(tuple_rows, key=lambda r: r['packageKey'])))
    uf = M.unified_features_identity(features); assert uf == bridge('native.unified-features.rust.v1', D / 'unified-features.json')
    # Step 6
    audit = json.loads((W / 'u2b-source-audits' / f"{e['slug']}.json").read_text()); man_rows = []
    for r in audit['rows']:
        key = lookup[r['packageId']]; files = {f['path']: dict(sha256=f['sha256'], byteLength=f['bytes']) for f in r['regularFiles']}
        listing = sorted(({'path': p, 'contentSha256': v['sha256'], 'byteLength': v['byteLength']} for p, v in files.items()), key=lambda x: x['path'].encode('utf-8'))
        mp = D / 'file-manifests' / f'{key}.json'; mp.parent.mkdir(exist_ok=True); mp.write_text(json.dumps(listing, indent=2) + '\n')
        fid = M.file_manifest_identity(files); assert 'sha256:' + fid == bridge('native.dependency-file-manifest.v1', mp)
        man_rows.append(dict(packageKey=key, packageTuple=[r['name'], r['version'], r['source']], fileManifest=pin(mp), fileManifestSha256=fid, fileCount=len(listing), totalBytes=sum(x['byteLength'] for x in listing), originalArchiveChecksum=r['archiveChecksum']))
    write(D / 'file-manifest-observations.json', dict(standing='PER-PACKAGE FILE MANIFESTS (U-2b)', rows=man_rows))
    # Step 7
    tuples = {(p['name'], p['version'], p.get('source', '')): p for p in lock_packages}; packages = []
    for r in man_rows:
        lp = tuples[tuple(r['packageTuple'])]; assert lp['checksum'] == r['originalArchiveChecksum']
        packages.append(dict(name=r['packageTuple'][0], version=r['packageTuple'][1], sourceKind='registry', sourceId=lp['source'], lockChecksum=lp['checksum'], fileManifestSha256=r['fileManifestSha256'], fileCount=r['fileCount'], totalBytes=r['totalBytes'],
                             acquisition=dict(mode='imported-descriptor', descriptorId=None, vendorPath=None), checksumVerification='tarball-matched', provenanceAssurance='registry-authenticated'))
    external = [p for p in j['packages'] if p['source'] is not None]; assert len(packages) == len(external)
    packages.sort(key=lambda p: tuple(p[k].encode() for k in ['name', 'version', 'sourceId']))
    descriptor = dict(schemaVersion=1, language='rust', lockfileIdentity=dict(path='Cargo.lock', contentSha256=receipt['originalLock']['sha256'], lockfileVersion=lockdoc['version']), packages=packages, completeness=dict(state='complete', missing=[]))
    write(D / 'descriptor.json', descriptor); sid = M.dependency_source_set_identity(descriptor); assert sid == bridge('native.dependency-source-set.v1', D / 'descriptor.json')
    control = None
    if e['entry'] == 'rs-medium-axum':
        assert (D / 'descriptor.json').read_bytes() == acc_desc and sid == 'sha256:879ff2348eb48e9c3f4559bb39be84c6688c9e69beddeb6ac3c84c29d0c5e4a8'
        assert {r['packageKey'] for r in tuple_rows} == set(acc_keys)
        for r in man_rows: assert Path(r['fileManifest']['path']).read_bytes() == (SP / 's-m-dependency-fragment-2026-10-09/package-file-manifests' / f"{r['packageKey']}.json").read_bytes(), r['packageKey']
        control = dict(descriptorByteEqualAccepted=True, setIdEqualAccepted=True, packageKeysEqualAccepted=True, fileManifestsByteEqualAccepted=len(man_rows))
    obs = dict(standing='U-2b DEPENDENCY-SOURCE SET DESCRIPTOR (REFERENCE AND PRODUCT BRIDGE AGREE); NO SOURCE OR IMPORT ADMISSION', entry=e['entry'], descriptor=pin(D / 'descriptor.json'), dependencySourceSetId=sid, unifiedFeaturesId=uf,
               resolverVersion=resolver, resolverBasis=resolver_basis, registryPackages=len(packages), regularFiles=sum(p['fileCount'] for p in packages), totalBytes=sum(p['totalBytes'] for p in packages),
               lockfile=pin(lockpath), lockfileVersion=lockdoc['version'], lockIsOriginal=(e['entry'] == 'rs-medium-axum'), axumControl=control, productBridge=bridge_build, referenceModel=pin(model), sourceAdmission=False, selectedImportWrapperConstructed=False)
    write(D / 'observations.json', obs); summary.append(dict(entry=e['entry'], slug=e['slug'], built=True, dependencySourceSetId=sid, registryPackages=len(packages), regularFiles=obs['regularFiles'], totalBytes=obs['totalBytes'], lockIsOriginal=obs['lockIsOriginal'], axumControl=control))
    print(e['entry'], sid[:23], len(packages), obs['regularFiles'], obs['totalBytes'], flush=True)
write(W / 'u2b-sets.json', dict(standing='U-2b DEPENDENCY-SOURCE SETS', sets=summary))
