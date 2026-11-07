.PHONY: pdf docx gifs inspect validate validate-strict test test-export check

CORE_RUN = uv run --with-requirements requirements/core.txt
PROFILE_PATH = $(if $(strip $(path)),$(path),data/profile.yaml)

pdf:
	@test -n "$(path)" || { echo "Usage: make pdf path=docs/resume/resume.md"; exit 2; }
	@uv run --with-requirements requirements/export.txt \
		python scripts/export_markdown.py "$(path)" --format pdf

docx:
	@test -n "$(path)" || { echo "Usage: make docx path=docs/resume/resume.md"; exit 2; }
	@uv run --with-requirements requirements/export.txt \
		python scripts/export_markdown.py "$(path)" --format docx

gifs:
	@uv run --with-requirements requirements/gif.txt \
		python scripts/create_terminal_demo_gif.py
	@uv run --with-requirements requirements/gif.txt \
		python scripts/create_workflow_gif.py

inspect:
	@$(CORE_RUN) python scripts/inspect_profile.py "$(PROFILE_PATH)"

validate:
	@$(CORE_RUN) python scripts/validate_profile.py "$(PROFILE_PATH)"

validate-strict:
	@$(CORE_RUN) python scripts/validate_profile.py "$(PROFILE_PATH)" --warnings-as-errors

test:
	@$(CORE_RUN) python -m unittest discover -s tests -v

test-export:
	@uv run --with-requirements requirements/export.txt \
		python -m unittest discover -s tests -p 'test_export_markdown.py' -v

check: test test-export validate
