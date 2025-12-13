import logging
import math

log = logging.getLogger("aoc_logger")


def primes_under_n(n):
    if n < 2:
        return list()
    elif n == 2:
        return [2]
    sieve = [True for i in range(n + 1)]
    sieve[0] = False
    sieve[1] = False
    pointer = 2
    movement = True
    while movement and pointer < len(sieve):
        movement = False
        prime = sieve[pointer]
        for i in range(pointer * 2, len(sieve), pointer):
            sieve[i] = False
            movement = True
        pointer += 1
        while pointer < len(sieve) and not sieve[pointer]:
            pointer += 1
    return [i for i in range(len(sieve)) if sieve[i]]


def factorize(n, in_primes=None):
    if n == 0:
        return dict()
    if in_primes is None:
        primes = primes_under_n(n)
    else:
        primes = in_primes
    factorization = dict()
    n_copy = n
    for p in primes:
        while n_copy % p == 0:
            if p not in factorization:
                factorization[p] = 0
            factorization[p] += 1
            n_copy = n_copy // p
    if factorization == {}:
        factorization[n] = 1  # is prime then
    return factorization


def sum_of_divisors(n, in_primes=None):
    factorization = factorize(n, in_primes)
    total = 1
    for prime, exponent in factorization.items():
        total *= (pow(prime, exponent + 1) - 1) // (prime - 1)
    return total
