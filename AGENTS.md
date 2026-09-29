# Working agreements

Keep this site small and static. Website files belong in `site/`; tooling and
deployment configuration stay outside it. Do not add a framework or runtime
JavaScript without a concrete need.

Preserve unrelated changes. Stage explicit files, inspect the staged diff and
make meaningful commits. Rebase feature branches onto `main` rather than merging
`main` into them.

Run `npm run check` before committing. The pre-commit hook formats staged files
and validates HTML; the pre-push hook requires Gitleaks on `PATH`. CI repeats
these checks before deployment. For layout changes, inspect desktop and narrow
mobile screens, keyboard focus and the contact link.

This is a public repository. Keep private source notes, pitch decks, customer
details, metrics and credentials out of commits. The landing page should remain
brief and suitable for a company in stealth.
