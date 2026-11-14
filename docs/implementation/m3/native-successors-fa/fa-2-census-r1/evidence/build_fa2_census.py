#!/usr/bin/env python3
"""Build and check FA2-CENSUS-r1, the FA-2 contract successor that states the
symbol-census population rules of errata FA2-CENSUS-E1, -E2 and -E3 in
native-evidence section 9.8.

Usage (from any directory; standard library only):

    python3 -I -B build_fa2_census.py [--root ARCH] [--check]

ARCH is the architecture checkout (default: six directories above this file's
directory). Without --check the script writes section-9-8.md, successor.json and
the subject manifest; with --check it writes nothing and exits 1 if any of them
differs from the bytes it would write. Every input is checked against its pinned
size and sha256 first, so the output is a function of pinned bytes only.

The script is evidence, not law. `stated_rules` below is a reference reader of
the stated-rules block for the host generator's author (unit CR1b-LOCK); the
syntax it reads is the one section 9.8 states.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

UNIT_DIR = "docs/implementation/m3/native-successors-fa/fa-2-census-r1"
RECORD = f"{UNIT_DIR}/successor.json"
SECTION = f"{UNIT_DIR}/section-9-8.md"
README = f"{UNIT_DIR}/README.md"
SCRIPT = f"{UNIT_DIR}/evidence/build_fa2_census.py"
SUBJECT = "docs/implementation/m3/native-successors-fa/fa-2-census-r1-subject.json"

NE = {"path": "docs/v2/contracts/product-v1/native-evidence.md", "bytes": 329013,
      "sha256": "83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0"}
FA2_RECORD = {"path": "docs/implementation/m3/native-successors-fa/fa-2/successor.json", "bytes": 38659,
              "sha256": "f6b105f49ee5c9ae716c1cbb0d05f5288e35870740a572023e5609872e165728"}
FA2_README = {"path": "docs/implementation/m3/native-successors-fa/fa-2/README.md", "bytes": 37836,
              "sha256": "59381765049d16320eb8d1886fb0f5a51651485d0e3c9ddea3641d5691225af7"}
FA2_SECTION = {"path": "docs/implementation/m3/native-successors-fa/fa-2/section-9-8.md", "bytes": 8270,
               "sha256": "2769b0935a7e1fd0d8b7a76c245d44dee7cd08588379f21a34f2be17c2e2e6c0"}
FA2_SUBJECT = {"path": "docs/implementation/m3/native-successors-fa/fa-2-subject.json", "bytes": 2394,
               "sha256": "dca02900a4f030d80021ea889afc73005df9ba4959ebfd682eb23d8118998538"}

E1 = {"path": "docs/implementation/m3/errata-2026-11-13b/ERRATUM-FA2-CENSUS-E1.md", "bytes": 32962,
      "sha256": "1dd70aa997e6250f0256557ff4eceb24217ffdcde16d4ae9d4649a8d7e3232c1"}
E2 = {"path": "docs/implementation/m3/errata-2026-11-13c/ERRATUM-FA2-CENSUS-E2.md", "bytes": 35800,
      "sha256": "56723546361dd29bed388b22837f57f2fbb4ae131e61a7a957544ab0ad6f031e"}
E3 = {"path": "docs/implementation/m3/errata-2026-11-14b/ERRATUM-FA2-CENSUS-E3.md", "bytes": 28608,
      "sha256": "83a1919be8a4a4a10f5d160ff403823433cf2df75d3bfdacb939d9194d382c5d"}
RC1 = {"path": "docs/implementation/m3/errata-2026-11-13b/ADOPTION-FA2-CENSUS-E1.md", "bytes": 3472,
       "sha256": "35cc11057dea4267a97d32fa43024a0be0e833849d5c71ea4ad32c7a53f76b46"}
RC2 = {"path": "docs/implementation/m3/errata-2026-11-13c/ADOPTION-FA2-CENSUS-E2.md", "bytes": 3574,
       "sha256": "a4434259e1ce294e066bc787d42935abcb3ee946c7d7b7c63b0c1ed7c48192d8"}
RC3 = {"path": "docs/implementation/m3/errata-2026-11-14b/ADOPTION-FA2-CENSUS-E3.md", "bytes": 8068,
       "sha256": "1d5a2c8d1b325e50ff2193ef4a62d27425a205b97151b8c3b87a480635f53261"}
LAW_FILES = [E1, RC1, E2, RC2, E3, RC3]

NE_LINE = 3313
NE_BEFORE = "No framing, process or compiler is exercised."
RULE_PREFIX = "native.symbol-census-population."

# The two sentences E1 amends, as FA-2's section-9-8.md holds them (9.8:3-5, :56-57).
OLD_POPULATION = ("A TypeScript or Rust provider's symbol census is its explicit population assertion (the\n"
                  "header above; identity §4): the first-party symbols its program declares over the binding's\n"
                  "symbol extent (enumeration contract §5), with the paths it examined.")
OLD_ROWS = ("Rows name first-party symbols only: an external symbol is not a row,\n"
            "  and a symbol with no fact is still one.")
# The anchor after 9.8:11, where E1 FCE1.2 inserts.
INSERT_ANCHOR = "`x-opensip-symbol-census-law`).\n\n**Negotiated payloads, not new frames.**"
README_282_OLD = "rows for every first-party symbol, including those with no fact"

FENCE_OPEN = "```opensip-stated-population-rules-v1"
FENCE_CLOSE = "```"
ROLES = ("rust-semantic", "typescript-semantic")
RULE_RE = re.compile(r"native\.symbol-census-population\.[a-z][a-z0-9-]*\.v[1-9][0-9]*")
HEX64 = re.compile(r"[0-9a-f]{64}")

# The stated rules: (rule id, standing, role subprotocol bound prospectively).
STATED = [
    (RULE_PREFIX + "default.v1", "prospective", "rust-semantic"),
    (RULE_PREFIX + "typescript.v1", "historical", None),
    (RULE_PREFIX + "typescript.v2", "historical", None),
    (RULE_PREFIX + "typescript.v3", "prospective", "typescript-semantic"),
]

# Incorporated passages: (label, file key, first line, last line, expected start of first line,
# expected start of last line, column/sentence limit or None, what it states).
PASSAGES = [
    ("I1", "E1", 74, 78, "> **The TypeScript population rule `native.symbol-census-population.typescript.v1`",
     "> **The two-copies rule (R2)", None,
     "rule `…typescript.v1`: its sentences, members and seeds, and the two-copies rule (FCE1.3)"),
    ("I2", "E1", 82, 111, "| # | Declaration class | Rule |", "| C28 |",
     "the columns \"#\", \"Declaration class\" and \"Rule\" only (`E1:80`)",
     "rule `…typescript.v1`: declaration classes C1-C28 (FCE1.3)"),
    ("I3", "E1", 122, 122, "> **Relations under `native.symbol-census-population.typescript.v1`.**",
     "> **Relations under", None, "relations under `…typescript.v1` (FCE1.4)"),
    ("I4", "E1", 132, 132, "> **A wider population is a new rule.**", "> **A wider population", None,
     "widening: a wider population is a new rule (FCE1.5)"),
    ("I5", "E1", 160, 160, "> **Each enumerator closure has exactly one population-rule binding.**",
     "> **Each enumerator closure", None, "one population-rule binding per enumerator closure (FCE1.7)"),
    ("I6", "E3", 19, 95, "> **A1. The enumerator closure.**", ">   A6 refuses any other Plan", None,
     "the carrier, statements A1-A10: the closure (A1), form (A2), bindable rules (A3), writer and conflicting "
     "bindings (A4), when the carrier exists (A5), the Plan-time checks (A6), retention, binding classes and the "
     "replay table (A7), review (A8), \"stated in this section\" (A9), the end of the complete-census prohibition (A10)"),
    ("I7", "E2", 53, 71, "> **The TypeScript population rule `native.symbol-census-population.typescript.v2`",
     ">    No other position holds.", None, "rule `…typescript.v2`: v1 with statements 0-3 (FCE2.2)"),
    ("I8", "E2", 103, 104, "`native.symbol-census-population.typescript.v1` is withdrawn.",
     "enumerator closure, and any reference to it moves to v2.",
     "from its first word to \"moves to v2.\"", "`…typescript.v1` withdrawn before any use (FCE2.3)"),
    ("I9", "E3", 159, 159, "> **The TypeScript population rule `native.symbol-census-population.typescript.v3`",
     "> **The TypeScript population rule", None, "rule `…typescript.v3`: v2 with statement 4 (FCE3.3)"),
    ("I10", "E3", 130, 147, "> 4. **Export entries with several declarations", "> **F3 and this rule.**",
     "line 141 included", "statement 4 of `…typescript.v3` and the two sentences on F3 (FCE3.2)"),
    ("I11", "E3", 167, 168, "**v2 is withdrawn before any use.**", "to it moves to v3.",
     "from its first word to \"moves to v3.\"", "`…typescript.v2` withdrawn before any use (FCE3.3)"),
]


class BuildError(Exception):
    pass


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pin_of(root: Path, path: str) -> dict:
    raw = (root / path).read_bytes()
    return {"path": path, "bytes": len(raw), "sha256": sha(raw)}


def pinned(root: Path, pin: dict) -> bytes:
    raw = (root / pin["path"]).read_bytes()
    if len(raw) != pin["bytes"] or sha(raw) != pin["sha256"]:
        raise BuildError(f"pinned input differs: {pin['path']}")
    return raw


def lines_of(raw: bytes) -> list[str]:
    return raw.decode("utf-8").splitlines()


def a2_bytes(rule: str) -> bytes:
    """E3 A2: the RFC 8785 form of {"populationRule": rule, "schemaVersion": 1}."""
    return json.dumps({"populationRule": rule, "schemaVersion": 1}, sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def block_line(rule: str, standing: str, role: str | None) -> str:
    row = {"a2Sha256": sha(a2_bytes(rule)), "bindsRoleSubprotocol": role, "rule": rule, "standing": standing}
    return json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def stated_rules(text: str) -> list[dict]:
    """Reference reader of the stated-rules block of a section 9.8 text (fail closed).

    Returns the rows in block order. Raises BuildError on anything the stated
    syntax does not allow; a reader never guesses or repairs.
    """
    lines = text.split("\n")
    opens = [i for i, line in enumerate(lines) if line == FENCE_OPEN]
    if text.count(FENCE_OPEN) != 1 or len(opens) != 1:
        raise BuildError("the text must hold the opening fence exactly once, as a whole line")
    try:
        close = lines.index(FENCE_CLOSE, opens[0] + 1)
    except ValueError:
        raise BuildError("unclosed stated-rules block") from None
    body = lines[opens[0] + 1:close]
    if not body:
        raise BuildError("empty stated-rules block")
    rows, previous, digests = [], None, set()
    for line in body:
        def pairs(items):
            keys = [k for k, _ in items]
            if len(keys) != len(set(keys)):
                raise BuildError("duplicate key in a stated-rules row")
            return dict(items)
        try:
            row = json.loads(line, object_pairs_hook=pairs)
        except ValueError as error:
            raise BuildError(f"stated-rules row is not JSON: {error}") from None
        if not isinstance(row, dict) or set(row) != {"a2Sha256", "bindsRoleSubprotocol", "rule", "standing"}:
            raise BuildError("stated-rules row has unknown or missing keys")
        rule, standing, role, digest = row["rule"], row["standing"], row["bindsRoleSubprotocol"], row["a2Sha256"]
        if not isinstance(rule, str) or not RULE_RE.fullmatch(rule):
            raise BuildError("stated-rules row has a malformed rule id")
        if standing == "prospective":
            if role not in ROLES:
                raise BuildError("a prospective row names one role subprotocol")
        elif standing == "historical":
            if role is not None:
                raise BuildError("a historical row binds no role subprotocol")
        else:
            raise BuildError("stated-rules standing is prospective or historical")
        if not isinstance(digest, str) or not HEX64.fullmatch(digest) or digest != sha(a2_bytes(rule)):
            raise BuildError("a2Sha256 is not the sha256 of the rule's A2 bytes")
        if block_line(rule, standing, role) != line:
            raise BuildError("stated-rules row is not in RFC 8785 form")
        if previous is not None and rule.encode("utf-8") <= previous.encode("utf-8"):
            raise BuildError("stated-rules rows must be strictly ascending by rule id")
        if digest in digests:
            raise BuildError("duplicate A2 digest")
        previous = rule
        digests.add(digest)
        rows.append(row)
    return rows


def norm(text: str) -> str:
    return " ".join(text.split())


def quote_line(lines: list[str], number: int) -> str:
    line = lines[number - 1]
    if not line.startswith("> "):
        raise BuildError(f"expected a quoted line at {number}")
    return line[2:]


def build(root: Path) -> dict[str, bytes]:
    for pin in (NE, FA2_RECORD, FA2_README, FA2_SECTION, FA2_SUBJECT, *LAW_FILES):
        pinned(root, pin)
    files = {"E1": lines_of(pinned(root, E1)), "E2": lines_of(pinned(root, E2)), "E3": lines_of(pinned(root, E3))}
    e1 = files["E1"]

    # FA-2's subject pins the two members this record overrides.
    fa2_subject = json.loads(pinned(root, FA2_SUBJECT))
    for pin in (FA2_README, FA2_SECTION, FA2_RECORD):
        if pin not in fa2_subject["files"]:
            raise BuildError(f"FA-2's subject does not pin {pin['path']}")

    # NE:3313 and FA-2's override of it; the override's after is FA-2's section 9.8 rendering.
    ne_lines = lines_of(pinned(root, NE))
    if ne_lines[NE_LINE - 1] != NE_BEFORE:
        raise BuildError("NE:3313 differs")
    fa2 = json.loads(pinned(root, FA2_RECORD))
    matches = [o for o in fa2["passageOverrides"] if o["parent"] == NE and o["selector"] == {"line": NE_LINE}]
    if len(matches) != 1 or matches[0]["before"] != NE_BEFORE:
        raise BuildError("FA-2 has no unique NE:3313 override")
    fa2_after = matches[0]["after"]
    old_section = pinned(root, FA2_SECTION).decode("utf-8")
    if fa2_after != NE_BEFORE + "\n\n" + old_section.rstrip("\n"):
        raise BuildError("FA-2's NE:3313 after is not its section-9-8.md rendering")

    # E1 FCE1.1 quotes the sentences; FCE1.2 gives their readings.
    if norm(OLD_POPULATION) != norm(quote_line(e1, 34)) or norm(OLD_ROWS) != norm(quote_line(e1, 38)):
        raise BuildError("the amended sentences differ from E1 FCE1.1's quotations")
    if old_section.count(OLD_POPULATION) != 1 or old_section.count(OLD_ROWS) != 1:
        raise BuildError("an amended sentence is not unique in FA-2's section 9.8")
    new_population, new_rows = quote_line(e1, 54), quote_line(e1, 58)
    if not e1[51].startswith("**`9.8:3-5`** is read as") or not e1[55].startswith("**`9.8:56-57`** is read as"):
        raise BuildError("E1:52 or E1:56 is not the reading instruction")

    # Incorporated passages: check each range's boundaries against the pinned lines.
    for label, key, first, last, start, end, _limit, _what in PASSAGES:
        lines = files[key]
        if not lines[first - 1].startswith(start) or not (lines[last - 1].startswith(end) or lines[last - 1].endswith(end)):
            raise BuildError(f"{label}: {key}:{first}-{last} boundaries differ")
        if last < len(lines) and lines[last].strip() not in ("", ">") and label not in ("I8", "I11"):
            raise BuildError(f"{label}: {key}:{last + 1} continues the passage")
    if files["E3"][140].startswith(">") or not files["E3"][140].startswith("   - (c) **`exported`"):
        raise BuildError("E3:141 changed")

    # E3 A3's two rows (E3:27-28) and its printed digests.
    a3 = {}
    for line in files["E3"][26:28]:
        cells = [c.strip().strip("`") for c in line.removeprefix(">").strip().strip("|").split("|")]
        a3[cells[0]] = (cells[1], cells[2])
    for rule, standing, role in STATED:
        digest = sha(a2_bytes(rule))
        if standing == "prospective" and a3.get(rule) != (role, digest):
            raise BuildError(f"prospective row {rule} differs from E3 A3")
    if {r for r, s, _ in STATED if s == "prospective"} != set(a3):
        raise BuildError("prospective rows are not exactly E3 A3's rows")

    def ref(pin: dict, label: str) -> str:
        return f"- **{label}** = `{pin['path']}`, {pin['bytes']:,} bytes, sha256 `{pin['sha256']}`."

    rows = "\n".join(f"| {label} | {key}:{first}-{last}" + (f", {limit}" if limit else "") + f" | {what} |"
                     if first != last else
                     f"| {label} | {key}:{first}" + (f", {limit}" if limit else "") + f" | {what} |"
                     for label, key, first, last, _s, _e, limit, what in PASSAGES)
    block = "\n".join([FENCE_OPEN, *(block_line(*row) for row in STATED), FENCE_CLOSE])
    insertion = "\n".join([
        "**Population rules and their carrier (errata FA2-CENSUS-E1, FA2-CENSUS-E2 and FA2-CENSUS-E3).** The "
        "passages I1-I11 below are text of this section, inserted here in that order. Each is incorporated from "
        "the exact bytes of the file named, at the lines given, without its block-quote markers (`>`), and reads "
        "as if it were written here. Its line references keep reading the files they name; `9.8:N` is "
        f"`{FA2_SECTION['path']}`, FA-2's rendering of this section. Nothing else in those files is text of this "
        "section: not their commentary, evidence, probes, code columns or status lines. The two sentences above "
        "and below that FA2-CENSUS-E1 amends (`9.8:3-5`, `9.8:56-57`) stand here in its words (`E1:54`, `E1:58`).",
        "",
        ref(E1, "E1") + f" Adopted by `{RC1['path']}` ({RC1['bytes']:,} bytes, sha256 `{RC1['sha256']}`).",
        ref(E2, "E2") + f" Adopted by `{RC2['path']}` ({RC2['bytes']:,} bytes, sha256 `{RC2['sha256']}`).",
        ref(E3, "E3") + f" Adopted by `{RC3['path']}` ({RC3['bytes']:,} bytes, sha256 `{RC3['sha256']}`).",
        "",
        "| Passage | Lines | What it states |",
        "|---|---|---|",
        rows,
        "",
        "Where these passages differ in wording, the later erratum governs, as it states itself: E3 A5 (`E3:34`) "
        "ends the interim readings of `E1:54` and `E1:160`, and E3 A3 (`E3:23-30`) is the only source of rules "
        "that packaging may write and a Plan may admit. So `…typescript.v1` and `…typescript.v2`, stated "
        "here, bind no closure (I8, I11; E3 A7, row RT-5).",
        "",
        "**The rules stated in this section.** The block below lists every population rule this section states. "
        "It adds no rule, binding or check. Its syntax: the block is the lines strictly between the one line of "
        "this section that is exactly three backquotes (U+0060) followed by `opensip-stated-population-rules-v1`, "
        "and the next line that is exactly three backquotes. Each "
        "line is one row, the RFC 8785 form of a JSON object with exactly the members `a2Sha256`, "
        "`bindsRoleSubprotocol`, `rule` and `standing`, and the rows are strictly ascending by the UTF-8 bytes "
        "of `rule`. `rule` is a rule id. `a2Sha256` is the lowercase hex sha256 of that rule's A2 bytes (E3 A2). "
        "`standing` is `prospective` for a rule of E3 A3, and then `bindsRoleSubprotocol` is the one role "
        "subprotocol whose closures that A3 row binds; the prospective rows are exactly A3's rows. `standing` "
        "is `historical` for a rule stated only for reading retained evidence (E3 A7), and then "
        "`bindsRoleSubprotocol` is `null`; such a rule is no A3 row and passes no check of E3 A6. A reader that "
        "finds anything else refuses the block and reads no rule as stated.",
        "",
        block,
    ])
    if not old_section.count(INSERT_ANCHOR) == 1:
        raise BuildError("insertion anchor after 9.8:11 is not unique")
    new_section = old_section.replace(OLD_POPULATION, new_population).replace(OLD_ROWS, new_rows)
    head, tail = INSERT_ANCHOR.split("\n\n", 1)
    new_section = new_section.replace(INSERT_ANCHOR, head + "\n\n" + insertion + "\n\n" + tail)
    after = NE_BEFORE + "\n\n" + new_section.rstrip("\n")
    parsed = stated_rules(after)
    if [(r["rule"], r["standing"], r["bindsRoleSubprotocol"]) for r in parsed] != STATED:
        raise BuildError("the reference reader does not read back the stated rules")

    # README:282 (X-FA2-FG): E1:60-62 give the words and their reading.
    readme_lines = lines_of(pinned(root, FA2_README))
    line_282 = readme_lines[281]
    if README_282_OLD not in e1[59] or line_282.count(README_282_OLD) != 1 or not line_282.startswith("| **X-FA2-FG** |"):
        raise BuildError("README:282 or E1:60 differs")
    readme_after = line_282.replace(README_282_OLD, quote_line(e1, 62))
    section_line_1 = old_section.split("\n", 1)[0]
    section_after = (section_line_1 + " (FA-2's rendering before errata FA2-CENSUS-E1, E2 and E3. The current "
                     f"text of this section is the FA2-CENSUS-r1 successor's, rendered in `{SECTION}`. Line "
                     "references `9.8:N` keep reading this file.)")

    record = {
        "schemaVersion": 1,
        "standing": (
            "PROPOSED FA2-CENSUS-r1 native contract successor (errata FA2-CENSUS-E1 r5, FA2-CENSUS-E2 r5 and "
            "FA2-CENSUS-E3 r5, each adopted by receipt, all owing this record): native-evidence section 9.8 "
            "states the symbol-census population rules. In law VD2's form: one contract passage supersession of "
            "FA-2's NE:3313 override (the section 9.8 text), naming FA-2's record by exact pin, and two line "
            "overrides of FA-2's own members (README:282, the emission duty, in E1's words; section-9-8.md:1, "
            "which marks that file as FA-2's rendering). The new section 9.8 keeps every word of FA-2's text "
            "except the two sentences E1 amends, which stand in E1's words (E1:54, E1:58). After its first "
            "paragraph it inserts eleven passages of the three errata by incorporation (exact lines of the "
            "pinned bytes; the three errata and their receipts are carried by value) and one machine-readable "
            "block of the rules it states. No wire member, token, schema, frame, deficiency, cause, key, binding "
            "or product file changes. Independent review and root assent are required."),
        "parents": sorted([FA2_README, FA2_SECTION, NE], key=lambda p: p["path"]),
        "passageOverrides": [
            {"parent": FA2_README, "selector": {"line": 282}, "before": line_282, "after": readme_after},
            {"parent": FA2_SECTION, "selector": {"line": 1}, "before": section_line_1, "after": section_after},
        ],
        "passageSupersessions": [
            {"parent": NE, "selector": {"line": NE_LINE}, "before": fa2_after, "after": after,
             "supersedes": {"record": FA2_RECORD, "parent": NE, "selector": {"line": NE_LINE}}},
        ],
        "lawFilesByValue": LAW_FILES,
    }
    section_bytes = new_section.encode("utf-8")
    out = {SECTION: section_bytes}
    candidates = [*LAW_FILES, pin_of(root, README), pin_of(root, SCRIPT),
                  {"path": SECTION, "bytes": len(section_bytes), "sha256": sha(section_bytes)}]
    record["candidates"] = sorted(candidates, key=lambda p: p["path"])
    record_bytes = (json.dumps(record, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    out[RECORD] = record_bytes
    members = record["candidates"] + [{"path": RECORD, "bytes": len(record_bytes), "sha256": sha(record_bytes)}]
    subject = {"schemaVersion": 1, "files": sorted(members, key=lambda p: p["path"])}
    out[SUBJECT] = (json.dumps(subject, indent=2) + "\n").encode("utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[6])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        out = build(args.root)
    except BuildError as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    differs = []
    for path, raw in out.items():
        target = args.root / path
        if args.check:
            if not target.exists() or target.read_bytes() != raw:
                differs.append(path)
        else:
            target.write_bytes(raw)
    for path, raw in out.items():
        print(f"{'DIFF' if path in differs else 'OK'} {path} {len(raw)} {sha(raw)}")
    return 1 if differs else 0


if __name__ == "__main__":
    sys.exit(main())
