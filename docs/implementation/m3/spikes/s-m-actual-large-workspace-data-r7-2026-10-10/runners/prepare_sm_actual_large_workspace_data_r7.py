from pathlib import Path
import os, stat, json, hashlib, shutil, collections

os.setpriority(os.PRIO_PROCESS, 0, 10)
B = Path('/tmp/opensip-implementation')
V = B / 'sm-large-original-context-census-2026-10-10'
D = B / 'sm-actual-large-workspace-data-r7-draft'
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

names = ['actual-other-large-workspace-attempts-r11.json', 'actual-other-large-workspace-attempts-r12.json', 'actual-smithy-original-workspace-attempts-r11.json', 'actual-original-hierarchy-workspace-attempts-r9.json']

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
assert collectors == 12 and queries == 46 and graphs == 8

# Lock-derived public intake evidence (lead decision 2026-10-10): receipts copied, public index/archive bytes whole-pinned externally.
intake_index_names = set(); intake_archives = 0
for directory in ['missing-public-index-inputs-other-large-r11', 'missing-public-index-inputs-other-large-r11-sui', 'missing-public-index-inputs-smithy-hierarchy-r12']:
    receipt = json.loads(checked(V / directory / 'receipt.json')[0]); copy(V / directory / 'receipt.json', 'intake/' + directory + '/receipt.json')
    for row in receipt['inputs']:
        if row['path'] not in external:
            _, external[row['path']] = checked(Path(row['path']), row)
        if directory != 'missing-public-index-inputs-other-large-r11':
            intake_index_names.add(row['name'])
for directory in ['missing-public-archive-inputs-other-large-r11-sui', 'missing-public-archive-inputs-other-large-r11-sui-retry1', 'missing-public-archive-inputs-smithy-hierarchy-r12', 'missing-public-archive-inputs-smithy-hierarchy-r12-retry1']:
    copy(V / directory / 'receipt.json', 'intake/' + directory + '/receipt.json')
for name in ['other-large-public-intake-packet-r11-sui.json', 'other-large-parameterized-public-intake-r11-sui.json', 'smithy-hierarchy-public-intake-packet-r12.json', 'smithy-hierarchy-parameterized-public-intake-r12.json', 'other-large-supplemental-registry-template-r10.json', 'other-large-supplemental-registry-template-r11.json', 'other-large-supplemental-registry-template-r12.json', 'other-large-workspace-retry-packets-r11.json', 'other-large-workspace-retry-packets-r12.json', 'smithy-workspace-retry-packets-r11.json', 'original-hierarchy-workspace-packets-r9.json']:
    if not (D / 'intake' / name).exists():
        copy(V / name, 'intake/' + name)
for name in ['other-large-parameterized-public-intake-r11-sui.json', 'smithy-hierarchy-parameterized-public-intake-r12.json']:
    intake_archives += json.loads((V / name).read_bytes())['outcome']['intake']['archives']
