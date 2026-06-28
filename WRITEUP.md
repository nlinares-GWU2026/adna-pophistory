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

The PCA (PC1 vs PC2) showed a clear gradient that matches the well-established picture of European population history: Sardinians (who retain the highest genetic affinity to Early European Farmers of any modern European population) sit at one end, the true ancient farmers (Turkey_N and LBK) cluster near them, French sit in an intermediate position, and Yamnaya/Corded Ware/WHG/Russian cluster together at the other end. This lines up with the standard model, where modern Europeans are a mix of three ancestral components: hunter-gatherer, Anatolian farmer, and steppe pastoralist. 

**Note** A small number of individuals labeled "Russian" in AADR exhibited a much more Siberian-shifted ancestry than the bulk of the Russian sample. This is likely because Russia spans an enormous geographic range, but it resulted in a few points being placed far outside the main cluster and would have compressed the rest of the plot if left in view. Rather than removing them from the analysis, I kept them in the data but set the plot's axis limits to focus on the dense, interpretable region. The same was true for one or two French individuals. I also excluded Yoruba (originally included as a deep outgroup) from the final plot, since it was not part of the population list used to build PCA axes and ended up landing in an uninformative spot in the middle of the plot, rather than off to the side, which could have been confusing to analyze. 

### The Peopling of the Americas

This case study utilized a robust dataset, as the v66.p1 AADR release incorporates several highly significant ancient individuals: 

- **Anzick** (~12,700 years old) - a Clovis culture infant burial from Montana, one of the oldest and most complete ancient Native American genomes to be sequenced
- **Kennewick Man** (~8,000 years old) - found in Washington State, the individual was the subject of a 20-year legal dispute under the National American Graves Protection and Repatriation Act (NAGPRA) between the U.S. Army Corps of Engineers and a coalition of Native American tribes seeking repatriation. Genetic analysis ultimately confirmed close affinity to modern Native American populations, which played a role in the case's resolution.
- **USR1 and USR2** ("Ancient Beringian," ~11,500 years old) - two infants from the Upward Sun River site in Alaska, representing a distinct, deeply diverged lineage split off from the ancestors of all other Native Americans before that population moved further south
- **AHUR_2064 and AHUR770c** (~11,000 years old) and the **Trail Creek** (~9,000 years old) - additional early Alaskan individuals
- A subsampled series of **Ancient California** individuals spanning roughly 3,000-7,400 years ago, and a set of **Ancient Maya** individuals from Belize and Mexico spanning the Archaic period
- Modern reference populations: **Han** (East Asian, serving as a proxy for the ancestral Asian source population), **Karitiana** and **Surui** (Amazonian Brazil), and **Pima** (Native American tribe indigenous to south-central Arizona)

The PCA showed a striking and biologically meaningful pattern: USR1, USR2, and Trail Creek consistently sat apart from the main ancient cluster (which included Anzick, Kennewick, the AHUR individuals, Ancient California, and Ancient Maya), positioned partway between Han and that main cluster

## Interpretation
*To be completed*
