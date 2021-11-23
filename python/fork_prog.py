import os 

pid_list = []

def main():
    pid_list.append(os.getpid())
    child_pid = os.fork()
    
    if child_pid == 0:
        pid_list.append(os.getpid())
        print()
        print("PRNT: hey I am the child process")
        print(f"PRNT: all the pid I know {pid_list}")
    else:
        pid_list.append(os.getpid())
        print()
        print("PRNT: hey I am the parent process")
        print(f"PRNT: the child pid is {child_pid}")
        print(f"PRNT: all the pid I know {pid_list}")


if __name__=="__main__":
    main()
