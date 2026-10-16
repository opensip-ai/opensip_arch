# B3-B3A1-r1 review

Verdict: **ACCEPT-UNIT**.

Required findings: none. One non-blocking wording observation appears below.

The subject manifest is 18195 bytes, SHA-256 `ffe3c284165b8a816450213a59797f8be3350aa8e1c1fc95b21e44d49fd9d92d`. All 75 members independently match their sizes and hashes. All eight mapped candidate files match the archived bytes and their parent pins, and the candidate changes exactly those paths. Product main is clean and the detached candidate is at `e367d7f465d8d0a74819cad5010a58b8641e4c7a`; architecture is at `ea65b4d5c6a481fde25974f48ef9588e2033898f`. Source authority and product-lock pins also match.

## Model and charge assignment

The model follows the current native request paths: the reused directory stack, status and by-name observations, shared bindings, per-phase entry/custody memoization, captured ACL/premise alternatives, bounded reads and post-read checks, and kept-read copies. Its item-6b model includes the pass-level sources once, W's device sample, each candidate's reserved identity slots and path records, placement markers, layout probes, config parsing and index decoding. The model deliberately combines ceiling/dearer alternatives as an upper bound; it does not claim these alternatives all occur together in one successful observation.

The modeled decision requests follow carrier selection, placement, visible-repository traversal, candidate checks and custody, member observation and links. Composition preserves branch B's links-before-walk order and branch A's fresh link observation after the walk, with one binding table across phases. Existing bindings are charged once; each fresh observation still pays its own observations, custody and reads. Member descent carries the walk's new bindings, while the walker itself receives admitted members. Ignoring index gitlink boundaries is conservative for descent and link reads here; the accepted product's gitlink-boundary behavior remains unchanged.

The reader/member/descent assignment preserves A2/A5. Placement and listing remain chargeable even at zero admitted members. Uncharged pure-reader parses contribute no invented ledger term; charged item-6b parsing/decoding remains included.

I tried additional inputs by importing only the permitted model module: a glob over visible directories with no repository/member, and two Cargo patch sources sharing one member and provider manifest. The former retained a nonzero member term without starting a session. The latter retained one member/session and charged repeat reads as copies. Feeding already-bound paths to descent added no duplicate records. These isolated request/memo probes used small cost operands, not native measurements; they supplement source comparison rather than replace the archived native evidence. No additional under-count was found.

## Closure, constants and envelopes

All 19 closure files rehash correctly. All 53 anchors match exactly once. The extension covers the four D15 request/charge owners and their existing platform helpers; the new metadata and identity-slot sizes are asserted against the build by the recorded tests. Formula anchors cover reads, record ownership, captures, binding/copy costs, config parsing, decoding, identity reservation, status and fixed-path opening. The two new generated-vector pins bind the model and composition inputs.

LD-2 is acceptable as an explicit structural envelope under item 12: D15 regular-file read attempts fill available buffer space or reach EOF, with interrupted retries excluded. This acceptance is conditional on that declared envelope; it is not a guarantee against arbitrary short reads, interruption or all filesystem behavior. The walker retains its existing one-byte envelope. Model probes give 12 attempts and 12,578,817 charged buffer bytes for a 4 MiB index at the ceiling. A one-byte-per-attempt envelope would require roughly 4.2 million edges for that index alone, exceeding the 2^21 edge cap and returning the caps to law. Native observations taking fewer attempts are supporting evidence, not the justification for silently changing an envelope.

LD-3 covers the admitted item-6b branch at config/index ceilings, global sources and fixed system sources. Charging a cap-plus-one read together with a cap-length parse/decode is conservative even where the actual oversized read would refuse before parsing. The macOS ARG_MAX environment estimate is an explicit platform envelope, not a new product input limit; it does not affect these repository rows because none starts a member session. Its application to workspace margins remains for B3-b3c. LD-4's per-dimension maximum of ACL ownership and premise checking bounds both native capture alternatives. Charging admitted descent without gitlinks supplies the larger traversed population.

