# Project Writeup: Ancient DNA Population History

## Background

This project uses ancient DNA to look at two of the largest migration stories in human prehistory: the Bronze Age expansion of steppe pastoralists into Europe, and the peopling of the Americas. Both stories are subjects modern DNA alone couldn't fully reveal. It took sequencing the genomes of people who actually lived thousands of years ago to figure out what truly occurred. 

The data come from the Allen Ancient DNA Resource (AADR), a massive, curated dataset maintained by the Reich Lab at Harvard that combines genotypes from thousands of ancient and modern individuals into a single, clean dataset. I used the v66.p1 release (published in June 2026) and the "HO" (Human Origins) panel specifically, as it has a much richer set of modern reference populations than the alternative 1240K panel, which was crucial for building clean PCA axes. 

### Why project ancient samples instead of just running PCA on everyone together?

Ancient DNA is degraded and has way more missing data than modern genomes. If you just combine ancient and modern samples into a normal PCA together, the ancient samples' sparsity can distort the whole analysis in ways that would not represent true ancestry differences. The standard fix, which was done in this project, is to compute the PCA axes using only clean modern reference populations, and then mathematically project the ancient individuals onto those already defined axes afterward. This was done with `lsqproject: YES` within `smartpca`, combined with a `poplistname` file specifying which populations get to define the axes.
 

## Methods
*To be completed*

## Results
*To be completed*

## Interpretation
*To be completed*
