
from zope import component

from ctrl.core.interfaces import ICtrlExtension
from .extension import CtrlZMQExtension


# register the extension
component.provideUtility(
    CtrlZMQExtension(),
    ICtrlExtension,
    'zmq')
