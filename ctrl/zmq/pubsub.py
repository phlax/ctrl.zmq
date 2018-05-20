
import asyncio

import aiozmq.rpc


class ServerHandler(aiozmq.rpc.AttrHandler):

    def __init__(self):
        self.connected = False

    @aiozmq.rpc.method
    def stop_service(self, service: str) -> bool:
        self.connected = True
        print('STOP:', service)
        return True


class ZMQRPC(object):

    def __init__(self, loop, server_addr):
        self.loop = loop
        self.server_addr = server_addr

    async def start(self):
        print("Starting ctrl-services pub-sub: %s" % self.server_addr)
        handler = ServerHandler()
        await aiozmq.rpc.serve_rpc(
            handler,
            bind=self.server_addr)
        print("SERVE", self.server_addr)


class ZMQSubscriber(object):

    def __init__(self, loop, server_addr):
        self.loop = loop
        self.server_addr = server_addr

    async def start(self):
        print("Connecting to socket server: %s" % self.server_addr)
        client = await aiozmq.rpc.serve_pubsub(connect=self.server_addr)
        while 1:
            pong = await client.publish('ctrl-services').ping()
            if pong:
                print(pong)
                break
            asyncio.sleep(0.1)
        stopped = await client.publish('ctrl-services').stop_service('foo')
        if stopped:
            print('Service stopped')
        else:
            print('Something went wrong')


class ZMQClient(object):

    def __init__(self, loop, server_addr):
        self.loop = loop
        self.server_addr = server_addr

    async def handle(self, command, *args):
        return await getattr(self, "handle_%s" % command)(*args)

    async def handle_stop(self, service, *args):
        print("Connecting to socket server: %s" % self.server_addr)
        client = await aiozmq.rpc.connect_rpc(connect=self.server_addr)
        return (
            'Service stopped'
            if await client.call.stop_service(service)
            else 'Something went wrong')


class ZMQPublisher(object):

    def __init__(self, loop, server_addr):
        self.loop = loop
        self.server_addr = server_addr

    async def handle(self, command, *args):
        return await getattr(self, "handle_%s" % command)(*args)

    async def handle_stop(self, service, *args):
        print("Connecting to socket server: %s" % self.server_addr)
        client = await aiozmq.rpc.connect_pubsub(connect=self.server_addr)
        return (
            'Service stopped'
            if await client.call.stop_service(service)
            else 'Something went wrong')
