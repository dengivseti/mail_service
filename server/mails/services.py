import random, string


def generate_value(count_symbol=5):
    return "".join([random.choice(string.ascii_lowercase) for i in range(count_symbol)])
