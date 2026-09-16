import hashlib
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
ep=S+'/src25/docs/coop/design-corrections/foundation/enumeration_model.v1.py'
esrc=open(ep,encoding='utf-8').read()
before=hashlib.sha256(esrc.encode()).hexdigest()
NL=chr(10)
old_f='    "ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION",'+NL
assert esrc.count(old_f)==1, esrc.count(old_f)
esrc=esrc.replace(old_f, old_f+'    "ENUMERATION_MEMBERSHIP_UNIT_ROOT",'+NL, 1)
HELPER='def _admit_membership_unit_roots(membership, faults: list[str]) -> bool:\n    """Decide the INTERNAL root representation of the membership units BEFORE any binding join.\n\n    The single authority is the native selector (NV.admit_unit_roots, reading\n    #/$defs/InternalUnitRootV1 and #/$defs/CanonicalRelativeDirV1); this function only translates\n    that decision into this model\'s internal fault vocabulary. Without it, a unit whose root is\n    spelled with the EXTERNAL sentinel \'.\' reaches _unit_for_cell, which then matches no unit, so\n    _u1_entry derives None and the mismatch against the retained\n    TypeScriptConfigGraphV1.entryConfigPath is reported as ENUMERATION_BINDING_PROGRAM_ENTRY: a\n    real refusal attributed to the wrong field. ENUMERATION_MEMBERSHIP_UNIT_ROOT is an INTERNAL\n    fault key only; it adds no public D9 code and no public route.\n    """\n    units = membership.get(\'units\') if isinstance(membership, dict) else None\n    if units is None:\n        return True\n    try:\n        NV.admit_unit_roots(units)\n    except NV.AdmissionError:\n        _add(faults, \'ENUMERATION_MEMBERSHIP_UNIT_ROOT\')\n        return False\n    return True\n\n\ndef admit_enumeration(\n'
old_d='def admit_enumeration('+NL
assert esrc.count(old_d)==1, esrc.count(old_d)
esrc=esrc.replace(old_d, HELPER, 1)
old_c='    _membership_covers_snapshot(membership, snapshot_paths, faults)'+NL
assert esrc.count(old_c)==1, esrc.count(old_c)
new_c='    if not _admit_membership_unit_roots(membership, faults):'+NL+'        empty["refusals"] = faults'+NL+'        return empty'+NL+NL+old_c
esrc=esrc.replace(old_c, new_c, 1)
open(ep,'w',encoding='utf-8').write(esrc)
print('before',before)
print('after ',hashlib.sha256(esrc.encode()).hexdigest())
