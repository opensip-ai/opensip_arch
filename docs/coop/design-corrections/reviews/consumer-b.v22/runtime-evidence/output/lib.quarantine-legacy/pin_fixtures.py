"""Pin every Run/vector semantic fixture label to the explicit, location-free constants in
opensip_fixture.py. Run once; idempotent and self-reporting."""
import os

LIB = os.path.dirname(os.path.abspath(__file__))

EDITS = {
    'run_syntax_code.py': [
        ("PROJECT_ID = 'prj1-' + '4b7f2c91a3e85d06fa1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f708192"
         "a3b4c5d6e'[:64]",
         "import opensip_fixture as FX\nPROJECT_ID = FX.PROJECT_ID['syntax-code']"),
        ("'profile': 'syntax-only',", "'profile': FX.PROFILE['syntax-code'],"),
    ],
    'run_syntax_data.py': [
        ("PROJECT_ID = 'prj1-' + '5d8c3a1f7e0b249635c8d1a4f7b0e3c6a9d2f5b8e1c4a7d0f3b6e9c2"
         "a5d8f1b4e'[:64]",
         "import opensip_fixture as FX\nPROJECT_ID = FX.PROJECT_ID['syntax-data']"),
        ("'profile': 'syntax-only-data',", "'profile': FX.PROFILE['syntax-data'],"),
    ],
    'run_ts.py': [
        ("PROJECT_ID = 'prj1-' + '7c1d9e4fa2b86035cd17e2f4a5b6c7d8e9f0a1b2c3d4e5f60718293"
         "a4b5c6d7e8'[:64]",
         "import opensip_fixture as FX\nPROJECT_ID = FX.PROJECT_ID['typescript']"),
        ("'profile': 'ts-default',", "'profile': FX.PROFILE['typescript'],"),
    ],
    'run_rust.py': [
        ("PROJECT_ID = 'prj1-' + '9e2a7b4c1d5f80369a7c2e4b6d8f0a1c3e5b7d9f2a4c6e8b0d1f3a5c7"
         "e9b0d2f'[:64]",
         "import opensip_fixture as FX\nPROJECT_ID = FX.PROJECT_ID['rust']"),
        ("'profile': 'rust-cargo',", "'profile': FX.PROFILE['rust'],"),
    ],
    'phase2.py': [
        ("import checkpoint as CK", "import checkpoint as CK\nimport opensip_fixture as FX"),
        ("'profile': 'consumer-b.v18.syntax-only',",
         "'profile': FX.PROFILE['vector-syntax'],"),
        ("'profile': 'consumer-b.v18.compiler-modes',",
         "'profile': FX.PROFILE['vector-compiler'],"),
        ("mut2['profile'] = 'consumer-b.v18.syntax-only.x'",
         "mut2['profile'] = FX.PROFILE['vector-compiler-mutated']"),
    ],
}


def main():
    for fn, pairs in EDITS.items():
        p = os.path.join(LIB, fn)
        s = open(p, encoding='utf-8').read()
        applied, missed = 0, []
        for a, b in pairs:
            if a in s:
                s = s.replace(a, b)
                applied += 1
            elif b.split('\n')[-1] in s:
                applied += 1          # already pinned
            else:
                missed.append(a[:70])
        open(p, 'w', encoding='utf-8').write(s)
        print('%-22s applied/already %d of %d  missed=%s' % (fn, applied, len(pairs), missed))


main()
