# Bounded native ACL path — advice 444

Actual Claude Opus 5, 2026-09-21. Read-only. **No native, Cargo, Node or C compiler job was run**
(root owns the lane for 440/442), no repo edits, no delegation. **This approves no source and no
unit**, including the private 443 sizing/cache drafts. I did not open
`native-positive.private.bin`; the sanitized pins sufficed.

## 1. Fixed buffer versus qualifying the current statx path

**Fixed buffer, clearly.** Both routes share one opaque premise, so the decision turns on the
blocker each *adds*.

Qualifying `statx_np` requires establishing that the running libc/kernel matches pinned Libc source.
`sys/statx_np.c:statx1` starts at `ACL_MIN_SIZE_HEURISTIC` and reallocates on a strictly growing
kernel-reported size with **no local attempt count or byte ceiling**, so a bound needs monotonicity,
a finite maximum *and* released-runtime correspondence. The audit is explicit that the pinned tree is
not mapped to the running macOS 26.6.2, and that correspondence is not evidence we can manufacture —
public main-branch source cannot establish it. `KAUTH_ACL_MAX_ENTRIES = 128` is an SDK declaration,
not an allocation proof. This blocker is **not resolvable in-repo**.

The fixed-buffer route's blockers — absence semantics, joint metadata, parser surface — are all
resolvable with in-repo engineering plus fixtures, and its bound is derivable *today*:
`KAUTH_FILESEC_SIZE(128)` = 44 + 128 × 24 = **3116 bytes** for the ACL attribute, plus fixed common
attributes. Probe r5 already showed the essential guard: a 32-byte buffer returned **rc = 0** while
`FSOPT_REPORT_FULLSIZE` reported 100, so success alone must never admit a capture; `full_size >
supplied` is the refusal.

The honest caveat: fixed buffers bound the **capture**, not the **resolution**. `mbr_uuid_to_id`
stays on both routes (§4).

## 2. Distinguishing no-ACL from unsupported

**The volume capability is necessary but not sufficient, and I can now say why precisely.**
`VOL_CAP_INT_EXTENDED_SECURITY` (attr.h:337–338, "the volume implements extended security (ACLs)")
is a **mount-level** statement, while XNU's gate is **vnode-level** — the attribute is emitted only
for a supported, non-null `va_acl`. A mount can implement ACLs while a particular vnode still does
not supply one. Different granularities; the capability cannot close the gap.

**The documented in-band premise is the `KAUTH_FILESEC_NOACL` sentinel**, which I verified in the
local SDK (kauth.h:220, `((u_int32_t)(-1))`). Its comment at kauth.h:222–227 states its purpose
exactly: it exists "to distinguish a kauth_filesec_t with an empty entry (Windows treats this as
'deny all') from one that merely indicates a file group and/or owner guid values." So **when the
attribute is returned**, `entrycount == NOACL` is a positive "no ACL" and `entrycount == 0` is a
positive "empty ACL, deny-all". Both are documented, in-band and bounded.

**The unresolved fact, stated plainly:** when the attribute is *omitted* there is no bounded,
documented, in-band observation that positively separates "this file has no ACL" from "this vnode
does not supply `va_acl`". I will not manufacture one. The defensible rule is: admit only positive
returns; **omission is a refusal**, never empty. Keep the same-descriptor capability as a
corroborating premise and as an independent refusal trigger when invalid/unsupported — never as a
converter from omission to empty.

**Independent observation worth root's attention:** the *currently selected* path already does what
the 411 audit forbids. `macos.rs` `descriptor_acl` returns `Ok((metadata, vec![]))` when
`filesec_query_property(FILESEC_ACL)` reports absent, so an unsupported filesystem presents to
policy as "no ACL writers", i.e. permissively. A fixed-buffer replacement that refuses on omission
would be **stricter** than today. That is the right direction, but it is a behavioural change to
review deliberately, and it means the conflation is a live issue in selected code, not only a
hypothetical for the new adapter.

## 3. Attributes needing joint capture

`observe_descriptor_with` compares three ways — `before` (fstat) == `during` == `after` (fstat) —
where `during` comes from the *same* syscall as the ACL. Preserving that requires the joint call to
reconstruct all ten `DescriptorMetadata` fields. Verified attr.h mappings: device
`ATTR_CMN_DEVID`, inode `ATTR_CMN_FILEID`, mode `ATTR_CMN_ACCESSMASK`, uid `ATTR_CMN_OWNERID`, gid
`ATTR_CMN_GRPID`, modified `ATTR_CMN_MODTIME`, changed `ATTR_CMN_CHGTIME`, flags `ATTR_CMN_FLAGS`.

