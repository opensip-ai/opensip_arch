# B2B-PLAN-r4 review

**Verdict: ACCEPT.** No required findings. One nonblocking observation below.

## Subject and base verification

Rehashed `subject.json`: 449 bytes, SHA-256 `7cfa2155256296156b5f4bb0b54ed8d46edf43042f49e30558c9dd9efb9dcecf`. Rehashed its sole member, `docs/implementation/m3/config-discovery-b/b2-b/PLAN-r4.md`: 27,902 bytes, SHA-256 `eaedd49f0f9383d42d33536f530e68379409deaefc48bc8f3e3c15f2554241da`. Both match.

Product HEAD is `94e5fdebd63a174694dadbb5e647063855614b77`; architecture HEAD is `424f64a3f331261d0f1e8fb323948492cda5a06d`. Both tracked states are clean. Inventory remains v191 and the product lock contains 163 contract successors. Section 0's implementation facts remain accurate against this unchanged base, including ordinary ledger caps, the 131-edge ACL allowance, missing by-name identity observation, absent upward provenance, unplumbed waiver and existing host rows. T2 acquisition/store facts remain documentary evidence; no T2 store or held-out entry was inspected or freshly verified.

## Required findings closed

**B2BPLAN-1 is resolved.** The current reference is now explicitly a reviewed observation adapter plus the bound DD and V3 projection, rather than a DD substitution alone. Pruning takes precedence: a pruned anchor contributes only its own parent-observed entry, with no child, including `.git` and `opensip.json`. The boundary-evidence exception is confined to non-pruned directories. Direct population assertions cover all four pruning reasons, alongside hidden-repository, nested-in-nested and unrelated-sibling cases. Historical SLM replay remains separate and frozen.

**B2BPLAN-2 is resolved again.** Explicit/config chain observation is parent-first and includes each level's `Cargo.toml` before classifying the next component. A known pruned prefix stops the chain unopened. An earlier nested boundary stops it first, preserving the crossing-first order that SLM can decide from this restricted population. Unrelated siblings remain absent, and an admitted array cannot fall through to automatic enumeration.

Independently spot-checked the specified restricted populations through read-only imports of the accepted SLM with the exact bound B2-a DD. No adapter implementation was created. Results agree with the plan:

- For both `explicitJoins` and `configWorkspaceRoots`, ancestor Cargo evidence plus an observed `target` prefix preserves `JOIN_INSIDE_PRUNED_TREE:cargo-build-output:target` without supplying its descendants.
- For both sources, `target/u` with no ancestor Cargo marker admits as ordinary source.
- A repository above `node_modules` yields `JOIN_CROSSES_NESTED_REPOSITORY`; a repository hidden below `node_modules` is absent and the refusal is `JOIN_INSIDE_PRUNED_TREE:dependency-tree:node_modules`.
- Own-entry-only populations for `.opensip`, `node_modules`, `.git` and Cargo `target` yield the respective pruned row without hidden nested repositories or projects.

**B2BPLAN-3 through B2BPLAN-5 stay resolved.** All-entry T2 objects/edges margin remains a B2-b completion gate, with held-out results outstanding for an authorized nondisclosing harness or a separately accepted law change. Typed owner-waiver plumbing and its negative controls remain assigned. By-name observations retain device/inode/kind for comparison before use; same-kind directory and marker swaps must refuse without retry.

## Plan assessment

The split into a separately accepted/bound reference design unit and four product sub-units is sound. Successor 164 is the next contract position at this base. The reference must be accepted before product vectors use it; acceptance of this plan does not accept that future artifact.

The two-pass reference rule is sound as a synthetic reference strategy: pass one supplies selection, a genuine pre-finish refusal remains unchanged, and pass two uses only the lawful observation population. Root/source equality is supplemented by explicit accounting for every outcome difference; unlisted causes fail the checker. This closes the previous safeguard gap. Running pass one over a supplied synthetic map grants no native whole-tree traversal authority.

The partial provenance contract is explicit and sound: no serialization or completion before B3-b; shape-only declaration fills are labeled and never emitted. The complete boundary inventory is compared and V3-validated now. LD-B2B-1 through LD-B2B-9 retain the proper division of custody, record completion, host projection and scenario testing. B2-c, B3-b, C1 and J1 retain native integration, readers/membership, read-set and production-composition ownership respectively.

The planned CI no-open/list/stat-inside trace, all-kind anchor handling, exact-source traces/budgets, identity swaps, exhaustion, typed-waiver cases, FW-01 controls and margin stop are sufficient for this implementation plan, with the adapter assertions and replay-difference controls added in r4. Each future sub-unit still requires its own concrete evidence and independent review. No product qualification or whole-unit completion follows from plan acceptance.

## Nonblocking observation

**NBO-1:** Add a direct 256/257-depth adapter-population control when implementing B2-b0, tied to B2-b3's existing depth stop. Deeper unseen marker paths must not create units or exclusion rows. This makes the promised native-observation population explicit at the depth boundary as well as pruning and authority boundaries.

## Boundaries

Used permitted read-only reading, hashing, JSON parsing, Git queries and architecture model imports over synthetic inputs. Ran no Cargo, tests, builds or lane; used no network, other panes or delegation; accessed no private 413 fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, stage nor control files were edited. Wrote only `REVIEW.md` and `review.json` in this directory. No product/reference implementation, binding, law change or qualification was made by this review.
