ALPHABET = [i for i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]


def bijective_encode(i):
    if i == 0:
        return ALPHABET[0]
    s = ''
    base = len(ALPHABET)
    while i > 0:
        s += ALPHABET[i % base]
        i /= base
        i = int(i)

    return s[::-1]
