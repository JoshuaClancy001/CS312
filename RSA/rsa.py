import random
import sys

# This may come in handy...
from fermat import miller_rabin
from fermat import fermat

# If you use a recursive implementation of `mod_exp` or extended-euclid,
# you recurse once for every bit in the number.
# If your number is more than 1000 bits, you'll exceed python's recursion limit.
# Here we raise the limit so the tests can run without any issue.
# Can you implement `mod_exp` and extended-euclid without recursion?
sys.setrecursionlimit(4000)

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


# Implement this function
def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    if a < b:        # constant
        a, b = b, a  # constant
    if b == 0:
        return 1, 0, a
    x, y, d = ext_euclid(b, a % b) # O(n^2) + constant = O(n^2)
    return y, x - (a // b) * y, d  # O(n^2) + O(n) + constant = O(n^2)
    # the recursion makes the O(n^2) work happen O(n) times making the time complexity O(n^3)

# Implement this function
def generate_large_prime(bits=512) -> int:
    is_prime: bool = False
    x: int = 0
    while not is_prime:  # O(n)
        x = random.getrandbits(bits)  # O(1)
        if miller_rabin(x, 100) == "prime": # O(n^4)
            return x

# Implement this function
def generate_key_pairs(bits: int) -> tuple[int, int, int]:
    p: int = generate_large_prime(bits) # O(n^5)
    q: int = generate_large_prime(bits) # O(n^5)
    N: int = p * q  # O(n^2) for multiplying n bit numbers
    e: int = 0

    for num in primes:
        x, y, z = ext_euclid((p-1)*(q-1), num)  # O(n^3)
        if z == 1:
            e = num
            break
    if y < 0:
        y += (p-1)*(q-1)  # O(n^2 + O(1) for multiplying n bit numbers and adding

    return N, e, y
