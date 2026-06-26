"""
07_plot_americas.py

Visualizes the Americas PCA: PC1 vs PC2, showing the peopling of the
Americas. Modern reference populations (Han, Karitiana, Surui, Mayan, Pima)
are plotted as circles. Ancient groups (Ancient_California, Ancient_Maya)
are plotted as triangles. Named landmark individuals (Anzick, Kennewick,
USR1, USR2, TrailCreek, AHUR samples) get large star markers with text
labels, since they're the narrative anchors of this case study.

Reads:  results/americas/americas.evec
Writes: results/americas/americas_pca.png
"""

import matplotlib.pyplot as plt
from adjustText import adjust_text

EVEC_FILE = "results/americas/americas.evec"
OUTPUT_PNG = "results/americas/americas_pca.png"

MODERN_GROUPS = {"Han", "Karitiana", "Surui", "Mayan", "Pima"}

# Named landmark individuals: raw .evec label -> (display name, color)
NAMED_INDIVIDUALS = {
    "USA_AncientBeringian": "Ancient Beringian (USR1/USR2)",
    "USA_Anzick_12700BP": "Anzick (~12,700 BP)",
    "USA_WA_Kennewick_8800BP": "Kennewick Man (~8,800 BP)",
    "USA_9000BP": "Trail Creek (~9,000 BP)",
    "USA_11000BP": "Ancient Beringian (~11,000 BP)",
}

COLORS = {
    "Han": "#9467bd",
    "Karitiana": "#2ca02c",
    "Surui": "#17becf",
    "Mayan": "#ff7f0e",
    "Pima": "#1f77b4",
    "Ancient_California": "#8c564b",
    "Ancient_Maya": "#e377c2",
    "Ancient Beringian (USR1/USR2)": "#d62728",
    "Anzick (~12,700 BP)": "#d62728",
    "Kennewick Man (~8,800 BP)": "#d62728",
    "Trail Creek (~9,000 BP)": "#d62728",
    "Ancient Beringian (~11,000 BP)": "#d62728",
}


def classify(raw_label: str):
    """Returns (group_name, is_named_individual)"""
    if raw_label in NAMED_INDIVIDUALS:
        return NAMED_INDIVIDUALS[raw_label], True
    if raw_label in MODERN_GROUPS:
        return raw_label, False
    if raw_label.startswith("USA_California_"):
        return "Ancient_California", False
    if "Maya" in raw_label:
        return "Ancient_Maya", False
    return None, False


def main():
    points = {}       # group_name -> {"x": [...], "y": [...], "seen_coords": set()}
    named_points = {}  # display_name -> {"x": [...], "y": [...], "labels": [...]}

    with open(EVEC_FILE) as f:
        next(f)  # skip #eigvals header
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            sample_id = parts[0]
            pc1 = float(parts[1])
            pc2 = float(parts[2])
            raw_label = parts[-1]

            group, is_named = classify(raw_label)
            if group is None:
                continue

            coord_key = (round(pc1, 3), round(pc2, 3))

            if is_named:
                named_points.setdefault(group, {"x": [], "y": [], "labels": []})
                named_points[group]["x"].append(pc1)
                named_points[group]["y"].append(pc2)
                named_points[group]["labels"].append(sample_id)
            else:
                points.setdefault(group, {"x": [], "y": [], "seen_coords": set()})
                if coord_key in points[group]["seen_coords"]:
                    continue
                points[group]["seen_coords"].add(coord_key)
                points[group]["x"].append(pc1)
                points[group]["y"].append(pc2)

    fig, ax = plt.subplots(figsize=(11, 9))

    # Modern reference populations: circles
    for group in MODERN_GROUPS:
        if group not in points:
            continue
        ax.scatter(
            points[group]["x"], points[group]["y"],
            c=COLORS[group], marker="o", s=28, alpha=0.45,
            edgecolors="white", linewidths=0.5,
            label=group,
        )

    # Ancient subsampled groups: triangles
    for group in ("Ancient_California", "Ancient_Maya"):
        if group not in points:
            continue
        ax.scatter(
            points[group]["x"], points[group]["y"],
            c=COLORS[group], marker="^", s=60, alpha=0.8,
            edgecolors="black", linewidths=0.5,
            label=group.replace("_", " "),
        )

    # Named landmark individuals: large stars, with text labels
    # Manual per-individual label offsets (x_offset, y_offset in points),
    # chosen by hand since only 6 labels exist and automatic placement
    # was adding unnecessary leader lines for points that didn't need them.
    LABEL_OFFSETS = {
        "USR1.SG": (10, 8),
        "USR2.SG": (10, -10),
        "TrailCreek.SG": (10, -2),
        "AHUR_2064.SG": (-10, -14),
        "AHUR770c.SG": (-75, 8),
        "Anzick.SG": (10, -2),
        "kennewick.SG": (10, 8),
    }

    for display_name, data in named_points.items():
        ax.scatter(
            data["x"], data["y"],
            c=COLORS[display_name], marker="*", s=320, alpha=0.95,
            edgecolors="black", linewidths=1.0,
            label=display_name, zorder=5,
        )
        for x, y, sample_id in zip(data["x"], data["y"], data["labels"]):
            offset = LABEL_OFFSETS.get(sample_id, (10, 8))
            ax.annotate(
                sample_id, (x, y),
                textcoords="offset points", xytext=offset,
                fontsize=7.5, fontweight="bold", zorder=6,
            )

    ax.set_xlim(-0.095, 0.065)
    ax.set_xlabel("PC1", fontsize=12)
    ax.set_ylabel("PC2", fontsize=12)
    ax.set_title(
        "The Peopling of the Americas\n"
        "Named landmark individuals (stars) and subsampled ancient groups (triangles)\n"
        "projected onto modern reference PCA (circles)",
        fontsize=13,
    )
    ax.legend(loc="best", fontsize=8, framealpha=0.9)
    ax.grid(alpha=0.2)

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=200)
    print(f"Saved plot to {OUTPUT_PNG}")

    print("\nModern/ancient group sizes plotted:")
    for group, data in points.items():
        print(f"  {group}: {len(data['x'])} individuals")

    print("\nNamed landmark individuals plotted:")
    for display_name, data in named_points.items():
        print(f"  {display_name}: {data['labels']}")


if __name__ == "__main__":
    main()
