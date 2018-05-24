
from zope.interface import Interface


class IZMQRPCServer(Interface):
    pass


class IZMQRPCReply(Interface):

    async def respond(socket, recv):
        pass
