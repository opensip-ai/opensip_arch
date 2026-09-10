"""Round two: every altered payload is retained under its OWN correct digest and
every referencing field is honestly repointed, so the store re-hash check cannot
fire. Any refusal here comes from the semantic law itself. Also exercises cache
lookup-key construction vs cache HIT admission, stage-spec identity across
execution/cache/regeneration, and legitimate miss/mismatch behaviour."""
import copy, hashlib, json, sys
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v7/docs/coop/design-corrections')
FOUND = SUB / 'foundation'
src = (FOUND / 'check-identity.py').read_text()
G = {'__file__': str(FOUND / 'check-identity.py'), '__name__': 'subject_fixtures'}
exec(compile(src[:src.index('a=argparse.ArgumentParser()')], str(FOUND / 'check-identity.py'), 'exec'), G)
M, C, N = G['M'], G['C'], G['N']
build, rekey, rekey_plan = G['build'], G['rekey'], G['rekey_plan']
R = {}

def attempt(fn):
    try:
        return {'admitted': True, 'value': str(fn())[:90]}
    except Exception as e:
        return {'admitted': False, 'error': type(e).__name__ + ':' + str(e)[:200]}

def fresh(**kw):
    r, o, b = build(**kw)
    return copy.deepcopy(r), copy.deepcopy(o), copy.deepcopy(b)

def put(blobs, raw):
    raw = raw if isinstance(raw, bytes) else C.canonical(raw)
    d = hashlib.sha256(raw).hexdigest(); blobs[d] = raw; return d

def ctx_of(run, objects, blobs, lang):
    want = 'native.context.%s.v2' % lang
    for d in objects[run['planId']][1]['nativeContextDigests']:
        if M.parse_h_frame(blobs[d], 'native-context')[0] == want:
            return d
    raise AssertionError(lang)

B = {}

# ---- B1 schema-VALID but admission-refused TS context, honestly re-framed and repointed.
# This is the "a frame proves retention, never admission" rule, reproduced independently.
run, objects, blobs = fresh(has_match=True)
old = ctx_of(run, objects, blobs, 'typescript')
_, ctx, _ = M.parse_h_frame(blobs[old], 'native-context')
alt = copy.deepcopy(ctx)
others = [m for m in ['node16', 'nodenext', 'bundler', 'node10', 'classic']
          if m != ctx['moduleResolutionMode']]
alt['moduleResolutionMode'] = others[0]
new = M.retain_h_identity('native.context.typescript.v2', alt, blobs)
# repoint the universe at the new context and re-frame it, then repoint the scope, then the Plan
scope_key = next(k for k, (d, v) in objects.items() if d == 'subject-scope')
scope = copy.deepcopy(objects[scope_key][1])
_, uni, _ = M.parse_h_frame(blobs[scope['sourceUniverse']], 'native-semantic-universe')
uni2 = {**copy.deepcopy(uni), 'nativeContextId': 'sha256:' + new}
newu = M.retain_h_identity('native.semantic-universe.typescript.v2', uni2, blobs)
scope['sourceUniverse'] = scope['targetUniverse'] = newu
rekey(objects, scope_key, scope, run)
plan = copy.deepcopy(objects[run['planId']][1])
plan['nativeContextDigests'] = sorted(set(plan['nativeContextDigests']) - {old} | {new})
rekey_plan(objects, blobs, run, plan)
B['B1_schemaValidButAdmissionRefusedTsContext'] = attempt(lambda: M.close_run(run, objects, blobs))
B['B1_note'] = ('the altered context is a well-formed, correctly-hashed frame of its registered '
                'record; only re-running admit_native_context can refuse it')

# ---- B2 raw canonical payload retained under its OWN sha and the Plan repointed at it
run, objects, blobs = fresh(has_match=True)
old = ctx_of(run, objects, blobs, 'typescript')
_, ctx, _ = M.parse_h_frame(blobs[old], 'native-context')
rawd = put(blobs, C.canonical(ctx))
plan = copy.deepcopy(objects[run['planId']][1])
plan['nativeContextDigests'] = sorted(set(plan['nativeContextDigests']) - {old} | {rawd})
rekey_plan(objects, blobs, run, plan)
B['B2_rawPayloadUnderItsOwnShaWhereFrameRequired'] = attempt(lambda: M.close_run(run, objects, blobs))

