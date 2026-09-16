"""Reference experiment: source-bound coverage rows, not a product storage API.

The unchanged reference owner admits the entire Run before projection. Inputs
are an isolated owned snapshot. Production must supply an admitted snapshot lease;
the deep copy here is test/reference custody, not a proposed storage strategy.
No caller-supplied coverageId is a stream identifier. Each coverageId binds one
descriptor and one registered CoverageResultV3 payload.
"""
import copy
import hashlib
import json


class ProjectionRefusal(ValueError):
    pass


PROVENANCE = {
    'verifiedInDocument': [
        'entry-coverage-ids-unique-and-in-canonical-order',
        'entry-descriptor-and-payload-identities-match',
        'entry-payload-schema-is-selected-native-document',
        'item-counts-consistent',
    ],
    'hostAsserted': [
        'source-is-exact-admitted-run-evidence',
        'entries-are-canonical-prefix-of-source-evidence-coverage-ids',
        'total-is-source-evidence-coverage-id-count',
    ],
}


def project(expected_run_id, run, objects, blobs, entry_limit, owner):
    """Item-prefix experiment; full-report byte budgeting is deliberately pending.

Reject missing/corrupt/unadmitted source through the actual owner's exception
types. Never reinterpret a source failure as an empty or omitted evidence list.
Do not retain caller-owned mutable dictionaries across admission and projection.
"""
    if type(entry_limit) is not int or not 0 <= entry_limit <= 3956:
        raise ProjectionRefusal('ENTRY_LIMIT')
    run, objects, blobs = copy.deepcopy((run, objects, blobs))
    admitted_id = owner.close_run(run, objects, blobs)
    if admitted_id != expected_run_id:
        raise ProjectionRefusal('SOURCE_RUN_MISMATCH')
    evidence_id = run['evidenceId']
    # close_run has checked domain, identity, roots, native admission and replay.
    evidence = objects[evidence_id][1]
    coverage_ids = evidence['coverageIds']
    if coverage_ids != sorted(set(coverage_ids)):
        raise ProjectionRefusal('SOURCE_COVERAGE_ORDER')
    entries = []
    for coverage_id in coverage_ids[:entry_limit]:
        descriptor = objects[coverage_id][1]
        raw = blobs[descriptor['payloadDigest']]
        entries.append({'coverageId': coverage_id, 'descriptor': descriptor,
                        'result': json.loads(raw)})
    omitted = len(coverage_ids) - len(entries)
    return {
        'source': {'runId': admitted_id, 'evidenceId': evidence_id},
        'entries': entries,
        'entriesProjection': {'total': len(coverage_ids), 'omitted': omitted,
                              'omissionCause': 'item-cap' if omitted else 'none'},
        'provenance': copy.deepcopy(PROVENANCE),
    }


def verify_embedded(panel, owner, validate):
    """Document-local checks only. These cannot prove source membership/admission.

`validate` uses the pinned proposed panel schema and exact native/identity
registry. Owner identifier/canonical functions supply the existing algorithms.
"""
    validate(panel)
    entries = panel['entries']
    ids = [row['coverageId'] for row in entries]
    if ids != sorted(set(ids)):
        raise ProjectionRefusal('ENTRY_ORDER_OR_DUPLICATE')
    for row in entries:
        descriptor = row['descriptor']
        native = owner.native_admission()
        registered_digest = native.schema_document_digest(native.NATIVE_SCHEMA_DOC)
        if descriptor['payloadSchemaDigest'] != registered_digest:
            raise ProjectionRefusal('ENTRY_SCHEMA_IDENTITY')
        if owner.identifier('coverage', descriptor) != row['coverageId']:
            raise ProjectionRefusal('ENTRY_DESCRIPTOR_IDENTITY')
        raw = owner.C.canonical(row['result'])
        if hashlib.sha256(raw).hexdigest() != descriptor['payloadDigest']:
            raise ProjectionRefusal('ENTRY_PAYLOAD_IDENTITY')
    projection = panel['entriesProjection']
    if projection['total'] != len(entries) + projection['omitted']:
        raise ProjectionRefusal('ENTRY_COUNTS')
    if (projection['omissionCause'] == 'none') != (projection['omitted'] == 0):
        raise ProjectionRefusal('ENTRY_OMISSION')


def verify_against_source(panel, expected_run_id, run, objects, blobs,
                          entry_limit, owner, validate):
    """Reference host join; no browser or generic envelope acceptance is implied."""
    verify_embedded(panel, owner, validate)
    expected = project(expected_run_id, run, objects, blobs, entry_limit, owner)
    if owner.C.canonical(panel) != owner.C.canonical(expected):
        raise ProjectionRefusal('SOURCE_PROJECTION_MISMATCH')
