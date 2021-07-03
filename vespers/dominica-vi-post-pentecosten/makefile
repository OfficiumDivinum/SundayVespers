.PHONY: all

all: vespers.pdf vespers-booklet.pdf

vespers.pdf: vespers.tex propers.tex
	env openout_any=a latexmk --shell-escape --pdflatex=lualatex --pdf vespers.tex

vespers-booklet.pdf: vespers.pdf
	pdfjam --landscape --suffix booklet --booklet true  vespers.pdf