# ---- B3 an H FRAME offered where a canonical-record digest is required
run, objects, blobs = fresh(has_match=True)
plan = copy.deepcopy(objects[run['planId']][1])
spec = C.parse(blobs[plan['analysisSpecDigest']])
framed = M.h_preimage_frame('native.context.typescript.v2', spec)
plan['analysisSpecDigest'] = put(blobs, framed)
rekey_plan(objects, blobs, run, plan)
B['B3_frameWhereCanonicalRecordRequired'] = attempt(lambda: M.close_run(run, objects, blobs))

# ---- B4 well-formed but WRONG-SCHEMA record under its own correct digest
run, objects, blobs = fresh(has_match=True)
plan = copy.deepcopy(objects[run['planId']][1])
plan['analysisSpecDigest'] = put(blobs, {'schemaVersion': 2, 'notAnAnalysisSpec': True})
rekey_plan(objects, blobs, run, plan)
B['B4_wrongSchemaRecordUnderItsOwnDigest'] = attempt(lambda: M.close_run(run, objects, blobs))

# ---- B5 altered source bytes, inventory row honestly updated, snapshot re-minted
run, objects, blobs = fresh(has_match=True)
snap = copy.deepcopy(objects[run['snapshotId']][1])
newbytes = b'ALTERED SOURCE\n'
snap['sourceInventory'] = sorted(
    [dict(r, sha256=put(blobs, newbytes), bytes=len(newbytes)) if r['path'] == 'a.ts' else r
     for r in snap['sourceInventory']], key=lambda r: r['path'].encode())
rekey(objects, run['snapshotId'], snap, run)
B['B5_alteredSourceHonestlyReInventoried'] = attempt(lambda: M.close_run(run, objects, blobs))
B['B5_note'] = 'vcs-observation.sourceInventoryDigest still names the ORIGINAL inventory'

# ---- B6 altered resolved config retained honestly; snapshot and Plan both repointed
run, objects, blobs = fresh(has_match=True)
newcfg = put(blobs, {'analysis': {'profileId': 'attacker', 'capabilities': ['references'],
                                  'budget': {'unit': 'work-units', 'limit': 1000}},
                     'components': {}, 'discovery': {}, 'policy': {}, 'evidence': {}})
plan = copy.deepcopy(objects[run['planId']][1]); plan['resolvedConfigDigest'] = newcfg
rekey_plan(objects, blobs, run, plan)
B['B6_planConfigDivergesFromSnapshot'] = attempt(lambda: M.close_run(run, objects, blobs))

# ---- B7 a foreign (other-snapshot) native context frame added to this Plan
run, objects, blobs = fresh(has_match=True)
r2, o2, b2 = fresh(has_match=True, stdlib_body=b'declare const es2022: string;\n')
foreign = ctx_of(r2, o2, b2, 'typescript')
blobs.update(b2); objects.update({k: v for k, v in o2.items() if v[0] == 'closure'})
plan = copy.deepcopy(objects[run['planId']][1])
plan['nativeContextDigests'] = sorted(set(plan['nativeContextDigests']) | {foreign})
rekey_plan(objects, blobs, run, plan)
B['B7_foreignContextAddedToPlan'] = attempt(lambda: M.close_run(run, objects, blobs))

# ---- B8 a Plan naming a context that is not retained at all
run, objects, blobs = fresh(has_match=True)
plan = copy.deepcopy(objects[run['planId']][1])
plan['nativeContextDigests'] = sorted(set(plan['nativeContextDigests']) | {'e' * 64})
rekey_plan(objects, blobs, run, plan)
B['B8_planNamesUnretainedContext'] = attempt(lambda: M.close_run(run, objects, blobs))

# ---- B9 Rust: dependency file-manifest member blob length lie
run, objects, blobs = fresh(has_match=True, universe_language='rust')
rd = ctx_of(run, objects, blobs, 'rust')
_, rctx, _ = M.parse_h_frame(blobs[rd], 'native-context')
depid = rctx['dependencySourceSetId'].removeprefix('sha256:')
_, dep, _ = M.parse_h_frame(blobs[depid], 'native-nested')
mid = dep['packages'][0]['fileManifestSha256']
_, man, _ = M.parse_h_frame(blobs[mid], 'native-nested')
row = man[0]
blobs[row['contentSha256']] = b'x' * (row['byteLength'] + 5)   # wrong length AND wrong bytes
B['B9_dependencyMemberBytesTampered'] = attempt(lambda: M.close_run(run, objects, blobs))

