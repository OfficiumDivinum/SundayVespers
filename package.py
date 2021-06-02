#!/usr/bin/python3
from pathlib import Path
from zipfile import ZipFile

Path("./pdfs").mkdir()

for pdf in Path("vespers/").glob("**/*.pdf"):
    with Path(f"./pdfs/{pdf.parent.name}.pdf").open("wb") as f:
        with pdf.open("rb") as g:
            f.write(g.read())
