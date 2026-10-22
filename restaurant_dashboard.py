"""
restaurant_dashboard.py
Bangalore Restaurant Recommendation System with Statistical Dashboard.
Streamlit Interactive Application.
"""

import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

from src.recommender import RestaurantRecommender

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Restaurant Recommendation - Analytics & Decision Support",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Sleek CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Top Header Banner */
    .hero-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 1.8rem 2.2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        border: 1px solid #334155;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin: 0;
        background: linear-gradient(90deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-top: 0.4rem;
        font-weight: 400;
    }
    
    /* Custom KPI Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    }
    .metric-title {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #0F172A;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.3rem 0;
    }
    .metric-sub {
        color: #10B981;
        font-size: 0.82rem;
        font-weight: 500;
    }
    
    /* Restaurant Recommendation Cards */
    .rest-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    .rest-card:hover {
        border-color: #3B82F6;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.15);
    }
    .rest-badge-budget {
        background-color: #DCFCE7;
        color: #15803D;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
    }
    .rest-badge-mid {
        background-color: #DBEAFE;
        color: #1D4ED8;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
    }
    .rest-badge-premium {
        background-color: #F3E8FF;
        color: #7E22CE;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
    }
    .score-badge {
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.4rem 0.8rem;
        border-radius: 10px;
        display: inline-block;
    }
    
    /* Tags */
    .cuisine-tag {
        background-color: #F1F5F9;
        color: #334155;
        font-size: 0.8rem;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        margin-right: 0.3rem;
        display: inline-block;
        margin-top: 0.2rem;
    }
    
    /* Tab formatting */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.95rem;
        font-weight: 600;
        padding: 10px 18px;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Loads cleaned restaurant dataset and cached metric jsons."""
    data_path = "Dataset/cleaned_zomato.csv"
    if not os.path.exists(data_path):
        from train_and_evaluate import run_pipeline
        run_pipeline()
    df = pd.read_csv(data_path)
    
    # Load metrics
    metrics = {}
    metric_files = {
        "cleaning_log": "results/metrics/cleaning_log.json",
        "descriptive_stats": "results/metrics/descriptive_stats.json",
        "correlation_matrix": "results/metrics/correlation_matrix.json",
        "hypothesis_tests": "results/metrics/hypothesis_tests.json",
        "linear_regression": "results/metrics/linear_regression_results.json",
        "logistic_regression": "results/metrics/logistic_regression_results.json",
        "cluster_profiles": "results/metrics/cluster_profiles.json"
    }
    for key, path in metric_files.items():
        if os.path.exists(path):
            with open(path, "r") as f:
                metrics[key] = json.load(f)
        else:
            metrics[key] = None
            
    return df, metrics


# Load dataset and metrics
df, metrics = load_data()
recommender = RestaurantRecommender(df)

# Top Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Restaurant Recommendation</div>
    <div class="hero-subtitle">
        A Data-Driven Analytical System for Restaurant Recommendation, Quality Assessment, and Econometric Modeling
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎯 Recommender Engine",
    "📊 Data Overview & EDA",
    "🧪 Hypothesis Testing",
    "📈 Linear Regression (OLS)",
    "🎯 Logistic Regression",
    "🔍 Segments (K-Means)",
    "📖 Methodology & Architecture"
])


# ==============================================================================
# TAB 1: RECOMMENDER ENGINE
# ==============================================================================
with tab1:
    st.markdown("### 🔍 Personalized Recommendation System")
    st.markdown(
        "Find Bangalore's top dining spots filtered to your exact taste, budget, and neighborhood. "
        "Rankings dynamically blend **Bayesian Trusted Rating** (shrinkage for vote count), **Value for Money** (percentile rating per rupee), and **Popularity** (scaled log votes)."
    )

    # Recommender Sidebar / Controls
    with st.expander("⚙️ Filter & Customization Controls", expanded=True):
        fcol1, fcol2, fcol3 = st.columns(3)

        with fcol1:
            locations = ["All Bangalore"] + sorted(df["location"].dropna().unique().tolist())
            selected_location = st.selectbox("📍 Neighborhood / Location", locations, index=0)
            
            segments = ["All Segments", "Budget", "Mid-range", "Premium"]
            selected_segment = st.selectbox("🏷️ Budget Segment", segments, index=0)

            # Available cuisines
            all_cuisines = sorted(list(set([
                c.strip() for sublist in df["cuisines"].dropna().str.split(",") for c in sublist if c.strip() != ""
            ])))
            popular_cuisines = ["North Indian", "Chinese", "South Indian", "Biryani", "Continental", "Italian", "Cafe", "Desserts", "Fast Food"]
            selected_cuisines = st.multiselect("🍲 Cuisines", all_cuisines, default=[])

        with fcol2:
            min_c = int(df["cost_for_two"].min())
            max_c = int(df["cost_for_two"].max())
            cost_range = st.slider("💰 Approx Cost for Two (INR)", min_value=min_c, max_value=max_c, value=(min_c, max_c), step=50)

            min_votes = st.slider("🗳️ Minimum Evidence (Votes)", min_value=0, max_value=1000, value=50, step=25,
                                  help="Filters out outlets with fewer total customer reviews.")

            search_query = st.text_input("🔎 Search Name / Dish Liked", placeholder="e.g., Truffles, Pasta, Biryani, Jalsa...")

        with fcol3:
            online_choice = st.radio("🛵 Online Ordering", ["Any", "Yes", "No"], horizontal=True)
            booking_choice = st.radio("📅 Table Booking", ["Any", "Yes", "No"], horizontal=True)

            listing_types = ["Any", "Delivery", "Dine-out", "Buffet", "Cafes", "Desserts", "Pubs and bars"]
            selected_listing = st.selectbox("🍽️ Listing Category", listing_types, index=0)

            top_n = st.slider("📋 Number of Recommendations", min_value=5, max_value=30, value=10, step=5)

    # Bayesian & Weight Parameter Tuning Accordion
    with st.expander("⚖️ Advanced Ranking Weights & Bayesian Prior (m-Parameter)", expanded=False):
        st.markdown("""
        **Bayesian Average Formula:**  
        $$R_{\\text{trusted}} = \\left(\\frac{v}{v + m}\\right) R + \\left(\\frac{m}{v + m}\\right) C$$
        Where $v$ is votes, $R$ is raw rating, $m$ is the confidence vote threshold, and $C$ is the city mean rating (**3.63**).
        """)
        wcol1, wcol2, wcol3, wcol4 = st.columns(4)
        with wcol1:
            w_trusted = st.slider("Weight: Trusted Rating (w1)", 0.0, 10.0, 5.0, 0.5)
        with wcol2:
            w_value = st.slider("Weight: Value for Money (w2)", 0.0, 10.0, 3.0, 0.5)
        with wcol3:
            w_popularity = st.slider("Weight: Popularity (w3)", 0.0, 10.0, 2.0, 0.5)
        with wcol4:
            m_param = st.slider("Confidence Parameter (m)", 10, 500, 100, 10,
                                help="Number of votes required before a restaurant's rating is fully trusted over the city mean.")

    # Convert filter options
    loc_param = None if selected_location == "All Bangalore" else selected_location
    seg_param = None if selected_segment == "All Segments" else selected_segment
    online_param = 1 if online_choice == "Yes" else (0 if online_choice == "No" else None)
    book_param = 1 if booking_choice == "Yes" else (0 if booking_choice == "No" else None)
    list_param = None if selected_listing == "Any" else selected_listing

    # Execute Recommender
    recommendations, n_matches = recommender.recommend(
        location=loc_param,
        budget_segment=seg_param,
        min_cost=cost_range[0],
        max_cost=cost_range[1],
        cuisines=selected_cuisines if len(selected_cuisines) > 0 else None,
        min_votes=min_votes,
        online_order=online_param,
        book_table=book_param,
        listing_type=list_param,
        search_query=search_query,
        m=m_param,
        w_trusted=w_trusted,
        w_value=w_value,
        w_popularity=w_popularity,
        top_n=top_n
    )

    # Top Results KPI Cards
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Matching Restaurants</div>
            <div class="metric-value">{n_matches:,}</div>
            <div class="metric-sub">Out of {len(df):,} total places</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        top_place = recommendations.iloc[0]["name"] if len(recommendations) > 0 else "None"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Top Recommended Place</div>
            <div class="metric-value" style="font-size: 1.3rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{top_place}</div>
            <div class="metric-sub">Rank #1 Match</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        avg_cost_match = f"₹{recommendations['cost_for_two'].mean():.0f}" if len(recommendations) > 0 else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Cost for Two (Top)</div>
            <div class="metric-value">{avg_cost_match}</div>
            <div class="metric-sub">Matching recommendations</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">City Prior Rating (C)</div>
            <div class="metric-value">{recommender.city_mean_rating:.2f} ★</div>
            <div class="metric-sub">Confidence m = {m_param} votes</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if n_matches == 0:
        st.warning("⚠️ No restaurants match your specific filter combinations. Try loosening the price range, votes threshold, or cuisine filter.")
    else:
        # Display Top Ranked Cards
        st.markdown(f"#### 🏆 Top {len(recommendations)} Recommendations")
        
        for idx, row in recommendations.iterrows():
            seg_class = "rest-badge-budget" if row.get("segment") == "Budget" else ("rest-badge-mid" if row.get("segment") == "Mid-range" else "rest-badge-premium")
            dishes = row["dish_liked"] if pd.notnull(row["dish_liked"]) and str(row["dish_liked"]).strip() != "" else "Chef specials, popular favorites"
            
            online_str = "✅ Online Order" if row["online_order_int"] == 1 else "❌ No Online Delivery"
            book_str = "📅 Table Booking" if row["book_table_int"] == 1 else "❌ Walk-in Only"
            
            st.markdown(f"""
            <div class="rest-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span style="font-size: 1.25rem; font-weight: 700; color: #0F172A;">#{row['rank']} {row['name']}</span>
                        <span class="{seg_class}" style="margin-left: 0.6rem;">{row.get('segment', 'Dining')}</span>
                        <span style="color: #64748B; font-size: 0.9rem; margin-left: 0.6rem;">📍 {row['location']}</span>
                    </div>
                    <div class="score-badge">
                        Score: {row['final_score_100']} / 100
                    </div>
                </div>
                <div style="margin-top: 0.6rem; display: flex; flex-wrap: wrap; gap: 1.5rem; color: #334155; font-size: 0.92rem;">
                    <div>⭐ <strong>Raw Rating:</strong> {row['rate_num']:.1f}/5.0 <span style="color: #64748B;">({int(row['votes']):,} votes)</span></div>
                    <div>🛡️ <strong>Trusted Rating:</strong> <span style="color: #2563EB; font-weight: 700;">{row['trusted_rating']:.2f}</span></div>
                    <div>💰 <strong>Cost for Two:</strong> ₹{int(row['cost_for_two']):,}</div>
                    <div>💎 <strong>Value Percentile:</strong> {row['value_score']*100:.1f}%</div>
                    <div>🔥 <strong>Popularity:</strong> {row['popularity_score']*100:.1f}%</div>
                </div>
                <div style="margin-top: 0.6rem;">
                    <strong>Cuisines:</strong> {', '.join([f'<span class=\"cuisine-tag\">{c.strip()}</span>' for c in str(row['cuisines']).split(',')])}
                </div>
                <div style="margin-top: 0.4rem; color: #475569; font-size: 0.85rem;">
                    🍽️ <strong>Must-Try Dishes:</strong> {dishes}
                </div>
                <div style="margin-top: 0.4rem; color: #64748B; font-size: 0.82rem;">
                    {online_str} &nbsp;|&nbsp; {book_str} &nbsp;|&nbsp; 🏢 {row['address']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Comparative Visualization Charts
        st.markdown("---")
        st.markdown("#### 📊 Comparative Analytics of Top Picks")
        c_chart1, c_chart2 = st.columns(2)

        with c_chart1:
            # Score decomposition bar chart
            fig_scores = go.Figure()
            fig_scores.add_trace(go.Bar(
                name="Trusted Rating (Norm)",
                x=recommendations["name"].head(10),
                y=recommendations["norm_trusted"].head(10) * 100,
                marker_color="#3B82F6"
            ))
            fig_scores.add_trace(go.Bar(
                name="Value for Money (Percentile)",
                x=recommendations["name"].head(10),
                y=recommendations["value_score"].head(10) * 100,
                marker_color="#10B981"
            ))
            fig_scores.add_trace(go.Bar(
                name="Popularity (Scaled)",
                x=recommendations["name"].head(10),
                y=recommendations["popularity_score"].head(10) * 100,
                marker_color="#F59E0B"
            ))
            fig_scores.update_layout(
                barmode="group",
                title="Decomposed Component Scores (0 - 100)",
                xaxis_tickangle=-30,
                height=380,
                margin=dict(l=20, r=20, t=40, b=80),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_scores, use_container_width=True)

        with c_chart2:
            # Cost vs Rating Scatter for candidates
            fig_scatter = px.scatter(
                recommendations,
                x="cost_for_two",
                y="trusted_rating",
                size="votes",
                color="segment" if "segment" in recommendations.columns else None,
                hover_name="name",
                hover_data={"votes": True, "rate_num": True, "cost_for_two": True, "final_score_100": True},
                title="Cost vs. Bayesian Trusted Rating (Bubble Size = Votes)",
                labels={"cost_for_two": "Approx Cost for Two (INR)", "trusted_rating": "Bayesian Trusted Rating"},
                color_discrete_map={"Budget": "#10B981", "Mid-range": "#3B82F6", "Premium": "#8B5CF6"},
                height=380
            )
            fig_scatter.update_layout(margin=dict(l=20, r=20, t=40, b=40))
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Tabular View and CSV Export
        with st.expander("📄 View & Download Full Recommendation Table", expanded=False):
            disp_cols = [
                "rank", "name", "location", "segment", "rate_num", "trusted_rating",
                "votes", "cost_for_two", "final_score_100", "cuisines", "online_order", "book_table"
            ]
            valid_disp_cols = [c for c in disp_cols if c in recommendations.columns]
            st.dataframe(recommendations[valid_disp_cols], use_container_width=True)
            csv = recommendations.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Recommendations CSV", data=csv, file_name="bangalore_restaurant_recommendations.csv", mime="text/csv")


# ==============================================================================
# TAB 2: DATA OVERVIEW & EDA
# ==============================================================================
with tab2:
    st.markdown("### 📊 Dataset Overview, Cleaning Log & Descriptive Statistics")
    st.markdown(
        "Zomato Bangalore restaurant listings data cleaning journey from **51,717 raw scraped rows** "
        "to a clean, deduplicated, and feature-engineered dataset of **9,244 distinct physical restaurants**."
    )

    # Dataset Summary Metrics
    dcol1, dcol2, dcol3, dcol4, dcol5 = st.columns(5)
    with dcol1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Initial Scraped Rows</div>
            <div class="metric-value">51,717</div>
            <div class="metric-sub">Multi-zone duplicates</div>
        </div>
        """, unsafe_allow_html=True)
    with dcol2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Cleaned Restaurants</div>
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-sub">Unique physical outlets</div>
        </div>
        """, unsafe_allow_html=True)
    with dcol3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">City Mean Rating</div>
            <div class="metric-value">{df['rate_num'].mean():.2f} ★</div>
            <div class="metric-sub">Std: {df['rate_num'].std():.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with dcol4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Median Cost for Two</div>
            <div class="metric-value">₹{df['cost_for_two'].median():.0f}</div>
            <div class="metric-sub">Mean: ₹{df['cost_for_two'].mean():.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with dcol5:
        online_share = df['online_order_int'].mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Online Enabled</div>
            <div class="metric-value">{online_share:.1f}%</div>
            <div class="metric-sub">Booking: {df['book_table_int'].mean()*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Step-by-Step Data Cleaning Log
    st.markdown("#### 1. Data Preparation & Cleaning Log")
    if metrics["cleaning_log"]:
        cl_df = pd.DataFrame(metrics["cleaning_log"])
        cl_df.columns = ["Step #", "Cleaning Operation", "Rows Remaining", "Rows Dropped", "Business / Methodological Rationale"]
        st.dataframe(cl_df, use_container_width=True, hide_index=True)

    # 2. Descriptive Statistics Table
    st.markdown("#### 2. Descriptive Statistics & Skewness Analysis")
    st.markdown(
        "Notice the extreme skewness and kurtosis in **votes** (skewness = 9.06, kurtosis = 131.74) and **cost for two** (skewness = 3.21), "
        "which strongly violates normality assumptions and necessitates the **log transformations**."
    )
    if metrics["descriptive_stats"]:
        ds_df = pd.DataFrame(metrics["descriptive_stats"])
        ds_display = ds_df[["display_name", "count", "mean", "median", "std", "skewness", "kurtosis", "cv_percent", "iqr", "min", "max"]].copy()
        ds_display.columns = ["Variable", "Count", "Mean", "Median", "Std Dev", "Skewness", "Kurtosis", "CV (%)", "IQR", "Min", "Max"]
        st.dataframe(ds_display, use_container_width=True, hide_index=True)

    # 3. Distribution Figures
    st.markdown("#### 3. Distribution Visualizations & Log Transformations")
    dist_col1, dist_col2 = st.columns(2)
    with dist_col1:
        if os.path.exists("results/figures/ratings_distribution.png"):
            st.image("results/figures/ratings_distribution.png", caption="Figure 1: Customer Rating Distribution & 4.0 Cutoff", use_container_width=True)
    with dist_col2:
        if os.path.exists("results/figures/cost_votes_distribution.png"):
            st.image("results/figures/cost_votes_distribution.png", caption="Figure 2: Raw vs. Log Transformed Cost & Votes", use_container_width=True)

    # 4. Correlation Matrices
    st.markdown("#### 4. Correlation Analysis (Pearson & Spearman)")
    st.markdown(
        "Because customer dining variables are non-normal and right-skewed, **Spearman rank correlation** is more robust and reliable than Pearson correlation."
    )
    if os.path.exists("results/figures/correlation_heatmap.png"):
        st.image("results/figures/correlation_heatmap.png", caption="Figure 3: Pearson vs Spearman Heatmap Matrices", use_container_width=True)


# ==============================================================================
# TAB 3: HYPOTHESIS TESTING
# ==============================================================================
with tab3:
    st.markdown("### 🧪 Formal Hypothesis Testing Suite (α = 0.05)")
    st.markdown(
        "We test 9 fundamental business hypotheses regarding online ordering, table booking, restaurant format, location, and cost drivers. "
        "Because large sample sizes ($N = 9,244$) will reject almost any sharp null hypothesis, we report the **standardized effect size** alongside every p-value to judge practical importance."
    )

    if metrics["hypothesis_tests"]:
        ht_df = pd.DataFrame(metrics["hypothesis_tests"])
        summary_cols = ["test_id", "test_name", "statistic_type", "statistic_val", "p_value", "effect_size_metric", "effect_size_val", "decision"]
        ht_summary = ht_df[summary_cols].copy()
        ht_summary.columns = ["#", "Hypothesis Test", "Stat Type", "Stat Value", "p-value", "Effect Size Metric", "Effect Size", "Decision (α=0.05)"]
        st.dataframe(ht_summary, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("#### 📋 Detailed Test Diagnostics & Practical Impact")

        for _, row in ht_df.iterrows():
            with st.expander(f"Test #{row['test_id']}: {row['test_name']} — [{row['decision']}]", expanded=(row['test_id'] in [1, 2])):
                tcol1, tcol2 = st.columns([2, 1])
                with tcol1:
                    st.markdown(f"**Variable Tested:** {row['variable_tested']}")
                    st.markdown(f"**Null Hypothesis ($H_0$):** {row['null_hypothesis']}")
                    st.markdown(f"**Alternative Hypothesis ($H_1$):** {row['alt_hypothesis']}")
                    st.markdown(f"**Sample Information:** {row['sample_info']}")
                    st.markdown(f"💡 **Practical & Managerial Takeaway:** {row['practical_impact']}")
                with tcol2:
                    st.metric(label=f"{row['statistic_type']}", value=f"{row['statistic_val']}")
                    st.metric(label="p-value", value=f"{row['p_value']:.4e}")
                    st.metric(label=f"Effect Size ({row['effect_size_metric']})", value=f"{row['effect_size_val']}")

        st.markdown("---")
        st.markdown("#### 🖼️ Hypothesis Visualizations")
        hfig_col1, hfig_col2 = st.columns(2)
        with hfig_col1:
            if os.path.exists("results/figures/hypothesis_online_order_boxplot.png"):
                st.image("results/figures/hypothesis_online_order_boxplot.png", caption="Test 1: Online Order Welch t-test", use_container_width=True)
            if os.path.exists("results/figures/hypothesis_listing_type_boxplot.png"):
                st.image("results/figures/hypothesis_listing_type_boxplot.png", caption="Tests 3 & 5: Listing Type ANOVA (Rating & Cost)", use_container_width=True)
        with hfig_col2:
            if os.path.exists("results/figures/hypothesis_table_booking_boxplot.png"):
                st.image("results/figures/hypothesis_table_booking_boxplot.png", caption="Test 2: Table Booking Welch t-test", use_container_width=True)
            if os.path.exists("results/figures/hypothesis_top_locations_boxplot.png"):
                st.image("results/figures/hypothesis_top_locations_boxplot.png", caption="Test 4: Top 10 Bangalore Locations ANOVA", use_container_width=True)


# ==============================================================================
# TAB 4: MULTIPLE LINEAR REGRESSION
# ==============================================================================
with tab4:
    st.markdown("### 📈 Multiple Linear Regression (OLS Econometric Model)")
    st.markdown(
        "Predicts continuous customer rating ($y = \\text{rate\\_num}$) from log votes, log cost, online ordering, table booking, listing category, and restaurant format using an **80/20 train-test split**."
    )

    if metrics["linear_regression"]:
        reg_m = metrics["linear_regression"]["metrics"]
        
        # Fit KPI Cards
        rcol1, rcol2, rcol3, rcol4, rcol5 = st.columns(5)
        with rcol1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Train R² (Fit)</div>
                <div class="metric-value">{reg_m['train_r2']:.3f}</div>
                <div class="metric-sub">Adj R²: {reg_m['adj_r2']:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        with rcol2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Test R² (Holdout)</div>
                <div class="metric-value">{reg_m['test_r2']:.3f}</div>
                <div class="metric-sub">Train-Test Gap: {abs(reg_m['train_r2']-reg_m['test_r2']):.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        with rcol3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Test RMSE</div>
                <div class="metric-value">{reg_m['test_rmse']:.3f}</div>
                <div class="metric-sub">MAE: {reg_m['test_mae']:.3f} stars</div>
            </div>
            """, unsafe_allow_html=True)
        with rcol4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">F-Statistic</div>
                <div class="metric-value">{reg_m['f_statistic']:.1f}</div>
                <div class="metric-sub">p-value = {reg_m['f_pvalue']:.4e}</div>
            </div>
            """, unsafe_allow_html=True)
        with rcol5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Observations</div>
                <div class="metric-value">{reg_m['n_train']:,}</div>
                <div class="metric-sub">Test set: {reg_m['n_test']:,}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Coefficient Table and Interpretation
        st.markdown("#### 1. Estimated Model Coefficients & Statistical Significance")
        coef_df = pd.DataFrame(metrics["linear_regression"]["coefficients"])
        coef_display = coef_df[["feature", "coefficient", "std_error", "t_statistic", "p_value", "ci_lower", "ci_upper"]].copy()
        coef_display.columns = ["Predictor Feature", "Coefficient (β)", "Std Error", "t-statistic", "p-value", "95% CI Lower", "95% CI Upper"]
        st.dataframe(coef_display, use_container_width=True, hide_index=True)

        # Multicollinearity (VIF) & Residual Diagnostics
        reg_c1, reg_c2 = st.columns(2)
        with reg_c1:
            st.markdown("#### 2. Multicollinearity Assessment (VIF)")
            st.markdown("Variance Inflation Factor (VIF) diagnostics check for predictor multicollinearity. All VIFs < 5 confirm clean model stability.")
            vif_df = pd.DataFrame(metrics["linear_regression"]["vif"])
            vif_df.columns = ["Feature", "VIF", "Collinearity Status"]
            st.dataframe(vif_df, use_container_width=True, hide_index=True)

        with reg_c2:
            st.markdown("#### 3. Econometric Residual Diagnostics")
            st.markdown(f"""
            - **Residual Mean:** `{reg_m['residual_mean']:.6f}` (Satisfies $E[e] = 0$)
            - **Residual Std Dev:** `{reg_m['residual_std']:.4f}`
            - **Breusch-Pagan Heteroscedasticity Stat:** `{reg_m['bp_hetero_stat']}` (p = `{reg_m['bp_hetero_pvalue']:.4e}`)
            - **Economic Interpretation:** An $R^2$ of ~0.39 (explaining ~39% of variance) is realistic for consumer dining because food flavor, ambiance, and personal diner preference are unobserved.
            """)
            if os.path.exists("results/figures/regression_residuals.png"):
                st.image("results/figures/regression_residuals.png", caption="Figure 4: Residuals vs Fitted & Normality", use_container_width=True)

        if os.path.exists("results/figures/regression_coefficients.png"):
            st.image("results/figures/regression_coefficients.png", caption="Figure 5: Feature Coefficient Impact on Rating", use_container_width=True)


# ==============================================================================
# TAB 5: LOGISTIC REGRESSION
# ==============================================================================
with tab5:
    st.markdown("### 🎯 Logistic Regression: Classifying 'Highly Rated' Outlets (≥ 4.0)")
    st.markdown(
        "Predicts whether an establishment achieves a premium customer rating of **4.0 or above** from service features, price point, review volume, and venue type."
    )

    if metrics["logistic_regression"]:
        logit_m = metrics["logistic_regression"]["metrics"]
        
        # Classification KPI Cards
        lcol1, lcol2, lcol3, lcol4, lcol5 = st.columns(5)
        with lcol1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Model Accuracy</div>
                <div class="metric-value">{logit_m['accuracy']*100:.1f}%</div>
                <div class="metric-sub">Overall Correct</div>
            </div>
            """, unsafe_allow_html=True)
        with lcol2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Majority Baseline</div>
                <div class="metric-value">{logit_m['majority_baseline_accuracy']*100:.1f}%</div>
                <div class="metric-sub">No-Skill Benchmark</div>
            </div>
            """, unsafe_allow_html=True)
        with lcol3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Accuracy Lift</div>
                <div class="metric-value">+{logit_m['accuracy_lift_over_baseline']*100:.1f}%</div>
                <div class="metric-sub">Over Majority Class</div>
            </div>
            """, unsafe_allow_html=True)
        with lcol4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">ROC-AUC Score</div>
                <div class="metric-value">{logit_m['roc_auc']:.3f}</div>
                <div class="metric-sub">High Discrimination</div>
            </div>
            """, unsafe_allow_html=True)
        with lcol5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Pseudo R² (McFadden)</div>
                <div class="metric-value">{logit_m['pseudo_r2_mcfadden']:.3f}</div>
                <div class="metric-sub">Excellent Fit (> 0.40)</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Odds Ratios and Interpretations
        st.markdown("#### 1. Odds Ratios (OR = e^β) & 95% Confidence Intervals")
        st.markdown(
            "An Odds Ratio of **2.0** means the feature doubles the odds of receiving a rating of 4.0 or above, holding other variables constant."
        )
        or_df = pd.DataFrame(metrics["logistic_regression"]["odds_ratios"])
        or_display = or_df[["feature", "coefficient", "odds_ratio", "p_value", "ci_lower", "ci_upper"]].copy()
        or_display.columns = ["Feature", "Coefficient (β)", "Odds Ratio (OR)", "p-value", "95% CI Lower", "95% CI Upper"]
        st.dataframe(or_display, use_container_width=True, hide_index=True)

        # Visualizations (ROC Curve, Confusion Matrix, Odds Ratio Forest Plot)
        st.markdown("#### 2. Classification Visual Diagnostics")
        vcol1, vcol2 = st.columns(2)
        with vcol1:
            if os.path.exists("results/figures/logistic_roc_curve.png"):
                st.image("results/figures/logistic_roc_curve.png", caption="Figure 6: ROC Curve (AUC = 0.911 vs Baseline 0.500)", use_container_width=True)
            if os.path.exists("results/figures/logistic_confusion_matrix.png"):
                st.image("results/figures/logistic_confusion_matrix.png", caption="Figure 7: Test Set Confusion Matrix", use_container_width=True)
        with vcol2:
            if os.path.exists("results/figures/logistic_odds_ratios.png"):
                st.image("results/figures/logistic_odds_ratios.png", caption="Figure 8: Odds Ratio Forest Plot", use_container_width=True)


# ==============================================================================
# TAB 6: SEGMENTS (K-MEANS)
# ==============================================================================
with tab6:
    st.markdown("### 🔍 Customer & Restaurant Segmentation (K-Means Clustering)")
    st.markdown(
        "Using standardized rating, log votes, and log cost, restaurants are segmented into **Budget**, **Mid-range**, and **Premium** clusters. "
        "Cluster profiles unveil distinct dining operational behaviors and consumer segments across Bangalore."
    )

    if metrics["cluster_profiles"]:
        km_data = metrics["cluster_profiles"]
        profiles_df = pd.DataFrame(km_data["profiles"])

        # Display 3 Segment KPI Cards
        scol1, scol2, scol3 = st.columns(3)
        for i, col in enumerate([scol1, scol2, scol3]):
            seg_row = profiles_df.iloc[i]
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">{seg_row['segment']} Segment</div>
                    <div class="metric-value">₹{seg_row['median_cost']:.0f}</div>
                    <div class="metric-sub">{seg_row['count']:,} Outlets ({seg_row['percentage']}%) | {seg_row['median_rating']:.1f} ★</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Full Cluster Profiles Table
        st.markdown("#### 1. Comprehensive Segment Profiles")
        prof_display = profiles_df[[
            "segment", "count", "percentage", "median_cost", "mean_cost",
            "median_rating", "mean_rating", "median_votes", "online_order_pct", "table_booking_pct"
        ]].copy()
        prof_display.columns = [
            "Segment", "Count", "Share (%)", "Median Cost (₹)", "Mean Cost (₹)",
            "Median Rating", "Mean Rating", "Median Votes", "Online Order %", "Table Booking %"
        ]
        st.dataframe(prof_display, use_container_width=True, hide_index=True)

        # Detailed qualitative profile tags
        for _, prow in profiles_df.iterrows():
            st.info(
                f"**{prow['segment']} Segment Snapshot:** Typical cost: ₹{prow['median_cost']:.0f} for two. "
                f"Top formats: `{', '.join(prow['primary_types'])}`. "
                f"Leading locations: `{', '.join(prow['top_locations'])}`. "
                f"Online adoption: **{prow['online_order_pct']}%**, Table booking adoption: **{prow['table_booking_pct']}%**."
            )

        # Visualizations (Elbow, Silhouette, Scatter)
        st.markdown("#### 2. Clustering Diagnostics & Cluster Map")
        kcol1, kcol2 = st.columns(2)
        with kcol1:
            if os.path.exists("results/figures/kmeans_elbow_silhouette.png"):
                st.image("results/figures/kmeans_elbow_silhouette.png", caption="Figure 9: Elbow Method & Silhouette Scores (k=2 to 8)", use_container_width=True)
        with kcol2:
            if os.path.exists("results/figures/kmeans_clusters_scatter.png"):
                st.image("results/figures/kmeans_clusters_scatter.png", caption="Figure 10: 2D Cluster Separation (Cost vs. Rating)", use_container_width=True)


# ==============================================================================
# TAB 7: METHODOLOGY & ARCHITECTURE
# ==============================================================================
with tab7:
    st.markdown("### 📖 Methodology, System Architecture & Experimental Verification")
    st.markdown(
        "Complete technical and algorithmic documentation mapping to Project Objectives, System Architecture, and Test Case Verifications."
    )

    with st.expander("🔄 1. End-to-End Methodology Flowchart", expanded=True):
        st.markdown("""
```
[Raw Zomato Dataset (51,717 rows)]
             │
             ▼
[1. Data Cleaning & Deduplication] ───► Deduplicate physical restaurants by (name, address)
             │                        ───► Clean ratings (drop NEW, -), parse cost (INR)
             │                        ───► Drop incomplete rows (9,244 unique places remain)
             ▼
[2. Feature Engineering]           ───► Log(Votes + 1), Log(Cost + 1)
             │                        ───► Binary coding (online_order, book_table)
             │                        ───► Binary target: highly_rated (≥ 4.0)
             ▼
[3. Statistical Exploratory Data]  ───► Descriptive Stats (Mean, SD, Skewness, Kurtosis, CV)
             │                        ───► Pearson & Spearman Rank Correlation
             ▼
[4. Hypothesis Testing (α = 0.05)] ───► Welch t-tests (Online order & Table booking)
             │                        ───► One-way ANOVAs (Listing types, Top locations, Cost)
             │                        ───► Kruskal-Wallis & Chi-square Independence tests
             │                        ───► Standardized Effect sizes (Cohen's d, η², Cramer's V)
             ▼
[5. Predictive Modeling]           ───► Multiple Linear Regression (OLS, VIF, Residuals)
             │                        ───► Logistic Regression (Odds ratios, ROC-AUC = 0.911)
             │                        ───► K-Means Clustering (k = 3: Budget, Mid-range, Premium)
             ▼
[6. Recommender Engine]            ───► Bayesian Average: R_trusted = (v/(v+m))·R + (m/(v+m))·C
             │                        ───► Value-for-Money percentile rank & Scaled Popularity
             │                        ───► Composite Weighted Score: (w1·R + w2·V + w3·P)/Σw
             ▼
[7. Streamlit Analytics App]       ───► Real-time dynamic dashboard & interactive recommendations
```
        """)

    with st.expander("📐 2. Mathematical Scoring Formulations", expanded=True):
        st.markdown("""
        #### A. Bayesian Average (Trusted Rating)
        Raw ratings are subject to small-sample variance (e.g., 5.0 from 2 reviews). The Bayesian estimator shrinks ratings toward the prior city mean:
        $$R_{\\text{trusted}} = \\left(\\frac{v}{v + m}\\right) R + \\left(\\frac{m}{v + m}\\right) C$$
        - $v$: Observed customer review count (votes)
        - $R$: Observed arithmetic average rating
        - $m$: Prior weight / confidence parameter (default $m = 100$ votes)
        - $C$: City-wide mean benchmark rating ($C = 3.63$)

        #### B. Value-for-Money Percentile Rank
        Evaluates the quality-to-cost ratio:
        $$\\text{Value Ratio} = \\frac{R_{\\text{trusted}}}{\\text{Cost for Two}}$$
        $$\\text{Value Score} = \\text{Percentile Rank}(\\text{Value Ratio})$$

        #### C. Final Composite Rank Score
        $$\\text{Composite Score} = \\frac{w_1 \\cdot \\text{Norm}(R_{\\text{trusted}}) + w_2 \\cdot \\text{Value Score} + w_3 \\cdot \\text{Popularity Score}}{w_1 + w_2 + w_3}$$
        """)

    with st.expander("🧪 3. Verified System Test Cases & Results", expanded=True):
        st.markdown("""
        #### Test Case 1: Student Budget Dining in Koramangala 5th Block
        - **Constraints:** Location = *Koramangala 5th Block*, Max Cost = *₹500*, Cuisines = *Fast Food, North Indian, Chinese*, Min Votes = *50*, Online Order = *Yes*.
        - **Weights:** Trusted = 5.0, Value = 3.0, Popularity = 2.0 | Confidence $m = 100$.
        - **Matches Found:** **25 matching restaurants**.
        - **Top Recommendations:**
          1. **Juice Junction** (Score: 70.9/100, Cost: ₹150, Raw: 4.1★, Trusted: 3.84★, Value Rank: 100th percentile)
          2. **Momo Hut** (Score: 70.0/100, Cost: ₹250, Raw: 4.0★, Trusted: 3.86★, Value Rank: 80th percentile)
          3. **Tall Blonde French** (Score: 67.3/100, Cost: ₹300, Raw: 4.1★, Trusted: 4.00★, Value Rank: 56th percentile)
          4. **Dosa Plaza** (Score: 66.6/100, Cost: ₹250, Raw: 3.8★, Trusted: 3.71★, Value Rank: 92nd percentile)

        #### Test Case 2: Premium Family Celebration Dining in Indiranagar
        - **Constraints:** Location = *Indiranagar*, Min Cost = *₹1,000*, Table Booking = *Yes*, Min Votes = *200*.
        - **Weights:** Trusted = 6.0, Value = 1.0, Popularity = 3.0 | Confidence $m = 100$.
        - **Matches Found:** **57 matching restaurants**.
        - **Top Recommendations:**
          1. **The Pizza Bakery** (Score: 86.2/100, Cost: ₹1,200, 1,724 votes, Raw: 4.8★, Trusted: 4.74★)
          2. **Barbeque Nation** (Score: 85.2/100, Cost: ₹1,600, 3,848 votes, Raw: 4.7★, Trusted: 4.67★)
          3. **Chianti** (Score: 84.4/100, Cost: ₹1,500, 3,416 votes, Raw: 4.7★, Trusted: 4.67★)
          4. **Smoke House Deli** (Score: 81.9/100, Cost: ₹1,600, 2,752 votes, Raw: 4.6★, Trusted: 4.57★)
          5. **Delhi Highway** (Score: 81.8/100, Cost: ₹1,200, 1,477 votes, Raw: 4.5★, Trusted: 4.44★)

        #### Test Case 3: Sensitivity Verification on Confidence Threshold ($m$)
        - Evaluated low-evidence outlet (15 votes, 4.70★) vs high-evidence outlet (1,200 votes, 4.30★) across prior weights $m \\in [10, 500]$:
          - At $m = 10$: Low-evidence outlet retains 4.27★.
          - At $m = 100$ (default): Low-evidence outlet drops to **3.77★**, while high-evidence outlet remains at **4.25★** (wins by +0.48★).
          - At $m = 500$: Low-evidence outlet collapses to near city average (**3.66★**), while high-evidence holds strong at **4.10★**.
        """)

    with st.expander("⚠️ 4. Project Limitations & Future Scope", expanded=False):
        st.markdown("""
        - **Limitations:**
          1. Scraped snapshot data does not reflect real-time kitchen changes or seasonal menu updates.
          2. Approximate cost for two is an aggregated midpoint that varies depending on alcohol consumption.
          3. Single-platform data without hygiene inspection or delivery speed telemetry.
        - **Future Scope:**
          1. Aspect-based Sentiment Analysis (ABSA) on free-text review comments using BERT/LLMs.
          2. Interactive map view with geospatial routing using Folium / Mapbox.
          3. Hybrid recommender blending content-based scores with collaborative filtering.
        """)
