"""S10-TSC scratch binding: the product's verify_design.verify on the candidate worktree, with the candidate lock plus
one synthetic appended contract-successor entry for this unit (a synthetic ACCEPT-DESIGN-UNIT review and root assent,
written to a scratch directory under the architecture root and removed afterwards). It proves the package binds and
that the candidate's generation and admission sources select its copies; it is not acceptance. Also runs the base lock
against the candidate tree, which must refuse (the S10 copies are not yet selected)."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, shutil

U = 'docs/implementation/m3/config-discovery-b/s10-tsc'
SCRATCH = 'docs/implementation/m3/reviews/scratch-s10-tsc-synthetic'


def pin(root, path):
    raw = (root / path).read_bytes()
    return dict(path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--architecture', type=Path, required=True)
    ap.add_argument('--product', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    arch, product = a.architecture, a.product
    spec = importlib.util.spec_from_file_location('candidate_verify_design', product / 'tools/verify_design.py')
    vd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vd)
    lock = json.loads((product / 'design-lock.json').read_text())
    out = {}
    try:
        vd.verify(arch, lock, product)
        out['baseLockCandidateTree'] = 'PASS (unexpected)'
    except vd.DesignError as e:
        out['baseLockCandidateTree'] = 'REFUSED: ' + str(e)
    scratch = arch / SCRATCH
    assert not scratch.exists()
    scratch.mkdir(parents=True)
    try:
        subject = pin(arch, U + '-subject.json')
        record = pin(arch, U + '/successor.json')
        (scratch / 'review.json').write_text(json.dumps(dict(verdict='ACCEPT-DESIGN-UNIT', requiredFindings=[],
                                                             subjectManifestSha256=subject['sha256'], synthetic=True), indent=2) + '\n')
        review = pin(arch, SCRATCH + '/review.json')
        (scratch / 'assent.json').write_text(json.dumps(dict(
            schemaVersion=1, unit='S10-TSC', status='ACCEPTED-DESIGN-UNIT', rootSubstantiveAssent=True, subjectManifest=subject,
            independentReview=review, acceptedSuccessor=record, requiredUnitFindings=[], synthetic=True), indent=2) + '\n')
        entry = dict(record=record, subjectManifest=subject, review=review, assent=pin(arch, SCRATCH + '/assent.json'))
        lock['contractSuccessors'].append(entry)
        result = vd.verify(arch, lock, product)
        out.update(withS10TSC='PASS' if result.get('passed') else 'FAIL', contractSuccessors=len(lock['contractSuccessors']),
                   generationSources=result.get('generationSources'), admissionSources=result.get('admissionSources'))
    except vd.DesignError as e:
        out['withS10TSC'] = 'REFUSED: ' + str(e)
    finally:
        shutil.rmtree(scratch)
    a.out.write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(out))


if __name__ == '__main__':
    main()
