# Law X12 r3 — configuration and policy-pack admission

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `policy-admission-x12/PROPOSAL.md` is 26705 bytes, sha256 `11628912f6bb63de9c8255178f2b5833163179f114b6f7a563c32871d34822ff`, matching `hashes.txt`. Preserved r2 is `PROPOSAL-r2.md`, 26394 bytes, sha256 `62bcdab188cdb8d67a7c2cef8d8715829d7fbc2d913433fda38d67458d2ad3bc`, the reviewed r2. Live product HEAD is `66bdd05ea71f8293ae104da697dbcf96f7d52f44`.

The diff from r2 is the title, the r3 provenance sentence, and the Declarativeness bullet.

## What holds

r2 RF-1 is closed. The bullet now forbids an imperative member or string expression in a document the caller presents from surfacing as anything but row 3, detail `POLICY.IMPERATIVE_KEY_REFUSED`, subject the member's pointer, and it states that a bundled imperative member surfaces as row 4. That is the same split item 7 already states: row 3 is a `Supplied` item 6.2 failure, and row 4 is a bundled item 6.2 failure with subject `pack:<packId>`. The types-and-codes bullet that forbids a bundled imperative member from surfacing as row 3 agrees with it. The r2 holdings on X12-0, the unchanged public code, and the zero-row registry stay in force.

## Verdict

ACCEPT. r2 RF-1 is closed.
