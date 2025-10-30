import yfinance as yf

funds_data = yf.Ticker('QQQ').funds_data

print(funds_data)

#save to json
import json
with open('funds_data.json', 'w') as f:
    # Build a JSON-serializable dict from the FundsData object using
    # its public accessors. Use default=str to safely convert non-JSON
    # native types (e.g. numpy/pandas types) to strings if necessary.
    data = {
        "quote_type": funds_data.quote_type(),
        "description": funds_data.description,
        "fund_overview": funds_data.fund_overview,
        "fund_operations": None if funds_data.fund_operations is None else funds_data.fund_operations.to_dict(),
        "asset_classes": funds_data.asset_classes,
        "top_holdings": None if funds_data.top_holdings is None else funds_data.top_holdings.to_dict(),
        "equity_holdings": None if funds_data.equity_holdings is None else funds_data.equity_holdings.to_dict(),
        "bond_holdings": None if funds_data.bond_holdings is None else funds_data.bond_holdings.to_dict(),
        "bond_ratings": funds_data.bond_ratings,
        "sector_weightings": funds_data.sector_weightings,
    }

    json.dump(data, f, indent=4, default=str)
#spy.description