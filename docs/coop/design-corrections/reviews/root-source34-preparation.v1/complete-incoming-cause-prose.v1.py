from pathlib import Path
import argparse,json,hashlib,difflib
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True)
rel='docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md';p=a.source/rel;before=p.read_text();s=before
old="""An owed **same-family** unavailable binding is a different case and stays **blocking** incoming: P1
emits `unavailable-program-binding` for it, and it makes the incoming result `unknown`, because a
selected program that did not run cannot have searched."""
new="""An unavailable binding whose family **is owed** (the same family or an unknown family under the
shared rule) stays **blocking** incoming: P1 emits `unavailable-program-binding` for it, and it makes
the incoming completeness result `unknown`."""
assert s.count(old)==1;s=s.replace(old,new)
old="""The remaining incoming emissions are: `population-unknown` with `universe: S` when expected source
ids are unknown, as the incoming paragraph below already requires; `uncovered-expected-source-subject`
with `universe: S` when an expected source id appears in no source scope;
`source-target-search-unattested` with `universe: S` under the **Search of U** paragraph below; and
`scope-without-coverage` with `universe: S` for a scope group with no Coverage and no attestation.
`coverage-unknown` is emitted by the same shared sufficiency rule as outgoing step 4."""
new="""The remaining population emissions are `population-unknown` with `universe: S` when expected
source ids are unknown, and `uncovered-expected-source-subject` with `universe: S` when an expected
source id appears in no source scope.

For the search-accounting cases below, a **qualifying attestation** is a matching, globally admitted,
provider-owned `IncomingSearchV1` with `completeSearch=true`, `coverage=complete`, and both its
`examinedExhaustive` and `resolutionCompleteness.examinedExhaustive` true. Its shared sufficiency
view is still evaluated; qualification alone does not establish sufficiency. Evaluate every paired
Coverage as required below, then apply these cases:

| Search-accounting case | Cause, with `universe: S` |
|---|---|
| Selected provider group has no source scopes and no qualifying attestation | `source-target-search-unattested` |
| Represented source scope has paired Coverage only at *S→V* (*V*≠*U*), and no qualifying attestation for *S→U* | `source-target-search-unattested` |
| Represented source scope has no paired Coverage at all, and no qualifying attestation | `scope-without-coverage` |

A represented scope with paired *S→U* Coverage or a qualifying attestation emits neither of those
two search-accounting causes; all other completeness and sufficiency causes remain. In particular,
a present but admitted non-qualifying attestation is insufficient under the same cases as an absent
one. `coverage-unknown` is emitted by the shared sufficiency rule in outgoing step 4, including when
an attestation's view fails sufficiency."""
assert s.count(old)==1;s=s.replace(old,new)
old='Missing/unadmitted/non-exhaustive attestation ⇒ `source-target-search-unattested`.'
new='An absent or admitted non-qualifying attestation cannot establish search; the incoming search-accounting cases above determine the emitted cause. A schema-invalid or misjoined attestation is a global admission refusal, not an accepted unknown search.'
assert s.count(old)==1;s=s.replace(old,new)
old="""   entire entry** and considers each later partition in turn; a later partition changes the result
   only where it is **strictly worse**, so every tie retains what is already there — the earliest
   partition in selection order. Field by field:"""
new="""   entire entry** and considers each later partition in turn. Ranked replacements occur only on a
   **strictly worse** rank; ties retain the incumbent whole value. The minimum, union and carrier
   rules are specified separately below. Field by field:"""
assert s.count(old)==1;s=s.replace(old,new)
old="""   lost the fold. Each rank above is a total order on the **admitted** enum, so an admitted
   partition set always folds to an admitted value."""
new="""   lost the fold. The fixed precedence above includes the stated complete/not-applicable tie;
   tie handling never independently merges fields from the tied records."""
assert s.count(old)==1;s=s.replace(old,new)
(a.out/'before.md').write_text(before);p.write_text(s);(a.out/'after.md').write_text(s);(a.out/'change.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile='author-v2',tofile='root-prose-completion')))
sha=lambda b:hashlib.sha256(b).hexdigest();(a.out/'change.json').write_text(json.dumps({'standing':'Root architecture prose correction matching existing reference branch and measured atom/attestation controls; fresh frozen independent review still required. No reference behavior/schema/token change or acceptance.','path':rel,'beforeSha256':sha(before.encode()),'afterSha256':sha(s.encode()),'basis':'root-atom-cause-draft-review.v2/incoming.stdout.json','rootAssent':False},indent=2)+'\n');print('Applied explicit incoming cause-accounting prose; independent review pending')
