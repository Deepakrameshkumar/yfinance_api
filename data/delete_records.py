#delete all records from fund_holdings table
import sqlite3

conn = sqlite3.connect('data/database.db')
c = conn.cursor()
c.execute("DELETE FROM fund_holdings")
conn.commit()
conn.close()