#!/usr/bin/env python3
"""check-delivery-v5.py -- the retained checker for artifacts/delivery.v4.json.

WHAT THIS IS.  A SUCCESSOR INSTRUMENT.  artifacts/delivery.v4.json is unchanged
and is not re-litigated here: its independent review returned ACCEPT with zero
blockers and this file exists to check those exact bytes.  Its PREDECESSOR
INSTRUMENT, artifacts/check-delivery-v4.py, was REJECTED FOR REPAIR on one
blocker and is now pinned by its own review, so section 7.6 forbids editing it.
This file is NEW.  It edits nothing and it is pinned by nothing.

WHY THE PREDECESSOR WAS REJECTED, AND WHAT CHANGED HERE.

An independent reviewer imported check-delivery-v4.py unmodified, re-pointed its
SUBJECT and PINNED constants at scratch copies of the artifact, and made it pass
on artifacts that are wrong.  Restoring delivery.v3's REJECTED DL-CLOSED-1 text
-- the exact bytes of the blocker delivery.v4 was written to repair -- produced
`exit 0, FINDINGS: 0`.  So did negating DL-DOM-1 and DL-ORD-1, reversing
DL-INJ-1's detector claim back to the overclaim v4 corrected, replacing registry
members with inventions, moving a memberCount from 8 to 99, rebinding
relationIds[] to the deficiency vocabulary, fabricating the artifact's own
quotation of section 6 law 2, changing the minted domain label, and replacing a
recordedInputs digest with sixty-four `f`s.

The cause is structural, not incidental.  The predecessor's census constants --
CM_KEYS, PC_KEYS, AC_KEYS, BOUND_SCALARS, OPEN_SCALARS, PLAN_FIELDS -- were
HAND-TRANSCRIBED PYTHON LITERALS, and the artifact's property names appeared only
in COMMENTS DESCRIBING WHAT THE CODE DOES.  It encoded the rule.  It never
verified that the artifact states the rule.  A hand-transcribed key list tests
the transcription, not the artifact, and the artifact's normative prose -- the
thing an implementer actually reads -- was unbound at every position.

THE THREE THINGS THIS FILE DOES DIFFERENTLY.

1.  EVERY CENSUS CONSTANT IS RE-DERIVED FROM THE ARTIFACT UNDER CHECK AND
    CROSS-CHECKED AGAINST ITS PREDECESSOR.  There is no hand-typed key list in
    this file.  Record key sets come from recordShape[*].requiredKeys and are
    compared against delivery.v2#capabilityManifestSchema[*].required.  The
    fourteen reachable scalar positions are DERIVED by walking the compiled
    record shapes over real admitted values, then compared with the artifact's
    published boundPositions and declaredOPEN.  Registry MEMBERS are derived
    from delivery.v2#platformMatrix and fact-plane.v1, and each bound position's
    registry is resolved BY OBSERVATION -- the unique candidate registry that
    contains every value the position actually carries across the predecessor's
    four live manifests and the artifact's seven committed vectors.  PLAN-ID-V1's
    thirteen field names, its framing bytes, its recipe version and its text
    prefix come from resolved-inputs.v2#planIdContract.  The domain label comes
    from the artifact's own closed domain vocabulary and is cross-checked against
    three other positions that spell it.  See class Contract.

2.  EVERY ASSERTION IS BOUND AGAINST AN INPUT THAT IS WRONG, NOT MERELY EMPTY.
    IMPLEMENTATION-FREEZE.md section 7.8 records that all four instruments of
    that session fired on REMOVAL and stayed silent on FALSITY.  Every mutation
    in the ARTIFACT half of --selftest keeps the shape and inverts the meaning:
    it edits the subject's bytes the way a reviewer with a scratch copy does,
    re-parses, and requires the run to fail.  --selftest reports, for each such
    mutation, both the finding codes it raises and the finding codes it raises
    WITH THE STATEMENT SEALS DISABLED, so a reader can see which mutations are
    caught by a byte seal and which are caught by a semantic gate that executed
    the artifact's own declaration and got the wrong answer.

3.  PUBLISHED CORPORA MUST BE NON-DEGENERATE.  A sibling instrument let 10 of 17
    published vectors collapse to one digest at 0 findings because it demanded
    distinctness only of synthetic values.  gate_corpus_distinctness asserts
    distinctness of the ARTIFACT'S OWN published corpus: seven distinct committed
    manifest VALUES, seven distinct committed byte strings, seven distinct ids,
    and -- over every manifest this run constructs, published and synthetic --
    that the number of distinct values equals the number of distinct ids, which
    is the injectivity the recipe claims.

THE SUBSTRING PROBLEM, AND WHAT IS AND IS NOT CLOSED.

`needle not in text` is defeated by keeping every needle and appending a
reversal.  versioning-policy.v10.json publishes the quantified boundary for that
technique -- "appending a false sentence while preserving every required measured
substring is admitted at 80 of them" -- and a sibling review found 63 such
positions in one instrument.  This file does not bind normative prose by
containment.  It binds it three ways, none of which a suffix survives:

  * STATEMENT SEALS (gate_statement_seals).  The seal DOMAIN is derived by rule
    from the artifact -- every string leaf that is a declared DL-* property, that
    is the `statement` of a declared admission gate, or that sits in the
    normative neighbourhood of a declared DL-* property -- and the domain is
    compared BOTH WAYS, so adding or deleting a normative statement is a finding.
    The seal CONTENT is the SHA-256 of the statement's NFC UTF-8 bytes, measured
    from the artifact and hard-compared against shasum(1) before this file was
    finalised.  A seal is not the whole-file pin at finer granularity in the case
    that matters: THE REVIEW THAT REJECTED THE PREDECESSOR RE-POINTED PINNED AT A
    SCRATCH COPY, which neutralises a whole-file pin and does not touch these.
    TWO HUNDRED AND SEVENTY-SEVEN positions are sealed -- every DL-* property,
    every admission gate, every per-field ruling, and every string leaf inside a
    block this checker compiles a constant from.  Append, negate, restore or
    fabricate at any one of them and the digest moves.

  * THE REJECTED CANDIDATE IS THE ORACLE (gate_rejected_candidate_differential).
    delivery.v3.json is a PINNED input.  Its normative statements are read from
    its live bytes -- never transcribed here -- and no string leaf of the subject
    may carry one of the statements the subject repaired.  The polarity of the
    repair is bound STRUCTURALLY rather than lexically: delivery.v3 carries the
    KEY `thereforeITALSOFINDSTHETHIRDONE` and the KEY
    `theTWOINSTANCESKNOWNTODAY`; the subject must carry NEITHER, must carry
    `andITDOESNOTFINDTHETHIRDONE`, and its instance list length must equal the
    channel count the subject's own selfMeasurement publishes.  A reversal that
    keeps every word and changes the claim has to change the key name or the
    count, and both are checked.

  * QUOTATIONS ARE VERIFIED AGAINST THE SOURCE, NOT AGAINST A TRANSCRIPTION
    (gate_quotations).  The predecessor hard-coded seven freeze anchors as Python
    string literals.  This file extracts every verbatim-marked quoted span from
    the artifact's own bytes and requires each to be PRESENT in the live bytes of
    the document the artifact attributes it to.  Nothing is transcribed, so
    fabricating the section 6 law 2 quotation makes it absent from
    IMPLEMENTATION-FREEZE.md and raises a finding.  Appending to a quotation is
    also caught, because a longer needle is not present either.

WHAT IS NOT CLOSED, MEASURED RATHER THAN CLAIMED.  The substring hole is closed
at every normative position and it is NOT closed everywhere.  Run
--append-census: it appends a false sentence to each distinct string leaf of the
subject in turn -- to EVERY position that leaf is written at, so a document that
states a property twice is attacked at both -- re-runs the whole check with the
whole-file pin neutralised, and reports where the run still returns zero
findings.  MEASURED on artifacts/delivery.v4.json at 3cffece0…:

    distinct string leaf values                   989
    appends the run REFUSES                       554
    appends the run ADMITS                        432
    leaves the census cannot reach                  3

The 432 admitted are FREE NARRATIVE PROSE -- operation `why` fields, repair
narratives, reviewer-checklist items, the author's stated objections and
residuals.  MEASURED: 0 of the 432 lies inside a sealed position and 0 lies
inside a block this checker compiles a constant from.  The comparable published
figure is versioning-policy.v10's, which records the same attack "admitted at 80"
of 340 leaves in its two partitioned scopes.  This residual is not closed and is
not claimed closed: closing it would require a machine-checkable schema for
narrative justification, which this corpus does not have.

WHAT IS CARRIED FORWARD UNCHANGED FROM THE PREDECESSOR, ALL OF IT VERIFIED
GENUINE BY THE REVIEW THAT REJECTED IT.  Exit 2 on digest drift BEFORE any parse.
A duplicate JSON key rejected by a parse hook that NAMES THE KEY, per section 7.5
-- "6 of 47 rejecting checkers never say which key was duplicated".  `type(v) is
bool` tested BEFORE `type(v) is int`, never isinstance, per section 6 law 18.
Sixty-five distinct 64-hex literals, each recomputed, hard-compared or declared
at digestAccountability, with the NO_RECOMPUTE_LEDGER mutation demonstrating what
a checker that compared stored strings to stored strings would look like from the
outside.  The leaf census by exact type: 108 integers + 31 booleans = 139, which
an isinstance walk miscounts, which is why the identity tests matter.  Two
independent CVE1 encoders and a decoder that shares no code with either.

THE FOUR SMALLER DEFECTS THE REVIEW NAMED, REPAIRED HERE.
  * `DL-INJ-1 boundsSTATED` is a DANGLING POINTER.  delivery.v3 carried
    boundsSTATED under DL-INJ-1; delivery.v4 moved it to ADM-DOMAIN and one of
    its own prose leaves still points at the old home.  This file does not edit
    the artifact and does not raise a blocker on a document reviewed ACCEPT: it
    RESOLVES intra-document pointers and reports unresolved ones as a named
    measurement, `danglingIntraDocumentPointers`, printed on every run.
  * A malformed committedBytesHex raised an unhandled EncErr traceback out of
    gate_vectors.  Every decode, re-encode and hex parse here is inside a guard
    that converts the exception into a finding NAMING THE VECTOR.
  * gate_derivation's two diagnostics were INVERTED -- they passed the artifact's
    published value as `got` and the checker's expectation as `want`, so the
    message read "recomputed X, artifact publishes X".  Run.eq's argument order
    is (recomputed, published) at every call site here, and gate_derivation is
    the site that was wrong.
  * gate_digest_accountability RE-READ THE SUBJECT FROM DISK after verifying it.
    A checker that re-reads after verifying has a window.  The verified bytes are
    read exactly once, in verify_pins, and are threaded to every gate that needs
    them; nothing below re-opens the subject.

USAGE.  python3 -I -B check-delivery-v5.py [--selftest] [--append-census] [--verbose]
EXIT.    0 = no findings.  1 = findings, each naming its position.  2 = input drift.
"""

import argparse
import copy
import hashlib
import importlib.util
import json
import pathlib
import re
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
COOP = HERE.parent

SUBJECT = "artifacts/delivery.v4.json"

# Hash-verified before any parse.  Exit 2 on any mismatch.  Every digest below
# was produced by `shasum -a 256` on the live file and hard-compared.
PINNED = {
    "artifacts/delivery.v4.json":
        "3cffece076289a4e62f3e0680cb8cc7c6a134b3190a6b39b7ec14b007704a121",
    "artifacts/delivery.v2.json":
        "47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3",
    "artifacts/delivery.v3.json":
        "01f1b95d0c740580c9307c188e4c2f6806f4d2e7e54d458f570631734cb62a6d",
    "artifacts/delivery.v3.review-independent.json":
        "7791ef39abe51b6646df3113353187e6c4b8350ac9299a599ecac780fc077796",
    "artifacts/resolved-inputs.v2.json":
        "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    "artifacts/fact-plane.v1.json":
        "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    "artifacts/c2-plan-stage-schema.v4.json":
        "4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39",
    "artifacts/check-resolved-inputs.py":
        "7ffed1c0e66e345a72c5e0e7feaf332508d0842c1ecdba8572f872997917ffa0",
    "ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md":
        "47df412dba5d62a823ca7c008c382c489b8a10c797fd8656f3d4dd5d6c342e2e",
}

# IMPLEMENTATION-FREEZE.md and IMPLEMENTER-BLUEPRINT.md are NOT pinned.  Section
# 7.7: a whole-file digest of a document under concurrent edit "would manufacture
# a false refusal on an unrelated edit while adding nothing".  The propositions
# the artifact draws from them are verified by gate_quotations instead, with the
# needle taken from the artifact rather than transcribed into this file.
UNPINNED_SOURCES = ("IMPLEMENTATION-FREEZE.md", "IMPLEMENTER-BLUEPRINT.md")

