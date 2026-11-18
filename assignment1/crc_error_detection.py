"""CRC error detection for frames sent between two switches.
Task 7 – Complete the Code
CSA07 – Computer Networks – Assignment 1
"""


def mod2_div(dividend, divisor):
    """Return the remainder of modulo-2 (XOR) division of two bit strings."""
    rem = list(dividend)
    for i in range(len(dividend) - len(divisor) + 1):
        # If the current leading bit rem[i] is 1, XOR the divisor into rem
        # starting at position i
        if rem[i] == "1":
            for j in range(len(divisor)):
                rem[i + j] = str(int(rem[i + j]) ^ int(divisor[j]))
    return "".join(rem[-(len(divisor) - 1):])


def encode(data, gen):
    crc = mod2_div(data + "0" * (len(gen) - 1), gen)
    return data + crc


def check(frame, gen):
    return set(mod2_div(frame, gen)) == {"0"}


if __name__ == "__main__":
    GEN = "1011"                               # x^3 + x + 1
    frame = encode("1101011011", GEN)
    print("transmitted:", frame)
    print("no error   :", check(frame, GEN))

    # Inject a 1-bit error
    bad = frame[:4] + ("1" if frame[4] == "0" else "0") + frame[5:]
    print("1-bit error:", check(bad, GEN))

    # Inject a 3-bit burst error
    burst = (frame[:2]
             + "".join("1" if b == "0" else "0" for b in frame[2:5])
             + frame[5:])
    print("3-bit burst:", check(burst, GEN))

    # Find an error pattern that generator 1011 cannot detect
    # Any multiple of the generator itself is undetectable.
    # Example: flip bits according to the generator pattern "1011"
    undetectable = list(frame)
    for i, bit in enumerate("1011"):
        if bit == "1":
            pos = i  # flip starting from the beginning
            undetectable[pos] = "1" if undetectable[pos] == "0" else "0"
    undetectable = "".join(undetectable)
    print("\nUndetectable error pattern (multiple of generator):")
    print("original   :", frame)
    print("corrupted  :", undetectable)
    print("check result:", check(undetectable, GEN),
          "(False means detected, True means MISSED)")
