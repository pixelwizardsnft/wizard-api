from decouple import config
from flask import Flask, request, jsonify, abort, render_template
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import urllib.parse as up
from pycoingecko import CoinGeckoAPI
from functools import wraps

cg = CoinGeckoAPI()
DATABASE_URL = config('DATABASE_URL')
API_KEY = config('API_KEY')

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
    tokens = "bitcoin,ethereum,stargaze,osmosis,cosmos,terrausd,terra-luna-2,ripple,uniswap,solana,the-sandbox,thorchain,near,mirror-protocol,decentraland,chainlink,internet-computer,polkadot,dogecoin,pancakeswap-token,binancecoin,avalanche-2,arweave,cardano,akash-network,algorand,arbitrum,axelar,canto,sentinel,magic,matic-network,mantadao,omniflix-network,fantom,harrypotterobamasonic10in,hedera-hashgraph,immutable-x,injective-protocol,stride,blockstack,kadena,kujira,lido-dao,pepe,render-token,secret,usd-coin,tezos,celestia,dydx"
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
        if symbol == "'ETHDYDX'":
            symbol = "'DYDX'"
            
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

### DECORATORS
def require_apikey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-Api-Key') and request.headers.get('X-Api-Key') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/v1/knowledge', methods=['GET'])
def api_get_all_knowledge():
    return jsonify(get_all_knowledge())

@app.route('/v1/knowledge/<token>', methods=['GET'])
def api_get_knowledge(token):
    return jsonify(get_knowledge_by_token(token))

@app.route('/v1/updateKnowledge', methods=['GET', 'POST'])
@require_apikey
def api_update_knowledge():
    save_knowledge()
    return jsonify(success=True)