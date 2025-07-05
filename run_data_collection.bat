@echo off

echo Installing required packages...
pip install -r requirements.txt

echo.
echo Fetching daily returns data...
python fetch_returns_data.py

echo.
echo Running example analysis...
python example_usage.py

echo.
echo Data collection complete!
echo Check the generated CSV files and plots.
pause