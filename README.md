# Ancient DNA Population History

A population genomics project using ancient DNA to reconstruct two of the most dramatic migration events in human prehistory:

1. **Bronze Age steppe expansion into Europe** (~5,000-4,000 years ago)
2. **The peopling of the Americas** (~15,000+ years ago)

This project builds on the population structure and ancestry estimation methods from `1kg-pop-structure`, applied here to ancient individuals projected onto modern reference populations.

## What this project does

Using genotype data from thousands of ancient and modern individuals, this project runs PCA with ancient samples projected onto axes built from modern reference populations, recovering two well-documented findings from the ancient DNA literature directly from raw data: 

- The three-way ancestry structure of modern Europeans (hunter-gatherer, Anatolian farmer, and steppe pastoralist), including the Yamnaya-associated migration into Europe during the Bronze Age
- The deep split between the "Ancient Beringian" lineage (represented by individuals from the Upward Sun River site in Alaska) and the rest of the Native American population, alongside landmark individuals like the Clovis-era Anzick child and Kennewick Man

## Data source 

Allen Ancient DNA Resource (AADR) v66.p1, Human Origins (HO) panel — Reich Lab, Harvard University, downloaded via Harvard Dataverse.

## Repository structure

```
adna-pophistory/
|-- config/
|  |--samples. txt                    # metadata for selected individuals
|-- data/
|  |-- raw/                           # AADR downloaded files (gitignored - too large)
|-- results/
|  |-- bronze_age/                    # filtered data, PCA output, and figure for Europe analysis
|  |-- americas/                      # filtered data, PCA output, and figure for Americas analysis
|-- scripts/
| |-- 02_filter_bronze_age.py         # subset to Bronze Age Europe individuals
| |-- 03_filter_americas.py           # subset to Americas individuals
| |-- 04a_convertf_bronze_age.par     # convertf parameter file (Bronze Age)
| |-- 04b_convertf_americas.par       # convertf parameter file (Americas)
| |-- 05a_smartpca_bronze_age.par     # smartpca parameter file (Bronze Age)
| |-- 05b_smartpca_americas.par       # smartpca parameter file (Americas)
| |-- 06_plot_bronze_age.py           # PCA figure for Bronze Age Europe
| |-- 07_plot_americas.py             # PCA figure for Americas
| |-- bronze_age_poplist.txt          # modern populations used to build Bronze Age PCA axes
| |-- americas_poplist.txt            # modern populations used to build Americas PCA axes
|-- environment.yml
|-- .gitignore
|-- README.md
|-- WRITEUP.md
```

## Tools

- **EIGENSOFT** (`smartpca`) for PCA with ancient-sample projection — installed via `sudo apt install eigensoft` on Ubuntu/WSL, since the bioconda build has a `libgfortran` compatibility issue with modern systems
- **AdmixTools** (`convertf`), compiled from source from [DReichLab/AdmixTools](https://github.com/DReichLab/AdmixTools) — required for reading the AADR v66.p1 release's new TGENO binary format, which older EIGENSOFT builds (including the apt and bioconda versions) cannot read
- **Python** (pandas, matplotlib) for filtering individuals and generating figures
- **conda** for Python environment management

## Installation notes
 
- EIGENSOFT must be installed via `sudo apt install eigensoft` on Ubuntu/WSL — the bioconda build has a libgfortran compatibility issue with modern systems
- `convertf` must be compiled from source (`DReichLab/AdmixTools`) to read the AADR v66.p1 TGENO format; the apt-installed and bioconda `convertf` builds will fail with a `bad ID (SNP): TGENO` error on this dataset
- All other dependencies are managed via conda: `conda env create -f environment.yml`

## Status
 
Complete. Both case studies have filtered datasets, PCA results, final figures, and a full writeup.
 
See [WRITEUP.md](WRITEUP.md) for the full background, methods, results, and interpretation.
