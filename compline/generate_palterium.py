#!/usr/bin/python3
from pathlib import Path

days = {
    "Dominica": [4, 90, 133],
    "Feria Secunda": [6, 7.1, 7.2],
    "Feria Tertia": [11, 12, 15],
    "Feria Quarta": [33.1, 33.2, 60],
    "Feria Quinta": [69, 70.1, 70.2],
    "Feria Sexta": [76.1, 76.2, 85],
    "Sabbato": [87, 102.1, 102.2]
}

output = Path("psalterium.tex")
if output.exists():
    output.rename("psalterium.tex.bak")

psalterium = """

\\section{Psalterium}
\\label{sec:psalterium}

\\setlength{\\vindent}{\\vgap}

\\let\\tmp\\subsection
\\renewcommand{\\subsection}{\\clearpage\\tmp}

"""

psalm_parts = {"1": "i", "2": "ii"}

for day, psalms in days.items():
    short_day = day.split(" ")[-1].lower()[:3]
    psalterium += f"\\subsection{{{day}}}\n"
    psalterium += f"\\label{{sec:{short_day}-perannum}}"
    psalterium += f"\\gregorioscore{{../psalm-antiphons/{day.lower().replace(' ','')}antiphon.gabc}}\n\n"
    

    for i, psalm in enumerate(psalms):
        i += 1
        try:
            a, b = str(psalm).split(".")
            psalterium += f"\\ps[{psalm_parts[b]}]{{{a}}}\n"
        except ValueError:
            psalterium += f"\\ps{{{psalm}}}\n"

        psalterium += f"\\gregorioscore{{perannum/{short_day}{i}.gabc}}\n"
        psalterium += "\n\\begin{verse}\n"
        with Path(f"perannum/{short_day}{i}.tex").open() as f:
            psalterium += f.read()
        psalterium += "\end{verse}\n"
    
        # psalterium += f"\\input{{perannum/{short_day}{i}.tex}}\n"

    psalterium += "\n\n"

psalterium += '\subsection{Tempore Paschalis}'
psalterium += '\let\subsection\\tmp'
psalterium += '\gregorioscore{../psalm-antiphons/alleluiapaschal.gabc}'

for day, psalms in days.items():
    short_day = day.split(" ")[-1].lower()[:3]
    psalterium += f"\\subsection{{{day}}}\n"
    psalterium += f"\\label{{sec:{short_day}-paschal}}"
    

    for i, psalm in enumerate(psalms):
        i += 1
        use_previous = None
        with Path(f"perannum/{short_day}1.gabc").open() as f:
            for line in f:
                if line.startswith("annotation"):
                    if '8' in line:
                        use_previous = True
                    else:
                        use_previous = False
                    break

        if use_previous is None:
            print("Unable to work out mode")

        if use_previous:
            psalterium += f"See p. \\pageref{{sec:{short_day}-perannum}}."
            break
                
        try:
            a, b = str(psalm).split(".")
            psalterium += f"\\ps[{psalm_parts[b]}]{{{a}}}\n"
        except ValueError:
            psalterium += f"\\ps{{{psalm}}}\n"

        psalterium += f"\\gregorioscore{{paschal/{short_day}{i}.gabc}}\n"
        psalterium += "\n\\begin{verse}\n"
        with Path(f"paschal/{short_day}{i}.tex").open() as f:
            psalterium += f.read()
        psalterium += "\end{verse}\n"

    psalterium += "\n\n"



with output.open("w") as f:
    f.write(psalterium)


print(psalterium)
        

        
        
        
