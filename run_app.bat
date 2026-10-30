@echo off
title Restaurant Recommendation - Streamlit Dashboard
echo ======================================================================
echo Launching Restaurant Recommendation System Dashboard...
echo Server running at: http://localhost:8501
echo Opening browser...
echo ======================================================================
start http://localhost:8501
python -m streamlit run restaurant_dashboard.py
pause