assert intake_archives == 10176 + 8501
for script in ['prepare_sm_other_large_supplemental_registry_template_r10.py', 'prepare_sm_other_large_workspace_retry_packets_r11.py', 'prepare_sm_other_large_missing_public_indexes_r11.py', 'prepare_sm_other_large_missing_public_indexes_r11_sui_subset.py', 'prepare_sm_other_large_missing_public_archives_r11_sui.py', 'retry_sm_other_large_public_archives_r11_sui.py', 'prepare_sm_other_large_public_cache_intake_packet_r11_sui.py', 'run_sm_other_large_public_cache_intake_r11_sui.py', 'prepare_sm_other_large_supplemental_registry_template_r11.py', 'prepare_sm_other_large_workspace_retry_packets_r12.py', 'prepare_sm_smithy_hierarchy_missing_public_indexes_r12.py', 'prepare_sm_smithy_hierarchy_missing_public_archives_r12.py', 'retry_sm_smithy_hierarchy_public_archives_r12.py', 'prepare_sm_smithy_hierarchy_public_cache_intake_packet_r12.py', 'run_sm_smithy_hierarchy_public_cache_intake_r12.py', 'prepare_sm_other_large_supplemental_registry_template_r12.py', 'prepare_sm_smithy_workspace_retry_packets_r11.py', 'prepare_sm_original_hierarchy_workspace_packets_r9.py']:
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
report = dict(unit='SM-ACTUAL-LARGE-WORKSPACE-DATA-r7', standing='UNREVIEWED RETAINED ORIGINAL LARGE WORKSPACE STATIC GRAPH DATA; NOT SELF-CONTAINED',
              actualCollectorRoots=collectors, compilerInformationQueries=queries, successfulGraphs=graphs,
              unsuccessfulGraphs=collectors-graphs, declaredOriginalWorkspaceEntries=33,
              originalPlannedWorkloads=4, actualObservedWorkloads=3, lockDerivedPublicIntakeRounds=2, lockDerivedIndexedNames=len(intake_index_names), lockDerivedVersionArchivesIntaken=intake_archives, closedIntakeMixedCaseNameGaps=['Inflector'], lockDerivedNamesLeadDecision=True, outcomeCategories=dict(outcomes), receiptPins=receipts,
              externalWholePinnedFiles=len(external), originalConfigurationsPreserved=True,
              earlierUnrelatedFailuresNotReplayed=True, originalLockBytePinsPreserved=True, successfulStaticGraphsRemainSeparateFromTypechecks=True,
              newCompilerSource=False, controlsRerun=False, typecheckExecuted=False,
              applicationExecuted=False, aliasExecuted=False, buildScriptOrProcMacroExecuted=False,
              fullWorkloadCoverage=False, fullCargoProfileEnvironment=False, sourceAuthentication=False,
              nativeAdmission=False, physicalPeakScratchMeasured=False, completeStatisticalSet=False,
              SMComplete=False, effectiveL=False, productQualification=False, entirePlanComplete=False)
(D / 'draft-source.json').write_text(json.dumps(report, indent=2) + '\n')
(D / 'REPORT.md').write_text("""Original large workspace static graph data, seventh retained set

Four new receipts contain 12 collector roots and 46 compiler information queries, with 8 successful static graphs and 4 retained unavailable outcomes.

Cargo's offline resolver reports one missing name per attempt, so (lead decision, 2026-10-10) the remaining crates.io names were derived from each failing entry's original pinned Cargo.lock together with the observed diagnostics. Every published version of each name was still acquired anonymously and admitted through the closed intake, which requires the whole version set; no version winner was chosen. Two intake rounds admitted 10176 (Sui Move) and 8501 (Smithy/hierarchy) whole-checksummed archives; transient HTTP 500 failures were retried with the original failure receipts retained. The closed intake admits lowercase names only, so the mixed-case `Inflector` (needed by the Deno root and Smithy `rust-runtime`) stays unavailable; those entries were deferred, not bypassed. The Deno root's other lock-derived names were indexed but not intaken.

Outcomes: Smithy `aws/rust-runtime` and all seven original multi-configuration tool workspaces now produce static graphs. `aws-smithy-fuzz` refuses because its original pinned lock is stale under --locked (no lock repair). Sui Move resolves but declares a bin target whose original source is a symlink excluded by the regular-file no-follow copy. Other-large r11 (crossterm/insta resolved, next dashmap/petgraph) is retained.

Static graphs are not typechecks; analysis series over these graphs are separate scopes. Raw packets, query argv/environment, outputs, outcomes and lock observations are archived; owned original source, public index/archive bytes and cumulative registry templates remain external, whole-pinned and freshly no-follow/stable-fstat hashed. Not self-contained. No application/alias/script/proc-macro execution, source authentication, native admission, physical peak, full S-M, effective L or qualification inference. Exact independent review, own assent and fresh verification are required before architecture-only publication. Product/lock unchanged, no push.
""")
copy(Path(__file__), 'runners/' + Path(__file__).name)
shutil.copytree(D, C / 'continuation-preserved' / D.name)
print(json.dumps({k:v for k,v in report.items() if isinstance(v,(str,int,bool))}, indent=2))
assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
