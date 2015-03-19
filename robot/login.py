#-*-coding: utf-8 -*-

import sys, os
paths = ('.', '../')
import struct
for path in paths:
    _path = os.path.abspath(path)
    if _path not in sys.path: 
        sys.path.append(_path)

from base import PbService, PbProtocol, PbFactory
import time
from twisted.internet import reactor, defer, protocol
from twisted.python import failure, log
import login_pb2
import config

class LoginRobot(PbService):
    def __init__(self, name):
         self.name = name
         self.Login(name)

    @defer.inlineCallbacks  
    def Login(self, name):
        log.msg('login request, name:%s '% name)
        try:
            LOGIN_connector = protocol.ClientCreator(reactor, PbProtocol )
            self.p = yield LOGIN_connector.connectTCP(config.ip, config.port)
            _factory = PbFactory(self)
            self.p.factory = _factory
        except Exception, e:
            self.p = None
            log.msg( 'Login... connect login error:', e ,self.name)
            reactor.callLater(10, self.Login, name)			
            defer.returnValue(None) 
        _msg = login_pb2.LoginRequest()
        _msg.user_name = name
        self.p.send(_msg)
     
    def loginresponse(self, p, request):
        result = request.result
        user_name = request.user_name
        log.msg('loginresponse, result:%s, user_name:%s'% (result, user_name))

if __name__ == '__main__':
    LoginRobot("s10009")
    reactor.run()
        
