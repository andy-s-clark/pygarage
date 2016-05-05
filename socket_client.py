import asyncio

import websockets


async def incoming_foo(message):
    print('Message: %s' % message)


async def ws_consumer_handler(websocket, path):
    while True:
        message = await websocket.recv()
        await incoming_foo(message)


event_loop = asyncio.get_event_loop()
ws_server = websockets.serve(ws_consumer_handler, 'localhost', 8765)
event_loop.run_until_complete(ws_server)
event_loop.run_forever()

# def producer(websocket, uri):
#     count = 0
#     while websocket.open:
#         yield from asyncio.sleep(1)
#         count += 1
#         yield from websocket.send(str(count))
#
#
# def consumer():
#     websocket = yield from websockets.connect('ws://localhost:8765/')
#     while websocket.open:
#         count = yield from websocket.recv()
#         print('%s' % count)
#
# start_server = websockets.serve(producer, 'localhost', 8765)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_until_complete(consumer())
# asyncio.get_event_loop().run_forever()