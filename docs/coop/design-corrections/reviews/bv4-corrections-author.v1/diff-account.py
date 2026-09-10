"""Complete diff account of the development copy against the frozen accepted v13 snapshot."""
import hashlib,json,sys,pathlib
BASE=pathlib.Path('/tmp/opensip-design-corrections/candidate-subject.v13')
WORK=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else
                  '/tmp/opensip-design-corrections/bv4-corrections-author.v1/work')
def tree(root):
    return {str(p.relative_to(root)):p for p in root.rglob('*') if p.is_file()}
b,w=tree(BASE),tree(WORK)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed=[{'path':k,'beforeSha256':sha(b[k]),'afterSha256':sha(w[k]),
          'beforeBytes':b[k].stat().st_size,'afterBytes':w[k].stat().st_size}
         for k in sorted(b) if k in w and sha(b[k])!=sha(w[k])]
out={'baseFileCount':len(b),'workFileCount':len(w),
     'added':sorted(set(w)-set(b)),'deleted':sorted(set(b)-set(w)),
     'changedFiles':changed,'changedCount':len(changed)}
print(json.dumps(out,indent=1))
