
install:
	pip install sphinx
doc: install
	sphinx-build -b html docsrc docs