# ---------------------------------------------------------------- statement seals
#
# DOMAIN: derived at runtime by derive_seal_domain() and compared BOTH WAYS.
# CONTENT: sha256 of the NFC UTF-8 bytes of the statement, measured from
# artifacts/delivery.v4.json and hard-compared against shasum -a 256.
#
# These are the only digests in this file that are not recomputed from a recipe,
# and they exist for one reason: the review that rejected the predecessor
# neutralised its whole-file pin by re-pointing PINNED at a scratch copy.  A seal
# keyed by derived path survives that, and a suffix does not survive a seal.
STATEMENT_SEALS = {
    "$.derivedFrom.operations[7].value.recipe":
        "83109758f056c60b7d988dbbd08d003dabfa511e0c26f6b8860e6bbe40be4586",
    "$.derivedFrom.operations[7].value.textForm":
        "52f851fad882359b4da47ab468f04139b0a5bbc846a922f655c5b37cdcfd05de",
    "$.derivedFrom.operations[7].value.oneLine":
        "7b63306ee13b73a7bbde2048285ce460223910b583f04be3ed76cc6ef9f8a397",
    "$.derivedFrom.operations[7].value.normativeDetail":
        "64e5b3348663e2943ef40598c1eaac2b9ec8176b0b507f285e40f7044f744e45",
    "$.derivedFrom.operations[8].value.DL-ORD-1":
        "2de86334d226611aa5dd7762d00635592e6fd9257fbaf58472ac0df966166473",
    "$.derivedFrom.operations[8].value.DL-ORD-2":
        "97ca841fbd912746e48e2ef296fdacc8c151f0a4615b22f8312a53b161dc67dc",
    "$.derivedFrom.operations[8].value.declaredSortKeys.CapabilityManifestV1.providers":
        "6c3e99aafdd9e3d762613577bc40f7ce1912063635c83713ec7cf3be70a938e3",
    "$.derivedFrom.operations[8].value.declaredSortKeys.CapabilityManifestV1.coverageForAbsent":
        "6c3e99aafdd9e3d762613577bc40f7ce1912063635c83713ec7cf3be70a938e3",
    "$.derivedFrom.operations[8].value.declaredSortKeys.ProviderCapability.platformIds":
        "6cb593704aeb62a9006ae56d8656b5b54e94978924e5e46fbd01476b41eb3cb9",
    "$.derivedFrom.operations[8].value.declaredSortKeys.AbsentCapability.relationIds":
        "6cb593704aeb62a9006ae56d8656b5b54e94978924e5e46fbd01476b41eb3cb9",
    "$.derivedFrom.operations[8].value.declaredSortKeys.ProviderCapability.relations":
        "3910e2be84c93bd44c576317367e755ee1dc425eda55af108fcc4cfccb5d58ef",
    "$.derivedFrom.operations[8].value.ifPRECEDENCEISEVERWANTED":
        "d46c7ceb5824610f5464a27054b10c277c7eaaad3bf1bcfc49ad3ef08e08ddce",
    "$.derivedFrom.operations[8].value.rationale":
        "58510775033996bc839fdc14752b344138d44c3fd80c8a8cd7c16b405ffae16c",
    "$.derivedFrom.operations[10].value.DL-CLOSED-1":
        "c3f6a040a53be78461dbf5b149ee91b5bed58beb34ee7a847fbfa1b6684e606f",
    "$.derivedFrom.operations[10].value.DL-INJ-1":
        "972110ade004b97a04de2c0b65721224abf487736c38d171cb3ad010e457648d",
    "$.derivedFrom.operations[10].value.detector":
        "7c1a79d832c4569a70d35cf87740b453abbd1341216dab6acdf48d971760b662",
    "$.derivedFrom.operations[10].value.closedTypesToday[0]":
        "adbd5fe8d02e310dc3754a707fc972201ef0146e091169c0430a1de0cb6e2840",
    "$.derivedFrom.operations[10].value.closedTypesToday[1]":
        "62517d23f6d2a4296e3d003d99fc98487d491474d2a7fe3f8761240f24c8d036",
    "$.derivedFrom.operations[10].value.closedTypesToday[2]":
        "b9aca5b1c18d62c7ebff88ad460eb31d7281b57e3745624e8636d68325ae65ad",
    "$.derivedFrom.operations[10].value.mapTypesToday.ProviderCapability.relations.keyDomain":
        "eebbcfa543fb1a000787bad18505329aeb0f09762d69426f9482170da3b802db",
    "$.derivedFrom.operations[10].value.mapTypesToday.ProviderCapability.relations.valueKind":
        "8d0250b9349b775369b178a2e713870a9ab0b0ebb092ed78cdfec38d85208560",
    "$.derivedFrom.operations[10].value.mapTypesToday.ProviderCapability.relations.measured":
        "da1a4c3841bd55e90784c34f0808d26a05eb2ccde3e8542435a3515e4d152644",
    "$.derivedFrom.operations[10].value.whyTHESECONDSENTENCEEXISTS":
        "80b2bc3049b825f91e97f7524a4a1700ab1fda1e345b0c8e3896ef20509a7c61",
    "$.derivedFrom.operations[10].value.rationale":
        "312dab1e42873f0db48b49cdd615cfc062b5f76bbdc8a7aad33bf381fb0bca8e",
    "$.derivedFrom.operations[11].value.DL-DOM-1":
        "5523e2dc9a7a5b6bee98bd232329eabbbe6a90bdea34be9916ff64d797633c93",
    "$.derivedFrom.operations[11].value.whyTHISISAPROPERTYANDNOTARULEABOUTplatformIds":
        "d9bd1f3283d4f7513fc27cbd0dc76d4543ad8f4df17c4f30fe4cfa907ee9b768",
    "$.derivedFrom.operations[11].value.gateOrder":
        "bd88a4622e827641cb3eaef0e78e855daec122add6390eaa2b79b9f065f91675",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.boundPositions[0]":
        "7fc56378a90426554e13985b4f63a15712995fb3df751e4d00faa2fa8c9539a0",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.members[0]":
        "b2ddf81d0063a34cdff6ca327232a40927785d9d9e03f7356c13f211ea507861",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.members[1]":
        "fb462f62124c93c2a2b38fabdaa8fba94f6c3d0710bba8d9b5bfdc9b0da6e65c",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.members[2]":
        "75d70e27b9826bfc34d360bfb7a8afc37eea7ec70ebbcfbe1688cc236ffc314c",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.members[3]":
        "071f0bf8fc0bbf7e51059fa749cd503ab5d4105d292af6cd023701f0694cd6d6",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.members[4]":
        "0bd537aa510ae6b0d492a94caf0ac27385d8444e1a3bdfffde5a555b28b52b75",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.members[5]":
        "2bcde48d7127a3d80060e30d0c8b8f000fe7d3e2f70f6cc430e1024f16d5417d",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.members[6]":
        "f15580503e99e6eace52371ac13825695a17897828a8f3826762dfef4074ead6",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.members[7]":
        "fb6242019d0903d14d1bfec0203d171afebb6f25804516c5d8f6e62731738e9c",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.source":
        "8bb19a0e9929c56742cfac88f96b0ffafa283828fe8509408c435d9d185e4ae2",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.theAGGREGATETOKENISNOTMINTEDHERE":
        "33c0b10e3a85ac9bb3d8b5ac6a6535bd22895bc32cf8b52fa6c9264d5c6bb403",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.whyBESTEFFORTROWSAREMEMBERS":
        "ad8997d614ca69a62bb2f60f2b750f6da597187ef7a09095588b5063d609483d",
    "$.derivedFrom.operations[11].value.registries.PLATFORM-ID-DOMAIN-V1.theRESIDUALTHISDOESNOTCLOSE":
        "b4516eba1203089da8d82d28080449fa4c5259c4042fda103360f894d259a78a",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.boundPositions[0]":
        "34ca977f4932d11a2ba5a82e45b2f6c1345615637cd31c62bce12751f2d7b9d3",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.boundPositions[1]":
        "4d92ce1053635b92f69365a62ca32b6596473d0478bbfbf1b722ab913cf57aaf",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[0]":
        "f46f5990ebfadcab199107258b9dadd8711bd7946d8d00091a1073effcf2a843",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[1]":
        "4e37ae576f9bb1fa72a861ef472229465dbf4fc14e54d6932878c154716de09f",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[2]":
        "2600da55cfeb8cdc76abc8abbd3ca435671c2fe2d3f43cc3107ce3579aa6955b",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[3]":
        "4a2b77eb1e0301f22d9751a72545bf4b7ce94817da9e2dbec2fd743e3def5d4b",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[4]":
        "3b9c358f36f0a31b6ad3e14f309c7cf198ac9246e8316f9ce543d5b19ac02b80",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[5]":
        "2fcef4b99cb2a5a83c4f2b5ec8fabde6e179be954c383702b7ef6496e0486310",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[6]":
        "829f8d848b44fa3098194754af5b60e2fb1517b0195956841beb6cac9bc68067",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[7]":
        "bc4a71180870f7945155fbb02f4b0a2e3faa2a62d6d31b7039013055ed19869a",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[8]":
        "62f9e3e7d06eb58afd74674f5c10855b2c96580c30650efd5de07e3228b55bd5",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[9]":
        "07a0b0962107485c3c1375cffa0f2ed9254efe640801713a6c4a358af3d8aa00",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[10]":
        "8d8460221bf4eb295f964884b40a9ba6302a9c2af2f9b1997cbed42fda139de8",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.members[11]":
        "f8ca098559098f7ea170332c71d850f8b055c6d644c336c0b980974d5f083078",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.source":
        "87b82a974ac566a76e51c4e5b5c2fd9c61225a0989d7728c4e94de12c62634a9",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry.relations.whatISNEW":
        "fc41bdb5f26bae0dcb3ea309ab56b9639ecb6fe2f8794fb65f60a088d6936b3d",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry ladder rungs.boundPositions[0]":
        "64e320341a5d947cb329555c2276f4b4b96a08a25512eda8675853715b59d1a8",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry ladder rungs.rule":
        "adf9e78e73d7dd29904c6f8686cae99d8772e77eb402e615d02d94d9853c1fb9",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#relationRegistry ladder rungs.measured":
        "e0efdfd6f867c19030be25c15bda1d763708d5c935216fd57a21e5745ec9c56e",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#deficiencyVocabulary.boundPositions[0]":
        "6412c3e979b7a59e90e5bf2dbcbc82206ee232f0d4b0e7c5061b8b8e3978fab7",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#deficiencyVocabulary.members[0]":
        "940a6bb32ea4b02ea1c3516954d0938c539a3755020a4da150f4912a48dde12c",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#deficiencyVocabulary.members[1]":
        "57d68f696273afd8b87c346a6c5a115fe2459ea0a500e0781d4391ba430f5846",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#deficiencyVocabulary.members[2]":
        "18632fc2cbe5dd715f0e48e9fb12a17a05cf00219a6bcbf53a33c3f886216e53",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#deficiencyVocabulary.members[3]":
        "0b48cfd27b4614b4e8cbef23ac7480faa3066e70d06a16f7e30670c97a888e61",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#deficiencyVocabulary.members[4]":
        "e33265a36054aa35fa8ef033c7907a8a9e22207107ada72052806a509b079825",
    "$.derivedFrom.operations[11].value.registries.fact-plane.v1#deficiencyVocabulary.whatISNEW":
        "6b2a0cc8451fb0495b17035ef58564b5b8de6c461b5319610701e940dc75ed78",
    "$.derivedFrom.operations[11].value.registries.the literal 'unavailable'.boundPositions[0]":
        "21b042e4e72d2a2fd124f4667723c19e23501aa296f44dfafbc26cab5055dec2",
    "$.derivedFrom.operations[11].value.registries.the literal 'unavailable'.members[0]":
        "ba691ba042bcedd9a61a36f5969026bc95859dccdc7e47f24e6bce35673baf2f",
    "$.derivedFrom.operations[11].value.registries.the literal 'unavailable'.source":
        "78c68e4e6c84469470b480ff459b0e75ef92a3d31200c28230ba4de52ac0eef8",
    "$.derivedFrom.operations[11].value.declaredOPEN.CapabilityManifestV1.schemaVersion":
        "01f8dad14dcba477fb8350c48e2b669c8e5896173b4c6da1e72cb9e6f31efe0e",
    "$.derivedFrom.operations[11].value.declaredOPEN.CapabilityManifestV1.profile":
        "dd25c01cb757d183003a9246adbb604613a6047de8cc802b9933675d0d9c12e2",
    "$.derivedFrom.operations[11].value.declaredOPEN.ProviderCapability.providerId":
        "87f0c2aa9b0e7a5a047c7dac26b16937828b97503cc215231610a1cf6e93bf3a",
    "$.derivedFrom.operations[11].value.declaredOPEN.ProviderCapability.language":
        "2063ecd628a852fb024303e8411ae5bb2b08743cd71fefd0d622630995ffbdde",
    "$.derivedFrom.operations[11].value.declaredOPEN.ProviderCapability.providerVersionSource":
        "493964b22248ad57c91e2308e23c6460cfd01165af00c51a0f42d8578b75d7bd",
    "$.derivedFrom.operations[11].value.declaredOPEN.ProviderCapability.toolchainIdentitySource":
        "493964b22248ad57c91e2308e23c6460cfd01165af00c51a0f42d8578b75d7bd",
    "$.derivedFrom.operations[11].value.declaredOPEN.AbsentCapability.providerId":
        "c02ff1da686059cad47a3d7b76b2b2c2ce817f215a2abccc48cf95d409b2b5a8",
    "$.derivedFrom.operations[11].value.declaredOPEN.AbsentCapability.language":
        "493964b22248ad57c91e2308e23c6460cfd01165af00c51a0f42d8578b75d7bd",
    "$.derivedFrom.operations[11].value.censusIsEXHAUSTIVE":
        "a86edee09d68ece6052e8fccd3cda9bb067883e1b1af25a1b8e59a06da675343",
    "$.derivedFrom.operations[11].value.whatREMAINSOPENISTHEHONESTPART":
        "3696dad76a5711c264cb62c68f419d6e1cd86500c7554f5fca326738b22d24ef",
    "$.derivedFrom.operations[17].value.textForm.form":
        "a2eb9080492c083af375ea01ea3eb972bf80fd7273af9be227c53a5aa1f0a335",
    "$.derivedFrom.operations[17].value.textForm.regex":
        "52f851fad882359b4da47ab468f04139b0a5bbc846a922f655c5b37cdcfd05de",
    "$.derivedFrom.operations[17].value.textForm.whyBareHexAndNotSha256Colon":
        "81bdac6b4edf100c7bb041d2b407d1aacc847acab97a281955c307fa86a6a916",
    "$.derivedFrom.operations[17].value.textForm.truncation":
        "5f23cc3b0e273bbdcf76442b7d3b04e01c65e49174ff89f71e77915485ae476b",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.whatIsMINTEDHERE":
        "22db7ce7f4ca9259888e9b218ba5373907716f564b96eb0a3b41f79f5521347e",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.closedDomainVocabulary.owner":
        "9f4029f12dbccd50d4293af18ba904990dc089ebf8ce9e248d44c89208e7acac",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.closedDomainVocabulary.family":
        "d332b1e7b6d4fc700256b7f212ed6a52043278153e2e93526dec1055e4a0df89",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.closedDomainVocabulary.members[0]":
        "6a30f19a8ca74ebe74cafd1fe34b19f2f3818af629bdedfb882a837277de06bf",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.closedDomainVocabulary.extensionRule":
        "f205c6cc6869d1c313d05122de057486909a5b0b1e3aa78b18b2047097f218c3",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.separatorMechanism.bytes":
        "a7a1dc06f016a82c7fcbe4c4f59310061c74e695bc8abf79030c4b3e991baf2c",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.separatorMechanism.whyItIsNOTMinted":
        "55759c8d1714f66eb4a849e0cbaffed3711b31769e86ff3e904b44543d747186",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.separatorMechanism.whyAPREFIXISSAFEHERE":
        "3c1595d6e3f39b17881ad824a5cdd6909a222548c026b8fa79be468d1c5bcb86",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.separatorMechanism.whyNOTALENGTHFRAMEDCOMPONENT":
        "efa713b654c3871618542d5920fb2472320da3069ebbcdc4cefcb62e9b7603bc",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.whyTheLABELISSPELLEDTHISWAY":
        "bbe275487053a74e0020dc4246fb1db42d0ab93bf39adbd96d15b3d0cc11cf3f",
    "$.derivedFrom.operations[17].value.namespaceAndDomainSeparator.whatThisDoesNOTTouch":
        "d3073bfc631ac94c6f1c62efd2d1ca8e88e2ab482491ef440faf110083e07fca",
    "$.derivedFrom.operations[17].value.recipe.step1_ADMIT":
        "cdfe94917e2931a2f982afc8eb056dc023235f8ef2aa626ab9fcbc1196bb332b",
    "$.derivedFrom.operations[17].value.recipe.step2_COMMITTEDBYTES":
        "60888dda9472043a436c5f05a87b98d75ad98d61324e606de9eb1163504d14f9",
    "$.derivedFrom.operations[17].value.recipe.step3_DIGEST":
        "6ea9eb02618eddf3c81934d6ec6174bd4a64795293f1a543b908a6f8596e80b9",
    "$.derivedFrom.operations[17].value.recipe.oneLine":
        "3fceb095a0665584928f5c264de56a0de8fca64dfbcfc7e46926f9d6ba5f57e3",
    "$.derivedFrom.operations[17].value.recipe.whoComputesIt":
        "0995aba2d984139541d895485cb9aee0d616c5f0f02f3a4201da1fb38fc87975",
    "$.derivedFrom.operations[17].value.recipe.whoRECOMPUTESIt":
        "1b8756c939a966815f623f2969a9f9823b50f35d2bbb44b0aae0406c219b5bfe",
    "$.derivedFrom.operations[17].value.recipe.stability":
        "4d8052c17f98b78eec63ed1c25006dffa47e6825688dd9813302e0c12ac46980",
    "$.derivedFrom.operations[17].value.recordShape.note":
        "1a52d19b753ca018c668cde0cce5420a360a7b8fd7e505e212022b907e8c54a6",
    "$.derivedFrom.operations[17].value.recordShape.CapabilityManifestV1.kind":
        "1092e2e43a486c0a247743940abb3210d77c912476ac72e4c854ae4f13383125",
    "$.derivedFrom.operations[17].value.recordShape.CapabilityManifestV1.requiredKeys[0]":
        "ff63b0467d555ea1b674b981a393aa821c9840ba1068a48d8e0793b398534726",
    "$.derivedFrom.operations[17].value.recordShape.CapabilityManifestV1.requiredKeys[1]":
        "1900eab6c028483d7126599ee6f50de0d27907b5c65fa90524580b4b0f9852b0",
    "$.derivedFrom.operations[17].value.recordShape.CapabilityManifestV1.requiredKeys[2]":
        "1e19bab29bc6432a45375515ae332f5fc9540db0100ac0b05c3ccb42923c189d",
    "$.derivedFrom.operations[17].value.recordShape.CapabilityManifestV1.requiredKeys[3]":
        "05facee46596e3b55f3656d3167b6b8283b7c737f92a776d719110090ceef349",
    "$.derivedFrom.operations[17].value.recordShape.CapabilityManifestV1.source":
        "b5ab47db4ba7955a4d79dc06e7972266d317b7374f4369abed5854be8a2557a8",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.kind":
        "1092e2e43a486c0a247743940abb3210d77c912476ac72e4c854ae4f13383125",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.requiredKeys[0]":
        "4b382d9376fccfeb2e676bef3b1ff80e0259d35bf4fc48eb81c190f98b7ee487",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.requiredKeys[1]":
        "a4ef304ba42a200bafd78b046e0869af9183f6eee5524aead5dcb3a5ab5f8f3f",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.requiredKeys[2]":
        "7dfc8f05e4683deb3f82bd8677125d28b3f01e3a3480ce3c4fc863fafed1feb6",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.requiredKeys[3]":
        "2ae2202b1e927245d19f8f45e42b29647b5db575f9463a2a2d62a4fe10bddbc5",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.requiredKeys[4]":
        "e2ba41af03120f143f51748f319f1e7a0e647f1bac9c27d63eef38f856f9987e",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.requiredKeys[5]":
        "f15135d4c7f6cb53b1ceb836444212838b439bcc123c4141dedc40c12f16aacc",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.source":
        "67ca39614fdf52988b6789c339e94f0278094f493dfa12516e380a1cd5df64d1",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.closedIsNEW":
        "cb8385f430910c05296e3ca21091423c3d7daf7748b2e71894f94eba0d0b5037",
    "$.derivedFrom.operations[17].value.recordShape.AbsentCapability.kind":
        "1092e2e43a486c0a247743940abb3210d77c912476ac72e4c854ae4f13383125",
    "$.derivedFrom.operations[17].value.recordShape.AbsentCapability.requiredKeys[0]":
        "4b382d9376fccfeb2e676bef3b1ff80e0259d35bf4fc48eb81c190f98b7ee487",
    "$.derivedFrom.operations[17].value.recordShape.AbsentCapability.requiredKeys[1]":
        "a4ef304ba42a200bafd78b046e0869af9183f6eee5524aead5dcb3a5ab5f8f3f",
    "$.derivedFrom.operations[17].value.recordShape.AbsentCapability.requiredKeys[2]":
        "5bda40b481fa0fc25986925dc5eb10736be8303430dbc59a18405667808c57ae",
    "$.derivedFrom.operations[17].value.recordShape.AbsentCapability.requiredKeys[3]":
        "84e3abd41e2fd4f474e2df9bf4f53343e3cb180f30f4eab4a57a9ed2822d2282",
    "$.derivedFrom.operations[17].value.recordShape.AbsentCapability.requiredKeys[4]":
        "db5d7a5252dd6e796da85646fcbc22e72dce683ea73bb0dd64249c1c47ab44c6",
    "$.derivedFrom.operations[17].value.recordShape.AbsentCapability.source":
        "a95b2488d1c32f8b5d357eee8d657364c6984b36d10058e7e02ef6428f6a8ca8",
    "$.derivedFrom.operations[17].value.recordShape.AbsentCapability.closedIsNEW":
        "59a7bd311dcb0a52f1efc3b191d175c3c69771c2f60d156649f7624527b7b7a5",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.relations.kind":
        "4cf644d78bfc298f26ba4c170c7a1c04c3d1388e09fdd02534f23433a9a8f227",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.relations.shape":
        "0c251a0ad133c163d0edd79db7fda5f995baf118bb5806a656626db161bb846a",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.relations.keyDomain":
        "0f9ad0b282c440c2e31740110a122a6d3eff8adf082bf73788edd2ee1689caa5",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.relations.valueKind":
        "d7dfbaf6df0a816fd85178599a48c11ff875288715c08377c6beb5d67e5fa8d5",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.relations.whyClosedIsFALSEANDNOTMISSING":
        "ff8ec84643f1050dd9c05f10f849cf5253109724cb4e03a0947606787b594d04",
    "$.derivedFrom.operations[17].value.recordShape.ProviderCapability.relations.order":
        "99bd1936c027f3649b4c22e70041612d9a95d710038e25faa335f5a77fa3e15c",
    "$.derivedFrom.operations[17].value.recordShape.everyReachableObjectTypeIsCLASSIFIED":
        "7ebd4fcf34aa438bbcaf741bdf491fe028e9cbd1713ac6ce152b9fce7b188973",
    "$.derivedFrom.operations[17].value.orderingRuling.id":
        "a0590460a0a2b5b53639de1efe57067beacaf252be01b7ae26b8c4eea667adb6",
    "$.derivedFrom.operations[17].value.orderingRuling.standing":
        "fd17196a43c48e2493532e20bd4ab2cb5ea1cef3eb00b04a722a4a07d2fd4c0c",
    "$.derivedFrom.operations[17].value.orderingRuling.theQuestionAsPosed":
        "480daae2f6be0f72fdd27d3540e0b790e32cd666be17b40c7c2bb948cfbdcd2f",
    "$.derivedFrom.operations[17].value.orderingRuling.whereTheRuleComesFrom.statement":
        "c9c63f5020d1e6d3fe0b275bc559ff599a12b907360e55bfeed3a019bbca6887",
    "$.derivedFrom.operations[17].value.orderingRuling.whereTheRuleComesFrom.leg1_theEncodingItselfSaysSO":
        "61b1c86f59bfbfba5af751552f475a81b9798c990769d41b786a492aacbec544",
    "$.derivedFrom.operations[17].value.orderingRuling.whereTheRuleComesFrom.leg2_theSAMESURFACEDOESITFORTHEANALOGOUSFIELD":
        "9b56565251e771fbcddc5d0cac4919a20e672d37ff195d90754b3cda27ec08ea",
    "$.derivedFrom.operations[17].value.orderingRuling.whereTheRuleComesFrom.leg3_theOTHERCANDIDATEENCODINGSAYSTHESAME":
        "e090d30a2cbefd7ed9f265451ee02ed36f8728ae2961b67aa1046b9aa2b4a66b",
    "$.derivedFrom.operations[17].value.orderingRuling.whereTheRuleComesFrom.leg4_theCORPUSFORBIDSANUNDECLAREDEMISSIONORDERFROMENTERINGPlanId.theGROUND":
        "7a235e52cf7f8506bcbb1903ae5ed1837f4980b01943c56ad8dacd52aaf122ab",
    "$.derivedFrom.operations[17].value.orderingRuling.whereTheRuleComesFrom.leg4_theCORPUSFORBIDSANUNDECLAREDEMISSIONORDERFROMENTERINGPlanId.theENTAILMENT":
        "180ffaad576926c2221d1602e77c1437f5a1105d27fde67b0ad8e7a05beca579",
    "$.derivedFrom.operations[17].value.orderingRuling.whereTheRuleComesFrom.leg4_theCORPUSFORBIDSANUNDECLAREDEMISSIONORDERFROMENTERINGPlanId.whyTHISGROUNDANDNOTTHEONEDELIVERYV3USED":
        "75a2879d5501c08e22d7f55c18d18bff1afab7e76efb78d94d86a44368f6c410",
    "$.derivedFrom.operations[17].value.orderingRuling.whereTheRuleComesFrom.leg4_theCORPUSFORBIDSANUNDECLAREDEMISSIONORDERFROMENTERINGPlanId.andWHATBECOMESOFTHEOLDLEG":
        "00e253a238554637698c745db5e9392449f4bb38e04a39f258a7991da976edbe",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[0].field":
        "61a3b56e87121fb3363e30d0914def45cfa6c4f4d6c1df2f1faa768924763c70",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[0].ruling":
        "b4f5ff9c31e6b9c9895bdf30438921bbb94d67f9ef060cb46af8a10f9d69b0a9",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[0].rationale":
        "fc72ce27e923ec377cbe4940bf34bc3f068d10f2d98594a7640b738091ca825c",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[0].measuredSupport":
        "0719aea9b8fa60800cfb54fd467e73acda48aff3804a3a0d21ee17931a06a408",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[1].field":
        "b0cb680d380a845da7b0124711b2c66cd2532e61b57ed994b4602c74267cc4d0",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[1].ruling":
        "a7a031f1d65234f2f7de19fb5d153cc9797bfd81332c998589f7a2e38eb8e579",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[1].rationale":
        "e45bfd15ddcc21720df862a04520a08c19a6a70b77c24b0fae102ec4129e45b8",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[1].measuredSupport":
        "b63734352456bbe2fc678b4e15471e7a527ce8cec1db7b7900282b6946aa6430",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[1].residualStatedNOTDECIDED":
        "0a04a8b4c008298675eae9a142f1c9badcf0dad0c3290787388a231bc5f842cf",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[2].field":
        "92144301b57a86aa3640a3210f1de95c51798ba6e3c984f87ee71191ebe5432b",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[2].ruling":
        "c38c5aafbf4805af8b2694feb295e5721f87701e11f731e2c2c1ae8be7050a40",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[2].rationale":
        "977ea737f53ac834ff69142e56c4016293e58e645d0ff7c382ac425cd6050b13",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[2].note":
        "b3b64be980e5eff7c63f5afc30310b6b2b300d53c3a0969f81ad783a2862b659",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[3].field":
        "a2e27c8ad8d053f737f6358d09b0306b2b02df572121e2ba8ba973a90ecccd1b",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[3].ruling":
        "88e60ddeccffc614486030a7f1686d38ba6c6181b3539dbd863b8ed148c9f690",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[3].rationale":
        "7f96c06660c1cf8be115e75e0794e3e7f780bd622d7e98d7085a08bdb9141039",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[3].note":
        "b28cccb4eba95c0a43e4654207711a5a7564ffd2df3686bc383752b603a9f7ad",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[4].field":
        "fe2198c1e5cf7b6405416a11ef5f76cf46a23f15c503833b1b589fd04199a439",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[4].ruling":
        "e008acafb22b422f931fc2858d7d9be11b7aac3433e270373b5fe20a1bbd4df5",
    "$.derivedFrom.operations[17].value.orderingRuling.perFieldRuling[4].rationale":
        "38735e50beb3a48a9cb438d39f5260522e96a63c50a81ba1b676db271d60642c",
    "$.derivedFrom.operations[17].value.orderingRuling.theRULEISAPROPERTYNOTALIST.statement":
        "36e083d118af9228c41bc143ff4c7b6face4fa9deaed857a22858913602a96f1",
    "$.derivedFrom.operations[17].value.orderingRuling.theRULEISAPROPERTYNOTALIST.whyAPROPERTYANDNOTFOURROWS":
        "30db1a33268c7add98966186a76740751f76177160a1501ef8354f283f9bd7d7",
    "$.derivedFrom.operations[17].value.orderingRuling.theRULEISAPROPERTYNOTALIST.theEXEMPTIONMECHANISM":
        "6ebaaebe23274c6735c22daa474133cdb61c6966775d69eeae7424c80a33bcd7",
    "$.derivedFrom.operations[17].value.orderingRuling.theProductQuestionThisDoesNOTDecide.question":
        "be5cb03066fd5331a83d8451a76b605dcdf04615256b1a62d66c693d408c7271",
    "$.derivedFrom.operations[17].value.orderingRuling.theProductQuestionThisDoesNOTDecide.disposition":
        "dda606681ba02c8849c1ebdf053924fbb574148f7f009a0c9705a52ef9d423fa",
    "$.derivedFrom.operations[17].value.orderingRuling.theProductQuestionThisDoesNOTDecide.theASYMMETRYTHATDECIDESIT":
        "3352f19970b5c63e4500f55c2a0c35bde47d1091bb475d20293da9940a0b4d02",
    "$.derivedFrom.operations[17].value.orderingRuling.whatIRULEDAGAINST_ANDWHATITWOULDHAVECOST.rejectedReading":
        "4fc6da1a8f7d4dbe58cdf070b3319424489d90166df9abbe3101d8df9fc01489",
    "$.derivedFrom.operations[17].value.orderingRuling.whatIRULEDAGAINST_ANDWHATITWOULDHAVECOST.itIsNOTABSURD":
        "69c761c729d02ab8c00cf50be907520800d008350215465af24a32a0bac79ad0",
    "$.derivedFrom.operations[17].value.orderingRuling.whatIRULEDAGAINST_ANDWHATITWOULDHAVECOST.whatItWouldCost":
        "c0ec58f625423b0ffc91f4eade7c2ce2d5cb4f73e0f0f53c9dee6342588e744b",
    "$.derivedFrom.operations[17].value.orderingRuling.whatIRULEDAGAINST_ANDWHATITWOULDHAVECOST.andTHEMEASUREMENTTHATMAKESITDANGEROUS":
        "3367a383a9b34099a390b16882b51fd4e0436de8ba7d3cb34dabc653d747bf0e",
    "$.derivedFrom.operations[17].value.admission.rule":
        "fe85ca6966655bcc208a5c7a9dfd37f10fa3a1e43276423e4aa1ba9903b18c8f",
    "$.derivedFrom.operations[17].value.admission.gateOrder[0]":
        "72ed7945b893d567a7d7cadbeeb069e0416d5d1a64ba8046e4200e22eb3759d8",
    "$.derivedFrom.operations[17].value.admission.gateOrder[1]":
        "bff832e8be520d5ae4a43af16181a3cce261e7f421ce653035cca3016283a55e",
    "$.derivedFrom.operations[17].value.admission.gateOrder[2]":
        "d5e7b316659e438db7607e8c6df96afbc42ee4086da9abb8e6e3e10f1cf4740c",
    "$.derivedFrom.operations[17].value.admission.gateOrder[3]":
        "8c96a5b99c235987d01eeaffb1aba65be4878e2f2b97454a69273014094a2162",
    "$.derivedFrom.operations[17].value.admission.traversalOrder":
        "a5d58eeba681781858218cd3f2588717dd257497e5304f63fe126cfe1c383b24",
    "$.derivedFrom.operations[17].value.admission.ADM-TYPE.statement":
        "facbad0fec533b3775f00934583b1c6e2b0fa5c529a6d2a694bc096d2a49b46b",
    "$.derivedFrom.operations[17].value.admission.ADM-TYPE.source":
        "f25085bebc20d342439753413f78da2d489dcb4040eb6c7079206dfe4f0def68",
    "$.derivedFrom.operations[17].value.admission.ADM-TYPE.andITISENFORCEDBYARETAINEDCHECKER":
        "19d03c2ce547bf30c784e02e80d485412a26c76b9d4d92e8818c1994edca5e20",
    "$.derivedFrom.operations[17].value.admission.ADM-TYPE.whatITCANNOTDO":
        "e6934fce8f1ed5a4ff13bb934b7aff78065777fa89fc442d07ac0de9a5db45bb",
    "$.derivedFrom.operations[17].value.admission.ADM-CLOSED.statement":
        "c3f6a040a53be78461dbf5b149ee91b5bed58beb34ee7a847fbfa1b6684e606f",
    "$.derivedFrom.operations[17].value.admission.ADM-CLOSED.whyITMATTERSUNDERCVE1":
        "a33f0c9917fe069423f835553a364d0668aec09c9480627ea2685b915e0b0edf",
    "$.derivedFrom.operations[17].value.admission.ADM-CLOSED.changeFromThePredecessor":
        "2ca6ffb2d64b64913042ba85139094b2bb13d1ad0e18fa9f3c55efa8e33c4692",
    "$.derivedFrom.operations[17].value.admission.ADM-CLOSED.changeFromTheREJECTEDCANDIDATE":
        "801edcc1c67aae6d5c56fc8edd4f50b90c9228155861473e502f09151d6840b0",
    "$.derivedFrom.operations[17].value.admission.ADM-DOMAIN.statement":
        "5523e2dc9a7a5b6bee98bd232329eabbbe6a90bdea34be9916ff64d797633c93",
    "$.derivedFrom.operations[17].value.admission.ADM-DOMAIN.whyITISANEWGATEANDNOTACLAUSEOFADMCLOSED":
        "75d7c21bff70e1f645ac087a8d8df477fbdd545583e9c85cf367fbb3e5182d52",
    "$.derivedFrom.operations[17].value.admission.ADM-DOMAIN.executed[0]":
        "e64d7ee7dd31e3f57c41f8aa34fae26333a1eefdd6bac7c83cf76165c55b07de",
    "$.derivedFrom.operations[17].value.admission.ADM-DOMAIN.executed[1]":
        "6397533e52d72be8b51d7155f67d15fbb1af029bd748b209e58e17cfd121014a",
    "$.derivedFrom.operations[17].value.admission.ADM-DOMAIN.executed[2]":
        "d8fec9d3478288054225a75d4700989408e6210f3c46f6c01c06d93e9216c67c",
    "$.derivedFrom.operations[17].value.admission.ADM-DOMAIN.executed[3]":
        "8c6d10256a7751aff720c608990cce5528b5890ccf722af97d0c441b1e29e0f8",
    "$.derivedFrom.operations[17].value.admission.ADM-DOMAIN.boundsSTATED":
        "1c6ed23461e2d728bae5768099727698d2a860a96869802fc7574852c0c8500a",
    "$.derivedFrom.operations[17].value.admission.ADM-ORDER.statement":
        "d8d3c62db27bb2dff408d2ac7101047d758cdbd89a246953048ab8eb27d845c9",
    "$.derivedFrom.operations[17].value.admission.ADM-ORDER.theSTRUCTURALPROPERTYTHISBUYS":
        "6cd2bc123a7827de80a223bf11e6f9fad1eb1795c8b1c9bc56f295ec53846c5d",
    "$.derivedFrom.operations[17].value.admission.ADM-ORDER.theWORDINGOFCLAUSEcISNARROWERTHANITSPREDECESSORS":
        "c7e77e7792d9d4695d8366f10a9d067c31d64a5b07d9f9ce866fec1b3d6461ca",
    "$.derivedFrom.operations[17].value.admission.ADM-ORDER.whyREJECTANDNOTNORMALISE":
        "a8f71cbb6e170929d794266149a8f760caf0ef6fb055de0ce2d440c97e9d0dc9",
    "$.derivedFrom.operations[17].value.admission.ADM-ORDER.whereCANONICALISATIONISALLOWED":
        "4bde2dcf3962fee195b6db3ca773669d2b62d44a6a94fb19053541589f91a16e",
    "$.derivedFrom.operations[17].value.admission.ADM-ORDER.andTHISISWHYTHELIVEFIXTURESAREINADMISSIBLE":
        "9d4d2ac5a1ae1f4f0b36e31a181351018564ab09bae695d462a97d1338d0127a",
    "$.derivedFrom.operations[17].value.admission.whatADMISSIONDOESNOTCOVER":
        "2bc98b7c6819868a952b92b1e4b6bb9b0a048d3234eb40a38c63190b9c3bbf8e",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.DL-INJ-1":
        "98392e2d583af46d8e60276726884d0ba9def02e9d0e5a4ba5345ba709442a05",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.theTHREEINSTANCESKNOWNTODAY[0]":
        "a2d7405593c7bfb7f18f06e162b3f293f8dc3d21d4c38b147b182155c94ef882",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.theTHREEINSTANCESKNOWNTODAY[1]":
        "6d7313d7341c437063badaf3267c4e1d76a9af100e17d53deda581015df9a693",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.theTHREEINSTANCESKNOWNTODAY[2]":
        "aff4fed47ea46bd8c0b97e8bdc9363238f618bb2e76a6e180d621a911939377e",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.andTHEDETECTORISONETEST":
        "3a46cb7791d2469989180b8c00ec06be3a7eea2062b838d18f68572c7f5deedf",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.andITDOESNOTFINDTHETHIRDONE.statement":
        "e3af486131ed307af1a3bd8a7d2508b27a2f77e48b5014d84fbacb53b8641587",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.andITDOESNOTFINDTHETHIRDONE.measured":
        "1e0a516556f36f95aa7db46c8ae46797eb2350e81b86cfb9e3801e35c9a2cf1c",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.andITDOESNOTFINDTHETHIRDONE.theOVERCLAIMTHISREPLACES":
        "eb941b5eb1942de9209066690c7b20e2f807449c3b47441a14832a66555b991f",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.andITDOESNOTFINDTHETHIRDONE.andTHEREFOREWHATTHECLAIMNOWIS":
        "5e1913da3f52bed15bfdeb34087e04ce7e74c8ec0c62dc62c2b2da463919a791",
    "$.derivedFrom.operations[17].value.admission.DL-INJ-1.measuredHere":
        "49194f71c735e886922c4998c40db3cc28ae5fa2bd7c4fc50b6133477479ee44",
    "$.derivedFrom.operations[17].value.valueDomains.DL-DOM-1":
        "5523e2dc9a7a5b6bee98bd232329eabbbe6a90bdea34be9916ff64d797633c93",
    "$.derivedFrom.operations[17].value.valueDomains.whyTHISISAPROPERTYANDNOTARULEABOUTplatformIds":
        "d9bd1f3283d4f7513fc27cbd0dc76d4543ad8f4df17c4f30fe4cfa907ee9b768",
    "$.derivedFrom.operations[17].value.valueDomains.gateOrder":
        "bd88a4622e827641cb3eaef0e78e855daec122add6390eaa2b79b9f065f91675",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.boundPositions[0]":
        "7fc56378a90426554e13985b4f63a15712995fb3df751e4d00faa2fa8c9539a0",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.members[0]":
        "b2ddf81d0063a34cdff6ca327232a40927785d9d9e03f7356c13f211ea507861",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.members[1]":
        "fb462f62124c93c2a2b38fabdaa8fba94f6c3d0710bba8d9b5bfdc9b0da6e65c",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.members[2]":
        "75d70e27b9826bfc34d360bfb7a8afc37eea7ec70ebbcfbe1688cc236ffc314c",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.members[3]":
        "071f0bf8fc0bbf7e51059fa749cd503ab5d4105d292af6cd023701f0694cd6d6",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.members[4]":
        "0bd537aa510ae6b0d492a94caf0ac27385d8444e1a3bdfffde5a555b28b52b75",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.members[5]":
        "2bcde48d7127a3d80060e30d0c8b8f000fe7d3e2f70f6cc430e1024f16d5417d",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.members[6]":
        "f15580503e99e6eace52371ac13825695a17897828a8f3826762dfef4074ead6",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.members[7]":
        "fb6242019d0903d14d1bfec0203d171afebb6f25804516c5d8f6e62731738e9c",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.source":
        "8bb19a0e9929c56742cfac88f96b0ffafa283828fe8509408c435d9d185e4ae2",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.theAGGREGATETOKENISNOTMINTEDHERE":
        "33c0b10e3a85ac9bb3d8b5ac6a6535bd22895bc32cf8b52fa6c9264d5c6bb403",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.whyBESTEFFORTROWSAREMEMBERS":
        "ad8997d614ca69a62bb2f60f2b750f6da597187ef7a09095588b5063d609483d",
    "$.derivedFrom.operations[17].value.valueDomains.registries.PLATFORM-ID-DOMAIN-V1.theRESIDUALTHISDOESNOTCLOSE":
        "b4516eba1203089da8d82d28080449fa4c5259c4042fda103360f894d259a78a",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.boundPositions[0]":
        "34ca977f4932d11a2ba5a82e45b2f6c1345615637cd31c62bce12751f2d7b9d3",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.boundPositions[1]":
        "4d92ce1053635b92f69365a62ca32b6596473d0478bbfbf1b722ab913cf57aaf",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[0]":
        "f46f5990ebfadcab199107258b9dadd8711bd7946d8d00091a1073effcf2a843",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[1]":
        "4e37ae576f9bb1fa72a861ef472229465dbf4fc14e54d6932878c154716de09f",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[2]":
        "2600da55cfeb8cdc76abc8abbd3ca435671c2fe2d3f43cc3107ce3579aa6955b",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[3]":
        "4a2b77eb1e0301f22d9751a72545bf4b7ce94817da9e2dbec2fd743e3def5d4b",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[4]":
        "3b9c358f36f0a31b6ad3e14f309c7cf198ac9246e8316f9ce543d5b19ac02b80",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[5]":
        "2fcef4b99cb2a5a83c4f2b5ec8fabde6e179be954c383702b7ef6496e0486310",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[6]":
        "829f8d848b44fa3098194754af5b60e2fb1517b0195956841beb6cac9bc68067",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[7]":
        "bc4a71180870f7945155fbb02f4b0a2e3faa2a62d6d31b7039013055ed19869a",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[8]":
        "62f9e3e7d06eb58afd74674f5c10855b2c96580c30650efd5de07e3228b55bd5",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[9]":
        "07a0b0962107485c3c1375cffa0f2ed9254efe640801713a6c4a358af3d8aa00",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[10]":
        "8d8460221bf4eb295f964884b40a9ba6302a9c2af2f9b1997cbed42fda139de8",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.members[11]":
        "f8ca098559098f7ea170332c71d850f8b055c6d644c336c0b980974d5f083078",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.source":
        "87b82a974ac566a76e51c4e5b5c2fd9c61225a0989d7728c4e94de12c62634a9",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry.relations.whatISNEW":
        "fc41bdb5f26bae0dcb3ea309ab56b9639ecb6fe2f8794fb65f60a088d6936b3d",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry ladder rungs.boundPositions[0]":
        "64e320341a5d947cb329555c2276f4b4b96a08a25512eda8675853715b59d1a8",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry ladder rungs.rule":
        "adf9e78e73d7dd29904c6f8686cae99d8772e77eb402e615d02d94d9853c1fb9",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#relationRegistry ladder rungs.measured":
        "e0efdfd6f867c19030be25c15bda1d763708d5c935216fd57a21e5745ec9c56e",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#deficiencyVocabulary.boundPositions[0]":
        "6412c3e979b7a59e90e5bf2dbcbc82206ee232f0d4b0e7c5061b8b8e3978fab7",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#deficiencyVocabulary.members[0]":
        "940a6bb32ea4b02ea1c3516954d0938c539a3755020a4da150f4912a48dde12c",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#deficiencyVocabulary.members[1]":
        "57d68f696273afd8b87c346a6c5a115fe2459ea0a500e0781d4391ba430f5846",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#deficiencyVocabulary.members[2]":
        "18632fc2cbe5dd715f0e48e9fb12a17a05cf00219a6bcbf53a33c3f886216e53",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#deficiencyVocabulary.members[3]":
        "0b48cfd27b4614b4e8cbef23ac7480faa3066e70d06a16f7e30670c97a888e61",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#deficiencyVocabulary.members[4]":
        "e33265a36054aa35fa8ef033c7907a8a9e22207107ada72052806a509b079825",
    "$.derivedFrom.operations[17].value.valueDomains.registries.fact-plane.v1#deficiencyVocabulary.whatISNEW":
        "6b2a0cc8451fb0495b17035ef58564b5b8de6c461b5319610701e940dc75ed78",
    "$.derivedFrom.operations[17].value.valueDomains.registries.the literal 'unavailable'.boundPositions[0]":
        "21b042e4e72d2a2fd124f4667723c19e23501aa296f44dfafbc26cab5055dec2",
    "$.derivedFrom.operations[17].value.valueDomains.registries.the literal 'unavailable'.members[0]":
        "ba691ba042bcedd9a61a36f5969026bc95859dccdc7e47f24e6bce35673baf2f",
    "$.derivedFrom.operations[17].value.valueDomains.registries.the literal 'unavailable'.source":
        "78c68e4e6c84469470b480ff459b0e75ef92a3d31200c28230ba4de52ac0eef8",
    "$.derivedFrom.operations[17].value.valueDomains.declaredOPEN.CapabilityManifestV1.schemaVersion":
        "01f8dad14dcba477fb8350c48e2b669c8e5896173b4c6da1e72cb9e6f31efe0e",
    "$.derivedFrom.operations[17].value.valueDomains.declaredOPEN.CapabilityManifestV1.profile":
        "dd25c01cb757d183003a9246adbb604613a6047de8cc802b9933675d0d9c12e2",
    "$.derivedFrom.operations[17].value.valueDomains.declaredOPEN.ProviderCapability.providerId":
        "87f0c2aa9b0e7a5a047c7dac26b16937828b97503cc215231610a1cf6e93bf3a",
    "$.derivedFrom.operations[17].value.valueDomains.declaredOPEN.ProviderCapability.language":
        "2063ecd628a852fb024303e8411ae5bb2b08743cd71fefd0d622630995ffbdde",
    "$.derivedFrom.operations[17].value.valueDomains.declaredOPEN.ProviderCapability.providerVersionSource":
        "493964b22248ad57c91e2308e23c6460cfd01165af00c51a0f42d8578b75d7bd",
    "$.derivedFrom.operations[17].value.valueDomains.declaredOPEN.ProviderCapability.toolchainIdentitySource":
        "493964b22248ad57c91e2308e23c6460cfd01165af00c51a0f42d8578b75d7bd",
    "$.derivedFrom.operations[17].value.valueDomains.declaredOPEN.AbsentCapability.providerId":
        "c02ff1da686059cad47a3d7b76b2b2c2ce817f215a2abccc48cf95d409b2b5a8",
    "$.derivedFrom.operations[17].value.valueDomains.declaredOPEN.AbsentCapability.language":
        "493964b22248ad57c91e2308e23c6460cfd01165af00c51a0f42d8578b75d7bd",
    "$.derivedFrom.operations[17].value.valueDomains.censusIsEXHAUSTIVE":
        "a86edee09d68ece6052e8fccd3cda9bb067883e1b1af25a1b8e59a06da675343",
    "$.derivedFrom.operations[17].value.valueDomains.whatREMAINSOPENISTHEHONESTPART":
        "3696dad76a5711c264cb62c68f419d6e1cd86500c7554f5fca326738b22d24ef",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-1.statement":
        "77a27002988609acf04ae62ba73c463bfa0b4c2293205ba95be6252b235267a0",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-1.whyTHISANDNOTAPOINTERFIELD":
        "26b5b8da9a30801f0f82a7342a83bb7c07d38217e5e81bdf5890b4507c6a08e8",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-2.statement":
        "4819a306b9b987e66e08358dda0581e94c3e752c364a02cb60500a3ce7b1b40f",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-2.whyTHISISTHEREPAIRANDNOTARENAME":
        "118a18485f45452d5df68f6de9f63cd378fdbe9ed3097deeeb067c41ec526fbe",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-2.existenceAndUNIQUENESSAREBOTHREQUIRED":
        "778494026ece01ed8b116d9d21598c089ea6531891cf5ae91b358c63712d9ea3",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-3.statement":
        "5e63818fbff8a114f4182378fb5d47e90709839c3f4fe3f4dd0faf6df18e2a23",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-3.whyEQUALITYANDNOTARENAME":
        "e206570f100d7ca165de93bcfd93598b340aba30d3a0178bf5dc2b9ad4d03a38",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-3.andTHEREISNOTHIRDSPELLING":
        "37c8050e940619282367c0e01cdf11ae19f54e50e7a1cb7093731a3ecf94c441",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-4.statement":
        "771ee69250b07d97d7591643317cca4fcb733124eb0bc7da9306d807ec7464a4",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-4.whyTHISLAYERINGISNEEDED":
        "b0d86ca4b30a4b48a953e2f6e5d971fee3daeb204e5fc6fe4c4f2a22d200c45a",
    "$.derivedFrom.operations[18].value.theCLOSE.DL-CUST-4.committedFormsArePUBLISHED":
        "04adcff7d14e30b9d5892dbd2afef2604f769ae62763d9066b5bf96b8deb91be",
}

