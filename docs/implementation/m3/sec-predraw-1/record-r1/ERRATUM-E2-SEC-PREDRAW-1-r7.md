# ERRATUM E-2 to SEC-PREDRAW-1 r7 (FB-1 r4 §3, as embedded in r7 §5): the hold's element size, 128 B not 120 B

**Author:** claude-sec-predraw-1 (w35:p1), Claude Opus 5.5 / high, R3-FRONTIER, long-horizon lead.

**Authority:** LD-Q-208 (`coordinator/msg-ldq208.txt`, `a6ec77d8…`). **Scope: sizes only.**

E-2 is a standalone erratum to the adopted record `SUCCESSOR-SEC-PREDRAW-1-r7.md` (`f8bbd0fb…`), whose §5 embeds the
adopted FB-1 r4 (`dfd803b5…`) verbatim. **The bytes of r7, FB-1 r4 and E-1 are not edited.** If E-2 is adopted, it is
read with r7 and E-1. On the byte terms named below, E-2 controls.

**Pins:**
- product `e8a62bbb8a226555075289791da5c273654e35f5`;
- dev head (SP-2 committed, SP-3 in the working tree) on the branch `claude/sec-predraw-1`;
- architecture `5f328f32`.

## 1. The defect

FB-1 r4 §3 (r7:1088) prices the hold at "`HeldComponent`, 120 B". The SP-3 element-size control measured these sizes on
the dev build (aarch64-apple-darwin):

| Type | `size_of` | `align_of` |
|---|---|---|
| `opensip_identity::JsonValue` (`V`) | 32 | **16** (it has an `i128` variant) |
| `component_manifest::Validated` (wraps `V`) | 32 | 16 |
| `String` | 24 | 8 |
| `Arc<[u8]>` | 16 | 8 |
| **`HeldComponent { path: String, body: Arc<[u8]>, envelope: Arc<[u8]>, manifest: Validated, release: V }`** | **128** | 16 |

The fields sum to 120, which is FB-1's figure. But the 16-byte alignment pads the struct to 128, and no field order
can reach 120. A compile-time `size_of` assertion would have caught this (§4).

## 2. The corrected terms (`n = 20`, `K = 2,580`, `R = 4,096`, as in FB-1 r4 §3)

| Term (r7 line) | Adopted (FB-1 r4) | Corrected (E-2) |
|---|---|---|
| hold row (r7:1088) | "`HeldComponent`, 120 B", 1 object, **2,528** B (`120·20 + 128`) | "`HeldComponent`, 128 B", 1 object, **2,688** B (`128·20 + 128`) |
| upper bound across branches (r7:1093) | 11 objects, **185,740** B | 11 objects, **185,900** B |
| success path (r7:1101) | ≤ 10 objects, **185,540** B | ≤ 10 objects, **185,700** B |
| revocation-refusal path (r7:1099-1100) | ≤ 5 objects (mark, subjects, two sort buffers, row); FB-1 states the object count only | **unchanged**: ≤ 5 objects, 99,032 B computed from the rows. The hold is allocated after step R |
| cap-refusal path | 0 | **unchanged**: 0 |
| fit, bytes row (r7:1126) | P-1 185,740; sum 58,905,996; ceiling 117,440,512; margin **58,534,516** | P-1 **185,900**; sum **58,906,156**; ceiling 117,440,512; margin **58,534,356** |
| fit on the success path | (not tabulated) | sum 58,905,956; margin 58,534,556 |

**Recomputation, row by row** (each row is `owned(b) = b + 128` bytes; the sort rows are two buffers each):

| mark | subjects | R's sort | row | **hold** | ids | index | step 3's sort | collided | **total** |
|---|---|---|---|---|---|---|---|---|---|
| 144 | 65,664 | 33,024 | 200 | **2,688** | 1,088 | 62,048 | 20,896 | 148 | **185,900** |

The only changed row is the hold, by `+8·n` = **+160 B** at `n = 20`. Every total moves by exactly 160 B.

**What stays the same:**
- **Objects:** 11 across branches, at most 10 on success and at most 5 on a revocation refusal. The fit is 116 + 11 =
  127 ≤ 128, with a margin of one object. All unchanged.
- **Edges:** 0. Unchanged.
- **The cap:** `MAX_CATALOG_COMPONENTS_M3 = 20`, with route (a). Unchanged.
- **The ceiling:** `TRUST_VIEW_COST = (128, 2048, 112 MiB)`. Unchanged.
- **The fit:** it holds. The byte headroom left after the read and P-1 is **58,534,356 B**.

**"The total is recomputed from the rows" (r7:1095)** is read as covering E-2's rows. FB-1's history sentence
("r2's 185,228 plus r3's four record overheads") stays as history. The current total is 185,900.

## 3. Controls affected

- **C-NC-20** ("the measured ledger use is at or below §3's bound") is checked against E-2's bounds: success at most
  10 objects and 185,700 B; upper bound 185,900 B.
- **C-NC-fit**'s byte sum takes the hold's element size from code, as `HELD_COMPONENT_BYTES = size_of::<HeldComponent>()`.
  It never uses a literal, and asserts the margin above.
- **SP-3's element-size control** asserts `size_of::<HeldComponent>() == 128` and `align_of::<JsonValue>() == 16`.
  This test found the defect.

## 4. Compile-time size assertions, which prevent this class (LD-Q-208)

Every element size used in P-1's bound (FB-1 r4 §3's table, as corrected here) is asserted at compile time in
`crates/security/src/trust_pre_draw.rs`. The code charges the same expressions it asserts:
- `owned(n · size_of::<T>())`;
- `MARK_BYTES`;
- `RELEASE_ROW_BYTES`.

A layout that exceeds a bound fails the build, error E0080.

| FB-1 row | Assertion |
|---|---|
| mark | `const _: () = assert!(size_of::<AttemptMark>() == 0 && MARK_BYTES <= 16);` with `MARK_BYTES = 2 * size_of::<usize>()` (an `Arc` of a zero-sized value) |
| revocation subjects | `const _: () = assert!(size_of::<&str>() <= 16);` |
| both reader-sort buffers (steps R and 3) | `const _: () = assert!(size_of::<u32>() <= 4);` |
| refusal row | `const _: () = assert!(RELEASE_ROW_BYTES <= 72);` with `RELEASE_ROW_BYTES = "release:".len() + 64` |
| hold | `const _: () = assert!(size_of::<HeldComponent>() <= 128);` |
| ids | `const _: () = assert!(size_of::<(&str, &str, &str)>() <= 48);` |
| index | `const _: () = assert!(size_of::<(&str, u32)>() <= 24);` |
| collided | `const _: () = assert!(size_of::<bool>() <= 1);` |

**Verified on the dev build:**
- with the hold assertion set to FB-1's old `<= 120`, the build fails with
  `error[E0080]: evaluation panicked: assertion failed: size_of::<HeldComponent>() <= 120`;
- restored to `<= 128`, the build succeeds.

**Scope.** These assertions bound the sizes on every target the crate builds for. They are not a claim about other
layouts: on any target where a size exceeds its bound, the build fails.

## 5. Out of scope

E-2 changes only what is listed above. It makes no change to:
- the law;
- the algorithm or its order;
- the refusals;
- the cap;
- the ceiling;
- the object or edge terms;
- any other row;
- E-1.
