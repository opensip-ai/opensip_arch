import hashlib
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
NL=chr(10)
def sha(fp): return hashlib.sha256(open(fp,'rb').read()).hexdigest()
# HARNESS FIX 1: canonical-set list unpacked by position
p1=S+'/src25/docs/coop/design-corrections/foundation/check-execution-inputs.v1.py'
s1=open(p1,encoding='utf-8').read(); b1=sha(p1)
old='    rel_schema, cov_schema = existing_view["schemaDigests"]'+NL
new=('    # `schemaDigests` is x-opensip-order: canonical-set, so its ORDER IS CONTENT, never role.'+NL+
     '    # Positional unpacking was only correct for the accidental digest values of one frozen'+NL+
     '    # revision: any registered document whose digest re-sorts the pair silently swaps the two.'+NL+
     '    # Select the coverage document by its registered identity instead of by position.'+NL+
     '    cov_schema = H.N.schema_document_digest(H.N.NATIVE_SCHEMA_DOC)'+NL+
     '    rel_schema = next(d for d in existing_view["schemaDigests"] if d != cov_schema)'+NL)
n1=s1.count(old)
assert n1==3, n1
s1=s1.replace(old,new)
open(p1,'w',encoding='utf-8').write(s1)
print('fix1 sites',n1,'| before',b1,'| after',sha(p1))
# HARNESS FIX 2: canonical-set arrays re-normalised after element substitution
p2=S+'/src25/docs/coop/design-corrections/security/check-analysis-seal-adapter.v1.py'
s2=open(p2,encoding='utf-8').read(); b2=sha(p2)
old2='    proof = replace(proof)'+NL+'    pid = M.identifier("proof-bundle", proof)'+NL
new2=('    proof = replace(proof)'+NL+
      '    # findingIds arrays are x-opensip-order: canonical-set. Substituting one element does not'+NL+
      '    # preserve that order, so re-normalise every canonical-set finding array after replacement'+NL+
      '    # rather than relying on the replacement digest sorting into the replaced position.'+NL+
      '    proof["findingIds"] = R.E.cset(proof["findingIds"])'+NL+
      '    proof["waivedFindingIds"] = R.E.cset(proof["waivedFindingIds"])'+NL+
      '    for _rr in proof["ruleResults"]:'+NL+
      '        _rr["findingIds"] = R.E.cset(_rr["findingIds"])'+NL+
      '    pid = M.identifier("proof-bundle", proof)'+NL)
n2=s2.count(old2)
assert n2==1, n2
s2=s2.replace(old2,new2,1)
old3='    evidence = replace(copy.deepcopy(evidence))'+NL
new3=('    evidence = replace(copy.deepcopy(evidence))'+NL+
      '    evidence["findingIds"] = R.E.cset(evidence["findingIds"])'+NL)
n3=s2.count(old3)
assert n3==1, n3
s2=s2.replace(old3,new3,1)
open(p2,'w',encoding='utf-8').write(s2)
print('fix2 sites',n2+n3,'| before',b2,'| after',sha(p2))
