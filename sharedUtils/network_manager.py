import network, time, socket

def setup_wlan(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(0.5)
    return wlan

def cleanup_port(port=80):
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

def start_server(port=80, reuse_addr=True):
    cleanup_port(port)

    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
    s = socket.socket()

    if reuse_addr:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            pass

    s.bind(addr)
    s.listen(1)
    return s, addr