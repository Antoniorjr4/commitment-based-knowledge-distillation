#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
pandoc manuscript_en.md --from=markdown+tex_math_single_backslash+autolink_bare_uris --standalone --number-sections --include-in-header=header.tex -V documentclass=article -V fontsize=10pt -V geometry:margin=0.85in -V colorlinks=true -V linkcolor=black -V urlcolor=blue -o manuscript_en.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript_en.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript_en.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript_en.tex
