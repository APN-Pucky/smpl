# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile install
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

install:
	python3 -m pip install --user .

build:
	python3 -m build

livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) --watch smpl/

test:
	find source/example/ -type f -name '*.ipynb' | xargs jupyter nbconvert --to script
	pytest -v --cov=smpl --cov-config=.coveragerc --cov-append  --cov-report=term --cov-report=xml --doctest-modules

commit: 
	-git add .
	-git commit

push: commit
	git push

pull: commit
	git pull

clean-all: clean
	find source/example/ -type f -name '*.ipynb' | xargs jupyter nbconvert --clear-output --inplace


release: push html
	git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
	git push --tags
