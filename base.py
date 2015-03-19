#-*-coding: utf-8 -*-

from twisted.internet import protocol, reactor, defer
from twisted.protocols import policies
from twisted.application.service import Service
import struct
from twisted.python import failure, log
import time
import login_pb2

class PbProtocol(protocol.Protocol, policies.TimeoutMixin):
    BUFFER = ''
    timeOut = 500
    header_format = 'IH'
    header_length = struct.calcsize(header_format)
    def connectionMade(self):
        self.transport.setTcpKeepAlive(True)
        self.setTimeout(self.timeOut)
        peer = self.transport.getPeer()

        log.msg( 'Connection made. host, port:', peer.host, peer.port)

    def dataReceived(self, data):
        self.resetTimeout()
        self.transport.pauseProducing()
        self.BUFFER += data
        buffer_length = len(self.BUFFER)
        _l = ''
        while (buffer_length >= self.header_length):
            len_pb_data, len_msg_name = struct.unpack(self.header_format, self.BUFFER[:self.header_length])#_bound.ParseFromString(self.BUFFER[:8])
            if len_msg_name:
                if len_msg_name > len(self.BUFFER[self.header_length:]):
                    log.msg( 'not enough buffer for msg name, wait for new data coming ...   ')
                    break
                else:
                    msg_name = struct.unpack('%ds'% len_msg_name,  self.BUFFER[self.header_length:len_msg_name + self.header_length])[0]
                    _func = getattr(self.factory.service, '%s' % msg_name.lower(), None) 
                    _msg =  getattr(login_pb2, msg_name, None)
                    if _func and _msg:
                        _request = getattr(login_pb2, msg_name)()
                        if len_pb_data <= len(self.BUFFER[self.header_length + len_msg_name :]):
                            _request.ParseFromString(self.BUFFER[self.header_length + len_msg_name : self.header_length + len_msg_name + len_pb_data])
                            reactor.callLater(0, _func, self, _request) 
                            self.BUFFER = self.BUFFER[self.header_length + len_msg_name + len_pb_data:]
                            buffer_length = len(self.BUFFER) 
                            continue
                        else:   
                            log.msg( 'not enough buffer for pb_data, waiting for new data coming ... ')
                            break
                    else:
                        log.msg( 'no such message handler. detail:', _func, hasattr(login_pb2, msg_name), repr(self.BUFFER))
                        if self.fromclient:
                            self.transport.loseConnection()
                        else:
                            self.BUFFER = ''

                        return
            else:
                log.msg( 'Un-supported message, no msg_name. detail:', len_msg_name)
                if self.fromclient:
                    self.transport.loseConnection()
                else:
                    self.BUFFER = ''
                return
            
        self.transport.resumeProducing()
        

    def send(self, msg):
        if msg:
            pb_data = msg.SerializeToString()
            _header = struct.pack(self.header_format + '%ds'%len(msg.__class__.__name__), len(pb_data), len(msg.__class__.__name__), msg.__class__.__name__)
            self.transport.write(_header + pb_data)

    def connectionLost(self, reason):
        self.setTimeout(None)

class PbFactory(protocol.ServerFactory):
    protocol = PbProtocol
    connections = 0

    def __init__(self, service):
        self.service = service

    def buildProtocol(self, addr):
        if self.connections <= 5000:
            p = protocol.ServerFactory.buildProtocol(self, addr)
            self.connections += 1
            return p
        else:
            log.msg('[ Too many connecitons ]Refuse connection from:', addr)

    def loseConnection(self, player_id):
        self.connections -= 1

class PbService(Service):
    def startService(self):
        log.msg('%s begin starting...' % self.__class__)

    def stopService(self):
        log.msg('%s is stoping...' % self.__class__)

