"""Root minimal reference proposal for actual Claude assessment, never live integration."""
from pathlib import Path
import json,shutil,hashlib,difflib
src=Path('/tmp/opensip-design-corrections/candidate-subject.v16');out=Path('/tmp/opensip-design-corrections/bv6-root-overlap-proposal.v1');assert not out.exists();out.mkdir();work=out/'work';shutil.copytree(src,work)
rel='docs/coop/design-corrections/foundation/identity-model.py';p=work/rel;before=p.read_text();needle="        for scope_id in view['scopeIds']:\n            scope=get(scope_id,'subject-scope')\n";assert before.count(needle)==1
replacement="""        # Root proposal, pending actual coauthor scope assessment: partition subjects WITHIN each
        # view, grouped by the same snapshot/relation/rung/source and target universe. A producer's
        # admission of one Coverage entry cannot decide this between-scopes property. Distinct views
        # may reuse the same scope; distinct tuples may interpret the same spelling independently.
        partition_subjects={}
        for scope_id in view['scopeIds']:
            scope=get(scope_id,'subject-scope')
            partition=tuple(scope[field] for field in ('snapshotId','relation','resolution','sourceUniverse','targetUniverse'))
            seen_subjects=partition_subjects.setdefault(partition,set())
            if seen_subjects.intersection(scope['subjects']):raise C.AdmissionError('SUBJECT_SCOPE_PARTITION_OVERLAP')
            seen_subjects.update(scope['subjects'])
"""
p.write_text(before.replace(needle,replacement));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'proposal.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),p.read_text().splitlines(True),fromfile='v16/'+rel,tofile='root-proposal/'+rel)))
(out/'proposal.json').write_text(json.dumps({'standing':'Root reference proposal ONLY, for actual Claude assessment. Not integrated, not source assent and not selected normative partition-key definition until mutually assessed.','baseManifestSha256':'ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9','source':{'path':rel,'beforeSha256':sha(src/rel),'afterSha256':sha(p)},'proposedGrouping':['snapshotId','relation','resolution','sourceUniverse','targetUniverse'],'scope':'Within each view; applies to its referenced subject scopes, including scopes without Coverage. Cross-view reuse and different-group same spelling remain allowed. Actual coauthor must assess these boundary choices, not just acknowledge failing overlap control.','singleProducerLimit':'One-scope Coverage producer cannot decide disjointness of a joint view; authoritative retained-Run boundary has both scopes. No new host effect or protocol invocation.','pins':'Original pins intentionally stale in proposal; no aggregate checks or acceptance inferred.'},indent=2)+'\n');print(out)
