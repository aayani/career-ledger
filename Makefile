.PHONY: bootstrap require-venv pdf docx gifs inspect validate validate-strict test test-export check

PYTHON = .venv/bin/python
export UV_CACHE_DIR := $(CURDIR)/.uv-cache
PROFILE_PATH = $(if $(strip $(path)),$(path),data/profile.yaml)

bootstrap:
	@uv venv .venv
	@uv pip install --python $(PYTHON) \
		-r requirements/core.txt \
		-r requirements/export.txt \
		-r requirements/gif.txt

require-venv:
	@test -x "$(PYTHON)" || { echo "Run 'make bootstrap' first."; exit 2; }

pdf: require-venv
	@test -n "$(path)" || { echo "Usage: make pdf path=docs/resume/resume.md"; exit 2; }
	@$(PYTHON) scripts/export_markdown.py "$(path)" --format pdf

docx: require-venv
	@test -n "$(path)" || { echo "Usage: make docx path=docs/resume/resume.md"; exit 2; }
	@$(PYTHON) scripts/export_markdown.py "$(path)" --format docx

gifs: require-venv
	@$(PYTHON) scripts/create_terminal_demo_gif.py
	@$(PYTHON) scripts/create_workflow_gif.py

inspect: require-venv
	@$(PYTHON) scripts/inspect_profile.py "$(PROFILE_PATH)"

validate: require-venv
	@$(PYTHON) scripts/validate_profile.py "$(PROFILE_PATH)"

validate-strict: require-venv
	@$(PYTHON) scripts/validate_profile.py "$(PROFILE_PATH)" --warnings-as-errors

test: require-venv
	@$(PYTHON) -m unittest discover -s tests -v

test-export: require-venv
	@$(PYTHON) -m unittest discover -s tests -p 'test_export_markdown.py' -v

check: test test-export validate
