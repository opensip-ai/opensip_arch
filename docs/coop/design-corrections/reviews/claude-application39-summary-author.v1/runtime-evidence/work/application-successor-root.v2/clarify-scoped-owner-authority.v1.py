from pathlib import Path
import hashlib,json,shutil,ast
base=Path(__file__).parent;dest=base/'scoped-owner-clarification-before.v1';dest.mkdir(exist_ok=False)
for n in ['assemble-records.py','prepare-validation.py']:shutil.copyfile(base/n,dest/n)
p=base/'assemble-records.py';s=p.read_text()
old="dict(v,id=k,reviewEvidence=evidence('/scopedReviewOwnerDispositions/'+k))"
new="dict(v,id=k,reviewEvidence=evidence('/scopedReviewOwnerDispositions/'+k),applicationDisposition='ACCEPT-DESIGN',gradeAuthority='The design review accepted routing only. A new subject-specific outcome requires substantive assessment by the fresh final application reviewer; no historical grade is extended.',finalApplicationReviewBinding=activation)"
assert s.count(old)==1;s=s.replace(old,new)
needle="# Every condition-2 row is separately reviewable, with all missing source/gate corrections."
insert="""# Make the prospective register's five new owner outcomes depend on the new full application review.
register_rel='docs/v2/architecture/08-decision-and-readiness-register.md'
register=(files/register_rel).read_text()
old_owner='This is a new subject-specific design review.'
assert register.count(old_owner)==5
register=register.replace(old_owner,'The new subject-specific outcome requires the fresh final application review bound by D-372 activation; the earlier v12 design review accepted routing only.')
writet(register_rel,register)
"""
assert s.count(needle)==1;s=s.replace(needle,insert+needle);p.write_text(s)
p=base/'prepare-validation.py';s=p.read_text();old="'subject-envelope-adapter-custody.v1.json']:";new="'subject-envelope-adapter-custody.v1.json','clarify-scoped-owner-authority.v1.py','scoped-owner-clarification.v1.json']:";assert s.count(old)==1;s=s.replace(old,new);old="'subject-envelope-adapter.v1']:";new="'subject-envelope-adapter.v1','scoped-owner-clarification-before.v1']:";assert s.count(old)==1;s=s.replace(old,new);p.write_text(s)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['assemble-records.py','prepare-validation.py']:ast.parse((base/n).read_text())
(base/'scoped-owner-clarification.v1.json').write_text(json.dumps({'standing':'Prospective application authority clarification after evidence clarification; no current record applied and accepted design bytes untouched.','changes':[{'path':n,'beforePath':'scoped-owner-clarification-before.v1/'+n,'beforeSha256':sha(dest/n),'afterSha256':sha(base/n)} for n in ['assemble-records.py','prepare-validation.py']]},indent=2)+'\n')
print('Scoped owner outcome authority clarified prospectively, exact changes retained.')
