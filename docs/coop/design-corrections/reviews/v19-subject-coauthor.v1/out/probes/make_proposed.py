"""Produce workflow.proposed.py from the exact frozen18 bytes. One site, one conditional."""
import hashlib
import pathlib

ROOT = pathlib.Path('/tmp/opensip-design-corrections/v19-subject-coauthor.v1')
before = (ROOT / 'workflow.before.py').read_text(encoding='utf-8')

OLD = """    def dd(t, remedy='see contract'):
        if detail:
            t['domainDetail'] = {'code': detail, 'remedy': obs.get('remedy', remedy)}
        return t
"""
NEW = """    def dd(t, remedy='see contract'):
        if detail:
            t['domainDetail'] = {'code': detail, 'remedy': obs.get('remedy', remedy)}
            # The DYNAMIC half of the disclosure, carried when the observation actually has one.
            # The public detail vocabulary is CLOSED and the workflows contract says what carries the
            # rest: \"Dynamic paths or refusal explanations travel in bounded `subject`/`remedy`
            # fields, never as newly invented codes.\" This rebuilt the DomainDetail field by field
            # and copied only two of the three, so a producer whose whole promise is its subject lost
            # it at the envelope. Native section 14's bounded selection refusal is the live case: it
            # promises `field:count>limit` and that \"the subject always names which one overflowed\",
            # and without this line every bounded field arrived as the same indistinguishable
            # PROJECT.SCOPE_LIMIT - leaving a caller who needs to know WHICH bound was hit with only
            # the new code that same sentence forbids.
            #
            # `Refusal.termination()` above already carries a subject onto the identical shape. Two
            # producers of one record disagreeing about one of its fields is the defect; this is that
            # existing rule applied at the observation boundary, not a new one, and the truthiness
            # test is deliberately the same one `Refusal.termination()` uses so the two agree on
            # every input including the empty string.
            #
            # STRICTLY ADDITIVE: an observation carrying no subject produces the byte-identical
            # termination it produced before. `subject` is an already-published optional
            # `BoundedText` on the common-schema DomainDetail, so nothing here needs a schema, code
            # or contract change. What this does NOT do is admit the value: a malformed trusted
            # observation supplying a non-string or over-length subject yields a DomainDetail the
            # published schema refuses, exactly as it does for a malformed `remedy` or `detail`, and
            # this line makes no admission claim on its behalf.
            if obs.get('subject'):
                t['domainDetail']['subject'] = obs['subject']
        return t
"""
assert before.count(OLD) == 1, 'anchor'
after = before.replace(OLD, NEW)
(ROOT / 'workflow.proposed.py').write_text(after, encoding='utf-8')
print('before', hashlib.sha256(before.encode()).hexdigest())
print('after ', hashlib.sha256(after.encode()).hexdigest())
print('added lines', after.count('\n') - before.count('\n'))
