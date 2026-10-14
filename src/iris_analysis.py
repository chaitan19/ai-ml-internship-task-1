"""Reproducible EDA for the genuine UCI Iris dataset."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_utils import DATA_DIR, IMAGE_DIR, clean_frame, ensure_dirs

FEATURES = ["sepal_length_cm", "sepal_width_cm", "petal_length_cm", "petal_width_cm"]

def run_iris_analysis() -> dict:
    ensure_dirs()
    path = DATA_DIR / "iris.csv"
    if not path.exists():
        raise FileNotFoundError(f"Iris data missing at {path}. Follow the UCI recovery instructions in README.md.")
    raw = pd.read_csv(path)
    cleaned, cleaning = clean_frame(raw)
    # Preserve all 150 source rows (including genuine repeated observations).
    cleaned.to_csv(DATA_DIR / "iris_cleaned.csv", index=False)
    numerical = cleaned[FEATURES]
    means = cleaned.groupby("species")[FEATURES].mean().round(3)
    summary = {"raw_shape": list(raw.shape), "cleaned_shape": list(cleaned.shape),
        "columns": cleaned.columns.tolist(), "dtypes": {k: str(v) for k,v in cleaned.dtypes.items()},
        "first_ten": cleaned.head(10).to_dict(orient="records"),
        "descriptive_statistics": numerical.describe().round(3).to_dict(),
        "missing_cells_before": int(raw.isna().sum().sum()), "missing_values_before": raw.isna().sum().to_dict(),
        "duplicate_rows_before": int(raw.duplicated().sum()), "cleaning": cleaning,
        "species_counts": cleaned["species"].value_counts().to_dict(),
        "species_means": {str(k): v.to_dict() for k,v in means.iterrows()},
        "correlation": numerical.corr().round(3).to_dict()}
    sns.set_theme(style="whitegrid", context="notebook")
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    for col, ax in zip(FEATURES, axes.flat):
        sns.histplot(data=cleaned, x=col, hue="species", element="step", stat="density", common_norm=False, ax=ax)
        ax.set(title=col.replace("_", " ").title(), xlabel="Measurement (cm)", ylabel="Density")
    fig.suptitle("Iris Measurement Distributions by Species"); fig.tight_layout()
    fig.savefig(IMAGE_DIR / "iris_histograms.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 6)); sns.scatterplot(data=cleaned, x="petal_length_cm", y="petal_width_cm", hue="species", s=60, ax=ax)
    ax.set(title="Iris Petal Measurements by Species", xlabel="Petal length (cm)", ylabel="Petal width (cm)")
    fig.tight_layout(); fig.savefig(IMAGE_DIR / "iris_scatter.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(11, 6)); sns.boxplot(data=cleaned.melt(id_vars="species", value_vars=FEATURES), x="variable", y="value", hue="species", ax=ax)
    ax.set(title="Iris Feature Distributions by Species", xlabel="Feature", ylabel="Measurement (cm)"); ax.tick_params(axis="x", rotation=15)
    fig.tight_layout(); fig.savefig(IMAGE_DIR / "iris_boxplot.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 6)); sns.heatmap(numerical.corr(), annot=True, fmt=".2f", cmap="vlag", center=0, square=True, ax=ax)
    ax.set_title("Iris Feature Correlation Heatmap"); fig.tight_layout(); fig.savefig(IMAGE_DIR / "iris_heatmap.png", dpi=160); plt.close(fig)
    (DATA_DIR.parent / "reports" / "iris_results.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    return summary

if __name__ == "__main__":
    result = run_iris_analysis()
    print(json.dumps({"shape": result["cleaned_shape"], "species_counts": result["species_counts"],
                      "missing": result["missing_cells_before"], "duplicates": result["duplicate_rows_before"]}, indent=2))
