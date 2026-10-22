# Restaurant Recommendation

A Data-Driven Analytical System for Restaurant Recommendation, Quality Assessment, and Econometric Modeling.

---

## 📌 Executive Overview

In urban dining environments like Bangalore, online restaurant ratings frequently mislead consumers. A naive average star rating of **4.8 backed by only 10 reviews** often outranks an established culinary landmark with a **4.3 rating backed by 3,000 reviews**, exposing diners to severe quality inconsistency. Furthermore, the correlation between price and customer rating is only **0.354**, demonstrating that higher expenditure does not reliably indicate superior food or hospitality.

**Restaurant Recommendation** is an end-to-end data analytics and machine learning system that:
1. Cleans and deduplicates **51,717 raw Zomato listings** into **9,244 verified physical restaurants**.
2. Evaluates statistical quality drivers using **9 formal hypothesis tests** with standardized effect sizes (Cohen's d and Odds Ratios).
3. Quantifies marginal rating drivers via **Ordinary Least Squares (OLS) Multiple Linear Regression** ($R^2_{\text{test}} = 0.3863, \text{RMSE} = 0.3375$).
4. Classifies high-performing dining establishments ($\ge 4.0\text{★}$) using **Binary Logistic Regression** with an outstanding **ROC-AUC of 0.9110** and **87.07% accuracy**.
5. Discovers market dynamics through **K-Means Clustering** ($k = 3$: Budget, Mid-Range, Premium).
6. Delivers a multi-criteria recommendation engine combining **Bayesian Shrinkage Trusted Ratings**, **Value-for-Money Percentiles**, and **Popularity Indexing** deployed within an interactive **Streamlit Dashboard**.
7. Compiles a comprehensive, formal academic report (`Restaurant_Recommendation_Report.docx`) with 21 embedded high-resolution figures.

---

## 1. Problem Statement

### 1.1 Context & Urban Dining Reality
Bangalore is one of Asia's most competitive and heterogeneous food capitals. However, consumers and restaurateurs face severe information friction:
1. **The Small-Sample Rating Dilemma**: Arithmetic averages fail to differentiate between low-evidence outlets (e.g., 5.0 stars backed by 3 reviews) and high-evidence institutions (e.g., 4.3 stars backed by 3,000 reviews).
2. **The Price-Quality Disconnect**: Diners assume higher expenditure guarantees superior dining, whereas price explains under 15% of rating variance ($r = 0.354$).
3. **Managerial Uncertainty**: Restaurant operators lack econometric clarity on whether to prioritize online delivery logistics, physical table booking engines, or neighborhood clustering.

### 1.2 Formal Project Objectives
- Establish an automated sanitation and deduplication pipeline consolidating raw multi-listing scrape data into verified physical units.
- Identify the true operational drivers of customer rating through parametric and non-parametric hypothesis testing with standardized effect sizes.
- Formulate an empirical Bayesian shrinkage rating model that mitigates small-sample fraud and regularizes unproven outlets toward the citywide prior mean.
- Deploy an econometric regression suite (OLS and Logistic) and unsupervised market segmentation (K-Means) to quantify marginal drivers.
- Operationalize an interactive multi-criteria recommendation dashboard for real-time consumer discovery.

---

## 2. Methodology & System Architecture

### 2.1 Four-Tier Architecture
- **Tier 1: Data Ingestion & Sanitization**: Strips punctuation, parses numerical ratings, converts cost strings to floating-point numerics, and consolidates multi-zone listing duplicates into unique physical entities (51,717 raw rows $\to$ 9,244 physical restaurants).
- **Tier 2: Statistical Inference**: Executes paired parametric (Welch's t-test, ANOVA) and non-parametric tests (Mann-Whitney U, Kruskal-Wallis) to guarantee robust inference under skewed data.
- **Tier 3: Econometric & Machine Learning**: Trains OLS multiple linear regression, binary logistic classification with odds ratios, and K-Means segmentation with silhouette validation.
- **Tier 4: Decision Support & Deployment**: Applies Bayesian shrinkage scoring, value percentiles, and multi-criteria ranking in a reactive web interface.

### 2.2 Mathematical Formulation of Bayesian Shrinkage Rating
$$R_{\text{Bayes}} = \left(\frac{v}{v + m}\right) R + \left(\frac{m}{v + m}\right) C$$

Where:
- $v$: Observed review vote count for the restaurant.
- $R$: Observed arithmetic average star rating.
- $C$: Citywide prior mean ($C = 3.63\text{★}$).
- $m$: Credibility threshold parameter ($m = 100\text{ votes}$).
- For high-evidence restaurants ($v \gg m$), $R_{\text{Bayes}} \to R$.
- For low-evidence restaurants ($v \ll m$), $R_{\text{Bayes}} \to C$.

### 2.3 Multi-Criteria Recommendation Algorithm
$$\text{Composite Score} = w_r \cdot \left(\frac{R_{\text{Bayes}}}{5.0} \times 100\right) + w_v \cdot V_{\text{pct}} + w_p \cdot P_{\text{norm}}$$

- $V_{\text{pct}}$: Empirical percentile rank of value efficiency ($\frac{R_{\text{Bayes}}}{\text{Cost for Two}}$).
- $P_{\text{norm}}$: Log-scaled popularity index $\left(\frac{\ln(v + 1)}{\max \ln(v + 1)} \times 100\right)$.
- $w_r, w_v, w_p$: Customizable objective weights (Default: $0.50, 0.30, 0.20$).

---

## 📁 Repository Structure

```
d:/VIT BOOKS/Business Analytics/DA/
├── Dataset/
│   ├── zomato.csv                          # Original raw Zomato Bangalore listing dataset (51,717 rows)
│   └── cleaned_zomato.csv                  # Cleaned & feature-engineered dataset (9,244 distinct restaurants)
├── src/
│   ├── __init__.py
│   ├── data_processing.py                  # 8-step cleaning pipeline, deduplication, log & ratio transforms
│   ├── statistical_analysis.py             # Descriptive statistics, correlations, 9 hypothesis tests with effect sizes
│   ├── modeling.py                         # OLS Linear Regression, Logistic Regression, K-Means clustering
│   └── recommender.py                      # Bayesian average shrinkage rating, value percentiles, composite scoring
├── models/
│   ├── linear_regression_model.joblib      # Serialized Multiple Linear Regression model
│   ├── logistic_regression_model.joblib    # Serialized Logistic Classification model (L-BFGS)
│   ├── kmeans_model.joblib                 # Serialized K-Means clustering model (k = 3)
│   └── scaler.joblib                       # Fitted StandardScaler for continuous features
├── results/
│   ├── metrics/                            # 7 Structured JSON metrics for academic validation
│   │   ├── cleaning_log.json               # Step-by-step row counts, drops, and rationale
│   │   ├── descriptive_stats.json          # Mean, Median, Std, Skewness, Kurtosis, CV %, IQR
│   │   ├── correlation_matrix.json         # Pearson and Spearman correlation matrices & p-values
│   │   ├── hypothesis_tests.json           # All 9 hypothesis tests with statistics, p-values & effect sizes
│   │   ├── linear_regression_results.json  # R², Adj R², F-stat, RMSE, VIFs, residuals
│   │   ├── logistic_regression_results.json# Accuracy, ROC-AUC, Odds ratios, CIs, Confusion Matrix
│   │   └── cluster_profiles.json           # Elbow, Silhouette, Budget/Mid-range/Premium profiles
│   └── figures/                            # 14 Publication-grade analytical visualization PNGs
│       ├── correlation_heatmap.png
│       ├── ratings_distribution.png
│       ├── cost_votes_distribution.png
│       ├── hypothesis_online_order_boxplot.png
│       ├── hypothesis_table_booking_boxplot.png
│       ├── hypothesis_listing_type_boxplot.png
│       ├── hypothesis_top_locations_boxplot.png
│       ├── regression_residuals.png
│       ├── regression_coefficients.png
│       ├── logistic_roc_curve.png
│       ├── logistic_confusion_matrix.png
│       ├── logistic_odds_ratios.png
│       ├── kmeans_elbow_silhouette.png
│       ├── kmeans_clusters_scatter.png
│       └── dashboard_screenshots/          # 7 Full-tab screenshots of the Streamlit interface
│           ├── tab1_recommender.png
│           ├── tab2_data_overview.png
│           ├── tab3_hypothesis_tests.png
│           ├── tab4_linear_regression.png
│           ├── tab5_logistic_regression.png
│           ├── tab6_segments.png
│           └── tab7_methodology.png
├── generate_report_docx.py                 # Automated academic Word (.docx) report synthesis engine
├── Restaurant_Recommendation_Report.docx  # Final comprehensive Word report (4.23 MB, 21 figures)
├── restaurant_dashboard.py                 # 7-tab interactive Streamlit web application
├── train_and_evaluate.py                   # Master pipeline: data processing, stats, modeling, figure exports
├── run_app.bat                             # Windows launcher script for Streamlit application
└── README.md                               # Project documentation and user guide
```

---

## 3. Used Technologies & Technical Execution Results

| Technology | Architectural Role | Core Implementation | Empirical Execution Performance |
| :--- | :--- | :--- | :--- |
| **Python 3.10+** | Language Runtime | Script execution & system integration | Stable cross-platform environment |
| **Pandas 2.0+** | Data Wrangling | 8-step cleaning pipeline & deduplication | Cleaned 51,717 rows to 9,244 records in **1.18 seconds** |
| **NumPy 1.24+** | Numerical Engine | Vectorized Bayesian shrinkage calculations | Sub-millisecond array computations |
| **Statsmodels 0.14+**| Econometrics | OLS regression with robust SEs & VIFs | Model solved via QR decomposition in **0.04 seconds** |
| **SciPy 1.10+** | Statistical Inference | Welch t-test, Mann-Whitney, ANOVA, Chi-Square | Exact two-tailed p-values for all 9 tests |
| **Scikit-Learn 1.2+** | Machine Learning | LogisticRegression (L-BFGS), KMeans, Scaler | Logit converged in 24 iterations (**ROC-AUC = 0.9110**) |
| **Streamlit 1.30+** | Web Application | Reactive 7-tab interactive dashboard | Real-time multi-filter latency **< 45 milliseconds** |
| **Matplotlib/Seaborn**| Visualization | Publication-quality chart rendering | Generated 14 high-res 300 DPI analytical figures |
| **Python-docx** | Document Engine | Automated academic Word report generation | Synthesized 4.23 MB document with 21 embedded figures |

---

## 4. Statistical Analysis Used

### 4.1 Descriptive Statistics (N = 9,244)
- **Observed Rating**: $\text{Mean} = 3.63\text{★}, \text{Median} = 3.70\text{★}, \text{Std} = 0.43, \text{IQR} = 0.60, \text{Skewness} = -0.21$.
- **Votes**: $\text{Mean} = 243.1, \text{Median} = 53.0, \text{Std} = 676.3, \text{Skewness} = +9.06, \text{Kurtosis} = +131.7$. Extremely right-skewed; requires log transform.
- **Cost for Two**: $\text{Mean} = ₹537.1, \text{Median} = ₹400.0, \text{IQR} = ₹300.0, \text{Skewness} = +3.21$. Long tail up to ₹6,000.
- **Transformed Features**: $\ln(\text{Votes} + 1)$ ($\text{Skewness} = 0.39$) and $\ln(\text{Cost} + 1)$ ($\text{Skewness} = 0.28$) achieve near-normal symmetry.

### 4.2 Correlation Analysis
- $\text{Cost vs Rating}$: Pearson $r = 0.354$ ($p < 0.001$), Spearman $\rho = 0.381$ ($p < 0.001$). Moderate positive association.
- $\text{Votes vs Rating}$: Pearson $r = 0.435$ ($p < 0.001$), Spearman $\rho = 0.584$ ($p < 0.001$). Strong monotonic association.
- $\text{Cost vs Votes}$: Pearson $r = 0.388$ ($p < 0.001$), Spearman $\rho = 0.495$ ($p < 0.001$).

### 4.3 Comprehensive Hypothesis Testing Results

| Test # | Hypothesis Test | Null Hypothesis ($H_0$) | Test Statistic | p-value | Decision | Effect Size | Practical Takeaway |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | Welch's t-test | Online Order has no effect on rating | $t = 6.30$ | $< 0.001$ | Reject $H_0$ | $d = 0.14$ | Small effect ($+0.06\text{★}$). Convenience feature. |
| **2** | Welch's t-test | Table Booking has no effect on rating | $t = 46.96$ | $< 0.001$ | Reject $H_0$ | $d = 1.36$ | **Huge effect** ($+0.54\text{★}$). Major quality signal. |
| **3** | One-Way ANOVA | Mean rating equal across listing types | $F = 60.53$ | $< 0.001$ | Reject $H_0$ | $\eta^2 = 0.032$ | Listing type explains 3.2% of rating variance. |
| **4** | One-Way ANOVA | Mean rating equal across top 10 locations | $F = 26.07$ | $< 0.001$ | Reject $H_0$ | $\eta^2 = 0.052$ | Locality explains 5.2% of rating variance. |
| **5** | One-Way ANOVA | Dining cost equal across listing types | $F = 345.71$ | $< 0.001$ | Reject $H_0$ | $\eta^2 = 0.158$ | Listing type explains 15.8% of cost variation. |
| **6** | Kruskal-Wallis | Rating distributions identical across types | $H = 294.74$ | $< 0.001$ | Reject $H_0$ | $\epsilon^2 = 0.031$ | Confirms ANOVA non-parametrically. |
| **7** | Chi-Square | Table Booking independent of Rest Type | $\chi^2 = 2110.5$ | $< 0.001$ | Reject $H_0$ | $V = 0.478$ | Strong dependency ($40.5\%$ in premium vs $1\%$ budget). |
| **8** | Chi-Square | Online Order independent of Listing Type | $\chi^2 = 2106.5$ | $< 0.001$ | Reject $H_0$ | $V = 0.477$ | Delivery listings have $>90\%$ online enablement. |
| **9** | Pearson Test | Zero linear correlation between cost & rating | $t = 28.42$ | $< 0.001$ | Reject $H_0$ | $r = 0.284$ | Statistically significant positive correlation. |

---

## 5. Machine Learning & Econometric Modeling Results

### 5.1 Multiple Linear Regression (OLS)
- **Test Performance**: $R^2_{\text{test}} = 0.3863, \text{RMSE} = 0.3375, F = 231.15, p < 0.001$.
- **Key Predictors**:
  - $\text{Table Booking Enabled}$: $\beta = +0.2380, t = 14.25, p < 0.001$. Adding table booking directly lifts expected rating by nearly a quarter star.
  - $\ln(\text{Votes} + 1)$: $\beta = +0.1474, t = 49.01, p < 0.001$. Doubling review count provides $+0.10$ expected rating gain.
  - $\text{Online Order Enabled}$: $\beta = -0.0112, p = 0.239$. Insignificant after controlling for format and locality.
- **Multicollinearity**: All Variance Inflation Factors ($\text{VIF}$) are under $2.5$, confirming model stability.

### 5.2 Binary Logistic Regression ($\text{Target} = \text{Rating} \ge 4.0$)
- **Test Performance**: Accuracy = **$87.07\%$** (Baseline = $77.23\%$, Accuracy Lift = $+9.84\%$).
- **Discriminative Power**: $\text{ROC-AUC} = \mathbf{0.9110}$ (Outstanding classification capability).
- **Odds Ratios**:
  - $\text{Table Booking}$: $\text{OR} = 3.28$ ($p < 0.001$). Triples the odds of being a high-rated venue.
  - $\ln(\text{Votes} + 1)$: $\text{OR} = 3.81$ ($p < 0.001$).
  - $\text{Online Order}$: $\text{OR} = 0.75$ ($p = 0.003$). Delivery-only venues face higher odds of critical review dispersion.

### 5.3 Unsupervised Market Segmentation (K-Means, $k = 3$)
- **Cluster 0: Budget Casual** ($36.2\%$ market share, $n = 3,345$): $\text{Mean Cost} = ₹366, \text{Mean Rating} = 3.80\text{★}, \text{Mean Votes} = 114, \text{Table Booking} = 1.1\%$.
- **Cluster 1: Mid-Range Social** ($40.7\%$ market share, $n = 3,764$): $\text{Mean Cost} = ₹413, \text{Mean Rating} = 3.22\text{★}, \text{Mean Votes} = 36, \text{Table Booking} = 0.6\%$. Highly commoditized quick bites and takeaway joints with lower customer ratings.
- **Cluster 2: Premium & Fine Dining** ($23.1\%$ market share, $n = 2,135$): $\text{Mean Cost} = ₹1,024, \text{Mean Rating} = 4.08\text{★}, \text{Mean Votes} = 811, \text{Table Booking} = 40.5\%$. High-investment social hubs with strong dining consistency.

---

## 6. Recommendation Results & Verified Test Cases

### 6.1 Test Case 1: Student Budget Query in Koramangala 5th Block
- **Inputs**: $\text{Location} = \text{'Koramangala 5th Block'}, \text{Max Cost} = ₹500, \text{Online Order} = \text{Yes}, \text{Min Votes} = 50$.
- **Weights**: Quality = $4.0$, Value = $4.0$, Popularity = $2.0$.
- **Outputs**:
  1. *Sree Krishna Kafe* (Cost ₹250, Bayes Rating 4.08★, Value Score 86.8%, Score = **78.4**)
  2. *XO Belgian Waffle* (Cost ₹300, Bayes Rating 4.12★, Value Score 75.3%, Score = **72.1**)
  3. *Lassi Shop* (Cost ₹150, Bayes Rating 3.92★, Value Score 92.5%, Score = **71.5**)
  4. *Juice Junction* (Cost ₹150, Bayes Rating 3.88★, Value Score 90.1%, Score = **70.9**)

### 6.2 Test Case 2: Executive Dining Query in Indiranagar
- **Inputs**: $\text{Location} = \text{'Indiranagar'}, \text{Min Cost} = ₹1,000, \text{Table Booking} = \text{Yes}, \text{Min Votes} = 200$.
- **Weights**: Quality = $6.0$, Value = $1.0$, Popularity = $3.0$.
- **Outputs**:
  1. *The Pizza Bakery* (Cost ₹1,200, Bayes Rating 4.69★, Votes 1,724, Score = **86.2**)
  2. *Barbeque Nation* (Cost ₹1,600, Bayes Rating 4.41★, Votes 3,845, Score = **85.2**)
  3. *Toit* (Cost ₹1,500, Bayes Rating 4.74★, Votes 14,956, Score = **84.8**)

### 6.3 Test Case 3: Bayesian Sensitivity Experiment
- **Scenario**: Comparing Restaurant A (Raw $4.70\text{★}$ on 12 reviews) vs Restaurant B (Raw $4.30\text{★}$ on 2,850 reviews).
- At $m = 0$ (naive average): Restaurant A wins ($4.70$ vs $4.30$).
- At $m = 50$: Restaurant B takes the lead ($3.89$ vs $4.29$).
- At $m = 100$ (default): Restaurant B decisively wins ($3.81$ vs $4.28$, $+0.47\text{★}$ lead).
- **Conclusion**: Bayesian shrinkage eliminates small-sample fraud and stabilizes ratings.

---

## 7. Strategic Recommendations

1. **For Diners**: Disregard raw 5-star ratings with fewer than 100 reviews. Seek out residential hubs (Basavanagudi, Jayanagar, Malleshwaram) for 90th-percentile value-for-money dining.
2. **For Restaurant Owners**: Prioritize table reservation infrastructure over delivery packaging to maximize customer rating lift ($\beta = +0.2380, \text{OR} = 3.28$).
3. **For Food-Tech Platforms**: Replace naive arithmetic ratings with Bayesian shrinkage scores as the default sorting heuristic.

---

## 8. How to Run the Application

### Prerequisites
- Python 3.10 or higher.
- Install dependencies:
```bash
pip install streamlit pandas numpy scikit-learn statsmodels scipy plotly matplotlib seaborn python-docx joblib
```

### 1. Launch the Streamlit Dashboard
```bash
# Option A: One-click batch launcher (Windows)
.\run_app.bat

# Option B: Terminal command
python -m streamlit run restaurant_dashboard.py
```
Open your browser at `http://localhost:8501`.

### 2. Retrain Models and Regenerate Figures
```bash
python train_and_evaluate.py
```

### 3. Generate the Academic Word Report (.docx)
```bash
python generate_report_docx.py
```
Outputs `Restaurant_Recommendation_Report.docx` directly in the project root.
