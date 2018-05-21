
import aiozmq.rpc


class SubscriptionHandler(aiozmq.rpc.AttrHandler):

    def __init__(self):
        self.connected = False

    @aiozmq.rpc.method
    def service_stopped(self, service: str):
        self.connected = True
        print('STOPPED:', service)


class ZMQSubscriber(object):

    def __init__(self, loop, server_addr):
        self.loop = loop
        self.server_addr = server_addr

    async def handle(self, subscribe, *args):
        await aiozmq.rpc.serve_pubsub(
            SubscriptionHandler(),
            subscribe=subscribe,
            bind=self.server_addr,
            log_exceptions=True)
        return (
            'Subscription (%s) started: %s'
            % (subscribe, self.server_addr))


class ZMQPublisher(object):

    def __init__(self, loop, server_addr):
        self.loop = loop
        self.server_addr = server_addr

    async def handle(self, command, *args):
        return await getattr(self, 'handle_%s' % command)(*args)

    async def handle_service_stopped(self, subscription, service, *args):
        client = await aiozmq.rpc.connect_pubsub(connect=self.server_addr)
        await client.publish(subscription).service_stopped(service)
        return (
            'Published service_stopped:%s (%s) to: %s'
            % (service, subscription, self.server_addr))
