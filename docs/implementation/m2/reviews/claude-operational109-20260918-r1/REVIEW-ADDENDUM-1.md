# Addendum 1 to the operational109 review — N-4 wording corrected

Reviewer: Claude. 2026-09-18. `REVIEW.md` is left byte-unchanged
(SHA-256 `3f9e45df34878eb5bf49d4232138d15dee9025225c25b38dd192e47a60aaf409`); this addendum supersedes its N-4
paragraph only. Verdict and all other findings are unchanged.

**What I wrote** could be read as "empty bytes may establish `witnesslessRestore`". That is wrong and
not what the owners say. Corrected statement, which I confirm:

1. A file that **exists and was read successfully with zero bytes is `Present(empty bytes)`**. The
   codec refuses it (`Decode`), and the capture layer reports it in the *malformed* class
   (`witnessMalformed` / the floor equivalent). It is **not** `Absent`, and it never supports
   `witnesslessRestore`.
2. **`Absent` comes only from an admitted filesystem presence result** (a definite not-found from the
   admitted directory handle). Only that observation can feed the v8 §5.4 row "witness absent with a
   non-empty journal → `witnesslessRestore`".
3. **Unreadable stays unavailable** (I/O error, permission, short read, non-regular object): neither
   malformed nor absent, and never a manufactured zero floor.

Owner support: v8 §5.4 lists "witness absent" and "witness fails the closed shape … string" as
separate rows, and the closed-shape row is about *content*; the read-only owner states for the carrier
that "a missing, empty or fallback carrier is never absence". Nothing in either owner lets content —
including empty content — prove absence.

The residual point of N-4 is therefore only this: the codec cannot itself distinguish the three
observations (it receives bytes), so the capture layer must carry presence as a separate typed
result and must call the codec **only** for `Present`. The 109 test name
`…limits_are_not_absence` already reflects this. No change to 109 is requested.
