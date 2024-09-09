def any_in_list(l: list, condition):
    for item in l:
        if condition(item):
            return item

    return None


def print_bitboard(b):
    out = str(bin(b))[2:]
    out = "0" * (64 - len(out)) + out
    for i, c in enumerate(out):
        print(c, end="\n" if i % 8 == 7 else "")


def square_to_index(x: int, y: int) -> int:
    return 63 - (x + y * 8)

def index_to_square(i: int):
    return (63-i) % 8, (63-i)//8