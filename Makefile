.DEFAULT_GOAL := help

.PHONY: check clean-build fix format install-global install-local lint lint-fix package-smoke test uninstall-global help

UV ?= uv
UV_PYTHON ?= 3.12
UV_RUN ?= $(UV) run --python $(UV_PYTHON) --extra test
PACKAGE := ytt

install-global: ## Install ytt globally from the current checkout (forced reinstall)
	$(UV) tool install --force --from . $(PACKAGE)

install-local: ## Sync the local uv environment with test extras
	$(UV) sync --python $(UV_PYTHON) --extra test

uninstall-global: ## Uninstall the globally installed ytt tool
	$(UV) tool uninstall $(PACKAGE)

lint: ## Run ruff lint checks
	$(UV_RUN) ruff check .

lint-fix: ## Apply safe ruff lint fixes
	$(UV_RUN) ruff check --fix .

fix: lint-fix ## Apply safe automated fixes

clean-build: ## Remove generated package build artifacts
	$(UV_RUN) python -c "import shutil; [shutil.rmtree(path, ignore_errors=True) for path in ('build', 'dist', 'src/ytt.egg-info', 'ytt.egg-info', 'youtube_transcript_tool.egg-info')]"

format: ## Format Python code with ruff
	$(UV_RUN) ruff format .

test: ## Run the test suite with pytest
	$(UV_RUN) pytest

package-smoke: clean-build ## Build source and wheel distributions
	$(UV_RUN) python -m build --sdist --wheel --no-isolation

check: lint test package-smoke ## Run the default local verification suite

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'
