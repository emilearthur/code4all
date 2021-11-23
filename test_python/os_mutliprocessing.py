from multiprocessing import Process
import os

def work(identifier: int):
    print(f"Hey, I am the process, {identifier}, pid {os.getpid()} \n")

def main():
    processes = [Process(target=work, args=(number,)) for number in range(10)]
    for process in processes:
        process.start()

    while processes:
        processes.pop().join()

if __name__ == "__main__":
    main()
