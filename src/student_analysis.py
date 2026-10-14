"""Reproducible UCI Student Performance mathematics EDA and chart generation."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from data_utils import DATA_DIR, IMAGE_DIR, clean_frame, ensure_dirs, read_student_data

def run_student_analysis() -> dict:
    ensure_dirs()
    raw = read_student_data()
    cleaned, cleaning = clean_frame(raw)
    cleaned.to_csv(DATA_DIR / "student_data_cleaned.csv", index=False)
    score = cleaned["Math Score"]
    mode_values = score.mode().tolist()
    numeric = cleaned.select_dtypes(include="number")
    summary = {
        "dataset": "UCI Student Performance - Mathematics (student-mat.csv)",
        "raw_shape": list(raw.shape), "cleaned_shape": list(cleaned.shape),
        "columns": cleaned.columns.tolist(), "dtypes": {k: str(v) for k, v in cleaned.dtypes.items()},
        "first_ten": cleaned.head(10).to_dict(orient="records"),
        "descriptive_statistics": numeric.describe().round(3).to_dict(),
        "math_score": {"mean": float(score.mean()), "median": float(score.median()),
                       "mode": mode_values, "min": int(score.min()), "max": int(score.max()),
                       "std": float(score.std()), "q1": float(score.quantile(.25)), "q3": float(score.quantile(.75))},
        "missing_values_before": raw.isna().sum().to_dict(),
        "missing_cells_before": int(raw.isna().sum().sum()),
        "duplicate_rows_before": int(raw.duplicated().sum()), "cleaning": cleaning,
        "correlation_g1_g3": float(cleaned["Period 1 Math Grade"].corr(score)),
        "correlation_g2_g3": float(cleaned["Period 2 Math Grade"].corr(score)),
        "school_mean_math": {str(k): float(v) for k, v in cleaned.groupby("school")["Math Score"].mean().items()},
        "iqr_outlier_count": int(((score < score.quantile(.25) - 1.5*(score.quantile(.75)-score.quantile(.25))) |
                                   (score > score.quantile(.75) + 1.5*(score.quantile(.75)-score.quantile(.25)))).sum()),
    }
    sns.set_theme(style="whitegrid", context="notebook")
    fig, ax = plt.subplots(figsize=(8, 5)); sns.histplot(score, bins=20, kde=True, ax=ax, color="#2864a5")
    ax.set(title="Distribution of Final Mathematics Scores", xlabel="Final grade (0-20)", ylabel="Number of students")
    fig.tight_layout(); fig.savefig(IMAGE_DIR / "math_score_histogram.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4)); sns.boxplot(x=score, ax=ax, color="#70b7a5")
    ax.set(title="Final Mathematics Scores and Potential Outliers", xlabel="Final grade (0-20)"); fig.tight_layout()
    fig.savefig(IMAGE_DIR / "math_score_boxplot.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 5)); sns.scatterplot(data=cleaned, x="Period 1 Math Grade", y="Math Score", hue="school", alpha=.75, ax=ax)
    ax.set(title="Earlier and Final Mathematics Grades", xlabel="Period 1 grade (G1)", ylabel="Final grade (G3)")
    fig.tight_layout(); fig.savefig(IMAGE_DIR / "math_scatter_plot.png", dpi=160); plt.close(fig)
    corr = numeric.corr()
    fig, ax = plt.subplots(figsize=(13, 10)); sns.heatmap(corr, cmap="vlag", center=0, ax=ax, square=False)
    ax.set_title("Correlation Heatmap of Numerical Student Attributes"); fig.tight_layout()
    fig.savefig(IMAGE_DIR / "correlation_heatmap.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 5)); sns.barplot(data=cleaned, x="school", y="Math Score", errorbar="sd", ax=ax, palette="muted", hue="school", legend=False)
    ax.set(title="Average Mathematics Score by School", xlabel="School", ylabel="Mean final grade (0-20)")
    fig.tight_layout(); fig.savefig(IMAGE_DIR / "average_score_by_school.png", dpi=160); plt.close(fig)
    (DATA_DIR.parent / "reports").mkdir(exist_ok=True)
    (DATA_DIR.parent / "reports" / "student_results.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    return summary

if __name__ == "__main__":
    result = run_student_analysis()
    print(json.dumps({"raw_shape": result["raw_shape"], "cleaned_shape": result["cleaned_shape"],
                      "score": result["math_score"], "cleaning": result["cleaning"]}, indent=2))