**Links and size are the real obstacle.** They live in the type-dependent groups
(`ATTR_FILE_LINKCOUNT` / `ATTR_FILE_DATALENGTH` versus `ATTR_DIR_LINKCOUNT`), and the existing
bracket accepts both `S_IFREG` and `S_IFDIR`. For directories there is no attrgroup member that
equals `st_size`, and `ATTR_DIR_LINKCOUNT` does not generally equal `st_nlink`. So a like-for-like
`during` is **not reconstructible for directories**. Two defensible routes, and the choice must be
explicit rather than silent: branch on `ATTR_CMN_OBJTYPE` and reconcile the directory fields in a
reviewed note, or keep metadata comparison on `fstat` and place the bounded ACL read inside the
same before/after sandwich — which is strictly weaker, because the ACL is then no longer atomic with
`during`, and must be reviewed as a named weakening.

Layout follows the documented getattrlist packing and canonical attribute ordering (pinned
`bsd/man/man2/getattrlist.2`), not request order; offsets must be derived from that, never invented.

## 4. Derivable work versus profile premise

Derivable now, per capture: **1** `fgetattrlist` outer call; **1** caller-owned fixed buffer of a
constant size (fixed common attrs + 3116); optionally **1** further call and buffer for the volume
capability; and **≤ K** `mbr_uuid_to_id` outer calls, where K is the number of mutating-allow ACEs
(today's loop resolves only `tag == 1` entries whose mask intersects MUTATION, so K ≤ 128 and is
usually far smaller). The 413 decoder adds **zero** allocations — it is borrowed and alloc-free.

Remains a profile/TCB premise: `mbr_uuid_to_id` internal allocation, directory-service IPC, cache
state, latency and any network effect; kernel-side filesec construction; allocator behaviour and RSS.
Outer call counts are not allocation proofs — the same split already stated for the account observer.

## 5. Next experiment, adapter boundary, fixture matrix

**Adapter boundary:** mirror the in-tree pattern that already works —
`directory_volume.rs::read_uuid_with(file, syscall)` takes an injectable `fgetattrlist`, bound to
`libc::fgetattrlist` in production, with a before/after recheck and refusal on incomplete attributes.
Reusing it makes the parser testable without native fixtures and keeps this off greenfield.

**Next probe (root's lane):** one descriptor, one call requesting the joint set — common metadata
plus `ATTR_CMN_EXTENDED_SECURITY`, with `FSOPT_REPORT_FULLSIZE` — reporting the returned bitmap,
each attribute offset/length, `full_size` and `entrycount`. It should include a **directory**
fixture, which r4–r6 do not cover (all used `mkstemp` files); that is the gap §3 turns on.

| Fixture | Expectation | Level |
| --- | --- | --- |
| no ACL, capability supported | attribute omitted → **refuse**, never empty | runtime |
| 1 allow ACE | present, count 1, 68 bytes | runtime (r5 already) |
| 128 ACEs | present, 3116 bytes, fits the fixed buffer | runtime |
| `entrycount == NOACL` | positive "no ACL" | runtime; may be unobtainable locally — say so if it is |
| `entrycount == 0` | positive "empty = deny all" | runtime; same caveat |
| short buffer | rc 0 but `full_size > supplied` → refuse | proven (r5) |
| **directory** | links/size reconstruction | runtime, **new** |
| volume lacking the capability | refuse | runtime; may be unobtainable locally |
| malformed/adversarial bytes | decoder refuses | code-level only |

Synthetic-byte decoder tests are **code-level** and prove no native property; runtime fixtures prove
one API response on one machine and OS version, not qualification.

**One concrete defect in the 413 draft.** It computes `explicit_no_acl` and then never exposes it:
`Acl` offers only `flags()` and `entry(index)`, and maps `NOACL` to `count = 0`. A consumer therefore
cannot distinguish "empty ACL, deny-all" from "no ACL, GUIDs only" — the very distinction kauth.h
created the sentinel for. That is the same conflation the audit is about, one level deeper, and it
should be fixed before the decoder informs any policy.

Nothing here supplies InitialActor, platform, custody or creator authority, amends selected law, or
resolves the UUID membership service, which stays opaque TCB work with no filesystem, home or
environment shortcut.
