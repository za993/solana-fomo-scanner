import requests
import time

API = "https://api.dexscreener.com"

def main():
    print("SOLANA FOMO SCANNER STARTED")
    print("TEST MODE - NO REAL TRADES")

    while True:
        try:
            url = API + "/token-profiles/latest/v1"
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            tokens = response.json()

            for token in tokens[:10]:
                if token.get("chainId") == "solana":
                    address = token.get("tokenAddress")
                    print("New Solana token:", address)

                    try:
                        result = requests.get(
                            API + "/latest/dex/tokens/" + address,
                            timeout=20
                        )
                        result.raise_for_status()
                        pairs = result.json().get("pairs") or []

                        for pair in pairs:
                            liquidity = float(
                                (pair.get("liquidity") or {}).get("usd") or 0
                            )
                            volume = float(
                                (pair.get("volume") or {}).get("h24") or 0
                            )

                            if liquidity >= 10000 and volume >= 5000:
                                print("POTENTIAL CANDIDATE")
                                print("Liquidity:", liquidity)
                                print("24h volume:", volume)
                                print("Pair:", pair.get("url"))
                    except requests.RequestException as error:
                        print("Token check error:", error)

                    time.sleep(1)

        except Exception as error:
            print("Scanner error:", error)

        print("Next scan in 60 seconds")
        time.sleep(60)


if __name__ == "__main__":
    main()
