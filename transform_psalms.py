#!/usr/bin/python3
from psalm_parser import process_verses
from pathlib import Path
from sys import argv

inf = Path(argv[1]).expanduser()
outd = Path(argv[2]).expanduser()

verses = process_verses(inf, "ab")
# enforce the first verse being exactly 2 lines long, in case we need to skip later

k = list(verses.keys())[0]
if "+" in verses[k]:
    verses[k] = verses[k].replace("~+\\\\\n", "~+\\\\")

with (outd / inf.name).open("w") as f:
    for _, verse in verses.items():
        f.write(verse + "\n")
