.DEFAULT_GOAL := help

.PHONY: install-global install-local uninstall-global test help

UV ?= uv
PACKAGE := ytt

install-global: ## Install ytt globally from the current checkout (forced reinstall)
	$(UV) tool install --force --from . $(PACKAGE)

install-local: ## Install ytt in editable mode with test extras (forced reinstall)
	$(UV) pip install --reinstall -e .[test]

uninstall-global: ## Uninstall the globally installed ytt tool
	$(UV) tool uninstall $(PACKAGE)

test: ## Run the test suite with pytest
	pytest

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'
