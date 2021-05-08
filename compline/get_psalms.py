#!/usr/bin/python3
"""Script to get all psalms for day in right tone and drop them in directory with right names"""
from pathlib import Path
from shutil import copy
from argparse import ArgumentParser

src = Path("/home/john/Library/Music/St-Cuthberts-Liturgy/gregorian-psalms/psalms")

parser = ArgumentParser()

parser.add_argument("PSALMS", nargs="+", help="psalm")
parser.add_argument("TONE", help="tone")
parser.add_argument("DAY", help="day")
parser.add_argument("--destdir", help="destdir, default = .")

args = parser.parse_args()
if not args.destdir:
    args.destdir = Path(".")
else:
    args.destdir = Path(args.destdir)

for i, psalm in enumerate(args.PSALMS):
    i+=1
    copy(src / f"{psalm}-{args.TONE}.gabc", args.destdir / f"{args.DAY}{i}.gabc")
    copy(src / f"{psalm}-{args.TONE}.tex", args.destdir / f"{args.DAY}{i}.tex")
    


