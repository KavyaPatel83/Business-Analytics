"""
src/modeling.py
Machine Learning and Statistical Modeling Module.
Contains:
1. Multiple Linear Regression (OLS with statsmodels & scikit-learn, VIF diagnostics, residual checks)
2. Logistic Regression (High rating prediction, Odds ratios with CIs, ROC-AUC, Confusion Matrix, Majority Baseline)
3. K-Means Clustering (Elbow/Silhouette analysis, 3 Segments: Budget, Mid-range, Premium, Profile tables)
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    silhouette_score
)
from sklearn.cluster import KMeans
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan


def prepare_regression_features(df):
    """
    Constructs feature matrix X and target y for linear and logistic regression.
    Uses log_votes, log_cost, online_order_int, book_table_int, plus dummy variables
    for listed_in_type and rest_type_grouped.
    """
    base_num = ["log_votes", "log_cost", "online_order_int", "book_table_int"]
    
    # Categorical dummies (drop first category to prevent dummy variable trap / exact collinearity)
    df_listing_dummies = pd.get_dummies(df["listed_in_type"], prefix="list", drop_first=True, dtype=float)
    df_rest_dummies = pd.get_dummies(df["rest_type_grouped"], prefix="rest", drop_first=True, dtype=float)
    
    X = pd.concat([df[base_num].reset_index(drop=True), df_listing_dummies.reset_index(drop=True), df_rest_dummies.reset_index(drop=True)], axis=1)
    y_reg = df["rate_num"].reset_index(drop=True)
    y_clf = df["highly_rated"].reset_index(drop=True)
    
    return X, y_reg, y_clf


def compute_vif(X):
    """
    Calculates Variance Inflation Factor (VIF) for all predictor variables.
    """
    X_const = sm.add_constant(X)
    vif_data = []
    for i in range(1, X_const.shape[1]): # Skip constant for report
        col = X_const.columns[i]
        try:
            val = variance_inflation_factor(X_const.values, i)
        except Exception:
            val = np.nan
        vif_data.append({
            "feature": col,
            "vif": round(float(val), 2),
            "status": "Safe (< 5)" if val < 5 else ("Moderate (5-10)" if val < 10 else "High Collinearity (> 10)")
        })
    return pd.DataFrame(vif_data)


def train_linear_regression(df, test_size=0.20, random_state=42):
    """
    Trains Multiple Linear Regression model with 80/20 train/test split.
    Reports:
    - Train & Test R², Adjusted R², F-statistic, RMSE, MAE
    - Coefficients, Std Errors, t-statistics, p-values, 95% Confidence Intervals
    - VIF Multicollinearity table
    - Residual diagnostics (Normality, Heteroscedasticity)
    """
    X, y, _ = prepare_regression_features(df)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # 1. Statsmodels OLS for econometric inferences
    X_train_sm = sm.add_constant(X_train)
    X_test_sm = sm.add_constant(X_test)
    
    ols_model = sm.OLS(y_train, X_train_sm).fit()
    y_pred_train_sm = ols_model.predict(X_train_sm)
    y_pred_test_sm = ols_model.predict(X_test_sm)
    
    # 2. Sklearn model for export
    sk_lr = LinearRegression()
    sk_lr.fit(X_train, y_train)
    
    # Evaluation Metrics
    train_r2 = float(r2_score(y_train, y_pred_train_sm))
    test_r2 = float(r2_score(y_test, y_pred_test_sm))
    train_rmse = float(np.sqrt(mean_squared_error(y_train, y_pred_train_sm)))
    test_rmse = float(np.sqrt(mean_squared_error(y_test, y_pred_test_sm)))
    train_mae = float(mean_absolute_error(y_train, y_pred_train_sm))
    test_mae = float(mean_absolute_error(y_test, y_pred_test_sm))
    
    # Coefficient table
    coef_df = pd.DataFrame({
        "feature": ols_model.params.index,
        "coefficient": ols_model.params.values.round(4),
        "std_error": ols_model.bse.values.round(4),
        "t_statistic": ols_model.tvalues.values.round(4),
        "p_value": ols_model.pvalues.values.round(6),
        "ci_lower": ols_model.conf_int()[0].values.round(4),
        "ci_upper": ols_model.conf_int()[1].values.round(4)
    })
    
    # VIF table
    vif_df = compute_vif(X_train)
    
    # Residual diagnostics
    residuals_train = ols_model.resid
    res_mean = float(np.mean(residuals_train))
    res_std = float(np.std(residuals_train))
    
    # Heteroscedasticity test (Breusch-Pagan)
    try:
        bp_stat, bp_pval, _, _ = het_breuschpagan(residuals_train, X_train_sm)
    except Exception:
        bp_stat, bp_pval = np.nan, np.nan
        
    metrics = {
        "train_r2": round(train_r2, 4),
        "adj_r2": round(float(ols_model.rsquared_adj), 4),
        "test_r2": round(test_r2, 4),
        "train_rmse": round(train_rmse, 4),
        "test_rmse": round(test_rmse, 4),
        "train_mae": round(train_mae, 4),
        "test_mae": round(test_mae, 4),
        "f_statistic": round(float(ols_model.fvalue), 2),
        "f_pvalue": float(ols_model.f_pvalue),
        "degrees_of_freedom": int(ols_model.df_resid),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "bp_hetero_stat": round(float(bp_stat), 2) if not np.isnan(bp_stat) else None,
        "bp_hetero_pvalue": float(bp_pval) if not np.isnan(bp_pval) else None,
        "residual_mean": round(res_mean, 6),
        "residual_std": round(res_std, 4)
    }
    
    # Save model and metadata
    os.makedirs("models", exist_ok=True)
    joblib.dump(sk_lr, "models/linear_regression_model.joblib")
    
    result = {
        "metrics": metrics,
        "coefficients": coef_df.to_dict(orient="records"),
        "vif": vif_df.to_dict(orient="records"),
        "feature_names": list(X.columns),
        "residuals_sample": residuals_train.sample(min(500, len(residuals_train)), random_state=42).tolist(),
        "fitted_sample": y_pred_train_sm.sample(min(500, len(y_pred_train_sm)), random_state=42).tolist(),
        "y_test": y_test.tolist(),
        "y_pred_test": y_pred_test_sm.tolist()
    }
    
    return sk_lr, ols_model, result


def train_logistic_regression(df, test_size=0.20, random_state=42):
    """
    Trains Logistic Regression predicting if a restaurant is 'highly rated' (rate >= 4.0).
    Reports:
    - Accuracy, ROC-AUC, Pseudo R² (McFadden's), Confusion Matrix, Precision, Recall, F1
    - Comparison with Majority-Class Baseline
    - Odds Ratios with 95% Confidence Intervals
    """
    X, _, y = prepare_regression_features(df)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Baseline: Majority class
    majority_class = int(y_train.mode()[0])
    majority_baseline_acc = float((y_test == majority_class).mean())
    
    # Scale continuous columns for numerical stability in logistic regression
    num_cols = ["log_votes", "log_cost"]
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])
    
    # 1. Statsmodels Logit for Odds Ratios and Pseudo R2
    X_train_sm = sm.add_constant(X_train)
    logit_model = sm.Logit(y_train, X_train_sm).fit(disp=False, maxiter=200)
    
    pseudo_r2 = float(logit_model.prsquared)
    
    # Odds ratios and 95% CI
    params = logit_model.params
    conf = logit_model.conf_int()
    ci_low_clipped = np.clip(conf[0].values, -30, 30)
    ci_up_clipped = np.clip(conf[1].values, -30, 30)
    params_clipped = np.clip(params.values, -30, 30)
    
    odds_ratios = pd.DataFrame({
        "feature": params.index,
        "coefficient": params.values.round(4),
        "odds_ratio": np.exp(params_clipped).round(4),
        "p_value": logit_model.pvalues.values.round(6),
        "ci_lower": np.exp(ci_low_clipped).round(4),
        "ci_upper": np.exp(ci_up_clipped).round(4)
    })
    
    # 2. Sklearn LogisticRegression for classification performance
    clf = LogisticRegression(max_iter=1000, random_state=random_state)
    clf.fit(X_train, y_train)
    
    y_pred_test = clf.predict(X_test)
    y_pred_proba_test = clf.predict_proba(X_test)[:, 1]
    
    acc = float(accuracy_score(y_test, y_pred_test))
    prec = float(precision_score(y_test, y_pred_test, zero_division=0))
    rec = float(recall_score(y_test, y_pred_test, zero_division=0))
    f1 = float(f1_score(y_test, y_pred_test, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_pred_proba_test))
    cm = confusion_matrix(y_test, y_pred_test).tolist()
    
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba_test)
    
    metrics = {
        "accuracy": round(acc, 4),
        "majority_baseline_accuracy": round(majority_baseline_acc, 4),
        "accuracy_lift_over_baseline": round(acc - majority_baseline_acc, 4),
        "roc_auc": round(roc_auc, 4),
        "pseudo_r2_mcfadden": round(pseudo_r2, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "highly_rated_prevalence": round(float(y.mean()), 4)
    }
    
    # Save model
    joblib.dump(clf, "models/logistic_regression_model.joblib")
    
    result = {
        "metrics": metrics,
        "odds_ratios": odds_ratios.to_dict(orient="records"),
        "fpr": fpr.tolist(),
        "tpr": tpr.tolist(),
        "y_test": y_test.tolist(),
        "y_pred_proba_test": y_pred_proba_test.tolist()
    }
    
    return clf, logit_model, result


def train_kmeans_clustering(df, random_state=42):
    """
    Segments restaurants into Budget, Mid-range, and Premium using K-Means (k=3).
    Evaluates inertia (Elbow) and Silhouette scores for k in [2, 8].
    Orders clusters by median cost and generates comprehensive segment profiles.
    """
    cluster_features = ["rate_num", "log_votes", "log_cost"]
    X_cluster = df[cluster_features].copy()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_cluster)
    
    # 1. Elbow and Silhouette evaluation
    k_range = list(range(2, 9))
    inertias = []
    silhouettes = []
    
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(float(km.inertia_))
        # Compute silhouette on sample if dataset is large for rapid response
        sample_idx = np.random.choice(len(X_scaled), min(3000, len(X_scaled)), replace=False)
        sil = float(silhouette_score(X_scaled[sample_idx], labels[sample_idx]))
        silhouettes.append(sil)
        
    # 2. Fit final KMeans with k=3
    final_kmeans = KMeans(n_clusters=3, random_state=random_state, n_init=20)
    raw_labels = final_kmeans.fit_predict(X_scaled)
    
    df_clustered = df.copy()
    df_clustered["raw_cluster"] = raw_labels
    
    # Order clusters by median cost to reliably label as Budget, Mid-range, Premium
    cost_medians = df_clustered.groupby("raw_cluster")["cost_for_two"].median().sort_values()
    label_map = {
        int(cost_medians.index[0]): "Budget",
        int(cost_medians.index[1]): "Mid-range",
        int(cost_medians.index[2]): "Premium"
    }
    label_map_str = {str(k): v for k, v in label_map.items()}
    
    df_clustered["segment"] = df_clustered["raw_cluster"].map(label_map)
    
    # Segment Profiles
    profiles = []
    total_count = len(df_clustered)
    
    for seg in ["Budget", "Mid-range", "Premium"]:
        sub = df_clustered[df_clustered["segment"] == seg]
        n_seg = len(sub)
        profiles.append({
            "segment": seg,
            "count": int(n_seg),
            "percentage": round(float((n_seg / total_count) * 100), 2),
            "median_cost": round(float(sub["cost_for_two"].median()), 2),
            "mean_cost": round(float(sub["cost_for_two"].mean()), 2),
            "min_cost": round(float(sub["cost_for_two"].min()), 2),
            "max_cost": round(float(sub["cost_for_two"].max()), 2),
            "median_rating": round(float(sub["rate_num"].median()), 2),
            "mean_rating": round(float(sub["rate_num"].mean()), 2),
            "median_votes": round(float(sub["votes"].median()), 2),
            "mean_votes": round(float(sub["votes"].mean()), 2),
            "online_order_pct": round(float(sub["online_order_int"].mean() * 100), 2),
            "table_booking_pct": round(float(sub["book_table_int"].mean() * 100), 2),
            "top_cuisines": sub["cuisines"].value_counts().head(3).index.tolist(),
            "top_locations": sub["location"].value_counts().head(3).index.tolist(),
            "primary_types": sub["rest_type_grouped"].value_counts().head(3).index.tolist()
        })
        
    profile_df = pd.DataFrame(profiles)
    
    # Save artifacts
    joblib.dump(final_kmeans, "models/kmeans_model.joblib")
    joblib.dump(scaler, "models/scaler.joblib")
    
    result = {
        "k_range": k_range,
        "inertias": inertias,
        "silhouettes": silhouettes,
        "profiles": profile_df.to_dict(orient="records"),
        "label_mapping": label_map_str
    }
    
    return final_kmeans, scaler, df_clustered, result


if __name__ == "__main__":
    df = pd.read_csv("Dataset/cleaned_zomato.csv")
    print("Training models...")
    _, _, lr_res = train_linear_regression(df)
    print("Linear Regression Metrics:", lr_res["metrics"])
    _, _, logit_res = train_logistic_regression(df)
    print("Logistic Regression Metrics:", logit_res["metrics"])
    _, _, df_clustered, km_res = train_kmeans_clustering(df)
    print("KMeans Profiles:", pd.DataFrame(km_res["profiles"]))
