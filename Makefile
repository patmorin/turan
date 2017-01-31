
ipefigs=$(wildcard figs/*.ipe)
slidefigs=$(wildcard figs/*.ipe)

turan.pdf : turan.tex bounds.tex turan.bib $(ipefigs)
	(cd figs; make)
	latexmk -pdf turan.tex 	

bounds.tex : turan-table.py
	./turan-table.py

slides.pdf : slides.tex
	(cd figs; make)
	(cd slidefigs; make)
	pdflatex slides

clean :
	rm -f turan.pdf figs/*.pdf
