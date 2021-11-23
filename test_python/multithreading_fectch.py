import time
import requests
from typing import Tuple

SYMBOLS: Tuple[str] = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')
BASES: Tuple[str] = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')

def fetch_rate(base: str):
    """Fetches value from vatcomply api
    Args:
        base (str): currency
    """
    try:
        response = requests.get(f"https://api.vatcomply.com/rates?base={base}")
        response.raise_for_status
        rates = response.json().get("rates")
        
        rates[base] = 1.
        
        rates_line = ", ".join([f"{rates[symbol]:7.03}" for symbol in SYMBOLS])
        print(f"1 {base} = {rates_line}")
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    

def main():
    for base in BASES:
        fetch_rate(base)

if __name__ == "__main__":
    started = time.time()
    main()
    elapsed = time.time() - started
    
    print()
    print("time elapsed: {:.2f}s".format(elapsed))
