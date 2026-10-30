"""
generate_da2_pdf.py
Academic Project Report for DA 2: Software / Model Implementation.
Course: Business Analytics (BMGT107L)
Institution: Vellore Institute of Technology (VIT), Chennai
Faculty: BALAJI J
Students: PATEL KAVYA VIPULKUMAR (23BDS1076), SAHIL KUMAR (23BDS1099)
"""

import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


class CleanNumberedCanvasDA2(canvas.Canvas):
    """
    Two-pass canvas that renders clean, minimalist page numbers at the bottom
    without distracting header/footer rules or redundant marks clutter.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#6B7280"))
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, page_str)
        self.drawString(54, 36, "VIT Chennai | Business Analytics (BMGT107L)")
        self.restoreState()


def get_styles():
    """Builds clean, publication-grade academic paragraph styles."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'CoverSubTitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11.5,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#374151"),
        spaceAfter=14
    ))
    styles.add(ParagraphStyle(
        'ReportTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1B365D"),
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'ReportSubtitle',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=14
    ))
    styles.add(ParagraphStyle(
        'SecHeading1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1B365D"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'SecHeading2',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2C3E50"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=3,
        leftIndent=14
    ))
    styles.add(ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),
        spaceBefore=5,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        'FigureAnalysis',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#374151"),
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1F2937")
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#111827")
    ))
    styles.add(ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1F2937")
    ))
    return styles


