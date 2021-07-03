#!/usr/bin/python3
from pathlib import Path

Path("./pdfs").mkdir()

for pdf in Path("vespers/").glob("**/*.pdf"):
    if pdf.stem.endswith("booklet"):
        target = Path(f"./pdfs/{pdf.parent.name}-booklet.pdf")
    else:
        target = Path(f"./pdfs/{pdf.parent.name}.pdf")

    # yeah, we could use copy...
    with target.open("wb") as f:
        with pdf.open("rb") as g:
            f.write(g.read())
