class PhoneNumber:
    def __init__(self, number: str) -> None:
        number_ = ''.join([i for i in number if i.isnumeric()])

        if (len(number_) < 10) or (len(number_) > 11) or ((number_).startswith('0')):
            raise ValueError("Length of number should be 10 or 11")

        if (len(number_) == 11) and not ((number_).startswith('1')):
            raise ValueError("Invalid Number, Digts starts with 1")

        if len(number_) == 10:
            self.number = number_
        else:
            self.number = number_[1: len(number_)+1]

        self.area_code = str(self.number)[:3]
        self.exchange_code = str(self.number)[3:6]
        self.subscriber_code = (self.number)[6:len(self.number)+1]

        if (self.area_code.startswith("0")) or (self.area_code.startswith("1")):
            raise ValueError("Area code cannot start with 0 or 1")
        if (self.exchange_code.startswith("0")) or (self.exchange_code.startswith("1")):
            raise ValueError("Exchange code cannot start with 0 or 1")

    def pretty(self: str) -> str:
        return f"({self.area_code})-{self.exchange_code}-{self.subscriber_code}"
