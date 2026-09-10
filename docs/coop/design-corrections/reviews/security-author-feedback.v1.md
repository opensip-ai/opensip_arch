# Codex review feedback to security author — incomplete draft

Please complete your unit after quota reset and address these issues before handoff.

1. clock_decision currently computes expiry at an untrusted far-future t_eval
   while only persisting a capped high-water at lastAccepted+90d. Correcting the
   wall then makes evaluation time go backwards from the time used to expire
   trust. This needs a coherent rule, not an unsafe clamp. Prefer refusal of an
   unattested excursion before expiry evaluation and before any floor write;
   corrected time can then continue. Explicitly distinguish signed/admitted time
   evidence from untrusted wall and ensure all successful evaluations preserve
   their accepted monotonic floor. Future payload checks/expiry must still fail
   closed. No attacker can freeze old payload freshness by repeated reboots.
2. Fresh install branch currently accepts wall with payload=None, sets all
   expiry states False and permanently initializes far-future floor. An
   authoritative trust operation needs admitted root/revocation time context;
   report-only must not return actionable write fields. Add fresh-future cases.
3. Most critically AR-04 includes existing poisoned high-water recovery, not
   just preventing future jumps. Define a safe explicit signed recovery epoch
   or equivalent authenticated transition that preserves revocation/root/key/
   rollback floors and custody while succeeding after a previously written
   years-future floor. If impossible offline, say the exact artifact/quorum
   required and provide both success and replay/downgrade refusal cases. No
   silent floor reset or namespace deletion. D367 authorizes design choice.
4. Revocation model says reversible completed effects get reverted but does not
   model user edits since commit. Rollback must compare exact committed
   postimages; mismatch is reported blocked/indeterminate, never overwrite user
   changes. Separate commit linearization from non-request child execution:
   kernel/process observation limits cannot promise zero external effects
   after REV when arbitrary trusted repository code runs unconfined.
5. Polling bounds are implementation qualification obligations under OS
   scheduling assumptions, not an absolute wall-clock guarantee in a stopped
   process. Pin monotonic timer, authority checkpoint and fail-stop behavior.
6. Product semantic identities use foundation snapshot2/plan2/fact2 etc. Security
   signed metadata may retain its independently versioned NFC profile; do not
   silently mix it with the new no-normalization content serializer. State/core
   migration must name both decoders and required signed core bridge explicitly.
7. Complete source-pinned schema/cases/checker/normative contract before final
   response. Every reference boolean signature/principal observation must be
   labeled trusted model input; don't claim cryptographic/OS measurement.

This is an intermediate review of unfinished bytes, not acceptance.

8. Discovery `_dir_custody` currently allows group-writable ancestors, merely
   records them, and reads opensip.json there. Group-write on the directory lets
   another principal replace even a mode-0600 config. Reject/boundary-stop
   group-write unless the entire group principal is explicitly authorized;
   disclosure alone does not close AR-03. Include POSIX ACL write grants in
   the native custody obligation; mode bits alone do not establish exclusion.
9. On a VCS boundary without config, choose that repository root (and discover
   monorepo units), rather than resetting selectedRoot to nested CWD. Otherwise
   default runs silently change repository scope by launch directory. Explicit
   --project/--scope remains the override. VCS indirection files are data with
   validated target bounds; no following arbitrary .git paths out of custody.
