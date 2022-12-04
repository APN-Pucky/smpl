livehtml:
	poetry run $(MAKE) -C docs livehtml

html:
	poetry run $(MAKE) -C docs html

doc: html

install:
	poetry install --with dev --with docs --extras opt
	python3 -m pip install --user .[opt]

build:
	poetry build

test:
	rm -f .coverage coverage.xml
	find source/example/ -type f -name '*.ipynb' | xargs jupyter nbconvert --to script
	poetry run pytest

commit: 
	-git add .
	-git commit

push: commit
	git push

pull: commit
	git pull
	
doc: clean-all html
	@echo -n ""

clean-all: clean
	rm -rf build
	find source/example/ -type f -name '*.ipynb' | xargs jupyter nbconvert --clear-output --inplace


release: push html
	git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
	git push --tags
