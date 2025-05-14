# 📊 Pair Trading Strategy App

This is an interactive Streamlit web application that implements a **Pair Trading Strategy** using **cointegration** and **Z-score** techniques. The app automatically detects the top N cointegrated stock pairs, displays price/spread charts, generates trading signals, backtests the strategy, and provides performance metrics with CSV export.

---

## 🚀 Features

- **Automatic Cointegration Scanner**  
  Detects the top N cointegrated pairs from a list of tickers using statistical testing (Engle-Granger method).

- **Interactive Pair Selection**  
  Choose a detected pair from a dropdown to explore detailed analysis and plots.

- **Live Price Chart & Spread Analysis**  
  Visualize price trends, spread, and Z-score between the selected stock pair.

- **Signal Generation (Long/Short/Exit)**  
  Based on configurable Z-score thresholds.

- **Backtesting with Metrics**  
  Computes cumulative returns, average daily return, Sharpe ratio, and counts of trade signals.

- **Downloadable Trade Signal Table**  
  Get all generated signals in a CSV format.

---

## 📂 Project Structure

```
pair-trading-app/
├── app/
    └──app.py
├── requirements.txt
├── notebook
├── README.md
└── scanner/
    └── pair_scanner.py
```

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

1. Clone the repository or download the files.
2. Ensure you have Python 3.7+ installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Example Stocks Used

You can customize the ticker list in `app.py` or `pair_scanner.py`. Default tickers:

```python
tickers = ['TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'RELIANCE.NS']
```

---


## ✍️ Author

Developed by **Tanya Sharma**  
Built using Python, Streamlit, and financial time series analysis.

---


