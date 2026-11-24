"""Network performance metrics from a captured packet trace (e.g. from Wireshark)."""
# (sequence number, send time in ms, receive time in ms or None if lost, size in bytes)
TRACE = [(1, 0, 42, 1200), (2, 20, 61, 1200), (3, 40, 85, 1200),
         (4, 60, None, 1200), (5, 80, 119, 1200), (6, 100, 146, 1200),
         (7, 120, 158, 1200), (8, 140, 190, 1200), (9, 160, None, 1200),
         (10, 180, 222, 1200)]
def metrics(trace):
    got = [(s, tx, rx, b) for s, tx, rx, b in trace if rx is not None]
    # TODO 1: Compute loss %, avg one-way delay, jitter, throughput kbps
    total = len(trace)
    lost = total - len(got)
    loss = (lost / total) * 100
    delays = [rx - tx for s, tx, rx, b in got]
    avg_delay = sum(delays) / len(delays)
    jitter = 0.0
    if len(delays) > 1:
        diffs = [abs(delays[i] - delays[i-1]) for i in range(1, len(delays))]
        jitter = sum(diffs) / len(diffs)
    first_tx = min(tx for s, tx, rx, b in got)
    last_rx = max(rx for s, tx, rx, b in got)
    bits = sum(b for s, tx, rx, b in got) * 8
    duration_ms = last_rx - first_tx
    throughput = bits / duration_ms   # kbps (bits per ms = kbps)
    return loss, avg_delay, jitter, throughput
loss, d, j, thr = metrics(TRACE)
print(f"packet loss {loss:.1f} %")
print(f"average delay {d:.1f} ms, jitter {j:.1f} ms")
print(f"throughput {thr:.1f} kbps")
print("VoIP quality:", "acceptable" if d < 150 and j < 30 and loss < 1 else "poor")
