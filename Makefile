# Makefile for common developer tasks
# Usage examples:
#   make install
#   make test
#   make build
#   make release LEVEL=patch PUSH=1

SHELL := /bin/bash
.PHONY: install precommit-install test lint build bump-version release publish clean

install:
	poetry install --no-interaction --no-root

precommit-install:
	poetry run pip install --upgrade pre-commit
	poetry run pre-commit install

test:
	poetry run pytest -q

lint:
	poetry run pre-commit run --all-files

build:
	poetry build -P ./py_apze

# bump-version: usage: make bump-version LEVEL=patch (major|minor|patch)
bump-version:
	LEVEL=${LEVEL:=patch}; \
	python3 scripts/bump_version.py ${LEVEL}

# release: bump version, commit, tag. Usage: make release LEVEL=patch PUSH=1
release: bump-version
	GITROOT=$(shell git rev-parse --show-toplevel); \
	cd "$$GITROOT"; \
	NEWVER=$$(sed -n 's/^version *= *"\(.*\)"/\1/p' pyproject.toml | head -n1); \
	if [ -z "$$NEWVER" ]; then NEWVER=0.0.0; fi; \
	git add pyproject.toml; \
	git commit --no-verify -m "chore(release): bump version to $$NEWVER" || echo "No changes to commit"; \
	git tag -a v$$NEWVER -m "Release v$$NEWVER"; \
	if [ "${PUSH}" = "1" ]; then git push origin tag v$$NEWVER; fi

# publish uses poetry build + twine upload
publish: build
	python -m pip install --upgrade pip twine
	python -m twine upload dist/* # or poetry publish --build -P ./py_apze

clean:
	rm -rf build dist *.egg-info .venv
