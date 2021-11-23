import threading


class BankAccount:
    def __init__(self):
        self._balance = 0
        self.__account_state = None
        self._lock = threading.Lock()

    def get_balance(self):
        if self.__account_state is True:
            return self._balance
        else:
            raise ValueError("Account is closed")

    def open(self):
        if self.__account_state:
            raise ValueError("Account is already opened")

        self.__account_state = True

    def deposit(self, amount):
        if self.__account_state is True:
            if not isinstance(amount, (int, float)):
                raise TypeError("amount should be numberic")
            if amount < 0:
                raise ValueError("Deposit cannot be negative")
            with self._lock:
                self._balance += amount
        else:
            raise ValueError("Account is Closed, Cannnot make Deposit")

    def withdraw(self, amount):
        if self.__account_state:
            if not isinstance(amount, (int, float)):
                raise TypeError("amount should be numberic")
            if amount < 0:
                raise ValueError("Deposit cannot be negative")
            if self._balance < amount:
                raise ValueError("Insufficient Funds ")
            with self._lock:
                self._balance -= amount
        else:
            raise ValueError("Account is Closed, Cannnot make Deposit")

    def close(self):
        if not self.__account_state:
            raise ValueError("Cannot is not opended. Open Account First")
        else:
            self.__account_state = False
            self._balance = 0
