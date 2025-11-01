# EMA Crossover Strategy – Infosys

This project implements a simple **Exponential Moving Average (EMA)** crossover strategy using Python.  
It uses 5-year data of Infosys (INFY.NS) from Yahoo Finance and evaluates performance using **QuantStats**.


## ⚠️ Disclaimer
This project was developed as part of my learning journey in quantitative trading and algorithmic research. Some portions of the code were assisted by AI tools (e.g., for syntax, debugging, and documentation), but all logic, structure, and validation were personally reviewed and tested.
This project is for educational and research purposes only.  
The results shown are based on historical simulations and do not represent real trading outcomes.  
Nothing here should be interpreted as investment advice or financial guidance.


## 📊 Overview
- **Fast EMA:** 5  
- **Slow EMA:** 15  
- **Benchmark:** NIFTY 50 (^NSEI)  
- **Output Report:** `infosys_ema_report.html`


## ⚙️ How to Run
```bash
pip install -r requirements.txt
python ema_strategy.py