# ---- B10 Rust: configProjection projected-file bytes not retained
run, objects, blobs = fresh(has_match=True, universe_language='rust')
rd = ctx_of(run, objects, blobs, 'rust')
_, rctx, _ = M.parse_h_frame(blobs[rd], 'native-context')
blobs.pop(rctx['configProjection']['projectionSha256'], None)
B['B10_rustProjectedConfigBytesMissing'] = attempt(lambda: M.close_run(run, objects, blobs))

# ---- B11 Rust: configProjectionSha256 replaced by the RAW projection file sha (H vs raw confusion)
run, objects, blobs = fresh(has_match=True, universe_language='rust')
rd = ctx_of(run, objects, blobs, 'rust')
_, rctx, _ = M.parse_h_frame(blobs[rd], 'native-context')
scope_key = next(k for k, (d, v) in objects.items() if d == 'subject-scope')
scope = copy.deepcopy(objects[scope_key][1])
_, uni, _ = M.parse_h_frame(blobs[scope['sourceUniverse']], 'native-semantic-universe')
u2 = {**copy.deepcopy(uni), 'configProjectionSha256': rctx['configProjection']['projectionSha256']}
scope['sourceUniverse'] = scope['targetUniverse'] = M.retain_h_identity(
    'native.semantic-universe.rust.v2', u2, blobs)
rekey(objects, scope_key, scope, run)
B['B11_rustConfigProjectionRawShaSubstituted'] = attempt(lambda: M.close_run(run, objects, blobs))
B['B11_note'] = ('projectionSha256 is raw SHA-256 of the projected .cargo/config.toml file bytes; '
                 'configProjectionSha256 is the H identity of the whole CargoConfigProjectionV2')

# ---- B12 Rust universe whose crateRootPaths name a path outside the snapshot
run, objects, blobs = fresh(has_match=True, universe_language='rust')
scope_key = next(k for k, (d, v) in objects.items() if d == 'subject-scope')
scope = copy.deepcopy(objects[scope_key][1])
_, uni, _ = M.parse_h_frame(blobs[scope['sourceUniverse']], 'native-semantic-universe')
u2 = {**copy.deepcopy(uni), 'crateRootPaths': ['src/not-in-snapshot.rs']}
scope['sourceUniverse'] = scope['targetUniverse'] = M.retain_h_identity(
    'native.semantic-universe.rust.v2', u2, blobs)
rekey(objects, scope_key, scope, run)
B['B12_rustCrateRootNotInventoried'] = attempt(lambda: M.close_run(run, objects, blobs))

R['deepAttacks'] = B

# =====================================================================  cache / regeneration
Kc = {}
run, objects, blobs = fresh(has_match=True)
run_id = M.close_run(run, objects, blobs)
exec_plan = objects[objects[run['evaluationSealId']][1]['executionPlanId']][1]
stage = exec_plan['stages'][0]
spec = C.parse(blobs[stage['stageSpecDigest']])
good = {'schemaVersion': 2, 'planId': run['planId'], 'producerClosure': spec['producerClosure'],
        'stageSpecDigest': stage['stageSpecDigest'], 'scopeIds': sorted(
            [k for k, (d, v) in objects.items() if d == 'subject-scope']),
        'inputRefs': [], 'outputSchemaDigest': spec['outputSchemaDigest']}

# lookup-key construction is PURE: same key, no store, both domains, stable
Kc['keyIsPureAndDeterministic'] = (M.cache_key('cache-key', good) == M.cache_key('cache-key', good))
Kc['cacheAndRegenDifferOnlyByDomain'] = (M.cache_key('cache-key', good)
                                         != M.cache_key('regeneration-key', good))