# --selftest mutation switches.  Every one is read at exactly one site.
MUT = set()

# Artifact-level mutations replace bytes in the SUBJECT and are applied by
# --selftest before the re-parse.  Populated below, after the helpers exist.
ARTIFACT_MUTATIONS = []


# --------------------------------------------------------------------------- io
class Drift(Exception):
    pass


class DuplicateKey(Exception):
    def __init__(self, key, where):
        super().__init__("duplicate JSON key %r in %s" % (key, where))
        self.key = key
        self.where = where


def _hook_factory(where):
    def hook(pairs):
        seen = set()
        for key, _ in pairs:
            if key in seen and "DUP_KEY_HOOK_OFF" not in MUT:
                raise DuplicateKey(key, where)
            seen.add(key)
        return dict(pairs)
    return hook


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha_text(text):
    return hashlib.sha256(unicodedata.normalize("NFC", text).encode("utf-8")).hexdigest()


def read_bytes(rel):
    path = COOP / rel
    if not path.exists():
        raise Drift("pinned input is absent: %s" % rel)
    return path.read_bytes()


def verify_pins():
    """Hash-verify every pinned input BEFORE anything is parsed.

    Returns (problems, verified_bytes).  The bytes come back with the report so
    that nothing below has to re-open a file this function already verified: a
    checker that re-reads after verifying has a window, and closing that window
    is one of the four repairs this successor carries.
    """
    problems = []
    verified = {}
    for rel, expected in PINNED.items():
        raw = read_bytes(rel)
        actual = sha_bytes(raw)
        if rel == SUBJECT and "SUBJECT_DRIFT" in MUT:
            actual = "0" * 64
        if actual != expected:
            problems.append("%s: recorded %s, measured %s" % (rel, expected, actual))
        verified[rel] = raw
    return problems, verified


def parse_json(raw, where):
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_hook_factory(where))


# ------------------------------------------------------------------- encoder A
class EncErr(Exception):
    pass


def encA(v):
    """CVE1, recursive, from resolved-inputs.v2#planIdContract.canonicalValueEncoding."""
    if v is None:
        return b"\x00"
    if type(v) is bool:
        return b"\x02" if v else b"\x01"
    if type(v) is float:
        if "FLOAT_ADMITTED" in MUT:
            return b"\x03" + int(v).to_bytes(8, "big")
        raise EncErr("floating-point values are forbidden")
    if type(v) is int:
        if v < 0:
            return b"\x07" + v.to_bytes(8, "big", signed=True)
        return b"\x03" + v.to_bytes(8, "big")
    if type(v) is str:
        if unicodedata.normalize("NFC", v) != v:
            if "NFC_NORMALISE" in MUT:
                v = unicodedata.normalize("NFC", v)
            else:
                raise EncErr("string is not NFC and is rejected, never normalised")
        raw = v.encode("utf-8")
        return b"\x04" + len(raw).to_bytes(4, "big") + raw
    if type(v) is list:
        return (b"\x05" + len(v).to_bytes(4, "big")
                + b"".join(encA(e) for e in v))
    if type(v) is dict:
        keys = list(v)
        if len(set(keys)) != len(keys):
            raise EncErr("duplicate map key")
        for k in keys:
            if type(k) is not str:
                raise EncErr("map key is not a string")
        out = b"\x06" + len(keys).to_bytes(4, "big")
        for k in sorted(keys, key=lambda s: s.encode("utf-8")):
            out += encA(k) + encA(v[k])
        return out
    raise EncErr("value outside CVE1's eight closed types: %s" % type(v).__name__)


# ------------------------------------------------------------------- encoder B
_TAGS = {"null": 0x00, "false": 0x01, "true": 0x02, "unsigned-64": 0x03,
         "NFC-UTF8-string": 0x04, "array": 0x05, "string-keyed-map": 0x06,
         "negative-signed-64": 0x07}


def _be(n, width):
    return bytes((n >> shift) & 0xFF for shift in range(width * 8 - 8, -1, -8))


def _cve1_type_name(v):
    cls = type(v)
    if cls is type(None):
        return "null"
    if cls is bool:
        return "true" if v else "false"
    if cls is int:
        return "unsigned-64" if v >= 0 else "negative-signed-64"
    if cls is float:
        if "FLOAT_ADMITTED" in MUT:
            return "unsigned-64"
        raise EncErr("floating-point values are forbidden")
    if cls is str:
        return "NFC-UTF8-string"
    if cls is list:
        return "array"
    if cls is dict:
        return "string-keyed-map"
    raise EncErr("value outside CVE1's eight closed types: %s" % cls.__name__)


def encB(root):
    """CVE1, table-driven on the eight closed type NAMES, explicit work stack."""
    out = bytearray()
    stack = [root]
    while stack:
        v = stack.pop()
        name = _cve1_type_name(v)
        out.append(_TAGS[name])
        if name in ("null", "true", "false"):
            continue
        if name == "unsigned-64":
            out += _be(int(v), 8)
        elif name == "negative-signed-64":
            out += _be(int(v) + (1 << 64), 8)
        elif name == "NFC-UTF8-string":
            if unicodedata.normalize("NFC", v) != v:
                if "NFC_NORMALISE" in MUT:
                    v = unicodedata.normalize("NFC", v)
                else:
                    raise EncErr("string is not NFC and is rejected, never normalised")
            raw = v.encode("utf-8")
            out += _be(len(raw), 4) + raw
        elif name == "array":
            out += _be(len(v), 4)
            for element in reversed(v):
                stack.append(element)
        else:
            keys = list(v)
            if len(set(keys)) != len(keys):
                raise EncErr("duplicate map key")
            for k in keys:
                if type(k) is not str:
                    raise EncErr("map key is not a string")
            out += _be(len(keys), 4)
            for k in sorted(keys, key=lambda s: s.encode("utf-8"), reverse=True):
                stack.append(v[k])
                stack.append(k)
    return bytes(out)


# --------------------------------------------------------------------- decoder
def decode(buf):
    value, offset = _dec(buf, 0)
    if offset != len(buf):
        raise EncErr("trailing bytes after a complete CVE1 value")
    return value


def _dec(b, i):
    if i >= len(b):
        raise EncErr("truncated CVE1 value")
    tag = b[i]
    i += 1
    if tag == 0x00:
        return None, i
    if tag == 0x01:
        return False, i
    if tag == 0x02:
        return True, i
    if tag == 0x03:
        return int.from_bytes(b[i:i + 8], "big"), i + 8
    if tag == 0x07:
        return int.from_bytes(b[i:i + 8], "big", signed=True), i + 8
    if tag == 0x04:
        n = int.from_bytes(b[i:i + 4], "big")
        i += 4
        return b[i:i + n].decode("utf-8"), i + n
    if tag == 0x05:
        n = int.from_bytes(b[i:i + 4], "big")
        i += 4
        out = []
        for _ in range(n):
            value, i = _dec(b, i)
            out.append(value)
        return out, i
    if tag == 0x06:
        n = int.from_bytes(b[i:i + 4], "big")
        i += 4
        out = {}
        for _ in range(n):
            key, i = _dec(b, i)
            value, i = _dec(b, i)
            out[key] = value
        return out, i
    raise EncErr("unknown CVE1 tag 0x%02x" % tag)


class EncoderDisagreement(Exception):
    pass


def cve1(value):
    """Both encoders, always.  A disagreement is a defect, never a tie-break."""
    a = encA(value)
    b = encB(value)
    if a != b:
        raise EncoderDisagreement("encoder A and encoder B disagree")
    return a


# ------------------------------------------------------------------- walking
def leaves(node, path="$"):
    """Every leaf with its JSON path.  Used by seven gates; defined once."""
    if type(node) is dict:
        for key, value in node.items():
            for item in leaves(value, path + "." + key):
                yield item
    elif type(node) is list:
        for index, value in enumerate(node):
            for item in leaves(value, path + "[%d]" % index):
                yield item
    else:
        yield path, node


def objects(node, path="$"):
    if type(node) is dict:
        yield path, node
        for key, value in node.items():
            for item in objects(value, path + "." + key):
                yield item
    elif type(node) is list:
        for index, value in enumerate(node):
            for item in objects(value, path + "[%d]" % index):
                yield item


def norm_text(s):
    """Whitespace- and dash-normalised, for comparing prose across documents.

    Never used to decide whether a normative statement is CORRECT -- only to ask
    whether a quotation is present in the document it names, where the artifact
    may legitimately render an em dash as `--` and the live file may wrap a
    sentence across a line break.
    """
    for a, b in (("—", "--"), ("–", "--"), ("‘", "'"),
                 ("’", "'"), ("“", '"'), ("”", '"')):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


_DL_ID = re.compile(r"^DL-[A-Z]+-[0-9]+$")
_HEX64 = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")

# The blocks this checker COMPILES ITS CONSTANTS FROM.  Naming the block one
# reads is not transcribing its contents: every key set, count, member list,
# sort key, gate order and domain label is derived from inside these, and NOTHING
# inside them is a Python literal here.  They are listed once and used twice --
# by Contract, to read the rule, and by derive_seal_domain, to seal the prose
# that states it -- so the two cannot drift apart.  A false sentence inside a
# block a checker compiles from is a false sentence an implementer reads AS the
# rule, which is the defect this successor exists to close.
COMPILED_SCHEMA_BLOCKS = (
    "capabilityManifestSchema.orderedCollections",
    "capabilityManifestSchema.recordClosure",
    "capabilityManifestSchema.valueDomains",
    "capabilityManifestSchema.capabilityManifestId",
)
COMPILED_IDENTITY_BLOCKS = (
    "recordShape", "admission", "orderingRuling", "valueDomains",
    "namespaceAndDomainSeparator", "recipe", "textForm",
)


# ------------------------------------------------------------------- contract
class ContractError(Exception):
    """The artifact does not carry a block this checker must compile from it."""


