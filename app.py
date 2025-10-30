import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
from flask import Flask


#spy.description
#spy.equity_holdings

#print("Description:", spy.description)

def get_fund_data(ticker):
    
    funds_data = yf.Ticker(ticker).funds_data
    top_holdings = funds_data.top_holdings

    # make it a df

    top_holdings = pd.DataFrame(top_holdings)
    #sort by weight
    top_holdings = top_holdings.sort_values(by='Holding Percent', ascending=False)

    #add rank column
    top_holdings['Rank'] = range(1, len(top_holdings) + 1)

    #add date column as yesterday's date
    yesterday = datetime.now() - timedelta(1)
    top_holdings['Date'] = yesterday.strftime('%Y-%m-%d')
    top_holdings['ticker'] = ticker
    return top_holdings

def save_to_db(df):
    

    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()

    # Create table if it doesn't exist with the desired schema (include Symbol column).
    c.execute('''CREATE TABLE IF NOT EXISTS fund_holdings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, Symbol TEXT, Rank INTEGER, Date TEXT, Name TEXT, ticker TEXT, 'Holding Percent' REAL)''')

    # Insert rows. Do not explicitly insert into the `id` primary key column so SQLite can manage it.
    for index, row in df.iterrows():
        # index is the Symbol when the DataFrame is indexed by Symbol
        symbol = index
        c.execute("INSERT INTO fund_holdings (Symbol, Rank, Date, Name, ticker, 'Holding Percent') VALUES (?, ?, ?, ?, ?, ?)",
                  (symbol, int(row['Rank']), row['Date'], row['Name'], row['ticker'], float(row['Holding Percent'])))

    #update last_updated timestamp in funds table
    c.execute("UPDATE funds SET last_updated = ? WHERE ticker = ?", (datetime.now(), df['ticker'].iloc[0]))
    
    conn.commit()
    conn.close()

    #ticker = 'XLK'
    # get the list of tickers from data/database.db from funds table


def fetch_all_and_save():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("SELECT ticker FROM funds")
    tickers = c.fetchall()
    conn.close()
    
    for ticker in tickers:
        ticker = ticker[0]
        print(f"fetching for {ticker}")
        df = get_fund_data(ticker)
        #print column names of the df
        #print(df.columns)
        #print(df.head())
        save_to_db(df)
        #print progress
        print(f"Fund data for {ticker} saved to database.")
    return "All fund data fetched and saved."



app = Flask(__name__)

@app.route('/fetch_fund_data', methods=['GET'])
def fetch_fund_data_endpoint():
    fetch_all_and_save()
    return "Fund data fetched and saved."

#approute to run sql query

@app.test_conn('/test', methods=['GET'])
def test_conn():
    return "sucessfully connected with the flask container"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)