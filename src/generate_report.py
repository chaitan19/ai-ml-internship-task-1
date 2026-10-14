"""Build populated Markdown and polished PDF reports from saved analysis results."""
import json
import argparse
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table,
                                TableStyle, PageBreak, KeepTogether)

ROOT = Path(__file__).resolve().parents[1]
REPORTS, IMAGES = ROOT / 'reports', ROOT / 'images'

def load_results():
    return (json.loads((REPORTS/'student_results.json').read_text(encoding='utf-8')),
            json.loads((REPORTS/'iris_results.json').read_text(encoding='utf-8')))

def write_markdown(s, i):
    m=s['math_score']; c=s['cleaning']; ic=i['cleaning']
    school=sorted(s['school_mean_math'].items())
    species=i['species_means']
    text=f'''# Exploratory Data Analysis Report\n\n**AI/ML Internship Task 1 — Student Performance Data Explorer and Iris Challenge**\n\n## Project overview\nThis report documents reproducible exploratory analysis of two genuine public datasets. It summarizes data quality, cleaning, descriptive statistics, visual evidence, limitations, and source attribution. The scripts and notebooks regenerate the tables and figures.\n\n## Datasets and sources\n\n### Student Performance (mathematics)\nThe mathematics subset (`student-mat.csv`) comes from the [UCI Machine Learning Repository, Student Performance dataset 320](https://archive.ics.uci.edu/dataset/320/student). Its original delimiter is a semicolon. The source data covers secondary students at two Portuguese schools and includes demographic, school, family, social, absence, and period-grade fields. `G3` is renamed **Math Score** for analysis; `G1` and `G2` are labeled Period 1 and Period 2 Math Grade.\n\n### Iris\nThe [UCI Iris dataset 53](https://archive.ics.uci.edu/dataset/53/iris), attributed to R. A. Fisher (1936), contains 150 flowers, four measurements in centimeters, and three species labels. The reusable CSV is stored at `data/iris.csv`.\n\n## Data quality and cleaning\n\n### Student data\nThe raw table has **{s['raw_shape'][0]} rows and {s['raw_shape'][1]} columns**. It contains {s['missing_cells_before']} missing cells and {s['duplicate_rows_before']} exact duplicate rows before cleaning. The pipeline removed {c['duplicate_rows_removed']} duplicate rows and imputed {c['missing_cells_before_imputation']} missing cells using numeric medians or categorical modes. After cleaning, {c['rows_after']} rows remain and {c['missing_cells_after']} missing cells remain. The raw file is preserved; the cleaned table is saved separately as `student_data_cleaned.csv`.\n\n### Iris data\nThe raw table has **{i['raw_shape'][0]} rows and {i['raw_shape'][1]} columns**. It contains {i['missing_cells_before']} missing cells and {i['duplicate_rows_before']} exact duplicate rows. The cleaning function removed {ic['duplicate_rows_removed']} duplicates and imputed {ic['missing_cells_before_imputation']} missing cells if present; the resulting table has {ic['rows_after']} rows.\n\n## Student mathematics results\nThe final grade is on a 0–20 scale. Mean: **{m['mean']:.2f}**; median: **{m['median']:.2f}**; mode(s): **{', '.join(map(str,m['mode']))}**; minimum: **{m['min']}**; maximum: **{m['max']}**; sample standard deviation: **{m['std']:.2f}**.\n\nThe Pearson correlation of Period 1 grade and final grade is **{s['correlation_g1_g3']:.3f}**; Period 2 grade and final grade is **{s['correlation_g2_g3']:.3f}**. These are associations in an observational dataset, not evidence that earlier grades cause later outcomes. The IQR rule flags **{s['iqr_outlier_count']}** final grades as potential outliers; this statistical flag is not proof of erroneous data.\n\nAverage final grade by school: {', '.join(f'**{escape(k)}** {v:.2f}' for k,v in school)}. Group averages are descriptive; the schools may differ in many unmeasured ways.\n\n### Student charts\n\n![Final mathematics score histogram](../images/math_score_histogram.png)\n\n*Figure 1. Distribution of final mathematics grades.*\n\n![Final mathematics score box plot](../images/math_score_boxplot.png)\n\n*Figure 2. IQR display of potential score outliers.*\n\n![Earlier and final grade scatter](../images/math_scatter_plot.png)\n\n*Figure 3. Period 1 and final mathematics grades, colored by school.*\n\n![Student numerical correlations](../images/correlation_heatmap.png)\n\n*Figure 4. Pearson correlations among numeric student attributes; correlation does not establish causation.*\n\n![Average score by school](../images/average_score_by_school.png)\n\n*Figure 5. Mean final mathematics grade by school; error bars show standard deviation.*\n\n## Iris results\nThere are {i['cleaned_shape'][0]} cleaned flowers, with species counts {', '.join(f'{escape(str(k))}: {v}' for k,v in sorted(i['species_counts'].items()))}. The feature means by species (cm) are:\n\n| Species | Sepal length | Sepal width | Petal length | Petal width |\n|---|---:|---:|---:|---:|\n'''
    for name, vals in sorted(species.items()):
        text += f"| {name} | {vals['sepal_length_cm']:.2f} | {vals['sepal_width_cm']:.2f} | {vals['petal_length_cm']:.2f} | {vals['petal_width_cm']:.2f} |\n"
    text += f'''\nPetal length and width vary substantially across species; the scatter plot separates setosa observations from the other groups, while versicolor and virginica overlap. This describes this small dataset only. Feature correlations summarize linear co-variation and are not causal.\n\n### Iris charts\n\n![Iris histograms](../images/iris_histograms.png)\n\n*Figure 6. Measurement distributions by species.*\n\n![Iris petal scatter plot](../images/iris_scatter.png)\n\n*Figure 7. Petal measurements colored by species.*\n\n![Iris box plots](../images/iris_boxplot.png)\n\n*Figure 8. Measurement spread by species.*\n\n![Iris heatmap](../images/iris_heatmap.png)\n\n*Figure 9. Pearson correlations among four Iris measurements.*\n\n## Limitations\nThe student data is observational, represents two Portuguese schools, and is not a random sample of all students. Its grade history is strongly related to the final grade by design. Missing-value handling is included but should not be read as a claim that the source has missing values; actual counts are stated above. Outlier rules are exploratory. Iris has only 150 observations, balanced among three classes, and should not be generalized to all flower populations. Neither EDA supports causal conclusions.\n\n## Conclusion\nThe project preserves the raw student file, provides a separately cleaned dataset, calculates reproducible summary statistics, and saves nine labeled charts. The notebooks and scripts make the inspection, cleaning, descriptive analysis, and visualization steps repeatable.\n\n## References and attribution\n1. Cortez, P. & Silva, A. (2008). Using data mining to predict secondary school student performance. UCI Machine Learning Repository, [Student Performance dataset](https://archive.ics.uci.edu/dataset/320/student).\n2. Fisher, R. A. (1936). The use of multiple measurements in taxonomic problems. *Annals of Eugenics*, 7, 179–188. UCI Machine Learning Repository, [Iris dataset](https://archive.ics.uci.edu/dataset/53/iris), DOI: 10.24432/C56C76 (CC BY 4.0).\n3. Statistical summaries are computed from the raw CSVs included in this project using pandas; chart styling uses Matplotlib and Seaborn.\n'''
    (REPORTS/'eda_report.md').write_text(text, encoding='utf-8')