def create_callout_box(text, title="Implementation Highlight", width=490):
    """Creates a highlighted academic callout box with a colored left stripe."""
    p_content = [
        Paragraph(f"<b>{title}</b>", ParagraphStyle('CT', fontName='Times-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor("#1E3A8A"), spaceAfter=3)),
        Paragraph(text, ParagraphStyle('CB', fontName='Times-Roman', fontSize=9, leading=13, alignment=TA_JUSTIFY, textColor=colors.HexColor("#1F2937")))
    ]
    tbl = Table([[p_content]], colWidths=[width])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F4F8")),
        ('LINELEFT', (0, 0), (0, -1), 3.5, colors.HexColor("#1E3A8A")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    return tbl


def create_da2_cover_page(styles):
    """Builds a clean, official cover page without marks clutter."""
    story = []
    story.append(Spacer(1, 14))

    # University Header
    story.append(Paragraph("<b>BUSINESS ANALYTICS (BMGT107L)</b>", ParagraphStyle('H1', fontName='Times-Bold', fontSize=16, leading=20, alignment=TA_CENTER, textColor=colors.black)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<u><b>VELLORE INSTITUTE OF TECHNOLOGY (VIT) UNIVERSITY</b></u>", ParagraphStyle('H2', fontName='Times-Bold', fontSize=13, leading=17, alignment=TA_CENTER, textColor=colors.black)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<i>Chennai Campus | School of Computer Science and Engineering (SCOPE)</i>", ParagraphStyle('H3', fontName='Times-Italic', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#374151"))))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>FALL SEMESTER 2026-27</b>", ParagraphStyle('H4', fontName='Times-Bold', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#111827"))))
    story.append(Spacer(1, 14))

    # Stage Line (Clean, Simple, No Marks)
    story.append(Paragraph("<b>DIGITAL ASSIGNMENT 2</b>", ParagraphStyle('DH', fontName='Times-Bold', fontSize=13, leading=17, alignment=TA_CENTER, textColor=colors.HexColor("#1B365D"))))
    story.append(Spacer(1, 16))

    # Project Title (Restaurant Recommendation as Main Title)
    story.append(Paragraph("<b>PROJECT TITLE</b>", ParagraphStyle('PTL', fontName='Times-Bold', fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.HexColor("#4B5563"))))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Restaurant Recommendation</b>", styles['CoverTitle']))
    story.append(Paragraph("A Data-Driven Analytical System for Restaurant Quality Assessment, Econometric Modeling, and Decision Support", styles['CoverSubTitle']))
    story.append(Spacer(1, 14))

    # Student & Faculty Table (Clean Box without Marks)
    tbl_data = [
        [Paragraph("<b>Programme:</b>", styles['TableCellBold']), Paragraph("B.Tech. Computer Science and Engineering (Data Science)", styles['TableCell']), Paragraph("<b>Slot:</b> G2 + TG2", styles['TableCellBold'])],
        [Paragraph("<b>Course:</b>", styles['TableCellBold']), Paragraph("BMGT107L – Business Analytics", styles['TableCell']), Paragraph("<b>Semester:</b> Fall 2026-27", styles['TableCell'])],
        [Paragraph("<b>Faculty In-Charge:</b>", styles['TableCellBold']), Paragraph("Prof. BALAJI J", styles['TableCellBold']), Paragraph("<b>School:</b> SCOPE", styles['TableCellBold'])],
        [Paragraph("<b>S.No.</b>", styles['TableHeader']), Paragraph("<b>Student Candidate Name</b>", styles['TableHeader']), Paragraph("<b>Registration No.</b>", styles['TableHeader'])],
        [Paragraph("1", styles['TableCellCenter']), Paragraph("<b>PATEL KAVYA VIPULKUMAR</b>", styles['TableCell']), Paragraph("23BDS1076", styles['TableCellCenter'])],
        [Paragraph("2", styles['TableCellCenter']), Paragraph("<b>SAHIL KUMAR</b>", styles['TableCell']), Paragraph("23BDS1099", styles['TableCellCenter'])]
    ]
    info_table = Table(tbl_data, colWidths=[110, 260, 120])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor("#1B365D")),
        ('BACKGROUND', (0, 0), (0, 2), colors.HexColor("#F9FAFB")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#111827")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 24))

    # Official Logo Centered
    logo_path = "results/figures/vit_chennai_logo.png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=220, height=80))
        story.append(Spacer(1, 14))

    story.append(Paragraph("<b>School of Computer Science and Engineering (SCOPE)</b>", ParagraphStyle('SC', fontName='Times-Bold', fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.black)))
    story.append(Paragraph("Vellore Institute of Technology, Chennai Campus, Vandalur-Kelambakkam Road, Chennai – 600127", ParagraphStyle('SCA', fontName='Times-Roman', fontSize=9, leading=13, alignment=TA_CENTER, textColor=colors.HexColor("#4B5563"))))
    story.append(PageBreak())
    return story


def build_da2_report_pdf():
    pdf_filename = "DA2_Implementation_Report.pdf"
    print(f"Generating DA 2 Report: {pdf_filename}...")
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    styles = get_styles()
    story = []

    # Load metrics
    with open("results/metrics/cleaning_log.json") as f:
        cleaning_log = json.load(f)
    with open("results/metrics/descriptive_stats.json") as f:
        desc_stats_list = json.load(f)
        ds_map = {item["variable"]: item for item in desc_stats_list}
    with open("results/metrics/linear_regression_results.json") as f:
        lr_results = json.load(f)
    with open("results/metrics/logistic_regression_results.json") as f:
        logit_results = json.load(f)
    with open("results/metrics/cluster_profiles.json") as f:
        km_results = json.load(f)

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.extend(create_da2_cover_page(styles))

    # =========================================================================
    # DOCUMENT HEADER ON PAGE 2
    # =========================================================================
    story.append(Paragraph("Digital Assignment 2: Restaurant Recommendation", styles['ReportTitle']))
    story.append(Paragraph("A Data-Driven Analytical System for Restaurant Quality Assessment, Econometric Modeling, and Decision Support", styles['ReportSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1B365D"), spaceAfter=14))

    # =========================================================================
    # SECTION 1: BRIEF INTRODUCTION AND OBJECTIVES
    # =========================================================================
    story.append(Paragraph("1. Brief Introduction and Objectives", styles['SecHeading1']))
    story.append(Paragraph(
        "Digital Assignment 2 marks the critical transition from theoretical project conceptualization (DA 1) into full software and model "
        "implementation. The objective of this phase is to build, calibrate, and validate a production-grade analytical engine in Python that "
        "overcomes the systemic biases inherent in digital restaurant rating aggregators.",
        styles['AcademicBody']
    ))
    story.append(Paragraph(
        "In urban food hubs like Bangalore, naive arithmetic star ratings systematically mislead consumers by failing to distinguish between "
        "untested low-evidence venues (e.g., 5.0 stars on 3 reviews) and proven culinary landmarks (e.g., 4.3 stars on 3,000 reviews). "
        "Simultaneously, restaurant operators lack econometric clarity regarding whether operational investments—such as table reservation engines "
        "or online delivery logistics—yield tangible improvements in customer perception. The implemented software system directly addresses "
        "these dilemmas through four operational modules:",
        styles['AcademicBody']
    ))

    mod_bullets = [
        ("Automated Data Wrangling & Entity Consolidation", "Ingests 51,717 raw web-scraped listings, cleans text ratings, parses currency strings, eliminates duplicate multi-zone listings, and creates a verified physical entity database of 9,244 restaurants."),
        ("Empirical Bayesian Shrinkage Engine", "Regularizes small-sample noise toward the citywide prior mean (C = 3.63 stars) using an empirical threshold (m = 100 votes), computing trusted ratings that reward authentic excellence."),
        ("Econometric & Machine Learning Suite", "Trains OLS multiple linear regression with VIF collinearity checks, binary logistic classification with odds ratios, and unsupervised K-Means clustering with silhouette validation."),
        ("Interactive Multi-Criteria Recommender Dashboard", "Deploys an end-user decision support tool in Streamlit allowing dynamic weight customization across quality, value-for-money percentiles, and popularity.")
    ]
    for mb_t, mb_d in mod_bullets:
        story.append(Paragraph(f"• <b>{mb_t}:</b> {mb_d}", styles['BulletText']))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: DATASET DESCRIPTION AND SOURCE
    # =========================================================================
    story.append(Paragraph("2. Dataset Description and Source", styles['SecHeading1']))
    story.append(Paragraph(
        "The software operates on the metropolitan Bangalore restaurant listing dataset extracted from Zomato. "
        "Bangalore represents an ideal testing environment due to its dense concentration of tech professionals, cosmopolitan migrants, and "
        "hyper-competitive dining formats.",
        styles['AcademicBody']
    ))
    story.append(Paragraph(
        "<b>Dataset Source:</b> Kaggle Open Data Archive / Zomato Public Listing Scrapes.<br/>"
        "<b>Raw Data Dimensions:</b> 51,717 observations across 17 attributes.<br/>"
        "<b>Target Attributes:</b> Continuous observed star rating (`rate`, range 1.8 to 4.9) and engineered binary classification indicator (`is_high_rated` = 1 for rate >= 4.0).<br/>"
        "<b>Key Operational Predictors:</b> `online_order` (binary 0/1), `book_table` (binary 0/1), `votes` (integer review counts), `cost_for_two` (dining spend in INR), `location` (neighborhood category), and `rest_type` (dining format).",
        styles['AcademicBody']
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 3: DATA PREPROCESSING
    # =========================================================================
    story.append(Paragraph("3. Data Preprocessing (Detailed Pipeline)", styles['SecHeading1']))
    story.append(Paragraph(
        "Real-world web scrape datasets contain severe structural noise, non-numeric artifacts, and duplication. "
        "To establish statistical integrity, an 8-stage automated data preprocessing pipeline was implemented in `src/data_processing.py`. "
        "Table 1 outlines the complete stage-by-stage cleaning log, showing exact row transitions and methodological justifications.",
        styles['AcademicBody']
    ))

    # Cleaning Log Table
    clean_table_data = [
        [Paragraph("<b>Step #</b>", styles['TableHeader']), Paragraph("<b>Cleaning Stage</b>", styles['TableHeader']), Paragraph("<b>Transformation Executed & Methodological Rationale</b>", styles['TableHeader']), Paragraph("<b>Rows Remaining</b>", styles['TableHeader'])]
    ]
    for step in cleaning_log:
        clean_table_data.append([
            Paragraph(str(step["step_num"]), styles['TableCellCenter']),
            Paragraph(str(step["step_name"]), styles['TableCellBold']),
            Paragraph(str(step["description"]), styles['TableCell']),
            Paragraph(f"{step['rows_remaining']:,}", styles['TableCellCenter'])
        ])
    t_clean = Table(clean_table_data, colWidths=[40, 105, 260, 85])
    t_clean.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_clean)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.1 Key Preprocessing Implementations", styles['SecHeading2']))
    story.append(Paragraph(
        "• <b>Regex Target Sanitization:</b> The raw `rate` column contained composite strings formatted as '4.1/5', unrated tags ('NEW'), "
        "and missing symbols ('-'). The regex pattern `^(\\d+\\.\\d+)/5$` was applied to extract floating-point ratings. Unrated outlets "
        "were explicitly removed to prevent zero-inflation in linear regressions.<br/>"
        "• <b>Entity Deduplication (Multi-Listing Resolution):</b> Zomato allows a single restaurant to be listed multiple times across "
        "search zones. Treating these as independent observations violates the i.i.d. assumption and artificially inflates sample size. "
        "Records were grouped by physical coordinates `(name, address, location)`, aggregating review votes and retaining verified attributes, "
        "consolidating 41,237 listing rows down to exactly <b>9,244 verified physical restaurants</b>.<br/>"
        "• <b>Logarithmic Transformations:</b> As shown in the descriptive statistics (Table 2), review votes exhibited extreme right skewness (+9.06) "
        "and kurtosis (+131.7). Applying `ln(votes + 1)` and `ln(cost_for_two)` normalized skewness to +0.39 and +0.28, stabilizing OLS residual variance.",
        styles['AcademicBody']
    ))

    # Descriptive Statistics Table
    story.append(Paragraph("3.2 Descriptive Statistics of Cleaned Features (N = 9,244)", styles['SecHeading2']))
    stats_rows = [
        [Paragraph("<b>Feature Name</b>", styles['TableHeader']), Paragraph("<b>Mean</b>", styles['TableHeader']), Paragraph("<b>Median</b>", styles['TableHeader']), Paragraph("<b>Std Dev</b>", styles['TableHeader']), Paragraph("<b>IQR</b>", styles['TableHeader']), Paragraph("<b>Skewness</b>", styles['TableHeader']), Paragraph("<b>Kurtosis</b>", styles['TableHeader'])],
        [Paragraph("Observed Rating (rate)", styles['TableCellBold']), Paragraph(f"{ds_map['rate_num']['mean']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['rate_num']['median']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['rate_num']['std']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['rate_num']['iqr']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['rate_num']['skewness']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['rate_num']['kurtosis']:.2f}", styles['TableCellCenter'])],
        [Paragraph("Review Votes (raw)", styles['TableCellBold']), Paragraph(f"{ds_map['votes']['mean']:.1f}", styles['TableCellCenter']), Paragraph(f"{ds_map['votes']['median']:.1f}", styles['TableCellCenter']), Paragraph(f"{ds_map['votes']['std']:.1f}", styles['TableCellCenter']), Paragraph(f"{ds_map['votes']['iqr']:.1f}", styles['TableCellCenter']), Paragraph(f"{ds_map['votes']['skewness']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['votes']['kurtosis']:.2f}", styles['TableCellCenter'])],
        [Paragraph("Cost for Two (INR)", styles['TableCellBold']), Paragraph(f"₹{ds_map['cost_for_two']['mean']:.1f}", styles['TableCellCenter']), Paragraph(f"₹{ds_map['cost_for_two']['median']:.1f}", styles['TableCellCenter']), Paragraph(f"₹{ds_map['cost_for_two']['std']:.1f}", styles['TableCellCenter']), Paragraph(f"₹{ds_map['cost_for_two']['iqr']:.1f}", styles['TableCellCenter']), Paragraph(f"{ds_map['cost_for_two']['skewness']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['cost_for_two']['kurtosis']:.2f}", styles['TableCellCenter'])],
        [Paragraph("Log Votes ln(votes+1)", styles['TableCellBold']), Paragraph(f"{ds_map['log_votes']['mean']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_votes']['median']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_votes']['std']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_votes']['iqr']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_votes']['skewness']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_votes']['kurtosis']:.2f}", styles['TableCellCenter'])],
        [Paragraph("Log Cost ln(cost+1)", styles['TableCellBold']), Paragraph(f"{ds_map['log_cost']['mean']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_cost']['median']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_cost']['std']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_cost']['iqr']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_cost']['skewness']:.2f}", styles['TableCellCenter']), Paragraph(f"{ds_map['log_cost']['kurtosis']:.2f}", styles['TableCellCenter'])],
        [Paragraph("Bayesian Rating (m=100)", styles['TableCellBold']), Paragraph("3.63", styles['TableCellCenter']), Paragraph("3.64", styles['TableCellCenter']), Paragraph("0.24", styles['TableCellCenter']), Paragraph("0.31", styles['TableCellCenter']), Paragraph("+0.18", styles['TableCellCenter']), Paragraph("+1.12", styles['TableCellCenter'])]
    ]
    t_stats = Table(stats_rows, colWidths=[130, 60, 60, 60, 60, 60, 60])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_stats)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 4: MODEL METHODOLOGY AND IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("4. Model Methodology and Implementation", styles['SecHeading1']))
    story.append(Paragraph(
        "The modeling architecture combines parametric econometrics, maximum likelihood classification, unsupervised cluster analysis, "
        "and empirical Bayes estimation. All models were implemented in modular Python scripts and serialized to disk via `joblib`.",
        styles['AcademicBody']
    ))

    # Model 1: OLS
    story.append(Paragraph("4.1 Ordinary Least Squares (OLS) Multiple Linear Regression", styles['SecHeading2']))
    story.append(Paragraph(
        "The OLS model specifies observed star rating as a linear function of operational, economic, format, and spatial variables:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>rate_i = beta_0 + beta_1 * online_order_i + beta_2 * book_table_i + beta_3 * ln(votes_i) + beta_4 * ln(cost_i) + sum(gamma_k * RestType_ik) + sum(delta_j * Loc_ij) + eps_i</i><br/>"
        "<b>Implementation Details:</b> Estimated using `statsmodels.api.OLS` and `scikit-learn.linear_model.LinearRegression`. "
        "Data was partitioned using an 80/20 train-test split (N_train = 7,395, N_test = 1,849) with random state 42. "
        "Multicollinearity was diagnosed by computing Variance Inflation Factors (VIF) for all predictors, ensuring no VIF exceeded 2.5.",
        styles['AcademicBody']
    ))

    # Model 2: Logistic Regression
    story.append(Paragraph("4.2 Binary Logistic Classification Model", styles['SecHeading2']))
    story.append(Paragraph(
        "To classify premier high-performing restaurants (`is_high_rated` = 1 for rating >= 4.0; prevalence = 22.8%), a binary logistic "
        "regression model was trained:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>ln[ P(Y_i = 1) / (1 - P(Y_i = 1)) ] = X_i * beta</i><br/>"
        "<b>Implementation Details:</b> Estimated using `scikit-learn.linear_model.LogisticRegression` with the `lbfgs` optimizer (max_iter = 1000). "
        "Continuous features (`log_votes`, `log_cost`) were scaled using `StandardScaler`. Exponentiated coefficients `exp(beta_j)` were computed "
        "to derive Odds Ratios (OR) with 95% Wald confidence intervals for business interpretability.",
        styles['AcademicBody']
    ))

    # Model 3: K-Means
    story.append(Paragraph("4.3 Unsupervised Market Segmentation (K-Means Clustering)", styles['SecHeading2']))
    story.append(Paragraph(
        "To identify latent dining market structures across Bangalore, K-Means clustering was executed on standardized features: "
        "`cost_for_two`, `votes`, and `rate`.<br/>"
        "<b>Implementation Details:</b> Evaluated across cluster candidates k = 2 through 8. The optimal partition was selected at k = 3 based on "
        "the Elbow method (inertia inflection) and Silhouette coefficient analysis (silhouette score = 0.354), yielding three distinct segments: "
        "Budget Casual Dining, Mid-Range Social/Takeaway, and Premium Fine Dining.",
        styles['AcademicBody']
    ))

    # Model 4: Bayesian Shrinkage
    story.append(Paragraph("4.4 Bayesian Shrinkage Recommendation Engine", styles['SecHeading2']))
    story.append(Paragraph(
        "The recommendation algorithm regularizes star ratings based on evidence volume using the Bayesian formulation:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>R_Bayes = [ v / (v + m) ] * R + [ m / (v + m) ] * C</i><br/>"
        "Where prior mean C = 3.6276 stars, and empirical credibility threshold m = 100 votes. "
        "The multi-criteria composite score integrates normalized Bayesian quality, empirical value-for-money percentile rank, "
        "and log-scaled popularity:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>Composite Score = w_r * (R_Bayes / 5.0 * 100) + w_v * Value_pct + w_p * Popularity_norm</i><br/>"
        "Fully vectorized via NumPy for sub-millisecond real-time execution in the web interface.",
        styles['AcademicBody']
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: STATISTICAL TECHNIQUES USED
    # =========================================================================
    story.append(Paragraph("5. Statistical Techniques Used", styles['SecHeading1']))
    story.append(Paragraph(
        "To establish empirical rigor prior to machine learning, six primary statistical techniques were implemented across nine formal tests. "
        "Standardized effect sizes were calculated to ensure practical relevance alongside statistical significance.",
        styles['AcademicBody']
    ))

    stat_techs = [
        ("Welch's Two-Sample t-Test", "Employed for testing mean rating equality across binary operational groups (Online Order, Table Booking). Welch's t-test does not assume equal population variances, providing robust inference under heteroscedasticity. Paired with Cohen's d effect size."),
        ("Mann-Whitney U Test", "Non-parametric counterpart to the t-test, evaluating whether rating rank distributions differ between operational groups without relying on normality assumptions."),
        ("One-Way Analysis of Variance (ANOVA)", "Used to test whether mean ratings and costs differ significantly across multiple listing categories (6 types) and geographic neighborhoods (top 10 locations). Effect size quantified via Eta-squared (eta^2)."),
        ("Kruskal-Wallis H-Test", "Non-parametric multi-group variance test confirming ANOVA findings on ordinal rating distributions across restaurant formats. Effect size quantified via Epsilon-squared (eps^2)."),
        ("Pearson and Spearman Correlation", "Pearson r evaluates linear association; Spearman rho evaluates monotonic rank relationship between dining expenditure, customer review volume, and star ratings."),
        ("Pearson Chi-Square Test of Independence", "Evaluates cross-tabulated contingency tables between operational features (Table Booking vs Rest Type; Online Order vs Listing Type). Effect size measured via Cramer's V.")
    ]
    for st_t, st_d in stat_techs:
        story.append(Paragraph(f"• <b>{st_t}:</b> {st_d}", styles['BulletText']))
    story.append(Spacer(1, 8))

    # Visualizations for Statistical Section
    corr_path = "results/figures/correlation_heatmap.png"
    if os.path.exists(corr_path):
        story.append(Image(corr_path, width=440, height=200))
        story.append(Paragraph("<b>Figure 1: Pearson and Spearman Correlation Heatmap of Dining Variables</b>", styles['FigureCaption']))
        story.append(Paragraph(
            "<b>Statistical Interpretation:</b> Dining cost exhibits only a moderate correlation with rating (Pearson r = 0.354, Spearman rho = 0.381), "
            "confirming that higher prices do not guarantee superior dining quality. Review votes demonstrate a strong positive monotonic association "
            "with rating (Spearman rho = 0.584), reflecting that social proof and community consensus accumulate around consistently satisfying venues.",
            styles['FigureAnalysis']
        ))
        story.append(Spacer(1, 8))

    # Hypothesis Boxplots
    story.append(Paragraph("5.1 Operational Quality Driver Boxplots", styles['SecHeading2']))
    h_box1 = "results/figures/hypothesis_table_booking_boxplot.png"
    if os.path.exists(h_box1):
        story.append(Image(h_box1, width=420, height=170))
        story.append(Paragraph("<b>Figure 2: Distribution of Ratings by Table Booking Enablement (Welch's t = 46.96, p < 0.001)</b>", styles['FigureCaption']))
        story.append(Paragraph(
            "<b>Statistical Takeaway:</b> Outlets with table booking exhibit a dramatically higher median rating (4.15★ vs 3.65★) with a massive "
            "Cohen's d effect size of 1.36. Table booking serves as the single strongest operational predictor of culinary and service excellence.",
            styles['FigureAnalysis']
        ))
        story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 6: SCREENSHOTS OR SAMPLE OUTPUTS
    # =========================================================================
    story.append(Paragraph("6. Screenshots and Sample Outputs of Working Model", styles['SecHeading1']))
    story.append(Paragraph(
        "The complete analytical pipeline was operationalized within a high-performance, 7-tab interactive web dashboard built with Streamlit (`restaurant_dashboard.py`). "
        "The interface executes real-time data filtering, dynamic re-ranking, and model diagnostic visualization in under 45 milliseconds. "
        "Figures 3 through 7 present actual interface screenshots capturing each operational module.",
        styles['AcademicBody']
    ))

    # Dashboard Screenshots
    dash_tabs = [
        ("results/figures/dashboard_screenshots/tab1_recommender.png", "Figure 3: Tab 1 – Multi-Criteria Interactive Recommender Interface",
         "The recommendation engine allows users to specify neighborhood filters, budget constraints, dining format preferences, and customize objective weights for Bayesian Quality, Value-for-Money, and Popularity in real-time."),
        ("results/figures/dashboard_screenshots/tab2_data_overview.png", "Figure 4: Tab 2 – Exploratory Data Overview & Citywide Metrics",
         "Presents interactive KPI metric cards, high-level dataset summaries, rating histograms, and cross-tabulated breakdowns of Bangalore's dining market."),
        ("results/figures/dashboard_screenshots/tab3_hypothesis_tests.png", "Figure 5: Tab 3 – Formal Hypothesis Testing Execution Suite",
         "Interactive interface enabling users to inspect all 9 formal hypothesis tests, complete with test statistics, p-values, degrees of freedom, and Cohen's d effect sizes alongside interactive comparative boxplots."),
        ("results/figures/dashboard_screenshots/tab4_linear_regression.png", "Figure 6: Tab 4 – Econometric Multiple Linear Regression Module",
         "Displays OLS regression coefficients, standard errors, t-statistics, p-values, Variance Inflation Factors (VIFs), and live residual diagnostic plots."),
        ("results/figures/dashboard_screenshots/tab6_segments.png", "Figure 7: Tab 6 – Unsupervised Market Segmentation (K-Means Clustering)",
         "Visualizes the 3-cluster market breakdown (Budget Casual, Mid-Range Social, Premium Fine Dining) with interactive 2D and 3D scatter plots and cluster profile summary cards.")
    ]
    for img_p, cap_t, anal_t in dash_tabs:
        if os.path.exists(img_p):
            story.append(Image(img_p, width=440, height=200))
            story.append(Paragraph(f"<b>{cap_t}</b>", styles['FigureCaption']))
            story.append(Paragraph(f"<b>Interface Description:</b> {anal_t}", styles['FigureAnalysis']))
            story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 7: INITIAL RESULTS AND RECOMMENDATIONS
    # =========================================================================
    story.append(Paragraph("7. Initial Results and Recommendations", styles['SecHeading1']))
    story.append(Paragraph(
        "Initial execution of the working model yielded robust empirical results across all predictive and segmentation modules. "
        "Table 3 summarizes the primary performance benchmarks of the implemented models.",
        styles['AcademicBody']
    ))

    # Initial Results Table
    results_summary_data = [
        [Paragraph("<b>Model / Module</b>", styles['TableHeader']), Paragraph("<b>Evaluation Metric</b>", styles['TableHeader']), Paragraph("<b>Observed Benchmark</b>", styles['TableHeader']), Paragraph("<b>Academic Interpretation & Significance</b>", styles['TableHeader'])],
        [Paragraph("Multiple Linear Regression (OLS)", styles['TableCellBold']), Paragraph("Test R^2 / RMSE", styles['TableCellCenter']), Paragraph(f"{lr_results['metrics']['test_r2']:.4f} / {lr_results['metrics']['test_rmse']:.4f}", styles['TableCellCenter']), Paragraph("Explains 38.6% of rating variance with low error (RMSE = 0.338 stars). F = 231.15, p < 0.001.", styles['TableCell'])],
        [Paragraph("Table Booking Marginal Lift", styles['TableCellBold']), Paragraph("OLS beta Coefficient", styles['TableCellCenter']), Paragraph(f"+{lr_results['coefficients'][4]['coefficient']:.4f} (t = 14.25)", styles['TableCellCenter']), Paragraph("Direct expected rating lift of nearly a quarter star (+0.24★) holding other factors constant.", styles['TableCell'])],
        [Paragraph("Binary Logistic Classification", styles['TableCellBold']), Paragraph("Classification Accuracy", styles['TableCellCenter']), Paragraph(f"{logit_results['metrics']['accuracy']*100:.2f}% (Lift: +{logit_results['metrics']['accuracy_lift_over_baseline']*100:.1f}%)", styles['TableCellCenter']), Paragraph("Outperforms majority class baseline (77.2%) by nearly 10 percentage points.", styles['TableCell'])],
        [Paragraph("Discriminative Power", styles['TableCellBold']), Paragraph("ROC-AUC Score", styles['TableCellCenter']), Paragraph(f"{logit_results['metrics']['roc_auc']:.4f}", styles['TableCellCenter']), Paragraph("Outstanding discrimination between premier (>=4.0★) and standard dining venues.", styles['TableCell'])],
        [Paragraph("Table Booking Odds Ratio", styles['TableCellBold']), Paragraph("Logistic Odds Ratio", styles['TableCellCenter']), Paragraph(f"{logit_results['odds_ratios'][3]['odds_ratio']:.2f}x (p < 0.001)", styles['TableCellCenter']), Paragraph("Triples the odds (OR = 3.28) of achieving high-rated status (>4.0★).", styles['TableCell'])],
        [Paragraph("K-Means Market Clustering", styles['TableCellBold']), Paragraph("Silhouette Score (k = 3)", styles['TableCellCenter']), Paragraph("0.3540", styles['TableCellCenter']), Paragraph("Discovers three coherent clusters: Budget (36.2%), Mid-Range (40.7%), Premium (23.1%).", styles['TableCell'])]
    ]
    t_res = Table(results_summary_data, colWidths=[130, 85, 105, 170])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 10))

    story.append(Paragraph("7.1 Initial Recommendations Derived from Working Model", styles['SecHeading2']))
    init_recs = [
        ("Managerial Recommendation for Restaurateurs",
         "Hospitality operators should prioritize table reservation infrastructure and physical hospitality over delivery packaging investments. Table booking yields an empirical rating lift of +0.24 stars and triples the odds of achieving a >= 4.0 star rating, whereas online delivery exhibits an insignificant marginal coefficient (beta = -0.0112, p = 0.239) once format and location are controlled."),
        ("Strategic Recommendation for Diners",
         "Diners should utilize the Bayesian shrinkage trusted rating and value-for-money percentile filters. Low-volume 5-star outlets are regularized toward the city prior mean (3.63 stars), safeguarding consumers from small-sample review manipulation while highlighting exceptional budget-friendly eateries in established neighborhoods like Basavanagudi and Jayanagar."),
        ("Platform Optimization for Food-Tech Architects",
         "Commercial food platforms should adopt Bayesian shrinkage as the default ranking heuristic to restore consumer confidence and penalize review farming schemes.")
    ]
    for ir_t, ir_d in init_recs:
        story.append(Paragraph(f"• <b>{ir_t}:</b> {ir_d}", styles['BulletText']))
    story.append(Spacer(1, 10))

    # Build document
    doc.build(story, canvasmaker=CleanNumberedCanvasDA2)
    print(f"Successfully generated clean DA 2 Report: {pdf_filename}")


if __name__ == "__main__":
    build_da2_report_pdf()
