.DEFAULT_GOAL := help

.PHONY: install-global install-local test help

UV ?= uv
PACKAGE := ytt
GIT_URL := git+https://github.com/dudarev/ytt.git

install-global: ## Install ytt globally using uv from the GitHub repository (forced reinstall)
	$(UV) tool install --force --from $(GIT_URL) $(PACKAGE)

install-local: ## Install ytt in editable mode with test extras (forced reinstall)
	$(UV) pip install --reinstall -e .[test]

test: ## Run the test suite with pytest
	$(UV) run pytest

help: ## Show available targets
@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'