## Rows and equality projection

I independently compared both candidate JSON records to main. The census differs at exactly 42 locations: closure, two sizes, and `d15` on 39 lead-readable repository rows. The vectors differ at exactly six top-level locations: closure, those two sizes, model pin, composition-vector pin and composition predictions. These are precisely the recorded allowlists; inherited walker fields, populations, margins, held-out standing and workspace rows remain equal.

Full-ledger classification correctly uses walker plus all three terms and can fail an entry and return the caps. All 39 lead-readable repository full-ledger rows pass. The tightest edge row, `rs-very-large-aws-sdk-rust`, has 1,747,455 objects, 1,007,770 edges and 431,546,479 bytes at R=4096; its margins are 2400/2080/2488 per mille. The test checks full-ledger arithmetic and classification rather than treating walker-only success as sufficient. Workspace full-ledger margins and held-out margins remain outstanding.

## Validation and evidence

The recorded native soundness run has 23 cases at each of R=134, 1024 and 4096: 69 measurements, all within prediction. Its accepted composition cases cover members, shared paths, exact roots, excluded members, and nested repository/project/pruning boundaries. The worst cases add ceiling carrier/config/index reads, global and five system sources, an oversized index, and descent-heavy storage. The valid-index builder reaches exactly 4 MiB with ordered version-2 entries and a SHA-1 seal, exercising the decode rather than stopping at a malformed header.

Measurement subtracts the ledger counters after retained-chain/item-6a preparation and before discovery, retaining the same ledger and failure latch. Synthetic root spellings vary the charged spelling length without inventing an impossible physical filename. LD-6 is therefore sound. Including the control from the existing test file avoids changing the production closure owner, as LD-7 states.

The worst exact-root case is exact in objects/edges (272/2528), with 4922 bytes of conservative slack; worst descent is exact in every dimension. Root-in-repository and oversize-carrier cases are exact too. The initially missed W device sample is now modeled as one edge and 512 bytes; removing it fails the near-tight exact-root case.

All five archived mutations fail the native measured-versus-predicted assertion: reader read omitted (root-in-repository), member index read omitted (worst automatic, byte under-count), W device sample omitted (worst exact roots, edge under-count), descent omitted (root-in-repository), and admitted walker members ignored (Cargo two-member case). The runner regenerates vectors for each mutated model and restores the bytes. These are runtime under-count detections, not compiler failures.

I independently parsed equal named full-suite failure sets: 14 at base and candidate, with total passes 1165 versus 1166. The full suites retain those base failures. The final lane also records passing warning-denied Clippy with and without scenario fixtures, formatting, the focused census/discovery tests, every vector check, FW-01/storage controls, 18 census controls, 19 synthetic blind controls, environment and operability checks, census verification over the readable cache, and successful verify_design with qualification false. Attempt 1 remains explicitly failed on formatting and Clippy's index-builder lint; the final attempt resolves those failures and is the lane of record.

I ran only the permitted vector-only census command, which passed and read no T2 store. The cache census and native executions above are reviewed evidence, not independent reruns.

## Non-blocking observation

**B3B3A1-R1-NBO-1 — regular-file envelope wording.** SCOPE LD-2 and the model read-envelope docstring say every D15 read is opened no-follow. Refusal-only system sources instead deliberately use `open_fixed_regular_following`; they may follow symbolic links, while still requiring a regular final file. The regular-file envelope remains applicable. Distinguish those sources from member/carrier/provider evidence when refining the wording.

This acceptance closes only B3-b3a1's bound unit. It is not B3-b3a2's pre-run gate, authorization for a held-out run, workspace-margin acceptance, qualification or completion of B3-b. No repository, worktree or control file was edited. Only the requested review artifacts are written. No compiler, Cargo, tests, builds, lane, network, prohibited fixture/installation/key/held-tree access, T2 held-out store, other pane or delegation was used.
