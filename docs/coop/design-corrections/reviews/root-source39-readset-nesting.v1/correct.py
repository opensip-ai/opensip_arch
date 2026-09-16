"""Keep dependency-package read permission subordinate to VCS exclusions at every depth."""
from pathlib import Path
import hashlib,json
S=Path('/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source');O=Path(__file__).parent
assert not (O/'correction.json').exists()
rows=[]
def edit(path,old,new):
    p=S/path;b=p.read_bytes();s=b.decode();assert s.count(old)==1,path
    q=O/'before-files'/path;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
    a=s.replace(old,new).encode();p.write_bytes(a)
    rows.append({'path':path,'beforeSha256':hashlib.sha256(b).hexdigest(),'sha256':hashlib.sha256(a).hexdigest()})
edit('docs/coop/design-corrections/foundation/identity-model.v3.py',
'''    for path in paths:
        hit=DD.classify_path(path,cargo_roots)
        if hit is None:continue
        if hit[1]=='dependency-tree' and any(path.startswith(package+'/') for package in packages):continue
        faults.append(path)''',
'''    for path in paths:
        # Discovery reports the outermost pruned tree. A package read allowance must not
        # hide a deeper VCS segment: VCS custody bytes are never selected program reads.
        if any(segment in DD.VCS_TREE_SEGMENTS for segment in path.split('/')):
            faults.append(path)
            continue
        hit=DD.classify_path(path,cargo_roots)
        if hit is None:continue
        if hit[1]=='dependency-tree' and any(path.startswith(package+'/') for package in packages):continue
        faults.append(path)''')
edit('docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py',
'''    row("A4", "vcs-tree-rows-are-never-reads", faults([".git/HEAD", "sub/.hg/store/data"]) == [".git/HEAD", "sub/.hg/store/data"])''',
'''    row("A4", "vcs-tree-rows-are-never-reads", faults([".git/HEAD", "sub/.hg/store/data"]) == [".git/HEAD", "sub/.hg/store/data"])
    nested_vcs = ["node_modules/left-pad/" + segment + "/metadata" for segment in (".git", ".hg", ".svn", ".jj")]
    row("A4", "listed-package-read-allowance-never-overrides-nested-vcs", faults(nested_vcs) == sorted(nested_vcs))
    row("A4", "nested-vcs-lookalike-segments-remain-lawful-package-reads",
        faults(["node_modules/left-pad/.git-like/index.js", "node_modules/left-pad/.gitignore"]) == [])''')
# Preserve the initial checker beforeimage while applying a second bounded edit.
p=S/'docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py';b=p.read_bytes();s=b.decode()
old='''    for name, extra in (("an-unlisted-dependency-file", {"node_modules/unlisted/index.js": b"module.exports = 2;\\n"}),
                        ("a-vcs-tree-file", {".git/HEAD": b"ref: refs/heads/main\\n"})):'''
new='''    got = refusal_any(lambda: ts_run({"node_modules/left-pad/.git-like/index.js": b"module.exports = 1;\\n"}))
    row("A4", "real-run-package-vcs-lookalike-remains-lawful", got is None, got)
    for name, extra in (("an-unlisted-dependency-file", {"node_modules/unlisted/index.js": b"module.exports = 2;\\n"}),
                        ("a-vcs-tree-file", {".git/HEAD": b"ref: refs/heads/main\\n"}),
                        ("listed-package-nested-git-metadata", {"node_modules/left-pad/.git/HEAD": b"ref: refs/heads/main\\n"}),
                        ("listed-package-nested-mercurial-metadata", {"node_modules/left-pad/.hg/store/data": b"metadata\\n"})):'''
assert s.count(old)==1;p.write_text(s.replace(old,new));rows[-1]['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
edit('docs/v2/contracts/product-v1/identity-and-evidence.md',
'''build-output row is never a read input of any published universe. Either violation
refuses `SNAPSHOT_PRUNED_TREE_NOT_A_READ`.''',
'''build-output row is never a read input of any published universe. A dependency
package's read allowance never overrides a VCS-tree exclusion deeper in that path;
the VCS exclusion uses exact segments at every depth. Either violation refuses
`SNAPSHOT_PRUNED_TREE_NOT_A_READ`.''')
(O/'correction.json').write_text(json.dumps({'standing':'Root correction of a reproduced A4 nested-VCS exception. Actual Claude focused review and final source review pending. No registered schema bytes change, product qualification or readiness.', 'files':rows,'checksAdded':5},indent=2)+'\n')
print('Corrected nested VCS exclusions, added5 focused controls and explicit prose.')
