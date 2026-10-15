# B2B-PLAN-r3 review

**Verdict: REQUIRED-FINDINGS.** The observation-adapter approach is appropriate, but its specified population has two remaining defects. B2BPLAN-1 remains open, and the explicit-source adapter reopens part of B2BPLAN-2. B2BPLAN-3 through B2BPLAN-5 stay resolved.

## Subject verification

Rehashed the 449-byte `subject.json`, SHA-256 `1bd9153e47c0c94b6decb6c7c1a70444bab9fa9a8cdafac37802a962e14b4012`, and its sole member `docs/implementation/m3/config-discovery-b/b2-b/PLAN-r3.md`: 23,385 bytes, SHA-256 `44659a6a839617470bc4b457fca068be79bdeb836c0a11ad8150f386e59b59a2`. Both match.

Product HEAD remains `94e5fdebd63a174694dadbb5e647063855614b77`; architecture HEAD remains `424f64a3f331261d0f1e8fb323948492cda5a06d`. Both tracked states are clean. Section 0 retains the accurate implementation facts checked in earlier rounds against this unchanged base. T2 store state remains documentary acquisition evidence; no store or held-out entry was inspected or freshly verified.

## B2BPLAN-1: Separate pruned-anchor observations from nested-boundary evidence

Location: PLAN-r3.md section 1.0, downward automatic population and anchor-entry exception.

The adapter excludes everything strictly below each excluding anchor, but then retains every anchor directory with its .git or opensip.json child. Those children are strictly below the anchor. A walker cannot obtain .opensip/.git or .opensip/opensip.json from the selected root parent listing without opening/listing the pruned directory. The same problem applies to node_modules, VCS and Cargo-output anchors. The population property only checks output paths against the retained population and cannot detect an unlawfully retained input child.

Required correction: Give pruning precedence over boundary detection. A pruned anchor contributes only its own parent-observed entry and no children. Keep the .git/opensip.json evidence exception only for ordinary directories whose boundary must be detected, never for an already pruned directory. Add direct adapter-population assertions that even those specially named children are absent under every pruned reason, alongside native no-open/list/stat-inside controls.

## B2BPLAN-2: Preserve ancestor Cargo-root evidence before checking exact roots

Location: PLAN-r3.md section 1.0, explicit/config chain population and two-pass assertion; LD-B2B-8.

The explicit/config adapter retains chain directories and their .git/opensip.json children, but omits Cargo.toml on those ancestors. Cargo roots are then derived only from markers in the retained population. This can turn a refused join inside Cargo target into an accepted unit. Comparing only selectedRoot and unit source between passes does not detect it.

Independently reproduced with permitted read-only imports of the accepted SLM and bound B2-a reference, using synthetic metadata only. The tree has a Cargo marker at `/h/w/Cargo.toml` and a package marker at `/h/w/target/u/package.json`. With explicit project `/h/w` and join `target/u`, the full reference refuses `JOIN_INSIDE_PRUNED_TREE:cargo-build-output:target`. Removing the ancestor Cargo marker, as the specified chain population does, accepts `/h/w/target/u`. Both results retain selected root `/h/w` and source `explicit-joins`, so the proposed two-pass assertion passes.

Required correction: Include the necessary ancestor marker observations to establish Cargo pruning before walking or admitting any named root. Do not descend into a known excluded target while building the population. Specify how the adapter preserves applicable finish-time JOIN refusals and add explicit/config target-join controls plus an ordinary-target-without-Cargo control. Keep unrelated subtrees excluded; do not solve this with a whole-root scan.

## Other plan decisions and controls

A pure outermost-first adapter, separate historical/current replay and a separately reviewed B2-b0 remain the right direction. The new hidden-repository, nested-in-nested and unrelated-sibling cases address the earlier over-observation finding in principle. They need the input-population assertions and ancestor-Cargo controls above; an output-path-is-in-population property cannot prove that the population itself was lawfully observed.

Running pass one over synthetic input solely to identify selection is a reference operation, not permission for a native full-tree walk. Preserving genuine refusals before `finish` is sound. The incomplete safeguard is after selection: finish-time explicit-root refusal can change even when root and source remain identical. The plan needs to preserve that pruning evidence rather than using root/source equality as the whole consistency check.

The split into one reference design unit and four product sub-units remains sound. Successor 164 is the next position at the stated base. Pending provenance remains internal and unserializable, shape-only declaration fills remain non-emitted, and the complete inventory remains schema-validated. B3-b retains reader completion. Custody on unit chains/markers, narrow typed waiver plumbing, existing host observation projections and the scenario seam remain sound decisions.

The all-entry T2 margin is still an explicit completion gate, with held-out results outstanding for an authorized nondisclosing harness or accepted law change. The no-follow by-name observation still carries device/inode/kind for comparison before use, with same-kind swap controls. Those prior corrections remain intact.

CI trace, exhaustion, waiver, FW-01, boundary, sibling-budget and margin-stop controls remain useful. The two remaining population defects prevent accepting their sufficiency or the current-reference design as written. B2-c, B3-b, C1 and J1 retain their stated responsibilities. No implementation, binding, law change or qualification follows from this plan review.

## Boundaries

Used permitted read-only reading, hashing, JSON parsing, Git queries and architecture model imports over synthetic inputs. Ran no Cargo, tests, builds or lane; used no network, other panes or delegation; accessed no private 413 fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, stage nor control files were edited. Wrote only `REVIEW.md` and `review.json` in this review directory.
