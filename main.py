import uasyncio as asyncio
from sharedUtils.logger          import Logger
from sharedUtils.network_manager import setup_wlan          # async
from utils.command_dispatcher    import handle_request      # async

SSID, PASSWORD = "Igor", "igor_sokolov"
logger = Logger("[PICO] ")
logger.log("Boot…")

async def serve(reader, writer):
    try:
        req = await reader.read(1024)
        req_str = req.decode()

        if req_str.startswith("POST"):
            _, _, body = req_str.partition("\r\n\r\n")
            result  = await handle_request(body)
            logger.log(result)
            logger.log("Request accepted")
            status, payload = "200 OK", "OK"
        else:
            status, payload = "404 Not Found", ""

        resp = f"HTTP/1.0 {status}\r\nContent-Type: text/plain\r\n\r\n{payload}"
        await writer.awrite(resp)
    except Exception as e:
        logger.log("HTTP error:", e)
    finally:
        await writer.aclose()

async def main():
    wlan = await setup_wlan(SSID, PASSWORD)
    ip   = wlan.ifconfig()[0]
    logger.log(f"HTTP server → http://{ip}")

    server = await asyncio.start_server(serve, ip, 80, backlog=4)
    logger.log("Listening…")
    await server.wait_closed()

asyncio.run(main())
