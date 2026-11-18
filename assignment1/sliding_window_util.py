"""Link utilisation of stop-and-wait and sliding-window protocols on different links.
Task 9 – Complete the Code
CSA07 – Computer Networks – Assignment 1
"""


def utilisation(frame_bits, rate_bps, distance_m, window, speed=2e8):
    tx = frame_bits / rate_bps              # transmission time
    prop = distance_m / speed               # propagation time
    # a = prop / tx
    # Utilisation is window / (1 + 2a), but never more than 1.
    # Return the utilisation and a
    a = prop / tx
    u = min(1.0, window / (1 + 2 * a))
    return u, a


if __name__ == "__main__":
    links = [("Campus LAN, 200 m, 1 Gbps", 1e9, 200),
             ("City fibre, 50 km, 1 Gbps", 1e9, 50_000),
             ("Satellite, 36,000 km, 10 Mbps", 10e6, 36_000_000)]

    for name, rate, dist in links:
        u1, a = utilisation(12_000, rate, dist, 1)
        u7, _ = utilisation(12_000, rate, dist, 7)
        u127, _ = utilisation(12_000, rate, dist, 127)
        print(f"{name:<31} a = {a:7.2f}  stop-and-wait {u1:6.1%}  "
              f"W=7 {u7:6.1%}  W=127 {u127:6.1%}")

    # Extra calculation required by the task:
    # Smallest window that gives 100 % utilisation on the satellite link
    _, a_sat = utilisation(12_000, 10e6, 36_000_000, 1)
    w_min = int(1 + 2 * a_sat) + 1          # ceiling
    print(f"\nSmallest window for 100% util on satellite: W = {w_min}")
    u_full, _ = utilisation(12_000, 10e6, 36_000_000, w_min)
    print(f"Utilisation with that window: {u_full:.1%}")
