# Implementation route 446 — bounded ACL capture and creator private-access evidence

Actual Claude Opus 5, 2026-09-21. Read-only route advice. **No native, compiler or Node job was run**
(root owns the lane for 43 integration and probe 445). No repo edits. **This approves no source and
no code.** I did not access the private 413 UUID file.

I verified both additional 445 pins byte-for-byte, read the two cited XNU passages myself, and read
the executed 445r2 results.

## Correction to my own 444 advice, from source I read this session

At 444 I proposed `KAUTH_FILESEC_NOACL` as the documented in-band positive premise for "no ACL".
**I retire that.** XNU `vfs_vnops.c:1637–1667` (pin `f9afaa44…`, verified) *synthesizes* it:

```c
if (VATTR_IS_SUPPORTED(&va, va_acl) && (va.va_acl != NULL)) { __nochk_bcopy(...); }
else { fsec->fsec_acl.acl_entrycount = KAUTH_FILESEC_NOACL; }
```

so NOACL is emitted precisely when `va_acl` is **unsupported** (given one supported UUID attribute) —
the case it was supposed to exclude. With all three unsupported the kernel returns
`KAUTH_FILESEC_NONE`, and Libc `statx_np.c:202–214` then clears `FILESEC_ACL` for NOACL *or* an
undersized result. My premise was wrong; root's independent reading was right to flag the area.

## 1. Joint capture, and what the change actually is

445r2 settles this empirically. For **regular files** the joint call reconstructs everything:
`links_equal=1 size_equal=1 common_matches=1`. For **directories** it does not —
`links_equal=0` in both directory fixtures (the documented dot/dotdot exclusion, with
`vfs_attrlist.c:2663` substituting 1 when `va_dirlinkcount` is unsupported) and `size_available=0`,
since no joint `st_size` equivalent exists. `mode_contains_type=1` happened to hold, but the manual
guarantees permissions only, so `OBJTYPE` must carry type.

**The change, named precisely.** Today `observe_descriptor_with` requires
`before == during == after` over all ten `DescriptorMetadata` fields, where `during` comes from the
same `vnode_getattr` as the ACL (`vfs_vnops.c:1530–1546` confirms one call). A fixed-buffer route
keeps that for regular files, but for directories two fields (links, size) would be compared only
across the `before`/`after` fstat pair, not jointly with the ACL. That is a **real reduction in what
is jointly bound**, not a refactor.

**Does a selected passage forbid it?** I could not find one, and I will not manufacture one. §1a
step 6 requires "recheck all original owners"; §8 requires that all captures and original-owner
checks use the same authoritative operation budget and that a session "rechecks all relevant
contributing owners"; §1b requires that "the final native filesystem profile must qualify actual
original directory/file descriptors; a generic path parse or successful syscall is insufficient".
None prescribes *one syscall* for metadata and ACL — that criterion is current implementation, not
selected law. So a reviewed source-contract refinement is **not barred by a named passage**, but §1b
means it must be qualified rather than assumed equivalent, and neither the probe's stability across
four fixtures nor XNU source excludes ABA between two samples. Claiming equivalence from repeated
stable tests would be the error.

## 2. Positive absence — not available, and do not fake it

**No.** Both public paths conflate, for different reasons:

- **fgetattrlist**: omission means null *or* unsupported (411's reading of `vfs_attrlist.c:2051–2064`).
  445r2 strengthens this decisively: omission persisted on both no-ACL fixtures while
  `acl_cap_valid=1 acl_cap_supported=1 acl_attr_valid=1 acl_attr_native=1`. Volume capability **and**
  the richer `ATTR_VOL_ATTRIBUTES` native bit were both positive and still did not convert omission
  into "no ACL".
- **fstatx/filesec**: the synthesis quoted above.

So there is **no documented public bounded API delivering positive absence** without a per-vnode
support premise, and I found none in the inspected set. What can be implemented now is capture that
*preserves* the distinction and refuses to interpret it; what remains unavailable is the
qualification that would let omission mean null.

One narrowing worth using rather than a blanket refusal: §1b has OpenSIP **create** `OpenSIP`, final
I and its private descendants (0700/0600). For objects this creator just made, absence is a much
smaller premise than for arbitrary pre-existing ancestors — though ACL inheritance means it is a
narrowing, not a proof. Pre-existing external ancestors are where the unresolved premise really
bites. Refusing every ordinary no-ACL directory is not a completed feature, and I do not recommend it.

## 3. statx qualification versus fixed capture

Fixed capture **strictly dominates** on proof obligations. Qualifying `statx1` needs *both* an
allocation bound — finite, monotone returned sizes plus released-runtime correspondence we cannot
manufacture — *and* an absence-semantics premise, because its NOACL is synthesized. Fixed capture
needs only the absence premise; its byte bound is already derivable (44 + 128×24 = 3116, and the
probe's 3244-byte buffer held every case). Opaque OS and name-service work stays separately
disclosed on both routes and excuses neither unbounded controlled allocation.

## 4. Smallest next code unit

**Boundary:** a new module beside the existing ones, `crates/platform/src/filesystem/descriptor_acl_capture.rs`,
exporting a capture that takes an injectable syscall exactly like
`directory_volume.rs::read_uuid_with(file, syscall)`. No new schema, no new crate, and **no rewiring
of `descriptor_acl` or `observe_descriptor_with` in this unit**.

**What it must return**, driven by §1b needing *two different* predicates — external ancestors require
"no ACL write grant to any other principal", private descendants require "no group/other access
granted by mode or ACL", which includes read and search. Today's `Vec<AclWriter>` resolves only
mutating-allow ACEs, so an empty writer list is **not** evidence of no foreign access. The capture
must therefore preserve per ACE: tag (allow/deny), the full rights mask **including unknown bits**,
flags (inherit, inherit-only, inherited), and the resolved principal (`User`/`Group`/`Unresolved`) —
plus the returned/omitted discriminator kept distinct from empty.

**Bounds:** ≤128 outer membership resolutions, all caller-owned representation bytes reserved before
capture via the accepted ledger; resolver-internal effects remain a profile premise.

**Tests (code-level unless stated):** decoder refuses malformed/oversize/unaligned records; omission
decodes to *unavailable*, never empty; unknown rights bits survive round-trip; a non-mutating
allow-read ACE for a foreign principal is represented and would fail an access-exclusion predicate
while today's writer list is empty; deny and inherit-only ACEs are represented distinctly;
unresolved principals stay unresolved; membership resolutions are counted and capped. Native fixture
coverage stays root's lane.

**This helper alone is not creator completion.** It supplies evidence; completion additionally needs
the reviewed private-access predicate that consumes it, the per-vnode absence qualification, the
joint-capture contract decision from §1, and the profile premise for resolver effects.

## Root qualifications on my 43 review — accepted

"Only allocation" should read "only the retained `Arc` copy" (the `Vec`, callback, map and allocator
internals remain separately accounted). Validation parity with the reader applies to `max` only; the
reader has no `attempts` parameter, so `attempts == 0` is a calculator-specific rule. And the
legacy-owned refusal closes the **owned `Budget`**, not a shared ledger that does not exist in that
configuration.
