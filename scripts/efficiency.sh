#!/bin/bash -x

python efficiency_hist.py
python -c 'from efficiency_hist import add_legend; add_legend(True)'

pdfcrop efficiency_legend.pdf efficiency_legend.pdf
pdfcrop runtimes.pdf runtimes.pdf
pdfcrop memory_usage.pdf memory_usage.pdf

pdftops -eps efficiency_legend.pdf
pdftops -eps runtimes.pdf
pdftops -eps memory_usage.pdf

latex efficiency.tex
dvipdf efficiency.dvi
pdfcrop efficiency.pdf efficiency.pdf
pdftoppm -png efficiency.pdf > efficiency.png

mv efficiency.pdf ../plots/
mv efficiency.png ../plots/
rm efficiency.aux
rm efficiency.dvi
rm efficiency.log
rm efficiency_legend.eps
rm runtimes.eps
rm memory_usage.eps
rm efficiency_legend.pdf
rm runtimes.pdf
rm memory_usage.pdf
