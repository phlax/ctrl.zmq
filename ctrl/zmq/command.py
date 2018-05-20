
from zope import interface

from ctrl.command.interfaces import ISubcommand


@interface.implementer(ISubcommand)
class ZMQSubcommand(object):

    def __init__(self, context):
        self.context = context
