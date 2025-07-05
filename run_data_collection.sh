#!/bin/bash

# Script to run the data collection

echo "Installing required packages..."
pip install -r requirements.txt

echo "\nFetching daily returns data..."
python fetch_returns_data.py

echo "\nRunning example analysis..."
python example_usage.py

echo "\nData collection complete!"
echo "Check the generated CSV files and plots."