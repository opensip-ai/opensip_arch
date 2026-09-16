"""EXPLICIT, location-free semantic fixture metadata.

v16 instruction: "Runtime location itself must not become evidence of a semantic change:
semantic fixture metadata must be chosen explicitly, and relocation with the same declared
inputs should reproduce selected graph identities."

At v15 this origin rewrote content-bearing labels during a PATH rebind, so the session
directory name reached `component-manifest.description` -> `closure.manifestDigest` ->
`closure2` -> native context -> universe -> every fact/scope/Coverage -> `run3`. Any
relocation therefore moved every Run identity for a purely runtime reason. That was a
reconstruction defect, not a normative change.

Every semantic label this reconstruction mints is now pinned here, chosen once, and is
independent of the session directory, the output directory and the process environment.
Nothing in this module may be derived from a path.
"""

# The fixture namespace that appears inside synthetic component-manifest bodies.
FIXTURE_NAMESPACE = 'opensip.blind-reconstruction.fixture.v1'

# Capability-manifest `profile` values. Chosen explicitly per subject shape.
PROFILE = {
    'syntax-code': 'syntax-only',
    'syntax-data': 'syntax-only-data',
    'typescript': 'tsjs-allowjs',
    'rust': 'rust-cargo',
    'rust-partial': 'rust-cargo',
    'vector-syntax': 'fixture.syntax-only',
    'vector-compiler': 'fixture.compiler-modes',
    'vector-compiler-mutated': 'fixture.compiler-modes.x',
}

# ProjectIds are fixed hex constants chosen once per subject, never derived from a path.
PROJECT_ID = {
    'syntax-code': 'prj1-4b7f2c91a3e85d06fa1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f708192a3b4c5d6',
    'typescript': 'prj1-7c1d9e4fa2b86035cd17e2f4a5b6c7d8e9f0a1b2c3d4e5f60718293a4b5c6d7e',
    'rust': 'prj1-9e2a7b4c1d5f80369a7c2e4b6d8f0a1c3e5b7d9f2a4c6e8b0d1f3a5c7e9b0d2f',
    'syntax-data': 'prj1-5d8c3a1f7e0b249635c8d1a4f7b0e3c6a9d2f5b8e1c4a7d0f3b6e9c2a5d8f1b4',
}


def assert_location_free(blobs, object_table, forbidden_substrings):
    """Independent control: no retained graph byte and no object-table value may contain any
    runtime-location string. Returns the list of offending sites (empty is the pass)."""
    bad = []
    for d, b in sorted(blobs.items()):
        for s in forbidden_substrings:
            if s.encode() in b:
                bad.append({'site': 'blob:' + d, 'substring': s})
    import json as _j
    for tid, rec in sorted(object_table.items()):
        txt = _j.dumps(rec)
        for s in forbidden_substrings:
            if s in txt or s in tid:
                bad.append({'site': 'object:' + tid, 'substring': s})
    return bad
