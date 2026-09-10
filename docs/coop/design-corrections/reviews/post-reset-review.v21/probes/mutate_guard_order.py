"""REAL owning entrypoint probe for NEW-SHOULD-1.

Phase A calls the ACTUAL workflows_model.verify_scope_parameter_binding on the FROZEN bytes with
admitted positive data first. Phase B mutates exactly ONE law - the position of the at-most-one
ambiguity guard relative to the payload-digest match - in a disposable copy, and re-calls the same
real entrypoint. No algorithm is copied and no error is manufactured.
"""
import importlib.util,json,sys,hashlib,os,shutil
FROZEN='/tmp/opensip-design-corrections/candidate-subject.v21/docs/coop/design-corrections'
MUT='/tmp/opensip-design-corrections/post-reset-review.v21/work/mutation/tree/docs/coop/design-corrections'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s)
    sys.modules[name]=m;s.loader.exec_module(m);return m
def scenarios(root):
    C=load('canon_%s'%abs(hash(root)),os.path.join(root,'foundation/canonical.py'))
    W=load('wfm_%s'%abs(hash(root)),os.path.join(root,'workflows/workflows_model.v1.py'))
    POL=open(os.path.join(root,'workflows/schemas/policy-document.schema.json'),'rb').read()
    def row(doc): return {'schemaDigest':hashlib.sha256(POL).hexdigest(),
                          'payloadDigest':hashlib.sha256(C.canonical(doc)).hexdigest()}
    A={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['src/**/*.ts'],'exclude':['src/vendor/**']}
    B={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['src/**/*.ts'],'exclude':['src/generated/**']}
    Cc={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['src/**/*.ts'],'exclude':['src/legacy/**']}
    rA,rB,rC=row(A),row(B),row(Cc)
    def spec(rows): return {'schemaVersion':2,'requestedCapabilities':[],'policyPackIds':[],'parameters':rows}
    res={}
    for name,rows,doc in [
        ('POSITIVE: one row C, document C',[rC],Cc),
        ('POSITIVE: one row A, document A',[rA],A),
        ('zero rows, non-candidate C',[],Cc),
        ('one row A, non-candidate C',[rA],Cc),
        ('two rows A+B, NON-candidate C',[rA,rB],Cc),
        ('two rows A+B, candidate A',[rA,rB],A),
        ('two rows A+B, candidate B',[rA,rB],B),
    ]:
        try:
            v=W.verify_scope_parameter_binding(spec(rows),doc)
            res[name]={'outcome':'VERIFIED','digest':v,'isExpectedDigest':v==row(doc)['payloadDigest']}
        except W.Refusal as e:
            res[name]={'outcome':'REFUSAL','error_code':e.error_code,'detail':e.detail}
        except Exception as e:
            res[name]={'outcome':'OTHER-EXCEPTION','type':type(e).__name__,'msg':str(e)[:200]}
    return res
# ---- Phase B mutation: move the guard block below the payload match ----
src=os.path.join(MUT,'workflows/workflows_model.v1.py')
t=open(src).read()
GUARD=("    if len(rows) > 1:\n"
"        raise Refusal('CONFIG.INVALID', 'CONFIG.INVALID',\n"
"                      'the analysis spec selects more than one ScopeDocumentV1 parameter; state exactly one',\n"
"                      subject='parameters[schemaDigest=' + document + ']x' + str(len(rows)))\n")
MATCH=("    if not any(row.get('payloadDigest') == digest for row in rows):\n"
"        raise Refusal('REQUEST.PRECONDITION_FAILED', 'BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH',\n"
"                      'the supplied scope document is not the selected scope parameter')\n")
assert t.count(GUARD)==1, 'guard block not found exactly once'
assert t.count(MATCH)==1, 'match block not found exactly once'
assert t.index(GUARD) < t.index(MATCH), 'guard is not already before the match'
mutated=t.replace(GUARD,'',1).replace(MATCH,MATCH+GUARD,1)
assert mutated.index(MATCH) < mutated.index(GUARD)
open(src,'w').write(mutated)
out={'mutation':'verify_scope_parameter_binding: at-most-one ambiguity guard MOVED below the payload-digest match. Exactly one law changed; no other byte edited.',
     'mutatedFile':'docs/coop/design-corrections/workflows/workflows_model.v1.py',
     'frozenSha256':hashlib.sha256(open(os.path.join(FROZEN,'workflows/workflows_model.v1.py'),'rb').read()).hexdigest(),
     'mutatedSha256':hashlib.sha256(mutated.encode()).hexdigest(),
     'bytesFrozen':len(t),'bytesMutated':len(mutated),
     'A_frozen_realEntrypoint':scenarios(FROZEN),
     'B_mutated_realEntrypoint':scenarios(MUT)}
a,b=out['A_frozen_realEntrypoint'],out['B_mutated_realEntrypoint']
out['differingScenarios']={k:{'frozen':a[k],'mutated':b[k]} for k in a if a[k]!=b[k]}
out['unchangedScenarioCount']=len([k for k in a if a[k]==b[k]])
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v21/results/mutation-guard-order.json','w'),indent=1)
print(json.dumps(out,indent=1))
