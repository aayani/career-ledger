.PHONY: pdf validate validate-complete test check

# Usage: make pdf path=docs/resume/backend.md
pdf:
	@test -n "$(path)" || { echo "Usage: make pdf path=docs/resume/backend.md"; exit 2; }
	@uv run --with-requirements requirements/base.txt \
		python scripts/markdown_to_pdf.py "$(path)"

validate:
	@python3 scripts/validate_career.py

validate-complete:
	@python3 scripts/validate_career.py --require-complete

test:
	@python3 -m unittest discover -s tests -v

check: test validate
