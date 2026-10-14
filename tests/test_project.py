"""Integrity tests for downloaded data, cleaned outputs, and generated figures."""
from pathlib import Path
import sys
import unittest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

class ProjectIntegrityTests(unittest.TestCase):
    def test_real_source_dataset_shapes_and_delimiter(self):
        student = pd.read_csv(ROOT / "data" / "student_data.csv", sep=";")
        iris = pd.read_csv(ROOT / "data" / "iris.csv")
        self.assertEqual(student.shape, (395, 33))
        self.assertIn("G3", student.columns)
        self.assertEqual(iris.shape, (150, 5))
        self.assertEqual(iris["species"].nunique(), 3)

    def test_cleaned_datasets_and_results_are_consistent(self):
        student = pd.read_csv(ROOT / "data" / "student_data_cleaned.csv")
        iris = pd.read_csv(ROOT / "data" / "iris_cleaned.csv")
        self.assertEqual(student.shape, (395, 33))
        self.assertFalse(student.isna().any().any())
        self.assertEqual(iris.shape, (147, 5))
        self.assertFalse(iris.duplicated().any())

    def test_all_nine_charts_exist_and_are_nonempty(self):
        names = ["math_score_histogram.png", "math_score_boxplot.png", "math_scatter_plot.png",
                 "correlation_heatmap.png", "average_score_by_school.png", "iris_histograms.png",
                 "iris_scatter.png", "iris_boxplot.png", "iris_heatmap.png"]
        for name in names:
            with self.subTest(name=name):
                self.assertGreater((ROOT / "images" / name).stat().st_size, 1000)

    def test_four_editable_workflow_diagrams_exist(self):
        names = ["ai_ml_project_lifecycle.mmd", "project_structure.mmd",
                 "eda_workflow.mmd", "git_github_workflow.mmd"]
        for name in names:
            with self.subTest(name=name):
                text = (ROOT / "diagrams" / name).read_text(encoding="utf-8")
                self.assertIn("flowchart", text)
                self.assertIn("-->", text)

    def test_reports_and_executed_notebooks_are_populated(self):
        self.assertGreater((ROOT / "reports" / "EDA_Report.pdf").stat().st_size, 100_000)
        self.assertIn("mean", (ROOT / "reports" / "eda_report.md").read_text(encoding="utf-8"))
        for path in (ROOT / "notebooks").glob("*.ipynb"):
            import json
            notebook = json.loads(path.read_text(encoding="utf-8"))
            code = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
            self.assertTrue(code)
            self.assertTrue(all(cell["execution_count"] is not None for cell in code))
            self.assertFalse(any(out.get("output_type") == "error" for cell in code for out in cell["outputs"]))

if __name__ == "__main__":
    unittest.main(verbosity=2)
