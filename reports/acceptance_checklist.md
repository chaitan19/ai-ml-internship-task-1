# Task 1 Acceptance Checklist

Verification performed on 2026-10-14 with Python 3.13.7 and the project virtual environment.

| Requirement | Status | Evidence / notes |
|---|---|---|
| Python fundamentals examples | PASS | `src/python_practice.py` ran successfully and demonstrated requested constructs and error handling. |
| Genuine UCI student mathematics data | PASS | Official UCI dataset 320; preserved 395 × 33 semicolon-delimited source rows. |
| Student inspection and cleaning | PASS | Shape, columns, types, first ten, descriptive statistics, missing cells, and duplicates are analyzed; 0 missing, 0 duplicates; cleaned output has 395 rows. |
| Required student statistics and five charts | PASS | Mean 10.415, median 11, mode 10, min 0, max 20, standard deviation 4.581; all five PNGs exist. |
| Genuine Iris dataset and cleaning | PASS | Official UCI dataset 53; raw 150 × 5 preserved, 0 missing, 3 duplicate rows removed into a separate 147-row cleaned CSV. |
| Iris comparison and four charts | PASS | Species counts and feature means calculated; all four PNGs exist. |
| Two professional notebooks | PASS | Both notebooks executed fully with nbconvert; execution outputs are saved in the notebooks. |
| Reusable code, dependencies, README, and ignore rules | PASS | Python modules, dependency file, Windows setup/run guidance, sources, interpretation limits, and `.gitignore` present. |
| Populated Markdown and PDF report | PASS | Actual counts, statistics, interpretation, sources, captions, and embedded charts; PDF visually rendered and reviewed (6 pages). |
| Four workflow diagrams | PASS | Four editable Mermaid `.mmd` sources included in `diagrams/`; no Mermaid renderer was installed for PNG exports. |
| Python compile and project integrity tests | PASS | `compileall` completed; 5 unittest checks passed. |
| Local Git preparation | PASS | New local repository initialized; no remote configured and nothing published. |
| GitHub URL / push | PARTIAL | Requires the user's GitHub account and repository authorization; project is intentionally not published. |
| Genuine application screenshots | PARTIAL | Generated charts are included; screenshots from the user's VS Code/Jupyter session must be captured locally if required by submission. |
| Local IDE / Git installation | PARTIAL | Python and Git repository were verified here; VS Code installation/extensions were not inspected or configured. |

## Commands verified

The analysis scripts, Python practice script, notebook creation, notebook execution, and report generation were run using `.venv`. Five integrity tests passed. The report's six rendered pages were visually inspected after layout adjustment.
