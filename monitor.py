import json
import yfinance as yf


def load_holdings(filepath):
    """Read holdings.json and return the list of positions."""
    with open(filepath) as f:
        return json.load(f)


def fetch_prices(tickers):
    """Ask yfinance for the current price of each ticker.

    Returns a dict like {"AAPL": 189.50, "TSLA": 245.00}.
    """
    prices = {}
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).fast_info
            prices[ticker] = info.last_price
        except Exception:
            print(f"WARNING: Could not fetch price for {ticker} — check the ticker symbol.")
            prices[ticker] = None
    return prices


def calculate_row(holding, current_price):
    """Compute P/L % and current value for one position.

    current_value is kept internally so calculate_weights() can use it,
    but it is never printed.
    """
    total_cost = holding["shares"] * holding["cost_basis"]
    current_value = holding["shares"] * current_price
    pl_pct = (current_value / total_cost - 1) * 100
    return {
        "ticker": holding["ticker"],
        "current_value": current_value,
        "total_cost": total_cost,
        "pl_pct": pl_pct,
    }


def calculate_weights(rows):
    """Add a weight_pct field to each row (current value / total portfolio value)."""
    total_value = sum(row["current_value"] for row in rows)
    for row in rows:
        row["weight_pct"] = (row["current_value"] / total_value) * 100
    return rows


def print_table(rows):
    """Print a formatted summary table with no dollar amounts or share counts."""
    total_value = sum(row["current_value"] for row in rows)
    total_cost = sum(row["total_cost"] for row in rows)
    total_pl_pct = (total_value / total_cost - 1) * 100

    header = f"{'Ticker':<10}  {'Weight':>8}  {'P/L %':>8}"
    divider = f"{'-'*10}  {'-'*8}  {'-'*8}"

    print(header)
    print(divider)
    for row in rows:
        pl_sign = "+" if row["pl_pct"] >= 0 else ""
        print(
            f"{row['ticker']:<10}  {row['weight_pct']:>7.1f}%  "
            f"{pl_sign}{row['pl_pct']:>7.1f}%"
        )
    print(divider)

    total_sign = "+" if total_pl_pct >= 0 else ""
    print(f"{'TOTAL':<10}  {'100.0%':>8}  {total_sign}{total_pl_pct:>7.1f}%")


def main():
    holdings = load_holdings("holdings.json")
    tickers = [h["ticker"] for h in holdings]
    prices = fetch_prices(tickers)

    rows = [calculate_row(h, prices[h["ticker"]]) for h in holdings if prices[h["ticker"]] is not None]
    rows = calculate_weights(rows)
    print_table(rows)


if __name__ == "__main__":
    main()
