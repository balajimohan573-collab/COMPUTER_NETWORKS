"""Iterative DNS resolution through root, TLD and authoritative servers."""
SERVERS = {
    "root": {"in.": "tld-in", "com.": "tld-com"},
    "tld-in": {"ac.in.": "ns-ac"},
    "tld-com": {"example.com.": "ns-example"},
    "ns-ac": {"simats.ac.in.": "ns-simats"},
    "ns-simats": {"results.simats.ac.in.": "10.20.30.40"},
    "ns-example": {"www.example.com.": "93.184.216.34"},
}
cache = {}
def resolve(name):
    if name in cache:
        return cache[name], 0
    server, queries = "root", 0
    while True:
        queries += 1
        # TODO 1: Look in SERVERS[server] for the longest key that name ends with. If
        #   the value looks like an IP address (it contains a digit), cache it and
        #   return (ip, queries); otherwise continue with that server
        zone = SERVERS[server]
        # Find longest key that name ends with
        matches = [k for k in zone if name.endswith(k)]
        if not matches:
            raise ValueError(f"No match for {name} at {server}")
        longest = max(matches, key=len)
        value = zone[longest]
        if any(c.isdigit() for c in value):  # looks like IP
            cache[name] = value
            return value, queries
        else:
            server = value
for n in ("results.simats.ac.in.", "www.example.com.", "results.simats.ac.in."):
    ip, q = resolve(n)
    print(f"{n:<24} {ip:<15} queries sent: {q}")