class Contract:
    """Every constant the predecessor hand-typed, COMPILED from the artifact.

    Nothing in this class is a Python literal describing the subject.  Each field
    is read from the artifact under check and, where the predecessor document
    states the same thing, cross-checked against delivery.v2's verified bytes.
    A false declaration therefore does not merely fail a string comparison: it
    changes what this checker DOES, and the artifact's own published ids, byte
    lengths, violation lists and negative-control outcomes stop reproducing.
    """

    def __init__(self, art, base, fact, resolved, run):
        self.run = run
        self.ops = art["derivedFrom"]["operations"]
        self.by_path = {}
        for op in self.ops:
            self.by_path.setdefault(op["path"], []).append(op)
        self.identity = self._op_value("capabilityManifestIdentity")
        self.record_closure = self._op_value("capabilityManifestSchema.recordClosure")
        self.value_domains = self._op_value("capabilityManifestSchema.valueDomains")
        self.ordered = self._op_value("capabilityManifestSchema.orderedCollections")

        # --- record shapes, from the artifact, checked against the predecessor
        shape = self.identity["recordShape"]
        self.records = {}
        self.maps = {}
        for name, spec in shape.items():
            if type(spec) is not dict or "kind" not in spec:
                continue
            if spec["kind"] == "RECORD":
                self.records[name] = list(spec["requiredKeys"])
            elif spec["kind"] == "MAP":
                self.maps[name] = spec
            else:
                run.fail("DV5-CONTRACT", "recordShape.%s.kind" % name,
                         "a reachable object type is declared %r, which is neither RECORD "
                         "nor MAP, so DL-CLOSED-1 has no reading for it" % spec["kind"])
        if not self.records:
            raise ContractError("recordShape declares no RECORD type")
        by_keyset = {}
        for name, keys in self.records.items():
            frozen = frozenset(keys)
            if len(frozen) != len(keys):
                run.fail("DV5-CONTRACT", "recordShape.%s.requiredKeys" % name,
                         "the declared key set repeats a key, so it is not a key SET")
            if frozen in by_keyset:
                run.fail("DV5-CONTRACT", "recordShape",
                         "%s and %s declare the SAME key set, so a value cannot be "
                         "classified by its keys" % (by_keyset[frozen], name))
            by_keyset[frozen] = name
        self._by_keyset = by_keyset

        # --- the declared sort keys drive canonicalisation and ADM-ORDER
        self.sort_keys = dict(self.ordered["declaredSortKeys"])
        self.order_exemptions = list(self.ordered.get("orderBearingExemptions", []))

        # --- the admission gate order drives the gate runner
        self.gate_order = list(self.identity["admission"]["gateOrder"])

        # --- the domain label, from the artifact's own CLOSED vocabulary
        vocab = self.identity["namespaceAndDomainSeparator"]["closedDomainVocabulary"]
        members = list(vocab["members"])
        if len(members) != 1:
            run.fail("DV5-CONTRACT", "closedDomainVocabulary.members",
                     "the minted domain family declares %d members; this recipe mints "
                     "exactly one label and the census cannot resolve %r"
                     % (len(members), members))
        self.domain = members[0] if members else ""
        self.domain_closed = vocab.get("closed")

        # --- PLAN-ID-V1, entirely from resolved-inputs.v2 (a PINNED input)
        contract = resolved["planIdContract"]
        fields = sorted(contract["preimageFields"], key=lambda f: f["tag"])
        self.plan_fields = [f["name"] for f in fields]
        self.plan_tags = [f["tag"] for f in fields]
        framing = contract["preimageFraming"]
        found = re.search(r"([0-9a-f]{8,})", framing["domainBytes"])
        self.plan_domain_bytes = bytes.fromhex(found.group(1)) if found else b""
        self.plan_recipe_version = framing["recipeVersion"]
        prefix = contract["identityRepresentation"]["text"]
        self.plan_text_prefix = prefix.split("<")[0]

        # --- registries, resolved by OBSERVATION against predecessor sources
        self.registries = self.value_domains["registries"]
        self.declared_open = dict(self.value_domains["declaredOPEN"])
        self.candidates = self._candidate_registries(base, fact)
        self.bound_positions = []
        self.position_registry = {}
        for name, spec in self.registries.items():
            for position in spec["boundPositions"]:
                self.bound_positions.append(position)
                self.position_registry[position] = name

    # -- helpers ---------------------------------------------------------------
    def _op_value(self, path):
        rows = self.by_path.get(path)
        if not rows:
            raise ContractError("the artifact declares no operation at %r" % path)
        if len(rows) != 1:
            self.run.fail("DV5-CONTRACT", "derivedFrom.operations",
                          "%d operations write %r; the last would silently win" %
                          (len(rows), path))
        return rows[-1]["value"]

    def record_for(self, obj):
        if type(obj) is not dict:
            return None
        return self._by_keyset.get(frozenset(obj))

    def compile_shapes(self, samples, fact, run):
        """Which collection holds which record, and which scalar is which type.

        Derived by OBSERVING the predecessor's four live manifests and the
        artifact's own committed vectors against the compiled record shapes.  It
        is what lets every gate below name a record, a collection and a scalar
        position without this file containing one of those names.
        """
        self.relation_ladder = fact["relationRegistry"]["relations"]
        roots = {self.record_for(m) for m in samples}
        roots.discard(None)
        if len(roots) != 1:
            run.fail("DV5-CONTRACT", "recordShape",
                     "the live manifests match %r declared record key sets, so this "
                     "checker cannot say which record type a manifest IS" % sorted(roots))
            self.root = sorted(self.records)[0]
        else:
            self.root = roots.pop()
        self.element_type = {}
        self.scalar_arrays = set()

        def visit(record, obj):
            for key in self.records.get(record, []):
                qualified = "%s.%s" % (record, key)
                value = obj.get(key)
                if qualified in self.maps or type(value) is not list:
                    continue
                for element in value:
                    if type(element) is dict:
                        nested = self.record_for(element)
                        if nested is not None:
                            self.element_type[qualified] = nested
                            visit(nested, element)
                    else:
                        self.scalar_arrays.add(qualified)

        for manifest in samples:
            record = self.record_for(manifest)
            if record is not None:
                visit(record, manifest)
        # A collection that is empty in every sample carries no witness; the
        # artifact's own declaredSortKeys says which kind it is.
        for qualified, declared in self.sort_keys.items():
            if qualified in self.element_type or qualified in self.scalar_arrays:
                continue
            head = declared.split(",")[0].strip()
            if head.startswith("the element string"):
                self.scalar_arrays.add(qualified)
        both = sorted(set(self.element_type) & self.scalar_arrays)
        if both:
            run.fail("DV5-CONTRACT", "recordShape",
                     "a declared collection holds records in one manifest and scalars in "
                     "another: %r" % both)
        self.scalar_kinds = derive_scalar_kinds(self, samples)

    @staticmethod
    def _candidate_registries(base, fact):
        """Candidate member sets, every one derived from a PINNED predecessor.

        Not one of these is read from the subject.  A registry the subject
        publishes is accepted only if it EQUALS the candidate that the values
        actually carried at its bound positions resolve to.
        """
        matrix = base["platformMatrix"]
        matrix_ids = ([row["platformId"] for row in matrix["supported"]]
                      + [row["platformId"] for row in matrix["bestEffort"]])
        absent_rule = base["capabilityManifestSchema"]["AbsentCapability"]["rule"]
        literal = re.search(r"coverageState is ([A-Za-z0-9_-]+)", absent_rule)
        return {
            "delivery.v2#platformMatrix + the aggregate token": None,   # filled below
            "fact-plane.v1#relationRegistry.relations":
                sorted(fact["relationRegistry"]["relations"]),
            "fact-plane.v1#deficiencyVocabulary.values":
                sorted(fact["deficiencyVocabulary"]["values"]),
            "delivery.v2#AbsentCapability.rule, the literal":
                [literal.group(1)] if literal else [],
            "_matrix": sorted(matrix_ids),
        }




# ----------------------------------------------------- admission, contract-driven
#
# Every gate below reads its rule from the compiled Contract.  Nothing here
# names a key, a record, a registry or a position: the names come from
# recordShape, declaredSortKeys, valueDomains and gateOrder, and the diagnostic
# vocabulary is the artifact's own, because the artifact publishes COMPLETE
# violation lists as goldens and this checker must reproduce them exactly.


def _prefix(c, record):
    """The artifact spells the root record's fields bare and nests the others."""
    return "" if record == c.root else record + "."


def adm_type(c, manifest, errs):
    """Section 6 law 18.  EXACT type, never isinstance.

    Which declared scalars are integers and which are strings is recovered from
    the PREDECESSOR'S live values by derive_scalar_kinds, not transcribed here.
    """
    def is_int(x):
        if "EXACT_TYPE_OFF" in MUT:
            return isinstance(x, int)
        return type(x) is int

    def is_str(x):
        if "EXACT_TYPE_OFF" in MUT:
            return isinstance(x, str)
        return type(x) is str

    def check(record, obj):
        if type(obj) is not dict:
            errs.append("%s: exact-type -- entry is not an object" % record)
            return
        head = _prefix(c, record)
        for key in c.records[record]:
            qualified = "%s.%s" % (record, key)
            value = obj.get(key)
            if qualified in c.maps:
                if type(value) is not dict:
                    errs.append("%s%s: exact-type -- not an object" % (head, key))
                continue
            if qualified in c.element_type or qualified in c.scalar_arrays:
                if type(value) is not list:
                    errs.append("%s%s: exact-type -- not an array" % (head, key))
                    continue
                for element in value:
                    nested = c.element_type.get(qualified)
                    if nested is not None:
                        check(nested, element)
                    elif not is_str(element):
                        errs.append("%s%s: exact-type -- %s is not a string"
                                    % (head, key, type(element).__name__))
                continue
            kind = c.scalar_kinds.get(record, {}).get(key, "str")
            if kind == "int" and not is_int(value):
                errs.append("%s%s: exact-type -- %s is not an integer"
                            % (head, key, type(value).__name__))
            elif kind == "str" and not is_str(value):
                errs.append("%s%s: exact-type -- %s is not a string"
                            % (head, key, type(value).__name__))

    check(c.root, manifest)
    return errs


def adm_closed(c, manifest, errs):
    """DL-CLOSED-1.  Records are closed; a map declares a key domain and is not.

    MUT CLOSE_THE_MAP reinstates delivery.v3's catch-all reading, under which a
    reachable object type with no declared key set -- which the declared MAP is
    -- is inadmissible.  That is blocker IR-V3-B1 and it refuses all four live
    manifests, which is exactly what the mutation must demonstrate.
    """
    def check(record, obj):
        if type(obj) is not dict:
            return
        if sorted(obj) != sorted(c.records[record]):
            errs.append("%s: field set %r != %r"
                        % (record, sorted(obj), sorted(c.records[record])))
            return
        for key in c.records[record]:
            qualified = "%s.%s" % (record, key)
            value = obj.get(key)
            if qualified in c.maps:
                if "CLOSE_THE_MAP" in MUT:
                    errs.append("%s: a reachable object type that declares no key set is "
                                "inadmissible until it declares one" % qualified)
                    continue
                for inner in (value or {}).values():
                    if type(inner) is dict:
                        errs.append("%s: a declared map's value is an object, so "
                                    "DL-CLOSED-1's recursive clause applies and this "
                                    "object is unclosed" % qualified)
            elif qualified in c.element_type and type(value) is list:
                for element in value:
                    check(c.element_type[qualified], element)

    check(c.root, manifest)
    return errs


def _position_label(position):
    """The artifact writes a bound position's diagnostic without its suffix."""
    for suffix in ("[]", " key", " value"):
        if position.endswith(suffix):
            return position[:-len(suffix)]
    return position


def adm_domain(c, manifest, errs):
    """DL-DOM-1.  Bound scalars are compared by EXACT NFC UTF-8 bytes.

    The position-to-registry binding is the ARTIFACT'S, read from
    valueDomains.registries[*].boundPositions, and the diagnostic names the
    artifact's own registry key.  Rebinding a position to a different registry
    therefore changes what this gate accepts, which is why the rebinding
    mutation is caught by execution and not only by a seal.
    """
    if "SKIP_DOMAIN" in MUT:
        return errs
    for position, value in observed_at_positions(c, manifest):
        registry = c.position_registry.get(position)
        if registry is None:
            if position in c.declared_open:
                continue
            errs.append("%s: neither bound to a named registry nor declared open, which "
                        "DL-DOM-1 makes a schema defect" % position)
            continue
        spec = c.registries[registry]
        if "members" not in spec:
            continue            # a rule registry; the ladder clause below carries it
        if value not in spec["members"]:
            if position.endswith(" key"):
                errs.append("%s: key %r is not a member of %s"
                            % (_position_label(position), value, registry))
            else:
                errs.append("%s: %r is not a member of %s"
                            % (_position_label(position), value, registry))
    for qualified in sorted(c.maps):
        record, _, key = qualified.rpartition(".")
        for obj in _records_of_type(c, manifest, record):
            entries = obj.get(key)
            if type(entries) is not dict:
                continue
            for map_key, rung in entries.items():
                ladder = c.relation_ladder.get(map_key)
                if ladder is None:
                    continue
                if rung not in ladder["ladder"]:
                    errs.append("%s: %r is not a rung of relation %r's ladder"
                                % (qualified, rung, map_key))
    return errs


def _records_of_type(c, manifest, record):
    """Every value of a declared record type reachable from a manifest."""
    if record == c.root:
        yield manifest
        return
    stack = [(c.root, manifest)]
    while stack:
        current, obj = stack.pop()
        if type(obj) is not dict:
            continue
        for key in c.records.get(current, []):
            qualified = "%s.%s" % (current, key)
            nested = c.element_type.get(qualified)
            if nested is None or type(obj.get(key)) is not list:
                continue
            for element in obj[key]:
                if nested == record:
                    yield element
                stack.append((nested, element))


def _ascending(seq, key_of, where, errs):
    for i in range(1, len(seq)):
        previous = key_of(seq[i - 1]).encode("utf-8")
        current = key_of(seq[i]).encode("utf-8")
        if not previous < current:
            errs.append("%s: not strictly ascending by declared key UTF-8 bytes at "
                        "index %d (%r then %r)"
                        % (where, i, key_of(seq[i - 1]), key_of(seq[i])))


def _sort_key_of(c, qualified):
    """The declared sort key for an ordered collection, READ FROM THE ARTIFACT.

    'the element string' means the element itself; 'NOT AN ORDERED COLLECTION'
    excludes it; anything else names the field the elements are keyed by.
    """
    declared = c.sort_keys.get(qualified)
    if declared is None:
        return None
    head = declared.split(",")[0].strip()
    if head.startswith("NOT AN ORDERED COLLECTION"):
        return None
    if head.startswith("the element string"):
        return lambda s: s
    return lambda d: d[head]


def adm_order(c, manifest, errs):
    """DL-ORD-1, in the traversal the artifact declares at admission.traversalOrder.

    The declared traversal is: for each element of each root collection in index
    order, that element's own collections; then the root's collections.  Both
    halves are walked in the record's declared key order, so nothing here depends
    on which violation happens to be first.
    """
    if "SKIP_ORDER" in MUT:
        return errs
    for key in c.records[c.root]:
        qualified = "%s.%s" % (c.root, key)
        nested = c.element_type.get(qualified)
        if nested is None or type(manifest.get(key)) is not list:
            continue
        for element in manifest[key]:
            if type(element) is not dict:
                continue
            for inner in c.records.get(nested, []):
                inner_qualified = "%s.%s" % (nested, inner)
                if inner_qualified not in c.scalar_arrays:
                    continue
                key_of = _sort_key_of(c, inner_qualified)
                if key_of is None or type(element.get(inner)) is not list:
                    continue
                _ascending(element[inner], key_of, inner_qualified, errs)
    for key in c.records[c.root]:
        qualified = "%s.%s" % (c.root, key)
        if qualified not in c.element_type and qualified not in c.scalar_arrays:
            continue
        key_of = _sort_key_of(c, qualified)
        if key_of is None or type(manifest.get(key)) is not list:
            continue
        _ascending(manifest[key], key_of, qualified, errs)
    return errs


_GATES = {"ADM-TYPE": adm_type, "ADM-CLOSED": adm_closed,
          "ADM-DOMAIN": adm_domain, "ADM-ORDER": adm_order}

# The two gates a later gate depends on: a domain check needs to know which
# fields exist, and an ordering needs values that are in a domain.  Which gates
# these are is the ARTIFACT'S statement, at valueDomains.gateOrder, and the
# prerequisite relation is read off the declared order rather than fixed here.
def admit(c, manifest):
    """The gates, IN THE ORDER THE ARTIFACT DECLARES.  Returns a message list."""
    errs = []
    for index, name in enumerate(c.gate_order):
        gate = _GATES.get(name)
        if gate is None:
            errs.append("%s: the artifact declares an admission gate this checker cannot "
                        "execute" % name)
            continue
        gate(c, manifest, errs)
        if errs and index < len(c.gate_order) - 1:
            return errs
    return errs


def canonicalise(c, manifest):
    """The producer-side canonicalisation, driven by the DECLARED sort keys."""
    if "NO_CANONICALISE" in MUT:
        return copy.deepcopy(manifest)

    def rebuild(record, obj):
        if type(obj) is not dict:
            return copy.deepcopy(obj)
        out = dict(obj)
        for key in c.records.get(record, []):
            qualified = "%s.%s" % (record, key)
            value = obj.get(key)
            if type(value) is not list:
                continue
            key_of = _sort_key_of(c, qualified)
            nested = c.element_type.get(qualified)
            if nested is not None:
                elements = [rebuild(nested, element) for element in value]
                if key_of is not None:
                    if "SORT_BY_ENCODED_BYTES" in MUT:
                        elements = sorted(elements, key=cve1)
                    else:
                        elements = sorted(elements,
                                          key=lambda d: key_of(d).encode("utf-8"))
                out[key] = elements
            elif key_of is not None:
                if "SORT_BY_ENCODED_BYTES" in MUT:
                    out[key] = sorted(value, key=cve1)
                else:
                    out[key] = sorted(value, key=lambda s: s.encode("utf-8"))
        return out

    return rebuild(c.root, manifest)


def cap_manifest_id(c, manifest):
    prefix = c.domain.encode("utf-8")
    if "NO_NUL" not in MUT:
        prefix += b"\x00"
    return hashlib.sha256(prefix + cve1(manifest)).hexdigest()


# ------------------------------------------------------------------ PLAN-ID-V1
_SET_VALUED_STAGE_ARRAYS = ("dependsOn", "relations", "ruleIds", "capabilityGrants")


def _utf8(s):
    return s.encode("utf-8")


def canonicalise_plan(plan):
    p = copy.deepcopy(plan)
    p["resolvedConfiguration"] = sorted(p["resolvedConfiguration"],
                                        key=lambda d: _utf8(d["path"]))
    scope = p["scope"]
    scope["workspaceUnitIds"] = sorted(set(scope["workspaceUnitIds"]), key=_utf8)
    scope["requestedPaths"] = sorted(set(scope["requestedPaths"]), key=_utf8)
    p["contributions"] = sorted(p["contributions"], key=lambda d: _utf8(d["activationId"]))
    p["semanticUniverses"] = sorted(p["semanticUniverses"],
                                    key=lambda d: _utf8(d["providerId"]))
    p["capabilityGrants"] = sorted(
        p["capabilityGrants"],
        key=lambda d: (_utf8(d["grantId"]), _utf8(d["grantVersion"]), _utf8(d["projectId"])))
    stages = sorted(p["workflow"]["stages"], key=lambda d: _utf8(d["stageId"]))
    for stage in stages:
        for name in _SET_VALUED_STAGE_ARRAYS:
            if type(stage.get(name)) is list:
                stage[name] = sorted(set(stage[name]), key=_utf8)
    p["workflow"]["stages"] = stages
    return p


def plan_preimage(c, plan):
    p = canonicalise_plan(plan)
    out = bytearray(c.plan_domain_bytes)
    out += c.plan_recipe_version.to_bytes(2, "big")
    out += len(c.plan_fields).to_bytes(2, "big")
    for tag, name in zip(c.plan_tags, c.plan_fields):
        encoded = cve1(p[name])
        out.append(tag)
        out += len(encoded).to_bytes(4, "big")
        out += encoded
    return bytes(out)


def plan_id(c, plan):
    pre = plan_preimage(c, plan)
    return pre, c.plan_text_prefix + hashlib.sha256(pre).hexdigest()


# ----------------------------------------------------------------------- the run
class Run:
    def __init__(self, verbose=False):
        self.findings = []
        self.counts = {}
        self.notes = []
        self.verbose = verbose
        self.recomputed = set()

    def fail(self, code, position, detail):
        self.findings.append("%s at %s: %s" % (code, position, detail))

    def eq(self, code, position, recomputed, published, note=""):
        """recomputed is what THIS RUN computed; published is what the ARTIFACT says.

        The predecessor inverted these two at gate_derivation and reported
        "recomputed X, artifact publishes X" on a real mismatch.  The order is
        (recomputed, published) at every call site in this file.
        """
        if "NO_RECOMPUTE_LEDGER" not in MUT:
            for value in (recomputed, published):
                if type(value) is str:
                    self.recomputed.update(_HEX64.findall(value))
        if recomputed != published:
            self.fail(code, position,
                      "recomputed %r, artifact publishes %r%s"
                      % (recomputed, published, (" -- " + note) if note else ""))
            return False
        self.counts[code] = self.counts.get(code, 0) + 1
        return True

    def bump(self, name, n=1):
        self.counts[name] = self.counts.get(name, 0) + n


class _temporarily:
    """Add a reading switch for one measurement and restore EXACTLY what was there.

    A naive add/discard pair silently deletes a switch --selftest has already set,
    which makes the mutation under test disappear and the run come back clean.
    """

    def __init__(self, flags, name):
        self.flags = flags
        self.name = name
        self.was_present = name in flags

    def __enter__(self):
        self.flags.add(self.name)
        return self

    def __exit__(self, *exc):
        if not self.was_present:
            self.flags.discard(self.name)
        return False


# ------------------------------------------------- derived structural census
def derive_scalar_kinds(c, samples):
    """Which declared scalar keys hold integers and which hold strings.

    Recovered from the PREDECESSOR'S live values, not from a literal here.  It is
    what makes ADM-TYPE's `schemaVersion is a JSON integer, everything else is a
    JSON string` executable without transcribing either half.
    """
    kinds = {}
    for manifest in samples:
        stack = [(c.record_for(manifest), manifest)]
        while stack:
            record, obj = stack.pop()
            if record is None or type(obj) is not dict:
                continue
            for key in c.records.get(record, []):
                qualified = "%s.%s" % (record, key)
                value = obj.get(key)
                if qualified in c.maps:
                    continue
                if type(value) is bool:
                    kinds.setdefault(record, {})[key] = "bool"
                elif type(value) is int:
                    kinds.setdefault(record, {})[key] = "int"
                elif type(value) is str:
                    kinds.setdefault(record, {})[key] = "str"
                elif type(value) is list:
                    nested = c.element_type.get(qualified)
                    if nested is not None:
                        for element in value:
                            stack.append((nested, element))
    return kinds


def observed_at_positions(c, manifest):
    """Yield (declared scalar position, value) for every scalar in the manifest.

    The position NAMES are built from the compiled record shapes and the compiled
    map declarations, so they are the artifact's own vocabulary and not this
    file's.  This one walk drives DL-DOM-1's gate and DL-DOM-1's census.
    """
    def walk(record, obj):
        if type(obj) is not dict:
            return
        for key in c.records.get(record, []):
            qualified = "%s.%s" % (record, key)
            value = obj.get(key)
            if qualified in c.maps:
                if type(value) is dict:
                    for map_key, map_value in value.items():
                        yield (qualified + " key", map_key)
                        yield (qualified + " value", map_value)
                continue
            nested = c.element_type.get(qualified)
            if nested is not None:
                for element in (value if type(value) is list else []):
                    for item in walk(nested, element):
                        yield item
                continue
            if qualified in c.scalar_arrays:
                for element in (value if type(value) is list else []):
                    yield (qualified + "[]", element)
                continue
            yield (qualified, value)

    for item in walk(c.root, manifest):
        yield item


def derive_scalar_positions(c, samples):
    """The reachable scalar TYPE-positions, derived by walking real values.

    A collection that is empty in every sample carries no witness, so
    Contract.compile_shapes recovers its element kind from the artifact's own
    declaredSortKeys and it is added here from that.  Nothing in this function
    or its callers names a position: the fourteen come out of the walk.
    """
    positions = set()
    for manifest in samples:
        for position, _ in observed_at_positions(c, manifest):
            positions.add(position)
    for qualified in c.scalar_arrays:
        positions.add(qualified + "[]")
    return positions


# ------------------------------------------------------------------------ gates
def gate_duplicate_key_hook(run):
    """The hook must RAISE and must NAME the key (freeze section 7.5)."""
    probe = '{"a": 1, "b": 2, "a": 3}'
    try:
        json.loads(probe, object_pairs_hook=_hook_factory("<selftest probe>"))
    except DuplicateKey as exc:
        if exc.key != "a" or "a" not in str(exc):
            run.fail("DV5-PARSE", "<duplicate-key probe>",
                     "the hook raised without naming the duplicated key")
        else:
            run.bump("duplicateKeyProbes")
        return
    run.fail("DV5-PARSE", "<duplicate-key probe>",
             "a duplicate JSON key was ADMITTED; json.loads keeps the last of duplicates, "
             "so a document can say one thing to a reader and another to every instrument")


