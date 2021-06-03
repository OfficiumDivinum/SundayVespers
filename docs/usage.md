# About this repository

There are quite a few tools out there to make producing high-quality chant
booklets easy.  The [gregorio](https://gregorio-project.github.io/) project
makes setting chant extremely easy; TeX and LaTeX make producing beautiful
booklets as easy as writing a markup language dreamed up in the days when
redefining a looping macro to null to get out of a loop seemed reasonable, and
GitHub will host anything and build anything, hopefully for the indefinite
future.

This repository is designed to make it easy to *tinker*. I have deliberately
avoided trying to automate everything. Each booklet makes sense by hand: the
propers are defined as macros in `propers.tex`, the layout is in `vespers.tex`
and there is a makefile so you don't have to remember how to compile. The goal
is to make the whole thing maintainable in the long term by anyone with at least
a basic knowledge of LaTeX and the ability to read a readme.

The original layout was written by John (@2e0byo) and the logo was drawn by
Endre (@kormose).
