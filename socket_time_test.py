import asyncio
import websockets

import datetime
import random


@asyncio.coroutine
def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        yield from websocket.send(now)
        yield from asyncio.sleep(random.random() * 3)


host, port = 'localhost', 5678
start_server = websockets.serve(time, host, port)
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(start_server)
print('Host "%s" listening on port  %i' % (host, port))
event_loop.run_forever()