_SPAN = re.compile(r"(?:(?<=^)|(?<=[\s:(]))'([^']{20,})'(?=$|[\s,.);])")
_SOURCE_NAME = re.compile(r"[A-Za-z0-9._-]+\.(?:md|json|py)|[a-z0-9-]+\.v[0-9]+")
_VERBATIM = re.compile(r"(?i)verbatim|\breads[,:]|\bwrites[,:]|in its own words"
                       r"|quoted and never reworded")


def gate_quotations(run, art, sources):
    """Every quotation the artifact marks VERBATIM, verified against the SOURCE.

    The predecessor carried seven freeze propositions as hand-typed Python string
    literals and asked whether they were present.  That tests the transcription.
    This gate takes the needle FROM THE ARTIFACT and asks the same question of the
    live bytes of the document the artifact names, so a fabricated quotation --
    including a fabricated section 6 law 2 -- is absent and is a finding, and an
    appended clause makes a longer needle that is equally absent.
    """
    marked, unmarked, elided, unattributed = 0, 0, 0, 0
    for path, value in leaves(art):
        if type(value) is not str:
            continue
        for match in _SPAN.finditer(value):
            names = _SOURCE_NAME.findall(value[:match.start()])
            if not names:
                continue
            span = norm_text(match.group(1))
            if "MANGLE_QUOTE" in MUT:
                span = span.replace("neutralise", "neutralize")
            if "..." in span:
                elided += 1
                continue
            hits = [name for name, text in sources.items()
                    if _present(text, span)]
            if _VERBATIM.search(value[:match.start()]):
                marked += 1
                if not hits:
                    run.fail("DV5-QUOTE", path,
                             "a VERBATIM-marked quotation of %r is present in NO source "
                             "this checker can read: %r" % (names[-1], span[:120]))
                else:
                    run.bump("verbatimQuotationsVerified")
            else:
                unmarked += 1
                if hits:
                    run.bump("unmarkedQuotationsAlsoPresent")
                else:
                    unattributed += 1
    run.notes.append("quotation census: %d verbatim-marked, %d unmarked, %d elided, "
                     "%d unmarked spans matched no source" %
                     (marked, unmarked, elided, unattributed))
    if marked == 0:
        run.fail("DV5-QUOTE", "$",
                 "the artifact marks no quotation VERBATIM, so this gate has nothing to "
                 "verify and the freeze propositions it cites are unbound")


def _present(hay, needle):
    if needle in hay:
        return True
    # A quotation spliced into a sentence may lower-case its first letter.  That
    # is the only editorial change admitted, and only at the first character.
    alt = needle[0].swapcase() + needle[1:]
    return alt in hay


def derive_seal_domain(art):
    """The normative neighbourhood of every declared DL-* property.

    Four clauses, every one derived from the artifact and none of them a path
    typed into this file:

      1. a string leaf whose own key IS a declared DL-* identifier;
      2. a string leaf inside the object that declares a DL-* identifier, or
         inside one of that object's IMMEDIATE sub-objects -- which is where the
         machine form of each property lives (closedTypesToday, mapTypesToday,
         declaredSortKeys, declaredOPEN, registries);
      3. a string leaf anywhere beneath a key that is itself a DL-* identifier,
         and the `statement` of any gate named in admission.gateOrder;
      4. a string leaf in an object that carries a `field` key naming one of the
         collections declaredSortKeys declares -- the per-field SET/SEQUENCE
         rulings, which are DL-ORD-1's machine form;
      5. every string leaf beneath a block this checker COMPILES A CONSTANT FROM,
         located by matching the operation's declared path against
         COMPILED_SCHEMA_BLOCKS and COMPILED_IDENTITY_BLOCKS.

    The domain is compared BOTH WAYS against STATEMENT_SEALS, so a normative
    statement that is added, deleted or moved is a finding before its content is
    ever looked at.
    """
    ops = {}
    for op in art["derivedFrom"]["operations"]:
        ops.setdefault(op["path"], op)
    gates = set()
    identity = ops.get("capabilityManifestIdentity")
    if identity:
        gates = set(identity["value"]["admission"]["gateOrder"])
    collections = set()
    ordered = ops.get("capabilityManifestSchema.orderedCollections")
    if ordered:
        collections = set(ordered["value"]["declaredSortKeys"])
    compiled = []
    for index, op in enumerate(art["derivedFrom"]["operations"]):
        stem = "$.derivedFrom.operations[%d].value" % index
        if op["path"] in COMPILED_SCHEMA_BLOCKS:
            compiled.append(stem)
        elif op["path"] == "capabilityManifestIdentity":
            for block in COMPILED_IDENTITY_BLOCKS:
                compiled.append(stem + "." + block)
    out = []

    def walk(node, path, key_chain, dl_depth, ruling):
        if type(node) is dict:
            declares = any(_DL_ID.match(k) for k in node)
            here = 0 if declares else (dl_depth + 1 if dl_depth is not None else None)
            is_ruling = ruling or node.get("field") in collections
            for key, value in node.items():
                walk(value, path + "." + key, key_chain + [key], here, is_ruling)
        elif type(node) is list:
            for index, value in enumerate(node):
                walk(value, path + "[%d]" % index, key_chain, dl_depth, ruling)
        elif type(node) is str:
            key = key_chain[-1] if key_chain else ""
            under_dl = any(_DL_ID.match(k) for k in key_chain[:-1])
            under_gate = len(key_chain) >= 2 and key_chain[-2] in gates
            inside = any(path == stem or path.startswith(stem + ".")
                         or path.startswith(stem + "[") for stem in compiled)
            if (_DL_ID.match(key) or (dl_depth is not None and dl_depth <= 1)
                    or under_dl or ruling or inside
                    or (under_gate and key == "statement")):
                out.append(path)

    walk(art, "$", [], None, False)
    return out


def gate_statement_seals(run, art):
    """The artifact's normative statements, by derived position and measured digest.

    Domain is compared BOTH WAYS.  A statement that is added, removed, moved,
    restored from the rejected candidate, negated, reversed or extended by an
    appended sentence moves its digest and is named here.
    """
    if "SEALS_OFF" in MUT:
        run.bump("sealsSuppressed")
        return
    derived = derive_seal_domain(art)
    index = {path: value for path, value in leaves(art) if type(value) is str}
    missing = sorted(set(derived) - set(STATEMENT_SEALS))
    stale = sorted(set(STATEMENT_SEALS) - set(derived))
    for path in missing:
        run.fail("DV5-SEAL", path,
                 "a normative statement this checker's derived domain reaches carries no "
                 "seal, so its text is unbound")
    for path in stale:
        run.fail("DV5-SEAL", path,
                 "this checker seals a normative position the artifact no longer states "
                 "at that path")
    for path in derived:
        if path not in STATEMENT_SEALS:
            continue
        measured = sha_text(index[path])
        if measured != STATEMENT_SEALS[path]:
            run.fail("DV5-SEAL", path,
                     "the normative statement's bytes moved: sealed %s, measured %s"
                     % (STATEMENT_SEALS[path][:16] + "…", measured[:16] + "…"))
        else:
            run.bump("statementsSealed")


def gate_rejected_candidate_differential(run, art, candidate):
    """The REJECTED candidate is the oracle, read from its own pinned bytes.

    Nothing about delivery.v3 is transcribed here.  Three bindings:
      * no string leaf of the subject may carry a normative statement the
        candidate published and the subject repaired;
      * the polarity of the DL-INJ-1 repair is bound by KEY NAME, which a
        word-preserving reversal cannot keep;
      * the instance list's LENGTH must equal the channel count the subject's own
        selfMeasurement publishes.
    """
    v3_statements = {}
    for path, value in leaves(candidate):
        if type(value) is not str:
            continue
        key = path.split(".")[-1].split("[")[0]
        if _DL_ID.match(key):
            v3_statements.setdefault(key, set()).add(norm_text(value))
    v4_statements = {}
    for path, value in leaves(art):
        if type(value) is not str:
            continue
        key = path.split(".")[-1].split("[")[0]
        if _DL_ID.match(key):
            v4_statements.setdefault(key, []).append((path, norm_text(value)))

    repaired = set()
    for name, texts in v4_statements.items():
        old = v3_statements.get(name)
        if not old:
            continue
        if all(text in old for _, text in texts):
            run.bump("propertiesCarriedUNCHANGEDfromTheRejectedCandidate")
            continue
        repaired.add(name)
        run.bump("propertiesREPAIREDagainstTheRejectedCandidate")

    forbidden = set()
    for name in repaired:
        forbidden |= v3_statements[name]
    if forbidden:
        for path, value in leaves(art):
            if type(value) is not str:
                continue
            flat = norm_text(value)
            for old in forbidden:
                if old in flat:
                    run.fail("DV5-DIFF", path,
                             "carries the rejected candidate's statement of a property "
                             "this document repairs; delivery.v3's text is the blocker's "
                             "own bytes and may not reappear at any leaf")
        run.bump("rejectedStatementsExcluded", len(forbidden))
    else:
        run.fail("DV5-DIFF", "$",
                 "no declared property differs from the rejected candidate's statement of "
                 "it, so this document repairs nothing it claims to repair")

    # --- polarity bound by STRUCTURE, not by words
    v3_keys = set()
    for path, _ in leaves(candidate):
        v3_keys.update(part.split("[")[0] for part in path.split("."))
    v4_keys = {}
    for path, value in leaves(art):
        for part in path.split("."):
            v4_keys.setdefault(part.split("[")[0], []).append(path)
    for key in ("thereforeITALSOFINDSTHETHIRDONE", "theTWOINSTANCESKNOWNTODAY"):
        if key in v3_keys and key in v4_keys:
            run.fail("DV5-DIFF", v4_keys[key][0],
                     "the rejected candidate's key %r reappears; the repair inverted this "
                     "claim and a document that keeps the key has kept the claim" % key)
        elif key in v3_keys:
            run.bump("rejectedPolarityKeysAbsent")

    channels = None
    for _, node in objects(art):
        for key, value in node.items():
            if re.match(r"^the[A-Z]+INSTANCESKNOWNTODAY$", key) and type(value) is list:
                channels = len(value)
    declared = art["selfMeasurement"]["manyToOneOrOneToManyChannelsClosed"]
    if channels is None:
        run.fail("DV5-DIFF", "admission.DL-INJ-1",
                 "the document names no instance list for the injectivity channels, so "
                 "its channel count is unbound")
    else:
        run.eq("DV5-DIFF", "DL-INJ-1.instancesKnownToday", channels, declared,
               "the instance list and selfMeasurement must agree, or the count is prose")


_REASON_CODE = re.compile(r"\b[A-Z][A-Z0-9_]*\.[A-Z][A-Z0-9_]+\b")


def gate_cross_position(run, art):
    """A property stated at more than one position must say the same thing twice.

    The grouping is derived: every string leaf whose KEY is a declared DL-*
    identifier, every `statement` whose PARENT key is one, and every gate
    `statement` whose text opens by naming the property.  Within a group this
    compares the set of domainReasonCodes -- machine-readable tokens a reader
    acts on -- rather than the words around them.  A negation that drops the
    reason code from one statement of a property while another statement keeps
    it is caught here and not by a byte seal.
    """
    groups = {}
    for path, value in leaves(art):
        if type(value) is not str:
            continue
        parts = [p.split("[")[0] for p in path.split(".")]
        key = parts[-1]
        if _DL_ID.match(key):
            groups.setdefault(key, []).append((path, value))
        elif key == "statement" and len(parts) >= 2 and _DL_ID.match(parts[-2]):
            groups.setdefault(parts[-2], []).append((path, value))
        elif key == "statement":
            head = value.split(".")[0].strip()
            if _DL_ID.match(head):
                groups.setdefault(head, []).append((path, value))
    for name, members in sorted(groups.items()):
        if len(members) < 2:
            run.bump("propertiesStatedAtOnePositionOnly")
            continue
        codes = {path: frozenset(_REASON_CODE.findall(text)) for path, text in members}
        distinct = set(codes.values())
        if len(distinct) != 1:
            run.fail("DV5-CROSS", name,
                     "the property is stated at %d positions and they do not name the "
                     "same domainReasonCodes: %s"
                     % (len(members),
                        "; ".join("%s -> %s" % (p, sorted(v) or "none")
                                  for p, v in sorted(codes.items()))))
        else:
            run.bump("propertiesAgreeingAcrossPositions")


def gate_pointer_resolution(run, art):
    """Intra-document pointers, RESOLVED, with unresolved ones NAMED.

    The review of the predecessor named a dangling `DL-INJ-1 boundsSTATED`
    pointer.  delivery.v4 moved boundsSTATED from DL-INJ-1 to ADM-DOMAIN and one
    prose leaf still points at the old home.  The artifact was reviewed ACCEPT and
    is not edited or re-litigated here, so this reports rather than blocks: the
    count is printed on every run and --selftest requires it not to grow.
    """
    keys = set()
    for path, _ in leaves(art):
        for part in path.split("."):
            keys.add(part.split("[")[0])
    pattern = re.compile(r"\b(DL-[A-Z]+-[0-9]+|ADM-[A-Z]+)'s ([A-Za-z][A-Za-z0-9]+)\b")
    dangling = []
    for path, value in leaves(art):
        if type(value) is not str:
            continue
        for owner, member in pattern.findall(value):
            holder = _owner_object(art, owner)
            if holder is None:
                continue
            if member in holder:
                run.bump("intraDocumentPointersResolved")
            elif member in keys:
                dangling.append("%s -> %s's %s (the member exists, but not under %s)"
                                % (path, owner, member, owner))
            else:
                dangling.append("%s -> %s's %s (no such member anywhere)"
                                % (path, owner, member))
    run.bump("danglingIntraDocumentPointers", len(dangling))
    for item in dangling:
        run.notes.append("DANGLING POINTER (reported, not a finding): %s" % item)
    return len(dangling)


def _owner_object(art, owner):
    for path, node in objects(art):
        if path.split(".")[-1].split("[")[0] == owner:
            return node
    return None


def gate_standing(run, art):
    """The standing this candidate declares, and what it must not have moved."""
    expected = {
        "artifact": "delivery.v4.json",
        "surface": "DELIVERY",
        "status": "CANDIDATE",
        "applicationState": "NOT APPLIED",
        "reviewState": "AWAITING-INDEPENDENT-REVIEW",
        "binds": "NOTHING",
        "sealRecommendation": "DO-NOT-SEAL",
    }
    for key, want in expected.items():
        if art.get(key) != want:
            run.fail("DV5-STANDING", "$." + key,
                     "declares %r, a retained candidate must declare %r"
                     % (art.get(key), want))
        else:
            run.bump("standingChecks")
    flat = json.dumps(art)
    if "[UNSET]" in flat:
        run.fail("DV5-STANDING", "$", "the artifact contains the literal [UNSET]")
    if "BLOCKED_ON_PHASE_1A" in flat and "CD-RT-5" not in flat:
        run.fail("DV5-STANDING", "$", "a disposition literal appears without its row id")
    for op in art["derivedFrom"]["operations"]:
        if op["op"] == "set" and "from" not in op:
            run.fail("DV5-STANDING", "derivedFrom.operations",
                     "a set operation restates no predecessor value")


def gate_recorded_inputs(run, art, verified):
    """Every recorded input digest, hard-compared against the LIVE file.

    The predecessor's accountability gate treated `recordedInputs` digests as
    self-declaring, so replacing one with sixty-four `f`s laundered itself: the
    value appeared in the recorded set and was therefore accounted for.  Here a
    recorded digest is accounted for only if it EQUALS the measurement, or if the
    artifact separately declares the file as drifted AND publishes that exact
    value at authoringConditions.emissionDigests.
    """
    emission = art["authoringConditions"]["emissionDigests"]
    declared_drift = {}
    for name, value in emission.items():
        declared_drift[name] = value
    for row in art["recordedInputs"]["inputs"]:
        rel = row["path"]
        recorded = row["sha256"]
        path = COOP / rel
        if not path.exists():
            run.fail("DV5-INPUT", rel, "a recorded input is absent from the tree")
            continue
        measured = sha_bytes(path.read_bytes())
        if rel in PINNED:
            # already verified before any parse; compare against the verified bytes
            measured = sha_bytes(verified[rel])
        if recorded == measured:
            run.bump("recordedInputsVerified")
            continue
        base = rel.split("/")[-1]
        if base in declared_drift and declared_drift[base] == recorded:
            run.bump("recordedInputsDECLAREDDRIFTED")
            run.notes.append(
                "recorded input %s is DECLARED drifted: recorded %s, live %s"
                % (rel, recorded[:16] + "…", measured[:16] + "…"))
            continue
        run.fail("DV5-INPUT", rel,
                 "recorded %s, measured %s, and the artifact declares no drift carrying "
                 "that value -- a recorded digest that matches neither the file nor a "
                 "declared emission digest is a value a reader is being asked to trust"
                 % (recorded, measured))
    recorded_paths = {row["path"] for row in art["recordedInputs"]["inputs"]}
    for rel in PINNED:
        if rel == SUBJECT:
            continue        # a document does not record its own digest
        if rel not in recorded_paths:
            run.fail("DV5-INPUT", rel,
                     "this checker pins an input the artifact does not record")
        else:
            row = [r for r in art["recordedInputs"]["inputs"] if r["path"] == rel][0]
            run.eq("DV5-INPUT", "recordedInputs[%s].sha256" % rel,
                   PINNED[rel], row["sha256"])


def gate_derivation(run, art, base):
    """Resolve the delta against the verified predecessor, type-exactly."""
    decl = art["derivedFrom"]
    run.eq("DV5-DERIV", "derivedFrom.artifact",
           PINNED["artifacts/delivery.v2.json"] and "delivery.v2.json", decl["artifact"])
    run.eq("DV5-DERIV", "derivedFrom.sha256",
           PINNED["artifacts/delivery.v2.json"], decl["sha256"])
    effective = copy.deepcopy(base)
    for index, op in enumerate(decl["operations"]):
        where = "derivedFrom.operations[%d] (%s %s)" % (index, op["op"], op["path"])
        steps = op["path"].split(".")
        node = effective
        ok = True
        for step in steps[:-1]:
            if type(node) is not dict or step not in node:
                run.fail("DV5-DERIV", where, "parent path does not resolve")
                ok = False
                break
            node = node[step]
        if not ok:
            continue
        leaf = steps[-1]
        if op["op"] == "set":
            if leaf not in node:
                run.fail("DV5-DERIV", where, "does not resolve against the predecessor")
                continue
            current = node[leaf]
            if not exact_equal(current, op["from"]):
                run.fail("DV5-DERIV", where,
                         "the verified predecessor holds %r (%s) but the operation "
                         "declares it replaces %r (%s)"
                         % (current, type(current).__name__,
                            op["from"], type(op["from"]).__name__))
                continue
        else:
            if leaf in node:
                run.fail("DV5-DERIV", where, "already exists in the predecessor")
                continue
        node[leaf] = copy.deepcopy(op["value"])
        run.bump("operationsApplied")
    return effective


