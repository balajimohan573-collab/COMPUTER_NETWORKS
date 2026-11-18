"""Hamming(7,4) code: correct a single-bit error in a 4-bit sensor reading.
Task 8 – Complete the Code
CSA07 – Computer Networks – Assignment 1
"""


def encode(d):
    # d = [d1, d2, d3, d4]
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]  # positions 1..7


def decode(c):
    # Compute the syndrome bits
    # s1 (positions 1,3,5,7), s2 (2,3,6,7) and s3 (4,5,6,7)
    # pos = s1 + 2*s2 + 4*s3
    # If pos is not 0, flip bit pos (index pos-1)
    # Return pos and the data bits at positions 3, 5, 6, 7
    s1 = c[0] ^ c[2] ^ c[4] ^ c[6]
    s2 = c[1] ^ c[2] ^ c[5] ^ c[6]
    s3 = c[3] ^ c[4] ^ c[5] ^ c[6]
    pos = s1 + 2 * s2 + 4 * s3
    if pos != 0:
        c = c[:]               # work on a copy
        c[pos - 1] ^= 1
    data = [c[2], c[4], c[5], c[6]]
    return pos, data


if __name__ == "__main__":
    word = encode([1, 0, 1, 1])
    print("codeword   :", "".join(map(str, word)))

    for flip in (None, 5):
        rx = word[:]
        if flip:
            rx[flip - 1] ^= 1
        pos, data = decode(rx)
        print(f"error at {str(flip):<4}: syndrome {pos}, data {''.join(map(str, data))}")

    # Demonstrate that two-bit errors produce incorrect "correction"
    print("\n----- Two-bit error demonstration -----")
    rx2 = word[:]
    rx2[2] ^= 1   # flip position 3
    rx2[4] ^= 1   # flip position 5
    pos, data = decode(rx2)
    print(f"two flips (pos 3 & 5): syndrome {pos}, recovered data {''.join(map(str, data))}")
    print("(Notice the decoder 'corrects' the wrong bit – Hamming(7,4) only handles single errors.)")
