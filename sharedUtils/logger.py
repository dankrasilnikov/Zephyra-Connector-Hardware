import time

class Logger:
    def __init__(self, PREFIX="[PICO] "):
        self.PREFIX = PREFIX

    def log(self, msg):
        print(f"{time.ticks_ms():>8} ms " + self.PREFIX + f": {msg}")