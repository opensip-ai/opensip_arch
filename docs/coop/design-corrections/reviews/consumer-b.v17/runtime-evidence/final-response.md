## consumer-b.v17 — verdict: CHANGES_REQUIRED

### Input custody (three separate claims)

| | |
|---|---|
| manifest SHA-256 | `4cee77543946d66f2282dcbc7a8621e0b4117d78d37b44cf57a5f0ad3ca5e237` ✓ |
| declared parent (31) | `ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5` ✓ — **declared binding only**; the parent is not held |
| 101 disclosed files | 101/101 PASS, and **byte-identical to my v16 kit measured per path** against my own v16 custody record |
| what actually changed | the manifest's own digest and its parent custody row. No Run needed reminting for a kit change |

Source-31 reference code was not accessed. No author model, checker, root output, expected answer, other origin's review or candidate snapshot was read.

### The second clause-to-code audit found real omissions in my own work

My v16 report said all 131 requirements were executed with no open helper failures. That was true of what I had checked — and the audit shows a passing emitter plus a passing replay proved nothing about clauses both omitted:

| | clause | what my sealed graphs actually contained |
|---|---|---|
| **V17-D3** | `ATOM_KIND_INCOMPATIBLE`, kindApplicability | **2 of 5 graphs carried a malformed DISABLED rule** (`literal` is sourceSubjectKind `symbol`; declared `file`/`package`). The `disabled` outcome hid it; both graphs closed, replayed and passed 14 controls |
| **V17-D2** | atom §3 per-rung filters | the registry spec is a per-rung *map*; I compared it to the string `"forbidden"`, so every rung-forbidden filter was admitted |
| **V17-D4** | enumeration §§1/3/4/5/8 | the enumeration plan was **never validated**. 4 of 5 graphs declared a compiler/grammar-filtered FILE extent; one narrowed `inventory` to a consumer-chosen `[file]`; one had a binding with no extents and no symbol inventory |
| **V17-D5** | enumeration §§1/3/4 + exec-inputs §6 | I had *weakened* the kinds-equality to available bindings and published the gap as advisory **V16-A2** |
| **V17-D6** | workflows §1 | my invocation was schema-valid with **one-based** stepIds, no comparison step result, no attempt derivation binding |
| **V17-D7** | workflows §6 | my "valid" repair descriptor asked to **CREATE a path the selected snapshot already contained** |
| **V17-D1 / D8** | — | the rebind corrupted an ancestry digest row; and two writers were wrongly in `SELF_EXCLUDE`, so they wrote into the v16 tree |

All fixed, all five graphs re-minted: closure 759/944/1044/655/678 checks, 0 refusals, `REPLAY_MATCH` each, 14 controls each. New discriminating controls: **18** policy (incl. 6 kind/endpoint + a lawful `endpoint=target` contrast), **8** enumeration, **14** invocation (**10 of 12 negatives are admitted by the owning schema** and refused only by the normative joins), **4** repair snapshot-condition.

### V16-A2 withdrawn as factually wrong

The kit *does* state the unavailable case: §1 keeps host extents, §§3/4 give exactly-one-per-kind plus the `unavailable` shape, and exec-inputs §6 says null-universe "**does not discard** same-cell inventory items". A missing record is not a retained unavailable record. My graph had no such record; now it does.

### Still unresolved (not mine to close)

**V16-S1** (which Coverage entry's `ClosedWorldV2` owns the repair projection) and **V16-S2** (trailing `**`) remain pending source-author work — no new normative bytes were supplied and I invented no selector or glob law.

On V16-S2 I correct my own arithmetic: I wrote that a zero-or-more reading makes `src/**` match "`src/` only". That is wrong — a zero-or-more set contains the nonzero lengths. Restated: the published example forces `**` to be a separator-terminated segment group, under which a *trailing* `**` matches no file at all, while an "any remaining suffix" reading matches every descendant. Both honour the closed alphabet and the one example, and they disagree on admissibility. The arithmetic error was mine; the underspecification stands.

### Disclosure I must not bury

Before my own control caught it, this session overwrote **two** files under `consumer-b.v16/output`: `helper-corrections.json` and `notes/siblings-untouched.json`. v14 and v15: zero writes. No prior Run export, review file, requirement status, checkpoint or vector was touched. Their prior bytes were not retained and I cannot restore them. Census: `notes/prior-generation-writes.json`; row V17-D8.

### Exports and command

From-scratch: `/tmp/opensip-architecture-review-env/bin/python -I -B …/consumer-b.v17/output/lib/verify_all.py` → **33 stages, 0 failed**.

```
syntax-code  run3:f8dc43b3…0199a  ce3d2f085f1501fd3e979450948b65965fac2478fd8d2a09dde5320eef555660
typescript   run3:e22b6ccf…e225a  7997118098d0d5f0191b4879f001e343df571881bad03cbbd899a7ec69af8eeb
rust         run3:56d0f726…9a64e  0962944f1872b6cb685495d31129a313bddaba7bb3134b5ce97065e402430986
rust-partial run3:34375643…f1058  b60526e89358a8528dfa54d6bad089131bb5d5b532cc44389a133cca1d96d440
syntax-data  run3:89fdb7e9…eaa5d  5335ffe8c47308c4f66f04c68b75afd8a792cf52874735dfac0d0951de7ec8bd
```

131/131 non-future requirements executed, 3 future-qualification items not demanded. No root admission or agreement is claimed; every compiler/provider/OS observation remains a synthetic trusted input; no product implementation, repo mutation, commit, real repair, baseline adoption or qualification.
