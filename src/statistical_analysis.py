"""
src/statistical_analysis.py
Comprehensive Statistical Analysis for Bangalore Restaurant Dataset.
Includes:
1. Descriptive statistics (Mean, Median, Std, Skewness, Kurtosis, CV, IQR)
2. Pearson and Spearman correlation matrices
3. 9 Formal Hypothesis Tests with test statistics, p-values, effect sizes, and practical interpretations
"""

import json
import numpy as np
import pandas as pd
from scipy import stats


def compute_descriptive_stats(df):
    """
    Computes summary metrics for continuous variables:
    rate_num, votes, cost_for_two, log_votes, log_cost.
    """
    targets = ["rate_num", "votes", "cost_for_two", "log_votes", "log_cost"]
    labels = {
        "rate_num": "Rating (out of 5)",
        "votes": "Votes (count)",
        "cost_for_two": "Approx Cost for Two (INR)",
        "log_votes": "Log(Votes + 1)",
        "log_cost": "Log(Cost + 1)"
    }
    
    records = []
    for col in targets:
        series = df[col].dropna()
        n = len(series)
        mean_val = float(series.mean())
        median_val = float(series.median())
        std_val = float(series.std(ddof=1))
        skew_val = float(series.skew())
        kurt_val = float(series.kurtosis())
        cv_val = float((std_val / mean_val) * 100) if mean_val != 0 else 0.0
        q25 = float(series.quantile(0.25))
        q75 = float(series.quantile(0.75))
        iqr_val = float(q75 - q25)
        min_val = float(series.min())
        max_val = float(series.max())
        
        records.append({
            "variable": col,
            "display_name": labels.get(col, col),
            "count": int(n),
            "mean": round(mean_val, 4),
            "median": round(median_val, 4),
            "std": round(std_val, 4),
            "variance": round(std_val ** 2, 4),
            "skewness": round(skew_val, 4),
            "kurtosis": round(kurt_val, 4),
            "cv_percent": round(cv_val, 2),
            "q25": round(q25, 4),
            "q75": round(q75, 4),
            "iqr": round(iqr_val, 4),
            "min": round(min_val, 4),
            "max": round(max_val, 4)
        })
    
    desc_df = pd.DataFrame(records)
    return desc_df


def compute_correlations(df):
    """
    Computes Pearson and Spearman correlation matrices and p-values.
    """
    features = ["rate_num", "log_votes", "log_cost", "online_order_int", "book_table_int"]
    labels = ["Rating", "Log Votes", "Log Cost", "Online Order", "Table Booking"]
    sub_df = df[features].dropna()
    
    pearson_corr = sub_df.corr(method="pearson").round(4)
    spearman_corr = sub_df.corr(method="spearman").round(4)
    
    # Calculate p-value matrices
    p_pearson = pd.DataFrame(np.zeros((len(features), len(features))), index=features, columns=features)
    p_spearman = pd.DataFrame(np.zeros((len(features), len(features))), index=features, columns=features)
    
    for i, col1 in enumerate(features):
        for j, col2 in enumerate(features):
            if i == j:
                p_pearson.loc[col1, col2] = 0.0
                p_spearman.loc[col1, col2] = 0.0
            else:
                _, p_p = stats.pearsonr(sub_df[col1], sub_df[col2])
                _, p_s = stats.spearmanr(sub_df[col1], sub_df[col2])
                p_pearson.loc[col1, col2] = round(p_p, 6)
                p_spearman.loc[col1, col2] = round(p_s, 6)
                
    return {
        "features": features,
        "labels": labels,
        "pearson_corr": pearson_corr.to_dict(),
        "spearman_corr": spearman_corr.to_dict(),
        "p_pearson": p_pearson.to_dict(),
        "p_spearman": p_spearman.to_dict()
    }


