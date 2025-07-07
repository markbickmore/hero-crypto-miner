import requests
import os
from datetime import datetime, timedelta

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "TEST1234567890FAKEKEY")

def scan_ethereum_address(address: str, token: str, days: int = 7):
    cutoff = int((datetime.now() - timedelta(days=days)).timestamp())

    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "1":
            return {"status": "error", "message": data.get("message", "No transactions found.")}

        txs = data["result"]
        filtered = []

        for tx in txs:
            if int(tx["timeStamp"]) >= cutoff:
                filtered.append({
                    "hash": tx["hash"],
                    "from": tx["from"],
                    "to": tx["to"],
                    "value": int(tx["value"]) / 1e18,
                    "status": "Success" if tx["isError"] == "0" else "Failed",
                    "timestamp": datetime.fromtimestamp(int(tx["timeStamp"])).isoformat(),
                    "chain": "Ethereum"
                })

        return {"status": "ok", "transactions": filtered[:10]}

    except Exception as e:
        return {"status": "error", "message": str(e)}