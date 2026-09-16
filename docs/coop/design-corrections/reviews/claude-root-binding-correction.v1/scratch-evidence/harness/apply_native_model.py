
import hashlib,sys
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
p=S+'/src25/docs/coop/design-corrections/native/native_evidence_model.v2.py'
src=open(p,encoding='utf-8').read()
before=hashlib.sha256(src.encode()).hexdigest()

HELPER = '''AdmissionError = C.AdmissionError

# The INTERNAL unit-root representation, READ from the published schema selectors rather than
# restated here, so the model and the schema document cannot drift apart: InternalUnitRootV1 is
# the empty string (project root) or a CanonicalRelativeDirV1, and the EXTERNAL sentinel "." is
# never a retained value of WorkspaceUnitV2.rootPath.
UNIT_ROOT_SELECTOR = "#/$defs/InternalUnitRootV1"
MEMBER_ROOT_SELECTOR = "#/$defs/CanonicalRelativeDirV1"
UNIT_ROOT_FAULT = "NATIVE_UNIT_ROOT_REPRESENTATION"
_UNIT_ROOT_RE = re.compile(SCHEMAS["$defs"]["InternalUnitRootV1"]["pattern"])
_MEMBER_ROOT_RE = re.compile(SCHEMAS["$defs"]["CanonicalRelativeDirV1"]["pattern"])


def admit_unit_roots(units: list[dict]) -> list[dict]:
    """Decide the INTERNAL root representation of every unit BEFORE membership, path slicing or
    enumeration binding reads it. Returns `units` unchanged so a caller may wrap its argument.

    ORDERING IS THE POINT. `_under_unit`, `_rel` and the deepest-unit `len(rootPath)` ranking all
    consume this field as an exact string prefix, and not one of them fails loudly on a
    non-internal spelling. With "." every `_under_unit` test is false, so the unit silently owns
    no file and the run is an empty but schema-valid analysis; `_rel` slices `len(root) + 1`
    characters and returns corrupted relative paths; `unit_scope_descriptor` spells "." back out
    through `DD.spell_root`, where it is indistinguishable from a correct project root; and
    enumeration binding reaches `_unit_for_cell` -> None and reports
    ENUMERATION_BINDING_PROGRAM_ENTRY, which blames a different field. Deciding the representation
    first replaces all four outcomes with one refusal that names the offending root.

    BOUNDARY. `units` is HOST-GENERATED at this point: it is `discover_units` output, which already
    emits the internal form and schema-validates each unit. A violation here is therefore a broken
    host invariant about this caller's input and is raised as an AdmissionError, exactly like the
    membership totality invariant at the end of `assign_membership`. It is deliberately NOT a
    `ReferenceEnvironmentError`, which is reserved for a host that cannot produce a conforming
    answer at all, and it is deliberately NOT a new public D9 route: the EXTERNAL spelling boundary
    already exists and is untouched here, because Config2 `discovery.workspaceRoots` and CLI
    `--workspace-root` are normalized inward by `DD.normalize_explicit_root` and a malformed one is
    the typed public refusal `native.explicit-root-grammar` (CONFIG.INVALID). The classification is
    decided by WHICH BOUNDARY the value crossed, never by a spelling, a file name or a message
    prefix.
    """
    if not isinstance(units, list):
        raise AdmissionError(UNIT_ROOT_FAULT + ":units:not-a-list")
    for i, u in enumerate(units):
        if not isinstance(u, dict):
            raise AdmissionError(UNIT_ROOT_FAULT + ":units[%d]:not-an-object" % i)
        root = u.get("rootPath")
        if not isinstance(root, str) or _UNIT_ROOT_RE.match(root) is None:
            raise AdmissionError("%s:units[%d].rootPath:%s:%r" % (UNIT_ROOT_FAULT, i, UNIT_ROOT_SELECTOR, root))
        members = u.get("memberPackageRoots")
        if members is None:
            continue
        if not isinstance(members, list):
            raise AdmissionError(UNIT_ROOT_FAULT + ":units[%d].memberPackageRoots:not-a-list" % i)
        for j, m in enumerate(members):
            if not isinstance(m, str) or _MEMBER_ROOT_RE.match(m) is None:
                raise AdmissionError("%s:units[%d].memberPackageRoots[%d]:%s:%r"
                                     % (UNIT_ROOT_FAULT, i, j, MEMBER_ROOT_SELECTOR, m))
    return units
'''

anchor = "AdmissionError = C.AdmissionError\n"
assert src.count(anchor) == 1, src.count(anchor)
src = src.replace(anchor, HELPER, 1)

edits = [
 ('def assign_membership(units: list[dict], files: list[str], boundaries: dict | None = None) -> dict:',
  '    if boundaries is not None:\n        validate_native("AdmittedBoundaryInventoryV1", boundaries)\n    rows: list[dict] = []; unsupported: list[str] = []; outside: list[str] = []\n',
  '    admit_unit_roots(units)   # internal root representation decided BEFORE any prefix test or slice\n    if boundaries is not None:\n        validate_native("AdmittedBoundaryInventoryV1", boundaries)\n    rows: list[dict] = []; unsupported: list[str] = []; outside: list[str] = []\n'),
 ('def unit_scope_descriptor',
  '    if boundaries is not None:\n        validate_native("AdmittedBoundaryInventoryV1", boundaries)\n    roots = sorted({u["rootPath"] for u in units}, key=lambda x: x.encode("utf-8"))\n',
  '    admit_unit_roots(units)   # decided BEFORE DD.spell_root makes a wrong root indistinguishable\n    if boundaries is not None:\n        validate_native("AdmittedBoundaryInventoryV1", boundaries)\n    roots = sorted({u["rootPath"] for u in units}, key=lambda x: x.encode("utf-8"))\n'),
]
for name, old, new in edits:
    assert src.count(old) == 1, (name, src.count(old))
    src = src.replace(old, new, 1)
open(p,'w',encoding='utf-8').write(src)
print('before',before)
print('after ',hashlib.sha256(src.encode()).hexdigest())
