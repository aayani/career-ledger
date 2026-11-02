.PHONY: pdf inspect validate validate-strict test test-export check

CORE_RUN = uv run --with-requirements requirements/core.txt
PROFILE_PATH = $(if $(strip $(path)),$(path),data/profile.yaml)

# Usage: make pdf path=docs/resume/resume.md (writes PDF and DOCX)
pdf:
	@test -n "$(path)" || { echo "Usage: make pdf path=docs/resume/resume.md"; exit 2; }
	@uv run --with-requirements requirements/export.txt \
		python scripts/export_markdown.py "$(path)"

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
		python -m unittest discover -s tests -p 'test_export_markdown.py' \
		-k docx_preserves_links_and_a4_styling -v

check: test test-export validate
