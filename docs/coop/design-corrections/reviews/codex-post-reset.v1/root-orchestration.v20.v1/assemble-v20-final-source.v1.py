from pathlib import Path
import json,hashlib,shutil,subprocess,difflib
B=Path('/tmp/opensip-design-corrections');P=B/'v20-combined-source.v1';R=B/'v20-route-coauthor.v1';F=B/'v20-final-source.v1';assert not F.exists();F.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
subprocess.run(['cp','-Rc',str(P/'work'),str(F/'work')],check=True)
changes=json.loads((R/'results/changed-files.json').read_text())['changed']
for row in changes:
 rel=row['path'];assert sha(F/'work'/rel)==row['beforeSha256'];assert sha(R/'overlay'/rel)==row['afterSha256'];shutil.copyfile(R/'overlay'/rel,F/'work'/rel)
D=F/'work/docs/coop/design-corrections'
root_before={}
def edit(p,old,new):
 root_before.setdefault(str(p.relative_to(F/'work')),p.read_bytes());s=p.read_text();assert s.count(old)==1,(p,old,s.count(old));p.write_text(s.replace(old,new))
p=D/'native/native-evidence.schemas.v2.json'
edit(p,'Two requestedCapabilities rows carry the same (capabilityId, languageMode, workspaceRoot) and disagree on `required`. The tuple NAMES one cell of work for one unit and `required` is that cell\'s attribute, so the record leaves requiredness undetermined for a cell whose value decides whether a missing Coverage entry contributes indeterminate - and both rows enter analysisSpecDigest and therefore PlanId, so the contradiction is committed rather than transient.', 'Two requestedCapabilities rows carry the same (capabilityId, languageMode, workspaceRoot). The tuple names one cell of work for one unit and `required` is its attribute. Distinct rows can disagree on requiredness, whose value decides whether a missing Coverage entry contributes indeterminate; if admitted, that contradiction would enter analysisSpecDigest and PlanId. Default construction can instead produce identical rows through a host invariant violation. Both cases violate the one-row-per-tuple law; the precise admission paths are stated below.')
p=F/'work/docs/v2/contracts/product-v1/native-evidence.md'
edit(p,'so the one refusal the default path can\n  reach had no derivable public termination at all','so this duplicate-selection refusal had no derivable\n  public termination')
p=D/'foundation/check-identity.py'
edit(p,'# public_termination_for and failure_envelope_errors both refused it and the one refusal the default\n# path can reach had no derivable public termination at all.', '# public_termination_for and failure_envelope_errors both refused it, so this duplicate-selection\n# refusal had no derivable public termination.')
edit(p,"check('adopt_baseline-with-the-selected-document-raises-neither-scope-binding-refusal',\n      _adopt_scope_detail([_SCOPE_ROW_A],SCOPE_DOCUMENT) not in _SCOPE_DETAILS)","check('adopt_baseline-with-the-selected-document-returns-without-any-refusal',\n      _adopt_scope_detail([_SCOPE_ROW_A],SCOPE_DOCUMENT) is None)")
edit(p,"_v20_domains=SCHEMA['$defs']['Domain']['enum']", "# A fragment may declare selected schemas, but each must name a current registered document.\n# This is a fixture-drift guard, not evidence that the fragment is a sealed or replayed Run.\ncheck('v20-native-view-fixture-declares-current-registered-schemas',\n      bool(NATIVE_FIXTURES['coverageView']['schemaDigests']) and\n      set(NATIVE_FIXTURES['coverageView']['schemaDigests'])<=M.registered_schema_documents())\n_v20_domains=SCHEMA['$defs']['Domain']['enum']")
p=D/'native/native-cases.v2.json';d=json.loads(p.read_text());old=d['fixtures']['coverageView']['schemaDigests'];assert len(old)==1
edit(p,old[0],sha(D/'native/native-evidence.schemas.v2.json'))
parent=json.loads((P/'proposal.json').read_text());paths={x['path'] for x in parent['changedFiles']} if 'changedFiles' in parent else {x['path'] for x in parent['files']}
paths|={x['path'] for x in changes};paths|=set(root_before)
rows=[]
for rel in sorted(paths):
 before=B/'candidate-subject.v19'/rel;after=F/'work'/rel;route=R/'overlay'/rel
 routebytes=route.read_bytes() if route.exists() else (P/'work'/rel).read_bytes()
 rows.append({'path':rel,'beforeSha256':sha(before),'preliminarySha256':sha(P/'work'/rel),'routeSha256':hashlib.sha256(routebytes).hexdigest(),'afterSha256':sha(after)})
 diff=''.join(difflib.unified_diff(routebytes.decode().splitlines(True),after.read_text().splitlines(True),fromfile='a/'+rel,tofile='b/'+rel));q=F/'root-diffs'/(Path(rel).name+'.diff');q.parent.mkdir(exist_ok=True);q.write_text(diff)
 q=F/'complete-diffs'/(Path(rel).name+'.diff');q.parent.mkdir(exist_ok=True);q.write_text(''.join(difflib.unified_diff(before.read_text().splitlines(True),after.read_text().splitlines(True),fromfile='a/'+rel,tofile='b/'+rel)))
manifest={'standing':'Unfrozen final source composition PROPOSED; requires bounded Claude assent then root final source assessment and six checked/pinned commands before freezing.','parentManifestSha256':'312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b','preliminaryManifestSha256':sha(P/'proposal.json'),'routeChangesSha256':sha(R/'results/changed-files.json'),'files':rows,'rootChanges':['Refine duplicate-tuple route opening to cover both distinct and identical duplicates.','Narrow overbroad only-default-refusal claim to this duplicate-selection refusal in prose/comment.','Strengthen selected baseline positive to reject any Refusal; projection helper only, caller-admitted inputs remain precondition.','Refresh native coverageView fragment schema declaration to final native schema bytes.','Add durable native fragment registered-schema membership drift guard.'],'knownRequiredWork':['Bounded Claude/root alignment on final added delta','Final source pins/reports and all six commands','Freeze/fresh independent review','NEW blind consumer','Complete independently reviewed application/readiness']}
(F/'proposal.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({'manifest':str(F/'proposal.json'),'sha256':sha(F/'proposal.json'),'files':len(rows)}))
