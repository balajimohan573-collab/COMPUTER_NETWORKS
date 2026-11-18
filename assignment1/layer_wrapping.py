"""How data is wrapped by each layer at the sender and unwrapped at the receiver.
Task 3 – Complete the Code
CSA07 – Computer Networks – Assignment 1
"""

LAYERS = [("Application", "HTTP"), ("Transport", "TCP"), ("Network", "IP"),
          ("Data link", "ETH")]


def send(message):
    pdu = message
    for layer, tag in LAYERS:
        # Wrap pdu with this layer's header "[tag|" and, for the data link layer
        # only, also a trailer "|FCS]"; for other layers close with "]".
        # Print the layer name and the size of the new PDU
        if tag == "ETH":
            pdu = "[" + tag + "|" + pdu + "|FCS]"
        else:
            pdu = "[" + tag + "|" + pdu + "]"
        print(f"{layer}  adds {tag} ->  {len(pdu)} bytes")
    return pdu


def receive(frame):
    pdu = frame
    for layer, tag in reversed(LAYERS):
        head = "[" + tag + "|"
        tail = "|FCS]" if tag == "ETH" else "]"
        assert pdu.startswith(head) and pdu.endswith(tail), f"{layer}: bad header"
        pdu = pdu[len(head):-len(tail)]
    return pdu


if __name__ == "__main__":
    # Original 12-byte message
    frame = send("GET /results")
    print("on the wire:", frame)
    print("delivered  :", receive(frame))
    print(f"overhead   : {len(frame) - len('GET /results')} bytes for 12 bytes of data")

    print("\n----- Same program with a 1400-byte message -----")
    long_msg = "X" * 1400
    frame2 = send(long_msg)
    print("on the wire length:", len(frame2))
    print("delivered length  :", len(receive(frame2)))
    overhead = len(frame2) - 1400
    print(f"overhead   : {overhead} bytes for 1400 bytes of data "
          f"({100 * overhead / len(frame2):.1f} %)")
