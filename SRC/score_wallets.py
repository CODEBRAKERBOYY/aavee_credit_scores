import argparse, pathlib
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

def load_and_prepare(json_path):
    df = pd.read_json(json_path)
    df = df.rename(columns={'userWallet': 'user'})
    df['action'] = df['action'].str.lower()
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df['date'] = df['datetime'].dt.date
    return df

def engineer_features(df):
    rows = []
    for wallet, group in tqdm(df.groupby('user')):
        dep = (group['action'] == 'deposit').sum()
        bor = (group['action'] == 'borrow').sum()
        rep = (group['action'] == 'repay').sum()
        red = (group['action'] == 'redeemunderlying').sum()
        liq = (group['action'] == 'liquidationcall').sum()
        total = len(group)
        days = group['date'].nunique()
        rows.append({
            'wallet': wallet,
            'repay_ratio': rep / bor if bor else 0,
            'redeem_ratio': red / dep if dep else 0,
            'liquid_rate': liq / total if total else 0,
            'active_days': days
        })
    return pd.DataFrame(rows)

def compute_scores(features_df, w_repay=6, w_redeem=3, w_liquid=8, w_activity=5):
    raw = (
        features_df['repay_ratio'] * w_repay +
        features_df['redeem_ratio'] * w_redeem +
        (1 - features_df['liquid_rate']) * w_liquid +
        (features_df['active_days'] / features_df['active_days'].max()) * w_activity
    )
    raw = np.log1p(raw * 5)
    scaler = MinMaxScaler((0, 1000))
    features_df['credit_score'] = scaler.fit_transform(raw.values.reshape(-1, 1))
    return features_df[['wallet', 'credit_score']]

def plot_distribution(df, out_path):
    df = df.copy()
    df['range'] = pd.cut(df['credit_score'], bins=np.arange(0, 1100, 100))
    df['range'].value_counts().sort_index().plot.bar(figsize=(10, 5))
    plt.title('Wallet Credit Score Distribution')
    plt.xlabel('Score Range')
    plt.ylabel('Wallet Count')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    print("✓ Plot saved:", out_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to input JSON file')
    parser.add_argument('--output', required=True, help='Path to save output CSV')
    args = parser.parse_args()

    print("⏳ Loading data...")
    df = load_and_prepare(args.input)

    print("⚙️  Engineering features...")
    features_df = engineer_features(df)

    print("📊 Computing scores...")
    scored_df = compute_scores(features_df)

    print("💾 Saving CSV...")
    scored_df.to_csv(args.output, index=False)
    print("✅ CSV saved:", args.output)

    print("📈 Saving plot...")
    plot_path = str(pathlib.Path(args.output).with_suffix('.png'))
    plot_distribution(scored_df, plot_path)
