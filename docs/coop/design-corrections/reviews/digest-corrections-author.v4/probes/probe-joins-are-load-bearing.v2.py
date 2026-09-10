"""PROBE v2 (supersedes probe-joins-are-load-bearing.v1-STALE-MUTATION.py): every v8-S2 negative must fail BECAUSE of the new join, not incidentally.

Method: monkey-patch the enforcement out of the loaded model (registry rows emptied, body join
removed) and re-run each negative. If a negative still refuses, its control did not reach the
intended join and the test would be false coverage.
"""
import copy,importlib.util,json,sys
from pathlib import Path
H=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/foundation')
sys.argv=[sys.argv[0]]
spec=importlib.util.spec_from_file_location('chk',H/'check-identity.py')
mod=importlib.util.module_from_spec(spec)
try:spec.loader.exec_module(mod)
except SystemExit:pass
M=mod.M
NEGATIVES={
 # each lambda below is the EXACT mutation check-identity.py ships, not a paraphrase
 'fabricated-path':lambda:mod.file_fact_mutation(lambda f,p,b,o,r:p.update(path='invented/not-in-snapshot.ts')),
 'wrong-content-hash':lambda:mod.file_fact_mutation(lambda f,p,b,o,r:p.update(contentSha256=mod.put_blob(b,b'other bytes entirely\n'))),
 'wrong-byte-length':lambda:mod.file_fact_mutation(lambda f,p,b,o,r:p.update(byteLength=p['byteLength']+1)),
 'foreign-snapshot':mod.file_claim_over_a_foreign_snapshot,
 'second-owner-anchor':mod.second_owner_borrows_a_file_payload,
 'body-frame-level-version':lambda:mod.clone_mutation(lambda f,p,b,o,r:p.update(bodyIdentity=mod.reframed(p,b,version=p['normalisationVersion'].encode('ascii')))),
 'body-frame-language':lambda:mod.clone_mutation(lambda f,p,b,o,r:p.update(bodyIdentity=mod.reframed(p,b,language='rust'))),
 'body-frame-language-version':lambda:mod.clone_mutation(lambda f,p,b,o,r:p.update(bodyIdentity=mod.reframed(p,b,language_version=mod.C.canonical({'languageMode':'ts-tsconfig','synthesizerVersion':'0.0.0'})))),
 'body-frame-level':lambda:mod.clone_mutation(lambda f,p,b,o,r:p.update(bodyIdentity=mod.reframed(p,b,level='L1-lexical'))),
 'l0-span':lambda:mod.clone_mutation(lambda f,p,b,o,r:p.update(bodyIdentity=mod.reframed(p,b,body=(lambda x:len(x).to_bytes(4,'big')+x)(b'export const foo = 2;\n')))),
 'anchor-cardinality':lambda:mod.clone_mutation(lambda f,p,b,o,r:f.__setitem__('anchors',sorted(f['anchors']+[dict(f['anchors'][0],endByte=f['anchors'][0]['endByte']-1)],key=mod.C.canonical))),
}
def run(label):
    out={}
    for name,fn in NEGATIVES.items():
        try:fn();out[name]='CLOSED'
        except Exception as exc:out[name]=type(exc).__name__+':'+str(exc)[:70]
    return out
before=run('enforced')
saved=copy.deepcopy(M.RELATIONS)
for row in M.RELATIONS.values():
    row['snapshotJoins']=[];row.pop('bodyIdentityJoin',None)
M._RELATION_LAW_CLOSURE.clear()
# the residue rule would now refuse every annotated relation, so neutralise it for the probe only
M.relation_annotation_closure=lambda name,document=None:M.RELATIONS[name]
after=run('disabled')
print(json.dumps({'withEnforcement':before,'withoutEnforcement':after,
 'loadBearing':sorted(n for n in NEGATIVES if before[n]!='CLOSED' and after[n]=='CLOSED'),
 'notLoadBearing':sorted(n for n in NEGATIVES if after[n]!='CLOSED')},indent=1))
