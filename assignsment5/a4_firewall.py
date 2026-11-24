"""A stateless packet filter: the first matching rule decides (like iptables)."""
RULES = [  # (action, protocol, destination port or None for any, source prefix or None)
    ("allow", "tcp", 443, None),
    ("allow", "tcp", 22, "10.1."),
    ("deny", "tcp", 22, None),
    ("allow", "udp", 53, None),
]
DEFAULT = "deny"
def decide(proto, port, src):
    for action, p, dport, prefix in RULES:
        # TODO 1: A rule matches when its protocol equals proto, its port is None or
        #   equals port, and its prefix is None or src starts with it. Return the action
        #   of the first matching rule
        if p != proto:
            continue
        if dport is not None and dport != port:
            continue
        if prefix is not None and not src.startswith(prefix):
            continue
        return action
    return DEFAULT
packets = [("tcp", 443, "49.37.2.8"), ("tcp", 22, "10.1.4.20"),
           ("tcp", 22, "49.37.2.8"), ("udp", 53, "10.1.4.20"),
           ("tcp", 80, "49.37.2.8"), ("icmp", None, "49.37.2.8")]
for pk in packets:
    print(f"{pk[0]:<5} {str(pk[1]):<5} from {pk[2]:<10} -> {decide(*pk)}")
