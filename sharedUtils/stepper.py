from machine import Pin
from time import sleep_ms

class Stepper28BYJ48:
    _seq = (
        (1,0,0,0),
        (1,1,0,0),
        (0,1,0,0),
        (0,1,1,0),
        (0,0,1,0),
        (0,0,1,1),
        (0,0,0,1),
        (1,0,0,1),
    )

    def __init__(self, pins, rpm=15):
        if len(pins) != 4:
            raise ValueError("Нужно ровно 4 вывода GPIO")

        self.coils = [Pin(p, Pin.OUT) for p in pins]
        self.set_rpm(rpm)
        self._step = 0
        self._position = 0

    def _write_seq(self):
        pattern = self._seq[self._step]
        for coil, level in zip(self.coils, pattern):
            coil.value(level)

    def _do_steps(self, n):
        direction = 1 if n > 0 else -1
        for _ in range(abs(n)):
            self._step = (self._step + direction) % 8
            self._position += direction
            self._write_seq()
            sleep_ms(self._delay_ms)

    def set_rpm(self, rpm):
        self._delay_ms = int((60_000 / (4096 * rpm)) + 0.5)

    def step(self, n):
        self._do_steps(n)

    def turn_deg(self, deg):
        steps = int(deg * 4096 / 360)
        self._do_steps(steps)

    def goto(self, angle):
        angle = max(0, min(180, angle))
        target = int(angle * 4096 / 360)
        delta = target - (self._position % 4096)
        self._do_steps(delta)

    def open(self):
        self.turn_deg(-90)

    def close(self):
        self.turn_deg(90)


