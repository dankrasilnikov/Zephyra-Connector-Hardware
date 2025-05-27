from machine import PWM, Pin

class Servo:
    def __init__(self, pin_num, min_us=500, max_us=2400, start_angle=90 ,step_deg=1):
        self.pin = Pin(pin_num)
        self.pwm = PWM(self.pin)
        self.pwm.freq(50)
        self.min_us = min_us
        self.max_us = max_us
        self.angle = start_angle
        self.step_deg = step_deg
        self.goto(start_angle)

    def angle_to_duty(self, angle):
        angle = max(0, min(180, angle))
        us = self.min_us + (self.max_us - self.min_us) * angle / 180
        duty = int(us * 65535 / 20_000)
        return duty, int(us)

    def _us_for_angle(self, angle):
        span = self.max_us - self.min_us
        return self.min_us + span * angle // 180

    def goto(self, angle):
        self.angle = max(0, min(180, angle))
        us = self._us_for_angle(self.angle)
        duty = us * 65535 // 20000
        self.pwm.duty_u16(duty)

    def open(self, step=1, delay=0.01):
        self.goto(180)

    def close(self, step=1, delay=0.01):
        self.goto(90)