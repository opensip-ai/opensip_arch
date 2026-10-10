# Proposed native Cargo include-read compatibility

Lead preparation, 2026-10-10. UNREVIEWED and UNBOUND. This is a prospective compatibility selection for the complete native configuration profile. It changes no accepted source, product code, schema, inventory, contract lock or accepted review. It supplies no input custody, SourceCap, signed Tool, owner admission or qualification.

## Proposed selection

The native host projector does not honor the top-level Cargo configuration `include` member. Parse each selected original configuration file completely as UTF-8/TOML and convert the complete document with the pinned Cargo ConfigValue conversion before semantic filtering. Retain the original per-value and per-list-element Definition association. Then remove the actual top-level `include` value as stripped configuration. Do not call include_paths, resolve an include pathname, expand a glob/template, stat/open a referenced location, test optional existence, follow another file, or add an include-derived configuration document to the merge population. An include string is data, not a read capability.

Apply this to every selected original document before effective-document merging. An include directive in a document that would later lose an effective value must not cause a read either. A file present for an independent reason in the admitted snapshot is not an include input: this directive must not load it. This proposal grants no HOME/CARGO_HOME or ancestor discovery and chooses no include grammar, list members, path types, filename extension or numeric parser bound.

Ordinary upstream Cargo behavior remains unchanged outside the prospective native profile. This intentionally differs from Cargo's ordinary config loader, which converts the document and then follows includes before merging. It must be published as compatible native projection behavior; post-load filtering is insufficient.

## Invalid inputs and truthful accounting

A stripped member is not a license to skip complete parsing/conversion. Invalid UTF-8, malformed TOML, duplicate/dotted-key conflicts, a non-table root or values rejected by the complete pinned ConfigValue conversion remain failures at their actual input origin. No public code or fallback is selected here. Conversely, a successfully converted `include` value has no native include-specific type/path validation: its whole actual value is stripped without invoking the upstream include parser. Distinguish generic whole-document invalidity from an include-specific error that native projection never evaluates.

The actual stripped keys must remain represented in the complete projection's truthful key accounting under the separately published key representation/order rule, within the unchanged existing carrier bounds. This proposal does not define a dotted-key escape grammar, collapse descendants into a fabricated wildcard, omit overflowed keys or claim an empty list. An unrepresentable actual projection is a refusal under its owning publication; it cannot become partially successful native input. Include-only changes may leave projected semantic file bytes unchanged while changing the actual stripped-key disclosure if their key population changes; the existing file digest versus whole record identity distinction remains unchanged.

The complete replacement-location census required by CC5 remains distinct from the selected original merge population. Suppressing include traversal does not remove independently retained config locations from that census. Preserve exact legacy/current selection and admitted ancestor precedence from the discovery publication; do not use scratch physical ancestors or filename sorting as semantic precedence.

## Required controls before product use

1. A retained original include referring to a denied external canary: no lookup, metadata inspection or read at that location, while independently honored local values retain their original definitions.
2. A retained include referring to an independently retained in-snapshot file: its values do not enter the merge unless that file is independently selected by admitted original discovery.
3. Nested, cyclic, optional, absent, template and glob-looking include data: no include resolution/read; successfully converted values are stripped. These are hostile inputs, not an admitted include grammar.
4. Include-specific malformed shapes that are nevertheless valid ConfigValue data: stripping succeeds without invoking include-specific validation. Malformed UTF-8/TOML or generic conversion-invalid values still refuse before filtering.
5. Competing nearer/ancestor documents, including directives in losing values: every directive is removed before merge, with ordinary pinned non-include scalar/list precedence and original element roots preserved.
6. Same original input projected under two scratch roots: exact semantic bytes, key records and identities remain invariant; physical paths confer no authority.
7. Stripped key/location bound crossings: no dropped keys, invented wildcard, truncated population or empty-catalog success. Existing bounds are unchanged.
8. Actual once-only metadata context with initialized projection: disk/include reload guards refuse before reads; metadata consumes the admitted complete projection rather than ordinary discovery.

These are implementation requirements, not passing results. Existing merge, initialization, definition-consumer and discovery fixture controls retain their accepted narrow scopes and are not reopened. The six complete native publication duties remain open. Full discovery/read custody, definition-to-owned-path mapping, deterministic serializer artifact, complete key accounting, bounded parser/merge/storage lifetimes, origin-sensitive public failures, source/input/Tool association, actual production caller and worker integration are still required.

## Primary-source basis

Pinned Cargo commit f2d3ce0bd7f24a49f8f72d9000448f8838c4e850. Original source retained at /tmp/opensip-implementation/native-registry-alias-source-r1/src/cargo/util/context/mod.rs: load_values_from 1308-1327; load_file 1337-1339; _load_file 1344-1379; load_includes 1383-1414; include_paths 1418 onward. The exact file and spans will be pinned in the review subject. Current source helpers do not establish this selection as law.
