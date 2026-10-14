from pathlib import Path
import json, hashlib, difflib, re
# Read-only audit of U-1 (S-M report plan PLAN-r3, D-5): build-script-outputs-absent producer variant, static-profile
# executor variant and SM-4 coverage series. Writes u1-checks-r1.json beside itself.
V = Path(__file__).resolve().parent; B = Path('/tmp/opensip-implementation'); A = Path('/Users/sb/code/opensip-ai/opensip_arch')
SP = A / 'docs/implementation/m3/spikes/s-m-actual-static-profile-series-2026-10-10'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def changed(a, b):
    return [l for l in difflib.unified_diff(Path(a).read_text().splitlines(), Path(b).read_text().splitlines(), lineterm='', n=0) if l[:1] in '+-' and not l.startswith(('+++', '---'))]
# 1. Producer variant: only the two named files differ from the accepted producer (the parent copies were taken before editing).
ACC = B / 'sm-command-data-2026-10-10/producer'; VAR = V / 'producer'
stage_changed = B / 'sm-command-data-controls-r1-stage/changed-source'
for rel in ['src/cargo/core/compiler/experimental_command_data.rs', 'src/cargo/util/context/experimental_command_data.rs']:
    assert sha(ACC / rel) == sha(stage_changed / rel), rel  # the accepted producer still equals its accepted changed-source copy
assert sha(V / 'parent-experimental_command_data.rs') == sha(ACC / 'src/cargo/core/compiler/experimental_command_data.rs')
assert sha(V / 'parent-util-context-experimental_command_data.rs') == sha(ACC / 'src/cargo/util/context/experimental_command_data.rs')
producer_diff = changed(ACC / 'src/cargo/core/compiler/experimental_command_data.rs', VAR / 'src/cargo/core/compiler/experimental_command_data.rs')
control_diff = changed(ACC / 'src/cargo/util/context/experimental_command_data.rs', VAR / 'src/cargo/util/context/experimental_command_data.rs')
assert all(l.startswith('+') for l in control_diff)  # the control file only gains the new test
other = []
for p in sorted(ACC.rglob('*')):
    if p.is_file() and '/target/' not in str(p):
        q = VAR / p.relative_to(ACC)
        if not q.is_file() or sha(p) != sha(q): other.append(p.relative_to(ACC).as_posix())
assert sorted(other) == sorted(['src/cargo/core/compiler/experimental_command_data.rs', 'src/cargo/util/context/experimental_command_data.rs']), other
chk = json.loads((V / 'command-data-bsabsent-checks-r1.json').read_text()); assert chk['exitCode'] == 0
log = (V / 'command-data-bsabsent-controls-r1.log').read_text(); assert 'test result: ok. 4 passed; 0 failed' in log and 'command_data_build_script_only_consumer_constructed_with_outputs_absent ... ok' in log
img = json.loads((V / 'variant-image.json').read_text()); assert sha(img['path']) == img['sha256']
acc_img = json.loads((SP / 'source.json').read_text())['closedCargoImage']; assert sha(acc_img['path']) == acc_img['sha256']  # accepted image untouched
# 2. Collection: nine successful graphs; graphs equal the accepted ones modulo each packet's root; command data equal for every
#    previously constructed unit (modulo root); every newly constructed unit was blocked only via build scripts, OUT_DIR removed.
att = json.loads((V / 'bsabsent-command-data-attempts-r1.json').read_text()); acc_att = json.loads((B / 'sm-experimental-dependency-preparation-2026-10-10/actual-command-data-attempts-r1.json').read_text())
entries = []
for r, o in zip(att['results'], acc_att['results']):
    assert r['ordinal'] == o['ordinal'] and r['outcome']['success'] and r['rootObservationInformational']['returncode'] == 0
    # Normalise each packet root and each producer image directory (CARGO env names the image that constructed the data).
    norm = lambda path, root: Path(path).read_text().replace(root, '<ROOT>').replace('/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/check-target', '<IMAGE>').replace('/tmp/opensip-implementation/sm-command-data-2026-10-10/check-target', '<IMAGE>')
    assert norm(r['graph']['path'], r['packet']['root']) == norm(o['graph']['path'], o['packet']['root'])
    cv = json.loads(norm(r['unitCommandData']['path'], r['packet']['root'])); co = json.loads(norm(o['unitCommandData']['path'], o['packet']['root']))
    same = 0; new = []
    for a, b in zip(cv['units'], co['units']):
        if b['staticCargoCommandConstructed']:
            a2 = {k: v for k, v in a.items() if k != 'buildScriptOutputsAbsent'}; assert a2 == b and a['buildScriptOutputsAbsent'] is False, (r['ordinal'], a['index']); same += 1
        elif a['staticCargoCommandConstructed']:
            assert a['standing'] == 'actual-static-cargo-command-data-build-script-outputs-absent' and a['buildScriptOutputsAbsent'] is True and 'OUT_DIR' not in a['constructedEnvironment']
            new.append(dict(index=a['index'], name=a['target']['name'], firstParty=a['packageId'].startswith('path+'), outDirRemoved='OUT_DIR' in a['removedEnvironmentKeys']))
        else: assert a == b, (r['ordinal'], a['index'])
    entries.append(dict(ordinal=r['ordinal'], id=r['id'], graphEqualModuloRoot=True, previouslyConstructedUnchanged=same, newlyConstructed=new))
