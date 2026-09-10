"""Apply the SAME reordering mutation the first coauthor session used - the at-most-one guard moved
verbatim to below the payload match - to THIS peer proposal's workflows_model.v1.py. Must be a pure
transposition: identical multiset of bytes, length delta 0.
"""
import sys
from pathlib import Path
SRC,DST=Path(sys.argv[1]),Path(sys.argv[2])
t=SRC.read_text()
GUARD="""    if len(rows) > 1:
        raise Refusal('CONFIG.INVALID', 'CONFIG.INVALID',
                      'the analysis spec selects more than one ScopeDocumentV1 parameter; state exactly one',
                      subject='parameters[schemaDigest=' + document + ']x' + str(len(rows)))
"""
MATCH="""    if not any(row.get('payloadDigest') == digest for row in rows):
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH',
                      'the supplied scope document is not the selected scope parameter')
"""
BLOCK=GUARD+MATCH
if t.count(BLOCK)!=1:raise SystemExit('REFUSED: guard+match block occurs %d times'%t.count(BLOCK))
out=t.replace(BLOCK,MATCH+GUARD)
assert len(out)==len(t),'not length preserving'
assert sorted(out)==sorted(t),'not a pure transposition'
DST.write_text(out)
print('transposed guard below payload match; length delta',len(out)-len(t),
      '; differing characters',sum(1 for a,b in zip(t,out) if a!=b))
