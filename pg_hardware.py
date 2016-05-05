import asyncio

import datetime
import random
import websockets


class PGHardware(object):

    def __init__(self, _event_loop, host='localhost', port=5678):
        self.__connected = set()
        ws_server = websockets.serve(self.web_sockets_handler, host, port)
        _event_loop.run_until_complete(ws_server)
        print('Host "%s" listening on port  %i' % (host, port))

    @asyncio.coroutine
    def consumer(self, message):
        print('Message: %s' % message)

    @asyncio.coroutine
    def producer(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        yield from asyncio.sleep(2)
        return now

    @asyncio.coroutine
    def web_sockets_handler(self, websocket, path):
        self.__connected.add(websocket)
        print('Connected: %s' % websocket)
        try:
            yield from asyncio.wait([ws.send('client connected') for ws in self.__connected])
            while True:
                listener_task = asyncio.ensure_future(websocket.recv())
                producer_task = asyncio.ensure_future(self.producer())
                done, pending = yield from asyncio.wait(
                    [listener_task, producer_task],
                    return_when=asyncio.FIRST_COMPLETED)

                if listener_task in done:
                    message = listener_task.result()
                    yield from self.consumer(message)
                else:
                    listener_task.cancel()

                if producer_task in done:
                    message = producer_task.result()
                    yield from websocket.send(message)
                else:
                    producer_task.cancel()
        except websockets.exceptions.ConnectionClosed:
            print('Connection %s closed' % websocket)
        finally:
            self.__connected.remove(websocket)


if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'port': 5678
    }
    event_loop = asyncio.get_event_loop()
    pg_hardware = PGHardware(event_loop, **config)
    event_loop.run_forever()
