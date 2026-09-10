"""PROBE: every v5 language-version negative must fail BECAUSE of the new derived projection.

Method, same as v4's: neutralise the enforcement in the loaded model, then re-run each negative. A
negative that still refuses without the join did not reach it and would be false coverage. Each
lambda below is the EXACT mutation check-identity.py ships, not a paraphrase.

Two controls in the other direction are also measured: the no-leak vectors must CLOSE with the
enforcement on (an over-broad projection would refuse them), and the large-workspace vector must
close and stay inside the inherited u8 component bound.
"""
import copy,importlib.util,json,sys
from pathlib import Path
H=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/foundation')
sys.argv=[sys.argv[0]]
spec=importlib.util.spec_from_file_location('chk',H/'check-identity.py')
mod=importlib.util.module_from_spec(spec)
try:spec.loader.exec_module(mod)
except SystemExit:pass
M,C=mod.M,mod.C

def stale(language,**overrides):
    return lambda:mod.clone_mutation_in(language,lambda f,p,b,o,r:p.update(
        bodyIdentity=mod.reframed(p,b,language_version=mod.restated_language_version(f,b,language,**overrides))))

NEGATIVES={
 'rust-compilerVersion':stale('rust',compilerVersion='9.9.9'),
 'rust-compilerBuild':stale('rust',compilerBuild='f'*40),
 'rust-compilerName':stale('rust',compilerName='not-rustc'),
 'rust-dialect':stale('rust',dialect={'edition':2015}),
 'typescript-compilerVersion':stale('typescript',compilerVersion='9.9.9'),
 'typescript-compilerBuild':stale('typescript',compilerBuild='e'*64),
 'mixed-edition-ambiguous':lambda:mod.clone_run_with_universe(
     lambda u:u.update(edition={'fixture-root':2021,'legacy-crate':2015})),
 'empty-edition-absent':lambda:mod.clone_run_with_universe(lambda u:u.update(edition={})),
}
POSITIVES={
 'large-single-edition-workspace':lambda:mod.clone_run_with_universe(
     lambda u:u.update(edition=dict(mod.LARGE_EDITION))),
 'renamed-crate':lambda:mod.clone_run_with_universe(lambda u:u.update(edition={'renamed-crate':2021})),
 'extra-cfg-set':lambda:mod.clone_run_with_universe(lambda u:u.update(cfgSets=sorted(
     u['cfgSets']+[{'cfgSetId':'primary+bench','cfg':sorted(u['cfgSets'][0]['cfg']+['bench'])}],
     key=lambda row:C.canonical(row)))),
}

def measure(cases):
    out={}
    for name,fn in cases.items():
        try:
            value=fn();out[name]='CLOSED'
        except Exception as exc:out[name]=type(exc).__name__+':'+str(exc)[:80]
    return out

before=measure(NEGATIVES);positives=measure(POSITIVES)
# Neutralise ONLY the language-version join: keep every other body-identity component check, so a
# negative that refuses for an unrelated framing reason is still visible.
original=M.body_language_version
M.body_language_version=lambda universe,context,row:{'schemaVersion':1,'languageId':row['language'],
    'compilerName':'x','compilerVersion':'x','compilerBuild':'x','dialect':None}
def patched(payload,blobs,language,**overrides):
    return __import__('hashlib').sha256(C.canonical(
        {'schemaVersion':1,'languageId':language,'compilerName':'x','compilerVersion':'x',
         'compilerBuild':'x','dialect':None})).digest()
restated=mod.restated_language_version
mod.restated_language_version=lambda fact,blobs,language,**overrides:patched(fact,blobs,language)
after=measure(NEGATIVES)
M.body_language_version=original;mod.restated_language_version=restated

frames={}
for language in ('typescript','rust'):
    fact,payload,parts=mod.clone_frame_of(mod.CLONE_RUNS[language])
    frames[language]={'componentBytes':len(parts[4]),'inheritedMaximum':255,
                      'componentLengths':[len(p) for p in parts[:5]],'frameBytes':len(parts[0])+len(parts[5])}
print(json.dumps({
 'standing':'actual Claude coauthor probe; design/reference evidence only, no product qualification',
 'withEnforcement':before,'withoutTheLanguageVersionJoin':after,
 'positiveVectorsWithEnforcement':positives,
 'frameComponentSizes':frames,
 'rootVectorRawMapBytes':len(C.canonical({'edition':mod.LARGE_EDITION})),
 'loadBearing':sorted(n for n in NEGATIVES if before[n]!='CLOSED' and after[n]=='CLOSED'),
 'notLoadBearing':sorted(n for n in NEGATIVES if after[n]!='CLOSED'),
 'positivesThatMustClose':sorted(n for n,v in positives.items() if v!='CLOSED')},indent=1))

# TRUTHFUL LABEL, added after execution: the six STALE-VERSION rows of this run are valid and are
# retained as evidence. The two DIALECT rows are not measured by it: the neutralisation replaced
# body_language_version wholesale, which deletes the very unique-value rule those two cases
# exercise, so the model then disagreed with the fixture's frame and refused at
# BODY_IDENTITY_LANGUAGE_VERSION_JOIN for an unrelated reason. Their "notLoadBearing" rows are an
# artifact of this probe, not a finding. Superseded for those two cases by
# probe-language-version-joins-are-load-bearing.v2.py, which neutralises the no-guess rule into the
# guess a permissive implementation would make (take any value) on BOTH sides. Retained unaltered
# above this line.
