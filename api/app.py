from decouple import config
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import urllib.parse as up
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
DATABASE_URL = config('DATABASE_URL')

### BASE FUNCTIONS
def connect_to_db():
    con = None
    up.uses_netloc.append("postgres")
    url = up.urlparse(DATABASE_URL)
    con = psycopg2.connect(database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return con

def save_knowledge():
    tokens = "bitcoin,ethereum,stargaze,osmosis,cosmos,terrausd,terra-luna-2,ripple,uniswap,solana,the-sandbox,thorchain,near,mirror-protocol,decentraland,chainlink,internet-computer,polkadot,dogecoin,pancakeswap-token,binancecoin,avalanche-2,arweave,cardano"
    listKnowledge = cg.get_coins_markets(ids=tokens, vs_currency='usd', order='market_cap_desc', price_change_percentage='24h')
    con = connect_to_db()

    for knowledge in listKnowledge:
        log_knowledge(knowledge, con)
    
    con.close()


def log_knowledge(message, con):
    
    symbol = "'"+message["symbol"].upper()+"'"
    price = float(message["current_price"])
    priceHigh = float(message["high_24h"])
    priceLow = float(message["low_24h"])
    changePer = float(message["price_change_percentage_24h"])
    time = "'"+message["last_updated"]+"'"

    try:
        #con = connect_to_db()
        cur = con.cursor()
        cur.execute(f'''INSERT INTO tokenknowledge (symbol, price, pricehigh, pricelow, changeper, lastupdated) 
                        VALUES ({symbol}, {price}, {priceHigh}, {priceLow}, {changePer}, {time}) 
                        ON CONFLICT (symbol)
                        DO 
                            UPDATE SET symbol={symbol}, price={price}, pricehigh={priceHigh}, pricelow={priceLow}, changeper={changePer}, lastupdated={time}''')
        print("Updated: " + symbol)
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

### API FUNCTIONS
def get_all_knowledge():
    allknowledge = []
    try:
        con = connect_to_db()
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM tokenknowledge")
        rows = cur.fetchall()

        for i in rows:
            knowledge = {}
            knowledge["symbol"] = i["symbol"]
            knowledge["price"] = i["price"]
            knowledge["priceHigh"] = i["pricehigh"]
            knowledge["priceLow"] = i["pricelow"]
            knowledge["changePer"] = i["changeper"]
            knowledge["timestamp"] = i["lastupdated"]
            allknowledge.append(knowledge)
    except:
        allknowledge = []
    
    return allknowledge

def get_knowledge_by_token(token):
    knowledge = {}
    try:
        con = connect_to_db()
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f"SELECT * FROM tokenknowledge WHERE symbol ='{token}'")
        row = cur.fetchone()

        knowledge = {}
        knowledge["symbol"] = row["symbol"]
        knowledge["price"] = row["price"]
        knowledge["priceHigh"] = row["pricehigh"]
        knowledge["priceLow"] = row["pricelow"]
        knowledge["changePer"] = row["changeper"]
        knowledge["timestamp"] = row["lastupdated"]
    except:
        knowledge = {}
    
    return knowledge

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return 'Welcome to the Pixel Wizard "Book of Knowledge"!'

@app.route('/api/v1/knowledge', methods=['GET'])
def api_get_all_knowledge():
    return jsonify(get_all_knowledge())

@app.route('/api/v1/knowledge/<token>', methods=['GET'])
def api_get_knowledge(token):
    return jsonify(get_knowledge_by_token(token))

@app.route('/api/v1/updateKnowledge', methods=['GET', 'POST'])
def api_update_knowledge():
    save_knowledge()
    return 'OK', 200