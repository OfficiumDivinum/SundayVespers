vespers.pdf: vespers.tex propers.tex
	env openout_any=a latexmk --shell-escape --pdflatex=lualatex --pdf vespers.tex

vespers-booklet.pdf: vespers.pdf
	pdfjam --landscape --suffix booklet --signature 4 vespers.pdf

.PHONY: all

all: vespers.pdf vespers-booklet.pdf
