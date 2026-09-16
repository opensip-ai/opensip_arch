"""Reviewer probe: deterministic lexical corpus for the Rust/reference differential.

Writes probes/corpus.hex: one lowercase-hex input per line (an empty line is the
empty input). Inputs come from literal edge cases, a clean structured generator,
a noisy structured generator, deep spines and byte-level mutations.
"""
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SEED = 20260914
RANDOM_CASES = 20000
MAX_CASE_BYTES = 65536

HANDWRITTEN_TEXT = [
    '{"\U00010000":0,"":1,"\x80":2,"\x7f":3,"ab":4,"a":5,"":6,"B":7}',
    '{"/":1,"\\/":2}', '{"A":1,"\\u0041":2}', '{"é":1,"\\u00E9":2}',
    '"\\u00E9"', '"\\uD834\\uDD1E"', '"\\ud834\\udd1e"', '"\\u001F"', '"\\u002F\\/"',
    '"\\ud800\\ud800"', '"\\ud800\\n"', '"\\udfff"', '"\\ud800\\u12"', '"\\ud800\\"', '"\\ud800 \\udc00"',
    '"\\u1_23"', '"\\u+123"', '"\\u 123"', '"\\u-123"', '"\\U0041"', '"\\x41"', '"\\\'"',
    '\t\r\n [ \t1 \r\n, 2 ]\n', '\x0c1', '\xa01', '1\xa0', ' 1', '﻿null',
    '-', '--1', '1.', '0e', '-0.0', '00', '0x10', '1_000', '[-0]', '{"a":-0}', '+1', '.5',
    '1e+5', '1E-5', '-0 ',
    '18446744073709551615', '-9223372036854775808', '18446744073709551616', '-9223372036854775809',
    '170141183460469231731687303715884105727', '-170141183460469231731687303715884105728',
    '340282366920938463463374607431768211456', '9' * 5000,
    'NaN', '-NaN', 'Infinity', '-Infinity', 'nul', 'nullx', 'True', 'FALSE',
    '1 x', '[] []', '"\\', '"abc', '[1,,2]', '{"a"}', '{"a":}', '{:1}', '{"a":1 "b":2}', '[1 2]',
    '[,1]', '{,}', '{"a":1,"a":1.5}', '{"a":1.5,"a":1}',
    '{"s":"\\u0000\\u001f\\u001F\\b\\f\\n\\r\\t\\/\\"\\\\"}',
    '"\x7f  ﻿￾￿\U0010ffff"',
    '{"":{"":{"":[]}}}', '{"Å":1,"Å":2,"Å":3}',
    '[' * 32 + ']' * 32, '[' * 33 + ']' * 33, '[' * 40,
    '{"k":' * 32 + '0' + '}' * 32, '{"k":' * 33 + '0' + '}' * 33,
    '[' * 32 + '1.0' + ']' * 32, '[' * 33 + '1.0' + ']' * 33,
]
HANDWRITTEN_BYTES = [
    b'', b' ', b'"\x00"', b'\x00', b'"\x1f"', b'"\xff"', b'"\xed\xa0\x80"', b'"\xf4\x90\x80\x80"',
    b'"\xc0\xaf"', b'"\xe0\x80\xaf"', b'"\xf0\x9f\x98"', b'\x80', b'"\x20"',
]

CLEAN_STRING = ["a", "é", "é", " ", "\x7f", "\U0001f600", "\\n", "\\u0000", "\\u001F",
                "\\uD83D\\uDE00", "\\/", '\\"', "\\\\", "\\b", " ", "/", "￾"]
NOISY_STRING = CLEAN_STRING + ["\\ud800", "\\udc00", "\\u00zz", "\x01", "\\", "\t", "\\x"]
KEY_PIECES = ["a", "\\u0061", "b", "é", "\\u00e9", "é", "\\/", "/", "", "\U00010000", ""]
CLEAN_NUMBERS = ["0", "-1", "7", "18446744073709551615", "-9223372036854775808", "123456789", "-10"]
NOISY_NUMBERS = CLEAN_NUMBERS + ["-0", "01", "1.0", "1e0", "18446744073709551616",
                                 "-9223372036854775809", "-", "1E5", "+1"]
