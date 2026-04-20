# ts-usp-paper

Manuscript repository for the Universal Sequence Preconditioning for Time Series paper. Synced with Overleaf.

## Layout

- `main.tex`, `references.bib`, `main.bbl` — primary manuscript
- `figures/` — final figures used by `main.tex` (PDF + PNG)
- `tables/` — auto-generated tables (if any)
- `aaai2027/`, `icml2026_workshop/`, `neurips2026/` — conference-specific variants (each self-contained with their own figures and style files)

Figures are generated in the sibling research repo at `../` (branch `spectral_non_precond`). To refresh figures here, run `../sync_figures.sh` from the research repo root.
