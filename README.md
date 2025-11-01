# EMA Crossover Strategy – Infosys

This project implements a simple **Exponential Moving Average (EMA)** crossover strategy using Python.  
It uses 5-year data of Infosys (INFY.NS) from Yahoo Finance and evaluates performance using **QuantStats**.

---

## 📊 Overview
- **Fast EMA:** 5  
- **Slow EMA:** 15  
- **Benchmark:** NIFTY 50 (^NSEI)  
- **Output Report:** `infosys_ema_report.html`

---

## ⚙️ How to Run
```bash
pip install -r requirements.txt
python ema_strategy.py
