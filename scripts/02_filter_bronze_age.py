"""
02_filter_bronze_age.py

Filters the AADR Human Origins (.ind) dataset down to a curated set of
ancient and modern individuals representing the Bronze Age steppe
expansion into Europe.

Populations included:
- WHG (Western Hunter-Gatherers): Mesolithic Europe, pre-farming
- Turkey_N (Anatolian Neolithic): ancestral source for European farmers
- LBK (Linear Pottery Culture): Early European Farmers
- Yamnaya: Pontic-Caspian steppe pastoralists (the migration source)
- Corded_Ware: early steppe-admixed culture in central/northern Europe
- Modern reference populations: French, Sardinian, Russian
- Yoruba: deep outgroup for PCA stability

Output: results/bronze_age/bronze_age.ind (filtered EIGENSTRAT .ind file)
"""

import re
import random
from collections import defaultdict

random.seed(42)  # reproducibility

INPUT_IND = "data/raw/v66.p1_HO.PUB.ind"
OUTPUT_IND = "results/bronze_age/bronze_age.ind"
MAX_PER_ANCIENT_GROUP = 25

# Ancient groups: (regex pattern to match population label, group name for logging)
# Countries/regions whose Mesolithic populations represent genuine Western
# Hunter-Gatherer (WHG) ancestry, as established in the population genetics
# literature. Excludes Russian, Siberian, Caucasus, and Central/East Asian
# Mesolithic groups, which represent distinct, non-WHG hunter-gatherer lineages.
WHG_COUNTRIES = [
    "Luxembourg_Loschbour", "Spain", "France", "Belgium", "Germany",
    "Serbia_IronGates", "Romania_IronGates", "England", "Scotland",
    "Wales", "Ireland", "Netherlands", "Sweden", "Denmark", "Norway",
]
WHG_PATTERN = r"^(" + "|".join(WHG_COUNTRIES) + r").*_Mesolithic$"

ANCIENT_PATTERNS = [
    (WHG_PATTERN, "WHG"),
    (r"^Switzerland_Epipaleolithic$", "WHG"),
    (r"^Turkey_N$", "Turkey_N"),
    (r"_LBK$", "LBK"),
    (r"_LBK_", "LBK"),
    (r"_Yamnaya$", "Yamnaya"),
    (r"_CordedWare$", "Corded_Ware"),
]

# Modern reference populations: exact label match
MODERN_POPS = {"French", "Sardinian", "Russian", "Yoruba"}

# Suffixes that flag outliers / atypical individuals -- exclude these
EXCLUDE_SUFFIX_PATTERN = re.compile(r"-o[A-Za-z]*$|-\d+$|Proto|alt")


def is_outlier(label: str) -> bool:
    """Return True if this individual's label marks them as an outlier
    or non-standard variant that we want to exclude from the clean set."""
    return bool(EXCLUDE_SUFFIX_PATTERN.search(label))


def get_base_id(sample_id: str) -> str:
    """Strip data-type suffixes (.AG, .SG, .TW, .DG, .AG.TW etc.) so we can
    deduplicate individuals sequenced/processed multiple ways."""
    return re.sub(r"\.(AG|SG|TW|DG|HO)(\.(AG|SG|TW|DG|HO))*$", "", sample_id)


def quality_rank(sample_id: str) -> int:
    """Lower is better. Used to pick the best version of a duplicated individual."""
    if sample_id.endswith(".DG"):
        return 0  # diploid genotype calls, highest quality
    if sample_id.endswith(".AG.TW") or sample_id.endswith(".TW.AG"):
        return 1  # merged capture, very good
    if sample_id.endswith(".SG"):
        return 2  # shotgun
    if sample_id.endswith(".AG"):
        return 3  # standard capture
    return 4


def main():
    ancient_by_group = defaultdict(list)
    modern_lines = []

    with open(INPUT_IND) as f:
        for line in f:
            parts = line.split()
            if len(parts) != 3:
                continue
            sample_id, sex, label = parts

            # Modern reference populations: keep all, exact match
            if label in MODERN_POPS:
                modern_lines.append((sample_id, sex, label))
                continue

            # Ancient populations: check against our regex patterns
            for pattern, group_name in ANCIENT_PATTERNS:
                if re.search(pattern, label) and not is_outlier(label):
                    ancient_by_group[group_name].append((sample_id, sex, label))
                    break

    # Deduplicate ancient individuals by base ID, keeping best quality version
    final_ancient_lines = []
    for group_name, entries in ancient_by_group.items():
        best_by_base_id = {}
        for sample_id, sex, label in entries:
            base_id = get_base_id(sample_id)
            if base_id not in best_by_base_id or quality_rank(sample_id) < quality_rank(best_by_base_id[base_id][0]):
                best_by_base_id[base_id] = (sample_id, sex, label)

        deduped = list(best_by_base_id.values())
        random.shuffle(deduped)
        selected = deduped[:MAX_PER_ANCIENT_GROUP]
        final_ancient_lines.extend(selected)

        print(f"{group_name}: {len(entries)} raw -> {len(deduped)} deduplicated -> {len(selected)} selected")

    print(f"\nModern reference individuals kept: {len(modern_lines)}")
    for pop in sorted(MODERN_POPS):
        count = sum(1 for _, _, label in modern_lines if label == pop)
        print(f"  {pop}: {count}")

    all_lines = final_ancient_lines + modern_lines

    with open(OUTPUT_IND, "w") as f:
        for sample_id, sex, label in all_lines:
            f.write(f"{sample_id}\t{sex}\t{label}\n")

    print(f"\nTotal individuals written to {OUTPUT_IND}: {len(all_lines)}")


if __name__ == "__main__":
    main()
