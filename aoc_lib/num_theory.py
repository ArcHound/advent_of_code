import logging
import math

log = logging.getLogger("aoc_logger")


def is_prime_simple(n: int):
    """simple check if n is prime by dividing by numbers up to the square root"""
    ip = True
    if n in [2, 3]:
        return ip
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            ip = False
            break
    return ip


def primes_under_n(n):
    """Erastothenes sieve for generating primes under number n"""
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
    """Naive factorization by dividing with primes up to the n"""
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
    """sum of divisors of number n"""
    factorization = factorize(n, in_primes)
    total = 1
    for prime, exponent in factorization.items():
        total *= (pow(prime, exponent + 1) - 1) // (prime - 1)
    return total


def egcd(a, b):
    """Extended GCD for a,b. Returns gcd, (s,t) where sa+tb = gcd(a,b)"""
    old_r = max((a, b))
    r = min((a, b))
    old_s = 1
    s = 0
    old_t = 0
    t = 1
    while r != 0:
        q = old_r // r
        swap = r
        r = old_r - q * r
        old_r = swap
        swap = s
        s = old_s - q * s
        old_s = swap
        swap = t
        t = old_t - q * t
        old_t = swap
    if a < b:
        return (old_r, (old_t, old_s))
    else:
        return (old_r, (old_s, old_t))


def mod_inv(a, n):
    """modular inverse of a (mod n) or ValueError if not coprime"""
    gcd, coefs = egcd(a, n)
    if gcd != 1:
        raise ValueError(f"{a} and {n} are not coprime!")
    else:
        return coefs[0] % n


def tuple_crt(c1, c2):
    """finds x for (a_1, n_1) and (a_2, n_2) such that x = a_1 (mod n_1), x = a_2 (mod n_2) and 0<=x<=n_1*n_2 if n_1 and n_2 are coprime (else ValueError)"""
    a1, n1 = c1
    a2, n2 = c2
    gcd, coefs = egcd(n1, n2)
    if gcd != 1:
        raise ValueError(f"{n1} and {n2} are not coprime!")
    else:
        return (a1 * coefs[1] * n2 + a2 * coefs[0] * n1) % (n1 * n2)


def iterative_crt(l):
    """finds x for (a_1, n_1), ... (a_k,n_k) such that x = a_1 (mod n_1), ... x = a_k (mod n_k) and 0<=x<=prod(n_1... n_k) if n_1 to n_k are coprime (else ValueError)"""
    worklist = sorted(l, key=lambda x: x[1])
    while len(worklist) > 1:
        c1 = worklist[0]
        c2 = worklist[1]
        new_n = c1[1] * c2[1]
        new_a = tuple_crt(c1, c2)  # if this throws, we throwing up
        worklist = sorted(worklist[2:] + [(new_a, new_n)], key=lambda x: x[1])
    return worklist[0][0]
