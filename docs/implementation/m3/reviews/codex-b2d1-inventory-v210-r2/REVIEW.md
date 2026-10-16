# B2-D1 inventory v210 round-2 review

**Verdict: ACCEPT-UNIT.** Inventory candidate assessment: **ACCEPT**. No required findings or nonblocking observations. Product qualification: false.

## Round-1 correction

B2D1INV210-R1-RF-1 is resolved. The new yaml_subset.rs description now correctly states LF or CRLF line breaks, bare CR refused, and no leading indicator for plain scalars. No code change or inherited-row override was made.

Independently established the exact delta: reversing only these two description substitutions reconstructs the round-1 candidate's exact byte count and SHA-256. Reversing only the resulting candidate pin changes reconstructs the round-1 successor record's exact byte count and SHA-256. The census pin is unchanged. No unrelated candidate or record change was found.

## Exact subject

Rehashed the 698-byte staged manifest: `a255ee5b4d0bdd849d9cec4e602c1d78bc58e39927d228b5c51fbcaa72a410e1`. All three subject members match their pins.

- Candidate v210: 711,554 bytes, SHA-256 `31487036a79e0f1ba94871eb2407acb126275634f4a058801fc0a2028e381832`.
- Parent v209: 708,851 bytes, SHA-256 `c20976abdf1003c42091ea8b27e2814749975e6cf5a4909c63ffebf9cf5a9deb`.
- Successor record: 5,537 bytes, SHA-256 `7af0711bd14a8e84dcf177a76ebc5698d7d7b3f5cc699cf48c777938b0a99eff`.

The parent, accepted-code review, accepted-code subject and integration census pins are exact. The code review is ACCEPT-UNIT with no required findings and names the exact accepted subject. All six integrated paths match accepted archived bytes; no code re-review was performed. Live product main is clean at `46ed61aec70b61f8805521ccbc8b3db57ac49f69`; architecture HEAD is `f2c7e448863577cba44a7fe9c0d9c8c80a6ccd8a`.

## Inventory content

The candidate has **1,289 rows versus 1,285 in the parent**. Exactly the four stated paths are added, with no prior planned row. Their packages/roles are appropriate: opensip-host source, test and fixture, plus tooling builder. Only yaml_subset_vectors.json is generated. The corrected descriptions accurately describe the accepted library unit and evidence without granting qualification or mint authority.

Every inherited row remains equal by value. All other top-level fields remain equal, including **20 packages and nine pending decisions**. The candidate is sorted, unique and a strict superset. It covers all **1,191 tracked product paths**. All **98 inherited planned, still-absent paths** are retained unchanged without implementation claims. addedFiles and inheritedPlannedFilesRetained match the independently computed lists exactly.

The inherited lib.rs and test_discovery_fw01.py descriptions remain true, though incomplete about the new reader. No override is needed for either.

## Census and scope

The permitted live source check passes with **114 rows and no findings**, matching the staged census. Checker and exceptions pins match product bytes and are unchanged from the pre-B2-d1 base. The exception record contains the unchanged **439 mint-audit rows**. No mint authority is added. Census and successor explicitly disclaim product qualification.

The lead's assent, architecture publication and separate inventory-lock binding with fresh verify_design remain subsequent actions; this review does not claim them complete.

## Boundaries

Only reading, hashing, JSON parsing, Git queries and the explicitly permitted source check were used. No compiler, Cargo, tests, lane, network, other pane or delegation. No prohibited fixture, installation directory, signing key or held tree was accessed. Neither repository, stage nor control files were edited. Only REVIEW.md and review.json were written in the requested review directory.
