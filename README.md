# Ancient DNA Population History

A population genomics project using ancient DNA to reconstruct two of the most dramatic migration events in human prehistory:

1. **Bronze Age steppe expansion into Europe** (~5,000-4,000 years ago)
2. **The peopling of the Americas** (~15,000+ years ago)

## Data source 
Allen Ancient DNA Resource (AADR) v54.1 - Reich Lab, Harvard University

## Tools
EIGENSOFT (smartpca), Python, conda

## Status 
In progress

## Installation notes
- EIGENSOFT must be installed via `sudo apt install eigensoft` on Ubuntu/WSL — the bioconda build has a libgfortran compatibility issue with modern systems
- All other dependencies are managed via conda: `conda env create -f environment.yml`
