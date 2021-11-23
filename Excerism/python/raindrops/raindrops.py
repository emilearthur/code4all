def convert(number):
    _factor = {3: 'Pling', 5: 'Plang', 7: 'Plong'}
    output = []

    for key, value in _factor.items():
        if number % key == 0:
            output.append(value)

    # output = ''.join([str(_n) for _n in output if _n])

    return ''.join([str(_n) for _n in output if _n]) if output else str(number)
