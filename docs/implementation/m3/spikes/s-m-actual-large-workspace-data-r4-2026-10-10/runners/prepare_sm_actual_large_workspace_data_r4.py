from pathlib import Path
import os, stat, json, hashlib, shutil, collections

os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-large-original-context-census-2026-10-10'
D = B / 'sm-actual-large-workspace-data-r4-draft'
C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
assert not D.exists()
D.mkdir()

def checked(path, expected=None):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    with os.fdopen(fd, 'rb') as f:
        before = os.fstat(f.fileno())
        assert stat.S_ISREG(before.st_mode)
        raw = f.read()
        after = os.fstat(f.fileno())
        assert (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns)
    pin = dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    if expected:
        assert all(pin[k] == expected[k] for k in ['bytes', 'sha256'])
    return raw, pin

def copy(path, relative):
    raw, pin = checked(path)
    destination = D / relative
    assert not destination.exists()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(raw)
    checked(destination, pin)
    return pin

names = ['actual-smithy-original-workspace-attempts-r8.json', 'actual-original-hierarchy-workspace-attempts-r6.json', 'actual-other-large-workspace-attempts-r8.json']

receipts = []
external = {}
outcomes = collections.Counter()
collectors = queries = graphs = 0
for name in names:
    data = json.loads(checked(V / name)[0])
    receipt_pin = copy(V / name, 'receipts/' + name)
    receipts.append(receipt_pin)
    assert data['actualCollectorRoots'] == len(data['results'])
    collectors += data['actualCollectorRoots']
    queries += data['compilerInformationQueries']
    graphs += data['successfulGraphs']
    assert data['typecheckExecuted'] is False and data['SMComplete'] is False
    packet_receipt = data['inputPackets']
    checked(Path(packet_receipt['path']), packet_receipt)
    packet_name = Path(packet_receipt['path']).name
    if not (D / 'packet-receipts' / packet_name).exists():
        copy(Path(packet_receipt['path']), 'packet-receipts/' + packet_name)
    for record in data['results']:
        packet_ref = record['packet']
        raw, _ = checked(Path(packet_ref['path']), packet_ref)
        packet = json.loads(raw)
        root = Path(packet_ref['root'])
        assert root.is_relative_to(Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T'))
        prefix = 'raw/' + name.removesuffix('.json') + '/' + str(record['ordinal'])
        for path in sorted(root.iterdir()):
            if path.is_file():
                copy(path, prefix + '/' + path.name)
        directory = root / 'queries'
        if directory.exists():
            for path in sorted(directory.rglob('*')):
                if path.is_file():
                    copy(path, prefix + '/queries/' + path.relative_to(directory).as_posix())
        for row in packet['originalFiles']:
            path = Path(packet['memberRoot']) / row['path']
            key = str(path)
            if key not in external:
                _, external[key] = checked(path, row)
        template_ref = packet['registryTemplateMetadata']
        key = str(template_ref['path'])
        if key not in external:
            _, external[key] = checked(Path(key), template_ref)
            template = json.loads(Path(key).read_bytes())
            copy(Path(key), 'registry-template-receipts/' + Path(key).name)
            for row in template['files']:
                path = Path(template['templateRoot']) / row['path']
                if str(path) not in external:
                    _, external[str(path)] = checked(path, row)
        outcome = record.get('outcome')
        error = None if outcome is None else outcome.get('error')
        category = 'successful-static-graph' if outcome and outcome['success'] else 'unclassified-unavailable'
        if error:
            if 'location searched: crates.io index' in error:
                category = 'registry-dependency-unavailable'
            elif 'the option `Z` is only accepted on the nightly compiler' in error:
                category = 'original-nightly-flags-refused-by-stable-compiler'
            elif 'location searched:' in error and error.startswith('no matching package named `'):
                category = 'original-local-package-name-mismatch'
            elif 'failed to get' in error and ('git' in error or 'https://github.com' in error):
                category = 'original-git-dependency-unavailable'
            elif error.startswith('cannot update the lock file '):
                category = 'original-lock-update-refused'
            elif 'No such file or directory' in error:
                category = 'original-generated-or-path-input-unavailable'
        outcomes[category] += 1
assert collectors == 13 and queries == 43 and graphs == 0
for name in ['census.json', 'cargo-manifest-roles-r1.json', 'owned-corpus-copies-r1.json', 'original-workspace-entries-r1.json', 'smithy-local-package-mismatch-classification-r2.json']:
    copy(V / name, 'census/' + name)
for name in ['owned-original-inputs-r1.json', 'original-context-census-r1.json']:
    copy(B / 'sm-sui-original-inputs-2026-10-10' / name, 'sui-census/' + name)
for name in names:
    runner = 'run_sm_' + name.removesuffix('.json') + '.py'
    if (B / runner).exists():
        copy(B / runner, 'runners/' + runner)
for stem in ['sm-large-context-controls-r1', 'sm-original-rustflags-controls-r1', 'sm-original-config-hierarchy-controls-r1']:
    for name in ['subject.json', 'source.json', 'integration.json']:
        copy(B / (stem + '-stage') / name, 'closed-support/' + stem + '/' + name)
    for name in ['review.json', 'REVIEW.md']:
        copy(B / 'reviews' / ('grok-' + stem) / name, 'closed-support/' + stem + '/' + name)
(D / 'external-input-pins.json').write_text(json.dumps(dict(files=[external[k] for k in sorted(external)]), indent=2) + '\n')
report = dict(unit='SM-ACTUAL-LARGE-WORKSPACE-DATA-r4', standing='UNREVIEWED RETAINED ORIGINAL LARGE WORKSPACE STATIC GRAPH DATA; NOT SELF-CONTAINED',
              actualCollectorRoots=collectors, compilerInformationQueries=queries, successfulGraphs=graphs,
              unsuccessfulGraphs=collectors-graphs, declaredOriginalWorkspaceEntries=33,
              originalPlannedWorkloads=4, actualObservedWorkloads=3, outcomeCategories=dict(outcomes), receiptPins=receipts,
              externalWholePinnedFiles=len(external), originalConfigurationsPreserved=True,
              earlierUnrelatedFailuresNotReplayed=True, originalLockBytePinsPreserved=True, successfulStaticGraphsRemainSeparateFromTypechecks=True,
              newCompilerSource=False, controlsRerun=False, typecheckExecuted=False,
              applicationExecuted=False, aliasExecuted=False, buildScriptOrProcMacroExecuted=False,
              fullWorkloadCoverage=False, fullCargoProfileEnvironment=False, sourceAuthentication=False,
              nativeAdmission=False, physicalPeakScratchMeasured=False, completeStatisticalSet=False,
              SMComplete=False, effectiveL=False, productQualification=False, entirePlanComplete=False)
(D / 'draft-source.json').write_text(json.dumps(report, indent=2) + '\n')
(D / 'REPORT.md').write_text("Original large workspace static graph data, fourth retained set\n\nThree newsets contain13 collector roots and43 compiler information queries. Zero staticgraphs completed; all13 raw outcomes retained. Actual observedworkloads areSmithy,Deno andSui: threeofthefourplanned large workloads. Original33 declaredworkspaceentries do notestablish fullcoverage. DenoSQLite proceeds toamissing proc-macro2 archiveafterretained dependencyinputschange; thediagnostic remains anincomplete result. Originalsource/config/lockpins preserved; nolockrepair or --locked relaxation. Previouslysuccessfulgraphs andunchangedlock/nightly/Git/local/generatedfailures notrerun.\n\nRawpacket/queryargv/environment/output/outcome andlockobservations archived. Ownedpublicinput source andcumulative rawregistrybytes remain explicitlyexternal,whole-pinned andfreshlyno-follow/stable-fstat hashed. Notself-contained. No typechecking/application/alias/script/procmacro orsourceauthentication/native/physicalpeak/fullSM/effectiveL/qualification inference. Closedsupportcontrolsubjects remainclosed. Exactindependentreview/ownassent/freshverification required before architecture-onlypublication. Product/lock unchanged,no push.\n")
copy(Path(__file__), 'runners/' + Path(__file__).name)
shutil.copytree(D, C / 'continuation-preserved' / D.name)
print(json.dumps({k:v for k,v in report.items() if isinstance(v,(str,int,bool))}, indent=2))
assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
