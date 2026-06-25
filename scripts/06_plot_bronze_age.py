"""
06_plot_bronze_age.py

Visualizes the Bronze Age Europe PCA: PC1 vs PC2, with ancient populations
(Yamnaya, Corded_Ware, WHG, LBK, Turkey_N) plotted as triangles and modern
reference populations (French, Russian, Sardinian, Yoruba) plotted as circles.

Reads:  results/bronze_age/bronze_age.evec
Writes: results/bronze_age/bronze_age_pca.png
"""

import matplotlib.pyplot as plt

EVEC_FILE = "results/bronze_age/bronze_age.evec"
OUTPUT_PNG = "results/bronze_age/bronze_age_pca.png"

# Ancient populations: triangles. Modern populations: circles.
ANCIENT_GROUPS = {"Yamnaya", "Corded_Ware", "WHG", "LBK", "Turkey_N"}
MODERN_GROUPS = {"French", "Russian", "Sardinian"}

# Consistent color per population (same color used whether shown as
# triangle or circle, so related ancient/modern groups read clearly)
COLORS = {
    "Yamnaya": "#d62728",       # red
    "Corded_Ware": "#ff7f0e",   # orange
    "WHG": "#1f77b4",           # blue
    "LBK": "#2ca02c",           # green
    "Turkey_N": "#9467bd",      # purple
    "French": "#17becf",        # teal
    "Russian": "#8c564b",       # brown
    "Sardinian": "#e377c2",     # pink
    "Yoruba": "#7f7f7f",        # gray
}

# AADR labels in our .ind file are detailed strings (e.g. "Russia_Samara_EBA_Yamnaya").
# This maps those raw labels to our 9 clean group names for coloring/legend.
def classify(raw_label: str) -> str:
    if "Yamnaya" in raw_label:
        return "Yamnaya"
    if "CordedWare" in raw_label:
        return "Corded_Ware"
    if "Mesolithic" in raw_label or "Epipaleolithic" in raw_label:
        return "WHG"
    if "LBK" in raw_label:
        return "LBK"
    if raw_label == "Turkey_N":
        return "Turkey_N"
    if raw_label in MODERN_GROUPS:
        return raw_label
    return None  # shouldn't happen if our filtering was correct


def main():
    points = {}  # group_name -> {"x": [...], "y": [...]}

    with open(EVEC_FILE) as f:
        next(f)  # skip #eigvals header line
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            sample_id = parts[0]
            pc1 = float(parts[1])
            pc2 = float(parts[2])
            raw_label = parts[-1]

            group = classify(raw_label)
            if group is None:
                continue  # Yoruba and any other excluded groups land here noww

            points.setdefault(group, {"x": [], "y": [], "seen_coords": set()})

            # Round to 3 decimals to catch near-identical duplicate individuals
            # (same person under different sample IDs / data-type suffixes,
            # e.g. HGDP00903.HO and S_Russian-2.DG referring to one individual)
            coord_key = (round(pc1, 3), round(pc2, 3))
            if coord_key in points[group]["seen_coords"]:
                continue
            points[group]["seen_coords"].add(coord_key)

            points[group]["x"].append(pc1)
            points[group]["y"].append(pc2)

    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot modern populations first (circles), so ancient triangles draw on top
    for group in MODERN_GROUPS:
        if group not in points:
            continue
        ax.scatter(
            points[group]["x"], points[group]["y"],
            c=COLORS[group], marker="o", s=40, alpha=0.6,
            edgecolors="white", linewidths=0.5,
            label=group,
        )

    for group in ANCIENT_GROUPS:
        if group not in points:
            continue
        ax.scatter(
            points[group]["x"], points[group]["y"],
            c=COLORS[group], marker="^", s=70, alpha=0.85,
            edgecolors="black", linewidths=0.5,
            label=group,
        )
# A small number of individuals (a few "Russian"-labeled samples with
    # Siberian-shifted ancestry, and a couple of "French" outliers) fall far
    # outside the main cluster on PC2. We crop the view to the dense region
    # where the WHG/Farmer/Steppe structure is visible; the excluded points
    # are noted in WRITEUP.md rather than silently dropped from the data.
    ax.set_ylim(-0.03, 0.03)
    ax.set_xlabel("PC1", fontsize=12)
    ax.set_ylabel("PC2", fontsize=12)
    ax.set_title(
        "Bronze Age Steppe Expansion into Europe\n"
        "Ancient individuals (triangles) projected onto modern reference PCA (circles)",
        fontsize=13,
    )
    ax.legend(loc="best", fontsize=9, framealpha=0.9)
    ax.grid(alpha=0.2)

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=200)
    print(f"Saved plot to {OUTPUT_PNG}")

    # Print a quick summary so we can sanity-check group sizes before viewing the image
    print("\nGroup sizes plotted:")
    for group, data in points.items():
        print(f"  {group}: {len(data['x'])} individuals")


if __name__ == "__main__":
    main()
