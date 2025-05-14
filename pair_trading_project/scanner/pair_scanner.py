import yfinance as yf
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint

def download_data(tickers, start="2020-01-01", end="2023-12-31"):
    """
    Download adjusted close prices for the given tickers from Yahoo Finance.
    """
    data = yf.download(tickers, start=start, end=end, auto_adjust=True)
    if 'Adj Close' in data.columns:
        data = data['Adj Close']  
    else:
        data = data.get('Close')  
    return data

def find_cointegrated_pairs(data, significance=0.05):
    """
    Find pairs of cointegrated stocks based on the p-value from the cointegration test.
    """
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.columns
    pairs = []

    for i in range(n):
        for j in range(i + 1, n):
            series1 = data[keys[i]]
            series2 = data[keys[j]]
            result = coint(series1, series2)
            score_matrix[i, j] = result[0]
            pvalue_matrix[i, j] = result[1]
            
            if result[1] < significance:
                pairs.append((keys[i], keys[j], result[1]))  

    return pairs, pvalue_matrix

def auto_scan_pairs(tickers, n=5, significance=0.05):
    """
    Automatically scans for the top N cointegrated pairs from a list of tickers.
    Returns the top N pairs sorted by p-value.
    """
    data = download_data(tickers)
    pairs, pvalues = find_cointegrated_pairs(data, significance)
    sorted_pairs = sorted(pairs, key=lambda x: x[2])  
    return sorted_pairs[:n]  # Return the top N pairs based on p-value


tickers = ['TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HDFCBANK.NS', 'ICICIBANK.NS']
top_pairs = auto_scan_pairs(tickers, n=5)

# Display the top cointegrated pairs
for pair in top_pairs:
    print(f"{pair[0]} & {pair[1]} - p-value: {round(pair[2], 4)}")
