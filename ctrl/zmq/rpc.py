
import aiozmq.rpc


class ServerHandler(aiozmq.rpc.AttrHandler):

    def __init__(self):
        self.connected = False

    @aiozmq.rpc.method
    def stop_service(self, service: str) -> bool:
        self.connected = True
        print('STOP:', service)
        return True


class ZMQRPCServer(object):

    def __init__(self, loop, server_addr):
        self.loop = loop
        self.server_addr = server_addr

    async def handle(self, *args):
        await aiozmq.rpc.serve_rpc(
            ServerHandler(),
            bind=self.server_addr)
        return "Started ZMQ RPC Server: %s" % self.server_addr


class ZMQRPCClient(object):

    def __init__(self, loop, server_addr):
        self.loop = loop
        self.server_addr = server_addr

    async def handle(self, command, *args):
        return await getattr(self, "handle_%s" % command)(*args)

    async def handle_stop_service(self, service, *args):
        print("Connecting to ZMQ RPC server: %s" % self.server_addr)
        client = await aiozmq.rpc.connect_rpc(connect=self.server_addr)
        return (
            'Service stopped: %s' % service
            if await client.call.stop_service(service)
            else 'Something went wrong stopping: %s' % service)
