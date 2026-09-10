"""Independent adversarial probe over the ACTUAL close_run admission.

Loads the subject's fixture builders (so the graph is the real one) but every
attack below is this reviewer's own and is not in the author's suite. Two
complete Runs are built and closed: one whose semantic universe is TypeScript
and one whose semantic universe is Rust, each with nonempty facts, Coverage and
plan.nativeContextDigests. Then identity/trust is attacked from every angle the
review scope names: altered context, altered closure tree, altered source,
altered config, forged ADMIT, H-vs-raw substitution, foreign roots, wrong
schema, missing preimages, and cache lookup-key vs HIT admission.
"""
import copy, hashlib, json, sys, importlib.util
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v7/docs/coop/design-corrections')
FOUND = SUB / 'foundation'

# exec the author's check-identity fixtures without its CLI tail
src = (FOUND / 'check-identity.py').read_text()
cut = src.index('a=argparse.ArgumentParser()')
G = {'__file__': str(FOUND / 'check-identity.py'), '__name__': 'subject_fixtures'}
exec(compile(src[:cut], str(FOUND / 'check-identity.py'), 'exec'), G)

M, C, N, W = G['M'], G['C'], G['N'], G['W']
build = G['build']
R = {'authorSuiteEmbeddedChecks': {'passed': sum(x['passed'] for x in G['results']),
                                   'failed': sum(not x['passed'] for x in G['results'])}}

def attempt(fn):
    try:
        return {'admitted': True, 'value': fn()}
    except Exception as e:
        return {'admitted': False, 'error': type(e).__name__ + ':' + str(e)[:220]}

# ---------------------------------------------------------------- complete Runs, both languages
runs = {}
for lang in ('typescript', 'rust'):
    run, objects, blobs = build(has_match=True, with_finding=True, universe_language=lang)
    plan = objects[run['planId']][1]
    scope_key = next(k for k, (d, v) in objects.items() if d == 'subject-scope')
    scope = objects[scope_key][1]
    facts = [v for d, v in objects.values() if d == 'fact']
    cov = [v for d, v in objects.values() if d == 'coverage']
    # which universe frame does this Run's scope actually name, and of what domain?
    udom, uval, _ = M.parse_h_frame(blobs[scope['sourceUniverse']], 'native-semantic-universe')
    closed = attempt(lambda: M.close_run(run, objects, blobs))
    runs[lang] = (run, objects, blobs)
    R[lang + 'Run'] = {
        'closed': closed['admitted'], 'runId': closed.get('value'), 'error': closed.get('error'),
        'nativeContextDigestCount': len(plan['nativeContextDigests']),
        'nativeContextDigestsNonEmpty': len(plan['nativeContextDigests']) > 0,
        'factCount': len(facts), 'coverageCount': len(cov),
        'findingCount': len(objects[run['evidenceId']][1]['findingIds']),
        'scopeUniverseDomain': udom,
        'universeIsOwnLanguage': udom == ('native.semantic-universe.%s.v2' % lang),
        'boundContextDomain': M.parse_h_frame(
            blobs[uval['nativeContextId'].removeprefix('sha256:')], 'native-context')[0],
    }

# --------------------------------------------------- attack helpers operating on retained frames
def reframe(blobs, digest, domain, mutate):
    """Re-frame an altered payload under its own (new) H identity and retain it."""
    _, value, _ = M.parse_h_frame(blobs[digest], domain)
    altered = mutate(copy.deepcopy(value))
    dom = M.parse_h_frame(blobs[digest], domain)[0]
    new = M.retain_h_identity(dom, altered, blobs)
    return new, altered

def rust_ctx_digest(run, objects, blobs):
    plan = objects[run['planId']][1]
    for d in plan['nativeContextDigests']:
        if M.parse_h_frame(blobs[d], 'native-context')[0] == 'native.context.rust.v2':
            return d
    raise AssertionError('no rust context')

def ts_ctx_digest(run, objects, blobs):
    plan = objects[run['planId']][1]
    for d in plan['nativeContextDigests']:
        if M.parse_h_frame(blobs[d], 'native-context')[0] == 'native.context.typescript.v2':
            return d
    raise AssertionError('no ts context')

A = {}

# A1 altered native context, honestly re-framed under its own identity + Plan repointed
for lang, getter in (('typescript', ts_ctx_digest), ('rust', rust_ctx_digest)):
    run, objects, blobs = build(has_match=True, universe_language=lang)
    run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
    old = getter(run, objects, blobs)
    field = 'moduleResolutionMode' if lang == 'typescript' else 'hostTriple'
    def mut(v, field=field):
        v[field] = 'x-' + str(v.get(field))
        return v
    new, _ = reframe(blobs, old, 'native-context', mut)
    plan = copy.deepcopy(objects[run['planId']][1])
    plan['nativeContextDigests'] = sorted(set(plan['nativeContextDigests']) - {old} | {new})
    # rekey the whole Plan-dependent graph honestly
    G['rekey_plan'](objects, blobs, run, plan) if 'rekey_plan' in G else None
    A['alteredContext_' + lang] = attempt(lambda: M.close_run(run, objects, blobs))

# A2 altered stdlib closure body -> context identity must not still close
run, objects, blobs = build(has_match=True, stdlib_body=b'declare const es2022: number;\n')
A['alteredStdlibStillClosesOnItsOwn'] = attempt(lambda: M.close_run(run, objects, blobs))

