import db
import time
import schedule
import json
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def job():
    save_knowledge()
    schedule.every(1).minute.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

def save_knowledge():
    tokens = "bitcoin,ethereum,stargaze,osmosis,cosmos,terrausd,terra-luna-2,ripple,uniswap,solana,the-sandbox,thorchain,near,mirror-protocol,decentraland,chainlink,internet-computer,polkadot,dogecoin,pancakeswap-token,binancecoin,avalanche-2,arweave,cardano"
    listKnowledge = cg.get_coins_markets(ids=tokens, vs_currency='usd', order='market_cap_desc', price_change_percentage='24h')
    print("do call")
    for knowledge in listKnowledge:
        jKnowledge = json.dumps(knowledge)
        db.log_knowledge(jKnowledge)

if __name__ == "__main__":
    job()