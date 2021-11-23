
from threading import Lock
import time
import time
import requests
from typing import Tuple, Dict
from threading import Thread
from queue import Queue, Empty
import random

class Throttle:
    def __init__(self, rate: int) -> None:
        self._consume_lock = Lock()
        self.rate = rate
        self.tokens = 0
        self.last = None

    def consume(self, amount: int = 1):
        with self._consume_lock:
            now = time.time()

            # time measurement is initialized on first and token request to avoid initial bursts
            if self.last is None:
                self.last = now

            elapsed = now - self.last

            # make sure that quant of passed time is big enough to add new tokens.
            if elapsed * self.rate > 1:
                self.tokens += elapsed * self.rate
                self.last = now

            # never over-fill the bucket
            self.tokens = min(self.rate, self.tokens)

            # finally dispatch tokens if available
            if self.tokens >= amount:
                self.tokens -= amount
                return amount 
            return 0


THREAD_POOL_SIZE: int = 6

SYMBOLS: Tuple[str] = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')
BASES: Tuple[str] = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')

def fetch_rate(base: str) -> Tuple[str, Dict[str, float]]:
    """Fetches value from vatcomply api
    Args:
        base (str): currency
    """

    response = requests.get(f"https://api.vatcomply.com/rates?base={base}")
    rand_val = random.randint(0, 5)
    # if rand_val < 1:
    #     # simulate error by overiding status code
    #     response.status_code = 500
    response.raise_for_status()
    
    rates = response.json().get("rates")
    
    rates[base] = 1.
    return (base, rates)


def present_results(base: str, rates: Dict[str, float]):
    rates_line = ", ".join([f"{rates[symbol]:7.03} {symbol}" for symbol in SYMBOLS])
    print(f"1 {base} = {rates_line}")


def worker(work_queue: Queue, results_queue: Queue, throttle: Throttle):
    while True:
        try:
            item = work_queue.get_nowait()
        except Empty:
            break

        while not throttle.consume():
            time.sleep(0.1)

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
    throttle: Throttle = Throttle(10)

    for base in BASES:
        work_queue.put(base)

    threads = [Thread(target=worker, args=(work_queue, results_queue, throttle)) for  _ in range(THREAD_POOL_SIZE)]
    for thread in threads:
        thread.start()
    
    work_queue.join()

    while threads:
        threads.pop().join()

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
