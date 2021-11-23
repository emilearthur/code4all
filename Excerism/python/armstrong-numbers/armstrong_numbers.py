def is_armstrong_number(number):
    len_nums = len(str(number))

    armstrong = [int(i) ** len_nums for i in str(number)]

    if sum(armstrong) == number:
        return True
    return False
