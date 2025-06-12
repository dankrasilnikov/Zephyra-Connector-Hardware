import uasyncio as asyncio
from machine import Pin, SPI
import libs.max7219

spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)

display = libs.max7219.Matrix8x8(spi, cs, 1)
display.brightness(0)
display.fill(0)
display.show()

_CHECK = [(5,7),(6,6),(7,5),(6,4),(5,3),(4,2),(3,1),(2,0)]
_CROSS = [
    (0,0),(7,7),(1,1),(6,6),(2,2),(5,5),(3,3),(4,4),
    (0,7),(7,0),(1,6),(6,1),(2,5),(5,2),(3,4),(4,3)
]

async def play_check_icon(speed=80, pause=500):
    display.fill(0); display.show()
    for x, y in _CHECK:
        display.pixel(x, y, 1)
        display.show()
        await asyncio.sleep_ms(speed)
    await asyncio.sleep_ms(pause)
    for x, y in _CHECK:
        display.pixel(x, y, 0)
        display.show()
        await asyncio.sleep_ms(speed // 3)

async def play_cross_icon(speed=80, pause=500):
    display.fill(0); display.show()
    for i in range(0, len(_CROSS), 2):
        x1, y1 = _CROSS[i]
        x2, y2 = _CROSS[i+1]
        display.pixel(x1, y1, 1)
        display.pixel(x2, y2, 1)
        display.show()
        await asyncio.sleep_ms(speed)
    await asyncio.sleep_ms(pause)
    for i in range(len(_CROSS)-2, -1, -2):
        x1, y1 = _CROSS[i]
        x2, y2 = _CROSS[i+1]
        display.pixel(x1, y1, 0)
        display.pixel(x2, y2, 0)
        display.show()
        await asyncio.sleep_ms(speed // 2)

async def animations_loop():
    while True:
        await play_check_icon()
        await asyncio.sleep_ms(300)
        await play_cross_icon()
        await asyncio.sleep_ms(300)