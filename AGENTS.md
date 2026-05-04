# Repository Guidelines

## Project Structure & Module Organization

This repository contains manuscript sources for the Universal Sequence Preconditioning time-series paper. The root `main.tex`, `references.bib`, and compiled `main.pdf` are the primary manuscript. Submission-specific variants live in `icml2026_workshop/`, `csml_submission/`, `junior_paper/`, `aaai2027/`, and `neurips2026/`; treat each as self-contained unless a task explicitly asks for cross-copy updates. Shared or final paper assets are in `figures/` and `tables/`; variant-specific assets are usually under each submission folder, for example `icml2026_workshop/figures/`.

## Build, Test, and Development Commands

Compile the root paper with:

```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Compile a variant from its directory, for example:

```bash
cd icml2026_workshop
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Use `rg` for searches, e.g. `rg -n "Moirai-2|HD10|TODO" icml2026_workshop/main.tex`. If figures are regenerated in the sibling research repository, sync them into this repo rather than editing generated PDFs directly.

## Coding Style & Naming Conventions

Use concise LaTeX and keep notation consistent within each paper variant. Prefer semantic labels such as `tab:main`, `fig:arch`, and `eq:precond`. Keep table and figure captions self-contained but short. Avoid introducing new macros unless they reduce repeated notation across a section. Preserve anonymous formatting in workshop submissions.

## Testing Guidelines

There is no automated test suite. Verification means compiling the target PDF, checking the LaTeX log for errors, unresolved citations, and overfull boxes, and visually inspecting changed pages. For figure edits, render the PDF and confirm legends, labels, boxes, and arrows do not collide.

## Commit & Pull Request Guidelines

Recent commits use short imperative summaries such as `Update ICML workshop paper` or `Revise ICML workshop appendix`. Keep commits scoped to one paper or deliverable when possible. PRs or review requests should describe the paper variant changed, summarize content changes, mention whether the PDF was recompiled, and list any remaining compile warnings.

## Agent-Specific Instructions

Do not revert unrelated user edits. Avoid committing transient build files (`*.aux`, `*.log`, `*.blg`, video `build_video/`) unless explicitly requested. When updating a manuscript, edit the `.tex` source first, then recompile the corresponding PDF.