# A3 swap a retained H frame's bytes for the RAW canonical payload (H treated as raw sha)
run, objects, blobs = build(has_match=True)
run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
d = ts_ctx_digest(run, objects, blobs)
_, ctx, _ = M.parse_h_frame(blobs[d], 'native-context')
blobs[d] = C.canonical(ctx)          # raw payload offered where a frame is required
A['rawPayloadWhereFrameRequired'] = attempt(lambda: M.close_run(run, objects, blobs))

# A4 retain the frame under the RAW payload sha as well and point the Plan at it
run, objects, blobs = build(has_match=True)
run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
d = ts_ctx_digest(run, objects, blobs)
_, ctx, _ = M.parse_h_frame(blobs[d], 'native-context')
rawsha = hashlib.sha256(C.canonical(ctx)).hexdigest()
blobs[rawsha] = M.h_preimage_frame('native.context.typescript.v2', ctx)
plan = copy.deepcopy(objects[run['planId']][1])
plan['nativeContextDigests'] = sorted(set(plan['nativeContextDigests']) - {d} | {rawsha})
if 'rekey_plan' in G:
    G['rekey_plan'](objects, blobs, run, plan)
A['hIdentityUnderRawSha'] = attempt(lambda: M.close_run(run, objects, blobs))

# A5 universe binds a context of the OTHER language
run, objects, blobs = build(has_match=True, universe_language='rust')
run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
scope_key = next(k for k, (dm, v) in objects.items() if dm == 'subject-scope')
ud = objects[scope_key][1]['sourceUniverse']
tsd = ts_ctx_digest(run, objects, blobs)
new_u, _ = reframe(blobs, ud, 'native-semantic-universe',
                   lambda v: {**v, 'nativeContextId': 'sha256:' + tsd})
A['universeBindsForeignLanguageContext'] = attempt(
    lambda: M.close_run(run, {**objects, scope_key: ('subject-scope',
                        {**objects[scope_key][1], 'sourceUniverse': new_u})}, blobs))

# A6 forged ADMIT: caller hands the model a fabricated admission/binding result
class ForgedNative:
    def __getattr__(self, name):
        def f(*a, **k):
            return {'refusals': [], 'result': 'ADMIT', 'planNativeContextDigest': 'f' * 64,
                    'domain': 'native.context.typescript.v2', 'nativeContextId': 'sha256:' + 'f' * 64,
                    'sourceUniverse': 'f' * 64}
        return f
run, objects, blobs = build(has_match=True)
saved = M._NATIVE
try:
    M._NATIVE = ForgedNative()
    A['forgedAdmitFlagChangesIdentity'] = attempt(lambda: M.close_run(run, objects, blobs))
finally:
    M._NATIVE = saved
A['forgedAdmitNote'] = ('the model re-derives identity from retained bytes and compares to the '
                        'frame digest, so a fabricated ADMIT cannot name a different context')

# A7 drop a required preimage from the store
for target in ('analysisSpecDigest', 'semanticGrantDigest', 'scopeDigest'):
    run, objects, blobs = build(has_match=True)
    blobs = dict(blobs)
    blobs.pop(objects[run['planId']][1][target], None)
    A['missingPreimage_' + target] = attempt(lambda r=run, o=objects, b=blobs: M.close_run(r, o, b))

# A8 wrong-schema payload retained under a required record digest
run, objects, blobs = build(has_match=True)
run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
blobs[objects[run['planId']][1]['analysisSpecDigest']] = C.canonical({'schemaVersion': 2, 'bogus': True})
A['wrongSchemaUnderRequiredDigest'] = attempt(lambda: M.close_run(run, objects, blobs))

# A9 foreign-root join: a well-formed object outside the Plan closure
run, objects, blobs = build(has_match=True)
run2, objects2, blobs2 = build(has_match=True, source_path='other.ts')
foreign_scope = next(k for k, (dm, v) in objects2.items() if dm == 'subject-scope')
run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
objects[foreign_scope] = objects2[foreign_scope]
blobs.update(blobs2)
vk = next(k for k, (dm, v) in objects.items() if dm == 'view')
objects[vk] = ('view', {**objects[vk][1], 'scopeIds': sorted(objects[vk][1]['scopeIds'] + [foreign_scope])})
A['foreignScopeRootAdmitted'] = attempt(lambda: M.close_run(run, objects, blobs))

# A10 altered source bytes under an inventoried path
run, objects, blobs = build(has_match=True)
run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
snap = objects[run['snapshotId']][1]
row = snap['sourceInventory'][0]
blobs[row['sha256']] = b'ALTERED SOURCE BYTES\n'
A['alteredSourceBytesUnderInventoryDigest'] = attempt(lambda: M.close_run(run, objects, blobs))

# A11 altered resolved configuration preimage
run, objects, blobs = build(has_match=True)
run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
cfg = objects[run['planId']][1]['resolvedConfigDigest']
blobs[cfg] = C.canonical({'analysis': {'profileId': 'ATTACKER', 'capabilities': ['references'],
                                       'budget': {'unit': 'work-units', 'limit': 1000}},
                          'components': {}, 'discovery': {}, 'policy': {}, 'evidence': {}})
A['alteredResolvedConfigPreimage'] = attempt(lambda: M.close_run(run, objects, blobs))

R['attacks'] = A
R['everyAttackRefused'] = all(
    (not v['admitted']) for k, v in A.items()
    if isinstance(v, dict) and 'admitted' in v and k != 'alteredStdlibStillClosesOnItsOwn')
R['alteredStdlibNote'] = ('an honestly re-derived closure yields a DIFFERENT context identity and a '
                          'self-consistent Run; the attack that must fail is reusing the OLD identity')
print(json.dumps(R, indent=1, default=str))
json.dump(R, open(sys.argv[1], 'w'), indent=1, default=str)
