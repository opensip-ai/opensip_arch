"""RE-RUN of ROOT's inherited-limb consistency counterexample against the CORRECTED source.

NOT my construction. Provenance: docs/coop/design-corrections/reviews/codex-post-reset.v1/
annotation-inherited-limbs-draft-counterexample.v10/probe.py, authored by Codex/root against the
captured v7 model (identity-model.py sha256
77ff7d02d73cc5798d6786d0e3eaec42dacd2aa34ece9ddd994a79bf03a8b79e). The nine vectors - three
annotation LOCATIONS x three RETENTIONS - are theirs and are not rewritten. Only the repository
writes and the source capture are removed so nothing is written into the tree.

Root's own note records that an initial exploratory command used system python3 and failed importing
jsonschema before any model execution; their retained probe, and this re-run, use the review
environment.

Root's finding on the draft: the three FIELD vectors behaved correctly, while all six ALIAS and
BRANCH vectors ADMITTED - including a dangling preimage with no join and an invented retention.
Expected now: field behaviour unchanged, and alias and branch reaching the SAME earlier-limb causes,
with the lawful not-joined control still admitting at every location.
"""
from pathlib import Path
import copy,hashlib,importlib.util,json,shutil
from jsonschema import Draft202012Validator
root=Path('/Users/sb/code/opensip-ai/opensip_arch');dc=root/'docs/coop/design-corrections';model=dc/'foundation/identity-model.py';raw=model.read_bytes();spec=importlib.util.spec_from_file_location('codex_inherited_limbs',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M);rows=[]
for location in ('field','alias','branch'):
 for retention in ('preimage','invented-retention','not-joined'):
  d=copy.deepcopy(M.RELATION_DOCUMENT);d['$defs']['ProbeAlias']={'$ref':'#/$defs/DigestHex'};field={'$ref':'#/$defs/ProbeAlias'};annotation={'representation':'raw-artifact','retention':retention,'authority':'hypothetical-schema-probe','join':'Synthetic schema-only annotation-location control; no product field or authority.'}
  if location=='field':field['x-opensip-digest']=annotation
  elif location=='alias':d['$defs']['ProbeAlias']['x-opensip-digest']=annotation
  else:field={'oneOf':[{'type':'null'},{'$ref':'#/$defs/DigestHex','x-opensip-digest':annotation}]}
  d['$defs']['FilePayloadV1']['properties']['stray']=field;Draft202012Validator.check_schema(d)
  try:M.relation_annotation_closure('file',d);result={'admitted':True}
  except Exception as e:result={'admitted':False,'cause':str(e),'exception':type(e).__name__}
  rows.append({'id':location+'-'+retention,'location':location,'retention':retention,'coverage':M.relation_digest_annotation_coverage(d)['byRelation']['file'],'admission':result,'fieldSchema':field,'aliasSchema':d['$defs']['ProbeAlias']})

print(json.dumps({'standing':'actual Claude coauthor RE-RUN of a ROOT-authored counterexample against the CORRECTED source; schema/reference evidence only, not a payload or Run attack and not acceptance',
 'rootEvidence':'reviews/codex-post-reset.v1/annotation-inherited-limbs-draft-counterexample.v10/result.json',
 'correctedModelSha256':hashlib.sha256(raw).hexdigest(),
 'relationDocumentEdited':False,
 'vectors':[{k:r[k] for k in ('id','location','retention','admission')} for r in rows]},indent=1))
