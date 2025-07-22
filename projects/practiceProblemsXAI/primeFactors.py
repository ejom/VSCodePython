"""
Takes an int as input and returns a list of its prime factors from least to greatest. 
Examples:

20
[2, 2, 5]

100
[2, 2, 5, 5]
"""

def primeFactorization(num: int) -> list:
    primeFactors = []
    i = 2
    while i <= num:
        #print(num)
        if num%i == 0:
            primeFactors.append(i)
            #print(i)
            num = int(num/i)
            #print(num)
            i -= 1
        i+=1
    return primeFactors

print(primeFactorization(20))
print(primeFactorization(100))
print(primeFactorization(147))
print(primeFactorization(85731))

