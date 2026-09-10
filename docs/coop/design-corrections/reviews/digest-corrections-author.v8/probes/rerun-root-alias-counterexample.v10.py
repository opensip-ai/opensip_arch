"""RE-RUN of ROOT's alias-annotation counterexample against the CORRECTED source. NOT my construction.

Provenance: docs/coop/design-corrections/reviews/codex-post-reset.v1/
annotation-alias-positive-draft-counterexample.v10/probe.py, authored by Codex/root against the
captured in-progress v7 model. The three vectors below are theirs, byte-for-byte in their loop body;
only the repository writes and the source capture are removed so nothing is written into the tree,
and the model is loaded from the working tree.

Root's finding on the draft: the unannotated negative refused and annotation-on-the-FIELD admitted,
both correct, but annotation-on-the-alias-DEFINITION was reported unannotated and refused - which
contradicts the stated rule that an annotation anywhere on the path to a governed leaf covers it,
because governed_form chased the scalar alias and returned before walk ever saw the alias's own
annotation.

A fourth vector is added by me and labelled as mine: an annotation on the TERMINAL governed $def
(DigestHex itself). That must still REFUSE, and the boundary is deliberate - an annotation there
would be a blanket exemption for every field of that form in every relation, which is the hole this
limb exists to close, rather than a declaration about one field.

An earlier adaptation attempt of this file was discarded rather than shipped: a regex meant to strip
the repository writes also removed root's driver lines, so the probe produced no vectors. That
attempt is recorded here rather than passed off as a result.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path
from jsonschema import Draft202012Validator

root=Path('/Users/sb/code/opensip-ai/opensip_arch');dc=root/'docs/coop/design-corrections'
model=dc/'foundation/identity-model.py';raw=model.read_bytes()
spec=importlib.util.spec_from_file_location('claude_rerun_annotation_alias',model)
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
a={'representation':'raw-artifact','retention':'not-joined','authority':'hypothetical-schema-probe','join':'Synthetic schema annotation-location control; not a runtime field or authority.'};rows=[]
for label,at_use,at_definition in [('unannotated-negative',False,False),('annotation-on-field-positive',True,False),('annotation-on-alias-definition-positive',False,True)]:
 d=copy.deepcopy(M.RELATION_DOCUMENT);d['$defs']['ProbeAlias']={'$ref':'#/$defs/DigestHex'};d['$defs']['FilePayloadV1']['properties']['stray']={'$ref':'#/$defs/ProbeAlias'}
 if at_use:d['$defs']['FilePayloadV1']['properties']['stray']['x-opensip-digest']=a
 if at_definition:d['$defs']['ProbeAlias']['x-opensip-digest']=a
 Draft202012Validator.check_schema(d);c=M.relation_digest_annotation_coverage(d)
 try:M.relation_annotation_closure('file',d);result={'admitted':True}
 except Exception as e:result={'admitted':False,'cause':str(e),'exception':type(e).__name__}
 rows.append({'id':label,'coverage':c['byRelation']['file'],'admission':result,'fieldSchema':d['$defs']['FilePayloadV1']['properties']['stray'],'aliasSchema':d['$defs']['ProbeAlias']})

# --- added by actual Claude, labelled as mine rather than root's ---
d=copy.deepcopy(M.RELATION_DOCUMENT)
d['$defs']['ProbeAlias']={'$ref':'#/$defs/DigestHex'}
d['$defs']['FilePayloadV1']['properties']['stray']={'$ref':'#/$defs/ProbeAlias'}
d['$defs']['DigestHex']=dict(d['$defs']['DigestHex'],**{'x-opensip-digest':a})
Draft202012Validator.check_schema(d);c=M.relation_digest_annotation_coverage(d)
try:M.relation_annotation_closure('file',d);result={'admitted':True}
except Exception as e:result={'admitted':False,'cause':str(e),'exception':type(e).__name__}
rows.append({'id':'annotation-on-the-TERMINAL-governed-def-must-still-refuse','author':'actual Claude',
             'coverage':c['byRelation']['file'],'admission':result,
             'why':'an annotation on DigestHex itself would blanket-cover every field of that form in '
                   'every relation, which is the hole this limb closes, so it is deliberately not '
                   'inherited; only INTERMEDIATE alias definitions on the ref chain are'})

print(json.dumps({'standing':'actual Claude coauthor RE-RUN of a ROOT-authored counterexample against '
                             'the CORRECTED source, plus one boundary vector of my own; schema/reference '
                             'evidence only, not a Run or payload attack and not acceptance',
                  'rootEvidence':'reviews/codex-post-reset.v1/annotation-alias-positive-draft-counterexample.v10/result.json',
                  'modelSha256':hashlib.sha256(raw).hexdigest(),
                  'relationDocumentEdited':False,
                  'vectors':rows},indent=2))
