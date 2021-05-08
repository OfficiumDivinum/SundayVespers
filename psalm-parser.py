#!/usr/bin/python3
"""Basic parser for psalms as downloaded and converted to tex.
Format is:
{XX~} half verse * half verse
continue half verse

Last two verses are Gloria.
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("PATH", help="File to read in.")
parser.add_argument("-n", help="psalm number to output")
parser.add_argument("--range", help="Range to print")
parser.add_argument("-g", "--gloria", help="Print Gloria?", action="store_true")
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

with open(args.PATH, "r") as f:
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

if args.n:
    print(f"\\newcommand{{\\psalm{nos[int(args.n)]}}}{{")

for i in range(int(start), int(stop) + 1):
    print(verses[i])

if args.gloria:
    for i in list(verses.keys())[-2:]:
        print(verses[i])

if args.n:
    print("}\n\n")
