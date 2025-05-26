livehtml:
	hatch run docs:$(MAKE) -C docs livehtml

html:
	hatch run docs:$(MAKE) -C docs html

doc: html

install:
	python3 -m pip install --user .[full]

build:
	hatch build

test:
	rm -f .coverage coverage.xml
	MPLBACKEND=Agg hatch run test:pytest

commit: 
	-git add .
	-git commit

push: commit
	git push

pull: commit
	git pull

clean: 
	rm -r docs/build docs/source/_autosummary
	rm -r .eggs .pytest_cache *.egg-info
	find docs/source/example/ -type f -name '*.ipynb' | xargs jupyter nbconvert --clear-output --inplace


release: push html
	git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
	git push --tags