maps = json.loads((V / 'bsabsent-command-source-maps-r1.json').read_text()); acc_maps = json.loads((B / 'sm-command-data-2026-10-10/actual-command-source-maps-r1.json').read_text())
for m, o in zip(maps['results'], acc_maps['results']):
    assert m['preparedFiles'] == o['preparedFiles'] and m['sourceContentBytes'] == o['sourceContentBytes'] and sha(m['sourceMap']['path']) == m['sourceMap']['sha256']
# 3. Executor variants: diffs confined to the five build-script-edge sites and the recorded flag.
def exec_diff(parent, variant):
    d = changed(parent, variant); allowed = ('bs=', "parsed[i]=parse_static_arguments(row,dict(u,dependencies=", "for d in deps", "index(d['index'])", "if d['index'] not in bs", "for d in [d for d in u['dependencies'] if d['index'] not in bs]", "record=dict(buildScriptOutputsAbsent", '#', "for d in u['dependencies']:", "parsed[i]=parse_static_arguments(row,u)", "record=dict(index=i")
    bad = [l for l in d if not any(x in l for x in allowed)]; assert not bad, bad; return d
sp_diff = exec_diff(B / 'sm-command-data-2026-10-10/cargo_lint_spelling_graph_execution.py', V / 'cargo_lint_spelling_graph_execution_bsabsent.py')
fr_diff = exec_diff(B / 'sm-framed-analysis-2026-10-10/framed_profile_graph_execution.py', V / 'framed_profile_graph_execution_bsabsent.py')
# 4. The SM-4 coverage series (static-profile path).
ser = json.loads((V / 'bsabsent-static-profile-series-r1.json').read_text()); assert ser['executorPin']['sha256'] == sha(V / 'cargo_lint_spelling_graph_execution_bsabsent.py')
rows = []
for s, e in zip(ser['series'], entries):
    assert s['ordinal'] == e['ordinal'] and s['populationRepeated'] and s['readSetsRepeated'] and s['metadataRepeatForEveryAnalyzedUnit'] and s['acceptedAnalysedUnitsStillAnalysed']
    rows.append(dict(ordinal=s['ordinal'], id=s['id'], analysedUnits=s['analysedUnits'], incompleteUnits=len(s['incompleteUnits']), childrenPerRun=s['compilerChildren'] // 10,
                     newlyAnalysed=s['newlyAnalysedUnits'], newlyConstructedCommands=e['newlyConstructed'],
                     medianWholeGraphMs=s['medianWholeGraphNanos'] / 1e6, maxWholeGraphMs=s['maxWholeGraphNanos'] / 1e6, acceptedStaticProfileMedianMs=s['acceptedMedianWholeGraphNanos'] / 1e6))
result = dict(standing='UNREVIEWED READONLY AUDIT OF U-1 (PLAN-r3 D-5): BUILD-SCRIPT-OUTPUTS-ABSENT PRODUCER AND EXECUTOR VARIANTS AND SM-4 COVERAGE SERIES; LEAD macOS PRELIMINARY',
              producerVariant=dict(image=img, otherFilesUnchanged=True, filterDiff=producer_diff, controlFileOnlyAddsTest=True, controlsPassed=4), acceptedProducerAndImageUnchanged=True,
              collection=entries, sourceMapsEqualAcceptedCounts=True, staticProfileExecutorDiff=sp_diff, framedExecutorDiff=fr_diff,
              metadataEmbedsPacketRoot='each metadata file embeds its packet registry root path (54 times in hyper; the variant root is 9 bytes longer, matching the 486-byte size difference), so byte equality with the accepted series is impossible by construction',
              series=rows, wholeGraphIncludesChildStartAndBookkeeping=True, buildScriptOrProcMacroExecuted=False, SM4ValueRecorded=False, FComputed=False, TComputed=False, outcomeRecorded=False, SMComplete=False, LG1Met=False, effectiveL=False)
(V / 'u1-checks-r1.json').write_text(json.dumps(result, indent=1) + '\n')
for r in rows: print(r['ordinal'], r['id'][:22], r['analysedUnits'], r['incompleteUnits'], round(r['medianWholeGraphMs'], 1), round(r['acceptedStaticProfileMedianMs'], 1), [u['name'] for u in r['newlyAnalysed'] if u['firstParty']])
