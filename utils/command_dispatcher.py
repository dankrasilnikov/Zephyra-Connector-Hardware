import ujson

from sharedUtils.display import play_check_icon, play_cross_icon
from sharedUtils.stepper import Stepper28BYJ48

motor = Stepper28BYJ48(pins=(15, 13, 9, 11), rpm=8)

def handle_request(body_bytes):
    try:
        data = ujson.loads(body_bytes)
    except ValueError:
        return None

    cmd = data.get("command", "").upper()
    if cmd == "OPEN":
        play_check_icon()
        motor.open()
        return "Jack in, honey. Connector opened."
    elif cmd == "CLOSE":
        play_cross_icon()
        motor.close()
        return "Already leaving? Connector closed."
    else:
        return f"Hey, disappointment (I mean creator). Unknown command: {cmd}"