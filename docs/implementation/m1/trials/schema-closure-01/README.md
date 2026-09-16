# Full-document schema reference probe

The explicit25-source set contains every referenced document ID. Five native
schema IDs are registered non-URN identifiers; the loader accepts their exact
registered spelling and never derives a filesystem/network location from them.
Source bytes matched the accepted source45/application46 overlay.

Following the pointers also finds a dangling reference in
`workflows/schemas/policy-document.v2.schema.json`:
`$defs.AtomSuccessorV1.properties.filters.items.$ref` names
`#/$defs/FieldFilterSuccessorV1`, which that document does not define. The probe
refuses before generation. The full source/reference closure has NOT passed.

The definition describes an earlier proposed Atom extension. Before selecting
product generation, determine whether this is unreachable historical residue
outside the selected entry points, or an intended carrier needing a reviewed
correction. Neither silently removing the constraint nor fabricating a target
is permitted. Explicit generation entry-point selection must be reviewed if it
excludes this definition while retaining the full source bytes as provenance.

This is an implementation tool-selection finding under RF-03; it does not on its
own establish a runtime defect or reopen the entire accepted design. No original
schema was changed. The trial's flattening code is unaccepted and was not reached.