CLEAN_LITERALS = ["null", "true", "false"]
NOISY_LITERALS = CLEAN_LITERALS + ["nul", "True", "NaN", "Infinity"]
CLEAN_SPACE = ["", "", "", " ", "\n", "\t", "\r\n"]
NOISY_SPACE = CLEAN_SPACE + ["\x0c", "\xa0"]
FRAGMENTS = [b"{", b"}", b"[", b"]", b",", b":", b'"', b"\\", b"u", b"d800", b"0", b"-", b".", b"e",
             b" ", b"\x00", b"\x7f", b"\xc3", b"\xff", b"null"]


def text(rng, pieces):
    return '"' + "".join(rng.choice(pieces) for _ in range(rng.randrange(0, 4))) + '"'


def space(rng, clean):
    return rng.choice(CLEAN_SPACE if clean else NOISY_SPACE)


def value(rng, depth, clean):
    roll = rng.random()
    if roll < 0.25 and depth < 34:
        items = [space(rng, clean) + value(rng, depth + 1, clean) + space(rng, clean)
                 for _ in range(rng.randrange(0, 4))]
        return "[" + ",".join(items) + "]"
    if roll < 0.5 and depth < 34:
        members = []
        for index in range(rng.randrange(0, 4)):
            key = text(rng, KEY_PIECES)
            if clean and rng.random() < 0.7:
                key = key[:-1] + str(index) + '"'
            members.append(space(rng, clean) + key + space(rng, clean) + ":" + space(rng, clean)
                           + value(rng, depth + 1, clean) + space(rng, clean))
        return "{" + ",".join(members) + "}"
    if roll < 0.7:
        return text(rng, CLEAN_STRING if clean else NOISY_STRING)
    if roll < 0.9:
        return rng.choice(CLEAN_NUMBERS if clean else NOISY_NUMBERS)
    return rng.choice(CLEAN_LITERALS if clean else NOISY_LITERALS)


def spine(rng, clean):
    opens, closes = [], []
    for _ in range(rng.randrange(28, 36)):
        if rng.random() < 0.5:
            opens.append("[")
            closes.append("]")
        else:
            opens.append('{"k":')
            closes.append("}")
    return "".join(opens) + value(rng, 99, clean) + "".join(reversed(closes))


def mutate(rng, data):
    data = bytearray(data)
    for _ in range(rng.randrange(1, 4)):
        operation = rng.randrange(4)
        position = rng.randrange(len(data) + 1)
        if operation == 0 and data:
            del data[min(position, len(data) - 1)]
        elif operation == 1:
            data[position:position] = rng.choice(FRAGMENTS)
        elif operation == 2 and data:
            data = data[:position]
        elif operation == 3 and data:
            start = rng.randrange(len(data))
            end = min(len(data), start + rng.randrange(1, 8))
            data[position:position] = data[start:end]
    return bytes(data)


def main():
    rng = random.Random(SEED)
    cases = [item.encode("utf-8") for item in HANDWRITTEN_TEXT] + HANDWRITTEN_BYTES
    for index in range(RANDOM_CASES):
        clean = index % 2 == 0
        if index % 10 == 0:
            raw = spine(rng, clean)
        else:
            raw = space(rng, clean) + value(rng, 0, clean) + space(rng, clean)
        raw = raw.encode("utf-8")
        if index % 3 == 0:
            raw = mutate(rng, raw)
        if len(raw) <= MAX_CASE_BYTES:
            cases.append(raw)
    unique = list(dict.fromkeys(cases))
    (HERE / "corpus.hex").write_text("".join(case.hex() + "\n" for case in unique))
    (HERE.parent / "results").mkdir(exist_ok=True)
    print(f"corpus cases: {len(unique)}")


if __name__ == "__main__":
    main()
