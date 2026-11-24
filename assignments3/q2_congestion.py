"""TCP congestion window over 20 round trips: slow start, avoidance and loss."""
def simulate(losses, ssthresh=16, reno=True):
    cwnd, trace = 1, []
    for rtt in range(1, 21):
        trace.append(cwnd)
        # TODO 1: If this RTT is in losses: set ssthresh = max(cwnd // 2, 2) and set
        #   cwnd to ssthresh (Reno, fast recovery) or to 1 (Tahoe). Otherwise double
        #   cwnd in slow start (cwnd < ssthresh, capped at ssthresh) or add 1 in
        #   congestion avoidance
        if rtt in losses:
            ssthresh = max(cwnd // 2, 2)
            if reno:
                cwnd = ssthresh  # Reno: fast recovery
            else:
                cwnd = 1  # Tahoe
        else:
            if cwnd < ssthresh:
                cwnd = min(cwnd * 2, ssthresh)
            else:
                cwnd += 1
    return trace
for label, reno in (("Reno ", True), ("Tahoe", False)):
    tr = simulate({8, 14}, reno=reno)
    print(label, " ".join(f"{w:2d}" for w in tr), f"| segments sent {sum(tr)}")
