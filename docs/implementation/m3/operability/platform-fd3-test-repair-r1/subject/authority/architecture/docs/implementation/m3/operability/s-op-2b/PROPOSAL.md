# S-OP-2b. The harness instrumentation sink

**Draft r1, PROPOSED, not accepted.** 2026-10-05. Grok, implementation lead. This design unit is the owed contract successor named by the accepted law M3-O1 r2 (X-O1). The body below that heading's owed paragraph is that law's owed text, taken from `PROPOSAL-r2.md` and unchanged. Nothing here binds the unit. Binding waits until S-OP-2-P and then S-OP-2-R are bound, because this record's parent becomes an accepted base only when S-OP-2-R selects it.

**S-OP-2b. The harness instrumentation sink.** Contract successor to S-OP-2 r6 (`docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, sha256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`). It adds one sink and changes nothing else.

1. **The sink.** Item 12's sink table gains one row: `harness`; owner: this successor for the channel and the content, Q0 for the projection; classes P0 and P1; present only in a build with the `harness-instrumentation` feature (rule 2). Item 12's projection rule applies unchanged: the encoder writes a field only if its static class is P0 or P1, and counts every other field in `omitted`.
2. **The build.** The feature is never a default and is never enabled from a `[dependencies]` table. It refuses, at compile time, any build without debug assertions. A featureless release binary contains none of the sink's strings, and a release-absence check proves it.
3. **Selection and level.** The feature is the release constant that selects the sink (item 21). The sink's level is the constant `info`. No environment variable, flag or configuration value selects or tunes it.
4. **The channel.** File descriptor 3, inherited from the harness driver. At logging start the host admits it once: it must be open, a FIFO or a regular file, and writable. The host then sets close-on-exec on it, so no child inherits it. If any check fails, the sink does not exist for the invocation: nothing is projected to it, and no tally counts it.
5. **Encoding and bounds.** JSON lines, under item 13c's wire schema, rule E and item 14's bound. The stream's first record is `log.stream.opened` with `sink: harness`. The `Sink` table gains the member `harness`.
6. **Accounting.** The sink is a persistent sink under items 15 to 17, with its own direct enqueue tally, writer snapshot, gate and marker. It has no pre-scope partition, because it is admitted at logging start, before any record. Finalization closes its gate as it closes any persistent sink's, and its outcomes are in the frozen summary.
7. **The record digest.** The exploratory envelope's `operationalRecords[].recordSha256` (`exploratory-quality-envelope.schema.v1`, r13) is the SHA-256 of the exact bytes the harness driver read from descriptor 3 for that invocation, from the first byte to end of file, a torn last line included. The host computes no digest of the stream.
8. **Reading.** The harness projects the stream only through item 13a's reader, at ceiling P0 and P1.
9. **Custody.** The stream is harness evidence in Q0's custody. It is never product evidence and never read by recovery. It enters no Run, Plan, Coverage, identity or digest, apart from `recordSha256` in the exploratory envelope.
10. **Control C-13.**
    - (a) A build without debug assertions refuses the feature.
    - (b) A featureless release binary contains none of the sink's strings.
    - (c) `recordSha256` equals the SHA-256 the driver computes over the bytes it read.
    - (d) The stream's first record is `log.stream.opened` with `sink: harness`.
    - (e) A closed, read-only or wrong-type descriptor 3 leaves the sink absent and the result unchanged.
    - (f) A reader that stalls or closes its end gives `sink-failed` or `drain-abandoned` within item 16's deadline, with the result unchanged.
    - (g) No child process inherits descriptor 3.
    - (h) C-4's canaries never appear in the stream, and no P2 field does.

**What it does not change:** any other sink, ceiling, kind, class, bound, escaping rule or reader rule. The phase events and the `PhaseOutcome` members the stream carries are ordinary registrations (M3-O1 item 14), not successor content.
