import argparse
import random


# This is a convenience function for main(). You don't need to touch it.
def prime_test(N: int, k: int) -> tuple[str, str]:
    return fermat(N, k), miller_rabin(N, k)


# You will need to implement this function and change the return value.
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0:  # constant work       # Time Complexity = O(1)
        return 1  # constant work
    else:
        z: int = mod_exp(x, y // 2, N)  # Time Complexity = O(n^2)
        if y % 2 == 0:
            return (z * z) % N          # Time Complexity = O(n^2) + O(n^2) + c = O(n^2)
        else:
            return (x * (z * z)) % N    # Time Complexity = O(n^2) + O(n^2) + O(n^2) + c = O(n^2) Space Complexity =
        # Recursion means O(logy) steps and at each step O(n^2) work takes place making the final Time complexity O(n^3)
        # Recustion adds O(logy) calls to the stack frame and if y is an n bit number, logy = n so the Space Complexity
        # is O(n)


# You will need to implement this function and change the return value.
def fprobability(k: int) -> float:
    return 1 - (1 / (2 ** k))


# You will need to implement this function and change the return value.
def mprobability(k: int) -> float:
    return 1 - (1 / (4 ** k))


# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low, hi) which gives a random integer between low and
# hi, inclusive.
def fermat(N: int, k: int) -> str:
    for i in range(k):  #     O(k)
        a = random.randint(1, N - 1) # O(1)
        if mod_exp(a, N - 1, N) != 1:  # O(n^3)
            return "composite"
    return "prime"


# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low, hi) which gives a random integer between low and
# hi, inclusive.
def miller_rabin(N: int, k: int) -> str:
    for i in range(k):  # O(k)
        a: int = random.randint(1, N - 1)
        if mod_exp(a, N - 1, N) != 1:  # O(n^3)
            return "composite"
        y = (N - 1) // 2
        while y % 2 == 0:  # O(logN) = O(n)
            result = mod_exp(a, y, N) # O(n^3)
            if result == 1:
                y = y // 2
            elif result != 1:
                if result == N - 1 or result == -1:
                    return "prime"
                else:
                    return "composite"
    return "prime"


def main(number: int, k: int):
    fermat_call, miller_rabin_call = prime_test(number, k)
    fermat_prob = fprobability(k)
    mr_prob = mprobability(k)

    print(f'Is {number} prime?')
    print(f'Fermat: {fermat_call} (prob={fermat_prob})')
    print(f'Miller-Rabin: {miller_rabin_call} (prob={mr_prob})')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    parser.add_argument('k', type=int)
    args = parser.parse_args()
    main(args.number, args.k)
