"""
src/recommender.py
Intelligent Restaurant Recommendation Engine.
Calculates:
1. Bayesian Average Trusted Rating:
   R_trusted = (v / (v + m)) * R + (m / (v + m)) * C
   Where v = votes, R = raw rating, m = credibility threshold (default 100), C = city mean rating.
2. Value Score:
   Percentile rank of (trusted rating / cost_for_two) among candidate/matching restaurants.
3. Popularity Score:
   Scaled log(1 + votes) normalized between 0 and 1.
4. Final Composite Score:
   Score = (w1 * Scaled_Trusted + w2 * Value + w3 * Popularity) / (w1 + w2 + w3)
"""

import numpy as np
import pandas as pd


class RestaurantRecommender:
    def __init__(self, df):
        """
        Initializes the recommender with the cleaned restaurant dataset.
        Computes city-wide baseline metrics.
        """
        self.df = df.copy()
        self.city_mean_rating = float(self.df["rate_num"].mean())
        self.max_log_votes = float(np.log1p(self.df["votes"].max()))
        self.min_rating = float(self.df["rate_num"].min())
        self.max_rating = float(self.df["rate_num"].max())
        
    def calculate_trusted_rating(self, votes, rating, m=100):
        """
        Calculates the Bayesian Average rating.
        m: confidence parameter (minimum votes needed to fully trust raw rating).
        """
        votes = np.array(votes, dtype=float)
        rating = np.array(rating, dtype=float)
        weight_obs = votes / (votes + m)
        weight_prior = m / (votes + m)
        trusted = (weight_obs * rating) + (weight_prior * self.city_mean_rating)
        return trusted

    def recommend(
        self,
        location=None,
        budget_segment=None,
        min_cost=None,
        max_cost=None,
        cuisines=None,
        min_votes=0,
        online_order=None,
        book_table=None,
        listing_type=None,
        search_query=None,
        m=100,
        w_trusted=5.0,
        w_value=3.0,
        w_popularity=2.0,
        top_n=10
    ):
        """
        Filters candidate restaurants and ranks them by composite score.
        Returns top_n matches, full filtered table, and matching count.
        """
        filtered = self.df.copy()

        # 1. Location filter
        if location and location not in ["All", "Any"]:
            if isinstance(location, list):
                filtered = filtered[filtered["location"].isin(location)]
            else:
                filtered = filtered[filtered["location"] == location]

        # 2. Budget Segment filter
        if budget_segment and budget_segment not in ["All", "Any"]:
            if "segment" in filtered.columns:
                if isinstance(budget_segment, list):
                    filtered = filtered[filtered["segment"].isin(budget_segment)]
                else:
                    filtered = filtered[filtered["segment"] == budget_segment]

        # 3. Numeric cost filters
        if min_cost is not None and min_cost > 0:
            filtered = filtered[filtered["cost_for_two"] >= min_cost]
        if max_cost is not None and max_cost > 0:
            filtered = filtered[filtered["cost_for_two"] <= max_cost]

        # 4. Minimum votes filter
        if min_votes > 0:
            filtered = filtered[filtered["votes"] >= min_votes]

        # 5. Online order filter (1 for Yes, 0 for No, None for Any)
        if online_order is not None and online_order in [0, 1]:
            filtered = filtered[filtered["online_order_int"] == online_order]

        # 6. Table booking filter (1 for Yes, 0 for No, None for Any)
        if book_table is not None and book_table in [0, 1]:
            filtered = filtered[filtered["book_table_int"] == book_table]

        # 7. Listing type filter
        if listing_type and listing_type not in ["All", "Any"]:
            # Check if restaurant offers this listing type in available_listing_types or listed_in_type
            mask_primary = filtered["listed_in_type"].str.contains(listing_type, case=False, na=False)
            mask_all = filtered["available_listing_types"].str.contains(listing_type, case=False, na=False) if "available_listing_types" in filtered.columns else False
            filtered = filtered[mask_primary | mask_all]

        # 8. Cuisines filter
        if cuisines:
            if isinstance(cuisines, str):
                cuisines = [cuisines]
            cuisine_conditions = [
                filtered["cuisines"].str.contains(c.strip(), case=False, na=False)
                for c in cuisines if c.strip() != ""
            ]
            if cuisine_conditions:
                # Matches if ANY of the chosen cuisines is present
                combined_mask = np.logical_or.reduce(cuisine_conditions)
                filtered = filtered[combined_mask]

        # 9. Free-text search query (name, address, dish liked)
        if search_query and search_query.strip():
            sq = search_query.strip().lower()
            mask_q = (
                filtered["name"].str.lower().str.contains(sq, na=False)
                | filtered["cuisines"].str.lower().str.contains(sq, na=False)
                | filtered["dish_liked"].astype(str).str.lower().str.contains(sq, na=False)
                | filtered["address"].str.lower().str.contains(sq, na=False)
            )
            filtered = filtered[mask_q]

        n_matches = len(filtered)
        if n_matches == 0:
            return pd.DataFrame(), 0

        # Calculate Scores
        filtered = filtered.copy()
        
        # 1. Trusted Rating
        filtered["trusted_rating"] = self.calculate_trusted_rating(
            filtered["votes"].values,
            filtered["rate_num"].values,
            m=m
        )
        
        # Scale trusted rating to 0 - 1
        # Range is anchored from min possible rating (e.g. 1.5) to 5.0
        r_min = min(2.0, float(filtered["trusted_rating"].min()))
        r_max = 5.0
        filtered["norm_trusted"] = np.clip((filtered["trusted_rating"] - r_min) / (r_max - r_min), 0.0, 1.0)

        # 2. Value Score: Percentile rank of (trusted_rating / cost_for_two)
        filtered["value_ratio"] = filtered["trusted_rating"] / filtered["cost_for_two"]
        if n_matches > 1:
            filtered["value_score"] = filtered["value_ratio"].rank(pct=True)
        else:
            filtered["value_score"] = 1.0

        # 3. Popularity Score: Scaled log(votes + 1)
        # Scaled relative to the city-wide max log votes so it's a global benchmark
        filtered["popularity_score"] = np.clip(np.log1p(filtered["votes"]) / self.max_log_votes, 0.0, 1.0)

        # 4. Final Composite Score
        total_w = w_trusted + w_value + w_popularity
        if total_w == 0:
            total_w = 1.0
            
        filtered["final_score"] = (
            (w_trusted * filtered["norm_trusted"])
            + (w_value * filtered["value_score"])
            + (w_popularity * filtered["popularity_score"])
        ) / total_w
        
        # Rescale final score to 0 - 100 for intuitive presentation
        filtered["final_score_100"] = (filtered["final_score"] * 100).round(1)

        # Sort descending by final score
        ranked = filtered.sort_values(by=["final_score", "trusted_rating", "votes"], ascending=False).reset_index(drop=True)
        ranked["rank"] = ranked.index + 1

        top_recommendations = ranked.head(top_n)
        return top_recommendations, n_matches
