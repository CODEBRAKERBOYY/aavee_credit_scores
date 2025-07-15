
# 📊 Aave V2 Wallet Credit Scoring

This project presents a transparent and data-driven method to evaluate the creditworthiness of wallets interacting with the Aave V2 protocol. Using historical transaction-level data, we assign a **credit score between 0 and 1000** to each wallet — where higher scores reflect more responsible and reliable DeFi behavior.

---

## 🎯 Objective

- Analyze raw Aave V2 transaction data
- Engineer meaningful features from wallet behavior
- Score wallets using a rule-based model
- Deliver a **one-step script** to score any dataset

---

## 🏗️ Architecture & Folder Structure

```
aave-credit-score/
├── src/
│   └── score_wallets.py         # 🔁 One-step scoring script
├── wallet_scores_final.csv      # 📄 Output credit scores
├── wallet_scores_final.png      # 📊 Score distribution chart
├── README.md                    # 📘 Project overview
├── analysis.md                  # 📈 Score behavior breakdown
├── requirements.txt             # 📦 Python dependencies
```

---

## ⚙️ Processing Flow

1. Load raw JSON transaction data
2. Extract wallet-level actions (`deposit`, `repay`, `liquidate`, etc.)
3. Compute features like repay ratio, redeem ratio, active days
4. Score each wallet using a weighted rule-based formula
5. Normalize scores between 0–1000 using `MinMaxScaler`
6. Output CSV + visualization

---

## ✨ Features Engineered

| Feature         | Description                                           |
|----------------|-------------------------------------------------------|
| `total_txns`    | Total transactions by the wallet                     |
| `active_days`   | Number of unique active days                         |
| `repay_ratio`   | Ratio of repay to borrow transactions                |
| `redeem_ratio`  | Ratio of redeem to deposit transactions              |
| `liquid_rate`   | Ratio of liquidations to total transactions          |

---

## 🧮 Scoring Logic

A simple weighted scoring formula is applied:

```python
score_raw = (
    repay_ratio * 6 +
    redeem_ratio * 3 +
    (1 - liquid_rate) * 8 +
    normalized_active_days * 5
)
```

Scores are scaled to a range of 0–1000 using `MinMaxScaler`.

---

## ▶️ How to Run

### 1. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the Script:
```bash
python src/score_wallets.py   --input user-transactions.json   --output wallet_scores_final.csv
```

### Output:
- `wallet_scores_final.csv`: Final wallet credit scores
- `wallet_scores_final.png`: Credit score distribution plot

---

## 🔍 Score Interpretation

| Score Range  | Meaning                         |
|--------------|----------------------------------|
| 0–100        | Risky / bot-like / inactive     |
| 100–400      | Low activity / limited trust    |
| 400–700      | Consistent and healthy behavior |
| 700–1000     | Reliable and responsible users  |

> Details with charts available in `analysis.md`

---

## 🗃️ Data Source

We use real raw transaction-level Aave V2 data:

- JSON (~87MB): [Download](https://drive.google.com/file/d/1ISFbAXxadMrt7Zl96rmzzZmEKZnyW7FS/view?usp=sharing)
- Zipped (~10MB): [Download](https://drive.google.com/file/d/14ceBCLQ-BTcydDrFJauVA_PKAZ7VtDor/view?usp=sharing)

---

## 💡 Future Work

- Time-decay weighting on recent behavior
- Token value normalization
- ML-based credit model
