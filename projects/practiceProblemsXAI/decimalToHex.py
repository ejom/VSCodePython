"""
Takes a decimal input and outputs its hexedecimal equivalent as a string rounded to three decimals (concise). 
Example inputs and outputs:
in: 12, -3
out: 0C.000

in: 893, 1
out: 0380

in: -511, 0
out: FE01

in: -12.5, -2
out: F3.80
(Since hex of 12.5 with 2 decimal places is C.80, the twos compliment is thus 3.7F + 0.01 = 3.80)

in: 4.87, -3
out: 04.DEC
"""
def roundHex(val: str, N: int, trim: bool):
    val = list(val)
    val.reverse()
    #rounded digit is at N index of val
    #If ord(val[N-1]) (char to left of rounded) is > 55 ('7')
    if ord(val[N-1]) > 55:
        #Increment rounded digit by 1
        val[N] = chr(ord(val[N])+1)
    #Drop everything to the left of rounded
    #Set the last char of val to 0 (in case of overflow)
    if trim:
        val = val[N:]
    else:
        val[:N] = ['0'] * N
    val.append('0')
    #For each char in val:
    for i, char in enumerate(val):
        #If the char is 'G'
        if char == 'g':
            #Change the char to 0
            val[i] = '0'
            #Increment next char by 1
            val[i+1] = chr(ord(val[i+1])+1)
        #Elif the ord(char) == 58 ('9'+1 = :)
        elif char == ':':
            #Change the char to 'A'
            val[i] = 'a'
    val.reverse()
    return "".join(val)

def twoCompliment(val: str, bits: int, isBase: bool):
    val = list(val)
    for i, char in enumerate(val):
    #f is 102
        if ord(char) < 97:
            #This is a digit, shift to be inline with letters
            char = chr(ord(char)+39)
        #Add 48 to bring the difference to digits
        val[i] = chr(102 - ord(char)+48)
        #Shift back to letter if necessary
        if ord(val[i]) > 57:
            val[i] = chr(ord(val[i])+39)
    val = "".join(val)
    if bits>=-1:
        if isBase:
            sol = hex(int(val, 16)+16**(bits))
        else:
            sol = hex(int(val, 16)+16**(len(val)-1-bits))
            sol = list(sol)
            sol.reverse()
            for i, cha in enumerate(sol):
                if cha == 'f':
                    sol[i] = '0'
                else:
                    break
            sol.reverse()
            sol = "".join(sol)
        sol = sol[2:]
        while len(sol) < len(val):
            sol = f"0{sol}"
        val = sol
    return val

def main(num, N):
    if num < 0:
        isNeg = True
        num *= -1
    else:
        isNeg = False
    num *= 1.0
    #convert decimal to mantissa hex
    mant = num.hex()
    #Save the multiplant exponent (base 2)
    mult = mant[-1]
    #save the decimal of the mantissa
    decM = mant[4:-3]
    #Save how many digits are the decimal
    numPlaces = len(decM)
    #Convert to integer and multilpy by the multiplant
    #val = int(float.fromhex(decM)) * 2**(int(mult))
    val = int(decM, 16) * 2**(int(mult))
    #Convert back to hex
    decHexAdded = hex(val)
    #Split up how much is decimal
    decH = decHexAdded[-numPlaces:]
    #Split up how much is added to the base
    baseHexAdded = decHexAdded[2:-numPlaces]

    #Add the base to mantissa base 1 * mult
    if baseHexAdded:
        baseH = hex(int(baseHexAdded, 16) + 2**(int(mult)))
    else:
        baseH = hex(2**(int(mult)))
    baseH = baseH[2:]

    #Handle negetives
    if isNeg:
        baseH = twoCompliment(baseH, N, True)
        decH = twoCompliment(decH, N*-1 - 1, False)
    #Trim based on N
    if N<0:
        N = len(decH) + N
        decH = roundHex(decH, N, True)
        decH = decH[1:]
        finalHex = f"0{baseH}.{decH}".upper()
    elif N>0:
        baseH = roundHex(baseH, N, False)
        finalHex = baseH.upper()
    #If we round at N=0 we need the first decimal
    else:
        N = 1
        baseH = roundHex(f"{baseH}{decH[0]}", N, True)
        finalHex = baseH.upper()
    
    if isNeg:
        finalHex = f"F{finalHex[1:]}"
    return finalHex

#Testing with examples
testInputs = [[12, -3], [893, 1], [4.87, -3], [4.87, 0], [-511, 0], [-12.5, -2]]
testOutputs = ["0C.000", "0380", "04.DEC", "05", "FE01", "F3.80"]

for input, output in zip(testInputs, testOutputs):
    print(f"Test input: {input}")
    solution = main(input[0], input[1])
    print(f"Actual output: {solution}")
    print(f"Expected output: {output}")
    print(f"Test if outputs match: {solution == output}")
    print()

#Solving user test:
print(f"User test input: {-85.974, -5}")
print("Final answer:")
print(main(-85.974, -5))
"""
in: 12, -3
out: 0C.000

in: 893, 1
out: 0380

in: -511, 0
out: FE01

in: -12.5, -2
out: F3.80
(Since hex of 12.5 with 2 decimal places is C.80, the twos compliment is thus 3.7F + 0.01 = 3.80)

in: 4.87, -3
out: 04.DEC
"""