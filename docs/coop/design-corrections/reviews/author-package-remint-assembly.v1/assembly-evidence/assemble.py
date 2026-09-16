from pathlib import Path
import shutil,subprocess,json,hashlib
B=Path('/tmp/opensip-design-corrections');OLD=B/'claude-author-package-successor.v1';P=B/'claude-author-package-successor.v2';A=B/'claude-author-remint.v1/scratch';O=Path(__file__).parent
assert not P.exists();subprocess.run(['cp','-cR',str(OLD),str(P)],check=True)
H=P/'historical-source25-preparation';H.mkdir()
historic=['README.md','AUTHOR-STANDING.md','review-request.md','review-queue.json','author-properties.json','author-properties.before-f8.json','mixed-universe-view.probe.json','query-checks1','source-manifest.json','checkpoint3','normalized-examples6','rust-selection-examples1','semantic-controls1','checkpoint3-owner','normalized-examples6-owner','rust-selection-examples1-owner','semantic-controls1-owner']
for name in historic:shutil.move(P/name,H/name)
for rel,name in [('a-checkpoint3/checkpoint3','checkpoint3'),('b-normalized/normalized-examples6','normalized-examples6'),('c-rust-selection/rust-selection-examples1','rust-selection-examples1'),('d-controls/semantic-controls1','semantic-controls1'),('e-binding-controls','binding-controls')]:shutil.copytree(A/'out-a'/rel,P/name)
for f in (A/'portable').glob('*.py'):shutil.copyfile(f,P/f.name)
for f in (A/'helpers-overlay').glob('*.py'):shutil.copyfile(f,P/'author-helpers'/f.name)
for name in ['author-properties.json','mixed-universe.json','query-assessment.json']:
 shutil.copyfile(A/'evidence/probes-a'/name,P/('mixed-universe-view.probe.json' if name=='mixed-universe.json' else name))
shutil.copytree(A/'evidence/probes-a/query-checks1',P/'query-checks1')
shutil.copyfile(A/'evidence/control-diff-a.json',P/'semantic-controls1/assessment.json')
shutil.copytree(B/'root-author-remint-verification.v1',P/'root-replay-verification')
shutil.copyfile(B/'claude-author-remint.v1/source-manifest.json',P/'source-manifest.json')
shutil.copyfile(A/'COMMANDS.md',P/'author-delivery-commands.md')
shutil.copyfile(B/'claude-author-remint.v1/review.md',P/'claude-author-remint-review.md')
# The portable command currently allows a fresh output below its declared inputs despite its
# documented promise. Refuse overlap before fresh_out() can create anything.
q=P/'author_portable.py';raw=q.read_text();(O/'author_portable.before.py').write_text(raw)
needle='    return a\n';assert raw.count(needle)==1
insert='''    inputs = [a.source, a.package, a.kit, a.helpers or a.package / HELPERS_DIRNAME]
    for path in inputs:
        path = path.resolve()
        if a.out == path or a.out.is_relative_to(path) or path.is_relative_to(a.out):
            raise SystemExit('--out must be separate from every declared input: %s' % path)
    return a
'''
q.write_text(raw.replace(needle,insert))
# Keep original source25 verifier as history; current verifier is bound to this exact
# intermediate source. Final whole-design binding is a later freeze operation.
q=P/'verify-package.py';raw=q.read_text();(H/'verify-package.py').write_text(raw)
sourcehash=hashlib.sha256((P/'source-manifest.json').read_bytes()).hexdigest()
q.write_text(raw.replace('fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d',sourcehash))
(P/'README.md').write_text('''# Mutable author remint package — final review pending

Seven positive synthetic Runs and three semantic refusal controls were rebuilt with actual Claude on the merged native schema. Root independently replays the exact exports through the selected reference owner; all seven positives admit, all three negatives structurally admit and fail at complete-proof replay. Binding controls also demonstrate a lawful default, a refused non-null default entry and a lawful single explicit selection.

The current source manifest binds the intermediate merged reference snapshot, not final candidate26. Final carrier/lifecycle integration and independent review remain pending. No product qualification or implementation authorization is claimed.

The four construction commands and build-binding-controls.py take explicit --source, --package and fresh --out paths. The patched bundled helpers are required; the commands supply their kit binding before import. Example: `python -I -B build-checkpoint3.py --source <source> --package <this-package> --out <fresh-outside-inputs>`. Source, package, kit and helper inputs cannot contain the output. The current package artifact manifest will be written only after root checks and final source selection.

Checkpoint3 compares the author helper with the reference owner; the other six positives have the owner both derive and replay proof, establishing self-consistency. These Runs exercise exists/none only. and/or/not remain unexercised; count-at-most/all-covered remain unimplemented in the partial helper. The attempted two-binding construction is incomplete and demonstrates no owner defect; the explicit-selection control is single-binding only.

The original 123/8/3 blind charter is unchanged. This author package must never be provided to a consumer described as blind. Historical source25 preparation is retained under historical-source25-preparation; the original source25 thirty-residual author assessment remains historical proposed evidence with independent grades pending. Earlier immutable packages and failed reviews are unchanged. The latest Claude report and root exact-export reports are included as evidence, not self-acceptance.
''')
(O/'assembly.json').write_text(json.dumps({'standing':'Mutable author successor assembly; final manifest, current source binding and independent review pending','package':str(P),'sourceManifestSha256':sourcehash,'nativeSchemaSha256':'673a9bf8b3d1d0d3643d0fdd75813a6fa14d362d792e90d0ddd5f63e16a6bbe2','additionalRootCorrection':'Refuse output overlapping any declared input before creating it'},indent=2)+'\n')
print('Assembled',P)
