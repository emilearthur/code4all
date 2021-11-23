def reverse(text):
    return "".join([text[i-1] for i in range(len(text), 0, -1)])
