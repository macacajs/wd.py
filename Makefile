all: install
install:
	pip install sphinx
doc: install
	sphinx-build -b html docsrc docs
build:
	python setup.py sdist build
upload:
	python setup.py sdist upload
build_wheel:
	python setup.py bdist_wheel --universal
upload_wheel:
	python setup.py bdist_wheel upload
