"""Run labelled tools/seq.py groups strictly in order (each group's logs retained under its own label); later groups still run if one fails.
Usage: python3 tools/v2_chain.py <label>:<script>[,<script>...] ...   (a script with arguments uses '+' between tokens)
"""
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/output/preserved/pre-s42"


def main(argv):
    worst = 0
    for group in argv:
        label, scripts = group.split(":", 1)
        args = []
        for i, s in enumerate(scripts.split(",")):
            if i:
                args.append("--")
            args += s.split("+")
        p = subprocess.run([sys.executable, OUT + "/tools/seq.py", label] + args, capture_output=True, text=True)
        print(f"##### {label} exit {p.returncode}\n{p.stdout[-6000:]}{p.stderr[-2000:]}")
        worst = worst or p.returncode
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