Kc['cachePrefix'] = M.cache_key('cache-key', good).split(':')[0]
Kc['regenPrefix'] = M.cache_key('regeneration-key', good).split(':')[0]
Kc['unregisteredDomainRefused'] = attempt(lambda: M.cache_key('run', good))
# a key can be CONSTRUCTED for a stage that does not exist -> construction grants nothing
bogus = {**good, 'stageSpecDigest': 'b' * 64}
Kc['keyConstructsForNonexistentStage'] = attempt(lambda: M.cache_key('cache-key', bogus))
Kc['butHitAdmissionRefusesIt'] = attempt(
    lambda: M.admit_cache_entry('cache-key', bogus, run, objects, blobs))
# honest HIT
Kc['legitimateHit'] = attempt(lambda: M.admit_cache_entry('cache-key', good, run, objects, blobs))
Kc['legitimateRegenHit'] = attempt(
    lambda: M.admit_cache_entry('regeneration-key', good, run, objects, blobs))
Kc['hitGrantsNoEvidenceAuthority'] = M.admit_cache_entry(
    'cache-key', good, run, objects, blobs)['grantsEvidenceAuthority'] is False
# the SAME stage-spec record is used by execution plan and cache key
Kc['stageSpecIsTheSameRecordInBothPlaces'] = (
    M.admit_cache_entry('cache-key', good, run, objects, blobs)['stageSpec']
    == C.parse(blobs[stage['stageSpecDigest']]))
# caller invents an output schema for a reused stage
Kc['inventedOutputSchema'] = attempt(lambda: M.admit_cache_entry(
    'cache-key', {**good, 'outputSchemaDigest': put(blobs, b'{"invented":true}')},
    run, objects, blobs))
# caller swaps the producing closure
Kc['swappedProducerClosure'] = attempt(lambda: M.admit_cache_entry(
    'cache-key', {**good, 'producerClosure': 'closure2:' + 'c' * 64}, run, objects, blobs))
# cross-Plan key
r2, o2, b2 = fresh(has_match=True, source_path='other.ts')
Kc['crossPlanKey'] = attempt(lambda: M.admit_cache_entry(
    'cache-key', {**good, 'planId': r2['planId']}, run, objects, blobs))
# a foreign scope
foreign_scope = next(k for k, (d, v) in o2.items() if d == 'subject-scope')
o3 = dict(objects); o3[foreign_scope] = o2[foreign_scope]; b3 = {**blobs, **b2}
Kc['foreignScopeInKey'] = attempt(lambda: M.admit_cache_entry(
    'cache-key', {**good, 'scopeIds': sorted(good['scopeIds'] + [foreign_scope])}, run, o3, b3))
# a payload-domain reference offered as an authoritative consumed input
Kc['payloadDomainRefAsRoot'] = attempt(lambda: M.admit_cache_entry(
    'cache-key', {**good, 'inputRefs': [{'domain': 'fact-payload', 'digest': 'a' * 64}]},
    run, objects, blobs))
# a native context input ref that this Plan did not select
Kc['unselectedContextInputRef'] = attempt(lambda: M.admit_cache_entry(
    'cache-key', {**good, 'inputRefs': [{'domain': 'native-context', 'digest': 'd' * 64}]},
    run, objects, blobs))
# a legitimate MISS: the key simply does not match any stage; construction still succeeds
Kc['missIsNotAFailure'] = (isinstance(M.cache_key('cache-key', bogus), str)
                           and not Kc['butHitAdmissionRefusesIt']['admitted'])
R['cache'] = Kc

R['summary'] = {
    'deepAttacksAllRefused': all(v['admitted'] is False for k, v in B.items()
                                 if isinstance(v, dict) and 'admitted' in v),
    'deepAttacksAdmitted': [k for k, v in B.items()
                            if isinstance(v, dict) and v.get('admitted')],
    'cacheNegativesAllRefused': all(
        v['admitted'] is False for k, v in Kc.items()
        if isinstance(v, dict) and 'admitted' in v
        and k not in ('legitimateHit', 'legitimateRegenHit', 'keyConstructsForNonexistentStage')),
    'legitimateHitsAdmitted': Kc['legitimateHit']['admitted'] and Kc['legitimateRegenHit']['admitted'],
}
print(json.dumps(R, indent=1, default=str))
json.dump(R, open(sys.argv[1], 'w'), indent=1, default=str)
