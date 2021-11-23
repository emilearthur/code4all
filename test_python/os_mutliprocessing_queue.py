from multiprocessing import Process
import os
import time
import requests
from typing import Tuple, Dict

from queue import Queue, Empty
import random

PROCESS_POOL_SIZE: int = 10

SYMBOLS: Tuple[str] = ('USD', 'EUR')
BASES: Tuple[str] = ('USD', 'EUR')

def fetch_rate(base: str) -> Tuple[str, Dict[str, float]]:
    """Fetches value from vatcomply api
    Args:
        base (str): currency
    """

    response = requests.get(f"https://api.vatcomply.com/rates?base={base}")
    
    response.raise_for_status()
    
    rates = response.json().get("rates")
    
    rates[base] = 1.
    return (base, rates)


def present_results(base: str, rates: Dict[str, float]):
    rates_line = ", ".join([f"{rates[symbol]:7.03} {symbol}" for symbol in SYMBOLS])
    print(f"1 {base} = {rates_line}")


def worker(work_queue: Queue, results_queue: Queue):
    while not work_queue.empty():
        try:
            item = work_queue.get_nowait()
        except Empty:
            break

        try:
            result = fetch_rate(item)
        except Exception as err:
            results_queue.put(err)
        else:
            results_queue.put(result)
        finally:
            work_queue.task_done()


def main():
    work_queue: Queue = Queue()
    results_queue: Queue = Queue()

    for base in BASES:
        work_queue.put(base)

    processes = [Process(target=worker, args=(work_queue, results_queue)) for  _ in range(10)]
    for process in processes:
        process.start()
    
    work_queue.join()

    while processes:
        processes.pop().join()

    while not results_queue.empty():
        result = results_queue.get()
        if isinstance(result, Exception):
            raise result
        present_results(*result)


if __name__ == "__main__":
    started = time.time()
    main()
    elapsed = time.time() - started
    
    print()
    print("time elapsed: {:.2f}s".format(elapsed))
