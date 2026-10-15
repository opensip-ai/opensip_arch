# B2-b3 plan r3 amendment review

Verdict: **ACCEPT**. No required findings or non-blocking observations.

## Subject and review scope

The 452-byte subject.json independently hashes to `bdf28579b863d79cc451e784e9ab559c6b6ef8e0c12f1524093972fc280fffe5`. Its sole member, docs/implementation/m3/config-discovery-b/b2-b3/PLAN-r3.md, independently matches 26,476 bytes and SHA-256 `30968bea104d3e310217f177227f9f44551e0f808309d826bca236fb051502aa`.

Product HEAD matches `aa037d09995f7710bda5f8993ff9133f829e3df3` and is clean; architecture HEAD matches `c568f47930163bc3c8a85457c060a09eff0a4e34`. The review is limited to the LD-B2B3-12 amendment and its related facts, split row and sequencing text. The full diff against accepted PLAN-r2 was inspected. LD-1 through LD-11, LD-13 and section 3 remain unchanged.

## Facts and fixture gates

The amendment's relevant facts are correct. X8 r3 item 4b uses the single X9-1 site list and expressly requires a law revision for an additional fixture gate. crash_matrix_sites.rs identifies the shared installation fixture while specifying that its read-session helpers remain cfg(test). installation_read_fixture::session_at and ObservationSession::for_tests are cfg(test), so widening those helpers to the repeatable scenario-fixtures read seam contemplated by r2 would require changing the accepted gate policy. Existing production read-session admission is not such a repeatable fixture constructor.

The host's resolve_analysis_configuration and its input types are pub(crate). A separate integration-test crate cannot call them. B1-b's existing a_refused_project_pack_stops_before_the_registry_composed_across_crates control is a host unit test and demonstrates the proposed resolver/captured-carrier callback pattern without publicizing the resolver.

## Write-path composition

The amended order is sound: analysis phase 1 with the explicit path, waiver and upward record; host resolution and immediate pack admission on the captured carriers and CLI layer; phase 2 with the waiver; tracking and conditional first registration; begin_operation and its fence-releasing handoff; discovery_root and downward discovery on one fresh discovery ledger; operation end.

InstallationAt::writer and its existing operation composition already reach the required signed-tree, fixture-home, writer, trust and handoff gates. The amendment introduces no new cfg predicate, fixture receipt producer, observation-session reset, lending constructor or production authority surface. The callback returns resolution data rather than security authority. Selection/refused configuration ends before later admission stages, with the writer released. The retained r2 control explicitly prevents resolution/pack-admission failure from reaching phase 2 or downward observation.

The extra tracking, registration, namespace/lease and end work is fixture operation setup/teardown in the synthetic scratch installation. It is not attributed to discovery, and does not authorize discovery writes in production. The walk still begins after the actual handoff and consumes the existing ProjectOperation lending. Implementation review must verify the ordinary chain and all refusal cleanup as specified; plan acceptance does not establish that unimplemented seam behavior.

## Flag controls and owner path

The planned controls cover the COV source-join method for --project and --workspace-root: explicit selection from a different launch, absent explicit path before resolution, owner-waiver provenance and non-waivable other-write refusal, CLI workspace-root precedence and flag-layer provenance, missing named-root refusal without automatic fall-through, configuration-only roots, and automatic discovery when neither source is present. Rejecting configuration project/trustProjectOwner impersonation before phase 2 tests the consent boundary. Returning plain records lends no execution or custody authority.

Leaving foreign-owner behavior with the already accepted selection and walker vectors is sound for this fixture composition. Those controls test the typed waiver and unwaived markers using supplied invoking identities; the host seam's owned scratch roots test source joining and provenance. The amendment does not claim that these together qualify foreign-owned production admission or every later write-path waiver consumer.

COV:5268-5407 names crates/host/tests/discovery_tests.rs as a planned behavioral owner and specifies exact applicability, provenance and precedence, with selection granting no execution/custody and configuration unable to impersonate consent. Parent plan r4 LD-B2B-7 explicitly uses the test-only scenario seam until J1. Verifying the same source-join behavior now in a host unit-test module is a reasonable interim owner location because the resolver is crate-private. The amendment retains the COV integration path as planned for J1 and requires B2-b3c's records to identify where these controls actually run. It does not rewrite COV or declare J1's public integration coverage complete.

The rejected alternatives are justified: widening read-session fixture helpers would change the gate policy; an extra released-writer lending would alter LD-1; making the host resolver public solely for integration tests broadens the API unnecessarily; and deferring all flag controls would leave B2-b's present obligation untested. No accepted decision outside this amendment is changed.

## Verification limits

Evidence came only from read-only reading, hashing, JSON parsing, text comparison and Git queries. Inspected X8 item 4b/4c, its product site-list pin, the shared writer/operation and read-session fixture sources, scenario.rs, the host resolver and existing cross-crate control, parent plan r4 LD-B2B-7, and the cited COV flag entries. No Cargo, tests, builds, lane, network, private fixture, installation directory, signing keys, held trees or T2 held-outs were accessed or executed.

Only REVIEW.md and review.json were written. Neither repository, stage nor controls were edited. No B2-b3c code, binding, law amendment or product qualification is claimed.
