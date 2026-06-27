# Project Writeup: Ancient DNA Population History

## Background

This project uses ancient DNA to look at two of the largest migration stories in human prehistory: the Bronze Age expansion of steppe pastoralists into Europe, and the peopling of the Americas. Both stories are subjects modern DNA alone couldn't fully reveal. It took sequencing the genomes of people who actually lived thousands of years ago to figure out what truly occurred. 

The data come from the Allen Ancient DNA Resource (AADR), a massive, curated dataset maintained by the Reich Lab at Harvard that combines genotypes from thousands of ancient and modern individuals into a single, clean dataset. I used the v66.p1 release (published in June 2026) and the "HO" (Human Origins) panel specifically, as it has a much richer set of modern reference populations than the alternative 1240K panel, which was crucial for building clean PCA axes. 

### Why project ancient samples instead of just running PCA on everyone together?

Ancient DNA is degraded and has way more missing data than modern genomes. If you just combine ancient and modern samples into a normal PCA together, the ancient samples' sparsity can distort the whole analysis in ways that would not represent true ancestry differences. The standard fix, which was done in this project, is to compute the PCA axes using only clean modern reference populations, and then mathematically project the ancient individuals onto those already defined axes afterward. This was done with `lsqproject: YES` within `smartpca`, combined with a `poplistname` file specifying which populations get to define the axes.
 
## Methods

### Data source
- Allen Ancient DNA Resource v66.p1, Human Origins (HO) panel
- Downloaded from Harvard Dataverse: `v66.p1_HO.aadr.patch.PUB.geno/.snp/.ind`, plus the `.anno` annotation file
- 27,594 individuals total in the full dataset, ~584,000 SNPs

### Format obstacle
The v66.p1 release actually uses a brand-new binary format called TGENO (a transposed version of the standard packed EIGENSTRAT format), which had been published only about two weeks before I downloaded it. Neither the `apt`-installed EIGENSOFT nor the bioconda build could read it. Both failed immediately on the file header. The fix was to compile the latest version of `AdmixTools` directly from Reich Lab's source code, which includes built-in support for the new TGENO format. While standard tools failed, this custom build successfully handled the files. This resolved the bottleneck, and downstream tools like `smartpca` ran without issues because they only handle smaller, already-converted files.  

### Filtering individuals
For each case study, I used a Python script that scans the full `.ind` file and selects individuals matching specific population labels, while:
- Excluding individuals flagged with outlier suffixes (e.g., `-o`, `-1`, `-2`) that AADR uses to mark atypical individuals relative to their main population cluster
- Deduplicating individuals who appear multiple times under different data-processing suffixes (`.AG`, `.SG`, `.TW`, `.DG`), keeping the highest-quality version of each person
- Randomly subsampling large populations (some, like Yamnaya, have 200+ individuals in the AADR) down to a manageable number per group for a readable plot

### Extracting subset datasets
To get a self-contained `.geno`/`.snp`/`.ind` dataset for each case study (rather than depending on the full multi-gigabyte original files), I used `convertf` with a unique method from the EIGENSOFT documentation: rather than writing a short `.ind` file with only the selected individuals, I used a full-length `ind` file matching the original 27,594-individual count, where every non-selected individual is labeled `"Ignore"`. `convertf` then outputs a data set containing only the individuals with real population labels, while still satisfying its internal check that input file lengths are consistent. 

### Running smartpca
For each case study, modern reference populations were listed in a `poplistname` file and used with `lsqproject: YES` to build the PCA axes; ancient individuals were left out of that list and projected onto the resulting axes. I disabled the `numoutlieriter` (set to 0) since `smartpca` by default automatically removes individuals it considers outliers (which would have removed the exact ancient individuals I intended to study, since they are expected to look different from modern populations). 

## Results

### Bronze Age Europe

I included five ancient population groups and three modern reference populations:
- **Yamnaya** - Bronze Age steppe pastoralists from the Pontic-Caspian region (Russia, Ukraine, Kazakhstan, and neighboring areas)
- **Corded Ware** - an early culture in central/northern Europe with substantial steppe ancestry, descended from groups like Yamnaya
- **WHG (Western Hunter-Gatherers)** - pre-forming Mesolithic Europeans, including the well-known Loschbour and La Braña individuals, plus a cluster from the Iron Gates region of the Danube (Serbia/Romania)
- **LBK (Linear Pottery Culture)** - Early European Farmers, mostly from Germany, Austria, Slovakia, and Hungary
- **Turkey_N** - Anatolian Neolithic farmers, the ancestral source population for LBK
- Modern reference: **French, Russian, Sardinian** 

## Interpretation
*To be completed*
