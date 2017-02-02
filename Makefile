
ipefigs=$(wildcard figs/*.ipe)
slidefigs=$(wildcard figs/*.ipe)

turan.pdf : figs turan.tex bounds.tex turan.bib $(ipefigs)
	latexmk -pdf turan.tex 	

figs: $(ipefigs)
	(cd figs; make)

bounds.tex : turan-table.py
	./turan-table.py

slides.pdf : slides.tex
	(cd figs; make)
	(cd slidefigs; make)
	pdflatex slides

clean :
	rm -f turan.pdf figs/*.pdf
