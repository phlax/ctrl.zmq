
import asyncio

import zmq
import zmq.asyncio


class ZMQService(object):
    bind = True

    def __init__(self, loop, server_addr):
        self._started = False
        self.loop = loop
        self.server_addr = server_addr
        self.ctx = zmq.asyncio.Context()
        self.sock = self.get_socket(self.ctx)
        if self.bind:
            print("Binding %s" % self)
            self.sock.bind(self.server_addr)
            print("Bound %s" % self)
        else:
            print("Connecting %s" % self)
            self.sock.connect(self.server_addr)

    def __str__(self):
        return (
            '<%s (%s) />'
            % ('.'.join(
                [self.__module__,
                 self.__class__.__name__]),
               self.server_addr))

    def set_socket_options(self, socket):
        return socket

    def get_socket(self, ctx):
        return ctx.socket(getattr(self, 'protocol', zmq.SUB))

    async def run(self, *args):
        asyncio.ensure_future(self.handle(*args))


class ZMQClient(ZMQService):
    bind = False
    wait_on_start = 0

    async def handle(self, command, *args):
        if not self._started:
            self._started = True
            if self.wait_on_start:
                await asyncio.sleep(self.wait_on_start)
        return await getattr(self, 'handle_%s' % command)(*args)
