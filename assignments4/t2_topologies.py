"""Compare topologies for n offices: links, ports and single-link failures."""
from itertools import combinations
from collections import deque

def links(kind, n):
    nodes = list(range(n))
    if kind == "bus":
        return [(i, i + 1) for i in range(n - 1)]
    if kind == "ring":
        return [(i, (i + 1) % n) for i in range(n)]
    if kind == "star":
        return [("hub", i) for i in nodes]
    if kind == "mesh":
        return list(combinations(nodes, 2))
    raise ValueError(kind)

def connected_after_failure(edges, n, broken):
    # TODO 1 completed: Remove broken link, BFS from office 0
    remaining = [e for e in edges if e != broken and e != (broken[1], broken[0])]
    adj = {}
    for a, b in remaining:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    visited = set()
    q = deque([0])
    visited.add(0)
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in visited:
                visited.add(v)
                q.append(v)
    return set(range(n)).issubset(visited)

n = 6
for kind in ("bus", "ring", "star", "mesh"):
    e = links(kind, n)
    ports = max(sum(1 for a, b in e if x in (a, b)) for x in set(sum(e, ())))
    ok = sum(connected_after_failure(e, n, b) for b in e)
    print(f"{kind:<5} links {len(e):2d}  max ports on one device {ports}  "
          f"single-link failures survived {ok}/{len(e)}")
