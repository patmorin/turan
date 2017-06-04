
ipefigs=$(wildcard figs/*.ipe)
slidefigs=$(wildcard figs/*.ipe)

turan.pdf : figs turan.tex bounds.tex turan.bib $(ipefigs)
	latexmk -pdf turan.tex

figs: $(ipefigs)
	make -C figs

bounds.tex : turan-table.py
	./turan-table.py

slides.pdf : slides.tex
	make -C figs
	make -C slidefigs
	pdflatex slides

clean :
	rm -f turan.pdf figs/*.pdf
