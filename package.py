#!/usr/bin/python3
from pathlib import Path
from zipfile import ZipFile

with ZipFile("pdfs.zip", "w") as zipf:
    for pdf in Path("vespers/").glob("**/*.pdf"):
        zipf.write(pdf, arcname=f"{pdf.parent.name}.pdf")
print(list(Path(".").glob("*")))
print(Path(".").resolve())
