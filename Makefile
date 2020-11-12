commit:
		-git add .
		-git commit
push: commit
		git push

release: push
		git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(v\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
		git push --tags


pull: commit
		git pull

