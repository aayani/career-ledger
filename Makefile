.PHONY: pdf inspect validate validate-complete validate-strict test check

CORE_RUN = uv run --with-requirements requirements/core.txt
PROFILE_PATH = $(if $(strip $(path)),$(path),data/profile.yaml)

# Usage: make pdf path=docs/resume/backend.md
pdf:
	@test -n "$(path)" || { echo "Usage: make pdf path=docs/resume/backend.md"; exit 2; }
	@uv run --with-requirements requirements/pdf.txt \
		python scripts/markdown_to_pdf.py "$(path)"

inspect:
	@$(CORE_RUN) python scripts/inspect_profile.py "$(PROFILE_PATH)"

validate:
	@$(CORE_RUN) python scripts/validate_profile.py "$(PROFILE_PATH)"

validate-complete:
	@$(CORE_RUN) python scripts/validate_profile.py "$(PROFILE_PATH)" --require-complete

validate-strict:
	@$(CORE_RUN) python scripts/validate_profile.py "$(PROFILE_PATH)" --warnings-as-errors

test:
	@$(CORE_RUN) python -m unittest discover -s tests -v

check: test validate
