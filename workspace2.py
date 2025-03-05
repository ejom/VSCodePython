import pandas as pd

def sieve(limit):
    """Generate a list of prime numbers up to 'limit' using the Sieve of Atkin."""
    if limit < 2:
        return []
    
    res = [False] * (limit + 1)
    res[2] = res[3] = True

    for i in range(1, int(limit**0.5) + 1):
        for j in range(1, int(limit**0.5) + 1):
            n = (4 * i * i) + (j * j)
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                res[n] ^= True

            n = (3 * i * i) + (j * j)
            if n <= limit and n % 12 == 7:
                res[n] ^= True

            n = (3 * i * i) - (j * j)
            if i > j and n <= limit and n % 12 == 11:
                res[n] ^= True

    for r in range(5, int(limit**0.5) + 1):
        if res[r]:
            for k in range(r * r, limit + 1, r * r):
                res[k] = False

    return [i for i in range(limit + 1) if res[i]]  # Return list of prime numbers

def pick_prime(primes, min_size=1000):
    """Returns the smallest prime >= min_size, or the largest prime in the list if none exist."""
    for prime in primes:
        if prime >= min_size:
            return prime
    return primes[-1] if primes else None

def hash_function(string, modulus):
    """Implements polynomial rolling hash function."""
    hash_value = 5381
    for char in string:
        hash_value = ((hash_value << 5) + hash_value) ^ ord(char)  # hash * 33 XOR char
    return hash_value % modulus

if __name__ == '__main__':
    primes = sieve(10)  # Generate prime numbers up to 10,000
    modulus = pick_prime(primes, 1000)  # Pick a suitable prime modulus

    test_array = ["alpha", "beta", "gamma", "delta", "epsilon"]

    for string in test_array:
        hash_value = hash_function(string, modulus)
        print(f"Hash of '{string}' is {hash_value}")
