"""Shared portable dataset loading and quality-check helpers."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
IMAGE_DIR = ROOT / "images"

def read_student_data(path: Path = DATA_DIR / "student_data.csv") -> pd.DataFrame:
    """Read UCI student-mat.csv (semicolon delimited) and expose readable grade names."""
    if not path.exists():
        raise FileNotFoundError(f"Student dataset not found at {path}. See README.md for recovery steps.")
    frame = pd.read_csv(path, sep=";")
    return frame.rename(columns={"G1": "Period 1 Math Grade", "G2": "Period 2 Math Grade", "G3": "Math Score"})

def clean_frame(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Drop exact duplicate rows and impute missing values by type; report each operation."""
    before = len(frame)
    duplicated = int(frame.duplicated().sum())
    cleaned = frame.drop_duplicates().copy()
    missing_before = int(cleaned.isna().sum().sum())
    numeric = cleaned.select_dtypes(include="number").columns
    categorical = cleaned.select_dtypes(exclude="number").columns
    for col in numeric:
        if cleaned[col].isna().any():
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
    for col in categorical:
        if cleaned[col].isna().any():
            modes = cleaned[col].mode(dropna=True)
            cleaned[col] = cleaned[col].fillna(modes.iloc[0] if not modes.empty else "Unknown")
    return cleaned, {"rows_before": before, "duplicate_rows_removed": duplicated,
                     "rows_after": len(cleaned), "missing_cells_before_imputation": missing_before,
                     "missing_cells_after": int(cleaned.isna().sum().sum())}

def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
