import random

def generate_move(ratio, dart_count):
    return ''.join(
        random.choices('b123456789a', weights=ratio, k=dart_count)
    )
