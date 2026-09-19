# Independent review — frozen `trust-layout-reference-checkpoint-201`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: the frozen 201 reference bytes — owner follow-up to my 199 review: floor placement (F-1), transition-layout boundary (W-1), spelling vs stored names (W-2), provisioning and marker notes (N-1, N-2, N-4). Prose only. Not native, host or implementation approval; nothing cumulative.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `ebd5b03f68479c26cfa10b1784a9f796f0ecd594c56b5e5389911874b86eeeb5`, 2,193,960 B = request = `archive-pin.json` |
| Members | 1,376, all regular/safe, verified from the tar before extraction; re-verified at the end |
| Candidate pins | 1,300/1,300; none unpinned; declared changes equal computed |
| Parent | equals **my own verified 199 extraction**; 10 changed = five prose owners (layout, readonly, S&L, build plan, carrier-format) + five pin manifests; **91/91 Python identical**; models, SQL, schemas, fixtures identical by pin |

## 2. Owner checks re-run
Reference order, `-I -B`, fresh outputs: all seven lanes exit 0 (`claude-out/owner/exits.txt`); integration 1,787 passed, carrier 479 / 0 failed. No lane exercises a file system.

## 3. Closure of 199

| 199 | 201 | Status |
|---|---|---|
| **F-1** floors beside the journal they guard | `trust/journal-floors/N/G.floor`, "deliberately outside `host/projects/N/` as well as outside every store instance. Restoring a project namespace's journal/witness directory alone must not restore the trusted high-water files along with it." Bound stated honestly: coordinated rollback of both domains, incl. whole-installation rollback, "remains outside that detection bound; no monotonic hardware anchor is claimed". Still option A: no collection copy, no `trust.sqlite` duplicate, six-counter law untouched | **closed.** All four citing owners were updated to the same wording; a tree-wide search finds **no residual** "projects/N/floors", "stable namespace", "beside SC-OPS" or "namespace-scoped collection" (one hit is the new "namespace-keyed … separate install-level trust domain" sentence). The S&L l.718–723 / v8 §5.4 non-rollback claim is true again for a namespace-directory restore |
| **W-1** transition objects unplaced | new "Deliberate transition-layout boundary": lists all seven (ancestor-stage carrier, carrier binding/state record, prepared six-counter image, source-fence record, selection pair, active-slot/transition-journal carrier, lineage table); "needs a versioned location owner before implementing those writes"; `.staging/E` reserved for the forward tree, not inferable for the ancestor carrier; "No filename or typed path value is evidence that a transition progressed"; build plan repeats the boundary | **closed** as a scope statement. The work itself remains, as said |
| **N-2** `floors/` creation discipline | fenced authorized provisioner; exclusive no-follow creation, root/invoker ownership, 0700, directory+parent barriers before use; existing components need custody admission, "a spelling collision is not adoption"; readers never provision; missing dir/file = absence only **after** the parent context is admitted, unreadable/misbound parent = unavailable | **closed**; consistent with S7.1 (absence ≠ zero floor → `unknown-custody`), so deleting `trust/journal-floors/N` fails closed |
| **N-1** marker bridge cost | installed product `fa72e50` has no marker writer or store creator → no earlier product encoding; explicitly "not a claim about arbitrary preexisting files"; unsupported bytes refuse without reinterpretation | **closed** (I did not inspect `fa72e50`; this is the owner's statement of fact) |
| **N-4** 72 vs 128 | "The cap is 128 bytes; a valid marker … is 72 bytes" | **closed**; equals my computed value |

## 4. W-2 — the owner declined my suggestion, and is right to

My 199 W-2 said "The before/after **name observations** the owner already demands are what close this — say that they compare the stored name bytes." **That asserted a mechanism I had not checked.** Checked now in my verified 198 product extraction: `platform/src/filesystem/path_binding.rs` compares `dev`/`ino` per re-resolved edge (l.68–69, l.146) and its own doc comment says "Spelling is retained, but OS case/normalization aliases may bind the same identity" (l.26–27). It does not read directory-entry bytes. 201's wording — spelling restrictions apply to "constructor inputs or emitted components … not a claim that the filesystem stores the same case"; "No stored-name byte comparison is claimed or silently added here" — is the accurate statement, and mine was not.

**Does any existing identity/custody law require stricter entry bytes for these layout components?** I looked for one and found none:
- *Identity* is never the name: store identity = marker == S **and** the five-member binding digest; carrier identity = `projectKeyDigest` in content; namespace = registry binding. An alias that resolves to the same object yields the same marker, the same content and — for leases — the same lock inode, which is the property S7 needs.
- *Creation/publication* laws are exclusivity laws, and aliases make them stricter, not weaker: exclusive no-follow create and no-overwrite publication fail with "exists" when a case-alias entry is present on a folding file system, which is refusal, not adoption ("An existing directory cannot be adopted"; "a spelling collision is not adoption").
- All variable components and fixed names are ASCII, so Unicode normalization cannot alias them; only case folding can.
- The one existing law that *does* compare path bytes is the registry's **project root** binding ("compare all four values and canonical native path bytes with registry", lifecycle contract `nativeIdentity`) — a different object (the repository root), already paired with dev/ino/birth, and outside this layout.
- Where entry spelling *will* matter is **enumeration**, not lookup: a GC/census/purge that lists `host/projects/`, `stores/` or `trust/journal-floors/` and compares listed names with registry values byte-for-byte would see a case-variant entry as "unregistered". Existing law already blunts this — "A directory listing is never selection, registration or transition progress proof", cleanup only of directories "with no retained journal/witness/root", "this layout grants no deletion of retained trust files" — but when a census owner is written, it should say that a non-canonical spelling is *foreign and untouched*, never the namespace and never garbage. That is future work, not a defect here.
So: no stricter law exists, none is needed for identity, and 201 correctly leaves alias behaviour to native qualification. I withdraw the mechanism claim in my 199 W-2; its residue is the enumeration note above.

## 5. Findings
No new finding. Two small observations:
- **N-1** S7's summary sentence now lists both "per-generation trust floors … stable across store selection" and "places journal high-water files under the separate install-level trust domain" — the same objects named twice under two names. Not contradictory; one name would read better.
- **N-2** `I/trust/` itself is not a row in the location table (only the floor path and `trust.sqlite` are). The provisioning paragraph covers "any missing trust/journal-floors/N directory components", which includes it; a table row would make the 0700/ownership expectation for the trust directory explicit, since it now anchors the detection property F-1 was about.

## 6. Limits
Owner-text review; lanes re-run; one product source file read only to check the mechanism statement in W-2 (no product build or test). No file-system experiment: case-folding behaviour is reasoned from the stated laws and POSIX exclusivity semantics, not measured, and belongs to the owed native qualification.

## 7. Verdict (bounded)
**201 closes 199 F-1 with the separate install-level trust subtree and an honestly stated bound, applied consistently in all five owners with no residual old wording; W-1, N-1, N-2 and N-4 are closed as clarifications. On W-2 the owner's precision is correct and my earlier suggestion asserted an unverified mechanism: the product compares device/inode, not entry bytes, and I found no existing identity or custody law that requires stored-name equality for these components — only future enumeration-based operations need a spelling rule.** No approval of implementation, native qualification or cumulative readiness.
