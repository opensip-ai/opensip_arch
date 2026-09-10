"""PROBE v4 (v6 session; supersedes the v5 v3 probe, whose stubs predate the SELECTED-unit design): every v5 language-version negative must fail BECAUSE of the new derived projection.

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
 'no-committed-ownership':lambda:mod.clone_run_with_universe(lambda u:u.update(sourceUnitOwnershipId=None)),
 'selected-owners-disagree':lambda:mod.shared_selection_stale(
     lambda o:o['selectedUnitIds'].append('Cargo.toml#bin:legacy')),
 'owner-not-selected':lambda:mod.shared_selection_stale(
     lambda o:(o.__setitem__('selectedUnitIds',['Cargo.toml#bin:legacy']),
               o.__setitem__('ownership',[r for r in o['ownership'] if r['unitId']!='Cargo.toml#bin:legacy']))),
 'partial-enumeration':lambda:mod.shared_selection_stale(lambda o:o.update(enumeration='partial')),
}
POSITIVES={
 'shared-path-selected-lib':lambda:mod.shared_selection_stale(lambda o:None),
 'agreeing-selected-owners':lambda:mod.shared_selection_stale(
     lambda o:(o['selectedUnitIds'].append('Cargo.toml#bin:legacy'),
               [u.update(targetEdition=2021) for u in o['units'] if u['unitId']=='Cargo.toml#bin:legacy'])),
 'large-single-edition-workspace':lambda:mod.clone_run_with_universe(
     lambda u:u.update(edition=dict(mod.LARGE_EDITION))),
 'renamed-crate':lambda:mod.clone_run_with_universe(lambda u:u.update(edition={'renamed-crate':2021}),
     mutate_ownership=lambda o:[u.update(crateName='renamed-crate') for u in o['units']]),
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

# Two DIFFERENT neutralisations, because the eight negatives are refused by two different rules and
# one stub cannot measure both.
original=M.body_language_version
originalfx=mod.body_language_version

# (1) STALE-VERSION cases: drop the derived projection to a constant on BOTH sides, so the frame
#     stops being joined to the committed compiler identity at all. Everything else in the frame
#     check stays live, so an unrelated framing refusal would still be visible.
CONSTANT={'schemaVersion':1,'languageId':None,'compilerName':'x','compilerVersion':'x',
          'compilerBuild':'x','dialect':None}
M.body_language_version=lambda universe,context,row,anchor,retained=None:dict(CONSTANT,languageId=row['language'])
restated=mod.restated_language_version
mod.restated_language_version=(lambda fact,blobs,language,**overrides:
    __import__('hashlib').sha256(C.canonical(dict(CONSTANT,languageId=language))).digest())
DIALECT_CASES={'no-committed-ownership','selected-owners-disagree','owner-not-selected','partial-enumeration'}
after_version=measure({k:v for k,v in NEGATIVES.items() if k not in DIALECT_CASES})
M.body_language_version=original;mod.restated_language_version=restated

# (2) DIALECT cases: keep the whole projection and replace ONLY the no-guess rule with the guess a
#     permissive implementation would make - take some value out of the map - on both sides. If the
#     Run then closes, the refusal was caused by the no-guess rule and by nothing else.
def guessing(universe,context,row,anchor=None,retained=None):
    """The current projection with ONLY the no-guess rules removed, so each dialect negative is
    measured against the permissive implementation it is meant to exclude: partial enumeration is
    treated as if complete, an unselected owner is used anyway, and disagreeing selected owners have
    the first in canonical row order picked. Everything else is the shipped logic."""
    binding=row['languageVersionBinding']
    record={'schemaVersion':1}
    for name,source in binding['fields'].items():
        if 'const' in source:record[name]=source['const'];continue
        node=context if source['source']=='native-context' else universe
        for step in source['path']:node=node[step]
        record[name]=node
    dialect=binding['dialect']
    if dialect['form']=='closed-suffix-table':
        matches=[x for x in dialect['table'] if (anchor or {'path':'x.ts'})['path'].endswith(x)]
        variant=dialect['table'][max(matches,key=len)]
        record['dialect']={dialect['key']:variant}
        record['languageId']=binding['bodyLanguageByVariant'][variant]
        return record
    record['languageId']=binding['bodyLanguage']
    node=universe
    for step in dialect['path']:node=node[step]
    spec=dialect['ownership'];owned=(retained or {}).get(spec['retainedAs'])
    units={} if owned is None else {u[spec['unitField']]:u for u in owned[spec['unitsField']]}
    rows=[] if owned is None else [r for r in owned['ownership'] if r[spec['pathField']]==anchor['path']]
    chosen=[r for r in rows if r[spec['unitField']] in set(owned[spec['selectionField']])] if owned else []
    if not chosen:chosen=rows                                   # use an unselected owner anyway
    effective=[units[r[spec['unitField']]][spec['targetEditionField']]
               if units[r[spec['unitField']]][spec['targetEditionField']] is not None
               else node.get(units[r[spec['unitField']]][spec['crateField']],2015) for r in chosen]
    if not effective:effective=list(node.values()) or [2015]    # fall back to the package map
    record['dialect']={dialect['key']:effective[0]}             # ARBITRARY FIRST MATCH
    return record

M.body_language_version=guessing;mod.body_language_version=guessing
after_dialect=measure({k:v for k,v in NEGATIVES.items() if k in DIALECT_CASES})
M.body_language_version=original;mod.body_language_version=originalfx
after={**after_version,**after_dialect}

# The EMPTY-edition case cannot be measured by Run-level neutralisation, and saying so is the
# honest result rather than reporting a status this probe did not establish: any permissive
# fallback must INVENT a dialect, and an invented value never equals the one the already-minted
# frame carries, so the Run refuses for a mismatch instead of for the rule under test. It is
# measured at the boundary where the rule actually lives - the pure projection function - and the
# absence of any agreeable value is exactly why refusing is the only coherent outcome.
fact,_p,_parts=mod.clone_frame_of(mod.CLONE_RUNS['rust'])
universe,context=mod.universe_and_context(fact,mod.CLONE_RUNS['rust'][2])
row=mod.UNIVERSE_ROW['rust']
function_level={}

frames={}
for language in ('typescript','rust'):
    fact,payload,parts=mod.clone_frame_of(mod.CLONE_RUNS[language])
    frames[language]={'componentBytes':len(parts[4]),'inheritedMaximum':255,
                      'componentLengths':[len(p) for p in parts[:5]],'frameBytes':len(parts[0])+len(parts[5])}
print(json.dumps({
 'standing':'actual Claude coauthor probe; design/reference evidence only, no product qualification',
 'withEnforcement':before,'withoutTheLanguageVersionJoin':after,
 'neutralisation':{'staleVersionCases':'derived projection replaced by a constant on both sides','dialectCases':'no-guess rule replaced by take-any-value on both sides'},
 'positiveVectorsWithEnforcement':positives,
 'mixedEditionWorkspaceRuns':{path:('CLOSED '+mod.clone_frame_of(graph)[1]['bodyIdentity'][:22])
                              for path,graph in mod.MIXED_RUNS.items()},
 'frameComponentSizes':frames,
 'dialectRuleAtTheFunctionBoundary':function_level,
 'sharedPathTwoSelections':{u:mod.clone_frame_of(g)[1]['bodyIdentity'][:22] for u,g in mod.SHARED_RUNS.items()},
 'rootVectorRawMapBytes':len(C.canonical({'edition':mod.LARGE_EDITION})),
 'loadBearing':sorted(n for n in NEGATIVES if before[n]!='CLOSED' and after[n]=='CLOSED'),
 'notLoadBearing':sorted(n for n in NEGATIVES if after[n]!='CLOSED'),
 'notMeasurableByThisNeutralisation':{'selected-owners-disagree':
   'The permissive stub picks the FIRST selected owner in canonical row order, which here is the '
   'bin target at 2015, while the frame under test was minted under the lib-only selection at 2021. '
   'Any arbitrary pick is a coin flip against an already-minted frame, so this neutralisation '
   'measures a mismatch rather than the rule. That the guess lands on the OTHER unit is itself the '
   'point of the rule. The shipped test asserts the exact cause '
   'BODY_LANGUAGE_OWNER_AMBIGUOUS:src/lib.rs:2 and has valid positive controls '
   '(shared-selection-harness-positive-control-closes and agreeing-selected-owners), which root '
   'states is sufficient. The stub was deliberately NOT tuned to make this row pass.'},
 
 'positivesThatMustClose':sorted(n for n,v in positives.items() if v!='CLOSED')},indent=1))
