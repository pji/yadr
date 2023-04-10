.PHONY: build
build:
	sphinx-build -b html docs/source/ docs/build/html
	python -m build
	twine check dist/*

.PHONY: clean
clean:
	rm -rf docs/build/html
	rm -rf dist
	rm -rf yadr.egg-info
	rm -rf tests/__pycache__
	rm -rf yadr/__pycache__

.PHONY: docs
docs:
	sphinx-build -b html docs/source/ docs/build/html

.PHONY: pre
pre:
	python precommit.py
	git status
