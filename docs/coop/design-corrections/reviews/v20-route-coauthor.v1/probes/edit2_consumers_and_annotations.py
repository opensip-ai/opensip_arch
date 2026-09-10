"""EDIT 2 (item 1): consumer updates and emission-site annotation for the registration.

Every replacement asserts it matched EXACTLY ONCE, so a silent miss is impossible.
No executable behaviour is changed by this file: the two count constants move 287 -> 289 because
the registry really does have 289 members now, and the rest is comment/annotation text stating the
law that edit 1 selected.
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
applied = []


def sub(rel, old, new, count=1):
    p = ROOT / rel
    s = p.read_text()
    n = s.count(old)
    assert n == count, '%s: expected %d occurrence(s), found %d for %r' % (rel, count, n, old[:80])
    p.write_text(s.replace(old, new))
    applied.append({'file': rel, 'occurrences': n})


# --- the two closed-registry size constants ------------------------------------------------
# check-identity.py asserts the registry size twice, in two different sections. Both are real
# drift guards and both must state the true size; neither is weakened to an inequality.
sub('foundation/check-identity.py',
    "check('no-new-public-detail-code-is-introduced-for-this-boundary',\n"
    "      len(PUBLIC_CODES)==287 and 'PROJECT.SCOPE_LIMIT' in PUBLIC_CODES)",
    "check('no-new-public-detail-code-is-introduced-for-this-boundary',\n"
    "      len(PUBLIC_CODES)==289 and 'PROJECT.SCOPE_LIMIT' in PUBLIC_CODES)")

sub('foundation/check-identity.py',
    "      len(PUBLIC_CODES)==287 and\n",
    "      len(PUBLIC_CODES)==289 and\n")

sub('workflows/check_workflows.v1.py',
    "# DomainDetailCode is a 287-member registry, so this is a statement about the NINE native outcomes",
    "# DomainDetailCode is a 289-member registry, so this is a statement about the NINE native outcomes")

# --- the emission site says which vocabulary each of its three refusals uses ----------------
sub('workflows/workflows_model.v1.py',
    "    # PUBLIC ROUTE, no new vocabulary: CONFIG.INVALID is a member of the closed D9 error codes AND\n"
    "    # of the closed public DomainDetailCode registry, and it is the code the native route registry\n"
    "    # already assigns to an invalid caller-supplied selection record. The two existing refusals\n"
    "    # above and below keep their exact codes, details and reachability.\n",
    "    # PUBLIC ROUTE, no new vocabulary: CONFIG.INVALID is a member of the closed D9 error codes AND\n"
    "    # of the closed public DomainDetailCode registry, and it is the code the native route registry\n"
    "    # already assigns to an invalid caller-supplied selection record. The two existing refusals\n"
    "    # above and below keep their exact codes, details and reachability.\n"
    "    #\n"
    "    # ALL THREE DETAILS ARE NOW CARRIABLE, which they were not. BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER\n"
    "    # and BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH were emitted here into the public\n"
    "    # DomainDetail.code position while being members of neither public-detail-registry.v1.json nor the\n"
    "    # mirrored DomainDetailCode enum, so the real carrier - common.schema.json#/$defs/StepTermination -\n"
    "    # REFUSED both terminations and neither refusal could be published at all. They are now REGISTERED\n"
    "    # under the same names, owner `workflows`, rather than remapped: the two conditions are distinct\n"
    "    # answers to `what do I do next` - state a scope parameter, versus supply the one already selected -\n"
    "    # and this code, the owning prose and the existing controls all already used these exact names.\n"
    "    # Nothing about the emissions themselves changed: same class, same error code, same detail spelling,\n"
    "    # same remedy, same order, same reachability.\n")

print({'applied': applied})
