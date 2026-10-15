# B2-A-REFERENCE-r1 review

**Verdict: REQUIRED-FINDINGS.** One required correction prevents design-unit acceptance.

## Required finding B2AREF-1: iterator member roots lose SX-1 protection

`reference/discovery-defaults.sx1-r1.py:111-143, 191-238` accepts `member_roots: Iterable[str]` but reuses that iterable across classifications and nested helper calls. `_custody_state` consumes it. A single-pass iterator is a valid iterable, yet loses the admitted member roots after the first call.

Independently reproduced by importing the staged reference read-only:

```python
cargo_roots_from_markers(
    ['m/Cargo.toml', 'm/.opensip/Cargo.toml'], iter(['m']))
# actual: {'m', 'm/.opensip'}; list input: {'m'}

enumerate_units(
    ['m/Cargo.toml', 'm/.opensip/package.json'],
    member_roots=iter(['m']))
# actual: unitDirs ['m', 'm/.opensip'], prunedTrees []
# list input: unitDirs ['m'], with the m/.opensip custody row

pruned_anchors_from_directories(
    ['m', 'm/.opensip'], [], iter(['m']))
# actual: {}; list input: {('m/.opensip', 'opensip-custody-state'): None}
```

This changes discovery selection: custody state becomes a unit or Cargo root, or its observed directory row disappears. It violates SX-1 and the accepted plan's propagation requirement. Snapshot member roots into a reusable tuple or set at each entry point that traverses or forwards them repeatedly, including all three functions above. Add list/iterator equivalence controls, including directory observations after marker processing, and regenerate evidence and pins. The existing checker uses reusable lists and misses this defect.

## Verified evidence

Rehashed the manifest (1,345 bytes, SHA-256 `b38bac53199550302039bf08cd5f06a2dcbe2c9a4e0220830ac05bbc1b9f1e5d`) and all six members. Every size and hash matches. The successor record matches its requested 3,003-byte pin and `43f1fbbf223153aab78c5920439922bfbe9da2085bccf00593744bceea932541` digest.

Product HEAD matches `2191674d873ed7c0eb4459683dcc29cf7da42440`; architecture HEAD matches `ccb8b07cc43ba5debc77c600b1f77e06611cf47b`. Tracked state is clean. Architecture has a pre-existing untracked `docs/implementation/m3/syntax-e/e2s/` directory, which was left uninspected and untouched.

Reconstructed the candidate in memory from the pruning copy using all 19 literal asserted replacements in `author.py`; the result exactly equals the staged candidate. Did not execute the author script. The AST checker confines changes to the six named functions, added helper, seven changed constants, added constant and module docstring. DD and the pruning copy match their accepted pins. Plan-review NBO-1 is applied: `PRUNED_TREE_ROW_VERSION` is 3 and asserted by the checker.

Ran only the permitted staged checker. [checker-rerun.json](checker-rerun.json) reports 77 passing controls: 49 unchanged pruning controls, 21 SX-1 controls and seven V3 controls. Its bytes exactly match staged `evidence/checks.json` (SHA-256 `4d6c2adcb05052294e9c0a5530ca5b9edc9849e5a65e15c13e0edf7e5b6a3bd5`). Those results do not cover B2AREF-1.

Direct inspection confirms exact segment matching and outermost comparison in `classify_path` itself. Additional read-only spot checks passed for target over a member custody anchor, custody over `.git`, dependency over member custody, UTF-8 member identity and member enumeration with list input. The failure concerns repeated use of single-pass member-root iterables.

The V3 converter preserves the accepted-provenance trust boundary: relative UTF-8-sorted member paths are carried separately, add no boundary prefix, and fit B-S1's V3 inventory for admitted inputs. The merged-schema controls validate its outputs; V1/V2 conversion refuses explicitly, with unknown and boolean versions also checked. The upstream admission/schema obligations retain the 64-member bound; this converter is not a membership admission mechanism.

All eight record parent pins match current bytes and accepted source/application manifests, prior successor candidates or selected inventory v190. Parent ordering is correct. The five candidates exactly cover the subject apart from the included record. No passage overrides exist. With 162 existing successors, 163 is the correct next binding position. This is a structural assessment, conditional on corrected independent acceptance and assent. The supplied scratch support reports base and appended-lock verification passing with synthetic review/assent; it was inspected, not rerun, and is not actual acceptance or binding.

## Nonblocking observation NBO-1

The check named `outermost-target-over-member-anchor` uses `m/target/x`, with no custody anchor. Use `target/m/.opensip/x`, Cargo root `''`, member root `target/m`, expecting `target`, to exercise the claimed competition. Add `.opensip/.git/x` expecting `.opensip` for the opposite VCS ordering. Independent spot checks passed, so these are evidence improvements rather than another functional finding.

## Scope and boundaries

Reference-only review under plan section 1.1, B-S1 SX-1/LD-3/LD-4/LD-14/BS1-F3, its passages and SLS fragment, the accepted pruning correction, DD, and product `contract_successor` verification rules. No product code, schema, SLM or native-model change; no qualification. No binding was made. Ran no Cargo, tests, builds, lane or network operations; accessed no private fixture, installation directory, signing keys or held trees; used no other panes or delegation. Neither repository, stage nor control files were edited. Wrote only this review, `review.json`, and the permitted checker output.
