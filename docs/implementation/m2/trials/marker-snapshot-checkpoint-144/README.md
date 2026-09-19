# Candidate 144: quarantine markers from a retained SQLite snapshot

Unaccepted, uninstalled implementation candidate based on frozen 143. This adds the SQL marker reader required by the reviewed marker125/reference142 contract. It does not confer continuation, mutation or custody authority.

`CurrentCarrierSnapshot::capture_marker` reads `carrier_quarantine` through the snapshot's existing read transaction. The private child module owns admitted marker construction. It captures SQL `typeof` values and `CAST(body AS BLOB)`, requires UTF-8 for present markers, admits the exact nine-member canonical document and checks project/generation/reason/tail mirrors. The observation distinguishes absent, admitted and unusable. SQL failures remain errors. Within-bound raw bytes remain owned and unchanged for both admitted and unusable observations; an over-bound value is unusable without copying it. The existing SQLite length limit also bounds engine reads.

UTF-16 carriers remain allowed by the generic carrier contract: absence is still absence there, but present UTF-16 markers are unusable. The reader does not rewrite, normalize, insert or delete markers. Invalid historical inputs are not repaired.

Validation: 166 independently reference-derived row cases (25 admitted, 141 refused); actual SQLite tests exercise concurrent journal/marker writes after transaction opening, mutation/deletion after capture, exact byte ownership, byte bounds, SQL errors, and both UTF-16 encodings. The full security suite has 85 tests. Eight compiled behavioral mutants are detected. Strict workspace Clippy passes after an equivalent boolean simplification. Final exact-source isolated host88 uses 34 pinned fixtures and 51 checksum-verified crate archives; host87 is the preserved pre-Clippy-expression run. Mutation/security r1 receipts precede that equivalent expression edit; host88 tests final bytes.

Initial generator refused a deliberately out-of-range integer before emitting fixtures; the negative-fixture raw encoding fallback and failed attempt are retained. The initial Clippy diagnostic and pre-edit source are retained. No test is represented as having passed on different bytes without disclosure.

Still required: complete generation population/origin/gap/predecessor admission, inherited history, historical floors, retained ancestor custody and exclusion, actual writer/recovery integration, consumer qualification and formal selection. This is one component of 118I2, not closure of that whole issue. Production M2 and M3–M6 remain incomplete.
