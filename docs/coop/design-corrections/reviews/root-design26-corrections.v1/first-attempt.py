from pathlib import Path
import json,hashlib,difflib
T=Path('/tmp/opensip-design-corrections/claude-return-successor.v1');O=Path('/tmp/opensip-design-corrections/root-design26-corrections.v1');O.mkdir(exist_ok=False)
rows=[]
def edit(rel,fn):
 p=T/rel;old=p.read_text();new=fn(old);assert new!=old
 for name,data in [('before',old),('after',new)]:
  q=O/name/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(data)
 p.write_text(new);rows.append({'path':rel,'beforeSha256':hashlib.sha256(old.encode()).hexdigest(),'afterSha256':hashlib.sha256(new.encode()).hexdigest(),'diff':''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=rel,tofile=rel))})
def replace(old,new):
 def fn(s):assert s.count(old)==1,(old,s.count(old));return s.replace(old,new)
 return fn
edit('docs/v2/contracts/product-v1/identity-and-evidence.md',replace('**Every 64-hex field in\nidentity-schemas.v3 has exactly one representation and one retention mode**','**Every bare 64-hex digest field in\nidentity-schemas.v3 has exactly one representation and one retention mode**'))
# Save the second prose refinement within the same owned after-image.
p=T/'docs/v2/contracts/product-v1/identity-and-evidence.md';s=p.read_text().replace('There is no residue: a 64-hex field carrying no annotation is','There is no residue: a bare 64-hex digest field carrying no annotation is').replace('default, which is stronger: a new 64-hex field added without an annotation','default, which is stronger: a new bare 64-hex digest field added without an annotation')
s=s.replace('The four representations are closed.','The machine-readable `x-opensip-digest-domains.scope` selects bare digest\nfields, including a reference to `#/$defs/Hash` and a non-null alternative of a\nnullable field. A typed-prefix identity field is outside this annotation scope:\nits prefix selects the identity domain and representation in the §3 identity\ntable. Its hex suffix is not a separate bare digest field.\n\nThe four representations are closed.',1);p.write_text(s);(O/'after'/p.relative_to(T)).write_text(s);rows[0]['afterSha256']=hashlib.sha256(s.encode()).hexdigest();rows[0]['diff']=''.join(difflib.unified_diff((O/'before'/p.relative_to(T)).read_text().splitlines(True),s.splitlines(True),fromfile=str(p.relative_to(T)),tofile=str(p.relative_to(T))))
def schema(s):
 j=json.loads(s);r=j['x-opensip-digest-domains'];r['standing']=r['standing'].replace('Every 64-hex field in this bundle','Every bare 64-hex digest field in this bundle')
 r['scope']={'governs':'bare-64-hex-digest-fields','schemaSelectors':{'pattern':'^[0-9a-f]{64}(?![\\s\\S])','$ref':'#/$defs/Hash'},'nullableAlternatives':'Apply to the non-null branch; the annotation may be on that branch.','typedPrefixIdentities':'Outside this annotation scope. Resolve the typed prefix through the identity-and-evidence section 3 identity table; its hex suffix is not a separate bare digest field.'}
 return json.dumps(j,indent=2)+'\n'
edit('docs/coop/design-corrections/foundation/identity-schemas.v3.json',schema)
edit('docs/coop/design-corrections/security/carrier-migration.v1.md',replace('validated before any durable act. It uses','validated before any durable act on the inherited-carrier migration path (acts A–B–C),\nincluding a resumed migration. The fresh-install path in open dispatch step 8,\nincluding its interrupted-install act-C resume, takes no CarrierMigrationIntentV1;\nits first generation is 1 and its migration fields are null. It uses'))
edit('docs/coop/design-corrections/security/carrier-dispatch.v3.json',replace('CarrierMigrationIntentV1 is private, host-projected and validated before any act.','CarrierMigrationIntentV1 is private, host-projected and validated before any act on the inherited-carrier migration path (acts A-B-C), including a resumed migration. The fresh-install path in openDispatch step 8, including its interrupted-install act-C resume, takes no CarrierMigrationIntentV1; first_generation is 1 and migration fields are null.'))
def anchor(s):
 j=json.loads(s);rows=j['frozenSourceAnchors'];hits=[r for r in rows if r['id']=='B11'];assert len(hits)==2;assert hits[1]['path']=='docs/coop/completion/security-completion.v1.md';hits[1]['id']='B14';s=json.dumps(j,indent=2)+'\n';assert s.count('(B11/B12)')==2;return s.replace('(B11/B12)','(B14/B12)')
edit('docs/v2/architecture/report-asset-binding.v1.json',anchor)
edit('docs/v2/contracts/product-v1/security-and-lifecycle.md',replace('runs 456 cases across\nsixteen fixtures','runs the current case fixtures'))
p=T/'docs/v2/contracts/product-v1/security-and-lifecycle.md';s=p.read_text().replace('and ten invariant sweeps','and the current invariant sweeps',1).replace('`security-lifecycle-report.v1.json`. Every signer','`security-lifecycle-report.v1.json`, whose measured totals are the authority for\ncase and sweep counts. Every signer',1);p.write_text(s);(O/'after'/p.relative_to(T)).write_text(s);rows[-1]['afterSha256']=hashlib.sha256(s.encode()).hexdigest();rows[-1]['diff']=''.join(difflib.unified_diff((O/'before'/p.relative_to(T)).read_text().splitlines(True),s.splitlines(True)))
def carrier(s):
 return s+'\n**Evidence custody and diagnosis vocabulary.** The `scratch/out/cN.json` and other\n`scratch/` citations in this document and the dispatch are relative to the original\nauthor review runtime, not companion files at these normative paths. They add no\nlaw and their presence must not be inferred from a citation. The current\n`check-integrated-carrier.v1.py` reconstructs the historical validator layout from\nthe selected normative companions and runs `check-carrier-v3.py`; that rerun is\nnew reference evidence, not reproduction of the original C1–C18 measurements.\n`witnessMalformed` is a read-only recovery diagnosis only. It deliberately is not\na durable `carrier_quarantine.reason`: read-only recovery cannot write a marker,\nand this revision preserves the inherited quarantine table definition.\n'
edit('docs/coop/design-corrections/security/carrier-format.v3.md',carrier)
(O/'changes.json').write_text(json.dumps({'standing':'Root corrections proposed for independent successor review; no acceptance. S1/S2/S3 and advisory A1/A2/A3. M1 is separately retained in root-target-hint-correction.v1.','changes':rows},indent=2)+'\n');print('Changed',len(rows),'files')
