#!/usr/bin/python3
"""Basic parser for psalms as downloaded and converted to tex.
Format is:
{XX~} half verse * half verse
continue half verse

Last two verses are Gloria.
"""

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("PATH", help="File to read in.")
parser.add_argument("OUTDIR", help="outdir")
parser.add_argument("N", help="psalm number to output")
parser.add_argument("--range", help="Range to print")
parser.add_argument("-g", "--gloria", help="Print Gloria?", action="store_true")
parser.add_argument("-c", "--copy", action="store_true", help="Copy .gabc to approprately named file")
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

verses = {}
inf = Path(args.PATH).expanduser()
outd = Path(args.OUTDIR).expanduser()

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

with (outd / "psalms.tex").open("a") as f:

    f.write(f"\\newcommand{{\\psalm{nos[int(args.N)]}}}{{\n")

    for i in range(int(start), int(stop) + 1):
        f.write(verses[i] + "\n")

    if args.gloria:
        for i in list(verses.keys())[-2:]:
            f.write(verses[i] + "\n")

    f.write("}\n\n")

if args.copy:
    outf = outd / f"psalm{args.N}.gabc"
    with outf.open("w") as f:
        with inf.with_suffix(".gabc").open() as g:
            f.write(g.read())
