import json
import yfinance as yf


SUB_SECTOR_LABELS = {
    "ai_compute_merchant_silicon":   "Merchant Silicon",
    "ai_compute_custom_silicon":     "Custom Silicon",
    "ai_compute_foundry":            "Foundry",
    "ai_networking":                 "Networking",
    "ai_data_center_infrastructure": "DC Infrastructure",
    "ai_data_center_reit":           "DC REIT",
    "ai_data_infrastructure":        "Data Infra",
    "ai_enterprise_applications":    "Enterprise Apps",
    "ai_neocloud":                   "Neocloud",
}


def load_holdings(filepath):
    """Load coverage universe from holdings.json. Returns the positions list."""
    with open(filepath) as f:
        data = json.load(f)
    if data.get("schema_version") != 2:
        raise ValueError(f"Unsupported schema_version: {data.get('schema_version')}. Expected 2.")
    return data["positions"]


def fetch_market_data(positions):
    """
    Fetch historical daily closes for each covered name, starting from
    each position's coverage_start_date.

    Returns a dict mapping ticker -> DataFrame (None if fetch failed).
    """
    market_data = {}
    for position in positions:
        ticker = position["ticker"]
        start_date = position["coverage_start_date"]
        try:
            df = yf.Ticker(ticker).history(start=start_date)
            market_data[ticker] = df
        except Exception:
            print(f"WARNING: Could not fetch data for {ticker} — skipping.")
            market_data[ticker] = None
    return market_data


def compute_returns(df):
    """
    Compute 1d, 5d, 30d, and since-coverage returns from a price history DataFrame.

    Each window requires a minimum number of rows to compute:
      1d  -> 2 rows   (today vs yesterday)
      5d  -> 6 rows   (today vs 5 trading days ago)
      30d -> 31 rows  (today vs 30 trading days ago)
    Returns None for any window that doesn't have enough data.
    """
    if df is None or len(df) == 0:
        return {
            "current_price": None,
            "return_1d": None,
            "return_5d": None,
            "return_30d": None,
            "return_since_coverage": None,
        }

    closes = df["Close"]
    current_price = closes.iloc[-1]

    def pct(start, end):
        return (end / start - 1) * 100

    return {
        "current_price": current_price,
        "return_1d":             pct(closes.iloc[-2], current_price) if len(closes) >= 2  else None,
        "return_5d":             pct(closes.iloc[-6], current_price) if len(closes) >= 6  else None,
        "return_30d":            pct(closes.iloc[-31], current_price) if len(closes) >= 31 else None,
        "return_since_coverage": pct(closes.iloc[0],  current_price) if len(closes) >= 2  else None,
    }


def print_coverage_table(rows):
    """Print the AI infrastructure coverage universe dashboard."""

    def fmt_pct(val):
        if val is None:
            return "N/A"
        sign = "+" if val >= 0 else ""
        return f"{sign}{val:.1f}%"

    def fmt_price(val):
        if val is None:
            return "N/A"
        return f"${val:.2f}"

    def fmt_direction(val):
        return "neutral" if val == "neutral_monitor" else val

    header = (
        f"{'Ticker':<8}  {'Sub-Sector':<18}  {'Price':>9}  "
        f"{'1d':>8}  {'5d':>8}  {'30d':>8}  {'Since Cov.':>10}  "
        f"{'Depth':<10}  {'Direction':<9}"
    )
    divider = "-" * len(header)

    print()
    print("AI Infrastructure Coverage Universe")
    print(divider)
    print(header)
    print(divider)

    for row in rows:
        sub_sector_label = SUB_SECTOR_LABELS.get(row["sub_sector"], row["sub_sector"])
        print(
            f"{row['ticker']:<8}  "
            f"{sub_sector_label:<18}  "
            f"{fmt_price(row['current_price']):>9}  "
            f"{fmt_pct(row['return_1d']):>8}  "
            f"{fmt_pct(row['return_5d']):>8}  "
            f"{fmt_pct(row['return_30d']):>8}  "
            f"{fmt_pct(row['return_since_coverage']):>10}  "
            f"{row['coverage_depth']:<10}  "
            f"{fmt_direction(row['thesis_direction']):<9}"
        )

    print(divider)
    print()


def main():
    positions = load_holdings("holdings.json")
    market_data = fetch_market_data(positions)

    rows = []
    for position in positions:
        ticker = position["ticker"]
        returns = compute_returns(market_data.get(ticker))
        rows.append({
            "ticker": ticker,
            "sub_sector": position["sub_sector"],
            "coverage_depth": position["coverage_depth"],
            "thesis_direction": position["thesis_direction"],
            **returns,
        })

    print_coverage_table(rows)


if __name__ == "__main__":
    main()
