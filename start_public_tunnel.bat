@echo off
title Restaurant Recommendation - Public Live Deployment
echo ======================================================================
echo Starting Restaurant Recommendation System with Live Public URL...
echo ======================================================================
start "Streamlit Server" cmd /c "python -m streamlit run restaurant_dashboard.py --server.port 8501 --server.headless true"
timeout /t 4 /nobreak >nul
echo ======================================================================
echo Launching Cloudflare HTTPS Public Tunnel...
echo The public HTTPS link will appear below:
echo ======================================================================
"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8501
pause
