
ipefigs=$(wildcard figs/*.ipe)

turan.pdf : turan.tex $(ipefigs)
	(cd figs; make)
	latexmk -pdf turan.tex 	

clean :
	rm -f slides.pdf figs/*.pdf