def build_pdf(s, i):
    path=REPORTS/'EDA_Report.pdf'
    doc=SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm, title='EDA Report - AI/ML Internship Task 1', author='AI/ML Internship Project')
    st=getSampleStyleSheet(); st.add(ParagraphStyle(name='Cover', parent=st['Title'], fontSize=22, leading=28, alignment=TA_CENTER, textColor=colors.HexColor('#174a73'), spaceAfter=12)); st.add(ParagraphStyle(name='Caption', parent=st['Normal'], fontSize=8, leading=10, textColor=colors.HexColor('#445566'), alignment=TA_CENTER, spaceAfter=10)); st.add(ParagraphStyle(name='Small', parent=st['BodyText'], fontSize=8, leading=10))
    story=[]
    def H(t): story.append(Paragraph(escape(t),st['Heading1']))
    def P(t): story.append(Paragraph(t,st['BodyText'])); story.append(Spacer(1,6))
    def chart(file, caption, width=165*mm):
        p=IMAGES/file
        if p.exists():
            im=Image(str(p)); im._restrictSize(width, 82*mm); story.extend([im,Paragraph(escape(caption),st['Caption'])])
    m=s['math_score']; c=s['cleaning']; ic=i['cleaning']
    story += [Spacer(1,25*mm),Paragraph('Exploratory Data Analysis',st['Cover']),Paragraph('AI/ML Internship Task 1',st['Heading2']),Spacer(1,8*mm)]
    P('Student Performance Data Explorer and complete Iris EDA challenge. This report presents results computed from the included UCI datasets, with data-quality counts, descriptive statistics, visualizations, and limitations.')
    P('<b>Project contents:</b> reusable Python analyses, two Jupyter notebooks, raw and cleaned data, nine chart files, editable Mermaid workflow diagrams, and this report.')
    story.append(PageBreak())
    H('1. Dataset descriptions and sources')
    P('The UCI Student Performance mathematics dataset (dataset 320; student-mat.csv) describes secondary students from two Portuguese schools. It contains student, family, school, and grade attributes. Its original CSV uses semicolon delimiters. G3 is presented as Math Score; G1 and G2 are prior period grades.')
    P('The UCI Iris dataset (dataset 53), credited to R. A. Fisher (1936), contains 150 flowers, three species, and four continuous measurements in centimeters. The source is licensed CC BY 4.0.')
    H('2. Data quality and cleaning')
    P(f"Student raw shape: {s['raw_shape'][0]} rows × {s['raw_shape'][1]} columns. Missing cells: {s['missing_cells_before']}; exact duplicate rows: {s['duplicate_rows_before']}. Removed duplicates: {c['duplicate_rows_removed']}; imputed missing cells: {c['missing_cells_before_imputation']}; cleaned rows: {c['rows_after']}; missing cells remaining: {c['missing_cells_after']}. The original CSV remains unchanged, and the cleaned version is separate.")
    P(f"Iris raw shape: {i['raw_shape'][0]} × {i['raw_shape'][1]}. Missing cells: {i['missing_cells_before']}; duplicate rows: {i['duplicate_rows_before']}. Removed duplicates: {ic['duplicate_rows_removed']}; imputed cells: {ic['missing_cells_before_imputation']}; cleaned rows: {ic['rows_after']}.")
    H('3. Student performance: descriptive results')
    P(f"Final mathematics grade summary (0–20): mean {m['mean']:.2f}; median {m['median']:.2f}; mode {', '.join(map(str,m['mode']))}; minimum {m['min']}; maximum {m['max']}; standard deviation {m['std']:.2f}. The IQR rule flags {s['iqr_outlier_count']} potential outliers; these are not necessarily errors.")
    P(f"Correlation between Period 1 and final grade: {s['correlation_g1_g3']:.3f}; Period 2 and final: {s['correlation_g2_g3']:.3f}. This association is expected to be strong for sequential grades, but it does not show causation.")
    tbl=[["School","Mean final grade"]]+[[str(k),f"{v:.2f}"] for k,v in sorted(s['school_mean_math'].items())]
    t=Table(tbl,colWidths=[65*mm,65*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#174a73')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.4,colors.grey),('PADDING',(0,0),(-1,-1),6)])); story.extend([t,Spacer(1,8)])
    H('4. Student performance visualizations')
    for f,cap in [('math_score_histogram.png','Figure 1. Distribution of final mathematics scores.'),('math_score_boxplot.png','Figure 2. Final grade box plot and potential outliers.'),('math_scatter_plot.png','Figure 3. Earlier and final mathematics grades colored by school.'),('correlation_heatmap.png','Figure 4. Correlations among numerical student attributes.'),('average_score_by_school.png','Figure 5. Mean mathematics score by school.')]: chart(f,cap)
    story.append(PageBreak()); H('5. Iris challenge results')
    P(f"The cleaned Iris dataset contains {i['cleaned_shape'][0]} records. Species counts are {', '.join(f'{k}: {v}' for k,v in sorted(i['species_counts'].items()))}. Petal length and width differ noticeably among species; setosa forms a distinct cluster, while versicolor and virginica overlap. This is a descriptive pattern from a small classic dataset.")
    tbl=[["Species","Sepal L","Sepal W","Petal L","Petal W"]]
    for name, vals in sorted(i['species_means'].items()): tbl.append([name]+[f"{vals[k]:.2f}" for k in ['sepal_length_cm','sepal_width_cm','petal_length_cm','petal_width_cm']])
    t=Table(tbl,colWidths=[45*mm,26*mm,26*mm,26*mm,26*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#174a73')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.4,colors.grey),('PADDING',(0,0),(-1,-1),5)])); story.extend([t,Spacer(1,8)])
    for f,cap in [('iris_histograms.png','Figure 6. Histograms of four measurements by species.'),('iris_scatter.png','Figure 7. Species-colored scatter of petal measurements.'),('iris_boxplot.png','Figure 8. Measurement box plots by species.'),('iris_heatmap.png','Figure 9. Correlation heatmap of Iris measurements.')]: chart(f,cap)
    H('6. Interpretation and limitations')
    P('Correlation describes linear co-variation and does not establish causation. Student data is observational, from two schools, and includes prior grades that are naturally related to final grades. School means do not control for confounders. The IQR rule is a screening heuristic. Iris has only 150 records and three species; its patterns should not be generalized to every population.')
    H('7. Conclusion and references')
    P('The project preserves raw data, separates cleaned outputs, includes two executable notebooks, and generates nine figures from genuine source data.')
    story.append(Paragraph('Sources: Cortez & Silva (2008), UCI Student Performance dataset 320, archive.ics.uci.edu/dataset/320/student. Fisher (1936), UCI Iris dataset 53, DOI 10.24432/C56C76 (CC BY 4.0). Tools: Python, pandas, Matplotlib, Seaborn, ReportLab.',st['Small']))
    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont('Helvetica',8); canvas.setFillColor(colors.grey); canvas.drawString(18*mm,10*mm,'AI/ML Internship Task 1 — EDA Report'); canvas.drawRightString(A4[0]-18*mm,10*mm,str(doc.page)); canvas.restoreState()
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

def main():
    REPORTS.mkdir(exist_ok=True)
    parser=argparse.ArgumentParser()
    parser.add_argument('--markdown-only', action='store_true')
    parser.add_argument('--pdf-only', action='store_true')
    args=parser.parse_args()
    s,i=load_results()
    if not args.pdf_only: write_markdown(s,i); print(f"Wrote {REPORTS/'eda_report.md'}")
    if not args.markdown_only: build_pdf(s,i); print(f"Wrote {REPORTS/'EDA_Report.pdf'}")

if __name__=='__main__': main()
