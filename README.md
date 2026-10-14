# AI/ML Internship Task 1

A beginner-friendly, reproducible project for Python foundations, exploratory data analysis (EDA), and Git workflows. It contains a Student Performance mathematics analysis and a complete Iris EDA challenge, based on genuine UCI data.

## Objectives

- Demonstrate core Python data types, operators, control flow, collections, functions, file handling, and error handling.
- Inspect and clean UCI's semicolon-delimited Student Performance mathematics data without changing the raw file.
- Explore real Iris data with descriptive statistics, species comparisons, and plots.
- Produce two top-to-bottom executable notebooks, reusable scripts, nine figures, Mermaid diagrams, and a populated Markdown/PDF report.

## Requirements

- Windows 10/11 and Python 3.12 or later (validated here with Python 3.13.7).
- Git is recommended for version control. VS Code with Python and Jupyter extensions is recommended for notebooks.
- Internet access is needed only to download the datasets or packages.

## Setup (PowerShell)

Open PowerShell in this project directory (`AI-ML-Internship`) and run:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Command Prompt activation is:

```bat
.venv\Scripts\activate.bat
```

## Data sources and attribution

- Student mathematics subset: [UCI Student Performance, dataset 320](https://archive.ics.uci.edu/dataset/320/student), specifically `student-mat.csv` from UCI's `student+performance.zip`. It has 395 observations and uses semicolon delimiters. Keep `data/student_data.csv` as the raw source copy. The analysis changes only the in-memory names G1, G2, and G3 to readable grade labels.
- Iris: [UCI Iris, dataset 53](https://archive.ics.uci.edu/dataset/53/iris), credited to R. A. Fisher (1936), DOI 10.24432/C56C76, CC BY 4.0. The project CSV names the four measurements and species explicitly.

If a file is absent, visit the UCI pages above and download the listed files. For Student Performance, extract `student-mat.csv` and place it at `data/student_data.csv`. For Iris, use `iris.data` from the UCI Iris download, add the header `sepal_length_cm,sepal_width_cm,petal_length_cm,petal_width_cm,species`, and save it as `data/iris.csv`. Do not create substitute rows.

## Structure

```text
AI-ML-Internship/
  data/        raw and cleaned CSV datasets
  diagrams/    four editable Mermaid workflow diagrams
  images/      generated charts
  models/      reserved for later modeling work
  tests/       project integrity checks
  notebooks/   student_performance_eda.ipynb, iris_eda.ipynb
  reports/     populated Markdown and PDF EDA report
  src/         Python practice, loading, analysis, notebook, and report scripts
```

## Run the project

Activate `.venv`, then from the project root:

```powershell
python src/python_practice.py
python src/student_analysis.py
python src/iris_analysis.py
python src/create_notebooks.py
python src/generate_report.py
```

Open `notebooks/student_performance_eda.ipynb` and `notebooks/iris_eda.ipynb` in VS Code or Jupyter and run all cells from top to bottom. The scripts save the cleaned student file, all nine PNGs, and intermediate JSON results in `reports/`. The report command rebuilds `reports/eda_report.md` and `reports/EDA_Report.pdf` from those actual analysis results. Run both analyses before generating the report.

## Expected outputs

- `data/student_data.csv` (preserved raw source), `data/student_data_cleaned.csv`, `data/iris.csv` (all source rows), and `data/iris_cleaned.csv` (exact duplicates removed).
- Five student plots: score histogram, box plot, G1-vs-G3 scatter, numerical correlation heatmap, and school mean comparison.
- Four Iris plots: measurement histograms, species-colored petal scatter, measurement box plots, and correlation heatmap.
- Two notebooks, four editable `.mmd` diagrams, `reports/eda_report.md`, and `reports/EDA_Report.pdf`.

## Interpretation and limitations

Missing values are counted rather than assumed. If present, numeric fields are median-imputed, categorical fields mode-imputed, and exact duplicate rows removed; actual counts are included in the generated outputs. IQR flags indicate potential outliers, not errors. Correlation does not establish causation. The student dataset is observational and limited to two Portuguese schools; prior grades are naturally associated with the final grade. Iris is a small, classic dataset and its patterns are not universal botanical conclusions.

## Workflow diagrams

- [AI/ML lifecycle](diagrams/ai_ml_project_lifecycle.mmd)
- [Project folder structure](diagrams/project_structure.mmd)
- [EDA workflow](diagrams/eda_workflow.mmd)
- [Git and GitHub workflow](diagrams/git_github_workflow.mmd)

## Git and GitHub

This folder can be committed locally. Review `git status`, stage and commit changes with meaningful messages, then create a GitHub repository and add its remote only after signing into your own account. Example commands (replace the URL with your repository):

```powershell
git status
git add -A
git commit -m "Complete Task 1 data exploration project"
git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPOSITORY.git
git push -u origin main
```

Never commit `.venv`, credentials, or `.env` files. This project is not automatically published.

## Submission notes

The generated charts are submission-ready images; capture any requested screenshots yourself from VS Code/Jupyter because genuine application screenshots cannot be fabricated. Verify local tool installation (Python, Git, VS Code) on your computer before submission. This project does not create or push a GitHub repository.
