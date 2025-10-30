# add a table in database called funds and add ticker, name, description columns, last updated timestamp

import sqlite3

def create_funds_table():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS funds
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, ticker TEXT, name TEXT, description TEXT, last_updated TIMESTAMP)''')
    conn.commit()
    conn.close()

create_funds_table()

# add a list of fund tickers to the table
#IT_funds = ['XLK', 'QQQ', 'VGT', 'IXN', 'SOXX']
#Healthcare_funds = ['XLV', 'VHT', 'IYH', 'IBB', 'XBI']
#Renewable_energy_funds = ['ICLN', 'TAN', 'CNRG', 'GRID', 'FAN']
#Financial_services_funds = ['XLF', 'VFH', 'IAI', 'IXG', 'KCE']
#Infrastructure_funds = ['IGF', 'PAVE', 'IFRA', 'GII', 'NFRA']
#Consumer_staples_funds = ['XLP', 'VDC', 'KXI', 'RHS', 'SPLV']
Real_estate_funds = ['XLRE', 'VNQ', 'SCHH', 'IYR', 'ICF','SPLV']


# add ticker, name and description to the table
def add_fund_to_db(ticker):
    import yfinance as yf
    fund = yf.Ticker(ticker)
    name = fund.info.get('longName', '')
    description = fund.funds_data.description

    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute("INSERT INTO funds (ticker, name, description) VALUES (?, ?, ?)",
              (ticker, name, description))
    conn.commit()
    conn.close()

for ticker in Real_estate_funds:
    add_fund_to_db(ticker)