import json
import sqlite3
import datetime

def init_db():
    con = sqlite3.connect('tokenKnowledge.db')
    cur = con.cursor()

    cur.execute(''' CREATE TABLE IF NOT EXISTS TokenKnowledge
                    (Symbol text PRIMARY KEY, Price real, PriceHigh real, PriceLow real, ChangePer real, Timestamp text)''')
    con.commit()
    con.close()

def log_knowledge(message):
    parsed = json.loads(message)
    
    symbol = parsed["symbol"].upper()
    price = float(parsed["current_price"])
    priceHigh = float(parsed["high_24h"])
    priceLow = float(parsed["low_24h"])
    changePer = float(parsed["price_change_percentage_24h"])
    time = parsed["last_updated"]

    now = datetime.datetime.now()
    print("log: " + now.strftime("%Y-%m-%d %H:%M:%S"))
    #print("Symbol: " + symbol)
    #print("Price: " + str(price))
    #print("24h%: " + str(changePer))
    #print("Time: " + str(time))

    row = (symbol, price, priceHigh, priceLow, changePer, time)
    con = sqlite3.connect('tokenKnowledge.db')
    cur = con.cursor()
    cmd = "INSERT OR REPLACE INTO TokenKnowledge (Symbol, Price, PriceHigh, PriceLow, ChangePer, Timestamp) values (?, ?, ?, ?, ?, ?)"
    cur.execute(cmd, row)
    con.commit()
    con.close()