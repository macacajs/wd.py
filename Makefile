all: install
install:
	pip install sphinx
	pip install	twine
doc:
	sphinx-build -b html docsrc docs
build:
	python setup.py sdist build
	python setup.py bdist_wheel --universal
upload: build
	twine upload dist/*