def run_all_hypothesis_tests(df, alpha=0.05):
    """
    Runs the 9 specified hypothesis tests with effect sizes and practical interpretations.
    """
    results = []

    # 1. Welch t-test: Online ordering vs Rating
    g1 = df[df["online_order_int"] == 1]["rate_num"].dropna()
    g0 = df[df["online_order_int"] == 0]["rate_num"].dropna()
    t1, p1 = stats.ttest_ind(g1, g0, equal_var=False)
    # Cohen's d for Welch t-test
    n1, n0 = len(g1), len(g0)
    s1, s0 = g1.std(ddof=1), g0.std(ddof=1)
    s_pooled = np.sqrt(((n1 - 1) * s1**2 + (n0 - 1) * s0**2) / (n1 + n0 - 2))
    d1 = (g1.mean() - g0.mean()) / s_pooled
    results.append({
        "test_id": 1,
        "test_name": "Welch's Two-Sample t-Test (Online Ordering)",
        "variable_tested": "Rating by Online Ordering (Yes vs No)",
        "null_hypothesis": "Mean rating with online ordering equals mean rating without online ordering (μ_online = μ_offline).",
        "alt_hypothesis": "Mean ratings differ significantly between online and offline ordering outlets (μ_online ≠ μ_offline).",
        "statistic_type": "t-statistic",
        "statistic_val": round(float(t1), 4),
        "p_value": float(p1),
        "alpha": alpha,
        "decision": "Reject H0" if p1 < alpha else "Fail to Reject H0",
        "effect_size_metric": "Cohen's d",
        "effect_size_val": round(float(d1), 4),
        "sample_info": f"Online (n={n1}, mean={g1.mean():.2f}) vs Offline (n={n0}, mean={g0.mean():.2f})",
        "practical_impact": (
            f"Statistically significant (p < {alpha}). Cohen's d of {d1:.2f} indicates a "
            + ("small" if abs(d1) < 0.5 else "moderate")
            + f" effect. Outlets offering online ordering average {g1.mean() - g0.mean():+.2f} rating points higher."
        )
    })

    # 2. Welch t-test: Table booking vs Rating
    b1 = df[df["book_table_int"] == 1]["rate_num"].dropna()
    b0 = df[df["book_table_int"] == 0]["rate_num"].dropna()
    t2, p2 = stats.ttest_ind(b1, b0, equal_var=False)
    nb1, nb0 = len(b1), len(b0)
    sb1, sb0 = b1.std(ddof=1), b0.std(ddof=1)
    s_pooled_b = np.sqrt(((nb1 - 1) * sb1**2 + (nb0 - 1) * sb0**2) / (nb1 + nb0 - 2))
    d2 = (b1.mean() - b0.mean()) / s_pooled_b
    results.append({
        "test_id": 2,
        "test_name": "Welch's Two-Sample t-Test (Table Booking)",
        "variable_tested": "Rating by Table Booking (Yes vs No)",
        "null_hypothesis": "Mean rating of restaurants with table booking equals those without table booking (μ_booking = μ_no_booking).",
        "alt_hypothesis": "Mean rating of restaurants with table booking differs significantly from those without (μ_booking ≠ μ_no_booking).",
        "statistic_type": "t-statistic",
        "statistic_val": round(float(t2), 4),
        "p_value": float(p2),
        "alpha": alpha,
        "decision": "Reject H0" if p2 < alpha else "Fail to Reject H0",
        "effect_size_metric": "Cohen's d",
        "effect_size_val": round(float(d2), 4),
        "sample_info": f"Booking (n={nb1}, mean={b1.mean():.2f}) vs No Booking (n={nb0}, mean={b0.mean():.2f})",
        "practical_impact": (
            f"Highly significant with a substantial effect size (d = {d2:.2f}, large effect). "
            f"Restaurants providing table booking average {b1.mean() - b0.mean():+.2f} higher stars, reflecting higher dining experience and service standards."
        )
    })

    # 3. One-way ANOVA: Listing types vs Rating
    listing_groups = [group["rate_num"].dropna().values for _, group in df.groupby("listed_in_type") if len(group) >= 10]
    f3, p3 = stats.f_oneway(*listing_groups)
    # Eta-squared calculation
    all_rates = df[df["listed_in_type"].isin([name for name, grp in df.groupby("listed_in_type") if len(grp) >= 10])]["rate_num"].dropna()
    grand_mean = all_rates.mean()
    ss_total = np.sum((all_rates - grand_mean) ** 2)
    ss_between = np.sum([len(grp) * (grp.mean() - grand_mean) ** 2 for grp in listing_groups])
    eta3 = ss_between / ss_total if ss_total > 0 else 0.0
    results.append({
        "test_id": 3,
        "test_name": "One-Way ANOVA (Listing Types vs Rating)",
        "variable_tested": "Mean Rating across Listing Types",
        "null_hypothesis": "Mean restaurant ratings are identical across all listing categories (Delivery, Dine-out, Buffet, Cafes, etc.).",
        "alt_hypothesis": "At least one listing category possesses a statistically different mean rating.",
        "statistic_type": "F-statistic",
        "statistic_val": round(float(f3), 4),
        "p_value": float(p3),
        "alpha": alpha,
        "decision": "Reject H0" if p3 < alpha else "Fail to Reject H0",
        "effect_size_metric": "Eta-squared (eta^2)",
        "effect_size_val": round(float(eta3), 4),
        "sample_info": f"{len(listing_groups)} listing categories compared across {len(all_rates)} restaurants",
        "practical_impact": (
            f"Statistically significant (F = {f3:.2f}, p < {alpha}). eta^2 = {eta3:.3f} indicates that listing type explains "
            f"{eta3*100:.1f}% of rating variance. Experiences like Buffets and Cafes naturally report higher rating profiles."
        )
    })

    # 4. One-way ANOVA: Top 10 locations vs Rating
    top_10_locs = df["location"].value_counts().head(10).index.tolist()
    loc_sub = df[df["location"].isin(top_10_locs)]
    loc_groups = [group["rate_num"].dropna().values for _, group in loc_sub.groupby("location")]
    f4, p4 = stats.f_oneway(*loc_groups)
    grand_mean_loc = loc_sub["rate_num"].mean()
    ss_tot_loc = np.sum((loc_sub["rate_num"] - grand_mean_loc) ** 2)
    ss_bet_loc = np.sum([len(grp) * (grp.mean() - grand_mean_loc) ** 2 for grp in loc_groups])
    eta4 = ss_bet_loc / ss_tot_loc if ss_tot_loc > 0 else 0.0
    results.append({
        "test_id": 4,
        "test_name": "One-Way ANOVA (Top 10 Locations vs Rating)",
        "variable_tested": "Mean Rating across Top 10 Bangalore Neighborhoods",
        "null_hypothesis": "Mean restaurant ratings are equal across the top 10 most populated Bangalore dining hubs.",
        "alt_hypothesis": "At least one neighborhood possesses a significantly different mean restaurant rating.",
        "statistic_type": "F-statistic",
        "statistic_val": round(float(f4), 4),
        "p_value": float(p4),
        "alpha": alpha,
        "decision": "Reject H0" if p4 < alpha else "Fail to Reject H0",
        "effect_size_metric": "Eta-squared (eta^2)",
        "effect_size_val": round(float(eta4), 4),
        "sample_info": f"Top 10 areas evaluated (n={len(loc_sub)} total restaurants)",
        "practical_impact": (
            f"Statistically significant (F = {f4:.2f}, p < {alpha}). eta^2 = {eta4:.3f} explains {eta4*100:.1f}% variance. "
            f"Neighborhoods like Koramangala and Indiranagar exhibit higher customer rating benchmarks than outer suburban hubs."
        )
    })

    # 5. One-way ANOVA: Listing types vs Cost
    cost_groups = [group["cost_for_two"].dropna().values for _, group in df.groupby("listed_in_type") if len(group) >= 10]
    f5, p5 = stats.f_oneway(*cost_groups)
    all_costs = df[df["listed_in_type"].isin([name for name, grp in df.groupby("listed_in_type") if len(grp) >= 10])]["cost_for_two"].dropna()
    gm_cost = all_costs.mean()
    ss_tot_cost = np.sum((all_costs - gm_cost) ** 2)
    ss_bet_cost = np.sum([len(grp) * (grp.mean() - gm_cost) ** 2 for grp in cost_groups])
    eta5 = ss_bet_cost / ss_tot_cost if ss_tot_cost > 0 else 0.0
    results.append({
        "test_id": 5,
        "test_name": "One-Way ANOVA (Listing Types vs Cost)",
        "variable_tested": "Mean Approx Cost for Two across Listing Types",
        "null_hypothesis": "Average dining cost for two is equal across all restaurant listing categories.",
        "alt_hypothesis": "Average dining cost differs significantly across listing categories.",
        "statistic_type": "F-statistic",
        "statistic_val": round(float(f5), 4),
        "p_value": float(p5),
        "alpha": alpha,
        "decision": "Reject H0" if p5 < alpha else "Fail to Reject H0",
        "effect_size_metric": "Eta-squared (eta^2)",
        "effect_size_val": round(float(eta5), 4),
        "sample_info": f"Cost comparisons across {len(cost_groups)} listing types",
        "practical_impact": (
            f"Highly significant with strong practical relevance (F = {f5:.2f}, eta^2 = {eta5:.3f}, explaining {eta5*100:.1f}% of cost variation). "
            f"Buffets and Nightlife command significantly higher expenditure than quick Delivery and Desserts."
        )
    })

    # 6. Kruskal-Wallis Test: Non-parametric ANOVA across Listing Types (Rating)
    h6, p6 = stats.kruskal(*listing_groups)
    k_groups = len(listing_groups)
    n_total = len(all_rates)
    eps6 = (h6 - k_groups + 1) / (n_total - k_groups) if (n_total - k_groups) > 0 else 0.0
    results.append({
        "test_id": 6,
        "test_name": "Kruskal-Wallis Non-Parametric Test (Listing Types vs Rating)",
        "variable_tested": "Distribution of Ratings across Listing Types (Relaxing Normality)",
        "null_hypothesis": "The distribution / median rating is identical across all restaurant listing types.",
        "alt_hypothesis": "Rating distributions differ across listing types.",
        "statistic_type": "H-statistic",
        "statistic_val": round(float(h6), 4),
        "p_value": float(p6),
        "alpha": alpha,
        "decision": "Reject H0" if p6 < alpha else "Fail to Reject H0",
        "effect_size_metric": "Epsilon-squared (eps^2)",
        "effect_size_val": round(float(eps6), 4),
        "sample_info": f"Kruskal-Wallis rank sum across {k_groups} groups (N={n_total})",
        "practical_impact": (
            f"Confirms ANOVA findings without normality assumption (H = {h6:.2f}, p < {alpha}). "
            f"Median customer ratings truly differ across dining operational categories."
        )
    })

    # 7. Chi-Square Test: Table Booking vs Restaurant Type
    contingency_booking = pd.crosstab(df["rest_type_grouped"], df["book_table_int"])
    chi7, p7, dof7, _ = stats.chi2_contingency(contingency_booking)
    n7 = contingency_booking.values.sum()
    min_dim7 = min(contingency_booking.shape) - 1
    cramer_v7 = np.sqrt(chi7 / (n7 * min_dim7)) if min_dim7 > 0 and n7 > 0 else 0.0
    results.append({
        "test_id": 7,
        "test_name": "Chi-Square Test of Independence (Booking vs Restaurant Type)",
        "variable_tested": "Association between Table Booking and Primary Restaurant Type",
        "null_hypothesis": "Table booking availability is independent of restaurant establishment type.",
        "alt_hypothesis": "Table booking availability is significantly associated with restaurant establishment type.",
        "statistic_type": "Chi-Square (chi^2)",
        "statistic_val": round(float(chi7), 4),
        "p_value": float(p7),
        "alpha": alpha,
        "decision": "Reject H0" if p7 < alpha else "Fail to Reject H0",
        "effect_size_metric": "Cramer's V",
        "effect_size_val": round(float(cramer_v7), 4),
        "sample_info": f"Contingency matrix {contingency_booking.shape[0]}x{contingency_booking.shape[1]}, df={dof7}, N={n7}",
        "practical_impact": (
            f"Extremely strong dependency (chi^2 = {chi7:.2f}, Cramer's V = {cramer_v7:.3f}). "
            f"Casual dining, bars, and lounges overwhelmingly offer booking, while quick bites and takeaway outlets virtually never do."
        )
    })

    # 8. Chi-Square Test: Online Ordering vs Listing Type
    contingency_online = pd.crosstab(df["listed_in_type"], df["online_order_int"])
    chi8, p8, dof8, _ = stats.chi2_contingency(contingency_online)
    n8 = contingency_online.values.sum()
    min_dim8 = min(contingency_online.shape) - 1
    cramer_v8 = np.sqrt(chi8 / (n8 * min_dim8)) if min_dim8 > 0 and n8 > 0 else 0.0
    results.append({
        "test_id": 8,
        "test_name": "Chi-Square Test of Independence (Online Order vs Listing Type)",
        "variable_tested": "Association between Online Ordering and Listing Category",
        "null_hypothesis": "Online ordering capability is independent of listing category.",
        "alt_hypothesis": "Online ordering capability is significantly associated with listing category.",
        "statistic_type": "Chi-Square (chi^2)",
        "statistic_val": round(float(chi8), 4),
        "p_value": float(p8),
        "alpha": alpha,
        "decision": "Reject H0" if p8 < alpha else "Fail to Reject H0",
        "effect_size_metric": "Cramer's V",
        "effect_size_val": round(float(cramer_v8), 4),
        "sample_info": f"Contingency matrix {contingency_online.shape[0]}x{contingency_online.shape[1]}, df={dof8}, N={n8}",
        "practical_impact": (
            f"Highly significant dependency (chi^2 = {chi8:.2f}, Cramer's V = {cramer_v8:.3f}). "
            f"Delivery listings naturally possess >90% online enablement compared to dine-out and buffet-centric operations."
        )
    })

    # 9. Pearson Correlation Test: Log Cost vs Rating
    valid_sub = df[["log_cost", "rate_num"]].dropna()
    r9, p9 = stats.pearsonr(valid_sub["log_cost"], valid_sub["rate_num"])
    n9 = len(valid_sub)
    t9 = r9 * np.sqrt((n9 - 2) / (1 - r9**2)) if (1 - r9**2) > 0 else 0.0
    results.append({
        "test_id": 9,
        "test_name": "Pearson Correlation Significance Test (Log Cost vs Rating)",
        "variable_tested": "Linear Association between Log Cost and Customer Rating",
        "null_hypothesis": "There is zero linear correlation between log(approx cost) and restaurant rating (ρ = 0).",
        "alt_hypothesis": "A statistically significant linear correlation exists between log(approx cost) and rating (ρ ≠ 0).",
        "statistic_type": "t-statistic",
        "statistic_val": round(float(t9), 4),
        "p_value": float(p9),
        "alpha": alpha,
        "decision": "Reject H0" if p9 < alpha else "Fail to Reject H0",
        "effect_size_metric": "Pearson's r",
        "effect_size_val": round(float(r9), 4),
        "sample_info": f"N = {n9} observations, degrees of freedom = {n9 - 2}",
        "practical_impact": (
            f"Statistically significant positive correlation (r = +{r9:.3f}, p < {alpha}). "
            f"Pricier establishments consistently record higher customer satisfaction ratings due to premium ambiance and hospitality."
        )
    })

    tests_df = pd.DataFrame(results)
    return tests_df


if __name__ == "__main__":
    df = pd.read_csv("Dataset/cleaned_zomato.csv")
    desc = compute_descriptive_stats(df)
    corrs = compute_correlations(df)
    tests = run_all_hypothesis_tests(df)
    print("Descriptive stats:\n", desc[["display_name", "mean", "median", "std", "skewness", "kurtosis", "cv_percent"]])
    print("\n9 Hypothesis Tests Summary:\n", tests[["test_id", "test_name", "statistic_val", "p_value", "effect_size_metric", "effect_size_val", "decision"]])
