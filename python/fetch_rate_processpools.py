
from time import time
from multiprocessing import Pool

import requests
from typing import List, Tuple, Dict

SYMBOLS : Tuple[str] = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')
BASES: Tuple[str] = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')

POOL_SIZE : int = 4

def fetch_rate(base: str) -> Tuple[str, Dict[str, float]]:
    response = requests.get(f"https://api.vatcomply.com/rates?base={base}")
    rates = response.json()["rates"]
    
    rates[base] = 1
    return base, rates

def present_results(base: str, rates: Dict[str, float]) -> None:
    rates_line = ", ".join([f"{rates[symbol]:7.03} {symbol}" for symbol in SYMBOLS])
    print(f"1 {base} = {rates_line}")

def main():
    with Pool(POOL_SIZE) as pool:
        results = pool.map(fetch_rate, BASES)
    
    for result in results:
        print(*result)

if __name__ == "__main__":
    started: time = time()
    main()
    elapsed: time = time() - started

    print()
    print("time elapsed: {:.2f}s".format(elapsed))
