def worker(connection):
    while True:
        instance = connection.recv()
        if instance:
            print(f"CHILD: recv: {instance}")
        if instance is None:
            break

from multiprocessing import Process, Pipe

class CustomClass:
    pass

def main():
    parent_conn, child_conn = Pipe()
    child = Process(target=worker, args=(child_conn,))

    for item in (42, "some string",{"one":1}, CustomClass, None):
        parent_conn.send(item)

    child.start()
    child.join()
    

if __name__ == "__main__":
    main()
