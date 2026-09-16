"""Align current prose with integrated native laws; retain exact beforeimages."""
from pathlib import Path
import hashlib, json
S=Path('/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source')
O=Path(__file__).parent
assert not (O/'changes.json').exists()
rows=[]
def edit(path, old, new):
    p=S/path; before=p.read_bytes(); text=before.decode()
    assert text.count(old)==1, path
    backup=O/'before'/path; backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(before)
    after=text.replace(old,new).encode();p.write_bytes(after)
    rows.append({'path':path,'beforeSha256':hashlib.sha256(before).hexdigest(),'sha256':hashlib.sha256(after).hexdigest()})
edit('docs/v2/contracts/product-v1/security-and-lifecycle.md',
'''**Pruned trees and the read set (A-5).** "No custody walk" for a pruned tree
means discovery neither enumerates units in it nor walks its directories for
custody. Bytes a language program later reads from such a tree (a TypeScript
resolution reading `node_modules`, native §2.2/§9.4) enter the snapshot read
set through the identity unit's snapshot custody, are Plan-bound like every
other read-set byte, and are never a discovery unit; they are not exempt from
custody, they are custody-checked by the snapshot reader instead of the
discovery walk.''',
'''**Pruned trees and the read set (A-5).** A pruned tree is never custody-walked.
Its files enter the snapshot source inventory only when a Plan-selected context
actually read them under a committed read set. Today that means `node_modules`
package directories listed by a retained `ResolvedNodeModulesLayoutV1` of a
context with `nodeModulesInReadSet`. Such rows are `host-ignore-convention`
members joined at Run closure, refusing `SNAPSHOT_PRUNED_TREE_NOT_A_READ`.
VCS trees and Cargo build output are never reads. Required inputs outside the
project root stay in their owning closures. Which files inside a listed package
were read, and that the custody walk was complete, are host TCB observations
that bytes-only replay cannot prove. Identity §3 owns the inventory and joins;
native §1.4 U-4a/U-4b owns discovery and membership.''')
# A second edit to the same file preserves the immediately preceding bytes separately.
p='docs/v2/contracts/product-v1/security-and-lifecycle.md'
text=(S/p).read_text()
old='''record unchanged to native `discover_units`, `assign_membership` and
`unit_scope_descriptor`; the native instrument then yields exactly this
instrument's unit set, excludes every marker directory and file at or below a
boundary, refuses an explicit root crossing one'''
new='''record unchanged to native `discover_units`, `assign_membership` and
`unit_scope_descriptor`; the native instrument then yields this instrument's
marker-derived unit set. Native §1.4 U-9 additionally supplies its one default
syntax-only fallback when no language unit survives; that fallback is not a
marker directory, does not count toward the workspace-unit cap and claims no
program-member row. The native instrument excludes every marker directory and
file at or below a boundary, refuses an explicit root crossing one'''
assert text.count(old)==1
before=text.encode(); after=text.replace(old,new).encode()
(O/'security-after-readset-before-fallback.md').write_bytes(before)
(S/p).write_bytes(after)
rows.append({'path':p,'beforeSha256':hashlib.sha256(before).hexdigest(),'sha256':hashlib.sha256(after).hexdigest()})
edit('docs/v2/contracts/product-v1/native-evidence.md',
'''  package-directory read record such rows are joined to at Run closure. Its schema
  description's statement that no inventory row "could exist" for them predates
  this rule and is superseded here for files actually read; the layout rows
  themselves remain resolution observations, not inventory rows. Cases''',
'''  package-directory read record such rows are joined to at Run closure. Its
  registered schema description states the same distinction: layout rows are
  resolution observations, and files actually read are snapshot inventory rows.
  Cases''')
(O/'changes.json').write_text(json.dumps({'standing':'Root cross-owner prose alignment after actual native and recovery author integration; pending independent review. No new record or reference behavior.', 'files':rows},indent=2)+'\n')
print('Aligned source-inventory custody, fallback unit agreement and current schema wording.')
