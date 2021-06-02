#!/usr/bi/python3
from pathlib import Path
from zipfile import ZipFile

with ZipFile("pdfs.zip", "w") as zipf:
    for pdf in Path("vespers/").glob("**/*.pdf"):
        zipf.write(pdf, arcname=f"{pdf.parent.name}.pdf")

from os import get_cwd
print("Working dir is", get_cwd)

