"""Two bundled 2020-12 meta-schema pattern keywords still use Python re.search `$`.
Not a generic regex-engine product. format_checker does not affect these.
"""
from __future__ import annotations

import json
import re
import sys

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

ANCHOR = r"^[A-Za-z_][-A-Za-z0-9._]*$"
IDPAT = r"^[^#]*#?$"


def check(doc, none=False):
    try:
        if none:
            Draft202012Validator.check_schema(doc, format_checker=None)
        else:
            Draft202012Validator.check_schema(doc)
        return True
    except SchemaError:
        return False


def base(extra):
    d = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}
    d.update(extra)
    return d


def main() -> None:
    rows = []
    for name, extra, expect_admit in [
        ("anchor-a", {"$anchor": "a"}, True),
        ("anchor-a-lf", {"$anchor": "a\n"}, True),
        ("anchor-a-cr", {"$anchor": "a\r"}, False),
        ("id-a-hash-lf", {"$id": "a#\n"}, True),
        ("id-a-hash-cr", {"$id": "a#\r"}, False),
        ("id-a-hash-foo", {"$id": "a#foo"}, False),
    ]:
        s = extra[next(iter(extra))]
        pat = ANCHOR if "$anchor" in extra else IDPAT
        rows.append(
            {
                "name": name,
                "re_search": bool(re.search(pat, s)),
                "re_fullmatch": bool(re.fullmatch(pat, s)),
                "check_schema_default": check(base(extra), none=False),
                "check_schema_none": check(base(extra), none=True),
                "selectedShapeAdmit": expect_admit,
            }
        )
    print(
        json.dumps(
            {
                "python": sys.version.split()[0],
                "jsonschemaPatternKeyword": "re.search",
                "anchorPattern": ANCHOR,
                "idPattern": IDPAT,
                "dollarMatchesBeforeTrailingLFNotCR": True,
                "cases": rows,
                "scope": "Fixed meta-schema pattern keywords only; not format:regex; not a unit review of any projection.",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
