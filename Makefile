doc:
	mkdir -p doc
html: doc
	epydoc -v --graph=all --dotpath=doc/html --html *.py -o doc/html
pdf: doc
	epydoc -v --graph=all --pdf *.py -o doc/pdf
latex: doc
	epydoc -v --graph=all --latex *.py -o doc/latex
clean:
	rm -rf doc bin __pycache__ .DS_Store ; rm -f *.pyc
run:
	python3 main.py || python main.py
compile:
	python -m py_compile *.py
