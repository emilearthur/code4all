def slices(series, length):
    # len_series = len(series)
    # series = [i for i in series]

    if length > len(series):
        raise ValueError("length cannot be greater than length of seies ")

    if not series:
        raise ValueError("Series cannot be empty")

    if length <= 0:
        raise ValueError("Length cannot be zero or non negative")

    str_nums = []

    for iter_ndx in range(len(series)):
        out = ""
        for ndx in range(iter_ndx, len(series)):
            out += series[ndx]

            if len(out) == length:
                str_nums.append(out)
                break
    return str_nums


def slices_(series, length):
    if length > len(series):
        raise ValueError("length cannot be greater than length of seies ")

    if not series:
        raise ValueError("Series cannot be empty")

    if length <= 0:
        raise ValueError("Length cannot be zero or non negative")

    return [series[i:i+length] for i in range(len(series) - length + 1)]
