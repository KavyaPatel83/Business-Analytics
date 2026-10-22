"""
src/data_processing.py
Data Cleaning and Feature Engineering Pipeline for Bangalore Restaurant Recommendation System.
"""

import os
import json
import numpy as np
import pandas as pd


def clean_zomato_data(raw_csv_path="Dataset/zomato.csv", output_clean_path="Dataset/cleaned_zomato.csv"):
    """
    Cleans raw Zomato Bangalore data according to the 8-step project specification:
    1. Records initial count and removes duplicate restaurant records across listing types.
    2. Converts rate strings (e.g. '4.1/5') to numeric, dropping 'NEW' and '-' entries.
    3. Cleans approx_cost(for two people) by stripping commas and converting to numeric.
    4. Drops rows missing critical values (votes, cost, location, cuisines).
    5. Codes online_order and book_table to binary 0/1, groups rare rest_types.
    6. Generates log(cost) and log(votes) to address strong right skewness.
    7. Creates binary target 'highly_rated' (rating >= 4.0).
    8. Records step-by-step row counts in a structured cleaning log.
    """
    print(f"Loading raw data from: {raw_csv_path}")
    df = pd.read_csv(raw_csv_path)
    
    cleaning_log = []
    cleaning_log.append({
        "step_num": 1,
        "step_name": "Raw Dataset Loaded",
        "rows_remaining": int(len(df)),
        "rows_dropped": 0,
        "description": "Initial raw Zomato Bangalore listing dataset with multi-zone listing duplicates."
    })
    
    # Aggregate listing types per restaurant before deduplicating
    print("Aggregating listing types per physical restaurant (name + address)...")
    listing_agg = (
        df.groupby(["name", "address"])["listed_in(type)"]
        .apply(lambda s: ", ".join(sorted(set(str(x).strip() for x in s.dropna() if str(x).strip() != ""))))
        .reset_index()
        .rename(columns={"listed_in(type)": "available_listing_types"})
    )
    
    # Step 1: Remove duplicate restaurants
    initial_len = len(df)
    df_dedup = df.drop_duplicates(subset=["name", "address"]).copy()
    df_dedup = df_dedup.merge(listing_agg, on=["name", "address"], how="left")
    rows_dropped = initial_len - len(df_dedup)
    cleaning_log.append({
        "step_num": 2,
        "step_name": "Deduplicate Restaurants",
        "rows_remaining": int(len(df_dedup)),
        "rows_dropped": int(rows_dropped),
        "description": "Removed duplicate listings for identical restaurant entities listed across multiple Bangalore search zones."
    })

    # Step 2: Rate cleaning
    initial_len = len(df_dedup)
    df_dedup["rate_clean"] = df_dedup["rate"].astype(str).str.split("/").str[0].str.strip()
    valid_rate_mask = (
        ~df_dedup["rate_clean"].isin(["NEW", "-", "nan", "None", ""])
        & df_dedup["rate_clean"].notnull()
    )
    df_rate = df_dedup[valid_rate_mask].copy()
    df_rate["rate_num"] = pd.to_numeric(df_rate["rate_clean"], errors="coerce")
    df_rate = df_rate.dropna(subset=["rate_num"])
    rows_dropped = initial_len - len(df_rate)
    cleaning_log.append({
        "step_num": 3,
        "step_name": "Filter Unrated and NEW Outlets",
        "rows_remaining": int(len(df_rate)),
        "rows_dropped": int(rows_dropped),
        "description": "Extracted numeric ratings out of 5.0 and removed unrated outlets marked as 'NEW' or '-'."
    })

    # Step 3: Cost cleaning
    initial_len = len(df_rate)
    df_cost = df_rate.copy()
    df_cost["cost_for_two"] = (
        df_cost["approx_cost(for two people)"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df_cost["cost_for_two"] = pd.to_numeric(df_cost["cost_for_two"], errors="coerce")
    df_cost = df_cost.dropna(subset=["cost_for_two"])
    rows_dropped = initial_len - len(df_cost)
    cleaning_log.append({
        "step_num": 4,
        "step_name": "Parse Cost for Two",
        "rows_remaining": int(len(df_cost)),
        "rows_dropped": int(rows_dropped),
        "description": "Cleaned comma thousand-separators and parsed cost for two into numeric values in INR."
    })

    # Step 4: Drop nulls in essential fields
    initial_len = len(df_cost)
    df_clean = df_cost.dropna(subset=["votes", "location", "cuisines", "rest_type", "listed_in(type)"]).copy()
    # Also ensure votes >= 0 and cost > 0
    df_clean = df_clean[(df_clean["cost_for_two"] > 0) & (df_clean["votes"] >= 0)].copy()
    rows_dropped = initial_len - len(df_clean)
    cleaning_log.append({
        "step_num": 5,
        "step_name": "Drop Incomplete Records",
        "rows_remaining": int(len(df_clean)),
        "rows_dropped": int(rows_dropped),
        "description": "Removed records missing location, cuisines, restaurant category, or with zero cost."
    })

    # Step 5: Service features & restaurant type grouping
    df_clean["online_order_int"] = df_clean["online_order"].astype(str).str.strip().str.lower().apply(lambda x: 1 if x == "yes" else 0)
    df_clean["book_table_int"] = df_clean["book_table"].astype(str).str.strip().str.lower().apply(lambda x: 1 if x == "yes" else 0)

    # Clean primary restaurant type
    df_clean["primary_rest_type"] = df_clean["rest_type"].astype(str).apply(lambda x: x.split(",")[0].strip())
    # Group rare types with fewer than 100 occurrences as "Other"
    type_counts = df_clean["primary_rest_type"].value_counts()
    common_types = type_counts[type_counts >= 100].index.tolist()
    df_clean["rest_type_grouped"] = df_clean["primary_rest_type"].apply(
        lambda x: x if x in common_types else "Other"
    )

    # Standardize listed_in(type) column name
    df_clean["listed_in_type"] = df_clean["listed_in(type)"].astype(str).str.strip()

    # Step 6: Log transformations
    df_clean["log_cost"] = np.log1p(df_clean["cost_for_two"])
    df_clean["log_votes"] = np.log1p(df_clean["votes"])

    # Step 7: Create binary classification target
    df_clean["highly_rated"] = (df_clean["rate_num"] >= 4.0).astype(int)

    cleaning_log.append({
        "step_num": 6,
        "step_name": "Feature Engineering & Transformations",
        "rows_remaining": int(len(df_clean)),
        "rows_dropped": 0,
        "description": "Binary encoded services, grouped rare types into 'Other', computed log(cost) & log(votes), and established highly_rated target (>= 4.0)."
    })

    # Keep and rename selected clean columns
    selected_cols = [
        "name",
        "address",
        "location",
        "cuisines",
        "rest_type",
        "primary_rest_type",
        "rest_type_grouped",
        "listed_in_type",
        "available_listing_types",
        "dish_liked",
        "online_order",
        "book_table",
        "online_order_int",
        "book_table_int",
        "rate_num",
        "votes",
        "cost_for_two",
        "log_cost",
        "log_votes",
        "highly_rated"
    ]
    df_final = df_clean[selected_cols].reset_index(drop=True)

    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_clean_path), exist_ok=True)
    os.makedirs("results/metrics", exist_ok=True)

    # Save cleaned data
    print(f"Saving cleaned dataset ({len(df_final)} rows) to: {output_clean_path}")
    df_final.to_csv(output_clean_path, index=False)

    # Save cleaning log
    cleaning_log_path = "results/metrics/cleaning_log.json"
    with open(cleaning_log_path, "w") as f:
        json.dump(cleaning_log, f, indent=4)
    print(f"Cleaning log saved to: {cleaning_log_path}")

    return df_final, cleaning_log


if __name__ == "__main__":
    clean_zomato_data()
