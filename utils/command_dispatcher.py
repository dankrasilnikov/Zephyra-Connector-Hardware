import ujson, uasyncio as asyncio
from sharedUtils.display  import play_check_icon, play_cross_icon
from sharedUtils.stepper  import Stepper28BYJ48

motor = Stepper28BYJ48(pins=(15, 13, 9, 11), rpm=7)

async def handle_request(body):
    if isinstance(body, bytes):
        try:
            body = body.decode()
        except UnicodeError:
            return "Bad request: undecodable body"

    try:
        data = ujson.loads(body)
    except ValueError:
        return "Bad request: JSON expected"

    cmd = str(data.get("command", "")).strip().upper()

    if cmd == "OPEN":
        t_disp = asyncio.create_task(play_check_icon())
        t_motor = asyncio.create_task(motor.open())
        await t_disp
        await t_motor
        return "Jack in, honey. Connector opened."

    elif cmd == "CLOSE":
        t_disp = asyncio.create_task(play_cross_icon())
        t_motor = asyncio.create_task(motor.close())
        await t_disp
        await t_motor
        return "Already leaving? Connector closed."

    else:
        return f"Hey, disappointment. Unknown command: {cmd}"
