"""Nyquist and Shannon limits for the transmission media proposed for a campus.
Task 4 – Complete the Code
CSA07 – Computer Networks – Assignment 1
"""

import math


def nyquist(bandwidth_hz, levels):
    # Return the Nyquist maximum bit rate for a noiseless channel:
    # 2 * bandwidth * log2(levels)
    return 2 * bandwidth_hz * math.log2(levels)


def shannon(bandwidth_hz, snr_db):
    # Convert the SNR from decibels to a ratio (10 ** (dB / 10))
    # and return the Shannon capacity: bandwidth * log2(1 + SNR)
    snr = 10 ** (snr_db / 10.0)
    return bandwidth_hz * math.log2(1 + snr)


if __name__ == "__main__":
    media = [("Telephone line", 3_100, 30),
             ("Cat6 pair", 250e6, 40),
             ("Wi-Fi 6 channel", 160e6, 25)]

    for name, bw, snr in media:
        print(f"{name:<16} Shannon limit {shannon(bw, snr) / 1e6:10.2f} Mbps")

    print(f"Nyquist, 3,100 Hz with 4 levels: {nyquist(3_100, 4) / 1e3:.1f} kbps")

    # Extra calculation required by the task:
    # Find the SNR (in dB) a 3,100 Hz telephone line would need to carry 56 kbps
    target_bps = 56_000
    bw = 3_100
    # target_bps = bw * log2(1 + snr)  =>  snr = 2**(target/bw) - 1
    snr_linear = 2 ** (target_bps / bw) - 1
    snr_db = 10 * math.log10(snr_linear)
    print(f"\nSNR needed for 56 kbps on 3100 Hz line: {snr_db:.1f} dB")
    print("(Typical telephone-line SNR is only 30-40 dB, so 56 kbps is unrealistic.)")
