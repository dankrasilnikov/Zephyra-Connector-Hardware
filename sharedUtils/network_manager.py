import network, uasyncio as aio
from time import ticks_ms, ticks_diff

async def setup_wlan(ssid: str, password: str, timeout_ms: int = 15_000, *, led=None):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    if not sta.isconnected():
        sta.connect(ssid, password)
        t0 = ticks_ms()
        while not sta.isconnected():
            if ticks_diff(ticks_ms(), t0) > timeout_ms:
                raise RuntimeError("WLAN: timeout")
            if led:
                led.toggle()
            await aio.sleep_ms(200)

    if led:
        led.off()
    return sta

def _disable_ap():
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        ap.active(False)

async def start_server(handler, port: int = 80, backlog: int = 4):
    _disable_ap()
    srv = await aio.start_server(handler, "0.0.0.0", port, backlog=backlog)
    return srv
