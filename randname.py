#!/usr/bin/env python3

"""
Generate a random word using W. Sheldon Simms' algorithm.

Usage:
  ./randname.py [-n <count>] <dictionary> <min-length> <max-length>

Options:
  -n, --count <count>  Generate <count> words [default: 1].
"""

import collections
import docopt
import random


def build_prob_table(f, ord=ord, lower=str.lower, get=dict.get):
    result = collections.defaultdict(lambda: collections.defaultdict(dict))
    for line in f:
        prev_char = cur_char = 0
        for c in line.strip():
            next_char = ord(lower(c))
            d = result[prev_char][cur_char]
            d[next_char] = get(d, next_char, 0) + 1
            d[-1] = get(d, -1, 0) + 1
            prev_char = cur_char
            cur_char = next_char

        d = result[prev_char][cur_char]
        d[0] = get(d, 0, 0) + 1
        d[-1] = get(d, -1, 0) + 1

    return result


def generate(min_length, max_length, table, randrange=random.randrange):
    result = [0] * max_length
    while True:
        prev_char = cur_char = cur_length = 0
        while True:
            t = table[prev_char][cur_char]
            if not t:
                break
            prob = randrange(t[-1])
            for next_char, value in t.items():
                if next_char != -1:
                    if prob < value:
                        break
                    prob -= value
            else:
                assert False

            if next_char == 0:
                if cur_length >= min_length:
                    return "".join(map(chr, result[:cur_length]))
                elif len(t) == 2:
                    break
            elif cur_length == max_length:
                break
            else:
                result[cur_length] = next_char
                cur_length += 1
                prev_char = cur_char
                cur_char = next_char


def main():
    args = docopt.docopt(__doc__)
    with open(args["<dictionary>"]) as f:
        table = build_prob_table(f)

    min_length = int(args["<min-length>"])
    max_length = int(args["<max-length>"])
    assert table[0][0]
    assert min_length <= max_length
    for i in range(int(args["--count"])):
        print(generate(min_length, max_length, table))


if __name__ == "__main__":
    main()
