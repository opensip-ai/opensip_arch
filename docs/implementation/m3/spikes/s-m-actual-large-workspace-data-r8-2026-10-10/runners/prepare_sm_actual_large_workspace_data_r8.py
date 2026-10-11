from pathlib import Path
import os, stat, json, hashlib, shutil, collections

os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-large-original-context-census-2026-10-10'
D = B / 'sm-actual-large-workspace-data-r8-draft'
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

names = ['actual-other-large-workspace-attempts-r13.json', 'actual-smithy-original-workspace-attempts-r12.json']

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
            elif 'target resolution error' in error and b"can't find bin" in (root / 'stderr.log').read_bytes():
                category = 'original-nonregular-source-target-unavailable'
        outcomes[category] += 1
assert collectors == 2 and queries == 9 and graphs == 2

# Lock-derived mixed-case public intake r13 (reviewed SM-PUBLIC-INTAKE-MIXED-CASE-r1 entry): receipts copied, bytes pinned externally.
intake_index_names = set(); intake_archives = 0
receipt = json.loads(checked(V / 'missing-public-index-inputs-deno-smithy-r13' / 'receipt.json')[0]); copy(V / 'missing-public-index-inputs-deno-smithy-r13' / 'receipt.json', 'intake/missing-public-index-inputs-deno-smithy-r13/receipt.json')
for row in receipt['inputs']:
    if row['path'] not in external:
        _, external[row['path']] = checked(Path(row['path']), row)
    intake_index_names.add(row['name'])
for directory in ['missing-public-archive-inputs-deno-smithy-r13', 'missing-public-archive-inputs-deno-smithy-r13-retry1']:
    copy(V / directory / 'receipt.json', 'intake/' + directory + '/receipt.json')
for name in ['deno-smithy-public-intake-packet-r13.json', 'deno-smithy-mixed-case-public-intake-r13.json', 'other-large-supplemental-registry-template-r13.json', 'other-large-workspace-retry-packets-r13.json', 'smithy-workspace-retry-packets-r12.json']:
    copy(V / name, 'intake/' + name)
copy(B / 'sm-framed-bin-profile-2026-10-10/actual-deno-root-smithy-runtime-source-maps-r1.json', 'maps/actual-deno-root-smithy-runtime-source-maps-r1.json')
intake_archives = json.loads((V / 'deno-smithy-mixed-case-public-intake-r13.json').read_bytes())['outcome']['intake']['archives']
assert intake_archives == 20263
for script in ['prepare_sm_deno_smithy_missing_public_indexes_r13.py', 'prepare_sm_deno_smithy_missing_public_archives_r13.py', 'retry_sm_deno_smithy_public_archives_r13.py', 'prepare_sm_deno_smithy_public_cache_intake_packet_r13.py', 'run_sm_deno_smithy_public_cache_intake_r13.py', 'prepare_sm_other_large_supplemental_registry_template_r13.py', 'prepare_sm_other_large_workspace_retry_packets_r13.py', 'prepare_sm_smithy_workspace_retry_packets_r12.py', 'prepare_sm_actual_deno_root_smithy_runtime_source_maps_r1.py']:
    copy(B / script, 'intake-runners/' + script)
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
report = dict(unit='SM-ACTUAL-LARGE-WORKSPACE-DATA-r8', standing='UNREVIEWED RETAINED ORIGINAL LARGE WORKSPACE STATIC GRAPH DATA; NOT SELF-CONTAINED',
              actualCollectorRoots=collectors, compilerInformationQueries=queries, successfulGraphs=graphs,
              unsuccessfulGraphs=collectors-graphs, declaredOriginalWorkspaceEntries=33,
              originalPlannedWorkloads=4, actualObservedWorkloads=3, lockDerivedPublicIntakeRounds=1, mixedCaseIntakeVariantUsed=True, sourceMapDescriptorsOverClosedBound=2, denoRootDescriptorBytes=22825382, smithyRuntimeDescriptorBytes=5115131, lockDerivedIndexedNames=len(intake_index_names), lockDerivedVersionArchivesIntaken=intake_archives, closedIntakeMixedCaseNameGaps=[], lockDerivedNamesLeadDecision=True, outcomeCategories=dict(outcomes), receiptPins=receipts,
              externalWholePinnedFiles=len(external), originalConfigurationsPreserved=True,
              earlierUnrelatedFailuresNotReplayed=True, originalLockBytePinsPreserved=True, successfulStaticGraphsRemainSeparateFromTypechecks=True,
              newCompilerSource=False, controlsRerun=False, typecheckExecuted=False,
              applicationExecuted=False, aliasExecuted=False, buildScriptOrProcMacroExecuted=False,
              fullWorkloadCoverage=False, fullCargoProfileEnvironment=False, sourceAuthentication=False,
              nativeAdmission=False, physicalPeakScratchMeasured=False, completeStatisticalSet=False,
              SMComplete=False, effectiveL=False, productQualification=False, entirePlanComplete=False)
(D / 'draft-source.json').write_text(json.dumps(report, indent=2) + '\n')
(D / 'REPORT.md').write_text("""Original large workspace static graph data, eighth retained set

Two new receipts contain 2 collector roots and 9 compiler information queries; both produce static graphs: the original Deno root workspace (ordinal 25, 1800 units, 78 roots) and original Smithy `rust-runtime` (ordinal 7, 442 units, 30 roots).

They needed the mixed-case crates.io name `Inflector`, which the closed intake cannot admit. The separately reviewed mixed-case intake variant admitted one lock-derived round (lead decision: names from each entry's original pinned Cargo.lock): 402 indexes and 20263 whole-checksummed archives, with transient HTTP 500 failures retried and original failure receipts retained. The Deno root's 401 lowercase names reused the retained, pinned r11 index files.

Source maps for both graphs were computed before launch: the Deno root descriptor is 22825382 bytes (76424 rows) and Smithy `rust-runtime` 5115131 bytes (17742 rows), both over the closed prototype driver's 4194304-byte bound, so both are unavailable before launch; nothing was trimmed and the bound was not changed. This private absolute-path prototype descriptor is not a canonical native snapshot descriptor and neither shows nor refutes a native bound outcome.

Static graphs are not typechecks. Raw packets, query argv/environment, outputs, outcomes and lock observations are archived; owned original source, public index/archive bytes and the cumulative registry template stay external, whole-pinned and freshly no-follow/stable-fstat hashed. Not self-contained. No application/alias/script/proc-macro execution, source authentication, native admission, physical peak, full S-M, effective L or qualification inference. Exact independent review, own assent and fresh verification are required before architecture-only publication. Product/lock unchanged, no push.
""")
copy(Path(__file__), 'runners/' + Path(__file__).name)
shutil.copytree(D, C / 'continuation-preserved' / D.name)
print(json.dumps({k:v for k,v in report.items() if isinstance(v,(str,int,bool))}, indent=2))
assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
