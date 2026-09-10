"""PROBE: root's nine vectors, measured across the two ACTUAL source images.

A monkeypatch cannot express the pre-v8 state, because it held two notions of "annotated" at once -
coverage inherited them, retention and residue read direct properties - and a single stub over the
coverage function collapses both. That attempt is retained, labelled, at
result-unified-limbs-are-load-bearing.v1-STUB-COLLAPSED-LIMB3.json.

So this measures the real thing instead: root's nine vectors run against

  * v7: the retained image at reviews/digest-corrections-author.v7/author-source/, identity-model.py
    sha256 77ff7d02d73cc5798d6786d0e3eaec42dacd2aa34ece9ddd994a79bf03a8b79e - the model root
    captured for the counterexample - overlaid onto a copy of the current tree at
    runs/v7-image/ so that the files it imports and root owns (canonical.py, the workflow and native
    helpers) are present. Only the two owned files differ between the images, verified file by file
    against the retained hashes; and
  * v8: the current working tree.

The relation document is byte-identical in both, and is loaded from each image's own copy so neither
run depends on the other. The nine vectors are root's construction.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path

ROOT=Path('/Users/sb/code/opensip-ai/opensip_arch')
IMAGES={
 'v7':Path('/tmp/opensip-design-corrections/digest-corrections-author.v8/runs/v7-image/docs/coop/design-corrections/foundation/identity-model.py'),
 'v8':ROOT/'docs/coop/design-corrections/foundation/identity-model.py',
}

def load(label,path):
    spec=importlib.util.spec_from_file_location('inherited_limbs_'+label,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def vector(M,location,retention):
    """Root's construction, verbatim in shape."""
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    document['$defs']['ProbeAlias']={'$ref':'#/$defs/DigestHex'}
    annotation={'representation':'raw-artifact','retention':retention,
                'authority':'hypothetical-schema-probe',
                'join':'Synthetic schema-only annotation-location control; no product field or authority.'}
    field={'$ref':'#/$defs/ProbeAlias'}
    if location=='field':field['x-opensip-digest']=annotation
    elif location=='alias':document['$defs']['ProbeAlias']['x-opensip-digest']=annotation
    else:field={'oneOf':[{'type':'null'},{'$ref':'#/$defs/DigestHex','x-opensip-digest':annotation}]}
    document['$defs']['FilePayloadV1']['properties']['stray']=field
    return document

def measure(label,path):
    M=load(label,path);rows={}
    for location in ('field','alias','branch'):
        for retention in ('preimage','invented-retention','not-joined'):
            try:
                M.relation_annotation_closure('file',vector(M,location,retention))
                rows[location+'-'+retention]='ADMITTED'
            except Exception as exc:rows[location+'-'+retention]=str(exc)
    return rows,hashlib.sha256(path.read_bytes()).hexdigest()

rows={};hashes={}
for label,path in IMAGES.items():rows[label],hashes[label]=measure(label,path)

flipped=sorted(k for k in rows['v7'] if rows['v7'][k]=='ADMITTED' and rows['v8'][k]!='ADMITTED')
unchanged=sorted(k for k in rows['v7'] if rows['v7'][k]==rows['v8'][k])
lawful=[l+'-not-joined' for l in ('field','alias','branch')]

print(json.dumps({
 'standing':'actual Claude coauthor measurement across two retained source images, using a '
            'ROOT-authored construction; schema/reference evidence only, not a payload or Run '
            'attack, no runtime security claim and no product qualification',
 'rootEvidence':'reviews/codex-post-reset.v1/annotation-inherited-limbs-draft-counterexample.v10/result.json',
 'imageSha256':hashes,
 'relationDocumentEdited':False,
 'v7':rows['v7'],'v8':rows['v8'],
 'flippedFromAdmittedToRefused':flipped,
 'unchanged':unchanged,
 'lawfulNotJoinedAdmitsAtEveryLocationInBoth':all(rows[i][k]=='ADMITTED' for i in ('v7','v8') for k in lawful),
 'verdict':('CLOSED: the six alias and branch vectors were admitted on v7 and now refuse, the three '
            'field vectors are unchanged, and the lawful not-joined control still admits at every '
            'location in both images'
            if len(flipped)==4 and set(unchanged)>=set(lawful)|{'field-preimage','field-invented-retention'}
            else 'NOT AS EXPECTED: see the two tables')},indent=1))
