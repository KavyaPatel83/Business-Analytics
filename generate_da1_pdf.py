"""
generate_da1_pdf.py
Academic Project Report for Digital Assignment 1.
Project Title: Restaurant Recommendation
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


class CleanNumberedCanvasDA1(canvas.Canvas):
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
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#374151"),
        spaceAfter=16
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


def create_callout_box(text, title="Key Concept / Analytical Formula", width=490):
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


def create_da1_cover_page(styles):
    """Builds a clean, official cover page with 'Restaurant Recommendation' as the main title."""
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
    story.append(Spacer(1, 16))

    # Stage Line (Clean, Simple, No Marks, No Problem/Idea text)
    story.append(Paragraph("<b>DIGITAL ASSIGNMENT 1</b>", ParagraphStyle('DH', fontName='Times-Bold', fontSize=13, leading=17, alignment=TA_CENTER, textColor=colors.HexColor("#1B365D"))))
    story.append(Spacer(1, 16))

    # Project Title (Restaurant Recommendation as Main Title)
    story.append(Paragraph("<b>PROJECT TITLE</b>", ParagraphStyle('PTL', fontName='Times-Bold', fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.HexColor("#4B5563"))))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Restaurant Recommendation</b>", styles['CoverTitle']))
    story.append(Paragraph("A Data-Driven Analytical System for Restaurant Quality Assessment, Econometric Modeling, and Decision Support", styles['CoverSubTitle']))
    story.append(Spacer(1, 14))

    # Student & Faculty Table
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


def build_da1_report_pdf():
    pdf_filename = "DA1_Problem_Idea_Report.pdf"
    print(f"Generating DA 1 Report: {pdf_filename}...")
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

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.extend(create_da1_cover_page(styles))

    # =========================================================================
    # DOCUMENT HEADER ON PAGE 2 (Clean Header without Problem/Idea text)
    # =========================================================================
    story.append(Paragraph("Digital Assignment 1: Restaurant Recommendation", styles['ReportTitle']))
    story.append(Paragraph("A Data-Driven Analytical System for Restaurant Quality Assessment, Econometric Modeling, and Decision Support", styles['ReportSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1B365D"), spaceAfter=14))

    # =========================================================================
    # SECTION 1: TITLE OF THE PROJECT
    # =========================================================================
    story.append(Paragraph("1. Title of the Project", styles['SecHeading1']))
    story.append(Paragraph(
        "<b>Project Title:</b> Restaurant Recommendation",
        styles['AcademicBody']
    ))
    story.append(Paragraph(
        "<b>Subtitle & Analytical Scope:</b> A Data-Driven Analytical System for Restaurant Quality Assessment, "
        "Econometric Modeling, and Decision Support.",
        styles['AcademicBody']
    ))
    story.append(Paragraph(
        "<b>Academic Discipline:</b> Business Analytics, Econometrics, Quantitative Marketing Science, and Machine Learning.",
        styles['AcademicBody']
    ))
    story.append(Paragraph(
        "The project title 'Restaurant Recommendation' represents an end-to-end data analytics system designed to solve "
        "fundamental information friction in metropolitan dining markets. The research bridges consumer decision-making and "
        "hospitality business strategy through three integrated analytical components:",
        styles['AcademicBody']
    ))
    story.append(Paragraph(
        "• <b>Objective Quality Modeling:</b> Applying parametric Ordinary Least Squares (OLS) regression and Binary Logistic Classification "
        "to rigorously measure the marginal impact of key operational levers—specifically advance table reservations, online delivery enablement, "
        "pricing tiers, and geographical clustering—on verified customer satisfaction ratings.",
        styles['BulletText']
    ))
    story.append(Paragraph(
        "• <b>Empirical Bayesian Regularization:</b> Implementing an empirical Bayes shrinkage estimator that dynamically corrects arithmetic average "
        "star ratings based on review volume, penalizing low-sample variance (such as unverified 5-star outlets with only 3 reviews) while "
        "protecting established culinary institutions.",
        styles['BulletText']
    ))
    story.append(Paragraph(
        "• <b>Multi-Criteria Decision Support:</b> Formulating an interactive recommendation engine that synthesizes Bayesian quality, "
        "empirical value-for-money percentiles, and log-scaled popularity to deliver personalized dining discovery for consumers "
        "and empirical operational benchmarks for restaurant operators.",
        styles['BulletText']
    ))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: INTRODUCTION AND BACKGROUND OF THE PROBLEM
    # =========================================================================
    story.append(Paragraph("2. Introduction and Background of the Problem", styles['SecHeading1']))
    story.append(Paragraph(
        "Bangalore (Bengaluru), globally recognized as the technological and startup capital of India, houses one of the fastest-growing, "
        "most culturally heterogeneous food-service markets in South Asia. Driven by a massive influx of software professionals, university students, "
        "and cosmopolitan migrants with high disposable incomes, the city's food culture has rapidly evolved. Dining out and ordering food via digital aggregators "
        "have transitioned from occasional weekend indulgences into daily nutritional routines.",
        styles['AcademicBody']
    ))
    story.append(Paragraph(
        "Commercial food platforms like Zomato catalog tens of thousands of culinary venues across Bangalore's sprawling metropolitan geography—ranging "
        "from traditional South Indian vegetarian breakfast joints (Darshinis) and street food stalls to artisan cafes, microbreweries, and luxury dining destinations. "
        "However, this unprecedented choice has precipitated severe <b>information friction</b> and <b>consumer decision fatigue</b>. Patrons regularly spend 15 to 30 minutes "
        "navigating through hundreds of mobile app cards, sorting through conflicting star ratings, and deciphering ambiguous promotional claims without any objective "
        "guarantee that their expenditure will deliver high-quality dining, hygienic food preparation, or genuine value for money.",
        styles['AcademicBody']
    ))
    story.append(Paragraph(
        "Concurrently, the economic health of urban restaurants has grown precarious. The modern food and beverage industry operates under compressed operating margins "
        "(often between 8% and 15%), high commercial lease expenditures in prime tech corridors (such as Koramangala, Indiranagar, and Whitefield), and substantial aggregator "
        "commission fees (reaching 18% to 28% per order). In this hyper-competitive climate, restaurant entrepreneurs cannot afford capital misallocation. Yet, operators "
        "consistently lack empirical data on whether investing capital into physical table-booking infrastructure, dine-in floor space, or online-delivery packaging yields "
        "a measurable lift in customer ratings and lifetime reputational capital.",
        styles['AcademicBody']
    ))

    # =========================================================================
    # SECTION 3: PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("3. Problem Statement", styles['SecHeading1']))
    story.append(Paragraph(
        "The fundamental problem investigated in this project can be distilled into four interrelated structural breakdowns within existing "
        "restaurant aggregation and rating systems:",
        styles['AcademicBody']
    ))

    # Sub-problem 3.1
    story.append(Paragraph("3.1 The Small-Sample Rating Dilemma (Naive Arithmetic Star Average Fallacy)", styles['SecHeading2']))
    story.append(Paragraph(
        "The standard heuristic utilized across digital discovery platforms is the arithmetic mean star rating (1.0 to 5.0). "
        "Mathematically, this arithmetic mean treats every sample size identically, ignoring the law of large numbers. A newly established outlet with three 5-star reviews "
        "submitted by friends and family displays a perfect <b>5.0 / 5.0</b> rating. In contrast, an iconic institution operating for a decade with 4,500 verified reviews "
        "might exhibit a <b>4.2 / 5.0</b> rating due to statistical variance, diverse palate preferences, and unavoidable operational friction over time. "
        "When platforms sort listings by raw rating, the unverified 5.0 venue outranks the proven landmark, exposing consumers to severe quality risk and misleading "
        "algorithms that reward low-evidence variance over statistically reliable excellence.",
        styles['AcademicBody']
    ))

    # Sub-problem 3.2
    story.append(Paragraph("3.2 The Price-Quality Decoupling", styles['SecHeading2']))
    story.append(Paragraph(
        "Consumers implicitly assume that paying higher prices guarantees superior experiential quality. However, exploratory empirical analysis reveals that "
        "the Pearson correlation between dining cost for two and customer rating is only <b>r = 0.354</b>, meaning that dining expenditure accounts for under 15% of the "
        "variance in dining satisfaction. Diners frequently overpay for prime real estate, lavish interior aesthetics, and high aggregator advertising overhead rather "
        "than superior culinary execution. Conversely, numerous exceptional neighborhood eateries delivering extraordinary food at modest prices remain buried beneath "
        "heavily advertised premium brands due to the lack of an objective, normalized <i>Value-for-Money Percentile</i> metric.",
        styles['AcademicBody']
    ))

    # Sub-problem 3.3
    story.append(Paragraph("3.3 Restaurateur Capital Allocation and Operational Uncertainty", styles['SecHeading2']))
    story.append(Paragraph(
        "Restaurant owners face profound uncertainty when designing their business models. Key managerial dilemmas include: (a) Does adopting table reservation engines "
        "create a statistically significant premium on customer perception? (b) Does enabling online food delivery enhance customer loyalty, or does delivery transit time "
        "and packaging degrade perceived food quality? (c) How much do geographical neighborhood clusters (e.g., Koramangala vs. Jayanagar vs. Electronic City) contribute "
        "to baseline rating variance after controlling for restaurant format? Without rigorous econometric modeling (Ordinary Least Squares and Binary Logistic Regression), "
        "hospitality entrepreneurs operate on trial-and-error, often making costly capital allocation errors.",
        styles['AcademicBody']
    ))

    # Sub-problem 3.4
    story.append(Paragraph("3.4 Data Duplication and Multi-Listing Autocorrelation in Platform Scrapes", styles['SecHeading2']))
    story.append(Paragraph(
        "From an analytical perspective, raw restaurant scrape data presents severe statistical hazards. Aggregators allow a single physical establishment to be listed "
        "under multiple search categories (e.g., 'Delivery', 'Dine-out', 'Pubs') and across multiple geographical search radii. Naively running statistical regressions "
        "on raw listings (51,717 records) violates the fundamental assumption of independent and identically distributed (i.i.d.) observations, causing severe autocorrelation, "
        "deflated standard errors, and spurious statistical significance. A rigorous deduplication and physical entity consolidation pipeline is essential prior to modeling.",
        styles['AcademicBody']
    ))
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 4: OBJECTIVES OF THE MODEL
    # =========================================================================
    story.append(Paragraph("4. Objectives of the Model", styles['SecHeading1']))
    story.append(Paragraph(
        "To systematically address the stated problems through a structured business analytics framework, this project establishes six formal, measurable objectives:",
        styles['AcademicBody']
    ))

    objs = [
        ("Objective 1: Automated Sanitation & Entity Deduplication Pipeline",
         "Develop an end-to-end data processing pipeline that ingests 51,717 raw Zomato listings, eliminates string currency formatting, parses composite ratings ('4.1/5'), "
         "handles unrated records ('NEW', '-'), and consolidates multi-zone listings into exactly 9,244 verified, distinct physical dining establishments."),
        ("Objective 2: Statistical Quality Driver Identification via Hypothesis Testing",
         "Formulate and execute 9 formal parametric and non-parametric hypothesis tests (Welch's t-test, Mann-Whitney U, One-Way ANOVA, Kruskal-Wallis, Chi-Square, Pearson/Spearman) "
         "with standardized effect size metrics (Cohen's d, Eta-squared, Cramer's V) to isolate the true operational drivers of customer satisfaction."),
        ("Objective 3: Empirical Bayesian Shrinkage Rating Formulation",
         "Design and implement a Bayesian shrinkage rating engine (R_Bayes = (v/(v+m))*R + (m/(v+m))*C) with an empirical threshold m = 100 votes and citywide prior mean C = 3.63 stars, "
         "regularizing low-sample noise toward the prior while preserving authentic high-volume landmarks."),
        ("Objective 4: Econometric & Machine Learning Modeling",
         "Train an Ordinary Least Squares (OLS) Multiple Linear Regression model with Variance Inflation Factor (VIF) collinearity diagnostics and a Binary Logistic Classification model "
         "(target: rating >= 4.0) with odds ratios and ROC-AUC validation, quantifying marginal rating lifts for managerial decision-making."),
        ("Objective 5: Unsupervised Market Segmentation",
         "Apply K-Means clustering (supported by Elbow and Silhouette validation) on standardized dining cost, review volume, and rating to discover actionable business clusters (Budget Casual, Mid-Range Social, Premium Fine Dining)."),
        ("Objective 6: Algorithmic Multi-Criteria Recommendation Engine & Live Deployment",
         "Formulate a composite recommendation utility scoring algorithm combining Bayesian quality, value-for-money percentiles, and popularity, and operationalize it within an interactive Streamlit web application.")
    ]
    for o_title, o_desc in objs:
        story.append(Paragraph(f"• <b>{o_title}:</b> {o_desc}", styles['BulletText']))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: PROPOSED DATASET AND ITS SOURCE
    # =========================================================================
    story.append(Paragraph("5. Proposed Dataset and Its Source", styles['SecHeading1']))
    story.append(Paragraph(
        "<b>Dataset Identification:</b> Bangalore Metropolitan Restaurant Listing Dataset (Zomato Open Data Archive / Kaggle Repository).<br/>"
        "<b>Source URL / Origin:</b> Extracted from Zomato's public Bangalore listings via web scraping, published openly for academic research.<br/>"
        "<b>Original Dataset Volume:</b> 51,717 raw observation records across 17 attributes.<br/>"
        "<b>Consolidated Analytic Volume:</b> 9,244 distinct, physically verified restaurant units post-deduplication.",
        styles['AcademicBody']
    ))
    story.append(Paragraph(
        "The dataset captures the entire commercial dining ecosystem of metropolitan Bangalore across major geographical zones including Koramangala, "
        "Indiranagar, Whitefield, Jayanagar, HSR Layout, MG Road, and Malleshwaram. Table 1 defines the proposed variable schema, data types, and operational roles.",
        styles['AcademicBody']
    ))

    # Schema Table
    schema_data = [
        [Paragraph("<b>Variable Name</b>", styles['TableHeader']), Paragraph("<b>Data Type</b>", styles['TableHeader']), Paragraph("<b>Operational Role</b>", styles['TableHeader']), Paragraph("<b>Description & Domain Range</b>", styles['TableHeader']), Paragraph("<b>Sample Value</b>", styles['TableHeader'])],
        [Paragraph("name", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Identifier", styles['TableCell']), Paragraph("Registered trade name of dining outlet", styles['TableCell']), Paragraph("Truffles, Toit", styles['TableCell'])],
        [Paragraph("online_order", styles['TableCellBold']), Paragraph("Binary (0/1)", styles['TableCellCenter']), Paragraph("Predictor (Operational)", styles['TableCell']), Paragraph("Whether home delivery is enabled", styles['TableCell']), Paragraph("1 (Yes) / 0 (No)", styles['TableCellCenter'])],
        [Paragraph("book_table", styles['TableCellBold']), Paragraph("Binary (0/1)", styles['TableCellCenter']), Paragraph("Predictor (Operational)", styles['TableCell']), Paragraph("Whether table booking is enabled", styles['TableCell']), Paragraph("1 (Yes) / 0 (No)", styles['TableCellCenter'])],
        [Paragraph("rate", styles['TableCellBold']), Paragraph("Float (1.0-5.0)", styles['TableCellCenter']), Paragraph("Continuous Target", styles['TableCell']), Paragraph("Observed arithmetic mean star rating", styles['TableCell']), Paragraph("3.80 (Range: 1.8 - 4.9)", styles['TableCell'])],
        [Paragraph("votes", styles['TableCellBold']), Paragraph("Integer", styles['TableCellCenter']), Paragraph("Predictor / Weight", styles['TableCell']), Paragraph("Count of customer review ratings", styles['TableCell']), Paragraph("245 (Max: 16,832)", styles['TableCell'])],
        [Paragraph("location", styles['TableCellBold']), Paragraph("Categorical", styles['TableCellCenter']), Paragraph("Predictor (Spatial)", styles['TableCell']), Paragraph("Neighborhood / commercial dining zone", styles['TableCell']), Paragraph("Koramangala, Indiranagar", styles['TableCell'])],
        [Paragraph("rest_type", styles['TableCellBold']), Paragraph("Categorical", styles['TableCellCenter']), Paragraph("Predictor (Format)", styles['TableCell']), Paragraph("Primary dining format classification", styles['TableCell']), Paragraph("Quick Bites, Casual Dining", styles['TableCell'])],
        [Paragraph("cost_for_two", styles['TableCellBold']), Paragraph("Float (INR)", styles['TableCellCenter']), Paragraph("Predictor (Economic)", styles['TableCell']), Paragraph("Estimated dining expenditure for two", styles['TableCell']), Paragraph("₹600.0 (Range: ₹40 - ₹6,000)", styles['TableCell'])],
        [Paragraph("listed_in(type)", styles['TableCellBold']), Paragraph("Categorical", styles['TableCellCenter']), Paragraph("Predictor (Listing)", styles['TableCell']), Paragraph("Category of listing (Delivery, Dine-out, Pub)", styles['TableCell']), Paragraph("Delivery, Buffet, Cafes", styles['TableCell'])],
        [Paragraph("cuisines", styles['TableCellBold']), Paragraph("String", styles['TableCellCenter']), Paragraph("Metadata / Filter", styles['TableCell']), Paragraph("Specialty food offerings list", styles['TableCell']), Paragraph("North Indian, Continental", styles['TableCell'])],
        [Paragraph("bayes_rating", styles['TableCellBold']), Paragraph("Float (Engineered)", styles['TableCellCenter']), Paragraph("Engineered Metric", styles['TableCell']), Paragraph("Bayesian shrinkage trusted rating", styles['TableCell']), Paragraph("3.75 (Range: 2.76 - 4.88)", styles['TableCell'])],
        [Paragraph("value_pct", styles['TableCellBold']), Paragraph("Float (Engineered)", styles['TableCellCenter']), Paragraph("Engineered Metric", styles['TableCell']), Paragraph("Value-for-money empirical percentile", styles['TableCell']), Paragraph("84.5th Percentile", styles['TableCell'])],
        [Paragraph("is_high_rated", styles['TableCellBold']), Paragraph("Binary (Engineered)", styles['TableCellCenter']), Paragraph("Classification Target", styles['TableCell']), Paragraph("1 if rate >= 4.0 else 0", styles['TableCell']), Paragraph("0 (77.2%), 1 (22.8%)", styles['TableCellCenter'])]
    ]
    t_schema = Table(schema_data, colWidths=[80, 70, 95, 175, 70])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 10))

    # Exploratory Data Figures for DA 1
    story.append(Paragraph("5.1 Preliminary Exploratory Data Distributions", styles['SecHeading2']))
    story.append(Paragraph(
        "Initial inspection of the dataset reveals critical distributional characteristics that inform the proposed modeling strategy. "
        "Figure 1 displays the empirical distribution of observed customer ratings, while Figure 2 illustrates the extreme right-skewness "
        "present in customer review votes and dining costs across Bangalore.",
        styles['AcademicBody']
    ))

    fig1_path = "results/figures/ratings_distribution.png"
    if os.path.exists(fig1_path):
        story.append(Image(fig1_path, width=440, height=190))
        story.append(Paragraph("<b>Figure 1: Distribution of Customer Ratings across Bangalore Restaurants (N = 9,244)</b>", styles['FigureCaption']))
        story.append(Paragraph(
            "<b>Exploratory Analysis:</b> The observed ratings follow a bell-shaped distribution centered at a citywide mean of 3.63 stars (median = 3.70, std = 0.43). "
            "Ratings span from 1.8 to 4.9 stars, with mild negative skewness (-0.21). Outlets achieving 4.0 stars or higher constitute 22.8% of the market, "
            "providing a naturally balanced binary threshold for logistic classification modeling.",
            styles['FigureAnalysis']
        ))
        story.append(Spacer(1, 6))

    fig2_path = "results/figures/cost_votes_distribution.png"
    if os.path.exists(fig2_path):
        story.append(Image(fig2_path, width=440, height=190))
        story.append(Paragraph("<b>Figure 2: Empirical Distribution of Review Votes and Dining Cost for Two</b>", styles['FigureCaption']))
        story.append(Paragraph(
            "<b>Exploratory Analysis:</b> Review votes exhibit severe positive skewness (+9.06) with a heavy right tail extending to 16,832 votes while the median is only 53. "
            "Dining cost similarly exhibits right skewness (+3.21) with a median of ₹400 and an upper extreme of ₹6,000. These non-normal distributions justify "
            "the proposed natural logarithmic transformations ln(votes + 1) and ln(cost) prior to parametric econometric modeling.",
            styles['FigureAnalysis']
        ))
        story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: PROPOSED METHODOLOGY AND STATISTICAL TECHNIQUES
    # =========================================================================
    story.append(Paragraph("6. Proposed Methodology and Statistical Techniques", styles['SecHeading1']))
    story.append(Paragraph(
        "The project methodology is structured as a rigorous, four-tier analytical pipeline ensuring data integrity, statistical validity, "
        "econometric interpretability, and production-ready decision support.",
        styles['AcademicBody']
    ))

    # Architecture Overview
    story.append(Paragraph("6.1 Proposed Four-Tier System Architecture", styles['SecHeading2']))
    arch_bullets = [
        ("Tier 1: Data Ingestion & Sanitization Engine", "Executes automated text cleaning, regex currency extraction, mode imputation, and entity-level deduplication to produce 9,244 physical records."),
        ("Tier 2: Statistical Inference & Hypothesis Testing Suite", "Performs paired parametric and non-parametric tests with standardized effect sizes to evaluate operational quality drivers."),
        ("Tier 3: Econometric Modeling & Machine Learning Suite", "Estimates OLS regression with VIF collinearity checks, binary logistic regression with odds ratios, and K-Means clustering with silhouette validation."),
        ("Tier 4: Multi-Criteria Recommendation & Interactive Web UI", "Vectorizes Bayesian shrinkage ratings, computes value-for-money percentiles, and deploys an interactive Streamlit dashboard for real-time consumer discovery.")
    ]
    for ab_t, ab_d in arch_bullets:
        story.append(Paragraph(f"• <b>{ab_t}:</b> {ab_d}", styles['BulletText']))
    story.append(Spacer(1, 8))

    # Proposed 8-Step Preprocessing Table
    story.append(Paragraph("6.2 Proposed 8-Step Data Preprocessing Pipeline", styles['SecHeading2']))
    prep_steps = [
        [Paragraph("<b>Step #</b>", styles['TableHeader']), Paragraph("<b>Cleaning Stage</b>", styles['TableHeader']), Paragraph("<b>Proposed Transformation & Mathematical Operation</b>", styles['TableHeader']), Paragraph("<b>Methodological Rationale</b>", styles['TableHeader'])],
        [Paragraph("1", styles['TableCellCenter']), Paragraph("Raw Ingestion", styles['TableCellBold']), Paragraph("Ingest 51,717 raw CSV records into Pandas DataFrame", styles['TableCell']), Paragraph("Establish initial baseline schema and row count", styles['TableCell'])],
        [Paragraph("2", styles['TableCellCenter']), Paragraph("Rating Parsing", styles['TableCellBold']), Paragraph("Regex parse 'X.X/5' -> float; isolate 'NEW' and '-' entries", styles['TableCell']), Paragraph("Extract numerical target; prevent zero-inflation from unrated records", styles['TableCell'])],
        [Paragraph("3", styles['TableCellCenter']), Paragraph("Cost Sanitization", styles['TableCellBold']), Paragraph("Strip commas (e.g. '1,200' -> 1200.0) and cast to float", styles['TableCell']), Paragraph("Enable continuous numerical calculations on dining spend", styles['TableCell'])],
        [Paragraph("4", styles['TableCellCenter']), Paragraph("Binary Mapping", styles['TableCellBold']), Paragraph("Map 'Yes'/'No' to integer flags (1/0) for online_order and book_table", styles['TableCell']), Paragraph("Standardize boolean predictors for regression and classification", styles['TableCell'])],
        [Paragraph("5", styles['TableCellCenter']), Paragraph("Entity Deduplication", styles['TableCellBold']), Paragraph("Group by (name, address, location); aggregate votes", styles['TableCell']), Paragraph("Eliminate multi-listing scrape duplicates; satisfy i.i.d. assumption", styles['TableCell'])],
        [Paragraph("6", styles['TableCellCenter']), Paragraph("Categorical Mode Imputation", styles['TableCellBold']), Paragraph("Impute missing cuisine types with mode; prune uninformative URLs", styles['TableCell']), Paragraph("Ensure complete case analysis without dropping valuable records", styles['TableCell'])],
        [Paragraph("7", styles['TableCellCenter']), Paragraph("Log Transformation", styles['TableCellBold']), Paragraph("Compute ln(votes + 1) and ln(cost_for_two)", styles['TableCell']), Paragraph("Resolve severe positive skewness; satisfy OLS normality assumptions", styles['TableCell'])],
        [Paragraph("8", styles['TableCellCenter']), Paragraph("Percentile & Scaling", styles['TableCellBold']), Paragraph("Calculate empirical CDF percentiles for value and scale ML features", styles['TableCell']), Paragraph("Normalize multi-criteria dimensions; prepare features for K-Means and Logit", styles['TableCell'])]
    ]
    t_prep = Table(prep_steps, colWidths=[40, 100, 190, 160])
    t_prep.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_prep)
    story.append(Spacer(1, 10))

    # Proposed Statistical Techniques & Hypothesis Testing
    story.append(Paragraph("6.3 Proposed Statistical Techniques and Hypothesis Testing Matrix", styles['SecHeading2']))
    story.append(Paragraph(
        "To establish rigorous empirical relationships before predictive modeling, nine formal statistical hypothesis tests are proposed. "
        "Because customer review counts and costs deviate from normality, tests are designed with paired parametric and non-parametric counterparts "
        "and accompanied by standardized effect size metrics to prevent sample-size driven p-value fallacies. Table 3 outlines the testing matrix.",
        styles['AcademicBody']
    ))

    hypo_matrix = [
        [Paragraph("<b>#</b>", styles['TableHeader']), Paragraph("<b>Test Name</b>", styles['TableHeader']), Paragraph("<b>Null Hypothesis (H0)</b>", styles['TableHeader']), Paragraph("<b>Technique</b>", styles['TableHeader']), Paragraph("<b>Effect Size Metric</b>", styles['TableHeader'])],
        [Paragraph("1", styles['TableCellCenter']), Paragraph("Online Order vs Rating", styles['TableCellBold']), Paragraph("Mean rating equal with or without online order (mu1 = mu2)", styles['TableCell']), Paragraph("Welch's t-test", styles['TableCellCenter']), Paragraph("Cohen's d", styles['TableCellCenter'])],
        [Paragraph("2", styles['TableCellCenter']), Paragraph("Table Booking vs Rating", styles['TableCellBold']), Paragraph("Mean rating equal with or without table booking (mu1 = mu2)", styles['TableCell']), Paragraph("Welch's t-test", styles['TableCellCenter']), Paragraph("Cohen's d", styles['TableCellCenter'])],
        [Paragraph("3", styles['TableCellCenter']), Paragraph("Listing Type vs Rating", styles['TableCellBold']), Paragraph("Mean ratings identical across 6 listing types", styles['TableCell']), Paragraph("One-Way ANOVA", styles['TableCellCenter']), Paragraph("Eta-squared (eta^2)", styles['TableCellCenter'])],
        [Paragraph("4", styles['TableCellCenter']), Paragraph("Location vs Rating", styles['TableCellBold']), Paragraph("Mean ratings identical across top 10 dining locations", styles['TableCell']), Paragraph("One-Way ANOVA", styles['TableCellCenter']), Paragraph("Eta-squared (eta^2)", styles['TableCellCenter'])],
        [Paragraph("5", styles['TableCellCenter']), Paragraph("Cost across Listing Types", styles['TableCellBold']), Paragraph("Mean dining cost identical across listing types", styles['TableCell']), Paragraph("One-Way ANOVA", styles['TableCellCenter']), Paragraph("Eta-squared (eta^2)", styles['TableCellCenter'])],
        [Paragraph("6", styles['TableCellCenter']), Paragraph("Non-Parametric Rating Dist.", styles['TableCellBold']), Paragraph("Rating distributions identical across listing categories", styles['TableCell']), Paragraph("Kruskal-Wallis", styles['TableCellCenter']), Paragraph("Epsilon-squared (eps^2)", styles['TableCellCenter'])],
        [Paragraph("7", styles['TableCellCenter']), Paragraph("Table Booking vs Rest Type", styles['TableCellBold']), Paragraph("Table booking is independent of restaurant format", styles['TableCell']), Paragraph("Chi-Square (chi^2)", styles['TableCellCenter']), Paragraph("Cramer's V", styles['TableCellCenter'])],
        [Paragraph("8", styles['TableCellCenter']), Paragraph("Online Order vs Listing Type", styles['TableCellBold']), Paragraph("Online ordering is independent of listing category", styles['TableCell']), Paragraph("Chi-Square (chi^2)", styles['TableCellCenter']), Paragraph("Cramer's V", styles['TableCellCenter'])],
        [Paragraph("9", styles['TableCellCenter']), Paragraph("Cost vs Rating Correlation", styles['TableCellBold']), Paragraph("Population correlation between cost and rating is zero (rho = 0)", styles['TableCell']), Paragraph("Pearson / Spearman", styles['TableCellCenter']), Paragraph("r and rho", styles['TableCellCenter'])]
    ]
    t_hypo = Table(hypo_matrix, colWidths=[25, 125, 185, 85, 70])
    t_hypo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_hypo)
    story.append(Spacer(1, 10))

    # Proposed Mathematical Formulations Box
    math_text = (
        "<b>1. Bayesian Shrinkage Rating:</b> R_Bayes = [v / (v + m)] * R + [m / (v + m)] * C<br/>"
        "Where v = observed votes, R = observed rating, C = citywide prior mean (3.63 stars), m = shrinkage threshold (100 votes). "
        "For small samples (v << m), R_Bayes shrinks to prior C. For large samples (v >> m), R_Bayes approaches observed R.<br/><br/>"
        "<b>2. Multi-Criteria Composite Utility:</b> Composite = w_r * (R_Bayes / 5.0 * 100) + w_v * V_pct + w_p * P_norm<br/>"
        "Where V_pct = Empirical Percentile(R_Bayes / cost_for_two), P_norm = [ln(v + 1) / max ln(v + 1)] * 100, and w_r + w_v + w_p = 1.0.<br/><br/>"
        "<b>3. Econometric OLS Model:</b> rate_i = beta_0 + beta_1*online_order_i + beta_2*book_table_i + beta_3*ln(votes_i) + beta_4*ln(cost_i) + sum(gamma_k*D_ik) + eps_i<br/><br/>"
        "<b>4. Binary Logistic Model:</b> ln[P(rate >= 4.0) / (1 - P(rate >= 4.0))] = X * beta; Odds Ratio (OR) = exp(beta_j)"
    )
    story.append(create_callout_box(math_text, title="Proposed Mathematical Specifications & Formulations"))
    story.append(Spacer(1, 10))

    # Architecture Diagram Screenshot
    fig7_path = "results/figures/dashboard_screenshots/tab7_methodology.png"
    if os.path.exists(fig7_path):
        story.append(Image(fig7_path, width=440, height=200))
        story.append(Paragraph("<b>Figure 3: Proposed System Methodology and Deployed Dashboard Architecture</b>", styles['FigureCaption']))
        story.append(Paragraph(
            "<b>Architectural Flow:</b> Visual representation of the modular pipeline connecting data sanitation, statistical hypothesis verification, "
            "econometric regression, unsupervised segmentation, and the reactive decision-support interface.",
            styles['FigureAnalysis']
        ))
        story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: EXPECTED RECOMMENDATIONS AND OUTCOMES
    # =========================================================================
    story.append(Paragraph("7. Expected Recommendations and Outcomes", styles['SecHeading1']))
    story.append(Paragraph(
        "Upon successful execution of the proposed software and modeling pipeline, the project delivers the following tangible "
        "analytical outcomes, managerial guidelines, and software artifacts:",
        styles['AcademicBody']
    ))

    # Outcomes Breakdown
    story.append(Paragraph("7.1 Expected Analytical and Machine Learning Outcomes", styles['SecHeading2']))
    story.append(Paragraph(
        "• <b>Econometric Quantification of Operational Drivers:</b> The OLS model is expected to confirm that table reservation infrastructure "
        "provides a large, statistically significant positive marginal lift on customer ratings (anticipated beta > +0.20 stars, t > 10.0), "
        "whereas online delivery enablement will show minimal direct rating impact after controlling for format and locality.",
        styles['BulletText']
    ))
    story.append(Paragraph(
        "• <b>Discriminative Power in High-Tier Classification:</b> The binary logistic classification model is anticipated to achieve an "
        "outstanding ROC-AUC (> 0.90) and accuracy (> 85%), demonstrating that high-rated dining status is strongly predictable based on "
        "review evidence volume, table booking status, and geographic clustering.",
        styles['BulletText']
    ))
    story.append(Paragraph(
        "• <b>Market Structure Discovery:</b> Unsupervised K-Means clustering is expected to segment Bangalore's dining market into three distinct, "
        "operationally coherent clusters: Budget Casual Dining, Mid-Range Social/Takeaway Outlets, and Premium/Fine Dining Institutions.",
        styles['BulletText']
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.2 Expected Recommendations for Key Stakeholders", styles['SecHeading2']))
    recs = [
        ("For Consumers & Urban Diners",
         "Eliminate exposure to low-evidence rating fraud by adopting Bayesian shrinkage scores. Provide actionable value discovery enabling diners to locate 90th-percentile value-for-money culinary gems in residential pockets (e.g., Basavanagudi, Jayanagar) rather than overpaying in high-rent zones."),
        ("For Restaurant Operators & Hospitality Entrepreneurs",
         "Prioritize capital investment into dine-in customer hospitality and reservation infrastructure over delivery packaging, as table reservation yields a 3x higher odds ratio of reaching premier 4-star status. Recognize that online ordering operates as a hygiene/convenience channel rather than a rating booster."),
        ("For Food-Tech Aggregator Platforms (e.g., Zomato, Swiggy)",
         "Transition default search ranking algorithms away from naive arithmetic averages toward Bayesian shrinkage estimators. Expose normalized Value-for-Money percentile ratings to protect consumer trust and disincentivize fake review manipulation.")
    ]
    for r_title, r_desc in recs:
        story.append(Paragraph(f"• <b>{r_title}:</b> {r_desc}", styles['BulletText']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("7.3 Expected Software & Systems Deliverables", styles['SecHeading2']))
    story.append(Paragraph(
        "1. <b>Production Codebase:</b> Fully modular Python pipeline (`src/data_processing.py`, `src/statistical_analysis.py`, `src/modeling.py`, `src/recommender.py`).<br/>"
        "2. <b>Interactive Web Dashboard:</b> 7-tab reactive Streamlit web application supporting dynamic multi-criteria filtering, parametric hypothesis exploration, live model diagnostics, and real-time restaurant recommendation.<br/>"
        "3. <b>Comprehensive Academic Documentation:</b> Formal research reports detailing the complete data analytics lifecycle.",
        styles['AcademicBody']
    ))

    # Build document
    doc.build(story, canvasmaker=CleanNumberedCanvasDA1)
    print(f"Successfully generated clean DA 1 Report: {pdf_filename}")


if __name__ == "__main__":
    build_da1_report_pdf()
