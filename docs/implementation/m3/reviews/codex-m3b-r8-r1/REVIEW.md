# M3-B-r8 review

Verdict: **REQUIRED-FINDINGS**

Two required findings block acceptance. Non-blocking observations: none.

## Exact subject and scope

Rehashed subject.json: 440 bytes, SHA-256 `108f1b2db8fedc45612733ba2c7e9911298a2835a2ef173658be1908d3e770b2`. Its sole member PROPOSAL-r8.md is 128867 bytes, SHA-256 `777231ce30f13ae9fff1b8fe9d2b8e8d79ac264abaa1047116cddfb032481fb5`; the member pin matches.

Confirmed clean product main `01c73e2d54e037e3e41adc2f5d97df854552921e` and architecture HEAD `c7108e3f066a0a5d306e7e080a9790fc40f3e32d`. Independently diffed the candidate against live PROPOSAL.md. Substantive changes are confined to item 14a, S10 and the new Not claimed line; the remaining changes are the r8 title/banner/change summary and preservation of the historical acceptance banner. Existing law items are unchanged.

## M3BR8-R1-RF-1 — Specify the complete resolution grammar and node identity

Item 14a gives candidate order but not a closed grammar for the inputs to that order. “Under the npm package-name grammar” does not select an exact admitted language, and the package subpath is merely “the remainder.” No rule decides dot/dot-dot or empty segments, backslashes, trailing separators and encoded separators. “Any other form that names a filesystem path” is likewise not an exact discriminator between path and package forms.

For example, pkg/../base, pkg//base and pkg\base need explicit outcomes. Rejecting malformed subpaths, treating a form as an unresolved filesystem path, or normalizing it into another in-project candidate are different behaviors. A blanket prohibition on outside-root reads does not settle these in-project cases.

The law must also state the canonical project-relative identity used when a candidate is selected. Otherwise two spellings of a base can affect graph deduplication, cycle detection and the 32-node bound, despite NE requiring unique-by-path graph nodes and retained ordered edges. Do not leave these decisions to whichever filesystem/path API B2-c2 chooses.

Select or pin the package-name grammar, close the subpath and other-path forms, and specify normalization/root containment and graph identity before cycle/bound checks. Add disposition controls for the ambiguous forms. The existing nearest-first/candidate order can remain.

## M3BR8-R1-RF-2 — A D9 code does not select the public-detail remedy

Item 14a line 615 gives the new public detail native.typescript-config-unresolved but sends its remedy through B-S9's CONFIG.INVALID route. B-S9 README's “The change” section expressly says PUBLIC_ROUTE_REMEDIES is keyed by public code and that keys with another public detail are outside that string even where their D9 code is CONFIG.INVALID. The accepted native model's table follows that rule.

These are distinct fields: CONFIG.INVALID as the D9 error code does not make native.typescript-config-unresolved use PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"]. As written, S10 repeats the same route shorthand without requiring a remedy entry under the actual new public detail and its complete carrier/route mapping.

Require S10 to add the new public-key remedy and corresponding model/product public-termination route, with words true for all four aliases. It may use B-S9's successor-copy mechanism as a precedent, but must not select B-S9's CONFIG.INVALID entry by D9 code. Alternatively, explicitly reuse public detail CONFIG.INVALID and revise the new-record decision. Controls should derive a complete termination, subject and remedy for every internal key, not only normalize the alias name.

## Other assessment

A law step is needed: the selected native reference takes effective allowJs as an observation, while NE fixes option inheritance and graph retention without this pre-Plan lookup algorithm. A limited first-party data reader shared by B2-c2 and C2 is appropriate. JSONC comments/trailing commas, last-key behavior, 64 KiB/file and 32-node bounds, and typed malformed/cycle/bound outcomes form a reasonable bounded direction.

The effective-allowJs bullets match NE:527–545: jsconfig supplies its own true unless overridden, own options beat bases, later bases beat earlier, written allowJs wins including false, otherwise effective checkJs supplies the value with false default. Refusing every unresolved edge avoids inventing a partial-graph carrier and never guesses a mode.

The read-set/descent distinction follows NE:735–741: actually read pruned bytes enter the snapshot inventory under custody, without authorizing discovery enumeration. Requiring C1 custody on the path, forbidding outside-root reads and treating links as unresolved before C1 preserve the stated boundary. Nothing is fetched, installed or executed. These sound constraints do not remove RF-1's naming ambiguity.

Four internal keys normalized to one new graph-configuration public detail are reasonable in principle: they share an external configuration-repair family and can share one remedy. That design is not inherently incompatible with the context-free alias rule. Their D9 request-rejected/exit-2/CONFIG.INVALID classification and class-plus-config-path subject are appropriate for the declared authored-configuration failures; the unresolved public-key remedy is RF-2. A contract successor is the right general mechanism for selected registry/alias/vocabulary/remedy changes, with the B-S10 product materialization pattern, once its complete route is specified.

This is a law review only. No new registry row, product vocabulary, reader code, binding or qualification is made by this candidate. The successor and B2-c2 remain future work.

## Boundaries

Wrote only REVIEW.md and review.json in the requested directory. Neither repository, stage nor control files were edited. Used only read-only inspection, hashing, JSON parsing and Git queries. No Cargo, tests, builds, lane, network, other panes or delegation; no private fixture, installation directory, signing keys, held trees or T2 held-out entry was accessed.
