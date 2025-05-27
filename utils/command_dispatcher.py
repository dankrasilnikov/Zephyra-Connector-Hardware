import ujson
from sharedUtils.servo import Servo

_servo = Servo(pin_num=15)

def handle_request(body_bytes):
    try:
        data = ujson.loads(body_bytes)
    except ValueError:
        return None

    cmd = data.get("command", "").upper()
    if cmd == "OPEN":
        _servo.open()
        return "Jack in, honey. Connector opened."
    elif cmd == "CLOSE":
        _servo.close()
        return "Already leaving? Connector closed."
    else:
        return f"Hey, disappointment (I mean creator). Unknown command: {cmd}"