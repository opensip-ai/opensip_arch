"""Surgical, exact-anchor replacement of ONE docstring paragraph and ONE inline comment block in
workflows/workflows_model.v1.py. Starts from the FROZEN v20 file, not from the first proposal, so
the two edits are independently auditable. Refuses unless each anchor occurs exactly once.
"""
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
DST = Path(sys.argv[2])
text = SRC.read_text()

# --- edit 1: the docstring's CARDINALITY paragraph -------------------------------------------
DOC_OLD = """    scope policy, and that refusal is unchanged. MORE THAN ONE is refused before any payload
    comparison, because this verifier is EXISTENTIAL over the selected rows and two distinct
    entries each satisfy it, so a `verified` digest would prove selection of one document while
    another was equally selected. The foundation closure refuses the same spec independently; this
    check exists so a DIRECT caller is not relying on that closure having run in this process."""

DOC_NEW = """    scope policy, and that refusal is unchanged. MORE THAN ONE is REFUSED, because this verifier
    is EXISTENTIAL over the selected rows and two distinct entries each satisfy it, so without the
    refusal a `verified` digest would prove selection of one document while another was equally
    selected. That is why the refusal EXISTS. SEPARATELY, it is placed before the payload
    comparison, and that placement decides only which true reason a caller holding NEITHER
    candidate is given; both candidates are refused under either placement. See the note at the
    guard itself. The foundation closure refuses the same spec independently; this check exists so
    a DIRECT caller is not relying on that closure having run in this process."""

# --- edit 2: the inline comment above the at-most-one guard -----------------------------------
CMT_OLD = """    # AT MOST ONE, checked BEFORE the payload match and independently of the foundation closure
    # (CB8-MUST-1). This function is reachable directly - `adopt_baseline(..., analysis_spec=...)`
    # is one caller and a host verifying a retained spec is another - so it may see a spec no Run
    # closure in this process admitted, and it must not rely on that closure having run. Order is
    # the point: checking the digest first would let a caller who happens to hold one of two
    # candidate documents obtain a `verified` digest, which is precisely the existential proof that
    # made two spec entries indistinguishable. Both entries satisfy `any(...)` separately, so the
    # ambiguity has to be refused before the match is attempted, not after."""

CMT_NEW = """    # AT MOST ONE, checked BEFORE the payload match and independently of the foundation closure
    # (CB8-MUST-1). This function is reachable directly - `adopt_baseline(..., analysis_spec=...)`
    # is one caller and a host verifying a retained spec is another - so it may see a spec no Run
    # closure in this process admitted, and it must not rely on that closure having run.
    #
    # WHAT THE GUARD'S EXISTENCE DECIDES AND WHAT ITS POSITION DECIDES ARE TWO DIFFERENT THINGS.
    # EXISTENCE: with no such guard at all, a caller holding EITHER of the two candidates would
    # obtain a `verified` digest, because the existential match below succeeds for each of them
    # separately - precisely the proof that made two spec entries indistinguishable. That is why
    # the guard is here, and it is the whole of the soundness argument.
    # POSITION: moving it BELOW the payload match would NOT reopen that hole. A candidate holder
    # matches its own row, the match falls through without returning, and the ambiguity is still
    # reached and still refuses. What the later position changes is the answer given to a caller
    # holding NEITHER candidate: the match fails first, and a spec that selects two scope
    # parameters is reported as BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH - an ordinary statement
    # about the supplied document - when the defect belongs to the SPEC ALONE and no document
    # could have satisfied it. Position decides WHICH TRUE REASON is returned, not soundness.
    #
    # THE PRECEDENCE CLAIMED HERE IS EXACTLY ONE: ambiguity outranks the PAYLOAD-DIGEST MATCH for a
    # scope document this function has already digested. It is NOT precedence over admission in
    # general, and nothing here says ambiguity is answered first unconditionally. `doc_digest(scope)`
    # runs ABOVE, before the rows are even counted, so a scope argument that does not canonicalise
    # raises from there and never reaches this guard - the SAME ambiguous spec then answers with a
    # canonicalisation AdmissionError rather than CONFIG.INVALID. Admission earlier in
    # `adopt_baseline` - authority, then availability - likewise still precedes this function
    # entirely. The identity controls named
    # `an-ambiguous-spec-refuses-as-ambiguous-even-for-a-document-that-is-neither-candidate` and
    # `the-three-answers-for-one-non-candidate-document-stay-distinct-by-row-multiplicity` hold
    # this order; the two-candidate controls pass under either position and do not hold it."""

for old, new, label in ((DOC_OLD, DOC_NEW, 'docstring'), (CMT_OLD, CMT_NEW, 'comment')):
    n = text.count(old)
    if n != 1:
        raise SystemExit('REFUSED: anchor for %s occurs %d times, expected exactly 1' % (label, n))
    text = text.replace(old, new)
    print('replaced %s anchor (1 occurrence)' % label)

DST.write_text(text)
print('wrote', DST, DST.stat().st_size, 'bytes')
