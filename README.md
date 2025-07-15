# Aave V2 Wallet Credit Scoring

This project presents a data-driven method to evaluate the creditworthiness of wallets interacting with the Aave V2 protocol. Using historical transaction-level data, we assign a credit score between **0 and 1000** for each wallet, with higher scores indicating responsible and reliable usage.

---

## 🎯 Objective

- Analyze raw Aave transaction data
- Engineer wallet behavior features
- Score wallets using a rule-based logic
- Generate a one-step script for scoring any transaction log

---

## 📁 Project Structure

```
aave-credit-score/
├── src/
│   └── score_wallets.py         # Main scoring script
├── wallet_scores_final.csv      # Output credit scores
├── wallet_scores_final.png      # Score distribution chart
├── README.md                    # Project overview and method
├── analysis.md                  # Score analysis
├── requirements.txt             # Python dependencies
```

---

## ⚙️ Feature Engineering

The script extracts and computes the following wallet-level features:

| Feature         | Description                                           |
|----------------|-------------------------------------------------------|
| `total_txns`    | Number of actions by the wallet                      |
| `active_days`   | Unique days of activity                              |
| `repay_ratio`   | repay actions / borrow actions                       |
| `redeem_ratio`  | redeem actions / deposit actions                     |
| `liquid_rate`   | liquidation events / total actions                   |

---

## 📊 Scoring Formula

A simple weighted scoring logic is used:

```python
score_raw = (
    repay_ratio * 6 +
    redeem_ratio * 3 +
    (1 - liquid_rate) * 8 +
    normalized_active_days * 5
)
```

Then it's scaled to the 0–1000 range using `MinMaxScaler`.

---

## ▶️ How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python src/score_wallets.py \
  --input user-transactions.json \
  --output wallet_scores_final.csv
```

This generates:
- `wallet_scores_final.csv`: wallet scores
- `wallet_scores_final.png`: score distribution chart

---

## 📈 Example Output

**wallet_scores_final.csv**

| wallet                                  | credit_score |
|-----------------------------------------|--------------|
| 0x000...d4b6                            | 5.50         |
| 0x000...e2dc                            | 5.56         |
| ...                                     | ...          |

**wallet_scores_final.png** – Histogram of credit score distribution

---

## 🔍 Score Ranges

| Score Range  | Meaning                         |
|--------------|----------------------------------|
| 0–100        | Risky / bot-like / inactive     |
| 100–400      | Low activity / limited trust    |
| 400–700      | Consistent and healthy behavior |
| 700–1000     | Reliable and responsible users  |

Detailed insights available in `analysis.md`.

---

## 🗃️ Data Source

The dataset used is a raw Aave V2 transaction-level JSON file:

- Raw JSON (~87MB): [Download](https://drive.google.com/file/d/1ISFbAXxadMrt7Zl96rmzzZmEKZnyW7FS/view?usp=sharing)
- Zipped (~10MB): [Download](https://drive.google.com/file/d/14ceBCLQ-BTcydDrFJauVA_PKAZ7VtDor/view?usp=sharing)

---

## 💡 Future Improvements

- Time-decay weighting on recent transactions
- Normalization by token value
- ML-based model instead of rule-based logic
