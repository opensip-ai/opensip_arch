"""Author edit: add the S12 public-detail projection (blind consumer M-5) to the security model."""
import json, sys
from pathlib import Path
R = Path(sys.argv[1]); p = R / 'docs/coop/design-corrections/security/security_lifecycle_model_v1.py'
codes = json.loads(Path('/tmp/opensip-design-corrections/blind-corrections-author.v1/evidence/closed-detail-set.json').read_text())
lines = []
for i in range(0, len(codes), 3):
    lines.append('    ' + ' '.join("'%s'," % c for c in codes[i:i + 3]))
literal = '\n'.join(lines).rstrip(',')

block = '''

# ---------------------------------------------------------------------------------------------
# S12 - projecting a security outcome onto the ONE closed public DomainDetail  (blind consumer M-5)
# ---------------------------------------------------------------------------------------------
# A public termination carries exactly one `domainDetail` = {code, remedy, subject?} where `code` is a
# member of the single closed registry (`../public-detail-registry.v1.json`, mirrored by
# workflows/schemas/common.schema.json#/$defs/DomainDetailCode). This unit therefore states its OWN
# closed vocabulary here and refuses to emit anything outside it; there is no wildcard family and no
# open `PROFILE_SET.*` prefix rule.
#
# The projection rule, which is the rule these bytes already follow:
#   1. The BASE CODE is everything before the first ':'; everything after it is subject data.
#      ('ROOT.ROLE_SET:1' -> code ROOT.ROLE_SET, subject '1'.)
#   2. If a `detail` is present and its base code is in this closed set, that is the public code and
#      the rest of the detail is the subject. This is why the 38 ROOT.* document defects are public
#      codes rather than collapsing into one PAYLOAD-NOT-ADMISSIBLE, and it is exactly why the
#      ENVELOPE.* / PROFILE_SET.* defects of `admit_profile_set_envelope` must be registered too:
#      they occupy the same position for the same reason (S9.1 names them as `detail`).
#   3. Otherwise the `refusal` supplies the public code and the whole `detail` travels as subject.
#      This is the reading S12 already uses for RECOVERY.REFUSED (CHALLENGE_EXPIRED, COUNTER_MISMATCH,
#      ...), for CONFIG.CUSTODY_REFUSED (SYMLINK, WRITABLE_BY_OTHERS, ...) and for
#      PROJECT.EXPLICIT_PATH_INVALID (JOIN_PATH_GRAMMAR, ...). Those sub-details are NOT registry
#      members and must not become a second public vocabulary.
#   4. Anything else refuses. An unknown internal key never reaches a public envelope.
# The D9 class/exit/code always comes from the `refusal`, never from the detail: naming a defect more
# precisely never changes its termination branch.
SECURITY_PUBLIC_DETAIL_CODES = frozenset({
@@CODES@@
})

# The nine codes above that the shared registry does not yet carry. They are emitted by
# `admit_profile_set_envelope` today and are named normatively by S9.1/S12. The registry and the typed
# workflow enum are owned elsewhere, so this unit lists them and the checker asserts the gap never grows.
PENDING_PUBLIC_DETAIL_REGISTRATIONS = frozenset({
    'ENVELOPE.BODY_DIGEST', 'ENVELOPE.KIND', 'ENVELOPE.SHAPE',
    'PROFILE_SET.CANON', 'PROFILE_SET.CORE_PIN_MISMATCH', 'PROFILE_SET.NO_TR_PROFILE_ROLE',
    'PROFILE_SET.SCHEMA', 'PROFILE_SET.SCHEMA_SHAPE', 'PROFILE_SET.SIGNATURE_THRESHOLD',
})

# Internal decision keys this unit produces that are NOT public codes; the host normalizes them at the
# boundary exactly as it normalizes the native aliases. `PROFILE_SET_KEY_NOT_MACHINE_ID` is deliberately
# absent: it is not an alias but a SUBJECT sub-detail of the registered NT-TCB-PROFILE-UNQUALIFIED (S8).
SECURITY_INTERNAL_DETAIL_ALIASES = {
    'RF-6:AUTHORIZATION.GRANT_NOT_CURRENT': 'TRUST.COMPONENT_REVOKED_DURING_OPERATION',
}


def public_detail_split(text):
    """(base code, subject or None). The subject is everything after the FIRST colon."""
    if not isinstance(text, str) or not text:
        raise Reject('PUBLIC_DETAIL_EMPTY')
    base, sep, subject = text.partition(':')
    return base, (subject if sep else None)


def public_detail(refusal, detail=None, remedy=None):
    """Project one security refusal onto the closed public DomainDetail plus its D9 branch."""
    alias = SECURITY_INTERNAL_DETAIL_ALIASES.get(refusal)
    if alias is not None:
        refusal, detail = alias, (detail if detail is not None else refusal)
    refusal_base, refusal_subject = public_detail_split(refusal)
    if detail is not None:
        detail_base, detail_subject = public_detail_split(detail)
        if detail_base in SECURITY_PUBLIC_DETAIL_CODES:
            code, subject = detail_base, detail_subject
        elif refusal_base in SECURITY_PUBLIC_DETAIL_CODES:
            code, subject = refusal_base, detail
        else:
            raise Reject('PUBLIC_DETAIL_UNREGISTERED:' + detail_base)
    elif refusal_base in SECURITY_PUBLIC_DETAIL_CODES:
        code, subject = refusal_base, refusal_subject
    else:
        raise Reject('PUBLIC_DETAIL_UNREGISTERED_REFUSAL:' + refusal_base)
    out = {'code': code, 'subject': subject,
           'd9': d9(refusal_base) if refusal_base in D9 else d9('PAYLOAD-NOT-ADMISSIBLE'),
           'pendingRegistration': code in PENDING_PUBLIC_DETAIL_REGISTRATIONS}
    if remedy is not None:
        out['remedy'] = remedy
    return out


def public_details(outcome, refusal_key=None):
    """Every public DomainDetail a model outcome projects to.

    Two emitted shapes are covered: `{refusal, detail}` records (root/profile-set/envelope/storage
    admission, clock decisions) and `{refusals: [...]}` lists (grant, plan-projection, repair,
    recovery and transition admission), whose entries already carry their own base code and whose D9
    branch comes from the enclosing `refusal_key`.
    """
    if not isinstance(outcome, dict):
        raise Reject('PUBLIC_DETAIL_OUTCOME_SHAPE')
    items = []
    for entry in outcome.get('refusals') or ():
        items.append(public_detail(refusal_key or entry, None if refusal_key is None else entry))
    if outcome.get('refusal') is not None:
        items.append(public_detail(outcome['refusal'], outcome.get('detail')))
    return items
'''.replace('@@CODES@@', literal)

s = p.read_text()
anchor = "\nclass Reject(Exception):\n    pass\n"
assert anchor in s
# the projection needs `d9`, `D9` and `Reject`, all defined above the helpers section
marker = "\n# ---------------------------------------------------------------------------------------------\n# Helpers\n# ---------------------------------------------------------------------------------------------"
assert marker in s
s = s.replace(marker, block + marker, 1)
p.write_text(s)
print('inserted', len(block.splitlines()), 'lines')
