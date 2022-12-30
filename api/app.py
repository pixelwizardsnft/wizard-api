import sqlite3
#import knowledge
from flask import Flask, request, jsonify
from flask_cors import CORS

def connect_to_db():
    con = sqlite3.connect('api/tokenKnowledge.db')
    print("connected")
    return con

def get_all_knowledge():
    allknowledge = []
    try:
        con = connect_to_db()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM TokenKnowledge")
        rows = cur.fetchall()

        for i in rows:
            knowledge = {}
            knowledge["symbol"] = i["Symbol"]
            knowledge["price"] = i["Price"]
            knowledge["priceHigh"] = i["PriceHigh"]
            knowledge["priceLow"] = i["PriceLow"]
            knowledge["changePer"] = i["ChangePer"]
            knowledge["timestamp"] = i["Timestamp"]
            allknowledge.append(knowledge)
    except:
        allknowledge = []
    
    return allknowledge

def get_knowledge_by_token(token):
    knowledge = {}
    try:
        con = connect_to_db()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM TokenKnowledge WHERE symbol =?", (token,))
        row = cur.fetchone()

        knowledge = {}
        knowledge["symbol"] = row["Symbol"]
        knowledge["price"] = row["Price"]
        knowledge["priceHigh"] = row["PriceHigh"]
        knowledge["priceLow"] = row["PriceLow"]
        knowledge["changePer"] = row["ChangePer"]
        knowledge["timestamp"] = row["Timestamp"]    
    except:
        knowledge = {}
    
    return knowledge

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return 'Welcome to the Pixel Wizard "Book of Knowledge"!'

@app.route('/api/knowledge', methods=['GET'])
def api_get_all_knowledge():
    return jsonify(get_all_knowledge())

@app.route('/api/knowledge/<token>', methods=['GET'])
def api_get_knowledge(token):
    return jsonify(get_knowledge_by_token(token))