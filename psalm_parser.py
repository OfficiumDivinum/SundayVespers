#!/usr/bin/python3
"""Basic parser for psalms as downloaded and converted to tex.
Format is:
{XX~} half verse * half verse
continue half verse

Last two verses are Gloria.
"""

import argparse
import warnings
from pathlib import Path
from re import search

parser = argparse.ArgumentParser()
parser.add_argument("ANTIPHON", help="Antiphon file to parse")
parser.add_argument("PSALM_NAME", help="psalm name to output")
parser.add_argument("--range", help="Range to print")
parser.add_argument("-ng", "--no-gloria", help="Omit Gloria?", action="store_true")
parser.add_argument("-nc", "--no-copy", action="store_true", help="Skip .gabc file")
args = parser.parse_args()

nos = [
    "Zero",
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
]

antiphon = Path(args.ANTIPHON).expanduser()
mode, termination = None, None
with antiphon.open() as f:
    for line in f.readlines():
        if match := search("mode:(.+);", line):
            mode = match.group(1)
        if match := search("mode-differentia:(.+);", line):
            termination = match.group(1)
if not mode:
    raise Exception("No mode found")
if not termination:
    warnings.warn("No termination found")

if match := search("ant([0-9])", antiphon.stem):
    logical_name = match.group(1)
elif match := search("(.+)-ant", antiphon.stem):
    logical_name = match.group(1)
else:
    raise Exception("Unable to determine logical name")


verses = {}
if termination:
    inf = Path(f"../../psalms/{args.PSALM_NAME}-{mode}{termination}.tex")
else:
    inf = Path(f"../../psalms/{args.PSALM_NAME}-{mode}.tex")

outd = Path(".")

with inf.open() as f:
    for line in f:
        if line.startswith("{"):
            no, vpart = line.split("}", 1)
            no = int(no.lstrip("{").strip(".~"))
            verses[no] = (
                vpart.strip("\n")
                .replace("~†", "~\\+\\\\\n \\vin")
                .replace("~*", "~\\*\\\\\n \\vin")
            )
            last_verse = no
        else:
            verses[last_verse] = (
                verses[last_verse]
                + " "
                + line.strip("\n")
                .replace("~†", "~\\+\\\\\n \\vin")
                .replace("~*", "~\\*\\\\\n \\vin")
            )

if not args.range:
    start = min(verses.keys())
    stop = max(verses.keys()) - 2
else:
    start, stop = args.RANGE.split("-")

try:
    logical_name = int(logical_name)
    outf = outd / f"psalm{logical_name}.gabc"
    tex_name = f"\\newcommand{{\\psalm{nos[int(logical_name)]}}}{{\n"
except ValueError:
    outf = outd / f"{logical_name}.gabc"
    tex_name = f"\\newcommand{{\\{logical_name}}}{{\n"

with (outd / "psalms.tex").open("a") as f:
    f.write(tex_name)

    for i in range(int(start), int(stop) + 1):
        f.write(verses[i] + "\n")

    if not args.no_gloria:
        for i in list(verses.keys())[-2:]:
            f.write(verses[i] + "\n")

    f.write("}\n\n")

if not args.no_copy:
    with outf.open("w") as f:
        with inf.with_suffix(".gabc").open() as g:
            f.write(g.read())
