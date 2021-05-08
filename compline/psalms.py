#!/usr/bin/python3
from os import path
import re
"""Read and parse files from divinumofficium.org to spew out the right psalms."""
"""
[Completorium]
Dominica = Miserére * mihi, Dómine, et exáudi oratiónem meam.
4,90,133
Feria II = Salvum me fac, * Dómine, propter misericórdiam tuam.
6,7(2-10),7(11-18)
Feria III = Tu, Dómine, * servábis nos: et custódies nos in ætérnum.
11,12,15
Feria IV = Immíttet Ángelus Dómini * in circúitu timéntium eum: et erípiet eos.
33(2-11),33(12-23),60
Feria V = Adjútor meus * et liberátor meus esto, Dómine.
69,70(1-12),70(13-24)
Feria VI = Voce mea * ad Dóminum clamávi: neque obliviscétur miseréri Deus.
76(2-13),76(14-21),85
Sabbato = Intret orátio mea * in conspéctu tuo, Dómine.
87,102(1-12),102(13-22)
"""
divinumofficium = path.expanduser(
    "~/code/divinum-officium/web/www/horas/Latin")

rubric = {}
entry = []
# get data
with open(divinumofficium + "/Psalterium/Psalmi minor.txt", "r") as f:
    for line in f:
        if line.startswith("["):
            if len(entry) > 0:  # old entry
                rubric[entry_title] = entry
            entry = []
            entry_title = line.strip("[]\n")
        else:
            if len(line.strip()) > 0:
                entry.append(line.strip())

c = rubric['Completorium']  # this destroys in-situ
while c:
    (day, rep), psalms = (c[0].split("=")), c[1].split(",")
    c[:2] = []
    print("\\subsection{"+ day.strip() + "}\n")
    print(rep.strip(), "\n")
    for psalm in psalms:
        if "(" in psalm:
            (psalm, chunk) = psalm.split("(")
            chunk = chunk.strip(")").split("-")
        else:
            chunk = False
        print("\\begin{verse}")

        with open(divinumofficium + "/psalms1/Psalm" + psalm.strip() + ".txt",
                  "r") as f:
            lines = []
            start = False
            stop = False
            for line in f:
                if stop:
                    break
                if chunk:
                    if not start and psalm.strip() + ":" + chunk[0] in line:
                        start = True
                    elif start and start and psalm.strip() + ":" + chunk[1] in line:
                        stop = True
                else:
                    start = True
                if not start:
                    continue
                line = re.sub(r'[0-9]+:[0-9]+ ', '', line.strip()).replace(
                    "*", "\\*\\\\\n\\vin")
                lines.append(line + "\\\\")
            lines[-1] = lines[-1].rstrip("\\\\")
            for line in lines:
                print(line)
        print("\\end{verse}\n")
    print("\n" + rep.strip() + "\n")
