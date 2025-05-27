from sharedUtils.logger import Logger
from sharedUtils.network_manager import setup_wlan, start_server
from utils.command_dispatcher import handle_request

SSID      = "name"
PASSWORD  = "password"

logger = Logger("[PICO] ")
logger.log("Starting up")

wlan = setup_wlan(SSID, PASSWORD)

logger.log("HTTP server → http://" + wlan.ifconfig()[0])

s, addr = start_server(80, True)
logger.log(f"Listening on {addr}")

while True:
    client, addr = s.accept()
    try:
        req = client.recv(1024)
        req_str = req.decode('utf-8')

        if req_str.startswith('POST'):
            head, _, body = req_str.partition('\r\n\r\n')

            response = handle_request(body)

            logger.log(response)

            resp = 'HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nOK'
        else:
            resp = 'HTTP/1.0 404 Not Found\r\n\r\n'
        client.send(resp)
        client.close()
    except Exception as e:
        logger.log("Something wrong with me:", e)
    finally:
        client.close()