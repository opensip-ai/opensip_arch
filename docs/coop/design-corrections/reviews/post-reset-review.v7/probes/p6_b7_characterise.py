"""Characterise the one deep attack that was ADMITTED (B7): a second, fully
well-formed TypeScript native context added to plan.nativeContextDigests.
Question: is this an identity/trust break, or a legitimately admissible extra
Plan input? Tests whether the context is really re-admitted, whether its
closures are demanded, whether a genuinely snapshot-foreign context is refused,
whether an unreached retained context is refused, and whether any evidence can
be attributed to the extra context."""
import copy, hashlib, json, sys
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v7/docs/coop/design-corrections')
FOUND = SUB / 'foundation'
src = (FOUND / 'check-identity.py').read_text()
G = {'__file__': str(FOUND / 'check-identity.py'), '__name__': 'subject_fixtures'}
exec(compile(src[:src.index('a=argparse.ArgumentParser()')], str(FOUND / 'check-identity.py'), 'exec'), G)
M, C = G['M'], G['C']
build, rekey_plan = G['build'], G['rekey_plan']

def attempt(fn):
    try: return {'admitted': True, 'value': str(fn())[:80]}
    except Exception as e: return {'admitted': False, 'error': type(e).__name__ + ':' + str(e)[:180]}

def fresh(**kw):
    r, o, b = build(**kw); return copy.deepcopy(r), copy.deepcopy(o), copy.deepcopy(b)

def ts_ctx(run, objects, blobs):
    for d in objects[run['planId']][1]['nativeContextDigests']:
        if M.parse_h_frame(blobs[d], 'native-context')[0] == 'native.context.typescript.v2':
            return d

R = {}

def add_second_ctx(copy_closures=True, extra_blobs=True):
    run, objects, blobs = fresh(has_match=True)
    r2, o2, b2 = fresh(has_match=True, stdlib_body=b'declare const es2022: string;\n')
    foreign = ts_ctx(r2, o2, b2)
    if extra_blobs: blobs.update(b2)
    if copy_closures: objects.update({k: v for k, v in o2.items() if v[0] == 'closure'})
    plan = copy.deepcopy(objects[run['planId']][1])
    plan['nativeContextDigests'] = sorted(set(plan['nativeContextDigests']) | {foreign})
    rekey_plan(objects, blobs, run, plan)
    return run, objects, blobs, foreign

# 1. is the extra context really re-admitted, or waved through?
run, objects, blobs, f = add_second_ctx(copy_closures=False)
R['withoutItsClosures'] = attempt(lambda: M.close_run(run, objects, blobs))
run, objects, blobs, f = add_second_ctx(extra_blobs=False)
R['withoutItsFrameBytes'] = attempt(lambda: M.close_run(run, objects, blobs))
run, objects, blobs, f = add_second_ctx()
R['withEverythingRetained'] = attempt(lambda: M.close_run(run, objects, blobs))

# 2. a genuinely snapshot-FOREIGN context (lockfile digest not in this snapshot)
run, objects, blobs = fresh(has_match=True)
d = ts_ctx(run, objects, blobs)
_, ctx, _ = M.parse_h_frame(blobs[d], 'native-context')
alien = copy.deepcopy(ctx)
alien['lockfileIdentity'] = {**alien['lockfileIdentity'], 'contentSha256': 'a' * 64}
newd = M.retain_h_identity('native.context.typescript.v2', alien, blobs)
plan = copy.deepcopy(objects[run['planId']][1])
plan['nativeContextDigests'] = sorted(set(plan['nativeContextDigests']) | {newd})
rekey_plan(objects, blobs, run, plan)
R['snapshotForeignContext'] = attempt(lambda: M.close_run(run, objects, blobs))

# 3. a context whose configGraphPaths are not inventoried
run, objects, blobs = fresh(has_match=True)
d = ts_ctx(run, objects, blobs)
_, ctx, _ = M.parse_h_frame(blobs[d], 'native-context')
alien = copy.deepcopy(ctx)
alien['configProjection'] = {**alien['configProjection'],
                             'configGraphPaths': ['not/in/snapshot/tsconfig.json']}
newd = M.retain_h_identity('native.context.typescript.v2', alien, blobs)
plan = copy.deepcopy(objects[run['planId']][1])
plan['nativeContextDigests'] = sorted(set(plan['nativeContextDigests']) | {newd})
rekey_plan(objects, blobs, run, plan)
R['contextWithUninventoriedConfigPath'] = attempt(lambda: M.close_run(run, objects, blobs))

# 4. a retained context frame that NO Plan reaches (the contract's stated refusal)
run, objects, blobs = fresh(has_match=True)
r2, o2, b2 = fresh(has_match=True, stdlib_body=b'declare const es2022: string;\n')
blobs.update(b2)
objects.update({k: v for k, v in o2.items() if v[0] == 'closure'})
R['retainedButUnreachedContext'] = attempt(lambda: M.close_run(run, objects, blobs))
R['retainedButUnreachedNote'] = ('the set equality is over contexts REACHED by admission, so an '
                                 'unreferenced CAS blob is simply not an evaluation input')

# 5. can any evidence be attributed to the extra context?
run, objects, blobs, f = add_second_ctx()
M.close_run(run, objects, blobs)
universes = set()
for k, (dom, v) in objects.items():
    if dom in ('fact', 'subject-scope'):
        universes |= {v['sourceUniverse'], v['targetUniverse']}
bound = set()
for u in universes:
    _, uv, _ = M.parse_h_frame(blobs[u], 'native-semantic-universe')
    bound.add(uv['nativeContextId'].removeprefix('sha256:'))
R['extraContextIsBoundByNoUniverse'] = f not in bound
R['universesInEvidence'] = len(universes)
R['contextsBoundByEvidence'] = sorted(bound)
R['extraContextDigest'] = f
R['planSelectedContexts'] = sorted(objects[run['planId']][1]['nativeContextDigests'])

# 6. does the extra context change the Plan identity (so it is not silently equal)?
runA, oA, bA = fresh(has_match=True)
runB, oB, bB, _ = add_second_ctx()
R['planIdentityChanges'] = runA['planId'] != runB['planId']
R['runIdentityChanges'] = (M.close_run(runA, oA, bA) != M.close_run(runB, oB, bB))

print(json.dumps(R, indent=1, default=str))
json.dump(R, open(sys.argv[1], 'w'), indent=1, default=str)
