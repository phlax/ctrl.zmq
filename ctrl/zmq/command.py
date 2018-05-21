
from zope import interface

from ctrl.command.interfaces import ISubcommand

from .rpc import ZMQRPCClient


@interface.implementer(ISubcommand)
class ZMQSubcommand(object):

    def __init__(self, context):
        self.context = context

    async def handle(self, loop, command, *args):
        return await getattr(self, 'handle_%s' % command)(loop, *args)

    async def handle_rpc(self, loop, server_addr, command, *args):
        client = ZMQRPCClient(loop, server_addr)
        response = await client.handle(command, *args)
        print(response)
