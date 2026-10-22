"""
train_and_evaluate.py
Master Pipeline Execution Script:
1. Cleans dataset & generates features.
2. Computes descriptive statistics & correlation matrices.
3. Executes 9 formal hypothesis tests with effect sizes.
4. Fits & evaluates Multiple Linear Regression (OLS, VIF, Residual diagnostics).
5. Fits & evaluates Logistic Regression (Odds ratios, ROC-AUC, confusion matrix).
6. Trains K-Means clustering (Elbow, Silhouette, 3 segments: Budget, Mid-range, Premium).
7. Saves all trained models to models/ and metrics to results/metrics/.
8. Renders and saves all 14 analytical figures to results/figures/.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_processing import clean_zomato_data
from src.statistical_analysis import (
    compute_descriptive_stats,
    compute_correlations,
    run_all_hypothesis_tests
)
from src.modeling import (
    train_linear_regression,
    train_logistic_regression,
    train_kmeans_clustering
)

# Apply sleek modern plotting aesthetic
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#E2E8F0"
plt.rcParams["axes.linewidth"] = 0.8


def generate_all_figures(df, corr_data, reg_res, logit_res, km_res, tests_df):
    """
    Renders all 14 analytical figures required for the report and dashboard.
    """
    os.makedirs("results/figures", exist_ok=True)
    print("Generating and saving 14 publication-quality analytical figures...")

    # 1. Correlation Heatmap (Pearson & Spearman)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    features = corr_data["features"]
    labels = corr_data["labels"]
    
    p_df = pd.DataFrame(corr_data["pearson_corr"])
    s_df = pd.DataFrame(corr_data["spearman_corr"])
    p_df.columns = labels
    p_df.index = labels
    s_df.columns = labels
    s_df.index = labels

    sns.heatmap(p_df, annot=True, fmt=".2f", cmap="Blues", ax=axes[0], cbar_kws={"shrink": 0.8}, vmin=-0.2, vmax=1.0)
    axes[0].set_title("Pearson Correlation Matrix", fontsize=13, fontweight="bold", pad=12)

    sns.heatmap(s_df, annot=True, fmt=".2f", cmap="Purples", ax=axes[1], cbar_kws={"shrink": 0.8}, vmin=-0.2, vmax=1.0)
    axes[1].set_title("Spearman Rank Correlation Matrix", fontsize=13, fontweight="bold", pad=12)

    plt.tight_layout()
    plt.savefig("results/figures/correlation_heatmap.png", dpi=300)
    plt.close()

    # 2. Ratings Distribution & Highly Rated Cutoff
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["rate_num"], bins=25, kde=True, color="#3B82F6", ax=ax, edgecolor="white", alpha=0.7)
    ax.axvline(4.0, color="#EF4444", linestyle="--", linewidth=2, label="Highly Rated Cutoff (≥ 4.0)")
    ax.axvline(df["rate_num"].mean(), color="#10B981", linestyle=":", linewidth=2, label=f"Mean Rating ({df['rate_num'].mean():.2f})")
    ax.axvline(df["rate_num"].median(), color="#8B5CF6", linestyle="-.", linewidth=2, label=f"Median Rating ({df['rate_num'].median():.2f})")
    ax.set_title("Distribution of Restaurant Ratings (out of 5)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Customer Rating")
    ax.set_ylabel("Count of Restaurants")
    ax.legend(frameon=True, facecolor="white", framealpha=0.9)
    plt.tight_layout()
    plt.savefig("results/figures/ratings_distribution.png", dpi=300)
    plt.close()

    # 3. Cost & Votes Skewness vs Log Transformations
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    sns.histplot(df["cost_for_two"], bins=30, color="#F59E0B", ax=axes[0, 0], kde=True)
    axes[0, 0].set_title(f"Raw Cost for Two (Skewness: {df['cost_for_two'].skew():.2f})", fontweight="bold")
    axes[0, 0].set_xlabel("Cost for Two (INR)")

    sns.histplot(df["log_cost"], bins=30, color="#10B981", ax=axes[0, 1], kde=True)
    axes[0, 1].set_title(f"Log Transformed Cost (Skewness: {df['log_cost'].skew():.2f})", fontweight="bold")
    axes[0, 1].set_xlabel("Log(Cost + 1)")

    sns.histplot(df["votes"], bins=30, color="#EF4444", ax=axes[1, 0], kde=True)
    axes[1, 0].set_title(f"Raw Votes Count (Skewness: {df['votes'].skew():.2f})", fontweight="bold")
    axes[1, 0].set_xlabel("Number of Votes")

    sns.histplot(df["log_votes"], bins=30, color="#6366F1", ax=axes[1, 1], kde=True)
    axes[1, 1].set_title(f"Log Transformed Votes (Skewness: {df['log_votes'].skew():.2f})", fontweight="bold")
    axes[1, 1].set_xlabel("Log(Votes + 1)")

    plt.tight_layout()
    plt.savefig("results/figures/cost_votes_distribution.png", dpi=300)
    plt.close()

    # 4. Hypothesis 1 Boxplot: Online Order vs Rating
    fig, ax = plt.subplots(figsize=(7, 5))
    palette = {"No": "#94A3B8", "Yes": "#3B82F6"}
    sns.boxplot(x="online_order", y="rate_num", data=df, palette=palette, ax=ax, width=0.45, fliersize=2)
    ax.set_title("Hypothesis 1: Customer Rating by Online Ordering (Welch t-test)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Online Ordering Available")
    ax.set_ylabel("Rating (out of 5)")
    plt.tight_layout()
    plt.savefig("results/figures/hypothesis_online_order_boxplot.png", dpi=300)
    plt.close()

    # 5. Hypothesis 2 Boxplot: Table Booking vs Rating
    fig, ax = plt.subplots(figsize=(7, 5))
    palette_b = {"No": "#94A3B8", "Yes": "#10B981"}
    sns.boxplot(x="book_table", y="rate_num", data=df, palette=palette_b, ax=ax, width=0.45, fliersize=2)
    ax.set_title("Hypothesis 2: Customer Rating by Table Booking (Welch t-test)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Table Booking Available")
    ax.set_ylabel("Rating (out of 5)")
    plt.tight_layout()
    plt.savefig("results/figures/hypothesis_table_booking_boxplot.png", dpi=300)
    plt.close()

    # 6. Hypothesis 3 & 5: Listing Type Boxplots (Rating & Cost)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    sns.boxplot(x="listed_in_type", y="rate_num", data=df, ax=axes[0], palette="Blues_r", fliersize=2)
    axes[0].set_title("Hypothesis 3: Rating by Listing Type (ANOVA)", fontweight="bold")
    axes[0].set_xlabel("Listing Type")
    axes[0].set_ylabel("Rating")
    axes[0].tick_params(axis="x", rotation=30)

    sns.boxplot(x="listed_in_type", y="cost_for_two", data=df, ax=axes[1], palette="Oranges_r", fliersize=2)
    axes[1].set_title("Hypothesis 5: Approx Cost by Listing Type (ANOVA)", fontweight="bold")
    axes[1].set_xlabel("Listing Type")
    axes[1].set_ylabel("Cost for Two (INR)")
    axes[1].tick_params(axis="x", rotation=30)

    plt.tight_layout()
    plt.savefig("results/figures/hypothesis_listing_type_boxplot.png", dpi=300)
    plt.close()

    # 7. Hypothesis 4: Top 10 Locations vs Rating Boxplot
    fig, ax = plt.subplots(figsize=(12, 5.5))
    top_10 = df["location"].value_counts().head(10).index
    df_top_loc = df[df["location"].isin(top_10)]
    loc_order = df_top_loc.groupby("location")["rate_num"].median().sort_values(ascending=False).index
    sns.boxplot(x="location", y="rate_num", data=df_top_loc, order=loc_order, ax=ax, palette="mako", fliersize=2)
    ax.set_title("Hypothesis 4: Ratings across Top 10 Bangalore Dining Neighborhoods", fontsize=13, fontweight="bold")
    ax.set_xlabel("Neighborhood Location")
    ax.set_ylabel("Customer Rating")
    ax.tick_params(axis="x", rotation=35)
    plt.tight_layout()
    plt.savefig("results/figures/hypothesis_top_locations_boxplot.png", dpi=300)
    plt.close()

    # 8. Regression Residuals Diagnostic Plots
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    residuals = np.array(reg_res["residuals_sample"])
    fitted = np.array(reg_res["fitted_sample"])

    sns.scatterplot(x=fitted, y=residuals, ax=axes[0], color="#2563EB", alpha=0.5, s=25)
    axes[0].axhline(0, color="#EF4444", linestyle="--", linewidth=1.5)
    axes[0].set_title("Residuals vs. Fitted Values (Homoscedasticity Check)", fontweight="bold")
    axes[0].set_xlabel("Fitted Ratings (y_pred)")
    axes[0].set_ylabel("Residuals (e = y - y_pred)")

    sns.histplot(residuals, kde=True, ax=axes[1], color="#8B5CF6", bins=25, edgecolor="white")
    axes[1].axvline(0, color="#EF4444", linestyle="--", linewidth=1.5)
    axes[1].set_title(f"Residual Normality Distribution (Mean: {np.mean(residuals):.4f})", fontweight="bold")
    axes[1].set_xlabel("Residual Value")

    plt.tight_layout()
    plt.savefig("results/figures/regression_residuals.png", dpi=300)
    plt.close()

    # 9. Regression Coefficients Plot
    coef_df = pd.DataFrame(reg_res["coefficients"])
    coef_df = coef_df[coef_df["feature"] != "const"].sort_values(by="coefficient", ascending=True)
    
    fig, ax = plt.subplots(figsize=(9, 6.5))
    colors = ["#10B981" if c > 0 else "#EF4444" for c in coef_df["coefficient"]]
    ax.barh(coef_df["feature"], coef_df["coefficient"], color=colors, alpha=0.85)
    ax.axvline(0, color="#475569", linestyle="-", linewidth=0.8)
    ax.set_title("Multiple Linear Regression: Feature Coefficients (OLS)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Coefficient Impact on Restaurant Rating")
    plt.tight_layout()
    plt.savefig("results/figures/regression_coefficients.png", dpi=300)
    plt.close()

    # 10. Logistic Regression ROC Curve
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fpr = np.array(logit_res["fpr"])
    tpr = np.array(logit_res["tpr"])
    roc_auc = logit_res["metrics"]["roc_auc"]
    
    ax.plot(fpr, tpr, color="#2563EB", lw=2.5, label=f"Logistic Model (AUC = {roc_auc:.3f})")
    ax.plot([0, 1], [0, 1], color="#94A3B8", lw=1.5, linestyle="--", label="Random Chance / Majority Baseline (AUC = 0.500)")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate (1 - Specificity)")
    ax.set_ylabel("True Positive Rate (Sensitivity / Recall)")
    ax.set_title("ROC Curve: Predicting Highly Rated Restaurants (≥ 4.0)", fontsize=12, fontweight="bold")
    ax.legend(loc="lower right", frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig("results/figures/logistic_roc_curve.png", dpi=300)
    plt.close()

    # 11. Logistic Regression Confusion Matrix Heatmap
    fig, ax = plt.subplots(figsize=(6, 5))
    cm = np.array(logit_res["metrics"]["confusion_matrix"])
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    
    annot = np.array([[f"{count}\n({pct:.1%})" for count, pct in zip(row_c, row_p)] for row_c, row_p in zip(cm, cm_norm)])
    sns.heatmap(cm, annot=annot, fmt="", cmap="Blues", ax=ax, cbar=False,
                xticklabels=["Low/Mid (< 4.0)", "Highly Rated (≥ 4.0)"],
                yticklabels=["Low/Mid (< 4.0)", "Highly Rated (≥ 4.0)"])
    ax.set_title("Logistic Regression Confusion Matrix", fontsize=12, fontweight="bold")
    ax.set_xlabel("Predicted Class")
    ax.set_ylabel("Actual Class")
    plt.tight_layout()
    plt.savefig("results/figures/logistic_confusion_matrix.png", dpi=300)
    plt.close()

    # 12. Logistic Regression Odds Ratios Plot
    or_df = pd.DataFrame(logit_res["odds_ratios"])
    or_df = or_df[or_df["feature"] != "const"].sort_values(by="odds_ratio", ascending=True)
    
    fig, ax = plt.subplots(figsize=(9, 6.5))
    y_pos = range(len(or_df))
    ax.errorbar(
        or_df["odds_ratio"], y_pos,
        xerr=[or_df["odds_ratio"] - or_df["ci_lower"], or_df["ci_upper"] - or_df["odds_ratio"]],
        fmt='o', color='#2563EB', ecolor='#93C5FD', elinewidth=2, capsize=4, markersize=6
    )
    ax.axvline(1.0, color="#EF4444", linestyle="--", linewidth=1.5, label="Neutral Odds (OR = 1.0)")
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(or_df["feature"])
    ax.set_xlabel("Odds Ratio (OR) with 95% Confidence Interval")
    ax.set_title("Logistic Regression: Predictor Odds Ratios for High Rating", fontsize=12, fontweight="bold")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("results/figures/logistic_odds_ratios.png", dpi=300)
    plt.close()

    # 13. K-Means Elbow & Silhouette Plots
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    k_range = km_res["k_range"]
    inertias = km_res["inertias"]
    silhouettes = km_res["silhouettes"]

    axes[0].plot(k_range, inertias, marker="o", color="#2563EB", lw=2, markersize=7)
    axes[0].axvline(3, color="#EF4444", linestyle="--", label="Selected Optimal k=3")
    axes[0].set_title("Elbow Method: Within-Cluster Inertia vs. k", fontweight="bold")
    axes[0].set_xlabel("Number of Clusters (k)")
    axes[0].set_ylabel("Inertia (Sum of Squared Distances)")
    axes[0].legend()

    axes[1].plot(k_range, silhouettes, marker="s", color="#10B981", lw=2, markersize=7)
    axes[1].axvline(3, color="#EF4444", linestyle="--", label="Selected Optimal k=3")
    axes[1].set_title("Silhouette Score vs. k", fontweight="bold")
    axes[1].set_xlabel("Number of Clusters (k)")
    axes[1].set_ylabel("Mean Silhouette Coefficient")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig("results/figures/kmeans_elbow_silhouette.png", dpi=300)
    plt.close()

    # 14. K-Means Clusters Scatter (Cost vs Rating by Segment)
    fig, ax = plt.subplots(figsize=(9, 6))
    seg_palette = {"Budget": "#10B981", "Mid-range": "#3B82F6", "Premium": "#8B5CF6"}
    sns.scatterplot(
        x="cost_for_two", y="rate_num", hue="segment", size="votes",
        sizes=(20, 300), data=df, palette=seg_palette, alpha=0.65, ax=ax
    )
    ax.set_title("Restaurant Segments (K-Means k=3): Budget, Mid-range & Premium", fontsize=13, fontweight="bold")
    ax.set_xlabel("Approx Cost for Two (INR)")
    ax.set_ylabel("Customer Rating (out of 5)")
    ax.legend(title="Segment", frameon=True, facecolor="white", loc="lower right")
    plt.tight_layout()
    plt.savefig("results/figures/kmeans_clusters_scatter.png", dpi=300)
    plt.close()

    print("All 14 figures generated and saved successfully!")


def run_pipeline():
    print("=" * 70)
    print("BANGALORE RESTAURANT RECOMMENDATION & ANALYTICS PIPELINE")
    print("=" * 70)

    # 1. Clean data and feature engineering
    df, cleaning_log = clean_zomato_data(
        raw_csv_path="Dataset/zomato.csv",
        output_clean_path="Dataset/cleaned_zomato.csv"
    )

    # 2. Descriptive statistics
    print("\nComputing descriptive statistics...")
    desc_df = compute_descriptive_stats(df)
    desc_df.to_json("results/metrics/descriptive_stats.json", orient="records", indent=4)
    print(desc_df[["display_name", "mean", "median", "std", "skewness", "kurtosis", "cv_percent"]])

    # 3. Correlations
    print("\nComputing Pearson and Spearman correlations...")
    corr_data = compute_correlations(df)
    with open("results/metrics/correlation_matrix.json", "w") as f:
        json.dump(corr_data, f, indent=4)

    # 4. Hypothesis tests
    print("\nExecuting 9 formal hypothesis tests...")
    tests_df = run_all_hypothesis_tests(df)
    tests_df.to_json("results/metrics/hypothesis_tests.json", orient="records", indent=4)
    for _, row in tests_df.iterrows():
        print(f"Test #{row['test_id']}: {row['test_name']} -> {row['statistic_type']}={row['statistic_val']}, p={row['p_value']:.4e}, {row['effect_size_metric']}={row['effect_size_val']} [{row['decision']}]")

    # 5. Multiple Linear Regression
    print("\nTraining Multiple Linear Regression (OLS)...")
    _, _, reg_res = train_linear_regression(df)
    with open("results/metrics/linear_regression_results.json", "w") as f:
        json.dump(reg_res, f, indent=4)
    print("Linear Regression Metrics:", reg_res["metrics"])

    # 6. Logistic Regression
    print("\nTraining Logistic Regression (High Rating Prediction)...")
    _, _, logit_res = train_logistic_regression(df)
    with open("results/metrics/logistic_regression_results.json", "w") as f:
        json.dump(logit_res, f, indent=4)
    print("Logistic Regression Metrics:", logit_res["metrics"])

    # 7. K-Means Clustering
    print("\nTraining K-Means Clustering (k=3)...")
    _, _, df_clustered, km_res = train_kmeans_clustering(df)
    with open("results/metrics/cluster_profiles.json", "w") as f:
        json.dump(km_res, f, indent=4)
    
    # Save the clustered dataframe back with the 'segment' column for instant app use
    df_clustered.to_csv("Dataset/cleaned_zomato.csv", index=False)
    print("Updated Dataset/cleaned_zomato.csv with segment labels.")

    # 8. Generate all figures
    generate_all_figures(df_clustered, corr_data, reg_res, logit_res, km_res, tests_df)

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY! All models, metrics, and charts saved.")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
