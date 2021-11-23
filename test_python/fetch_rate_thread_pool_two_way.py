# two way queues.
import time
import requests
from typing import Tuple, Dict
from threading import Thread
from queue import Queue, Empty

THREAD_POOL_SIZE: int = 6

SYMBOLS: Tuple[str] = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')
BASES: Tuple[str] = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')

def fetch_rate(base: str) -> Tuple[str, Dict[str, float]]:
    """Fetches value from vatcomply api
    Args:
        base (str): currency
    """
    try:
        response = requests.get(f"https://api.vatcomply.com/rates?base={base}")
        response.raise_for_status()
        rates = response.json().get("rates")
        
        rates[base] = 1.
        return (base, rates)

    except requests.exceptions.RequestException as err:
        raise SystemExit(err)


def present_results(base: str, rates: Dict[str, float]):
    rates_line = ", ".join([f"{rates[symbol]:7.03} {symbol}" for symbol in SYMBOLS])
    print(f"1 {base} = {rates_line}")


def worker(work_queue: Queue, results_queue: Queue):
    while not work_queue.empty():
        try:
            item = work_queue.get_nowait()
        except Empty:
            break
        else:
            results_queue.put(fetch_rate(item))
            work_queue.task_done()


def main():
    work_queue: Queue = Queue()
    result_queue: Queue = Queue()

    for base in BASES:
        work_queue.put(base)

    threads = [Thread(target=worker, args=(work_queue, result_queue)) for  _ in range(THREAD_POOL_SIZE)]
    for thread in threads:
        thread.start()
    
    work_queue.join()

    while threads:
        threads.pop().join()

    while not result_queue.empty():
        present_results(*result_queue.get())

if __name__ == "__main__":
    started = time.time()
    main()
    elapsed = time.time() - started
    
    print()
    print("time elapsed: {:.2f}s".format(elapsed))
