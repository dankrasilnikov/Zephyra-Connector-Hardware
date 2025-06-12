from machine import Pin, SPI
import libs.max7219
from time import sleep_ms

spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)

display = libs.max7219.Matrix8x8(spi, cs, 1)
display.brightness(1)
display.fill(0)
display.show()

def play_check_icon():
    display.fill(0)
    display.show()

    check_coords = [
        (0, 5),
        (1, 6),
        (2, 7),
        (3, 6),
        (4, 5),
        (5, 4),
        (6, 3),
        (7, 2)
    ]

    for i in range(len(check_coords)):
        x, y = check_coords[i]
        display.pixel(x, y, 1)
        display.show()
        sleep_ms(80)

    sleep_ms(500)

    for i in range(len(check_coords)):
        x, y = check_coords[i]
        display.pixel(x, y, 0)
        display.show()
        sleep_ms(30)


def play_cross_icon(speed=80):
    display.fill(0)
    display.show()

    cross_coords = [
        (0, 0), (7, 7),
        (1, 1), (6, 6),
        (2, 2), (5, 5),
        (3, 3), (4, 4),
        (0, 7), (7, 0),
        (1, 6), (6, 1),
        (2, 5), (5, 2),
        (3, 4), (4, 3)
    ]

    for i in range(0, len(cross_coords), 2):
        x1, y1 = cross_coords[i]
        x2, y2 = cross_coords[i + 1]
        display.pixel(x1, y1, 1)
        display.pixel(x2, y2, 1)
        display.show()
        sleep_ms(speed)

    sleep_ms(500)

    for i in reversed(range(0, len(cross_coords), 2)):
        x1, y1 = cross_coords[i]
        x2, y2 = cross_coords[i + 1]
        display.pixel(x1, y1, 0)
        display.pixel(x2, y2, 0)
        display.show()
        sleep_ms(speed // 2)