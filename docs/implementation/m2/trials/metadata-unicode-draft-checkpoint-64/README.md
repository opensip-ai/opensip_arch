# Private metadata Unicode15 compatibility64

Exact290-file unaccepted62 parent;293 current pins,288 unchanged,two security source changes,one private module/two fixtures added. Lockfile and identity sources unchanged. Proposed inventory38/profile clarification depend on pending earlier candidates. This corrects a real Unicode15-reference/Unicode16-dependency discrepancy found by63 without changing product identity. No authority type or current trust is introduced.

707 unassigned-codepoint ranges derive from exact existing Unicode15 UnicodeData; all1112064 scalar assignments and NFC outputs compared to selected Python3.12/UCD15. Unassigned scalars are class-zero boundaries; spans use existing exact Unicode16 normalization engine under UAX15 section11.3 stability rules. A compile-time engine-version assertion requires requalification on upgrade.19,074 Unicode15 normalization rows exercise five forms each;9264 actual primary-reference metadata cases exercise values,keys and collision behavior. These are bounded conformance evidence, not a full arbitrary-string proof.

Initial illustrative regression incorrectly expected equal-class marks to reorder; preserved failed test and beforeimage. Corrected the example to descending combining classes; production adapter and independently generated expectations unchanged. Package17 tests/strict workspace lint passed. Freshhost31 COMPLETE173sources/40archives; build/tests/doctests/metadata/help/version passed,160totalRusttests. No independent reviewer assent or installation.

Primary sources: https://www.unicode.org/Public/15.0.0/ucd/NormalizationTest.txt and https://www.unicode.org/reports/tr15/tr15-53.html#Guaranteeing_Process_Stability . Metadata UCD15 source license remains tools/unicode/LICENSE.
