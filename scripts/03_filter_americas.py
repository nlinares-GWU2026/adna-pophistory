"""
03_filter_americas.py

Filters the AADR Human Origins (.ind) dataset down to a curated set of
ancient and modern individuals representing the peopling of the Americas.

Populations included:
- USA_AncientBeringian (USR1/USR2, ~11,500 BP): the deepest known Native
  American-related lineage, split off before all other Native Americans
- USA_Anzick (~12,700 BP): Clovis-era infant burial, Montana
- USA_WA_Kennewick (~8,800 BP): landmark individual with major legal/ethical
  history (NAGPRA repatriation dispute), confirmed close to modern
  Native Americans
- USA_California series (~3,000-7,400 BP): mid-Holocene time-depth samples
- Belize/Mexico ancient Maya (Archaic through Colonial): Mesoamerican branch
- Modern reference populations: Karitiana, Surui, Mayan, Pima
- Han, Yoruba: East Asian ancestral proxy and African deep outgroup

Output: results/americas/americas.ind (full-length EIGENSTRAT .ind file,
non-selected individuals marked "Ignore" for convertf subsetting)
"""

import re
import random
from collections import defaultdict

random.seed(42)

INPUT_IND = "data/raw/v66.p1_HO.PUB.ind"
OUTPUT_IND = "results/americas/americas.ind"

MAX_CALIFORNIA = 18
MAX_MAYA = 10

NAMED_PATTERNS = [
    (r"^USA_AncientBeringian$", "Ancient_Beringian"),
    (r"^USA_Anzick_12700BP$", "Anzick"),
    (r"^USA_WA_Kennewick_8800BP$", "Kennewick"),
    (r"^USA_9000BP$", "TrailCreek"),
    (r"^USA_11000BP$", "Ancient_Beringian_11kBP"),
]

SUBSAMPLE_PATTERNS = [
    (r"^USA_California_\d+BP$", "Ancient_California", MAX_CALIFORNIA),
    (r".*Archaic.*Maya$|.*Maya$", "Ancient_Maya", MAX_MAYA),
]

MODERN_POPS = {"Karitiana", "Surui", "Mayan", "Pima", "Han", "Yoruba"}

EXCLUDE_PATTERN = re.compile(r"-o[A-Za-z]*$|-\d+$|alt|Colonial")


def is_excluded(label):
    return bool(EXCLUDE_PATTERN.search(label))


def get_base_id(sample_id):
    return re.sub(r"\.(AG|SG|TW|DG|HO)(\.(AG|SG|TW|DG|HO))*$", "", sample_id)


def quality_rank(sample_id):
    if sample_id.endswith(".DG"):
        return 0
    if sample_id.endswith(".AG.TW") or sample_id.endswith(".TW.AG"):
        return 1
    if sample_id.endswith(".SG"):
        return 2
    if sample_id.endswith(".AG"):
        return 3
    return 4


def dedupe(entries):
    best_by_base_id = {}
    for sample_id, sex, label in entries:
        base_id = get_base_id(sample_id)
        if base_id not in best_by_base_id or quality_rank(sample_id) < quality_rank(best_by_base_id[base_id][0]):
            best_by_base_id[base_id] = (sample_id, sex, label)
    return list(best_by_base_id.values())


def main():
    named_lines = []
    subsample_by_group = defaultdict(list)
    modern_lines = []

    with open(INPUT_IND) as f:
        for line in f:
            parts = line.split()
            if len(parts) != 3:
                continue
            sample_id, sex, label = parts

            if label in MODERN_POPS:
                modern_lines.append((sample_id, sex, label))
                continue

            if is_excluded(label):
                continue

            matched = False
            for pattern, group_name in NAMED_PATTERNS:
                if re.match(pattern, label):
                    named_lines.append((sample_id, sex, label))
                    matched = True
                    break
            if matched:
                continue

            for pattern, group_name, _ in SUBSAMPLE_PATTERNS:
                if re.search(pattern, label):
                    subsample_by_group[group_name].append((sample_id, sex, label))
                    break

    named_lines = dedupe(named_lines)
    print("Named landmark individuals kept:")
    for sample_id, sex, label in named_lines:
        print(f"  {sample_id}\t{label}")

    final_subsample_lines = []
    max_lookup = {name: max_n for _, name, max_n in SUBSAMPLE_PATTERNS}
    for group_name, entries in subsample_by_group.items():
        deduped = dedupe(entries)
        random.shuffle(deduped)
        selected = deduped[:max_lookup[group_name]]
        final_subsample_lines.extend(selected)
        print(f"\n{group_name}: {len(entries)} raw -> {len(deduped)} deduplicated -> {len(selected)} selected")

    print(f"\nModern reference individuals kept: {len(modern_lines)}")
    for pop in sorted(MODERN_POPS):
        count = sum(1 for _, _, label in modern_lines if label == pop)
        print(f"  {pop}: {count}")

    all_lines = named_lines + final_subsample_lines + modern_lines
    selected_lookup = {sample_id: (sex, label) for sample_id, sex, label in all_lines}

    written = 0
    with open(INPUT_IND) as f_in, open(OUTPUT_IND, "w") as f_out:
        for line in f_in:
            parts = line.split()
            if len(parts) != 3:
                f_out.write(line)
                continue
            sample_id, sex, label = parts
            if sample_id in selected_lookup:
                sex, label = selected_lookup[sample_id]
                f_out.write(f"{sample_id}\t{sex}\t{label}\n")
                written += 1
            else:
                f_out.write(f"{sample_id}\t{sex}\tIgnore\n")

    print(f"\nFull-length .ind file written to {OUTPUT_IND}")
    print(f"Selected individuals (real labels): {written}")


if __name__ == "__main__":
    main()
