import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scanner.pair_scanner import download_data, auto_scan_pairs

st.title("Pair Trading Strategy App 📊")

# Automatically scan for the top 5 pairs
tickers = ['TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'RELIANCE.NS']
top_pairs = auto_scan_pairs(tickers, n=5)

# Display the top N pairs
st.subheader("Cointegrated Pairs (p < 0.05):")
for pair in top_pairs:
    st.write(f"{pair[0]} & {pair[1]} - p-value: {round(pair[2], 4)}")

# Create a list of pair names for the dropdown (as tuples of strings)
pair_names = [f"{pair[0]} & {pair[1]}" for pair in top_pairs]

# Select Pair
if top_pairs:
    selected_pair_name = st.selectbox("Select a Cointegrated Pair", pair_names)
    
    # Extract the selected pair from the name (split by ' & ')
    stock1, stock2 = selected_pair_name.split(" & ")
    data = download_data([stock1, stock2])
    s1 = data[stock1]
    s2 = data[stock2]

    # Spread & Rolling Z-Score
    spread = s1 - s2
    spread_mean = spread.rolling(window=30).mean()
    spread_std = spread.rolling(window=30).std()
    zscore = (spread - spread_mean) / spread_std

    st.subheader("Price Chart 📈")
    st.line_chart(pd.DataFrame({stock1: s1, stock2: s2}))

    st.subheader("Spread & Z-score 📉")
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax[0].plot(spread, label="Spread", color="blue")
    ax[0].axhline(spread.mean(), color='red', linestyle='--')
    ax[0].legend()

    ax[1].plot(zscore, label="Z-score", color="purple")
    ax[1].axhline(2.0, color='red', linestyle='--')
    ax[1].axhline(-2.0, color='green', linestyle='--')
    ax[1].legend()
    st.pyplot(fig)

    # Signal Logic 
    st.subheader("Signal Generation + Backtest")

    entry_threshold = st.slider("Entry Threshold (Z-score)", min_value=0.5, max_value=3.0, value=2.0, step=0.1)
    exit_threshold = st.slider("Exit Threshold (Z-score)", min_value=0.0, max_value=2.0, value=0.5, step=0.1)

    long_signals = zscore < -entry_threshold
    short_signals = zscore > entry_threshold
    exit_signals = np.abs(zscore) < exit_threshold

    # Position Logic: Long = 1, Short = -1, Exit = 0
    position = np.where(long_signals, 1, np.where(short_signals, -1, 0))
    position = pd.Series(position, index=zscore.index)

    # Calculate returns
    returns = (s1.pct_change() - s2.pct_change()) * position.shift()
    cumulative_returns = returns.cumsum()

    st.line_chart(cumulative_returns)

    # Metrics 
    st.subheader("Metrics Summary")
    total_return = round(cumulative_returns[-1] * 100, 2)
    avg_daily_return = round(returns.mean() * 100, 4)
    sharpe_ratio = round(returns.mean() / returns.std() * np.sqrt(252), 2)

    st.write(f"**Total Strategy Return:** {total_return}%")
    st.write(f"**Average Daily Return:** {avg_daily_return}%")
    st.write(f"**Sharpe Ratio:** {sharpe_ratio}")
    st.write(f"**Long Signals:** {long_signals.sum()}")
    st.write(f"**Short Signals:** {short_signals.sum()}")
    st.write(f"**Exit Signals:** {exit_signals.sum()}")

    # Signal Table
    st.subheader("Trade Signals")
    signal_df = pd.DataFrame({
        'Date': zscore.index,
        'Z-score': zscore,
        'Signal' : position.replace({1: 'Long', -1: 'Short', 0: 'Exit'})
    })
    st.dataframe(signal_df)

    # Download 
    csv = signal_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Signal Table as CSV 📥",
        data=csv,
        file_name='pair_trading_signals.csv',
        mime='text/csv',
    )

else:
    st.warning("No cointegrated pairs found. Try different tickers.")

st.markdown("---")
st.caption("Developed by Tanya Sharma. Pair trading strategy analysis using cointegration and z-score.")
