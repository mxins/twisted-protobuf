#-*-coding: utf-8 -*-

import sys, os

paths = ('.', '../')

for path in paths:
    _path = os.path.abspath(path)
    if _path not in sys.path:
        sys.path.append(_path)

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

from twisted.internet import reactor
reactor.suggestThreadPoolSize(50)

from twisted.application import internet, service
import loginserver
import config
from base import PbFactory

application = service.Application('Protobuf Messager Server')
_svc = loginserver.LoginService()

_svc.setServiceParent(service.IServiceCollection(application)) #@UndefinedVariable

_factory = PbFactory(_svc)
internet.TCPServer(config.port, _factory).setServiceParent(service.IServiceCollection(application)) #@UndefinedVariable

