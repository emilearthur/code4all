def classify(number):
    if number <= 0:
        raise ValueError("number is non negative")

    aliquout_number = [i for i in range(1, number) if number % i == 0]

    if sum(aliquout_number) == number:
        return "perfect"
    elif sum(aliquout_number) > number:
        return "abundant"
    elif sum(aliquout_number) < number:
        return "deficient"