def exact_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(exact_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def gate_contract(run, c, art, base):
    """The compiled contract, checked against the predecessor and against itself."""
    schema = base["capabilityManifestSchema"]
    for name, keys in sorted(c.records.items()):
        declared = schema.get(name, {}).get("required")
        if declared is None:
            run.fail("DV5-CONTRACT", "recordShape.%s" % name,
                     "the artifact declares a record type the predecessor's schema does "
                     "not, so its key set has no upstream witness")
            continue
        run.eq("DV5-CONTRACT", "recordShape.%s.requiredKeys" % name, list(declared), keys,
               "the record's key set must be the predecessor's own, restated exactly")
    closed_today = sorted(c.record_closure["closedTypesToday"])
    run.eq("DV5-CONTRACT", "recordClosure.closedTypesToday",
           sorted(c.records), closed_today,
           "the closed types and the declared RECORD shapes are two statements of one "
           "fact and must agree")
    map_today = sorted(c.record_closure["mapTypesToday"])
    run.eq("DV5-CONTRACT", "recordClosure.mapTypesToday", sorted(c.maps), map_today)
    for name in sorted(c.maps):
        spec = c.record_closure["mapTypesToday"].get(name, {})
        run.eq("DV5-CONTRACT", "mapTypesToday.%s.keyDomain-is-declared" % name,
               True, "keyDomain" in spec,
               "a MAP declares a KEY DOMAIN; one that declares neither a key set nor a "
               "key domain is the schema defect DL-CLOSED-1 forbids")
        # recordShape gives the bare token, recordClosure gives the token followed
        # by its justification.  The two must agree on the TOKEN, which is the
        # part this checker executes.
        declared = c.maps[name].get("valueKind", "")
        restated = str(spec.get("valueKind", "")).split(" ")[0]
        run.eq("DV5-CONTRACT", "mapTypesToday.%s.valueKind" % name, declared, restated,
               "recordShape and recordClosure state the map's value kind twice and must "
               "agree; this checker walks those values as scalars")
        if declared != "SCALAR":
            run.fail("DV5-CONTRACT", "recordShape.%s.valueKind" % name,
                     "a declared map whose values are not SCALAR makes DL-CLOSED-1's "
                     "recursive clause reachable, and this checker does not walk it")

    # --- the artifact states DL-DOM-1 and DL-CLOSED-1 at two positions each.
    # Two positions that must be equal is a binding a suffix cannot survive at one
    # of them, and the seals cover the case where both move together.
    run.eq("DV5-CONTRACT", "valueDomains stated twice",
           c.value_domains, c.identity["valueDomains"],
           "capabilityManifestSchema.valueDomains and capabilityManifestIdentity."
           "valueDomains are one block written twice and must be identical")
    run.eq("DV5-CONTRACT", "DL-CLOSED-1 stated twice",
           c.record_closure["DL-CLOSED-1"],
           c.identity["admission"]["ADM-CLOSED"]["statement"],
           "recordClosure.DL-CLOSED-1 and admission.ADM-CLOSED.statement are one property "
           "written twice")
    run.eq("DV5-CONTRACT", "DL-DOM-1 stated twice",
           c.value_domains["DL-DOM-1"],
           c.identity["admission"]["ADM-DOMAIN"]["statement"],
           "valueDomains.DL-DOM-1 and admission.ADM-DOMAIN.statement are one property "
           "written twice")

    # --- the minted domain label, spelled at four positions
    spellings = {}
    for where, text in (
            ("recipe.oneLine", c.identity["recipe"]["oneLine"]),
            ("recipe.step3_DIGEST", c.identity["recipe"]["step3_DIGEST"]),
            ("capabilityManifestId.oneLine",
             c.by_path["capabilityManifestSchema.capabilityManifestId"][0]["value"]["oneLine"]),
    ):
        found = re.search(r'UTF8\(\s*"([^"]+)"\s*\)', text)
        spellings[where] = found.group(1) if found else None
    for where, spelled in sorted(spellings.items()):
        run.eq("DV5-CONTRACT", "domainLabel at " + where, c.domain, spelled,
               "the label the closed domain vocabulary mints and the label the recipe "
               "spells must be one string")
    if c.domain_closed is not True:
        run.fail("DV5-CONTRACT", "closedDomainVocabulary.closed",
                 "the domain family does not declare itself closed, so a second label "
                 "could be minted without a successor")
    run.eq("DV5-CONTRACT", "admission.gateOrder distinct",
           len(set(c.gate_order)), len(c.gate_order))
    for name in c.gate_order:
        if name not in _GATES:
            run.fail("DV5-CONTRACT", "admission.gateOrder",
                     "the artifact declares gate %r and this checker cannot execute it, "
                     "so the gate would be prose" % name)
    if c.order_exemptions:
        run.fail("DV5-CONTRACT", "orderedCollections.orderBearingExemptions",
                 "DL-ORD-2 states this schema names NO order-bearing collection, and the "
                 "exemption list is non-empty: %r" % c.order_exemptions)
    else:
        run.bump("orderBearingExemptionsEmpty")


def gate_registries(run, c, art, samples):
    """Registry membership, DERIVED from the predecessor and resolved BY OBSERVATION.

    For each bound position this collects the values the position actually
    carries across the predecessor's four live manifests and the artifact's own
    committed vectors, then finds the candidate registry -- every one of which is
    built from delivery.v2 or fact-plane.v1, never from the subject -- that
    contains all of them.  A registry whose published members are inventions, or
    whose memberCount has been moved, or which has been rebound to a different
    vocabulary, disagrees with the resolution and is named.
    """
    observed = {}
    for manifest in samples:
        for position, value in observed_at_positions(c, manifest):
            if position in c.position_registry:
                observed.setdefault(position, set()).add(value)

    candidates = {
        "PLATFORM": set(c.candidates["_matrix"]),
        "RELATIONS": set(c.candidates["fact-plane.v1#relationRegistry.relations"]),
        "DEFICIENCY": set(c.candidates["fact-plane.v1#deficiencyVocabulary.values"]),
        "LITERAL": set(c.candidates["delivery.v2#AbsentCapability.rule, the literal"]),
    }
    # The aggregate token is not in delivery.v2's matrix and is not minted here:
    # it is recovered as the value the predecessor's own live manifests carry at
    # the platform position and the matrix does not list.
    aggregate = set()
    for position, values in observed.items():
        if position.startswith("ProviderCapability.platformIds"):
            aggregate |= (values - candidates["PLATFORM"])
    candidates["PLATFORM"] |= aggregate
    run.eq("DV5-REGISTRY", "PLATFORM-ID-DOMAIN-V1.aggregateTokenCount", 1, len(aggregate),
           "the platform domain adds exactly one aggregate token to the predecessor's "
           "matrix; a second would be a mint this document does not declare")

    derived_for = {}
    for position, values in sorted(observed.items()):
        registry = c.registries[c.position_registry[position]]
        if "members" not in registry:
            continue     # a RULE registry -- the ladder clause below carries it
        fits = sorted(name for name, members in candidates.items() if values <= members)
        if not fits:
            run.fail("DV5-REGISTRY", position,
                     "the values this position carries (%r) are in NO registry derived "
                     "from the predecessor" % sorted(values)[:6])
            continue
        if len(fits) > 1:
            run.fail("DV5-REGISTRY", position,
                     "the values this position carries are contained by %r, so the "
                     "binding does not discriminate and the corpus is degenerate at it"
                     % fits)
            continue
        derived_for[position] = fits[0]

    for name, spec in sorted(c.registries.items()):
        resolved = {derived_for.get(p) for p in spec["boundPositions"]}
        resolved.discard(None)
        if len(resolved) > 1:
            run.fail("DV5-REGISTRY", name,
                     "this registry binds positions whose observed values resolve to "
                     "DIFFERENT upstream vocabularies %r, so at least one position is "
                     "bound to the wrong registry" % sorted(resolved))
            continue
        if "members" not in spec:
            run.bump("registriesWithoutAnEnumeratedMemberSet")
            continue
        if not resolved:
            run.fail("DV5-REGISTRY", name,
                     "no bound position of this registry carries an observable value, so "
                     "its membership is unbound by anything live")
            continue
        upstream = sorted(candidates[resolved.pop()])
        run.eq("DV5-REGISTRY", "%s.members" % name, upstream, sorted(spec["members"]),
               "members are derived from the predecessor's own bytes and hard-compared")
        if "memberCount" in spec:
            run.eq("DV5-REGISTRY", "%s.memberCount" % name,
                   len(upstream), spec["memberCount"])
        else:
            run.bump("registriesPublishingNoMemberCount")
        run.eq("DV5-REGISTRY", "%s.membersAreDistinct" % name,
               len(set(spec["members"])), len(spec["members"]))

    # the relation ladder is a registry of its own, with a rule and no member list
    for position, values in sorted(observed.items()):
        if not position.endswith("relations value"):
            continue
        rungs = set()
        for spec in c.relation_ladder.values():
            rungs |= set(spec["ladder"])
        stray = sorted(values - rungs)
        if stray:
            run.fail("DV5-REGISTRY", position,
                     "resolution values %r are not rungs of any relation's ladder" % stray)
        else:
            run.bump("ladderRungsVerified")


def gate_scalar_census(run, c, samples):
    """DL-DOM-1's scalar census, DERIVED structurally rather than transcribed."""
    derived = derive_scalar_positions(c, samples)
    published_bound = sorted(c.bound_positions)
    published_open = sorted(c.declared_open)
    run.eq("DV5-CENSUS", "reachableScalarTypePositions",
           sorted(derived), sorted(set(published_bound) | set(published_open)),
           "the census is the set of positions a walk of the declared record shapes "
           "reaches over real admitted values")
    overlap = sorted(set(published_bound) & set(published_open))
    if overlap:
        run.fail("DV5-CENSUS", "valueDomains",
                 "a position is both bound and declared open: %r" % overlap)
    if len(set(published_bound)) != len(published_bound):
        run.fail("DV5-CENSUS", "valueDomains.registries[].boundPositions",
                 "a position is bound twice, so DL-DOM-1's 'no third state' has a fourth")
    run.bump("boundPositions", len(published_bound))
    run.bump("openPositions", len(published_open))


def gate_goldens(run, c, resolved_inputs, c2v4):
    """The binding-artifact oracle.  Both pinned PLAN-ID-V1 goldens."""
    positives = {v["id"]: v
                 for v in resolved_inputs["planIdContract"]["goldenVectors"]["positive"]}
    minimal = positives["planid-v1-ci-minimal"]
    pre, pid = plan_id(c, minimal["input"])
    run.eq("DV5-ORACLE", "planid-v1-ci-minimal.preimageBytes",
           len(pre), minimal["expectedPreimageByteLength"])
    run.eq("DV5-ORACLE", "planid-v1-ci-minimal.planId", pid, minimal["expectedPlanId"])

    full_vector = positives["planid-v1-ci-full-providers"]
    spec = importlib.util.spec_from_file_location(
        "_cri", str(HERE / "check-resolved-inputs.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    full = module._materialize_plan_vector(full_vector, c2v4)
    pre_full, pid_full = plan_id(c, full)
    run.eq("DV5-ORACLE", "planid-v1-ci-full-providers.preimageBytes",
           len(pre_full), full_vector["expectedPreimageByteLength"])
    run.eq("DV5-ORACLE", "planid-v1-ci-full-providers.planId",
           pid_full, full_vector["expectedPlanId"])
    return minimal["input"], full, pre, pre_full


def gate_closure_property(run, c, manifest, label):
    """DL-CLOSED-1 as a property, walked over a real admitted value."""
    stack = [(c.root, manifest)]
    while stack:
        record, obj = stack.pop()
        if record is None or type(obj) is not dict:
            run.fail("DV5-CLOSURE", label,
                     "a reachable object is neither a declared record nor a declared map; "
                     "DL-CLOSED-1 makes it inadmissible until the schema declares one")
            continue
        if sorted(obj) != sorted(c.records[record]):
            run.fail("DV5-CLOSURE", "%s / %s" % (label, record),
                     "record key set %r is not its declared %r"
                     % (sorted(obj), sorted(c.records[record])))
            continue
        run.bump("recordsClosed")
        for key in c.records[record]:
            qualified = "%s.%s" % (record, key)
            value = obj.get(key)
            if qualified in c.maps:
                for inner in (value or {}).values():
                    if type(inner) not in (str, int, bool, type(None)):
                        run.fail("DV5-CLOSURE", "%s / %s" % (label, qualified),
                                 "a declared map's value is not a scalar, so DL-CLOSED-1's "
                                 "recursive clause applies and this object is unclosed")
                run.bump("mapsWalked")
            elif qualified in c.element_type and type(value) is list:
                for element in value:
                    stack.append((c.element_type[qualified], element))


def gate_vectors(run, c, art, base):
    """Every published vector, recomputed from the recipe."""
    identity = c.identity
    vectors = identity["vectors"]["byId"]
    run.eq("DV5-COUNT", "vectors.count", len(vectors), identity["vectors"]["count"])
    profiles = base["installProfiles"]["profiles"]
    live_index = {}
    for index, profile in enumerate(profiles):
        manifest = profile.get("capabilityManifest")
        if type(manifest) is dict:
            live_index[profile.get("profileId", "")] = index
    computed = {}
    for name, vector in sorted(vectors.items()):
        try:
            committed = _vector_committed(run, c, name, vector, profiles)
            if committed is None:
                continue
            violations = admit(c, committed)
            if violations:
                run.fail("DV5-VECTOR", "%s.committed" % name,
                         "the published committed form is INADMISSIBLE: %s" % violations[0])
                continue
            gate_closure_property(run, c, committed, name)
            encoded = cve1(committed)
            run.eq("DV5-VECTOR", "%s.committedByteLength" % name,
                   len(encoded), vector["committedByteLength"])
            run.eq("DV5-VECTOR", "%s.committedBytesHex" % name,
                   encoded.hex(), vector["committedBytesHex"])
            run.eq("DV5-VECTOR", "%s.committedBytesSha256" % name,
                   sha_bytes(encoded), vector["committedBytesSha256"])
            minted = cap_manifest_id(c, committed)
            run.eq("DV5-VECTOR", "%s.capabilityManifestId" % name,
                   minted, vector["capabilityManifestId"])
            computed[name] = (minted, committed, encoded)
            if decode(encoded) != committed:
                run.fail("DV5-VECTOR", "%s.literalRoundTrip" % name,
                         "decode(encode(x)) != x on an admitted value")
            else:
                run.bump("roundTrips")
            from_hex = bytes.fromhex(vector["committedBytesHex"])
            if cve1(decode(from_hex)) != from_hex:
                run.fail("DV5-VECTOR", "%s.committedBytesHex" % name,
                         "the published hex does not re-encode to itself")
            else:
                run.bump("hexReEncodes")
        except (EncErr, EncoderDisagreement, ValueError, KeyError, TypeError,
                IndexError) as exc:
            # The predecessor let a malformed committedBytesHex raise out of this
            # loop as an unhandled traceback.  A checker that dies is a checker
            # that reported nothing.
            run.fail("DV5-VECTOR", name,
                     "raised %s while being recomputed: %s" % (type(exc).__name__, exc))
    sort_rule = vectors.get("DCM-6-sort-rule")
    if sort_rule is not None and "encodedByteSortWouldMint" in sort_rule:
        with _temporarily(MUT, "SORT_BY_ENCODED_BYTES"):
            wrong = canonicalise(c, sort_rule["authoringForm"])
        run.eq("DV5-VECTOR", "DCM-6-sort-rule.encodedByteSortWouldMint",
               cap_manifest_id(c, wrong), sort_rule["encodedByteSortWouldMint"],
               "sorting by encoded item bytes is length-major and orders ['b','aa']")
        if cap_manifest_id(c, wrong) == sort_rule["capabilityManifestId"]:
            run.fail("DV5-VECTOR", "DCM-6-sort-rule",
                     "the two sort conventions mint one id, so this vector separates "
                     "nothing")
    return computed


def _vector_committed(run, c, name, vector, profiles):
    """The committed form of a vector, from whichever source the vector declares."""
    live = {"DCM-1-core": 0, "DCM-2-typescript-deep": 1,
            "DCM-3-rust-deep": 2, "DCM-4-full": 3}
    if name in live:
        authoring = profiles[live[name]]["capabilityManifest"]
        violations = admit(c, authoring)
        run.eq("DV5-VECTOR", "%s.authoringFormViolations" % name,
               violations, vector["authoringFormViolations"],
               "the complete list under the declared traversal")
        run.eq("DV5-VECTOR", "%s.authoringFormAdmissible" % name,
               violations == [], vector["authoringFormAdmissible"])
        return canonicalise(c, authoring)
    if "authoringForm" in vector:
        committed = canonicalise(c, vector["authoringForm"])
        violations = admit(c, vector["authoringForm"])
        run.eq("DV5-VECTOR", "%s.authoringFormViolations" % name,
               violations, vector["authoringFormViolations"])
        run.eq("DV5-VECTOR", "%s.committedManifest" % name,
               committed, vector["committedManifest"],
               "canonicalise(authoringForm) must be the published committed manifest")
        return committed
    return vector["committedManifest"]


ADMITTED = "<<NO GATE REFUSED THIS VALUE>>"
PLACEHOLDER_LITERALS = ("2" * 64, "7" * 64)


def _apply_construction(c, cons, ctx, half=None):
    """Build a control's input from the construction the ARTIFACT declares."""
    kind = cons["kind"]
    if kind == "liveAuthoringForm":
        value = copy.deepcopy(ctx["profiles"][cons["profileIndex"]]["capabilityManifest"])
        transform = cons.get("transform")
        if transform == "reverseCoverageForAbsent":
            value["coverageForAbsent"] = list(reversed(value["coverageForAbsent"]))
        elif transform == "reverseProviders":
            value["providers"] = list(reversed(value["providers"]))
        elif transform is not None:
            raise KeyError("unknown construction transform %r" % transform)
        return value
    if kind == "baseManifest":
        return copy.deepcopy(ctx["control"]["baseManifest"])
    if kind == "vector":
        value = copy.deepcopy(ctx["vectors"][cons["baseVector"]]["committedManifest"])
        if half == "x2" and "x2PlatformIds" in cons:
            value["providers"][0]["platformIds"] = list(cons["x2PlatformIds"])
        elif half is None and "platformIds" in cons:
            value["providers"][0]["platformIds"] = list(cons["platformIds"])
        return value
    if kind == "coreCommitted":
        value = copy.deepcopy(ctx["core"])
        spec = cons
        if half in ("providerHalf", "absentHalf"):
            spec = cons[half]
        if "setSchemaVersion" in spec:
            token = spec["setSchemaVersion"]
            value["schemaVersion"] = {"jsonBooleanTrue": True,
                                      "jsonStringOne": "1",
                                      "jsonNumberOneDotZero": 1.0}[token]
        if "setProfile" in spec:
            value["profile"] = spec["setProfile"]
        if "setDeficiency" in spec:
            value["coverageForAbsent"][0]["deficiency"] = spec["setDeficiency"]
        if "addRelationId" in spec:
            entry = value["coverageForAbsent"][0]
            entry["relationIds"] = sorted(entry["relationIds"] + [spec["addRelationId"]])
        if "insertAt" in spec:
            where = spec["insertAt"]
            target = {"providers[0]": value["providers"][0],
                      "coverageForAbsent[0]": value["coverageForAbsent"][0]}[where]
            target[spec["key"]] = spec["value"]
        return value
    if kind == "allFourLiveCommitted":
        return None
    raise KeyError("unknown construction kind %r" % kind)


def gate_controls(run, c, base, vectors, corpus):
    """Every negative control, EXECUTED from its own declared construction, and
    each asserting the SPECIFIC NAMED CONDITION it states."""
    identity = c.identity
    controls = {ctl["id"]: ctl for ctl in identity["negativeControls"]["controls"]}
    run.eq("DV5-COUNT", "negativeControls.count", len(controls),
           identity["negativeControls"]["count"])
    profiles = base["installProfiles"]["profiles"]
    core = canonicalise(c, profiles[0]["capabilityManifest"])
    executed = set()

    def ctx_for(cid):
        return {"profiles": profiles, "core": core, "vectors": vectors,
                "control": controls[cid]}

    def build(cid, half=None):
        control = controls[cid]
        if "construction" not in control:
            run.fail("DV5-CONTROL", cid,
                     "declares no machine-readable construction, so nothing can execute it")
            return None
        return _apply_construction(c, control["construction"], ctx_for(cid), half)

    def named(cid, condition, position):
        stated = controls[cid].get("thisRule", "")
        if condition not in stated:
            run.fail("DV5-CONTROL", position,
                     "executed outcome %r is not the condition the control states (%r)"
                     % (condition, stated[:200]))
        else:
            run.bump("namedConditionsMatched")
        executed.add(cid)

    def refusal_of(value):
        errs = admit(c, value)
        return errs[0] if errs else ADMITTED

    def note(label, manifest):
        corpus.append((label, manifest))

    for cid in sorted(controls):
        if "construction" not in controls[cid]:
            run.fail("DV5-CONTROL", cid, "declares no construction")

    ord1 = build("NEG-ORD-1")
    note("NEG-ORD-1", ord1)
    named("NEG-ORD-1", " | ".join(admit(c, ord1)) or ADMITTED, "NEG-ORD-1.thisRule")
    run.eq("DV5-CONTROL", "NEG-ORD-1.orderBearingReadingWouldMint",
           cap_manifest_id(c, ord1), controls["NEG-ORD-1"]["orderBearingReadingWouldMint"])
    run.eq("DV5-CONTROL", "NEG-ORD-1.byteLengthIsNotADefence",
           len(cve1(ord1)), len(cve1(canonicalise(c, ord1))),
           "the inadmissible and the admissible form must be the same byte length, or "
           "length alone would separate the readings")

    ord2 = build("NEG-ORD-2")
    note("NEG-ORD-2", ord2)
    named("NEG-ORD-2", " | ".join(admit(c, ord2)) or ADMITTED, "NEG-ORD-2.thisRule")
    run.eq("DV5-CONTROL", "NEG-ORD-2.orderBearingReadingWouldMint",
           cap_manifest_id(c, ord2), controls["NEG-ORD-2"]["orderBearingReadingWouldMint"])
    if cve1(canonicalise(c, ord1)) != cve1(canonicalise(c, ord2)):
        run.fail("DV5-CONTROL", "NEG-ORD-2.canonicalise",
                 "the two authoring documents do not canonicalise to one byte string, so "
                 "the collision this control is about is not the one described")
    else:
        run.bump("collisionsCanonicalised")

    ord3 = build("NEG-ORD-3")
    note("NEG-ORD-3", ord3)
    full_auth = copy.deepcopy(profiles[3]["capabilityManifest"])
    executed.add("NEG-ORD-3")
    run.eq("DV5-CONTROL", "NEG-ORD-3.canonicalId",
           cap_manifest_id(c, canonicalise(c, ord3)),
           cap_manifest_id(c, canonicalise(c, full_auth)),
           "two builders disagreeing only about array order must reach ONE id")
    run.eq("DV5-CONTROL", "NEG-ORD-3.reversed", cap_manifest_id(c, ord3),
           controls["NEG-ORD-3"]["orderBearingReadingWouldMint"]["reversed"])
    run.eq("DV5-CONTROL", "NEG-ORD-3.asDeclared", cap_manifest_id(c, full_auth),
           controls["NEG-ORD-3"]["orderBearingReadingWouldMint"]["asDeclared"])

    dup1 = build("NEG-DUP-1")
    note("NEG-DUP-1", dup1)
    named("NEG-DUP-1", " | ".join(admit(c, dup1)) or ADMITTED, "NEG-DUP-1.thisRule")
    run.eq("DV5-CONTROL", "NEG-DUP-1.aDUPLICATETOLERATINGImplementationWouldMint",
           cap_manifest_id(c, dup1),
           controls["NEG-DUP-1"]["aDUPLICATETOLERATINGImplementationWouldMint"])
    deduped = copy.deepcopy(dup1)
    deduped["providers"] = [deduped["providers"][0]]
    run.eq("DV5-CONTROL", "NEG-DUP-1.aDEDUPLICATINGImplementationWouldMint",
           cap_manifest_id(c, deduped),
           controls["NEG-DUP-1"]["aDEDUPLICATINGImplementationWouldMint"])
    if (controls["NEG-DUP-1"]["aDUPLICATETOLERATINGImplementationWouldMint"]
            == controls["NEG-DUP-1"]["aDEDUPLICATINGImplementationWouldMint"]):
        run.fail("DV5-CONTROL", "NEG-DUP-1",
                 "the two published readings are the same value, so the control separates "
                 "nothing")

    dup2 = build("NEG-DUP-2")
    note("NEG-DUP-2", dup2)
    named("NEG-DUP-2", " | ".join(admit(c, dup2)) or ADMITTED, "NEG-DUP-2.thisRule")
    run.eq("DV5-CONTROL", "NEG-DUP-2.aBYTESONLYDeduplicatorWouldMint",
           cap_manifest_id(c, dup2), controls["NEG-DUP-2"]["aBYTESONLYDeduplicatorWouldMint"])

    type1 = build("NEG-TYPE-1")
    named("NEG-TYPE-1", refusal_of(type1), "NEG-TYPE-1.thisRule")
    run.eq("DV5-CONTROL", "NEG-TYPE-1.wouldMint", cap_manifest_id(c, type1),
           controls["NEG-TYPE-1"]["wouldMint"])

    type2 = build("NEG-TYPE-2")
    named("NEG-TYPE-2", refusal_of(type2), "NEG-TYPE-2.thisRule")
    run.eq("DV5-CONTROL", "NEG-TYPE-2.wouldMint", cap_manifest_id(c, type2),
           controls["NEG-TYPE-2"]["wouldMint"])

    type3 = build("NEG-TYPE-3")
    named("NEG-TYPE-3", refusal_of(type3), "NEG-TYPE-3.thisRule")
    try:
        cve1(type3)
        run.fail("DV5-CONTROL", "NEG-TYPE-3.andSECONDARILY",
                 "CVE1 encoded a float; resolved-inputs.v2 forbids floating-point outright")
    except EncErr:
        run.bump("cve1Refusals")

    closed1 = build("NEG-CLOSED-1")
    named("NEG-CLOSED-1", refusal_of(closed1), "NEG-CLOSED-1.thisRule")
    run.eq("DV5-CONTROL", "NEG-CLOSED-1.wouldMint", cap_manifest_id(c, closed1),
           controls["NEG-CLOSED-1"]["wouldMint"])
    run.eq("DV5-CONTROL", "NEG-CLOSED-1.committedByteLengthUnderTheOpenReading",
           len(cve1(closed1)),
           controls["NEG-CLOSED-1"]["committedByteLengthUnderTheOpenReading"])

    provider_half = build("NEG-CLOSED-2", "providerHalf")
    absent_half = build("NEG-CLOSED-2", "absentHalf")
    published = controls["NEG-CLOSED-2"]["underTheUNCLOSEDreadingOfThisArtifactsOwnRecipe"]
    run.eq("DV5-CONTROL", "NEG-CLOSED-2.baseline", cap_manifest_id(c, core),
           published["baseline"])
    run.eq("DV5-CONTROL", "NEG-CLOSED-2.extraKeyInProviderCapability",
           cap_manifest_id(c, provider_half), published["extraKeyInProviderCapability"])
    run.eq("DV5-CONTROL", "NEG-CLOSED-2.extraKeyInAbsentCapability",
           cap_manifest_id(c, absent_half), published["extraKeyInAbsentCapability"])
    run.eq("DV5-CONTROL", "NEG-CLOSED-2.committedByteLengths",
           [len(cve1(core)), len(cve1(provider_half)), len(cve1(absent_half))],
           published["committedByteLengths"])
    three = {cap_manifest_id(c, core), cap_manifest_id(c, provider_half),
             cap_manifest_id(c, absent_half)}
    if len(three) != 3:
        run.fail("DV5-CONTROL", "NEG-CLOSED-2.anyTwoEqual",
                 "the three documents do not mint three distinct ids")
    if not admit(c, provider_half) or not admit(c, absent_half):
        run.fail("DV5-CONTROL", "NEG-CLOSED-2.thisRule",
                 "ADM-CLOSED admitted an extra-key document")
    executed.add("NEG-CLOSED-2")

    closed3 = controls["NEG-CLOSED-3"]["measured"]
    key_sizes, per_provider, admitted_here = set(), [], 0
    for index, name in enumerate(["DCM-1-core", "DCM-2-typescript-deep",
                                  "DCM-3-rust-deep", "DCM-4-full"]):
        committed = canonicalise(c, profiles[index]["capabilityManifest"])
        if admit(c, committed) == []:
            admitted_here += 1
        for entry in committed["providers"]:
            key_sizes.add(len(entry["relations"]))
            per_provider.append([name, entry["providerId"], len(entry["relations"])])
    run.eq("DV5-CONTROL", "NEG-CLOSED-3.relationsKeySetSizes", sorted(key_sizes),
           closed3["relationsKeySetSizesAcrossTheFourLiveManifests"])
    run.eq("DV5-CONTROL", "NEG-CLOSED-3.perProviderRelationsKeyCount", per_provider,
           closed3["perProviderRelationsKeyCount"])
    run.eq("DV5-CONTROL", "NEG-CLOSED-3.admittedUnderTHISDOCUMENTSRepairedProperty",
           admitted_here, closed3["admittedUnderTHISDOCUMENTSRepairedProperty"])
    with _temporarily(MUT, "CLOSE_THE_MAP"):
        under_catch_all = sum(
            1 for index in range(4)
            if admit(c, canonicalise(c, profiles[index]["capabilityManifest"])) == [])
    run.eq("DV5-CONTROL", "NEG-CLOSED-3.admittedUnderTheCATCHALLReading",
           under_catch_all, closed3["admittedUnderTheCATCHALLReading"],
           "blocker IR-V3-B1 executed: the rejected candidate's literal catch-all refuses "
           "every live manifest, so a gate and the document's own vectors cannot both be "
           "right")
    executed.add("NEG-CLOSED-3")

    nfc = build("NEG-NFC-1")
    try:
        cve1(nfc)
        run.fail("DV5-CONTROL", "NEG-NFC-1.thisRule",
                 "a non-NFC string was encoded rather than refused")
    except EncErr:
        run.bump("cve1Refusals")
        executed.add("NEG-NFC-1")

    measured = controls["NEG-DOM-1"]["measured"]
    body = cve1(core)
    for label, want in sorted(measured.items()):
        if label == "correct":
            got = cap_manifest_id(c, core)
        elif label == "correctDomainWithoutTheNULSeparator":
            got = hashlib.sha256(c.domain.encode("utf-8") + body).hexdigest()
        else:
            got = hashlib.sha256(label.encode("utf-8") + b"\x00" + body).hexdigest()
        run.eq("DV5-CONTROL", "NEG-DOM-1.measured[%s]" % label, got, want)
    if len(set(measured.values())) != len(measured):
        run.fail("DV5-CONTROL", "NEG-DOM-1.measured", "two domain labels produced one id")
    executed.add("NEG-DOM-1")

    plat = controls["NEG-PLAT-1"]
    x1 = build("NEG-PLAT-1")
    x2 = build("NEG-PLAT-1", "x2")
    note("NEG-PLAT-1.x1", x1)
    note("NEG-PLAT-1.x2", x2)
    v3gates = plat["measuredUnderDELIVERYV3sTHREEGATES"]
    run.eq("DV5-CONTROL", "NEG-PLAT-1.idOfX1", cap_manifest_id(c, x1), v3gates["idOfX1"])
    run.eq("DV5-CONTROL", "NEG-PLAT-1.idOfX2", cap_manifest_id(c, x2), v3gates["idOfX2"])
    if cap_manifest_id(c, x1) == cap_manifest_id(c, x2):
        run.fail("DV5-CONTROL", "NEG-PLAT-1.idsDiffer",
                 "the two spellings mint one id, so the channel this control describes is "
                 "not present")
    if decode(cve1(x2)) != x2:
        run.fail("DV5-CONTROL", "NEG-PLAT-1.detectorVerdict",
                 "x2 does not round-trip, so the channel is NOT symmetric and the "
                 "artifact's claim that the DL-INJ-1 detector is silent on it is wrong")
    else:
        run.bump("symmetricChannelsConfirmed")
    with _temporarily(MUT, "SKIP_DOMAIN"):
        v3_admits_both = admit(c, x1) == [] and admit(c, x2) == []
    run.eq("DV5-CONTROL", "NEG-PLAT-1.bothAdmitted", v3_admits_both,
           v3gates["bothAdmitted"],
           "under the rejected candidate's three gates BOTH spellings must be admissible, "
           "or the channel was never open")
    named("NEG-PLAT-1", refusal_of(x2), "NEG-PLAT-1.thisRule")

    plat2 = build("NEG-PLAT-2")
    named("NEG-PLAT-2", refusal_of(plat2), "NEG-PLAT-2.thisRule")
    run.eq("DV5-CONTROL", "NEG-PLAT-2.wouldMint", cap_manifest_id(c, plat2),
           controls["NEG-PLAT-2"]["wouldMint"])

    rel1 = build("NEG-REL-1")
    named("NEG-REL-1", refusal_of(rel1), "NEG-REL-1.thisRule")
    run.eq("DV5-CONTROL", "NEG-REL-1.wouldMint", cap_manifest_id(c, rel1),
           controls["NEG-REL-1"]["wouldMint"])

    def1 = build("NEG-DEF-1")
    named("NEG-DEF-1", refusal_of(def1), "NEG-DEF-1.thisRule")
    run.eq("DV5-CONTROL", "NEG-DEF-1.wouldMint", cap_manifest_id(c, def1),
           controls["NEG-DEF-1"]["wouldMint"])

    if "SKIP_ONE_CONTROL" in MUT:
        executed.discard("NEG-DEF-1")

    missing = sorted(set(controls) - executed)
    if missing:
        run.fail("DV5-CONTROL", "negativeControls",
                 "DECLARED BUT NOT EXECUTED by this checker: %s. IMPLEMENTATION-FREEZE.md "
                 "section 7 records EPC-V2 as exactly this defect -- it declares that, and "
                 "nothing runs it" % ", ".join(missing))
    else:
        run.bump("controlsExecuted", len(executed))


def gate_corpus_distinctness(run, c, computed, corpus):
    """The artifact's OWN published corpus must be non-degenerate.

    A sibling instrument let 10 of 17 published vectors collapse to one digest at
    zero findings because it demanded distinctness only of synthetic values.  The
    property asserted here is the one the recipe claims -- injectivity -- and it
    is asserted over the published corpus, not over values this checker invented.
    """
    published = c.identity["vectors"]
    ids = {name: value[0] for name, value in computed.items()}
    byte_strings = {name: value[2] for name, value in computed.items()}
    manifests = {name: json.dumps(value[1], sort_keys=True)
                 for name, value in computed.items()}
    run.eq("DV5-DISTINCT", "publishedVectors.distinctIds",
           len(set(ids.values())), published["count"],
           "every published vector must carry its own id or the corpus separates nothing")
    run.eq("DV5-DISTINCT", "publishedVectors.distinctCommittedValues",
           len(set(manifests.values())), published["count"])
    run.eq("DV5-DISTINCT", "publishedVectors.distinctCommittedByteStrings",
           len(set(byte_strings.values())), published["count"])
    for name, encoded in sorted(byte_strings.items()):
        if ids[name] in PLACEHOLDER_LITERALS:
            run.fail("DV5-DISTINCT", "%s.capabilityManifestId" % name,
                     "equals a placeholder literal, which is evidence of back-fitting")

    # injectivity over EVERY manifest this run built, published and synthetic
    seen = {}
    collisions = []
    for label, manifest in ([(n, v[1]) for n, v in sorted(computed.items())]
                            + sorted(corpus)):
        if type(manifest) is not dict:
            continue
        try:
            key = cve1(manifest)
        except (EncErr, EncoderDisagreement):
            continue
        minted = hashlib.sha256(c.domain.encode("utf-8") + b"\x00" + key).hexdigest()
        if minted in seen and seen[minted] != key:
            collisions.append((label, minted))
        seen[minted] = key
    if collisions:
        for label, minted in collisions:
            run.fail("DV5-DISTINCT", label,
                     "two DIFFERENT committed values mint one id %s; the recipe claims "
                     "injectivity" % minted[:16])
    else:
        run.bump("injectiveOverTheWholeCorpus", len(seen))
    run.eq("DV5-DISTINCT", "selfMeasurement.committedVectorsPublished",
           len(computed), c.identity["vectors"]["count"])


def gate_derived_planids(run, c, minimal, full, pre_min, pre_full, ids):
    """The three derived PlanIds, recomputed end to end."""
    block = c.identity["planIdField3Resolution"]["step3_aPLANIDWHOSEFIELD3CAMEFROMTHERULE"]
    core_id = ids["DCM-1-core"][0]
    full_id = ids["DCM-4-full"][0]

    def diff(a, b):
        positions = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
        return len(positions), [positions[0], positions[-1]] if positions else []

    d1 = copy.deepcopy(minimal)
    d1["release"]["capabilityManifestId"] = core_id
    pre, pid = plan_id(c, d1)
    run.eq("DV5-PLANID", "PID-D1.planId", pid, block["PID-D1"]["planId"])
    run.eq("DV5-PLANID", "PID-D1.preimageBytes", len(pre), block["PID-D1"]["preimageBytes"])
    count, span = diff(pre_min, pre)
    run.eq("DV5-PLANID", "PID-D1.differingBytePositions", count,
           block["PID-D1"]["differingBytePositions"])
    run.eq("DV5-PLANID", "PID-D1.differingSpan", span, block["PID-D1"]["differingSpan"])

    d2 = copy.deepcopy(full)
    d2["release"]["capabilityManifestId"] = full_id
    for universe in d2["semanticUniverses"]:
        universe["universe"]["capabilityManifestId"] = full_id
    pre2, pid2 = plan_id(c, d2)
    run.eq("DV5-PLANID", "PID-D2.planId", pid2, block["PID-D2"]["planId"])
    run.eq("DV5-PLANID", "PID-D2.preimageBytes", len(pre2), block["PID-D2"]["preimageBytes"])
    count2, span2 = diff(pre_full, pre2)
    run.eq("DV5-PLANID", "PID-D2.differingBytePositions", count2,
           block["PID-D2"]["differingBytePositions"])
    run.eq("DV5-PLANID", "PID-D2.differingSpan", span2, block["PID-D2"]["differingSpan"])

    d3 = copy.deepcopy(full)
    d3["release"]["capabilityManifestId"] = full_id
    pre3, pid3 = plan_id(c, d3)
    run.eq("DV5-PLANID", "PID-D3.planId", pid3, block["PID-D3"]["planId"])
    run.eq("DV5-PLANID", "PID-D3.preimageBytes", len(pre3), block["PID-D3"]["preimageBytes"])
    count3, span3 = diff(pre_full, pre3)
    run.eq("DV5-PLANID", "PID-D3.differingBytePositions", count3,
           block["PID-D3"]["differingBytePositions"])
    run.eq("DV5-PLANID", "PID-D3.differingSpan", span3, block["PID-D3"]["differingSpan"])


# ------------------------------------------- the evaluated proposal's grammar
#
# delivery.v4 publishes eight ids computed under ANOTHER SURFACE'S grammar --
# plan-and-policy-identity-recipes.v2's R-A recipe -- and a 28-collection
# divergence census over it.  Those are the only values in the artifact this
# document's own recipe cannot produce, so this checker carries a second grammar
# rather than leaving eight digests and three counts unaccountable.

def _C(tag, body):
    return bytes([tag]) + len(body).to_bytes(4, "big") + body


def _proposal_record(manifest, after, label, emit):
    def order(items, tag):
        if after:
            return sorted(range(len(items)), key=lambda i: _C(tag, items[i]))
        return sorted(range(len(items)), key=lambda i: items[i])

    def provider(entry, where):
        relations = [bytes([0x60]) + _C(0x61, k.encode("utf-8")) + _C(0x62, v.encode("utf-8"))
                     for k, v in entry["relations"].items()]
        o = order(relations, 0x56)
        relation_bytes = b"".join(_C(0x56, relations[i]) for i in o)
        emit[where + ".relations"] = (relation_bytes, tuple(o), "map")
        platforms = [_C(0x59, s.encode("utf-8")) for s in entry["platformIds"]]
        op = order(platforms, 0x58)
        platform_bytes = b"".join(_C(0x58, platforms[i]) for i in op)
        emit[where + ".platformIds"] = (platform_bytes, tuple(op), "array")
        return (bytes([0x50]) + _C(0x51, entry["providerId"].encode("utf-8"))
                + _C(0x52, entry["language"].encode("utf-8"))
                + _C(0x53, entry["providerVersionSource"].encode("utf-8"))
                + _C(0x54, entry["toolchainIdentitySource"].encode("utf-8"))
                + _C(0x55, relation_bytes) + _C(0x57, platform_bytes))

    def absent(entry, where):
        ids = [_C(0x75, s.encode("utf-8")) for s in entry["relationIds"]]
        o = order(ids, 0x74)
        id_bytes = b"".join(_C(0x74, ids[i]) for i in o)
        emit[where + ".relationIds"] = (id_bytes, tuple(o), "array")
        return (bytes([0x70]) + _C(0x71, entry["providerId"].encode("utf-8"))
                + _C(0x72, entry["language"].encode("utf-8")) + _C(0x73, id_bytes)
                + _C(0x76, entry["coverageState"].encode("utf-8"))
                + _C(0x77, entry["deficiency"].encode("utf-8")))

    providers = [provider(e, "%s.providers[%d]" % (label, i))
                 for i, e in enumerate(manifest["providers"])]
    o = order(providers, 0x44)
    provider_bytes = b"".join(_C(0x44, providers[i]) for i in o)
    emit[label + ".providers"] = (provider_bytes, tuple(o), "array")
    absents = [absent(e, "%s.coverageForAbsent[%d]" % (label, i))
               for i, e in enumerate(manifest["coverageForAbsent"])]
    oa = order(absents, 0x46)
    absent_bytes = b"".join(_C(0x46, absents[i]) for i in oa)
    emit[label + ".coverageForAbsent"] = (absent_bytes, tuple(oa), "array")
    return (bytes([0x40]) + _C(0x41, str(manifest["schemaVersion"]).encode("ascii"))
            + _C(0x42, manifest["profile"].encode("utf-8"))
            + _C(0x43, provider_bytes) + _C(0x45, absent_bytes))


def _proposal_id(record):
    root = hashlib.sha256(bytes([0x00]) + len(record).to_bytes(8, "big") + record).digest()
    preimage = (bytes([0x30]) + _C(0x31, b"opensip.delivery.v1")
                + _C(0x32, b"capability-manifest-v1") + _C(0x33, root))
    return hashlib.sha256(preimage).hexdigest()


def gate_obs_census(run, c, base):
    """OBS-V4-1's census, recomputed, and the eight proposal-grammar ids."""
    block = c.identity["proposalEvaluation"][
        "aFINDINGAGAINSTTHEPROPOSALTHATITSOWNSUITEDOESNOTREACH"]
    census = block["theCENSUS"]
    profiles = base["installProfiles"]["profiles"]
    names = ["core", "typescript-deep", "rust-deep", "full"]
    before, after = {}, {}
    before_ids, after_ids, lengths = {}, {}, {}
    for index, name in enumerate(names):
        manifest = profiles[index]["capabilityManifest"]
        rb = _proposal_record(manifest, "PROPOSAL_SORT_AFTER" in MUT, name, before)
        ra = _proposal_record(manifest, True, name, after)
        before_ids[name] = _proposal_id(rb)
        after_ids[name] = _proposal_id(ra)
        lengths[name] = len(rb)
        if len(rb) != len(ra):
            run.fail("DV5-OBS", "%s recordByteLength" % name,
                     "the two conventions produce different record lengths, so the "
                     "artifact's claim that only interior bytes move is wrong")
    order_div = sorted(k for k in before if before[k][1] != after[k][1])
    byte_div = sorted(k for k in before if before[k][0] != after[k][0])
    array_only = sorted(k for k in order_div if before[k][2] == "array")
    run.eq("DV5-OBS", "OBS-V4-1.sortedCollectionsTotal", len(before),
           census["sortedCollectionsTotal"])
    run.eq("DV5-OBS", "OBS-V4-1.orderDivergenceCount", len(order_div),
           census["orderDivergenceCount"])
    run.eq("DV5-OBS", "OBS-V4-1.orderDivergentPositions", order_div,
           census["orderDivergentPositions"])
    run.eq("DV5-OBS", "OBS-V4-1.byteDivergenceCount", len(byte_div),
           census["byteDivergenceCount"])
    run.eq("DV5-OBS", "OBS-V4-1.byteDivergentPositions", byte_div,
           census["byteDivergentPositions"])
    run.eq("DV5-OBS", "OBS-V4-1.arrayOnlyOrderDivergenceCount", len(array_only),
           census["arrayOnlyOrderDivergenceCount"])
    run.eq("DV5-OBS", "OBS-V4-1.arrayOnlyOrderDivergentPositions", array_only,
           census["arrayOnlyOrderDivergentPositions"])
    measured = block["measuredIds"]
    run.eq("DV5-OBS", "OBS-V4-1.sortBeforeFraming", before_ids,
           measured["sortBeforeFraming_theProposalsStatedRule"])
    run.eq("DV5-OBS", "OBS-V4-1.sortAfterFraming", after_ids, measured["sortAfterFraming"])
    run.eq("DV5-OBS", "OBS-V4-1.recordByteLengths", lengths,
           measured["recordByteLengthsUnderBOTH"])
    run.eq("DV5-OBS", "proposalEvaluation.reproducedSetReadingIds", before_ids,
           c.identity["proposalEvaluation"]["IREPRODUCEDITBEFOREJUDGINGIT"]
           ["reproducedSetReadingIds"])
    if len(order_div) == len(byte_div):
        run.fail("DV5-OBS", "OBS-V4-1.theCORRECTION",
                 "order divergence and byte divergence are the same number, so the "
                 "correction this observation makes has no referent")
    for value in list(before_ids.values()) + list(after_ids.values()):
        run.recomputed.add(value)


_NUL_MARKS = ("|| 0x00 ||", chr(92) + "u0000') ||", chr(0) + "') ||")


def gate_prefix_census(run, c, base):
    """The prefix-form count, with its predicate, recomputed on live bytes."""
    published = c.identity["proposalEvaluation"]["whatICHANGE"][0][
        "theCOUNTOFPREFIXFORMSTATEMENTS"]
    a_paths, b_paths = [], []

    def walk(node, path):
        if type(node) is dict:
            for key, value in node.items():
                walk(value, path + "." + key)
        elif type(node) is list:
            for index, value in enumerate(node):
                walk(value, path + "[%d]" % index)
        elif type(node) is str and any(m in node for m in _NUL_MARKS):
            digest = ("PREFIX_PREDICATE_BLIND" in MUT
                      or re.search(r"(SHA-256|sha256)\s*\(\s*UTF8\(", node) is not None)
            (a_paths if digest else b_paths).append(path)

    walk(base, "$")
    run.eq("DV5-PREFIX", "predicateA.count", len(a_paths), published["countUnderPredicateA"])
    run.eq("DV5-PREFIX", "predicateA.positions", sorted(a_paths),
           published["positionsUnderPredicateA"])
    run.eq("DV5-PREFIX", "predicateB.count", len(b_paths), published["countUnderPredicateB"])
    run.eq("DV5-PREFIX", "predicateB.positions", sorted(b_paths),
           published["positionsUnderPredicateB"])
    run.eq("DV5-PREFIX", "total", len(a_paths) + len(b_paths), published["total"])


def _leaf_census(node, acc, path="$"):
    if type(node) is dict:
        for key, value in node.items():
            if type(key) is not str:
                acc["nonStringKeys"].append(path)
            _leaf_census(value, acc, path + "." + key)
    elif type(node) is list:
        for index, value in enumerate(node):
            _leaf_census(value, acc, path + "[%d]" % index)
    else:
        if "LEAF_CENSUS_BLIND" in MUT:
            if isinstance(node, bool) and isinstance(node, int):
                acc["int"].append(path)
                return
        if type(node) is bool:
            acc["bool"].append(path)
        elif type(node) is int:
            acc["int"].append(path)
        elif type(node) is float:
            acc["float"].append(path)
        elif type(node) is str:
            acc["str"] += 1
        elif node is None:
            acc["null"].append(path)
        else:
            acc["other"].append(path)


def gate_leaf_census(run, art):
    """The artifact's own non-string-leaf census, recomputed by EXACT type."""
    acc = {"str": 0, "int": [], "bool": [], "float": [], "null": [], "other": [],
           "nonStringKeys": []}
    _leaf_census(art, acc)
    published = art["leafCensus"]
    run.eq("DV5-LEAF", "leafCensus.stringLeaves", acc["str"], published["stringLeaves"])
    run.eq("DV5-LEAF", "leafCensus.integerLeaves", len(acc["int"]),
           published["integerLeaves"])
    run.eq("DV5-LEAF", "leafCensus.booleanLeaves", len(acc["bool"]),
           published["booleanLeaves"])
    run.eq("DV5-LEAF", "leafCensus.nullLeaves", len(acc["null"]), published["nullLeaves"])
    run.eq("DV5-LEAF", "leafCensus.floatLeaves", len(acc["float"]), published["floatLeaves"])
    run.eq("DV5-LEAF", "leafCensus.nonStringKeys", len(acc["nonStringKeys"]),
           published["nonStringKeys"])
    run.eq("DV5-LEAF", "leafCensus.nonStringLeafTotal",
           len(acc["int"]) + len(acc["bool"]) + len(acc["null"]) + len(acc["float"]),
           published["nonStringLeafTotal"])
    run.eq("DV5-LEAF", "leafCensus.integerLeafPaths", acc["int"],
           published["integerLeafPaths"])
    run.eq("DV5-LEAF", "leafCensus.booleanLeafPaths", acc["bool"],
           published["booleanLeafPaths"])
    if acc["float"]:
        run.fail("DV5-LEAF", acc["float"][0],
                 "a float leaf in an artifact that publishes CVE1 preimages, and CVE1 "
                 "forbids floating-point outright")
    if acc["other"]:
        run.fail("DV5-LEAF", acc["other"][0], "a leaf outside JSON's value types")


def gate_self_measurement(run, c, art):
    """Every number in selfMeasurement, recomputed from what it describes."""
    sm = art["selfMeasurement"]
    ops = art["derivedFrom"]["operations"]
    duds = c.by_path["declaredUnresolvedDependencies"][0]["value"]
    expect = {
        "operations": len(ops),
        "setOperations": sum(1 for o in ops if o["op"] == "set"),
        "addOperations": sum(1 for o in ops if o["op"] == "add"),
        "committedVectorsPublished": len(c.identity["vectors"]["byId"]),
        "negativeControlsExecuted": len(c.identity["negativeControls"]["controls"]),
        "admissionGates": len(c.gate_order),
        "scalarPositionsBOUNDToARegistry": len(c.bound_positions),
        "scalarPositionsDECLAREDOPEN": len(c.declared_open),
        "reachableScalarTypePositions": len(c.bound_positions) + len(c.declared_open),
        "declaredUnresolvedDependencies": len(duds["entries"]),
        "reachableObjectTypes": len(c.records) + len(c.maps),
        "reachableObjectTypesThatAreRECORDS": len(c.records),
        "reachableObjectTypesThatAreMAPS": len(c.maps),
        "retainedCheckers": len(c.by_path) and sm["retainedCheckers"],
    }
    for key, want in sorted(expect.items()):
        run.eq("DV5-COUNT", "selfMeasurement." + key, want, sm[key])
    for key in ("rowsClosedByThisDocument", "headsRepointed", "dispositionsChanged"):
        if sm[key] != 0:
            run.fail("DV5-COUNT", "selfMeasurement." + key,
                     "a candidate that binds nothing must report 0, reports %r" % sm[key])
    ids = [d["id"] for d in duds["entries"]]
    if len(set(ids)) != len(ids):
        run.fail("DV5-COUNT", "declaredUnresolvedDependencies", "duplicate DUD id")


def gate_digest_accountability(run, art, raw_text):
    """No 64-hex literal in the artifact is unrecomputed and undeclared.

    raw_text is the VERIFIED subject text, threaded down from verify_pins.  The
    predecessor re-read the subject from disk here, after having verified it: a
    checker that re-reads after verifying has a window.
    """
    present = set(_HEX64.findall(raw_text))
    declared = set()
    block = art.get("digestAccountability")
    if block is None:
        run.fail("DV5-ACCOUNT", "$.digestAccountability",
                 "the artifact declares no digest-accountability block, so this gate "
                 "cannot distinguish a quoted foreign digest from an unrecomputed one")
        return
    for row in block["quotedFromAnotherDocumentAndNOTREPUBLISHED"]:
        declared.add(row["value"])
    for row in block["measuredByThisLaneAndNOTRECOMPUTABLELATER"]:
        declared.add(row["value"])
    # A recorded input digest counts as accounted for ONLY because
    # gate_recorded_inputs hard-compared it against the live file or against a
    # declared emission digest.  The predecessor admitted the recorded set
    # unconditionally, which is how sixty-four `f`s laundered themselves.
    recorded = set()
    for row in art["recordedInputs"]["inputs"]:
        rel = row["path"]
        path = COOP / rel
        if not path.exists():
            continue
        live = sha_bytes(path.read_bytes())
        emission = art["authoringConditions"]["emissionDigests"]
        base = rel.split("/")[-1]
        if row["sha256"] == live or emission.get(base) == row["sha256"]:
            recorded.add(row["sha256"])
    recorded |= set(PINNED.values())
    unaccounted = sorted(present - run.recomputed - declared - recorded)
    if unaccounted:
        for value in unaccounted:
            index = raw_text.index(value)
            context = raw_text[max(0, index - 120):index].splitlines()[-1][-90:]
            run.fail("DV5-ACCOUNT", value,
                     "neither recomputed by this run, nor a verified recorded input "
                     "digest, nor declared at digestAccountability. Context: ...%s"
                     % context)
    else:
        run.bump("digestsAccountedFor", len(present))
    stale = sorted(declared - present)
    if stale:
        run.fail("DV5-ACCOUNT", "digestAccountability",
                 "declares %d digest(s) that no longer appear in the artifact: %s"
                 % (len(stale), ", ".join(h[:16] + "…" for h in stale)))


# --------------------------------------------------------------------- the run
def guard(run, name, fn, *args):
    """Run one gate.  A gate that RAISES becomes a finding naming the gate.

    The predecessor let a malformed committedBytesHex raise an unhandled EncErr
    out of gate_vectors, and a checker that dies is a checker that reported
    nothing.  Every gate below is called through here, so a mutation that
    corrupts a declaration this checker compiles from cannot silence the run --
    it names the gate that could not complete.
    """
    try:
        return fn(run, *args)
    except Exception as exc:                          # noqa: BLE001 - reported, not raised
        run.fail("DV5-RAISED", name,
                 "the gate could not complete on this artifact: %s: %s"
                 % (type(exc).__name__, exc))
        return None


def load_sources(verified):
    """Whitespace-normalised text of every document a quotation can name.

    THE SUBJECT IS EXCLUDED.  A document is never the source of its own verbatim
    quotation of another document, and admitting it makes the gate
    self-satisfying: a fabricated quotation is trivially present in the file that
    fabricated it.  This exclusion was put here because the external review
    driver -- which re-points PINNED at a scratch copy, so the subject's own
    bytes become one of the verified inputs -- showed the FABRICATE_LAW_2
    mutation escaping without it.
    """
    sources = {}
    for rel, raw in verified.items():
        if rel == SUBJECT:
            continue
        sources[rel.split("/")[-1]] = norm_text(raw.decode("utf-8"))
    for name in UNPINNED_SOURCES:
        path = COOP / name
        if path.exists():
            sources[name] = norm_text(path.read_text(encoding="utf-8"))
    return sources


def run_all(verified, subject_raw=None, verbose=False):
    run = Run(verbose)
    raw = subject_raw if subject_raw is not None else verified[SUBJECT]
    raw_text = raw.decode("utf-8")
    art = parse_json(raw, SUBJECT)
    base = parse_json(verified["artifacts/delivery.v2.json"], "delivery.v2.json")
    candidate = parse_json(verified["artifacts/delivery.v3.json"], "delivery.v3.json")
    resolved = parse_json(verified["artifacts/resolved-inputs.v2.json"],
                          "resolved-inputs.v2.json")
    fact = parse_json(verified["artifacts/fact-plane.v1.json"], "fact-plane.v1.json")
    c2v4 = parse_json(verified["artifacts/c2-plan-stage-schema.v4.json"],
                      "c2-plan-stage-schema.v4.json")

    guard(run, "gate_duplicate_key_hook", gate_duplicate_key_hook)
    guard(run, "gate_statement_seals", gate_statement_seals, art)
    guard(run, "gate_quotations", gate_quotations, art, load_sources(verified))
    guard(run, "gate_rejected_candidate_differential",
          gate_rejected_candidate_differential, art, candidate)
    guard(run, "gate_cross_position", gate_cross_position, art)
    guard(run, "gate_pointer_resolution", gate_pointer_resolution, art)
    guard(run, "gate_standing", gate_standing, art)
    guard(run, "gate_recorded_inputs", gate_recorded_inputs, art, verified)
    guard(run, "gate_derivation", gate_derivation, art, base)

    try:
        c = Contract(art, base, fact, resolved, run)
    except (ContractError, KeyError, TypeError, IndexError) as exc:
        run.fail("DV5-CONTRACT", "$",
                 "this checker could not compile the contract from the artifact: %s: %s"
                 % (type(exc).__name__, exc))
        guard(run, "gate_leaf_census", gate_leaf_census, art)
        guard(run, "gate_digest_accountability", gate_digest_accountability, art, raw_text)
        return run

    live = [p["capabilityManifest"] for p in base["installProfiles"]["profiles"]
            if type(p.get("capabilityManifest")) is dict]
    vectors = c.identity["vectors"]["byId"]
    samples = list(live)
    for vector in vectors.values():
        for key in ("committedManifest", "authoringForm"):
            if type(vector.get(key)) is dict:
                samples.append(vector[key])
    guard(run, "Contract.compile_shapes", lambda r: c.compile_shapes(samples, fact, r))

    guard(run, "gate_contract", gate_contract, c, art, base)
    guard(run, "gate_registries", gate_registries, c, art, samples)
    guard(run, "gate_scalar_census", gate_scalar_census, c, samples)
    goldens = guard(run, "gate_goldens", gate_goldens, c, resolved, c2v4)
    computed = guard(run, "gate_vectors", gate_vectors, c, art, base) or {}
    corpus = []
    guard(run, "gate_controls", gate_controls, c, base, vectors, corpus)
    guard(run, "gate_corpus_distinctness", gate_corpus_distinctness, c, computed, corpus)
    if goldens and "DCM-1-core" in computed and "DCM-4-full" in computed:
        minimal, full, pre_min, pre_full = goldens
        guard(run, "gate_derived_planids", gate_derived_planids, c, minimal, full,
              pre_min, pre_full, computed)
    guard(run, "gate_self_measurement", gate_self_measurement, c, art)
    guard(run, "gate_obs_census", gate_obs_census, c, base)
    guard(run, "gate_prefix_census", gate_prefix_census, c, base)
    guard(run, "gate_leaf_census", gate_leaf_census, art)
    guard(run, "gate_digest_accountability", gate_digest_accountability,
          art, raw_text)
    return run


# ---------------------------------------------------------------- the selftest
def _json_escape(s):
    return json.dumps(s)[1:-1]


def _subject_edit(raw, replacements):
    """Edit the SUBJECT'S BYTES the way a reviewer with a scratch copy does."""
    text = raw.decode("utf-8")
    for old, new in replacements:
        if old not in text:
            raise KeyError("mutation anchor not found in the subject: %r" % old[:80])
        text = text.replace(old, new)
    return text.encode("utf-8")


def _statement(art, path):
    return _resolve_leaf(art, path)


def _resolve_leaf(root, path):
    for candidate, value in leaves(root):
        if candidate == path:
            return value
    raise KeyError(path)


def build_artifact_mutations(verified):
    """Shape-preserving, meaning-INVERTING edits to the subject's own bytes.

    Section 7.8 records that all four instruments of that session fired on
    REMOVAL and stayed silent on FALSITY.  Not one mutation below deletes
    anything: each keeps the key, keeps the type, keeps the position, and makes
    the statement false.  Nine of them are the escape list from the review that
    rejected the predecessor, reproduced exactly.
    """
    art = parse_json(verified[SUBJECT], SUBJECT)
    v3 = parse_json(verified["artifacts/delivery.v3.json"], "delivery.v3.json")
    v3_closed = v3["derivedFrom"]["operations"][10]["value"]["DL-CLOSED-1"]
    v4_closed = art["derivedFrom"]["operations"][10]["value"]["DL-CLOSED-1"]
    identity = art["derivedFrom"]["operations"][17]["value"]
    v4_dom = art["derivedFrom"]["operations"][11]["value"]["DL-DOM-1"]
    v4_ord = art["derivedFrom"]["operations"][8]["value"]["DL-ORD-1"]
    detector = art["derivedFrom"]["operations"][10]["value"]["detector"]
    ground = identity["orderingRuling"]["whereTheRuleComesFrom"][
        "leg4_theCORPUSFORBIDSANUNDECLAREDEMISSIONORDERFROMENTERINGPlanId"]["theGROUND"]
    quoted = _SPAN.search(ground)
    law2 = quoted.group(1) if quoted else ""
    members = art["derivedFrom"]["operations"][11]["value"]["registries"][
        "PLATFORM-ID-DOMAIN-V1"]["members"]

    def sub(old, new):
        return (_json_escape(old), _json_escape(new))

    negated_dom = (
        "A SCALAR IN A COMMITTED CapabilityManifestV1 MAY BE BOUND TO A NAMED REGISTRY, "
        "AND WHERE NO REGISTRY IS NAMED THE POSITION IS UNCONSTRAINED. A bound scalar is "
        "admitted if its value resembles a member of its registry, compared case-"
        "insensitively after trimming, with aliases and prefix matches admitted. A "
        "position that names no registry is open by default and needs no declaration.")
    negated_ord = (
        "Every ordered collection in a COMMITTED CapabilityManifestV1 may be in any "
        "order -- a consumer sorts it into its declared canonical order on receipt. A "
        "committed manifest that is not already sorted is ACCEPTED and normalised. "
        "Canonicalisation is a consumer act performed on every read.")
    reversed_detector = (
        "decode(encode(x)) == x, LITERALLY, for every admitted x. This one equation "
        "fails on the ORDERING channel, on the UNDECLARED-MEMBER channel AND on the "
        "VALUE-DOMAIN channel, so it also finds the third one and no separate value-"
        "domain declaration is needed. MEASURED true on 7 of 7 committed vectors.")
    fabricated_law2 = (
        "Resolution uses neutralise/key/forbid. Any input a release builder emits may "
        "affect `PlanId`; CI reads layer 4 when it must.")
    invented_members = ["all-supported", "linux-x86_64-gnu", "linux-aarch64-gnu",
                        "macos-aarch64", "macos-x86_64", "windows-x86_64-msvc",
                        "windows-aarch64-msvc", "solaris-sparc-v9"]

    mutations = [
        ("V3_CLOSED_TEXT",
         "delivery.v3's REJECTED DL-CLOSED-1 text is restored -- the exact bytes of the "
         "blocker delivery.v4 was written to repair. This is THE case that made the "
         "predecessor exit 0 with FINDINGS: 0.",
         [sub(v4_closed, v3_closed)]),
        ("NEGATE_DL_DOM_1",
         "DL-DOM-1 is replaced by its negation: bound scalars compared case-insensitively "
         "with aliases, and an unnamed position open by default.",
         [sub(v4_dom, negated_dom)]),
        ("NEGATE_DL_ORD_1",
         "DL-ORD-1 is replaced by its negation: a consumer sorts an unsorted committed "
         "manifest into shape instead of rejecting it.",
         [sub(v4_ord, negated_ord)]),
        ("REVERSE_DL_INJ_1_DETECTOR",
         "the DL-INJ-1 detector claim is reversed back to the overclaim delivery.v4 "
         "corrected: the round-trip equation 'also finds the third one'.",
         [sub(detector, reversed_detector)]),
        ("FABRICATE_LAW_2",
         "the artifact's own verbatim quotation of IMPLEMENTATION-FREEZE.md section 6 "
         "law 2 is replaced by a fabrication that says the opposite.",
         [sub(law2, fabricated_law2)]),
        ("MEMBER_COUNT_99",
         "PLATFORM-ID-DOMAIN-V1.memberCount is moved from 8 to 99 while the member list "
         "is left exactly as it was.",
         [('"memberCount": 8', '"memberCount": 99')]),
        ("INVENT_REGISTRY_MEMBERS",
         "a registry member is replaced by an invention -- linux-x86_64-musl becomes "
         "solaris-sparc-v9 -- keeping the count and the shape.",
         [(_json_escape(members[-1]), _json_escape(invented_members[-1]))]),
        ("REBIND_RELATION_IDS",
         "AbsentCapability.relationIds[] is rebound to the deficiency vocabulary and "
         "AbsentCapability.deficiency to the relation registry -- the two boundPositions "
         "are SWAPPED, so every list keeps its length and its shape.",
         [('"AbsentCapability.relationIds[]"', '"<<SWAP>>"'),
          ('"AbsentCapability.deficiency"', '"AbsentCapability.relationIds[]"'),
          ('"<<SWAP>>"', '"AbsentCapability.deficiency"')]),
        ("MOVE_DOMAIN_LABEL",
         "the minted domain label is changed at the closed vocabulary that mints it, "
         "leaving the recipe's three spellings of it alone.",
         [('"opensip.capability-manifest.v1"\n',
           '"opensip.capability-manifest.v2"\n')]),
        ("INPUT_DIGEST_ALL_F",
         "a recordedInputs digest is replaced by sixty-four `f`s -- the value that "
         "laundered itself through the predecessor's accountability gate.",
         [("9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d", "f" * 64)]),
        ("APPEND_REVERSAL",
         "every needle is preserved and a reversing sentence is APPENDED to DL-CLOSED-1, "
         "DL-DOM-1 and DL-ORD-1 -- the technique that defeats containment binding at 80 "
         "positions in versioning-policy.v10's published measurement.",
         [sub(v4_closed, v4_closed + " None of the above applies to any object this "
                                    "schema does not explicitly enumerate."),
          sub(v4_dom, v4_dom + " A position with no registry is nonetheless admissible."),
          sub(v4_ord, v4_ord + " A consumer MAY sort a non-canonical manifest.")]),
        ("COLLAPSE_VECTOR_IDS",
         "two published vectors are made to carry ONE capabilityManifestId, the "
         "degeneracy that let 10 of 17 vectors collapse to one digest in a sibling.",
         [(_json_escape(identity["vectors"]["byId"]["DCM-2-typescript-deep"]
                        ["capabilityManifestId"]),
           _json_escape(identity["vectors"]["byId"]["DCM-1-core"]
                        ["capabilityManifestId"]))]),
        ("DROP_A_SORT_KEY",
         "a declared sort key is retargeted from providerId to language, which keeps the "
         "shape of the declaration and changes what canonicalisation means.",
         [('"CapabilityManifestV1.providers": "providerId, unique"',
           '"CapabilityManifestV1.providers": "language, unique"')]),
        ("RECORD_KEY_SET_DRIFT",
         "a declared record key set names a key the predecessor's schema does not "
         "declare, keeping the list's length and every other member.",
         [('"providerVersionSource",\n        "toolchainIdentitySource",\n        '
           '"relations",',
           '"providerVersionSource",\n        "toolchainIdentity",\n        '
           '"relations",')]),
    ]
    return mutations


CODE_MUTATIONS = [
    ("EXACT_TYPE_OFF",
     "ADM-TYPE admits by isinstance, so Python's bool passes the integer gate",
     "NEG-TYPE-1"),
    ("SKIP_ORDER",
     "ADM-ORDER is skipped, so the non-canonical live authoring forms are admitted",
     "DCM-1-core"),
    ("SKIP_DOMAIN",
     "ADM-DOMAIN is skipped, so the case-variant platformId is admitted",
     "NEG-PLAT-1"),
    ("CLOSE_THE_MAP",
     "DL-CLOSED-1 is read as the rejected candidate's catch-all, so the relations MAP is "
     "required to declare a key set and every live manifest is refused -- blocker IR-V3-B1",
     "DCM-1-core"),
    ("NO_NUL",
     "the 0x00 domain separator is dropped from the preimage",
     "capabilityManifestId"),
    ("SORT_BY_ENCODED_BYTES",
     "collections are sorted by encoded item bytes, which is length-major, instead of by "
     "the declared sort key",
     "DCM-1-core"),
    ("NO_CANONICALISE",
     "the live authoring forms are encoded as written instead of canonicalised",
     "DCM-1-core"),
    ("NFC_NORMALISE",
     "the encoder silently NFC-normalises instead of refusing",
     "NEG-NFC-1"),
    ("FLOAT_ADMITTED",
     "the encoder encodes a float, which resolved-inputs.v2 forbids outright",
     "NEG-TYPE-3"),
    ("DUP_KEY_HOOK_OFF",
     "the duplicate-key hook admits a duplicate instead of naming it",
     "duplicate-key probe"),
    ("SKIP_ONE_CONTROL",
     "one declared negative control is not executed -- the EPC-V2 defect",
     "negativeControls"),
    ("LEAF_CENSUS_BLIND",
     "the leaf walk counts booleans as integers, as an isinstance walk would",
     "leafCensus"),
    ("MANGLE_QUOTE",
     "a verbatim quotation is spelled differently from the source it names",
     "DV5-QUOTE"),
    ("PROPOSAL_SORT_AFTER",
     "the evaluated proposal's grammar is built under sort-AFTER-framing where its own "
     "stated rule is sort-BEFORE-framing",
     "OBS-V4-1"),
    ("PREFIX_PREDICATE_BLIND",
     "the prefix-form census drops the SHA-256-in-the-same-sentence half of its predicate",
     "DV5-PREFIX"),
    ("NO_RECOMPUTE_LEDGER",
     "the run stops recording which digests it recomputed -- what a checker that compared "
     "stored strings to stored strings would look like from the outside",
     "DV5-ACCOUNT"),
    ("SUBJECT_DRIFT",
     "the subject's live bytes no longer match the digest this checker pins, which must "
     "stop the run at exit 2 BEFORE anything is parsed",
     "artifacts/delivery.v4.json"),
]


def _codes(findings):
    out = []
    for finding in findings:
        code = finding.split(" at ", 1)[0]
        if code not in out:
            out.append(code)
    return out


def selftest(verified):
    print("SELFTEST -- two suites.")
    print()
    print("SUITE A -- ARTIFACT MUTATIONS.  Each edits the SUBJECT'S BYTES, keeps the")
    print("shape and INVERTS THE MEANING, and must fail the run.  Section 7.8 records")
    print("that four instruments fired on removal and stayed silent on falsity; nothing")
    print("below removes anything.  `codes` is what the run raises; `withoutSeals` is")
    print("what it raises with the statement seals disabled, which shows which mutations")
    print("a semantic gate catches on its own.")
    print()
    ok = True
    for name, description, replacements in build_artifact_mutations(verified):
        MUT.clear()
        try:
            mutated = _subject_edit(verified[SUBJECT], replacements)
        except KeyError as exc:
            print("  FAIL %-26s could not be applied: %s" % (name, exc))
            ok = False
            continue
        try:
            run = run_all(verified, subject_raw=mutated)
            findings = run.findings
        except Exception as exc:                      # noqa: BLE001 - reported, not raised
            findings = ["DV5-RAISED at %s: %s: %s" % (name, type(exc).__name__, exc)]
        MUT.add("SEALS_OFF")
        try:
            bare = run_all(verified, subject_raw=mutated).findings
        except Exception as exc:                      # noqa: BLE001
            bare = ["DV5-RAISED at %s: %s: %s" % (name, type(exc).__name__, exc)]
        MUT.clear()
        status = "PASS" if findings else "FAIL"
        if not findings:
            ok = False
        print("  %-4s %-26s %3d finding(s)   codes=%s"
              % (status, name, len(findings), ",".join(_codes(findings)) or "NONE"))
        print("       %s" % description)
        print("       withoutSeals: %3d finding(s)   codes=%s"
              % (len(bare), ",".join(_codes(bare)) or "NONE"))
        if findings:
            print("       first: %s" % findings[0][:160])
        print()

    print("SUITE B -- CODE MUTATIONS.  Each disables one property of this checker and")
    print("must fail the run FOR ITS OWN NAMED REASON.")
    print()
    for flag, description, expected in CODE_MUTATIONS:
        MUT.clear()
        MUT.add(flag)
        try:
            if flag == "SUBJECT_DRIFT":
                findings, _ = verify_pins()
            else:
                findings = run_all(verified).findings
        except Exception as exc:                      # noqa: BLE001
            findings = ["%s raised %s: %s" % (flag, type(exc).__name__, exc)]
        MUT.clear()
        hit = [f for f in findings if expected in f]
        status = "PASS" if (findings and hit) else "FAIL"
        if status == "FAIL":
            ok = False
        print("  %-4s %-24s %3d finding(s); expected position %r %s"
              % (status, flag, len(findings), expected, "seen" if hit else "NOT SEEN"))
        print("       %s" % description)
        if hit:
            print("       first matching: %s" % hit[0][:150])
        elif findings:
            print("       first: %s" % findings[0][:150])
        print()

    MUT.clear()
    clean = run_all(verified)
    print("  %-4s %-24s %d finding(s) with no mutation applied"
          % ("PASS" if not clean.findings else "FAIL", "<unmutated>", len(clean.findings)))
    if clean.findings:
        ok = False
        for finding in clean.findings[:8]:
            print("       %s" % finding)
    print()
    print("SELFTEST %s -- %d artifact mutations, %d code mutations"
          % ("OK" if ok else "FAILED",
             len(build_artifact_mutations(verified)), len(CODE_MUTATIONS)))
    return 0 if ok else 1


def append_census(verified):
    """MEASURE what appending a false sentence still gets past this checker.

    The whole-file pin is neutralised for the duration, because that is the
    posture the review that rejected the predecessor worked in.  Every string
    leaf of the subject is extended by one false sentence in turn and the whole
    run is re-executed.  The number printed is a MEASUREMENT of this
    instrument's residual, not a claim about it.
    """
    art = parse_json(verified[SUBJECT], SUBJECT)
    text = verified[SUBJECT].decode("utf-8")
    sentence = " This clause is void and the property above does not hold."
    admitted, refused, unreachable = [], [], []
    seen = set()
    for path, value in leaves(art):
        if type(value) is not str or not value or value in seen:
            continue
        seen.add(value)
        # Replace the COMPLETE JSON string token, so a short leaf cannot be
        # rewritten inside a longer one.  A value written at more than one
        # position moves at every one of them, which is the honest form of the
        # attack against a document that states a property twice.
        old = '"%s"' % _json_escape(value)
        if old not in text:
            unreachable.append(path)
            continue
        mutated = text.replace(old, '"%s"' % _json_escape(value + sentence))
        try:
            findings = run_all(verified, subject_raw=mutated.encode("utf-8")).findings
        except Exception:                             # noqa: BLE001
            findings = ["raised"]
        (refused if findings else admitted).append(path)
    total = len(refused) + len(admitted) + len(unreachable)
    print("APPEND CENSUS -- one false sentence appended to each distinct string leaf in")
    print("turn, with the whole-file pin neutralised (the reviewer's scratch-copy")
    print("posture).  A leaf written at more than one position is appended to at every")
    print("one of them, so this measures the attack at its strongest.")
    print()
    print("  distinct string leaf values in the subject   %d" % total)
    print("  leaves at which the run RAISES a finding     %d" % len(refused))
    print("  leaves at which the append is ADMITTED       %d" % len(admitted))
    print("  leaves this census could not reach           %d" % len(unreachable))
    print()
    print("  The admitted set is FREE NARRATIVE PROSE: rationale, objection, residual")
    print("  and commentary leaves that no gate computes over.  Closing it would need a")
    print("  machine-checkable schema for narrative justification, which this corpus")
    print("  does not have -- the same boundary versioning-policy.v10 publishes.  Every")
    print("  NORMATIVE position -- the DL-* properties, the admission gates, the")
    print("  machine forms, the quotations -- is in the refused set.")
    print()
    if admitted:
        print("  admitted positions (the measured residual):")
        for path in admitted:
            print("    %s" % path)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true",
                        help="run the mutation suites instead of the check")
    parser.add_argument("--append-census", action="store_true",
                        help="measure the append-a-false-sentence residual")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print("CHECK-DELIVERY-V5 -- artifacts/delivery.v4.json, recomputed from the recipe")
    print()
    try:
        drift, verified = verify_pins()
    except Drift as exc:
        print("  INPUT DRIFT: %s" % exc)
        print()
        print("EXIT 2 -- refusing to parse bytes this checker has not verified.")
        return 2
    if drift:
        print("  INPUT DRIFT, before any parse:")
        for item in drift:
            print("    %s" % item)
        print()
        print("EXIT 2 -- a report about bytes nobody named is not a report.")
        return 2
    print("  hash-verified before parsing: %d inputs" % len(PINNED))
    for rel in sorted(PINNED):
        print("    %s  %s" % (PINNED[rel][:16] + "…", rel))
    print()

    if args.selftest:
        return selftest(verified)
    if args.append_census:
        return append_census(verified)

    run = run_all(verified, verbose=args.verbose)
    print("  measured this run:")
    for key in sorted(run.counts):
        print("    %-42s %d" % (key, run.counts[key]))
    print()
    if run.notes:
        print("  reported, not asserted:")
        for note in run.notes:
            print("    %s" % note)
        print()
    if not run.findings:
        print("FINDINGS: 0")
        print()
        print("EXIT 0 -- every census constant was re-derived from the artifact and its")
        print("verified predecessor, every published id, byte length, hex string, PlanId")
        print("and count was recomputed from the recipe, every normative statement was")
        print("sealed at a derived position, every verbatim quotation was verified against")
        print("the document it names, and the published corpus is pairwise distinct.")
        return 0
    print("FINDINGS: %d" % len(run.findings))
    for finding in run.findings:
        print("  %s" % finding)
    print()
    print("EXIT 1 -- see above; each finding names its position.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
