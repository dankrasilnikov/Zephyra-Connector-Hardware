import uasyncio as asyncio
from machine import Pin

class Stepper28BYJ48:
    _SEQ = (
        (1,0,0,0), (1,1,0,0), (0,1,0,0), (0,1,1,0),
        (0,0,1,0), (0,0,1,1), (0,0,0,1), (1,0,0,1),
    )

    def __init__(self, pins, rpm=15):
        if len(pins) != 4:
            raise ValueError("Нужно ровно 4 вывода GPIO")

        self.coils     = [Pin(p, Pin.OUT) for p in pins]
        self.set_rpm(rpm)
        self._step     = 0
        self._pos      = 0
        self._lock     = asyncio.Lock()

    def _write_seq(self):
        patt = self._SEQ[self._step]
        for coil, lvl in zip(self.coils, patt):
            coil.value(lvl)

    async def _do_steps(self, n):
        async with self._lock:
            direction = 1 if n > 0 else -1
            for _ in range(abs(n)):
                self._step = (self._step + direction) & 7
                self._pos  += direction
                self._write_seq()
                await asyncio.sleep_ms(self._delay_ms)

    def set_rpm(self, rpm):
        self._delay_ms = max(1, int(60_000 / (4096 * rpm)))

    async def step(self, n):
        await self._do_steps(n)

    async def turn_deg(self, deg):
        await self._do_steps(int(deg * 4096 / 360))

    async def goto(self, angle):
        angle  = max(0, min(180, angle))
        target = int(angle * 4096 / 360)
        delta  = target - (self._pos & 0xFFF)
        await self._do_steps(delta)

    async def open(self):   await self.turn_deg(-90)
    async def close(self):  await self.turn_deg( 90)
